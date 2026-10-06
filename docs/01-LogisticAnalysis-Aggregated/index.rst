01 — Logistic Regression Analysis
==================================

Aggregated DRIAMS (A+B+C+D) — Top 3 drugs: Ciprofloxacin,
Amoxicillin-Clavulanic acid, Gentamicin.


Objective
---------

Baseline AMR prediction using logistic regression on pooled hospital data,
establishing the simplest model against which all subsequent analyses are
compared.

Approaches
----------

Three variants are evaluated, all with solver ``lbfgs`` and
``max_iter=5000``:

**A) Raw LR**
   :term:`LogisticRegression` with ``penalty=None`` (no regularisation) and
   the :term:`default threshold` of 0.5, with no tuning. Run on
   Ciprofloxacin only.

**B) L2 LR + Threshold Tuning**
   :term:`LogisticRegression` with ``penalty='l2'`` (see
   :term:`L2 regularization`) and ``class_weight='balanced'`` (see
   :term:`Class weight`). ``C``, the *inverse* regularisation strength, is
   selected by 3-fold :term:`GridSearchCV` over 15 values (5e-5 to 1e-3,
   scoring :term:`Balanced Accuracy`) on the **training set only**; the CV
   score uses the default 0.5 threshold. The decision threshold is then
   tuned on the held-out validation split over 91 values (0.05 to 0.95) by
   :term:`Threshold Tuning`.

**C) PCA + L2 LR + Threshold Tuning**
   :term:`Dimensionality reduction` via :term:`PCA` (retaining 94% variance,
   fitted on the training set) followed by the same L2 LR and
   :term:`Threshold Tuning` as B. Evaluates whether denoising spectra
   improves generalisation.

Preprocessing
-------------

- :term:`log1p transform` (stabilise variance)
- :term:`Standardize to zero mean` (fit on train only)

Train / Validation / Test Protocol
----------------------------------

- **Species-stratified** 70/15/15 (:term:`species-stratified split`, seed
  42): no species appears in more than one partition, forcing the model to
  generalise across species rather than memorising species-specific
  spectral features.
- **Train**: preprocessing fitted, model fitted, ``C`` selected by 3-fold
  :term:`GridSearchCV`, PCA basis fitted (approach C).
- **Validation**: decision threshold tuned over 91 values (0.05–0.95) by
  :term:`Threshold Tuning`; no model parameters are re-fitted.
- **Test**: scored once with every choice frozen.

See :doc:`/validation-protocol` for the shared protocol, including the MLP
internal validation split.

Key Findings
------------

- On Ciprofloxacin — the only drug where raw LR was evaluated — L2
  regularisation with class weighting improves test performance
  substantially: BalAcc 0.72 vs 0.63 and AUC 0.80 vs 0.72.
- :term:`PCA` does not help: it slightly reduces test performance on all
  three drugs (up to 0.008 BalAcc and 0.005 AUC versus L2-only), so the full
  6000-bin spectrum is retained.
- With ``class_weight='balanced'``, the optimal threshold sits near 0.5
  (0.47 / 0.50 / 0.39 for Ciprofloxacin / Amoxicillin-Clavulanic acid /
  Gentamicin) and :term:`Threshold Tuning` changes validation
  :term:`Balanced Accuracy` by at most 0.005 — the :term:`default threshold`
  is adequate for LR.
- Serves as the **linear baseline** for all subsequent models.

Training Diagnostics
--------------------

Logistic regression is convex, so there is no epoch-wise loss curve; the
analogue is the optimiser trajectory (see ``01-01-LR-Diagnostics.ipynb``):

- **Convergence**: ``lbfgs`` reaches a plateau after 72–80 iterations, with
  final train/val log-loss gaps of 0.055–0.067 — no overfitting in the epoch
  sense.
- **Threshold sweep**: the validation optimum is flat around 0.5, consistent
  with the class-weighted objective.
- **C-sweep**: the cross-validated optimum is interior for Ciprofloxacin
  (C=4.6e-4) and Amoxicillin-Clavulanic acid (C=2.5e-4), but at the lower
  grid edge for Gentamicin (C=5e-5, the minimum tested).

Notebooks
---------

- ``01-LogisticAnalysis-Aggregated.ipynb`` — main analysis (A/B/C, figures,
  summary CSV)
- ``01-01-LR-Diagnostics.ipynb`` — convergence, threshold sweep, C-sweep
- Outputs: ``results_lr_aggregated/`` and ``results_lr_diagnostics/``

Cross-Site Behaviour
--------------------

Trained on DRIAMS-A and tested on B/C/D (analysis 03), L2 LR reaches a mean
:term:`Balanced Accuracy` of 0.641 on B+C+D (PCA+L2 0.643) — on par with, or
slightly better than, the regularised MLP (0.634). The decision threshold is
tuned once on A validation and reused on all target sites. PCA has a mixed
effect, helping Vancomycin and Ciprofloxacin but hurting Ceftazidime. See
:doc:`03 </03-CrossSite-Classifier/index>` and
:doc:`03 loss curves </03-CrossSite-Classifier/loss-curves>`.

References Back
---------------

LR methodology established here is reused and extended in:

- :doc:`03 </03-CrossSite-Classifier/index>` — Cross-site (A→B/C/D)
- :doc:`06a </06a-Ceftazidime-E-coli/index>` — Species-specific LR
- :doc:`07 </07-Dedicated-MLP-Aggregated/index>` — Per-drug LR grid search
- :doc:`08 </08-Federated-mlp-lr-rf/index>` — Federated LR (FedAvg LR)
