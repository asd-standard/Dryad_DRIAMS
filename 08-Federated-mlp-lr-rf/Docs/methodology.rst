Federated Learning Methodology
================================

Flower Simulation Setup
-----------------------

:term:`Flower (flwr)`\ 's :term:`Ray simulation` runs 4 clients (one per hospital)
on the local machine. No real network communication — the simulation mimics
:term:`Federated learning` rounds with local training and server-side
aggregation.

::

   Server (strategy)
     │
     ├── Client 0 (DRIAMS-A)  ── local MLP/LR/RF training
     ├── Client 1 (DRIAMS-B)  ── local MLP/LR/RF training
     ├── Client 2 (DRIAMS-C)  ── local MLP/LR/RF training
     └── Client 3 (DRIAMS-D)  ── local MLP/LR/RF training
     │
     Server aggregates weights → global model → redistributes

Common Configuration
--------------------

=======================  ============================================
Parameter                 Value
=======================  ============================================
Input dimension           6000 bins (MALDI-TOF at 3 Da resolution)
MLP architecture          6000 → 512 → 256 → 128 → 2
Seed                      42 (all numpy/torch/sklearn)
Preprocessing             :term:`log1p transform` + :term:`Standardize to zero mean`
                          (fit per-site on train only)
Train/test split          :term:`species-stratified split` 90/10 per site
Device                    CPU (:term:`Ray simulation` workers have no GPU)
Framework                 :term:`Flower (flwr)` with :term:`Ray simulation` backend
=======================  ============================================

Strategy 1: :term:`FedAvg` MLP
------------------------------

Standard :term:`Federated learning` averaging over :term:`MLP` weights.

- **Rounds**: 40
- **Client training**: 1 local epoch per round (``LOCAL_EPOCHS=1``)
- **Batch size**: 16
- **Optimiser**: :term:`AdamW` with weight_decay=1e-4
- **Mixing**: :term:`Mixing` — small sites (<500 samples) train multiple seeds
  per round and average weights before sending.

  - <500 samples → 5 mixes
  - <1500 → 4 mixes
  - <5000 → 3 mixes
  - ≥5000 → 1 mix

- **Hyperparameters**: ``BEST_MLP_LR`` and ``BEST_MLP_DH`` from 07's
  :term:`best_params.csv`
- **Checkpoints**: :term:`Checkpoint` — per-client model + global model saved
  every round as ``.pt`` files. Metrics logged as ``metrics.json``.

Strategy 2: :term:`FedProx` MLP
-------------------------------

Adds a :term:`Proximal term (μ)` that penalises client weights drifting
too far from the global model. Controlled by μ (``proximal_mu``).

::

   Loss = CE_loss + (μ / 2) * ||client_weights - global_weights||²

- **μ values**: Per-drug tuned. Default 0.5. Ciprofloxacin uses 0.3,
  Ceftriaxone uses 0.1.
- **Same architecture and training as FedAvg**
- **Also supports mixing** for small sites
- **Checkpoints**: Same as FedAvg (per-client + global `.pt` files)

Strategy 3: :term:`FedLR` (Federated Logistic Regression)
---------------------------------------------------------

Federated training of a scikit-learn :term:`LogisticRegression` model.

- **Solver**: SAGA (supports warm-start and sparse gradients)
- **L2 regularisation**: ``C`` from 07's :term:`best_params.csv`
- **Class weight**: Balanced
- **Rounds**: 40 (same as :term:`FedAvg`)
- **Client training**: 1 ``max_iter`` per round (``warm_start=True``)
- **Checkpoints**: Per-client + global coefficients saved as ``.npz`` files

The retry notebook (``retry_lr.ipynb``) allows increasing ``max_iter``
and ``RETRY_ROUNDS`` for better convergence with fewer, higher-quality
local steps.

Strategy 4: :term:`FedRF` (:term:`Tree collection`)
---------------------------------------------------

Federated :term:`Random Forest` via :term:`Tree collection`. Each client
trains ``n_estimators`` trees locally using the per-drug hyperparameters
from 07's :term:`GridSearchCV`. The global model is simply the **union**
of all client trees.

- **Rounds**: 5 (explosive tree accumulation, fewer rounds needed)
- **RF params**: From 07's :term:`GridSearchCV`, selected via worst-site
  optimisation (Option A: per-site grid, pick combo that maximises
  worst-site score)
- **Trees per round**: :term:`n_estimators` (from RF_PARAMS, typically 100–500)
- **Global aggregation**: Concatenate all trees into one ensemble

  ::

     Global trees after round k = ∪ (client trees grown in round k)
                                  + trees from rounds 1..k-1

- **Threshold tuning**: Per-site CV, worst-site optimal. Same as Option A.

The :term:`Tree collection` approach is fundamentally different from weight
averaging: it grows the ensemble size linearly with rounds and client
count, potentially exceeding the centralized RF's tree budget.

Cross-Site Baselines
--------------------

To contextualise federated results, two pooled baselines are computed
within each drug notebook:

**Centralized (Pooled) MLP/RF**
   :term:`Aggregated (pooled) training` with the same hyperparameters.
   Preprocessing uses a single state fit on pooled data.

**Cross-Site (A → B/C/D)**
   :term:`Cross-site evaluation`: train MLP/RF on :term:`DRIAMS`-A only, test
   on B/C/D. Analogous to 03's approach, measuring the single-site lower bound.

Evaluation
----------

All strategies evaluate on **per-site 10% holdout sets**, which are
never seen during :term:`Federated learning`. The server runs evaluation
after each round via an ``evaluate_fn`` callback.

Metrics tracked per round, per site:
- ``{Site}_BalAcc`` — :term:`Balanced Accuracy`
- ``{Site}_AUC`` — :term:`AUC-ROC`
- ``All_BalAcc`` — All-site pooled :term:`Balanced Accuracy`
- ``All_AUC`` — All-site pooled :term:`AUC-ROC`
