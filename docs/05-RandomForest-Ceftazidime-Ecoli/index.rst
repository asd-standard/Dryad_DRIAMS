05 — Random Forest: Ceftazidime Resistance in *E. coli*
========================================================

Species-specific, drug-specific :term:`Random Forest` classifier on the
Ceftazidime × *Escherichia coli* slice of :term:`DRIAMS`. Introduces the third
model family and the :term:`Feature importance` machinery reused in 07 and 08.

.. note::

   All numbers on this page come from the local October 2026 re-run of the
   notebook (see `Provenance`_); the June 2026 exports are archived in
   ``results_rf_2026-06-13/``.


Objective
---------

Compare a tree ensemble against the linear (:doc:`01
</01-LogisticAnalysis-Aggregated/index>`) and :term:`MLP` (:doc:`02
</02-MLPClassifier-Aggregated/index>`) families on a single well-populated
drug–pathogen combination, and test whether :term:`Cross-site evaluation`
behaves as in :doc:`03 </03-CrossSite-Classifier/index>`.

Data
----

Pooled A+B+C+D, filtered to *E. coli*, 6000 bins at 3 Da resolution:

.. list-table::
   :header-rows: 1

   * - Site
     - Samples
     - Resistant
     - Susceptible
     - %R
   * - DRIAMS-A
     - 1255
     - 120
     - 1135
     - 9.6%
   * - DRIAMS-B
     - 213
     - 45
     - 168
     - 21.1%
   * - DRIAMS-C
     - 908
     - 139
     - 769
     - 15.3%
   * - DRIAMS-D
     - 1987
     - 178
     - 1809
     - 9.0%
   * - **Total**
     - **4363**
     - **482**
     - **3881**
     - **11.0%**

Method
------

**Preprocessing** — :term:`log1p transform` + :term:`Standardize to zero mean`
(MaldiDeepKit), fitted on the training split only for every evaluation: the
tuning train, Site A, or each seed's training split. No information from the
evaluation splits enters the transform.

**Hyperparameter tuning** — :term:`GridSearchCV` over 72 combinations with
3-fold cross-validation, scored by :term:`Balanced Accuracy` on a single
pooled stratified 75/25 split (seed 42; 3,272 train / 1,091 holdout,
361 / 121 resistant):

- :term:`n_estimators`: [100, 300, 500]
- :term:`max_depth`: [10, 20, 30, None]
- :term:`min_samples_leaf`: [2, 5, 10]
- :term:`Class weight`: ['balanced', 'balanced_subsample']

The winning configuration is **500 trees, max_depth 10, min_samples_leaf 10,
class_weight 'balanced'** with cross-validated Balanced Accuracy **0.6049**.
The 25% holdout was then scored once: **BalAcc 0.6152 / AUC 0.7805**
(:term:`OOB error` 0.0987).

**Cross-site evaluation** — fit on Site A only (1,255 spectra, 120 resistant)
with the tuned configuration, preprocessing fitted on A, and score B/C/D
separately. Thresholds are left at the :term:`default threshold` of 0.5; no
:term:`Threshold Tuning` is performed.

**Pooled multi-seed evaluation** — five independent label-stratified 75/25
splits of the pooled data (seeds 42, 123, 456, 789, 1011); the transform and
the model are refit per split, again at the 0.5 threshold.

**Feature importance** — a final RF is trained on all pooled data
(interpretation only, no held-out evaluation) and per-bin impurity importance
is mapped onto the m/z axis.

Key Findings
------------

**Grid search.** All four hyperparameters are nearly flat: mean CV Balanced
Accuracy stays in a ~0.51–0.60 band across every parameter level, with 500
trees and ``class_weight='balanced'`` at the top.

.. figure:: /_static/05-RandomForest-Ceftazidime-Ecoli/05_grid_search.svg
   :alt: GridSearchCV per-parameter cross-validated Balanced Accuracy for the Random Forest
   :width: 100%

   Mean 3-fold CV Balanced Accuracy (± SD across combinations) for each
   parameter level; the dashed line is the best score (0.6049).

**No cross-site transfer.** Trained on A, the model predicts *every* B/C/D
spectrum as susceptible at the 0.5 threshold, which pins Balanced Accuracy at
exactly 0.500: sensitivity 0, specificity 1.

.. figure:: /_static/05-RandomForest-Ceftazidime-Ecoli/05_cross_site_eval.svg
   :alt: Cross-site Balanced Accuracy and AUC for the Random Forest trained on DRIAMS-A
   :width: 100%

   Cross-site scores per site, with sample counts; A is scored in-sample as a
   reference and is not evidence of generalisation.

.. figure:: /_static/05-RandomForest-Ceftazidime-Ecoli/05_cross_site_confusion.svg
   :alt: Cross-site confusion matrices for DRIAMS-B, C and D
   :width: 100%

   Confusion matrices on B/C/D: zero resistant predictions everywhere.

.. list-table:: Cross-site results (train A)
   :header-rows: 1

   * - Site
     - n
     - BalAcc
     - AUC
   * - DRIAMS-A (train)
     - 1255
     - 0.999
     - 1.000
   * - DRIAMS-B
     - 213
     - 0.500
     - 0.599
   * - DRIAMS-C
     - 908
     - 0.500
     - 0.553
   * - DRIAMS-D
     - 1987
     - 0.500
     - 0.645

The AUCs stay above chance — the ranking carries some signal, strongest on D
(0.645) — but it does not survive the 0.5 decision threshold. The pattern
matches the :term:`Cross-site evaluation` findings of 03 and 04: the model
fits Site A almost perfectly (in-sample BalAcc 0.999) and transfers poorly,
with :term:`Domain shift` dominating.

**Pooled multi-seed: ranking signal, threshold-limited.** On pooled splits
the RF reaches **BalAcc 0.6162 ± 0.0198** and **AUC 0.7449 ± 0.0281** across
five seeds. The gap between AUC and Balanced Accuracy is the missing
threshold tuning: resistant spectra are ranked well but rarely exceed 0.5.

.. figure:: /_static/05-RandomForest-Ceftazidime-Ecoli/05_multi_seed_eval.svg
   :alt: Pooled multi-seed Balanced Accuracy and AUC with per-seed values
   :width: 100%

   Left: mean ± SD over five pooled 75/25 splits. Right: per-seed
   consistency.

.. list-table:: Per-seed pooled metrics
   :header-rows: 1

   * - Seed
     - BalAcc
     - AUC
     - OOB error
   * - 42 (tuning holdout)
     - 0.615
     - 0.781
     - 0.099
   * - 123
     - 0.654
     - 0.764
     - 0.104
   * - 456
     - 0.602
     - 0.743
     - 0.107
   * - 789
     - 0.599
     - 0.697
     - 0.105
   * - 1011
     - 0.611
     - 0.739
     - 0.103
   * - **Mean ± SD**
     - **0.616 ± 0.020**
     - **0.745 ± 0.028**
     - —

Seed 42 is also the 25% tuning holdout of the grid search (same split,
preprocessing and model seed, by construction).

**Feature importance.** The final RF put most impurity importance on a few
narrow regions of the spectrum: ~11.78 kDa, ~10.47 kDa, ~6.81 kDa,
~5.89 kDa, ~2.82 kDa and ~2.59 kDa, each represented by 2–4 adjacent bins.

.. figure:: /_static/05-RandomForest-Ceftazidime-Ecoli/05_feature_importance.svg
   :alt: Random Forest feature importance along the m/z axis and the top-30 bins
   :width: 100%

   Top: per-bin impurity importance along the m/z axis, with the top-30 bins
   marked. Bottom: the top-30 bins as a bar chart.

.. list-table:: Top-10 most important bins (all pooled data)
   :header-rows: 1

   * - Rank
     - Bin
     - m/z (Da)
     - Importance
   * - 1
     - ``bin_3260``
     - 11780
     - 0.005672
   * - 2
     - ``bin_3261``
     - 11783
     - 0.005004
   * - 3
     - ``bin_3262``
     - 11786
     - 0.004769
   * - 4
     - ``bin_2826``
     - 10478
     - 0.004632
   * - 5
     - ``bin_1297``
     - 5891
     - 0.004305
   * - 6
     - ``bin_272``
     - 2816
     - 0.004289
   * - 7
     - ``bin_1602``
     - 6806
     - 0.004213
   * - 8
     - ``bin_197``
     - 2591
     - 0.004197
   * - 9
     - ``bin_2825``
     - 10475
     - 0.004044
   * - 10
     - ``bin_2824``
     - 10472
     - 0.003923

Interpretation
--------------

- **Third model family.** The RF pipeline (tuning, cross-site, multi-seed,
  importance) works and is reused for the per-drug models of 07 and the
  federated RF of 08.
- **The cross-site story is unchanged.** As in 03/04, a model that fits Site A
  almost perfectly fails on B/C/D; here the failure is total at the 0.5
  threshold (all-susceptible), with only weak ranking signal (AUC 0.55–0.645).
- **Threshold tuning is the missing piece.** Pooled AUC 0.745 shows the RF
  ranks resistant spectra usefully, but without :term:`Threshold Tuning` this
  cannot convert into Balanced Accuracy. For comparison, the per-drug RF of
  07 (all species, thresholds tuned by cross-validated predictions) reaches
  0.686 / 0.759 on Ceftazidime — a different scope, but it illustrates what
  tuning adds.
- **Spectral regions.** The importance peaks are narrow and clustered
  (adjacent bins), consistent with a few informative peaks rather than a
  distributed signature.

Caveats
-------

- **No threshold tuning anywhere** — cross-site predictions collapse to
  all-susceptible, so cross-site BalAcc is uninformative at exactly 0.500;
  the AUCs (0.55–0.645) are the meaningful cross-site numbers.
- **Hyperparameters were selected on pooled A+B+C+D**, i.e. on data that
  include the cross-site test sites. The model fit itself is clean (A only),
  but model selection saw B/C/D, so cross-site numbers carry selection
  optimism. The grid is near-flat, which limits the practical effect.
- **Splits are label-stratified, not site-stratified** (single species, so
  species stratification is moot). Site B contributes only 213 spectra, and
  site composition varies across the five pooled splits.
- **Single drug–pathogen pair** with 482 resistant spectra overall; B/C/D
  resistant counts are 45 / 139 / 178, so per-site metrics are noisy.
- **In-sample A scores (0.999 / 1.000)** reflect memorisation and are not
  generalisation evidence.
- **Feature importance is impurity-based**, computed by a model trained on
  all pooled data, and correlated bins share/steal importance; treat the m/z
  regions as hypotheses, not mechanisms.
- **Environment**: results come from a single library stack (scikit-learn
  1.9.0, seed 42 family). The June exports differed materially (see
  `Provenance`_), so version sensitivity is real.

Provenance
----------

The June 2026 exports in ``results_rf_2026-06-13/`` were produced by an
earlier notebook state (100 trees, no preprocessing) and cannot be reproduced
from the committed pipeline: the grid search selected those parameters at the
time, while the current notebook adds log1p+standardize (commit ``ec38c13``)
and, on a local re-run, selects 500 trees. The earlier multi-seed metrics
(BalAcc 0.543 ± 0.008) matched neither the committed code nor its stated
parameters, so they were not used here. All numbers on this page come from a
clean local run on 2026-10-09; the notebook's feature-importance layout bug
(shared x-axis squashing the top-30 panel) was fixed during this pass.

Notebooks and Files
-------------------

- ``05-RandomForest-Ceftazidime-Ecoli.ipynb`` — the analysis
- ``recover_multi_seed_metrics.py`` — reproduces the pooled multi-seed loop
  and documents the June-vs-current discrepancy
- ``results_rf/`` — current outputs (``report.md`` + five figures)
- ``results_rf_2026-06-13/`` — archived June exports

References Back
---------------

- :doc:`01 </01-LogisticAnalysis-Aggregated/index>` — :term:`LogisticRegression`
  baseline
- :doc:`02 </02-MLPClassifier-Aggregated/index>` — :term:`MLP` architecture
- :doc:`03 </03-CrossSite-Classifier/index>` — :term:`Cross-site evaluation`
  protocol

References Forward
------------------

- :doc:`06a </06a-Ceftazidime-E-coli/index>` — same drug–pathogen pair,
  progressive LR/MLP/RF + federated analysis
- :doc:`07 </07-Dedicated-MLP-Aggregated/index>` — per-drug RF with tuned
  thresholds
- :doc:`08 </08-Federated-mlp-lr-rf/index>` — federated RF
  (:term:`FedRF` tree collection)
