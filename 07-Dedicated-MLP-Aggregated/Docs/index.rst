07 — Dedicated Per-Drug Models on Aggregated Data
====================================================

10 independent :term:`Per-drug model`\ s (LR, RF, MLP) on pooled A+B+C+D.
This is the most comprehensive non-federated baseline, producing the
hyperparameters reused by the :term:`Federated learning` study (08).

.. _notebook: 07-Dedicated-MLP-Aggregated.ipynb

.. toctree::
   :maxdepth: 1
   :caption: Sections

   results
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

- ``07-Dedicated-MLP-Aggregated.ipynb`` — Main: LR + RF + MLP for 10 drugs
- ``07-01-Dedicated-LR-MLP-Aggregated.ipynb`` — LR + MLP only (no RF)
- ``07-02-Dedicated-MLP-ClassWeight.ipynb`` — MLP with class weight
- ``07-03-Dedicated-RF-Fast.ipynb`` — Faster RF variant

Models
------

+-------+-------------------------------------------------------+-----------------+
| Model | Hyperparameter Search                                 | Output          |
+=======+=======================================================+=================+
| LR    | :term:`L2 regularization`, ``GridSearchCV(C)``,       | Per-drug C,     |
|       | :term:`Threshold Tuning`                              | threshold       |
+-------+-------------------------------------------------------+-----------------+
| RF    | :term:`GridSearchCV`\ (n_estimators, max_depth,       | Per-drug params,|
|       | min_samples_leaf, class_weight), :term:`Threshold Tuning` | threshold   |
+-------+-------------------------------------------------------+-----------------+
| MLP   | 8×8 :term:`GridSearchCV` lr×dropout, internal val,    | Per-drug lr,    |
|       | :term:`Early stopping` (patience=10)                  | dropout         |
+-------+-------------------------------------------------------+-----------------+

Split
-----

:term:`species-stratified split` 70/15/15 on pooled A+B+C+D per drug.

Preprocessing
-------------

:term:`log1p transform` + :term:`Standardize to zero mean` (fit on train only).

Key Relationships
-----------------

- Draws :term:`LogisticRegression` methodology from
  :doc:`01 </01-LogisticAnalysis-Aggregated/Docs/index>`
- Draws :term:`MLP` architecture from
  :doc:`02 </02-MLPClassifier-Aggregated/Docs/index>`
- Draws :term:`Random Forest` methodology from
  :doc:`05 </05-RandomForest-Ceftazidime-Ecoli/Docs/index>`
- Feeds :term:`best_params.csv` and ``rf_results.pkl`` directly into
  :doc:`08 </08-Federated-mlp-lr-rf/Docs/index>` as the source of
  :term:`Federated learning` hyperparameters and centralized (Pooled)
  baselines
