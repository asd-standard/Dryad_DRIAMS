Introduction
============

This project predicts antimicrobial resistance (AMR) directly from
MALDI-TOF mass spectra collected at four Swiss hospital sites
(:term:`DRIAMS` A/B/C/D). It starts from per-drug linear baselines and
builds towards :term:`Federated learning` with :term:`Flower (flwr)`:
each hospital keeps its spectra private and only model updates are shared.

Motivation
----------

- MALDI-TOF is already routine in clinical microbiology for species
  identification; the same spectra carry resistance information.
- Hospitals cannot pool patient data (privacy, regulation), which is why
  the project culminates in :term:`Federated learning`.
- A model that generalises across sites must survive :term:`Domain shift`
  — different instruments, patient populations, and bacterial ecology —
  which is quantified by :term:`Cross-site evaluation`.

At a Glance
-----------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Task
     - Binary resistant / susceptible prediction per drug from 6000-bin spectra
   * - Data
     - :term:`DRIAMS` A/B/C/D — 4 Swiss hospitals, 97 processed drug–site combinations
   * - Models
     - :term:`LogisticRegression`, :term:`MLP`, :term:`Random Forest`,
       :term:`Multi-label classification` shared backbone
   * - Metrics
     - :term:`Balanced Accuracy`, :term:`AUC-ROC`
   * - Federated stack
     - :term:`Flower (flwr)` with :term:`FedAvg`, :term:`FedProx`,
       :term:`FedLR`, :term:`FedRF`
   * - Data preparation
     - :doc:`data-processing` — ``process_driams.py`` → per-drug ``data.csv``

End-to-End Pipeline
-------------------

::

   Dryad DRIAMS archives (raw/, preprocessed/, binned_6000/, id/)
        │
        │  process_driams.py — S/R filtering (S ≥ 500, R ≥ 10)
        ▼
   Processed/Proc_DRIAMS-{A,B,C,D}/{drug}/data.csv
        │
        │  per-notebook preprocessing: log1p + standardize (fit on train only)
        ▼
   Analyses 01–08 (LR / MLP / RF, multi-label, cross-site, federated)

How the Analyses Fit Together
-----------------------------

.. list-table::
   :header-rows: 1
   :widths: 8 34 58

   * - #
     - Focus
     - Role in the project
   * - 01
     - Logistic regression, pooled data
     - Linear baseline; introduces :term:`Threshold Tuning` and
       :term:`L2 regularization`
   * - 02
     - MLP, pooled data
     - Non-linear baseline; architecture reused throughout
   * - 03
     - Cross-site (train A → test B/C/D)
     - Quantifies :term:`Domain shift`; lower bound for federated learning
   * - 04
     - Multi-label shared backbone
     - One network, 10 drug heads; :term:`Masked BCE loss`
   * - 05
     - Random Forest, Ceftazidime × *E. coli*
     - Third model family; :term:`Feature importance`
   * - 06a
     - Ceftazidime × *E. coli*
     - Single drug–pathogen case study; first federated prototype
   * - 06b
     - Ceftriaxone × *E. coli* (federated)
     - First full federated experiment; species/site diagnostics
   * - 07
     - Dedicated per-drug models
     - Most comprehensive pooled baseline; emits :term:`best_params.csv`
   * - 08
     - Federated MLP / LR / RF
     - Main federated study across 6 drugs and 4 sites

Suggested Reading Paths
-----------------------

- **Model complexity**: :doc:`01 </01-LogisticAnalysis-Aggregated/index>` →
  :doc:`02 </02-MLPClassifier-Aggregated/index>` →
  :doc:`07 </07-Dedicated-MLP-Aggregated/index>`
- **Generalisation**: :doc:`03 </03-CrossSite-Classifier/index>` →
  :doc:`04 </04-Multi-Label-mlp/index>` →
  :doc:`06a </06a-Ceftazidime-E-coli/index>` /
  :doc:`06b </06b-Ceftriaxone-E-coli/index>` →
  :doc:`08 </08-Federated-mlp-lr-rf/index>`
- **Random Forest**: :doc:`05 </05-RandomForest-Ceftazidime-Ecoli/index>` →
  :doc:`08 </08-Federated-mlp-lr-rf/index>`

Conventions
-----------

- Each analysis page states its objective, data, methods, key findings,
  and cross-references to related analyses.
- Terms throughout link to the :doc:`glossary`; ML and MALDI-TOF
  vocabulary is defined there.
- Data provenance and the processing pipeline are documented in
  :doc:`data-processing`.
