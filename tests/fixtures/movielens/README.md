<!-- SPDX-License-Identifier: LicenseRef-TRUST-NC-Research-1.0 -->
# Synthetic MovieLens-format fixture

Hand-written synthetic rows in the MovieLens 1M schema (`::`-separated). No row comes from
MovieLens. Titles are invented. The rows deliberately include one malformed row, one rating out
of range, one rating of an unknown movie, one repeated (user, movie) pair and one unrated movie,
so that every exclusion counter of `trust.ingest` is exercised.
