# Site-D Ablation (08)

Does site D hurt the federated models? This folder holds the **no-D arm**: the 08
federated runs re-executed with clients **A, B, C only**, while site D is kept in
evaluation as an unseen site.

## Contents

- `{Drug}/federated_noD.ipynb` — no-D run for each drug, generated from
  `Drugs/{Drug}/federated.ipynb` with:
  - `TRAIN_SITES = ["A", "B", "C"]` (3 clients); `SITE_ORDER` (4 sites) for eval
  - hyperparameters, thresholds and RF params loaded verbatim from the with-D
    run's `results/best_params_used.txt` (matched configuration; no re-tuning)
  - FedProx and cross-site cells skipped; checkpoint saving disabled
  - an extra `AllABC` metric (A/B/C-pooled) in every evaluation record
- `compare_noD.ipynb` — with-D vs no-D comparison tables and figures, written to
  `comparison_results/`.

## Matched runs

| Drug | no-D | with-D mirror | Rounds |
|---|---|---|---|
| Ceftriaxone | `Site-D-Ablation/Ceftriaxone` | `Drugs/Ceftriaxone/07-Run` | 50 |
| Ciprofloxacin | `Site-D-Ablation/Ciprofloxacin` | `Drugs/Ciprofloxacin/04-Run` | 50 |
| Ceftazidime | `Site-D-Ablation/Ceftazidime` | `Drugs/Ceftazidime/03-Run` | 30 |

The per-site 90/10 splits are computed per site with a fixed seed, so the A/B/C
test sets of the no-D arm are identical to the archived runs — per-site deltas
are paired comparisons. Single seed (42), as in the with-D runs: small deltas
cannot be separated from run-to-run noise.

## Gentamicin follow-up (seed noise floor + weight control)

`Gentamicin/` holds a second-round experiment on the same question:

- `federated_withD.ipynb` — all four clients, sample-proportional aggregation
  (control arm; mirrors `Drugs/Gentamicin/01-Run`, 40 rounds)
- `federated_noD.ipynb` — clients A/B/C only
- `federated_weight.ipynb` — all four clients, **uniform** aggregation weights
  (D keeps its data but loses its ~39 % weight share; implemented by returning a
  constant `num_examples` from each client, which Flower's `FedAvg` uses as the
  aggregation weight)
- `runs/{arm}_seed{seed}/` — executed copies: seeds 42/43/44 for withD and noD,
  42/43 for weight; local runs, results-only
- `compare_followup.ipynb` — noise floor (paired per-seed deltas) and the
  weight-control comparison

Purpose: quantify run-to-run noise (single-seed deltas in the pilot cannot be
separated from seed noise) and separate "D's data" from "D's aggregation
weight".

## Notes

- Results (CSVs/PDFs/SVGs) are local-only; the notebooks are tracked.
- Strategy set: Centralized MLP/RF (pooled A/B/C), FedAvg MLP, FedAvg LR, FedRF.
  FedProx is skipped (unstable at tuned μ in the with-D runs).
