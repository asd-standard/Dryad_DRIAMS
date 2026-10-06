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
   :term:`Class weight`). :term:`C <L2 regularization>`, the *inverse* regularisation strength, is
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
- **Train**: preprocessing fitted, model fitted, :term:`C <L2 regularization>` selected by 3-fold
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

Logistic regression is convex: the log-loss as a function of the
coefficients has a single global optimum and no local minima. Unlike a
neural network, there is therefore no epoch-wise loss curve to inspect;
the diagnostics below examine the optimiser trajectory, the threshold
sensitivity and the L2 strength (see ``01-01-LR-Diagnostics.ipynb`` and
:doc:`/validation-protocol`).

Convergence
~~~~~~~~~~~

.. figure:: /_static/01-LogisticAnalysis-Aggregated/01_lr_convergence.svg
   :alt: Train and validation log-loss versus cumulative lbfgs iterations
   :width: 100%

   Convergence of the L2 LR on the pooled data: train (solid) and
   validation (dashed) log-loss versus cumulative ``lbfgs`` iterations.

The model is refit with warm starts and increasing ``max_iter`` budgets
(5, 10, 25, 50, 100, 250, 500, 1000). Both train and validation log-loss
decrease monotonically and then flatten, reaching the optimum after 72
(Amoxicillin-Clavulanic acid), 73 (Gentamicin) and 80 (Ciprofloxacin)
cumulative iterations; larger budgets change nothing. The final train/val
log-loss pairs (0.338/0.393, 0.308/0.364, 0.426/0.493, gaps 0.055–0.067)
show a constant offset, not epoch-style overfitting: the gap is the price
of the :term:`L2 regularization` and :term:`Class weight` terms in the
objective, and both losses flatten together.

Threshold Sweep
~~~~~~~~~~~~~~~

.. figure:: /_static/01-LogisticAnalysis-Aggregated/01_lr_threshold_sweep.svg
   :alt: Validation Balanced Accuracy versus decision threshold
   :width: 100%

   Threshold sweep on the validation split; dotted lines mark each drug's
   optimum, the gray dashed line is the default 0.5.

Validation :term:`Balanced Accuracy` versus the decision threshold
(0.05–0.95). The optimum is broad and close to the :term:`default threshold`
of 0.5 — 0.50 for Amoxicillin-Clavulanic acid (no gain), 0.47 for
Ciprofloxacin (+0.002) and 0.39 for Gentamicin (+0.005) — so
:term:`Threshold Tuning` moves the metric by at most ~0.005. With
``class_weight='balanced'`` the probabilities are already recentred, which
is why the default threshold is adequate for LR. :term:`AUC-ROC` is
constant along each curve (0.796, 0.891, 0.856) because it does not depend
on the threshold.

L2 Strength (C) Sweep
~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/01-LogisticAnalysis-Aggregated/01_lr_C_sweep.svg
   :alt: Cross-validated Balanced Accuracy versus C
   :width: 100%

   L2 strength sweep: 3-fold CV Balanced Accuracy (mean ± SD) versus
   ``C`` on a log scale.

3-fold CV :term:`Balanced Accuracy` versus :term:`C <L2 regularization>`
(log scale). Ciprofloxacin (C = 4.6e-4) and Amoxicillin-Clavulanic acid
(C = 2.5e-4) have interior optima, so the grid brackets the best value; for
Gentamicin the optimum sits at the lower grid edge (C = 5e-5, the minimum
tested), indicating the search range should be extended towards stronger
regularisation. The curves are flat (SD 0.002–0.010), so the exact value
of ``C`` is not critical.

Notebooks
---------

- ``01-LogisticAnalysis-Aggregated.ipynb`` — main analysis (A/B/C, figures,
  summary CSV)
- ``01-01-LR-Diagnostics.ipynb`` — convergence, threshold sweep, C-sweep
- Outputs: ``results_lr_aggregated/`` and ``results_lr_diagnostics/``

References Back
---------------

LR methodology established here is reused and extended in:

- :doc:`03 </03-CrossSite-Classifier/index>` — Cross-site (A→B/C/D)
- :doc:`06a </06a-Ceftazidime-E-coli/index>` — Species-specific LR
- :doc:`07 </07-Dedicated-MLP-Aggregated/index>` — Per-drug LR grid search
- :doc:`08 </08-Federated-mlp-lr-rf/index>` — Federated LR (FedAvg LR)
