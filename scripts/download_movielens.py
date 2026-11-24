# SPDX-License-Identifier: LicenseRef-TRUST-NC-Research-1.0
"""Download MovieLens 1M (GroupLens) into data/raw/ and record its provenance.

MovieLens may be used for research but may not be redistributed (README usage licence), so the
files are git-ignored and never committed. This script records the URL, access date, size and
SHA-256 in data/raw/download_record.json (also git-ignored); the committed copy of those values
lives in data/manifest.json.

    python scripts/download_movielens.py            # download if missing, then verify
    python scripts/download_movielens.py --verify   # verify only; exit 1 on mismatch

The expected SHA-256 is pinned below once known; a mismatch stops the study (the calibration is
defined on this exact file).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import urllib.request
import zipfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
URL = "https://files.grouplens.org/datasets/movielens/ml-1m.zip"
README_URL = "https://files.grouplens.org/datasets/movielens/ml-1m-README.txt"
ZIP = RAW / "ml-1m.zip"
EXPECTED_SHA256 = "a6898adb50b9ca05aa231689da44c217cb524e7ebd39d264c56e2832f2c54e20"  # first download 2026-11-24
MAX_BYTES = 50 * 1024 * 1024  # the published file is about 6 MB; refuse anything far larger
MEMBERS = ("ml-1m/ratings.dat", "ml-1m/movies.dat", "ml-1m/README")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def download(url: str, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_suffix(dest.suffix + ".part")
    with urllib.request.urlopen(url, timeout=120) as resp, tmp.open("wb") as out:
        total = 0
        while chunk := resp.read(1 << 20):
            total += len(chunk)
            if total > MAX_BYTES:
                tmp.unlink()
                raise SystemExit(f"refused: {url} exceeds {MAX_BYTES} bytes")
            out.write(chunk)
    tmp.replace(dest)


def extract(zip_path: Path) -> None:
    """Extract only the files the study reads (users.dat, with demographics, is not extracted)."""
    with zipfile.ZipFile(zip_path) as zf:
        for name in MEMBERS:
            target = RAW / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(zf.read(name))


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--verify", action="store_true", help="verify the existing file only")
    a = p.parse_args(argv)
    if not a.verify and not ZIP.exists():
        download(URL, ZIP)
        record = {
            "dataset": "MovieLens 1M (GroupLens)",
            "url": URL,
            "readme_url": README_URL,
            "accessed_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        }
    else:
        rec_path = RAW / "download_record.json"
        record = json.loads(rec_path.read_text()) if rec_path.exists() else {"url": URL}
    if not ZIP.exists():
        print("missing: data/raw/ml-1m.zip; run without --verify", file=sys.stderr)
        return 1
    digest = sha256(ZIP)
    record.update({"file": "data/raw/ml-1m.zip", "size_bytes": ZIP.stat().st_size, "sha256": digest})
    if EXPECTED_SHA256 is not None and digest != EXPECTED_SHA256:
        print(f"SHA-256 mismatch: got {digest}, expected {EXPECTED_SHA256}", file=sys.stderr)
        return 1
    extract(ZIP)
    record["extracted"] = {m: sha256(RAW / m) for m in MEMBERS}
    (RAW / "download_record.json").write_text(json.dumps(record, indent=1, sort_keys=True) + "\n")
    print(json.dumps(record, indent=1, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
