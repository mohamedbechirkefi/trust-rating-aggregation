<!-- SPDX-License-Identifier: LicenseRef-TRUST-NC-Research-1.0 -->
# experiments/

Runnable configurations (JSON, schema `src/trust/schemas/config-v1.json`).

| File | Label | Purpose |
|---|---|---|
| `smoke.json` | exploratory | Smoke matrix of `research/protocol.md` section 7 (N = 50, nu in {3, 30}, 3 seeds) |
| `pilot-exp001-corners.json` | exploratory | Variance and runtime pilot, 4 corner cells of EXP-001, N = 200, 10 seeds, seed namespace 901 |
| `pilot-exp002-lambda.json` | exploratory | Variance pilot of the EXP-002 lambda contrast, N = 200, 10 seeds, seed namespace 902 |
| `EXP-001.json`, `EXP-002.json` | confirmatory | Full matrices; `run` refuses them until the owner freezes the protocol |
| `EXP-003-S1-min1.json`, `EXP-003-S1-min5.json`, `EXP-003-S2.json`, `EXP-003-S3.json`, `EXP-003-S4.json` | confirmatory | EXP-003 sensitivity sub-analyses; refused until frozen |

The pilot seed namespaces (901, 902) are disjoint from the confirmatory ones (1, 2), so no confirmatory catalogue has been generated. Protocols and reports live in `research/experiments/`.
