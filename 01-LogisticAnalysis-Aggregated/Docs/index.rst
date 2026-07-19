01 — Logistic Regression Analysis
==================================

Aggregated DRIAMS (A+B+C+D) — Top 3 drugs.

.. _notebook: 01-LogisticAnalysis-Aggregated.ipynb

Objective
---------

Baseline AMR prediction using logistic regression on pooled hospital data,
establishing the simplest model against which all subsequent analyses are
compared.

Approaches
----------

Three variants are evaluated:

**A) Raw LR**
   Vanilla :term:`LogisticRegression` (scikit-learn) with no regularisation
   and :term:`default threshold` of 0.5.

**B) L2 LR + Threshold Tuning**
   :term:`LogisticRegression`\ (C=1.0, penalty='l2') with :term:`Threshold Tuning`
   via cross-validation to maximise worst-site :term:`Balanced Accuracy`.

**C) PCA + L2 LR + Threshold Tuning**
   :term:`Dimensionality reduction` via :term:`PCA` (retaining 95% variance)
   followed by :term:`L2 regularization` LR with :term:`Threshold Tuning`.
   Evaluates whether denoising spectra improves generalisation.

Preprocessing
-------------

- :term:`log1p transform` (stabilise variance)
- :term:`Standardize to zero mean` (fit on train only)

Train/Test Split
----------------

- **Species-stratified** 70/15/15 — :term:`species-stratified split`
- Ensures no species appears in both train and test, forcing the model
  to generalise across species rather than memorising species-specific
  spectral features.

Key Findings
------------

- :term:`L2 regularization` consistently outperforms raw LR
- :term:`PCA` degrades performance — the full 6000-bin spectrum contains
  useful information that PCA discards
- :term:`Threshold Tuning` provides a modest improvement over the
  :term:`default threshold`
- Serves as the **linear baseline** for all subsequent models

References Back
---------------

LR methodology established here is reused and extended in:

- :doc:`03 </03-CrossSite-Classifier/Docs/index>` — Cross-site (A→B/C/D)
- :doc:`06a </06a-Ceftazidime-E-coli/Docs/index>` — Species-specific LR
- :doc:`07 </07-Dedicated-MLP-Aggregated/Docs/index>` — Per-drug LR grid search
- :doc:`08 </08-Federated-mlp-lr-rf/Docs/index>` — Federated LR (FedAvg LR)
