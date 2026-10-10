Progressive Analysis Notebooks
===============================

06-00: Cross-Site (A) + Aggregated
-----------------------------------
**LR, MLP, RF.** :term:`Cross-site evaluation` train on :term:`DRIAMS`-A,
test on B/C/D. Then :term:`Aggregated (pooled) training` on pooled A+B+C+D
for comparison. Establishes the cross-site vs. aggregated gap for this
specific drug–pathogen pair.

06-01: Cross-Site (D) + Aggregated
------------------------------------
Same as 00 but cross-site training uses :term:`DRIAMS`-D (the private lab
with the most samples) instead of A. Tests whether a larger single-site
training set closes the gap with :term:`Aggregated (pooled) training`.

.. note::

   Result files for 06-00/06-01 are not part of this documentation; their
   cross-site vs. aggregated question is covered quantitatively by the
   federated baselines on :doc:`federated` and by the pooled models below.

06-02: Aggregated Iterative (4 Runs)
-------------------------------------

**Protocol.** Pooled A+B+C+D filtered to *E. coli*; a fixed 10% test set is
extracted upfront (seed 99). Four sequential runs then use different 85/15
train/validation splits (seeds 42, 123, 456, 789) of the remaining 90%.
Models evolve across runs:

=========  ================================  ====================================
Model       Run 1                             Runs 2–4
=========  ================================  ====================================
LR          GridSearchCV(C) + CV threshold    Independent (new split, same proc)
MLP         6×6 grid lr×dropout + CV thresh   :term:`Warm-start training`, search LR only
RF          GridSearchCV + CV threshold       warm_start=True, accumulates trees
=========  ================================  ====================================

**Results** — mean ± std across the four runs on the fixed 10% test set:

.. list-table::
   :header-rows: 1

   * - Model
     - BalAcc
     - AUC
   * - LR
     - 0.735 ± 0.019
     - 0.800 ± 0.014
   * - MLP
     - 0.643 ± 0.007
     - 0.792 ± 0.013
   * - **RF**
     - **0.753 ± 0.017**
     - **0.820 ± 0.004**

.. figure:: /_static/06a-Ceftazidime-E-coli/06a_iterative_progression.svg
   :alt: Per-run Balanced Accuracy and AUC for LR, MLP and RF across the four iterative runs
   :width: 100%

   Per-run progression: Balanced Accuracy (left) and AUC (right) for the
   three model families across runs 1–4. LR is re-fit per split, MLP is
   warm-started with an LR-only search, RF accumulates trees.

.. figure:: /_static/06a-Ceftazidime-E-coli/06a_iterative_heatmap.svg
   :alt: Mean Balanced Accuracy and AUC per model across the four runs
   :width: 100%

   Mean test-set Balanced Accuracy and AUC per model across the four runs.

**Findings**

- **RF leads** on this cohort (0.753 / 0.820), narrowly ahead of LR
  (0.735 / 0.800); the MLP trails by ~0.11 BalAcc despite a better AUC than
  LR's early runs, i.e. it ranks acceptably but is harder to calibrate on the
  *E. coli*-only data.
- **Warm-started MLP:** AUC improves monotonically with each warm-start run
  (0.774 → 0.790 → 0.800 → 0.803) while Balanced Accuracy stays flat
  (~0.635–0.651) — more training stabilises the ranking, not the decision
  boundary.
- **Tree accumulation:** the RF peaks at run 2 (200 trees, 0.771 BalAcc) and
  later runs add little (400 trees: 0.749), so 200 trees suffice here.
- **Threshold tuning matters:** unlike the default-0.5 evaluation of
  :doc:`05 </05-RandomForest-Ceftazidime-Ecoli/index>` (RF 0.616 BalAcc /
  0.745 AUC pooled), these runs tune thresholds by cross-validated
  predictions within the training split — the same ranking quality converts
  into 0.753 Balanced Accuracy.

**Outputs:** ``Results/06-02-Runs/`` — ``per_run_results.csv``,
``summary.csv``, ``progression.pdf``, ``final_heatmap.pdf``.
