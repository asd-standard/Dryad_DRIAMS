03 — Cross-Site Classifier
=============================

Train on :term:`DRIAMS`-A (University Hospital Basel), test on B (Canton
Basel-Land), C (Canton Aarau), D (Viollier).


.. toctree::
   :maxdepth: 1
   :caption: Sections

   results
   loss-curves

Objective
---------

Test whether a model trained on one hospital's spectra can predict
antimicrobial resistance at completely different hospitals. This is the
hardest test of generalisation — also known as :term:`Cross-site evaluation`:
different instruments, different patient populations, different bacterial
ecology.

Why It Matters
--------------

In :term:`Federated learning` (08), each hospital trains locally and the
aggregated model must work across all sites. :term:`Cross-site evaluation` is
the pooled-data analogue — can Site A's data alone predict B/C/D's
resistance patterns?

Approaches
----------

**Logistic Regression:** Per-drug :term:`L2 regularization` :term:`LogisticRegression`
+ :term:`Threshold Tuning`, with and without :term:`PCA`.
See :doc:`01 </01-LogisticAnalysis-Aggregated/index>` for method details.

**MLP:** Per-drug regularised :term:`MLP` + attention :term:`MLP`, both with
:term:`Threshold Tuning`.
See :doc:`02 </02-MLPClassifier-Aggregated/index>` for architecture details.

Preprocessing
-------------

- :term:`log1p transform` + :term:`Standardize to zero mean`, fit on **A train only**
- No information from B/C/D leaks into preprocessing
- Split: :term:`species-stratified split` 80/20 on A; B/C/D used as-is

Validation Protocol (cross-site variant)
----------------------------------------

- **Train**: DRIAMS-A, species-stratified 80/20; preprocessing fitted on
  the A training split only.
- **Validation (A-val)**: the held-out 20% of A, used for model selection
  and :term:`Threshold Tuning`.
- **Test**: the complete B, C and D sites plus their pooled union B+C+D,
  scored once. The threshold selected on A-val is frozen and reused
  unchanged on every target site.

Validation and test therefore come from different domains: A-val
performance does not predict cross-site transfer (correlation 0.59–0.68
across the diagnostics; see :doc:`loss-curves`). See
:doc:`/validation-protocol` for the shared definitions.

Key Findings
------------

**Cross-site degradation.** Performance drops sharply compared to
:term:`Aggregated (pooled) training` (01/02): mean :term:`Balanced Accuracy`
on the ten common drugs falls from 0.807 on A validation to 0.632 on B+C+D —
a 15–19 point loss depending on the model.

**Model families.** :term:`LogisticRegression` transfers as well as, or
better than, the :term:`MLP`: B+C+D means are 0.641 (L2), 0.643 (PCA+L2),
0.634 (regularised MLP) and 0.608 (attention MLP); more complex models do not
generalise better.

**Site difficulty.** Site difficulty is not driven by dataset size: B is the
smallest site yet the easiest target (0.692), while D (Viollier, private lab)
is the largest and the hardest (0.601); C is intermediate (0.615).

**Per-drug transfer.** Transfer spans from Amoxicillin-Clavulanic acid
(0.737, gap 0.083) to Piperacillin-Tazobactam (0.536) and Amikacin (0.537),
near chance. The chart below shows the best approach per drug.

.. figure:: /_static/03-CrossSite-Classifier/cross_site_best_per_drug.svg
   :alt: Best approach per drug: A validation Balanced Accuracy, cross-site test Balanced Accuracy and AUC
   :width: 100%

   Best-performing approach per drug: A-validation Balanced Accuracy, test
   Balanced Accuracy on B+C+D, and test AUC on B+C+D.

**Validation does not predict transfer.** A-val performance does not predict
cross-site transfer (correlation 0.59–0.68); see :doc:`loss-curves`.

**Lower bound for federation.** :term:`Cross-site evaluation` establishes the
**lower bound** that :term:`Federated learning` (08) aims to beat by
incorporating data from all sites.

References Back
---------------

Cross-site evaluation methodology is reused in:

- :doc:`04 </04-Multi-Label-mlp/index>` — Multi-label cross-site (A→B/C/D)
- :doc:`05 </05-RandomForest-Ceftazidime-Ecoli/index>` — RF cross-site
- :doc:`06a </06a-Ceftazidime-E-coli/index>` — Species-specific cross-site
