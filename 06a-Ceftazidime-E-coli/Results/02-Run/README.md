# 02-Run — basic Ceftazidime FL (E. coli only)

Produced 2026-07-20 02:07 by the basic `06-03a`/`06-03b` lineage: four FL
strategies (FedAvg MLP, FedProx μ=0.5, FedLR, FedRF) plus centralized and
cross-site baselines; no species masking; 30 rounds.

Pooled BalAcc: Centralized MLP 0.683 (AUC 0.744); Centralized RF 0.660;
FedAvg 0.654 (r11); FedProx μ=0.5 0.562 (r28); FedLR 0.509 (r19);
FedRF 0.601 (r2); cross-site MLP 0.538.

Superseded by the `06-03c` species-masked runs; kept as the docs' basic
E. coli comparison (`06a/analysis`). Archive:
`results-20261010T130000Z-1-001.zip`.
