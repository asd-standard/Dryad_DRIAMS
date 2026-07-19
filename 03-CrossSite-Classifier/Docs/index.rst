03 — Cross-Site Classifier
=============================

Train on :term:`DRIAMS`-A (University Hospital Basel), test on B (Canton
Basel-Land), C (Canton Aarau), D (Viollier).

.. _notebook: 03-CrossSite-Classifier.ipynb

.. toctree::
   :maxdepth: 1
   :caption: Sections

   results

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
See :doc:`01 </01-LogisticAnalysis-Aggregated/Docs/index>` for method details.

**MLP:** Per-drug regularised :term:`MLP` + attention :term:`MLP`, both with
:term:`Threshold Tuning`.
See :doc:`02 </02-MLPClassifier-Aggregated/Docs/index>` for architecture details.

Preprocessing
-------------

- :term:`log1p transform` + :term:`Standardize to zero mean`, fit on **A train only**
- No information from B/C/D leaks into preprocessing
- Split: :term:`species-stratified split` 80/20 on A; B/C/D used as-is

Key Findings
------------

- Significant drop in performance compared to :term:`Aggregated (pooled) training` (01/02):
  training on a single site's data limits generalisation
- :term:`MLP` handles :term:`Domain shift` better than :term:`LogisticRegression`
- Site D (Viollier, private lab) is consistently the hardest target
- :term:`Cross-site evaluation` establishes the **lower bound** that
  :term:`Federated learning` (08) aims to beat by incorporating data from
  all sites

References Back
---------------

Cross-site evaluation methodology is reused in:

- :doc:`04 </04-Multi-Label-mlp/Docs/index>` — Multi-label cross-site (A→B/C/D)
- :doc:`05 </05-RandomForest-Ceftazidime-Ecoli/Docs/index>` — RF cross-site
- :doc:`06a </06a-Ceftazidime-E-coli/Docs/index>` — Species-specific cross-site
