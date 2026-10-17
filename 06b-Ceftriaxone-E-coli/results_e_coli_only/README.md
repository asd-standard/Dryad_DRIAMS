# results_e_coli_only/ — Ceftriaxone E. coli-only run

Produced 2026-07-17 by the `06-03a`/`06-03b` lineage, restricted to *E. coli*
spectra (FedProx μ=0.5, no species masking). Used in the docs as the
non-federated E. coli-only reference and in the Ceftazidime/Ceftriaxone
comparison (`06b/analysis`).

**2026-10-17 — FedLR re-run (fixed protocol).** The FedLR arm was re-run with
8 SAGA iterations per round (instead of 1) and per-site worst-site `C` and
decision threshold, same 30 rounds and splits:
`06-03b-Re-Run-lr-Ceftriaxone-E-coli-FIXED.ipynb` (archived copy in
`results/rerun_lr_notebook.ipynb`). FedLR moves from 0.523 (r24) to
**0.698 (r30, AUC 0.761)** — the best federated strategy of this run, still
rising at round 30. The other rows are unchanged.

Pooled BalAcc: Centralized MLP 0.670 (AUC 0.750); Centralized RF 0.702;
FedAvg 0.680 (r4); FedProx μ=0.5 0.677 (r11); FedLR 0.698 (r30, re-run
2026-10-17; previously 0.523 at r24); FedRF 0.677 (r2); cross-site MLP 0.591.
Archive: `../results-20260718T081728Z-1-001.zip` (original 2026-07-17 run).
