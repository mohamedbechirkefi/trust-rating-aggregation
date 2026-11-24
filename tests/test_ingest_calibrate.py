# SPDX-License-Identifier: LicenseRef-TRUST-NC-Research-1.0
"""Ingestion on a synthetic fixture and calibration parameter recovery on simulated counts."""

from pathlib import Path

import numpy as np
import pytest

from trust.calibrate import (
    fit_negbin,
    fit_quality,
    observed_item_star_shares,
    predicted_star_shares,
    split_movies,
)
from trust.ingest import IngestError, ingest
from trust.model import rating_probabilities

FIX = Path(__file__).parent / "fixtures" / "movielens"


def _fixture():
    return ingest((FIX / "movies.dat").read_bytes(), (FIX / "ratings.dat").read_bytes())


def test_ingest_counts_and_exclusions():
    d = _fixture()
    assert d.movie_ids.tolist() == [1, 2, 3, 4]
    # movie 1: 5, 4, 5 (user 10's repeat and the out-of-range 9 excluded)
    assert d.counts[0].tolist() == [0, 0, 0, 1, 2]
    assert d.counts[1].tolist() == [1, 0, 1, 0, 1]
    assert d.counts[2].tolist() == [0, 2, 0, 0, 0]
    assert d.counts[3].tolist() == [0, 0, 0, 0, 0]
    r = d.report
    assert r["rating_rows"] == 12
    assert r["rating_rows_invalid"] == 2  # malformed row, rating 9
    assert r["rating_rows_unknown_movie"] == 1
    assert r["rating_rows_duplicate_pair"] == 1
    assert r["ratings_kept"] == 8
    assert r["n_movies_unrated"] == 1
    assert r["n_users"] == 5  # user 14 rated only an unknown movie
    assert sum(r["star_shares"]) == pytest.approx(1.0)


def test_ingest_is_pure_and_deterministic():
    a, b = _fixture(), _fixture()
    assert np.array_equal(a.counts, b.counts) and a.report == b.report


def test_ingest_rejects_empty_catalogue():
    with pytest.raises(IngestError):
        ingest(b"garbage\n", b"")


def test_ingest_output_has_no_user_information():
    d = _fixture()
    assert d.counts.shape == (4, 5)
    assert not any("user" in k and k != "n_users" for k in d.report)


def test_split_is_deterministic_disjoint_and_complete():
    ids = np.arange(1, 102)
    f1, h1 = split_movies(ids)
    f2, h2 = split_movies(ids[::-1])
    assert np.array_equal(f1, f2) and np.array_equal(h1, h2)
    assert f1.size == 50 and h1.size == 51
    assert not set(f1) & set(h1) and set(f1) | set(h1) == set(ids)


def test_negbin_recovers_parameters():
    rng = np.random.default_rng(1)
    mean, r = 40.0, 0.7
    n = rng.negative_binomial(r, r / (r + mean), size=20000)
    fit = fit_negbin(n)
    assert fit["converged"]
    assert fit["mean"] == pytest.approx(mean, rel=0.05)
    assert fit["r"] == pytest.approx(r, rel=0.05)


def _simulate_counts(rng, a, b, sigma, m, nmean):
    mu = 1 + 4 * rng.beta(a, b, size=m)
    n = rng.poisson(nmean, size=m) + 1
    p = rating_probabilities(mu, sigma)
    return np.stack([rng.multinomial(k, pi) for k, pi in zip(n, p)])


def test_quality_fit_recovers_parameters():
    rng = np.random.default_rng(2)
    c = _simulate_counts(rng, 3.0, 2.0, 0.8, 1500, 30)
    fit = fit_quality(c, n_grid=1000)
    assert fit["a"] == pytest.approx(3.0, rel=0.15)
    assert fit["b"] == pytest.approx(2.0, rel=0.15)
    assert fit["sigma"] == pytest.approx(0.8, rel=0.08)
    assert len(fit["starts"]) == 3


def test_predicted_shares_match_simulated_item_shares():
    rng = np.random.default_rng(3)
    c = _simulate_counts(rng, 3.0, 2.0, 0.8, 4000, 20)
    pred = predicted_star_shares(3.0, 2.0, 0.8)
    assert pred.sum() == pytest.approx(1.0)
    assert np.allclose(observed_item_star_shares(c), pred, atol=0.01)
