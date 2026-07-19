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

06-02: Aggregated Iterative (4 Runs)
-------------------------------------

4 sequential runs with different 85/15 split seeds. Models evolve:

=========  ================================  ====================================
Model       Run 1                             Runs 2–4
=========  ================================  ====================================
LR          GridSearchCV(C) + CV threshold    Independent (new split, same proc)
MLP         6×6 grid lr×dropout + CV thresh   :term:`Warm-start training`, search LR only
RF          GridSearchCV + CV threshold       warm_start=True, accumulates trees
=========  ================================  ====================================

All runs evaluate on the same fixed 10% test set, extracted upfront.
Outputs: per-run tracking table, progression chart, mean±std heatmap.
