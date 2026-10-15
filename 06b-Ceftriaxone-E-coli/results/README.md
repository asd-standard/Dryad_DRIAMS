# results/ — canonical 06b run (all species)

Produced 2026-07-19 by `06-03c-Species-Masked-Ceftriaxone-Federated.ipynb`
(winning mask `none`, 30 rounds, μ=0.1). This is the run behind the docs page
`06b/federated` and Figure 7 of the report: `convergence.pdf` here is the
2-panel figure rendered as
`docs/_static/06b-Ceftriaxone-E-coli/06b_federated_convergence.svg`.

Pooled BalAcc: Centralized MLP unmasked 0.761 (AUC 0.826) / union 0.747 /
majority 0.760 / persite 0.742; FedAvg MLP 0.745 (r12); FedProx μ=0.1 0.746
(r19); FedLR 0.710 (r30); FedRF 0.500 (r2, threshold collapse); cross-site MLP
0.608. Archive: `../results-20260721T064626Z-1-001.zip` (12 files, includes
the Jul-20 loss files).

⚠️ All species, not E. coli-only (see `../RUNS.md`). Numbers predate the
October-2026 FedProx fix — federated rows pending refresh.
