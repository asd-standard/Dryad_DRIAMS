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
   Species-Masking/index
   umap-diagnostic
   site-d-ablation

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

Drug Selection
--------------

Six of the ten drugs available at all four sites are used in 08. The
selection is not arbitrary:

- **Resistance in every site.** All six reach the 5% resistant-prevalence
  threshold in each site and have at least ~100 resistant spectra even in
  the smallest site (DRIAMS-B). The four excluded drugs — Amikacin,
  Vancomycin, Imipenem and Cefepime — have at least one site where
  resistance is nearly absent (≤ 2.4%): that client would have little to
  learn and its per-site metrics would be unstable.
- **Continuity with the pilots.** Ceftazidime and Ceftriaxone are the two
  controlled cases of 06a/06b.
- **Class and mechanism diversity.** Fluoroquinolone (Ciprofloxacin),
  aminoglycoside (Gentamicin), penicillin/inhibitor combinations
  (Amoxicillin-Clavulanic acid, Piperacillin-Tazobactam), cephalosporins
  (Ceftazidime, Ceftriaxone).
- **Range of difficulty.** From the easiest (Amoxicillin-Clavulanic acid,
  pooled BalAcc 0.82) to the hardest (Ceftazidime 0.70, Ciprofloxacin
  0.72) dedicated models in 07.

.. list-table:: Resistant prevalence per site (sites A/B/C/D) — the ten
   drugs available at all four sites
   :header-rows: 1
   :widths: 32 10 10 10 10 8

   * - Drug
     - A
     - B
     - C
     - D
     - In 08
   * - Amoxicillin-Clavulanic acid
     - 38.9%
     - 26.2%
     - 30.7%
     - 23.0%
     - yes
   * - Ciprofloxacin
     - 20.3%
     - 15.2%
     - 10.2%
     - 11.6%
     - yes
   * - Piperacillin-Tazobactam
     - 20.6%
     - 14.8%
     - 11.3%
     - 8.4%
     - yes
   * - Ceftriaxone
     - 24.7%
     - 10.4%
     - 24.7%
     - 8.0%
     - yes
   * - Ceftazidime
     - 11.0%
     - 10.6%
     - 12.2%
     - 7.5%
     - yes
   * - Gentamicin
     - 18.9%
     - 8.4%
     - 13.5%
     - 4.9%
     - yes
   * - Cefepime
     - 17.4%
     - 15.2%
     - 13.1%
     - 2.4%
     - no
   * - Imipenem
     - 18.4%
     - 4.3%
     - 2.1%
     - 8.1%
     - no
   * - Vancomycin
     - 2.1%
     - 1.3%
     - 1.4%
     - 0.5%
     - no
   * - Amikacin
     - 1.0%
     - 1.2%
     - 1.6%
     - 1.7%
     - no

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
   ├── Site-D-Ablation/
   │   ├── {Drug}/federated_noD.ipynb       ← Leave-D-out run (3-drug pilot)
   │   ├── Gentamicin/federated_{withD,noD,weight}.ipynb ← Seed/weight follow-up
   │   └── compare_noD.ipynb, compare_followup.ipynb ← Comparison notebooks
   └── Docs/

Each drug notebook is self-contained: it loads data, preprocesses, runs
all FL strategies, evaluates, and saves results. The Agg-Analysis
notebook loads per-drug results and produces cross-drug comparisons.
Site-D-Ablation re-runs selected drugs without site D (see
:doc:`site-d-ablation`).

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
