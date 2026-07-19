06a — Ceftazidime × *E. coli*
===============================

Non-federated and federated analysis of a single drug–pathogen pair
with progressive model complexity. The federated counterpart for
Ceftriaxone × *E. coli* lives in
:doc:`06b </06b-Ceftriaxone-E-coli/Docs/index>`. 

.. toctree::
   :maxdepth: 1
   :caption: Sections

   analysis
   federated

Objective
---------

Use Ceftazidime × *E. coli* as a well-defined case study to explore:

1. Cross-site vs. :term:`Aggregated (pooled) training` (train on A vs.
   train on D vs. train on pooled A+B+C+D)
2. Iterative :term:`Warm-start training` across multiple random splits
3. Comparison of :term:`LogisticRegression`, :term:`MLP`, and
   :term:`Random Forest` on a single drug–pathogen pair
4. :term:`Federated learning` via :term:`Flower (flwr)` across 4
   :term:`DRIAMS` sites — the first federated experiment on Ceftazidime

Data
----

Pooled A+B+C+D, filtered to *E. coli* only. All splits are 85/15
stratified. Hyperparameter and threshold tuning happens entirely
within the 85% train; the 15% holdout is evaluated once.

Files
-----

Non-federated:
  - ``06-00-Ceftazidime-E-coli.ipynb`` — Cross-site (train A) + Aggregated
  - ``06-01-Ceftazidime-E-coli.ipynb`` — Cross-site (train D, largest site)
  - ``06-02-Ceftazidime-E-coli-Aggregated-Iterative.ipynb`` — 4 sequential
    runs with warm-start

Federated:
  - ``06-03a-Ceftazidime-E-coli-Federated.ipynb`` — Main FL notebook
  - ``06-03b-Ceftazidime-E-coli-Federated.ipynb`` — FL variant B
  - ``06-03c-Species-Masked-Ceftazidime-Federated.ipynb`` — Species masking
    variants for centralized baselines
  - ``retry_fedprox.ipynb`` — :term:`FedProx` μ retry utility

Related Analyses
----------------

Methodologies drawn from:

- :doc:`01 </01-LogisticAnalysis-Aggregated/Docs/index>` — :term:`LogisticRegression` with
  :term:`L2 regularization` and :term:`Threshold Tuning`
- :doc:`02 </02-MLPClassifier-Aggregated/Docs/index>` — :term:`MLP` architecture and training
- :doc:`05 </05-RandomForest-Ceftazidime-Ecoli/Docs/index>` — :term:`Random Forest` for same
  drug–pathogen pair
- :doc:`03 </03-CrossSite-Classifier/Docs/index>` — :term:`Cross-site evaluation` pattern

Results feed forward to:

- :doc:`06b </06b-Ceftriaxone-E-coli/Docs/index>` — Federated follow-up on Ceftriaxone × *E. coli*
- :doc:`08 </08-Federated-mlp-lr-rf/Docs/index>` — Full federated study across all 6 drugs
