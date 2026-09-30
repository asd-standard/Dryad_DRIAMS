02 — MLP Classifier Analysis
==============================

Aggregated DRIAMS (A+B+C+D) — Top 3 drugs: Ciprofloxacin (23,662 samples),
Amoxicillin-Clavulanic acid (19,967), Gentamicin (18,312).


Objective
---------

Replace the linear :term:`LogisticRegression` baseline (see :doc:`01 </01-LogisticAnalysis-Aggregated/index>`)
with a non-linear :term:`MLP`, evaluating whether deep learning
extracts richer information from MALDI-TOF spectra.

.. toctree::
   :maxdepth: 1

   architecture

Approaches
----------

Three MLP variants, all using **MaldiDeepKit's** ``MaldiMLPClassifier``:

**A) Baseline MLP**
   Standard :term:`MLP` with :term:`BatchNorm` and :term:`ReLU` activations. No
   :term:`Dropout`, no attention. Fixed :term:`default threshold` 0.5. Run on
   Ciprofloxacin only.

**B) Regularised MLP + Threshold Tuning**
   Adds :term:`Dropout` and weight-decay regularisation with a 10-epoch
   warmup. The lr × dropout grid (coarse 8×8 followed by a fine 5×5 around
   the best point) is searched on Ciprofloxacin and the winning configuration
   is reused for the other two drugs. :term:`Threshold Tuning` selects the
   decision threshold on the held-out validation split by overall
   :term:`Balanced Accuracy`.

**C) Attention MLP + Threshold Tuning**
   :term:`sigmoid-gated attention` mechanism on the 512-dimensional hidden
   layer, allowing the model to dynamically weight spectral regions. Uses a
   fixed configuration (lr=1e-3, dropout 0.4/0.2, weight decay 1e-3), so
   B-vs-C contrasts a tuned vanilla MLP with a default-config attention MLP
   rather than two equally tuned variants. :term:`Threshold Tuning` applied
   as in B.

Preprocessing
-------------

Same as 01: :term:`log1p transform` + :term:`Standardize to zero mean`.

Training Dynamics
-----------------

All reported scores come from the **best-validation checkpoint**
(``weights_source: best_val``), not the final epoch. Per-epoch histories are
saved as ``results_mlp_aggregated/metrics_*.csv`` and plotted by
``02-01-Loss-Curves.ipynb``:

- The regularised variant trains longer (best epoch 14–30, stopping at
  24–40 epochs) and ends with final val−train gaps of +0.15 to +0.21.
- Baseline and attention overfit quickly (best epoch 2–3, stopping at
  12–13 epochs) with final gaps of +0.29 to +0.54.
- Validation AUROC: Ciprofloxacin 0.83 / 0.80 / 0.82 (baseline /
  regularised / attention); Amoxicillin-Clavulanic acid 0.90 / 0.90;
  Gentamicin 0.86 / 0.86.

Key Findings
------------

- On validation AUROC the MLP improves over the tuned L2 LR (see
  :doc:`01 </01-LogisticAnalysis-Aggregated/index>`) on all three drugs:
  0.828 vs 0.796, 0.899 vs 0.891 and 0.863 vs 0.856 for Ciprofloxacin,
  Amoxicillin-Clavulanic acid and Gentamicin respectively. On the
  Ciprofloxacin test set the two are close (MLP 0.80–0.81 vs LR 0.80).
- Attention helps on Ciprofloxacin (test AUC 0.81 vs 0.78 for the
  regularised MLP; validation AUROC 0.821 vs 0.797) but does not separate
  from it on the other two drugs (validation AUROC within 0.003).
- Establishes the **non-linear baseline** and architecture used throughout
  the rest of the project.

Notebooks
---------

- ``02-MLPClassifier-Aggregated.ipynb`` — main analysis (A/B/C, figures,
  summary CSV)
- ``02-01-Loss-Curves.ipynb`` — best-config reruns with per-epoch logging
- Outputs: ``results_mlp_aggregated/``

Where This Appears Next
-----------------------

The MLP architecture (6000→512→256→128→2) and hyperparameter tuning
pattern are reused in:

- :doc:`03 </03-CrossSite-Classifier/index>` — Cross-site MLP
- :doc:`04 </04-Multi-Label-mlp/index>` — Multi-label shared-backbone MLP
- :doc:`06a </06a-Ceftazidime-E-coli/index>` — Species-specific MLP
- :doc:`07 </07-Dedicated-MLP-Aggregated/index>` — Per-drug 8×8 grid MLP
- :doc:`08 </08-Federated-mlp-lr-rf/index>` — Federated MLP (FedAvg / FedProx)
