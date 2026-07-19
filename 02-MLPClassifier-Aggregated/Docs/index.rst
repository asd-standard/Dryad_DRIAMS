02 — MLP Classifier Analysis
==============================

Aggregated DRIAMS (A+B+C+D) — Top 3 drugs.

.. _notebook: 02-MLPClassifier-Aggregated.ipynb

Objective
---------

Replace the linear :term:`LogisticRegression` baseline (see :doc:`01 </01-LogisticAnalysis-Aggregated/Docs/index>`)
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
   :term:`Dropout`, no attention. Fixed :term:`default threshold` 0.5.

**B) Regularised MLP + Threshold Tuning**
   Adds :term:`Dropout` regularisation. :term:`Threshold Tuning` applied
   per-site via cross-validation to maximise worst-site
   :term:`Balanced Accuracy`.

**C) Attention MLP + Threshold Tuning**
   :term:`sigmoid-gated attention` mechanism on the 512-dimensional hidden
   layer, allowing the model to dynamically weight spectral regions.
   :term:`Threshold Tuning` applied as in B.

Preprocessing
-------------

Same as 01: :term:`log1p transform` + :term:`Standardize to zero mean`.

Key Findings
------------

- MLP consistently outperforms LR across all three drugs
- Attention yields a small but consistent improvement over regularised MLP
- Threshold tuning is critical for imbalanced resistance labels
- Establishes the **non-linear baseline** and architecture used throughout
  the rest of the project

Where This Appears Next
-----------------------

The MLP architecture (6000→512→256→128→2) and hyperparameter tuning
pattern are reused in:

- :doc:`03 </03-CrossSite-Classifier/Docs/index>` — Cross-site MLP
- :doc:`04 </04-Multi-Label-mlp/Docs/index>` — Multi-label shared-backbone MLP
- :doc:`06a </06a-Ceftazidime-E-coli/Docs/index>` — Species-specific MLP
- :doc:`07 </07-Dedicated-MLP-Aggregated/Docs/index>` — Per-drug 8×8 grid MLP
- :doc:`08 </08-Federated-mlp-lr-rf/Docs/index>` — Federated MLP (FedAvg / FedProx)
