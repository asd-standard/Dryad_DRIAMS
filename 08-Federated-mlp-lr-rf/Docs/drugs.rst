Per-Drug Results
==================

Each drug directory contains self-contained federated notebooks that
produce the following outputs per run.

Run Directory Structure
-----------------------

::

   Drugs/{Drug}/{NN}-Run/
   ├── results/
   │   ├── final_results.csv         ← Best metrics per strategy
   │   ├── fedavg_per_round.csv      ← Per-round FedAvg MLP metrics
   │   ├── fedlr_per_round.csv       ← Per-round FedAvg LR metrics
   │   ├── fedrf_per_round.csv       ← Per-round FedRF metrics
   │   ├── fedprox_mu{μ}_per_round.csv ← Per-round FedProx metrics
   │   ├── best_params_used.txt      ← Hyperparameters snapshot
   │   ├── convergence.pdf           ← Convergence plot (all methods)
   │   ├── convergence_fedprox.pdf   ← FedProx per-site convergence
   │   ├── convergence_fedlr.pdf     ← FedLR per-site convergence
   │   ├── convergence_fedrf.pdf     ← FedRF per-site convergence
   │   ├── heatmap_balacc.pdf        ← Balanced Accuracy heatmap
   │   ├── heatmap_auc.pdf           ← AUC-ROC heatmap
   │   └── notebook.ipynb            ← Archived copy of the notebook
   └── models/
       ├── fedavg_mlp/round_NNN/client_{id}.pt + global_model.pt
       ├── fedprox_mlp_mu{μ}/round_NNN/client_{id}.pt + global_model.pt
       ├── fedavg_lr/round_NNN/client_{id}.npz + global_model.npz
       └── fedrf/round_NNN/client_{id}_trees.npy + global_trees.npy

final_results.csv Columns
--------------------------

``Method, A_BalAcc, A_AUC, B_BalAcc, B_AUC, C_BalAcc, C_AUC,
D_BalAcc, D_AUC, All_BalAcc, All_AUC, Peak_Round, Label``

The "peak round" is the round with the highest All_BalAcc after
excluding round 0 (initialisation).

Drugs
-----

+-------------------------------------+--------------------------------------------+
| Drug                                | Notes                                      |
+=====================================+============================================+
| Ciprofloxacin                       | Most complete: 04-Run, all 5 strategies    |
+-------------------------------------+--------------------------------------------+
| Gentamicin                          | All 3 notebooks (federated + retries)      |
+-------------------------------------+--------------------------------------------+
| Amoxicillin-Clavulanic acid         | All 3 notebooks                            |
+-------------------------------------+--------------------------------------------+
| Piperacillin-Tazobactam             | All 3 notebooks                            |
+-------------------------------------+--------------------------------------------+
| Ceftriaxone                         | All 3 notebooks                            |
+-------------------------------------+--------------------------------------------+
| Ceftazidime                         | All 3 notebooks                            |
+-------------------------------------+--------------------------------------------+

Retry Notebooks
---------------

**retry_fedprox.ipynb**
   Re-runs only FedProx with a new μ value, then merges results
   in-place into a target run directory. Reloads existing FedAvg,
   FedLR, and FedRF results from CSVs — only FedProx is re-trained.

**retry_lr.ipynb**
   Re-runs only Federated LR with new ``C``, ``max_iter``, and
   ``rounds``. Same in-place merge pattern.

Both utilities save time: no need to re-run FedAvg (40 rounds × 4
clients) just to test one new FedProx configuration.

Strategy Performance Patterns
-------------------------------

Common trends across all 6 drugs:

- **FedAvg MLP** is usually the strongest :term:`Federated learning` strategy,
  often within 2–5% of the centralized :term:`MLP`
- **FedProx** helps when site sizes are very imbalanced (site D is
  typically largest, A smallest)
- **FedAvg LR** is fast and stable but consistently below FedAvg MLP
  (linear model cannot capture the complexity)
- **FedRF** achieves strong results with only 5 rounds of
  :term:`Tree collection` — competitive with FedAvg MLP on some drugs
- **Cross-site** (A→B/C/D) is consistently the worst performer,
  confirming that single-site :term:`Cross-site evaluation` is insufficient

See :doc:`aggregated` for cross-drug comparisons.
