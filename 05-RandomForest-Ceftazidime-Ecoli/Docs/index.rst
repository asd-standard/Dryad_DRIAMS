05 — Random Forest: Ceftazidime Resistance in *E. coli*
========================================================

Species-specific, drug-specific Random Forest classifier.

.. _notebook: 05-RandomForest-Ceftazidime-Ecoli.ipynb

Objective
---------

Introduce :term:`Random Forest` as a third model family (after
:term:`LogisticRegression` in :doc:`01 </01-LogisticAnalysis-Aggregated/Docs/index>`
and :term:`MLP` in :doc:`02 </02-MLPClassifier-Aggregated/Docs/index>`). Evaluated
on a single well-populated drug–pathogen combination.

Scope
-----

- **Drug**: Ceftazidime
- **Pathogen**: *Escherichia coli* (the most common species in :term:`DRIAMS`)
- **Data**: All 4 sites, 6000 bins at 3 Da resolution

Analysis Steps
--------------

1. **Load and filter**: Ceftazidime data from all 4 sites, retain only E. coli
2. **Hyperparameter tuning**: :term:`RandomizedSearchCV` on pooled A+B+C+D
   with 20 iterations over:

   - :term:`n_estimators`: [100, 200, 300, 500]
   - :term:`max_depth`: [10, 20, 30, None]
   - :term:`min_samples_leaf`: [2, 5, 10]
   - :term:`Class weight`: ['balanced', 'balanced_subsample']

3. **Cross-site evaluation**: :term:`Cross-site evaluation` — train on
   :term:`DRIAMS`-A, test on B/C/D separately (same pattern as 03)
4. **Multi-seed pooled evaluation**: 5× random 75/25 splits on pooled
   A+B+C+D for robust error estimates
5. **Feature importance**: :term:`Feature importance` — which m/z bins drive
   resistance prediction?

Key Findings
------------

- :term:`Random Forest` achieves competitive but slightly lower performance
  than :term:`MLP`
- :term:`Feature importance` reveals specific spectral regions associated
  with ceftazidime resistance (β-lactamase-related peak shifts)
- :term:`Aggregated (pooled) training` substantially outperforms
  :term:`Cross-site evaluation`, consistent with 03's findings

References Forward
------------------

RF methodology is reused in:

- :doc:`06a </06a-Ceftazidime-E-coli/Docs/index>` — Species-specific RF comparison
- :doc:`07 </07-Dedicated-MLP-Aggregated/Docs/index>` — Per-drug RF for 10 drugs
- :doc:`08 </08-Federated-mlp-lr-rf/Docs/index>` — Federated RF (:term:`FedRF` tree collection)
