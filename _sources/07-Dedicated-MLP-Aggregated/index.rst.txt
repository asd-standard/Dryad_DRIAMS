07 — Dedicated Per-Drug Models on Aggregated Data
====================================================

10 independent :term:`Per-drug model`\ s (LR, RF, MLP) on pooled A+B+C+D.
This is the most comprehensive non-federated baseline, producing the
hyperparameters reused by the :term:`Federated learning` study (08).


.. toctree::
   :maxdepth: 1
   :caption: Sections

   results
   loss-curves
   integration

Objective
---------

Run a full systematic comparison of all three model families
(:term:`LogisticRegression`, :term:`MLP`, :term:`Random Forest`) across
all 10 drugs on pooled data, establishing:

1. The best achievable :term:`Aggregated (pooled) training` performance
   per drug
2. Optimal hyperparameters per drug per model — saved to
   :term:`best_params.csv` and reused by 08
3. The performance ceiling that :term:`Federated learning` can aim to recover

Notebooks
---------

- :notebook:`07-Dedicated-MLP-Aggregated.ipynb <07-Dedicated-MLP-Aggregated/07-Dedicated-MLP-Aggregated.ipynb>` — Main: LR + RF + MLP for 10 drugs
- :notebook:`07-01-Dedicated-LR-MLP-Aggregated.ipynb <07-Dedicated-MLP-Aggregated/07-01-Dedicated-LR-MLP-Aggregated.ipynb>` — LR + MLP only (no RF)
- :notebook:`07-02-Dedicated-MLP-ClassWeight.ipynb <07-Dedicated-MLP-Aggregated/07-02-Dedicated-MLP-ClassWeight.ipynb>` — MLP with class weight (**ran 2026-10-15**; see the class-weight ablation in :doc:`results`)
- :notebook:`07-02a-Prep-ClassWeight-Inputs.ipynb <07-Dedicated-MLP-Aggregated/07-02a-Prep-ClassWeight-Inputs.ipynb>` — rebuilds 07-02's input caches without MLP training
- :notebook:`07-03-Dedicated-RF-Fast.ipynb <07-Dedicated-MLP-Aggregated/07-03-Dedicated-RF-Fast.ipynb>` — Faster RF variant (**ran to produce the RF columns**)

Models
------

.. list-table::
   :header-rows: 1

   * - Model
     - Hyperparameter Search
     - Output
   * - LR
     - :term:`L2 regularization`, ``GridSearchCV(C)``, :term:`Threshold Tuning`
     - Per-drug :term:`C <L2 regularization>`, threshold
   * - RF
     - ``RandomizedSearchCV`` (``n_iter=20``, ``cv=2``, 5000-row subsample)
       over n_estimators, max_depth, min_samples_leaf, class_weight, plus
       :term:`Threshold Tuning` (see :notebook:`07-03
       <07-Dedicated-MLP-Aggregated/07-03-Dedicated-RF-Fast.ipynb>`)
     - Per-drug params, threshold
   * - MLP
     - 8×8 :term:`GridSearchCV` lr×dropout, internal val,
       :term:`Early stopping` (patience=10)
     - Per-drug lr, dropout

Split
-----

:term:`species-stratified split` 70/15/15 on pooled A+B+C+D per drug.

Preprocessing
-------------

:term:`log1p transform` + :term:`Standardize to zero mean` (fit on train only).

Key Findings
------------

- Mean test performance across the ten drugs on :term:`Aggregated (pooled) training`:
  :term:`LogisticRegression` 0.788 BalAcc / 0.862 AUC, :term:`MLP` 0.784 / 0.848,
  :term:`Random Forest` 0.761 / 0.843.
- LR and MLP are effectively tied, with the per-drug wins split: the MLP leads
  on Ciprofloxacin (+0.017), Amoxicillin-Clavulanic acid (+0.008),
  Piperacillin-Tazobactam (+0.009) and Amikacin (+0.010 BalAcc); LR leads on
  Gentamicin, Imipenem, Ceftazidime and Vancomycin.
- RF is below the two on average but remains close in AUC; it is the best model
  on Vancomycin Balanced Accuracy (0.897) and the weakest on Amikacin
  (0.606 BalAcc / 0.729 AUC), where the few resistant samples make the
  threshold fragile.
- Best-resolved drugs: Imipenem (0.89 BalAcc / 0.96 AUC), Cefepime
  (0.84 / 0.90) and Amoxicillin-Clavulanic acid (0.82 / 0.89); the hardest are
  Ceftazidime (0.70 / 0.78), Ciprofloxacin (0.72 / 0.80) and Amikacin
  (0.72 / 0.84).
- Class weighting (07-02) is close to neutral on average: 0.785 vs 0.784
  BalAcc for the unweighted MLP, while AUC improves on 9 of 10 drugs (mean
  0.854 vs 0.848). The gains concentrate on the rarest classes — see the
  class-weight ablation in :doc:`results`.
- These pooled numbers are the **centralised upper bound** for the federated
  study (08); the federated models aim to recover them without pooling raw data.

Key Relationships
-----------------

- Draws :term:`LogisticRegression` methodology from
  :doc:`01 </01-LogisticAnalysis-Aggregated/index>`
- Draws :term:`MLP` architecture from
  :doc:`02 </02-MLPClassifier-Aggregated/index>`
- Draws :term:`Random Forest` methodology from
  :doc:`05 </05-RandomForest-Ceftazidime-Ecoli/index>`
- Feeds :term:`best_params.csv` and ``rf_results.pkl`` directly into
  :doc:`08 </08-Federated-mlp-lr-rf/index>` as the source of
  :term:`Federated learning` hyperparameters and centralized (Pooled)
  baselines
