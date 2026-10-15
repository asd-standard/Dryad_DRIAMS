# results_e_coli_only/ — Ceftriaxone E. coli-only run

Produced 2026-07-17 by the `06-03a`/`06-03b` lineage, restricted to *E. coli*
spectra (FedProx μ=0.5, no species masking). Used in the docs as the
non-federated E. coli-only reference and in the Ceftazidime/Ceftriaxone
comparison (`06b/analysis`).

Pooled BalAcc: Centralized MLP 0.670 (AUC 0.750); Centralized RF 0.702;
FedAvg 0.680 (r4); FedProx μ=0.5 0.677 (r11); FedLR 0.523 (r24); FedRF 0.677
(r2); cross-site MLP 0.591. Archive: `../results-20260718T081728Z-1-001.zip`.
