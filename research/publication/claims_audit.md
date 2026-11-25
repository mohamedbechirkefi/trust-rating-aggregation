<!-- SPDX-License-Identifier: LicenseRef-TRUST-NC-Research-1.0 -->
# Claims audit checklist (M4)

Status: done at M4, 2026-11-25 (AI assistant; internal quality control). Details in `research/publication/evidence_audit.md`.

- [x] Every row of `research/claims_register.csv` has an evidence path that exists, or a source with its access status (26 rows: CLM-001 to CLM-018 measured or exploratory, CLM-019 to CLM-026 external).
- [x] Every number in the manuscript, supplement, reports, claims register, limitations and review notes matches the raw results: in-memory re-analysis 0 differences; 236 printed intervals traced, 0 unmatched. Demo and articles do not exist yet (M5).
- [x] Every simulated claim is labelled simulated and stays within the model's assumptions; exploratory claims (CLM-012 to CLM-015) are labelled exploratory.
- [x] No claim about real product quality, fraudulent reviews or commercial platform internals.
- [x] Null, negative and failed results are reported: H1b contradicted, H1c not supported, lambda null, S2 and S4 invalidation criteria met, S3 non-diagnostic; 0 failed runs.
- [x] A second review pass challenged the preferred hypothesis: `research/publication/review_pass_2.md` (AI assistant, 2026-11-25). The owner has not yet reviewed it.
