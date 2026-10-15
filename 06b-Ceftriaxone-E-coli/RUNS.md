# 06b — Ceftriaxone: results inventory

Result sets produced by the 06b notebooks. ⚠️ The species-masked pipeline runs
on **all species** (no E. coli filter), despite the folder name: *E. coli* is
only the target species for the `majority` mask. Everything under the result
folders is local-only. The federated numbers in the docs still come from the
July run and are **pending refresh** after the September/October protocol
fixes.

| Result set | Date | Notebook | Protocol | Pooled BalAcc (key rows) | Status |
|---|---|---|---|---|---|
| `results/` | 2026-07-19 | `06-03c-…-Species-Masked-Ceftriaxone-Federated.ipynb` | species-masked, winner `none`, 30 rounds, μ=0.1 | Centr 0.761 · FedAvg 0.745 · **FedProx 0.746** · FedLR 0.710 · FedRF 0.500 · cross-site 0.608 | **canonical** (docs `06b/federated`, report Fig. 7) |
| `results_e_coli_only/` | 2026-07-17 | `06-03a`/`06-03b` lineage | E. coli only, μ=0.5, no masks | Centr 0.670 · RF 0.702 · FedAvg 0.680 · FedProx(μ=0.5) 0.677 · FedLR 0.523 · FedRF 0.677 · cross-site 0.591 | baseline (docs `06b/analysis`) |
| `Run-260916/` | 2026-09-16/17 | `06-03c` | two-tier S/R downsampling (`c631264`) + extended grid (`5ad5485`); 30 rounds, μ=0.1; pre-FedProx-fix | Centr 0.763 · FedAvg 0.715 · FedProx 0.550 · FedLR 0.739 · FedRF 0.500 · cross-site 0.592 | intermediate experiment, not documented |
| `06-Ceftriaxone-E-coli/` | Jul/Sep 2026 | z-runs | saved model weights only (no CSVs) | — | weight backup; see its README |
| `06-03d-Phase1-SiteMask-Diagnostic/` | 2026-09 | `06-03d-…` | site-mask drop-vs-k diagnostic | — | docs `06b/mask-diagnostic` |
| `06-03d-SiteDeconfound-Diagnostic/` | 2026-09 | `06-03d-…` | site-deconfounding trade-off | — | docs `06b/mask-diagnostic` |

Protocol status — current notebooks (not yet run): `NUM_ROUNDS=50`,
`FEDPROX_MUS=[0.5, 1.0]`, squared proximal penalty (`5d8c8fc`, `d883dcd`),
RF threshold tuning. The docs' promised refresh awaits this final re-run.

Notes (2026-10-15 reorder):
- moved the Ceftazidime orphan `06-03c-Ceftazidime-Federated-z-Runs/` to 06a
  (now `06a-…/Results/06-03c-loss-test/`);
- removed `06-03c-Results.zip`: its 10 files are a byte-identical subset of
  `results-20260721T064626Z-1-001.zip` (12 files; the two extras are the Jul-20
  loss files), which is kept;
- the 2.1 GB `06-Ceftriaxone-E-coli-…-1-003.zip` is a full backup of the
  extracted `06-Ceftriaxone-E-coli/` tree (redundant; candidate for removal).
