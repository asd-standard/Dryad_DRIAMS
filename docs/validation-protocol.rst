Train / Validation / Test Protocol
==================================

How the per-drug analyses partition data and which decisions are made on
each partition. Applies to 01, 02 and the pooled half of 03; the cross-site
variant is documented in :doc:`03 </03-CrossSite-Classifier/index>` and the
per-site threshold variant of the federated study in
:doc:`08 </08-Federated-mlp-lr-rf/index>`.

Split Construction
------------------

- Splits are built with ``maldiamrkit.evaluation.stratified_species_drug_split``,
  seed 42. Species are kept disjoint across partitions: no species appears
  in more than one of train, validation or test, so the model cannot
  memorise species-specific spectral signatures.
- **01/02 (pooled)**: 70/15/15, produced in two stages. First 15% is held
  out as test; on the remaining 85%, a validation fraction
  :math:`\frac{0.15}{1-0.15} \approx 17.6\%` is held out, yielding 15% of
  the full dataset.
- Preprocessing (:term:`log1p transform` + :term:`Standardize to zero mean`)
  is fitted on the training split only and applied to validation and test.

Roles
-----

.. list-table::
   :header-rows: 1

   * - Operation
     - Train
     - Validation
     - Test
   * - Split share (01/02)
     - 70%
     - 15%
     - 15%
   * - Preprocessing fit
     - fit
     - apply
     - apply
   * - Model fitting
     - yes
     - \-
     - \-
   * - ``C`` search (3-fold GridSearchCV)
     - yes
     - \-
     - \-
   * - PCA fit (01/02 approach C)
     - fit
     - apply
     - apply
   * - :term:`Threshold Tuning`
     - \-
     - yes
     - \-
   * - Final metrics
     - reported
     - reported
     - evaluated once

The test set is never used for any choice: preprocessing state, ``C``, PCA
components, model configuration and decision threshold are all frozen
before it is scored. The validation split is used to select the decision
threshold and to report intermediate metrics.

MLP Internal Validation
-----------------------

``MaldiMLPClassifier`` additionally carves ``val_fraction=0.1`` out of the
**training** split for :term:`Early stopping` (patience 10, restoring the
best-validation weights). This internal split is nested inside train and is
distinct from the external validation set used for model and threshold
selection.

Metrics
-------

:term:`Balanced Accuracy` (threshold-dependent) is the selection metric;
:term:`AUC-ROC` (threshold-independent) is reported alongside it. See the
:doc:`glossary`.

Cross-Site Variant
------------------

Analysis 03 replaces the pooled split with a domain-shift protocol: train
on DRIAMS-A (species-stratified 80/20), use A validation for model and
threshold selection, and test on the complete B/C/D sites and their pooled
union. See :doc:`03 </03-CrossSite-Classifier/index>`.
