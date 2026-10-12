02 — MLP Classifier Analysis
==============================

Aggregated DRIAMS (A+B+C+D) — Top 3 drugs: Ciprofloxacin (23,662 samples),
Amoxicillin-Clavulanic acid (19,967), Gentamicin (18,312).


Objective
---------

Replace the linear :term:`LogisticRegression` baseline (see :doc:`01 </01-LogisticAnalysis-Aggregated/index>`)
with a non-linear :term:`MLP`, evaluating whether deep learning
extracts richer information from MALDI-TOF spectra.

.. toctree::
   :maxdepth: 1

   architecture
   loss-curves

Approaches
----------

Three MLP variants are compared, all using **MaldiDeepKit's**
``MaldiMLPClassifier`` (architecture on the :doc:`architecture` page):

**A) Baseline MLP**
   Standard :term:`MLP` with :term:`BatchNorm` and :term:`ReLU`
   activations; no :term:`Dropout` and no weight decay, batch size 32,
   100 epochs, fixed lr 1e-4 and no warmup. Fixed :term:`default threshold`
   0.5, no tuning. Run on Ciprofloxacin only.

**B) Regularised MLP + Threshold Tuning**
   Adds :term:`Dropout` (searched 0.5–0.8) and weight decay (1e-4) with a
   10-epoch warmup; batch size 64, 50 epochs, :term:`AdamW` with
   :term:`Cosine annealing` and :term:`Early stopping` (patience 10). The
   lr × dropout grid (coarse 8×8, then a fine 5×5 around the best point) is
   searched on Ciprofloxacin only — candidates are scored on the external
   validation split — and the winning configuration is reused for the other
   two drugs. The final model's decision threshold is tuned on the same
   validation split by :term:`Threshold Tuning`.

**C) Attention MLP + Threshold Tuning**
   :term:`sigmoid-gated attention` mechanism on the 512-dimensional hidden
   layer, allowing the model to dynamically weight spectral regions. Uses a
   fixed configuration (lr=1e-3, dropout 0.4/0.2, weight decay 1e-3, batch
   size 32, 100 epochs), so B-vs-C contrasts a tuned vanilla MLP with a
   default-config attention MLP rather than two equally tuned variants.
   :term:`Threshold Tuning` applied as in B.

Preprocessing
-------------

Same as 01: :term:`log1p transform` + :term:`Standardize to zero mean`.

Both MLP variants use the same 70/15/15 species-stratified splits and the
10% internal early-stopping split described in
:doc:`/validation-protocol`. Hyperparameters are selected on the external
validation split, and the decision threshold is tuned on the same split by
:term:`Threshold Tuning`.

Training Dynamics
-----------------

Unlike logistic regression (01), the MLP objective is non-convex: different
initialisations and training paths can reach different minima, so per-epoch
curves are informative. All reported scores come from the
**best-validation checkpoint** (``weights_source: best_val``), not the final
epoch; early stopping uses a 10% internal split carved out of training, with
patience 10 (see :doc:`/validation-protocol`).

The curves for the seven logged runs, the per-run overfitting table and the
full discussion are on the :doc:`loss-curves` page. In short: the regularised
models train longer (best epoch 14–30, stopping at 24–40) and end with
moderate final gaps (+0.15 to +0.21), while the baseline and attention models
overfit by epoch 2–3 with final gaps up to +0.54. Because the
best-validation checkpoint is used, these dynamics do not degrade the
reported test metrics.

The pooled best-config reruns with 07's hyperparameters (``02-01``) are
documented in
:doc:`07 loss curves </07-Dedicated-MLP-Aggregated/loss-curves>`.

Key Findings
------------

**MLP vs logistic regression.** Test performance is level with the tuned L2
LR (:doc:`01 </01-LogisticAnalysis-Aggregated/index>`) on all three drugs:
Ciprofloxacin 0.720 BalAcc / 0.806 AUC (attention) vs 0.721 / 0.798 (L2 LR);
Amoxicillin-Clavulanic acid 0.819 / 0.895 (regularised) vs 0.821 / 0.892;
Gentamicin 0.784 / 0.853 (regularised) vs 0.779 / 0.859. The non-linear model
does not extract substantially more signal on pooled data.

.. figure:: /_static/02-MLPClassifier-Aggregated/mlp_cip_roc.svg
   :alt: ROC curves for baseline, regularised and attention MLP on Ciprofloxacin
   :width: 100%

   ROC curves on the Ciprofloxacin test set for the three MLP variants.

**Attention.** Attention helps on Ciprofloxacin (test BalAcc 0.720 vs 0.707,
AUC 0.806 vs 0.783 for the regularised MLP) but does not separate from it on
the other two drugs (test AUC within 0.006). Since variant C uses a fixed,
untuned configuration, this is a conservative comparison.

.. figure:: /_static/02-MLPClassifier-Aggregated/mlp_cip_comparison.svg
   :alt: Train and test Balanced Accuracy and test AUC for the three MLP variants on Ciprofloxacin
   :width: 100%

   Ciprofloxacin comparison of the three MLP variants: train and test
   Balanced Accuracy and test AUC, with train-test gaps annotated.

**Role.** Establishes the **non-linear baseline** and the architecture used
throughout the rest of the project (see `Where This Appears Next`_).

.. figure:: /_static/02-MLPClassifier-Aggregated/mlp_three_drug_summary.svg
   :alt: Test Balanced Accuracy and AUC for the MLP variants across the three drugs
   :width: 100%

   Test Balanced Accuracy and AUC for the MLP variants across the three
   drugs.

Notebooks
---------

- :notebook:`02-MLPClassifier-Aggregated.ipynb <02-MLPClassifier-Aggregated/02-MLPClassifier-Aggregated.ipynb>` — main analysis (A/B/C, figures,
  summary CSV)
- :notebook:`02-01-Loss-Curves.ipynb <02-MLPClassifier-Aggregated/02-01-Loss-Curves.ipynb>` — best-config reruns with per-epoch logging
  (see :doc:`loss-curves`)
- Outputs: ``results_mlp_aggregated/`` (main) and
  ``results_loss_curves_02/`` (02-01)

Where This Appears Next
-----------------------

The MLP architecture (6000→512→256→128→2) and hyperparameter tuning
pattern are reused in:

- :doc:`03 </03-CrossSite-Classifier/index>` — Cross-site MLP
- :doc:`04 </04-Multi-Label-mlp/index>` — Multi-label shared-backbone MLP
- :doc:`06a </06a-Ceftazidime-E-coli/index>` — Species-specific MLP
- :doc:`07 </07-Dedicated-MLP-Aggregated/index>` — Per-drug 8×8 grid MLP
- :doc:`08 </08-Federated-mlp-lr-rf/index>` — Federated MLP (FedAvg / FedProx)
