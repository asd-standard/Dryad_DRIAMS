08 — Federated MLP / LR / RF
===============================

:term:`Federated learning` across 4 hospital sites (:term:`DRIAMS` A/B/C/D)
using :term:`Flower (flwr)`.

.. toctree::
   :maxdepth: 2
   :caption: Sections

   methodology
   drugs
   aggregated

Objective
---------

Train antimicrobial resistance predictors without ever pooling patient
data. Each hospital keeps its spectra private. Models train locally and
share only model updates (weights/coefficients/trees). The server
aggregates them into a global model that should perform as well as —
or close to — a model trained on centrally pooled data.

Scope
-----

===================  =========================================================
Drugs                 6 drugs: Ciprofloxacin, Gentamicin,
                      Amoxicillin-Clavulanic acid, Piperacillin-Tazobactam,
                      Ceftriaxone, Ceftazidime
Species               All species, :term:`species-stratified split`\ s
Sites                 :term:`DRIAMS` A (Basel), B (Basel-Land), C (Aarau), D (Viollier)
Strategies            :term:`FedAvg` MLP, :term:`FedProx` MLP, :term:`FedAvg` LR,
                       :term:`FedRF` tree collection,
                       :term:`Species masking` (optional)
Baselines             Centralized (pooled) MLP, RF; :term:`Cross-site evaluation` (A→B/C/D)
Framework             :term:`Flower (flwr)` with :term:`Ray simulation` backend
Checkpoints           :term:`Checkpoint` — per-client + global model saved every round
===================  =========================================================

Directory Structure
-------------------

::

   08-Federated-mlp-lr-rf/
   ├── Species-Masking/
   │   ├── compute_masks.ipynb             ← One-time mask computation
   │   └── shared_masks/                  ← .npy masks + .joblib RF models
   ├── Drugs/
   │   ├── Ciprofloxacin/
   │   │   ├── federated.ipynb              ← Main FL notebook
   │   │   ├── retry_fedprox.ipynb          ← Re-run FedProx with new μ
   │   │   ├── retry_lr.ipynb               ← Re-run FedLR with new params
   │   │   └── {NN}-Run/results/            ← Per-run outputs
   │   ├── Gentamicin/         (same structure)
   │   ├── Amoxicillin-Clavulanic_acid/
   │   ├── Piperacillin-Tazobactam/
   │   ├── Ceftriaxone/
   │   └── Ceftazidime/
   ├── Agg-Analysis/
   │   ├── aggregated_analysis.ipynb        ← Cross-drug comparison
   │   └── masked_aggregated_analysis.ipynb ← Cross-drug (masked runs)
   └── Docs/

Each drug notebook is self-contained: it loads data, preprocesses, runs
all FL strategies, evaluates, and saves results. The Agg-Analysis
notebook loads per-drug results and produces cross-drug comparisons.

How It All Fits Together
------------------------

.. list-table::
   :header-rows: 1

   * - Analysis
     - Role
   * - 01
     - :term:`LogisticRegression` baseline → used by :term:`FedLR` (08)
   * - 02 / 07
     - :term:`MLP` architecture + hyperparams → used by :term:`FedAvg` /
       :term:`FedProx` MLP (08)
   * - 05
     - :term:`Random Forest` methodology → used by :term:`FedRF`
       :term:`Tree collection` (08)
   * - 06a
     - Ceftazidime × *E. coli* non-federated analysis → methodological
       foundation
   * - 06b
     - First :term:`Federated learning` prototype: Ceftriaxone × *E. coli*
       → proved viability → expanded to all 6 drugs in 08
   * - 07
     - :term:`best_params.csv` → hyperparameters for all federated clients
   * - 08 Agg-Analysis
     - ``results_balacc.csv``, ``rf_results.pkl`` → Pooled baseline
       reference lines
