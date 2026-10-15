# 06-Ceftriaxone-E-coli/ — z-run model weights

Backup of per-round federated model weights (no result CSVs) from the 06b
runs:

- `06-03b-Ceftriaxone-E-coli-Federated-z-Runs/03-Run/` — Jul 17:
  `fedavg_lr`, `fedavg_mlp`, `fedprox_mlp_mu0.5`
- `06-03b-…-z-Runs/04-Run/` — Jul 17: `fedavg_lr`, `fedavg_mlp`,
  `fedprox_mlp_mu0.1`, `fedrf`
- `06-03c-Ceftriaxone-Federated-z-Runs/01-Run/` — Jul 19 + Sep 17:
  `fedprox_mlp_mu0.1_none` (a later re-run wrote additional rounds into the
  same folder) + `rf_species_models/` (site A)
- `06-03c-…-z-Runs/02-Run/` — Jul: `fedprox_mlp_mu0.1_majority`

The sibling 2.1 GB zip `../06-Ceftriaxone-E-coli-20261010T130325Z-1-003.zip`
is a full backup of this folder (redundant with the extracted tree; candidate
for removal).
