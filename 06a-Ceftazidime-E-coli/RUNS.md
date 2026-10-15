# 06a — Ceftazidime × *E. coli*: results inventory

Overview of the result sets produced by the 06a notebooks. Everything under
`Results/` is local-only (the repository tracks notebooks and docs, not data).
All federated numbers below were produced **before the October 2026 FedProx
proximal-term fix** (commit `b1a2e09`); the federated rows in the docs are
expected to be refreshed after a re-run.

| Result set | Date | Notebook | Protocol | Pooled BalAcc (key rows) | Status |
|---|---|---|---|---|---|
| `Results/06-03c-Results/results/` | 2026-07-20 ~12:44 | `06-03c-…-Species-Masked-Ceftazidime-Federated.ipynb` | species-masked, winner `majority`, 30 rounds, μ=0.1 | Centr 0.615 · FedAvg 0.641 · **FedProx 0.691** · FedLR 0.651 · FedRF 0.500 · cross-site 0.552 | **canonical** (docs `06a/federated`) |
| `Results/06-03c-Results/run1-mask-none/` | 2026-07-20 04:55 | same notebook, earlier revision | same pipeline; mask candidates still included `none` → winner `none` | Centr 0.659 · FedAvg 0.678 · FedProx 0.700 · FedLR 0.675 · FedRF 0.500 · cross-site 0.553 | **robustness run** (docs `06a/federated`, "Robustness") |
| `Results/02-Run/` | 2026-07-20 02:07 | `06-03a`/`06-03b` lineage | basic FL (E. coli only), no masks, μ=0.5 | Centr 0.683 · FedAvg 0.654 · FedProx(μ=0.5) 0.562 · FedLR 0.509 · FedRF 0.601 · cross-site 0.538 | superseded baseline (docs `06a/analysis`) |
| `Results/06-02-Runs/` | 2026-07 | `06-02-…-Aggregated-Iterative.ipynb` | non-federated iterative runs | see `summary.csv` | auxiliary (docs `06a/analysis`) |
| `Results/06-03c-loss-test/` | 2026-07-20 15:02 | `06-03c` (loss-capture test) | partial FedProx output only | — | test fragment (re-homed from 06b on 2026-10-15) |

The two 06-03c runs were produced on the same day while the notebook was being
revised: commit `fc8da15` (16:53) removed the `none` strategy from
`MASK_STRATEGIES`, and run 2 was executed with the later candidate set. The
docs' "Robustness" section reads the disagreement on the mask winner
(`majority` vs `none`) as weak evidence for mask selection.

Notes (2026-10-15 reorder):
- renamed `Results/06-03-c-Reulsts/` → `Results/06-03c-Results/` (typo) and
  `01_Results/` → `run1-mask-none/`; docs paths updated accordingly;
- removed: empty `Results/01-Run/` (folder + empty zip), empty zip
  `results-…130159Z`, and a stray copy of run 1's `convergence.pdf`
  (the former `02-Results`; byte-identical to the kept file);
- run archives are kept next to the extracted folders:
  `results-…130118Z` → run 2, `results-…130223Z` → run 1;
  `02-Run` and `06-02-Runs` archives sit at the `Results/` level.
