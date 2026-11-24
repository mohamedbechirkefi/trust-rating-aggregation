# SPDX-License-Identifier: LicenseRef-TRUST-NC-Research-1.0
"""Exploratory calibration fit on MovieLens 1M (protocol section 13.1; journal JRN-0005).

    PYTHONPATH=src .venv/bin/python scripts/fit_movielens.py

Reads data/raw/ml-1m/{movies,ratings}.dat (git-ignored), writes the aggregate fit record
data/calibration/movielens-1m-fit.json (parameters and summary counts only, no rows).
"""

from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np

from trust.calibrate import (
    fit_negbin,
    fit_quality,
    nb_loglik,
    nb_quantiles,
    observed_item_star_shares,
    predicted_star_shares,
    quality_loglik,
    split_movies,
)
from trust.ingest import ingest
from trust.provenance import git_revision, sha256_file

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "ml-1m"
OUT = ROOT / "data" / "calibration" / "movielens-1m-fit.json"
QS = (0.1, 0.25, 0.5, 0.75, 0.9)


def main() -> int:
    t0 = time.perf_counter()
    git = git_revision(ROOT)
    data = ingest((RAW / "movies.dat").read_bytes(), (RAW / "ratings.dat").read_bytes())
    f_ids, h_ids = split_movies(data.movie_ids)
    in_f = np.isin(data.movie_ids, f_ids)
    cf, ch = data.counts[in_f], data.counts[~in_f]
    nbf = fit_negbin(cf.sum(axis=1))
    q = fit_quality(cf)
    rated_h = ch[ch.sum(axis=1) >= 1]
    check = {
        "n_movies": int(ch.shape[0]),
        "n_rated": int(rated_h.shape[0]),
        "star_shares_observed_item_mean": observed_item_star_shares(ch).tolist(),
        "star_shares_predicted": predicted_star_shares(q["a"], q["b"], q["sigma"]).tolist(),
        "count_quantiles": [float(x) for x in np.quantile(ch.sum(axis=1), QS)],
        "count_quantiles_nb_predicted": nb_quantiles(nbf["mean"], nbf["r"], QS),
        "count_mean": float(ch.sum(axis=1).mean()),
        "nb_loglik_per_movie": nb_loglik(ch.sum(axis=1), nbf["mean"], nbf["r"]) / ch.shape[0],
        "quality_loglik_per_rated_movie": quality_loglik(rated_h, q["a"], q["b"], q["sigma"]) / rated_h.shape[0],
        "quality_loglik_per_rated_movie_planning_beta42": {
            str(s): quality_loglik(rated_h, 4.0, 2.0, s) / rated_h.shape[0] for s in (0.5, 1.0, 1.5)
        },
    }
    rec = {
        "kind": "TRUST calibration fit (exploratory, JRN-0005)",
        "protocol_section": "research/protocol.md section 13.1",
        "data": {
            "dataset": "MovieLens 1M",
            "ratings_sha256": sha256_file(RAW / "ratings.dat"),
            "movies_sha256": sha256_file(RAW / "movies.dat"),
        },
        "code_revision": git,
        "ingest_report": data.report,
        "split": {"seed": [20261124, 990], "n_fit": int(cf.shape[0]), "n_check": int(ch.shape[0])},
        "fit_negbin": nbf,
        "fit_quality": q,
        "fitted_values_for_configs": {
            "nb_dispersion": round(nbf["r"], 4),
            "quality": ["beta", round(q["a"], 4), round(q["b"], 4)],
            "sigma_hat_reference_only": round(q["sigma"], 4),
        },
        "check_split_H": check,
        "runtime_s": time.perf_counter() - t0,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(rec, indent=1) + "\n")
    print(json.dumps(rec, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
