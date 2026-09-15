Integration with Federated Learning (08)
============================================

07 produces three artefacts consumed by the federated notebooks in 08.

``best_params.csv`` — Hyperparameters
--------------------------------------

Each drug has an entry in ``07-01-results_dedicated_lr_mlp/best_params.csv``
with the format::

   Drug              LR            MLP
   Ciprofloxacin     C=0.000457    lr=7.8e-05 drop=0.8
   Gentamicin        ...           ...

The federated notebooks (08) read this file to set:

- ``BEST_LR_C`` — Regularisation strength for :term:`FedLR` clients
- ``BEST_MLP_LR`` — Learning rate for :term:`MLP` clients
  (:term:`FedAvg` / :term:`FedProx`)
- ``BEST_MLP_DH`` — :term:`Dropout` high for :term:`MLP` architecture

This ensures the :term:`Federated learning` models use the same hyperparameters
found optimal in the centralized (:term:`Aggregated (pooled) training`) setting.

2. ``results_balacc.csv`` / ``results_auc.csv`` — Pooled Baselines
-------------------------------------------------------------------

The "Pooled LR" and "Pooled MLP" entries in the aggregated analysis
(08 Agg-Analysis) are sourced directly from 07's results. These are
shown as horizontal reference lines on all convergence plots and serve
as the "centralized upper bound" in the centralized-vs-federated gap
analysis.

3. ``rf_results.pkl`` — Pooled RF Baseline
------------------------------------------

Serialised :term:`Random Forest` results per drug provide the "Pooled RF"
baseline in the aggregated comparison. Since :term:`FedRF` accumulates trees
across rounds, its final tree count may exceed the centralized RF's fixed
:term:`n_estimators`, making this comparison particularly interesting.

Data Flow
---------

::

   07-Dedicated-MLP-Aggregated
   ├── best_params.csv    ────────→  08 Drugs/{drug}/federated.ipynb
   │                                 (sets BEST_LR_C, BEST_MLP_LR, BEST_MLP_DH)
   ├── results_balacc.csv ────────→  08 Agg-Analysis/aggregated_analysis.ipynb
   ├── results_auc.csv    ────────→  (Pooled LR / Pooled MLP reference lines)
   └── rf_results.pkl     ────────→  (Pooled RF reference line)
