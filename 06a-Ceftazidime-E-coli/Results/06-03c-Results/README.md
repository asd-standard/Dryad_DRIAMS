# 06-03c results — Ceftazidime species-masked pipeline

Two runs of the `06-03c` species-masked pipeline, both produced on 2026-07-20.
See `../../RUNS.md` for the full inventory; docs: `06a/federated` and
`06a/analysis`.

- `results/` — **canonical run** (~12:44). Mask candidates
  {`union`, `majority`, `persite`}; winner `majority`. Pooled BalAcc:
  Centr unmasked 0.615 / union 0.625 / majority 0.616 / persite 0.655;
  FedAvg MLP 0.641 (r7), FedProx μ=0.1 0.691 (r16), FedLR 0.651 (r30),
  FedRF 0.500 (r2); cross-site MLP 0.552.
  Archive: `results-20261010T130118Z-1-001.zip`.
- `run1-mask-none/` — **earlier run** (04:55), used as the docs' robustness
  check. Mask candidates still included `none` (removed later the same day in
  commit `fc8da15`); winner `none`. Pooled BalAcc: Centr 0.659;
  FedAvg 0.678, FedProx 0.700, FedLR 0.675, FedRF 0.500; cross-site 0.553.
  Archive: `results-20261010T130223Z-1-001.zip`.

Provenance: pre-October-2026 FedProx fix; federated rows pending re-run.
Removed on 2026-10-15: an empty zip (`results-…130159Z`) and a byte-identical
copy of `run1-mask-none/results/convergence.pdf` (the former `02-Results`).
