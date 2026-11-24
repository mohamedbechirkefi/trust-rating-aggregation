# SPDX-License-Identifier: LicenseRef-TRUST-NC-Research-1.0
"""Ingestion of MovieLens 1M raw files into per-movie star counts (protocol section 13.1).

Pure functions of the raw bytes: no I/O, no randomness. The output holds no user information.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
from numpy.typing import NDArray

SEP = "::"
ENCODING = "latin-1"  # movies.dat is ISO-8859-1


class IngestError(ValueError):
    """Raised when a raw file cannot be used at all (for example an empty catalogue)."""


@dataclass(frozen=True)
class Ingested:
    movie_ids: NDArray[np.int64]  # catalogue movie ids, ascending
    counts: NDArray[np.int64]  # shape (M, 5); counts[i, k-1] = ratings of star k for movie_ids[i]
    report: dict = field(default_factory=dict)  # schema, exclusion and missingness counts

    @property
    def n(self) -> NDArray[np.int64]:
        return self.counts.sum(axis=1)


def _is_int(s: str) -> bool:
    return s.isdigit()


def parse_movies(raw: bytes) -> tuple[NDArray[np.int64], dict]:
    """movies.dat rows 'MovieID::Title::Genres'. Returns sorted unique ids and counts."""
    text = raw.decode(ENCODING)
    ids, bad, dup = [], 0, 0
    seen: set[int] = set()
    for line in text.splitlines():
        if not line.strip():
            continue
        parts = line.split(SEP)
        if len(parts) != 3 or not _is_int(parts[0]) or int(parts[0]) < 1:
            bad += 1
            continue
        mid = int(parts[0])
        if mid in seen:
            dup += 1
            continue
        seen.add(mid)
        ids.append(mid)
    if not ids:
        raise IngestError("movies.dat holds no valid movie")
    return np.asarray(sorted(ids), dtype=np.int64), {"movie_rows_invalid": bad, "movie_rows_duplicate": dup}


def ingest(movies_raw: bytes, ratings_raw: bytes) -> Ingested:
    """Validate ratings.dat rows 'UserID::MovieID::Rating::Timestamp' and count stars per movie.

    Exclusions (counted, never silent): rows failing the schema; ratings of movies not in the
    catalogue; repeated (user, movie) pairs beyond the first row.
    """
    movie_ids, rep = parse_movies(movies_raw)
    index = {int(m): i for i, m in enumerate(movie_ids)}
    counts = np.zeros((movie_ids.size, 5), dtype=np.int64)
    n_rows = bad = unknown = dup = 0
    seen: set[tuple[int, int]] = set()
    users: set[int] = set()
    for line in ratings_raw.decode("ascii", errors="replace").splitlines():
        if not line.strip():
            continue
        n_rows += 1
        parts = line.split(SEP)
        if len(parts) != 4 or not all(_is_int(p) for p in parts):
            bad += 1
            continue
        uid, mid, r, _ts = (int(p) for p in parts)
        if uid < 1 or mid < 1 or not 1 <= r <= 5:
            bad += 1
            continue
        if mid not in index:
            unknown += 1
            continue
        if (uid, mid) in seen:
            dup += 1
            continue
        seen.add((uid, mid))
        users.add(uid)
        counts[index[mid], r - 1] += 1
    n = counts.sum(axis=1)
    rep.update(
        {
            "rating_rows": n_rows,
            "rating_rows_invalid": bad,
            "rating_rows_unknown_movie": unknown,
            "rating_rows_duplicate_pair": dup,
            "ratings_kept": int(n.sum()),
            "n_users": len(users),
            "n_movies": int(movie_ids.size),
            "n_movies_unrated": int((n == 0).sum()),
            "share_movies_unrated": float((n == 0).mean()),
            "star_shares": [float(x) for x in counts.sum(axis=0) / max(int(n.sum()), 1)],
        }
    )
    return Ingested(movie_ids=movie_ids, counts=counts, report=rep)
