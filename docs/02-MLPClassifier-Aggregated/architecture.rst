MLP Architecture
================

The core :term:`MLP` used throughout the DRIAMS analysis is implemented via
MaldiDeepKit's ``MaldiMLPClassifier`` and later directly as
:term:`SpectralAttentionMLP`.

Layer Dimensions
----------------

::

   Input (6000 bins)
     ↓
   Linear(6000 → 512) + BatchNorm1d + ReLU
     ↓
   Linear(512 → 256) + BatchNorm1d + ReLU
     ↓
   Linear(256 → 128) + BatchNorm1d + ReLU
     ↓
   Linear(128 → 2)              [binary classification head]

Activation and Regularisation
-----------------------------

- **ReLU** activations with **BatchNorm** after each linear layer
- **Dropout** applied after BatchNorm; per-variant settings are listed under
  `Training Recipe`_ below

   See :term:`ReLU`, :term:`BatchNorm`, :term:`Dropout`.
- Output is raw logits; ``CrossEntropyLoss`` is used during training

Optional Attention (introduced in 02, used in 04+07+08)
-------------------------------------------------------

When ``use_attention=True``, a :term:`sigmoid-gated attention` mechanism is
applied to the 512-dimensional hidden representation. The gating vector
(element-wise sigmoid) is learned from the same hidden state, allowing
the model to suppress or amplify individual features.

Training Recipe
---------------

This page describes the shared architecture; the recipe of the 02 variants
(see :doc:`index`) differs as follows:

- **A — Baseline**: dropout 0, weight decay 0, batch size 32, 100 epochs,
  fixed lr 1e-4, no warmup.
- **B — Regularised**: dropout 0.5–0.8 (grid-searched), weight decay 1e-4,
  batch size 64, 50 epochs, 10-epoch warmup, lr searched (coarse 8×8 + fine
  5×5 on Ciprofloxacin only).
- **C — Attention**: dropout 0.4/0.2, weight decay 1e-3, batch size 32,
  100 epochs, fixed lr 1e-3, no warmup.

All variants use :term:`AdamW`, :term:`Cosine annealing`
(:math:`T_{\max} = \text{epochs} - \text{warmup}`, i.e. 40 for B and 100 for
A/C, ``eta_min=1e-6``) and :term:`Early stopping` with patience 10 on the
internal validation split, restoring the best-validation weights.

Hyperparameter Search
---------------------

- 02 searches lr × dropout with manual coarse (8×8) and fine (5×5) grids on
  Ciprofloxacin; the winning configuration is reused for the other two drugs.
- The systematic per-drug grid and the shipped :term:`best_params.csv` are
  produced in :doc:`07 </07-Dedicated-MLP-Aggregated/index>`.
- :term:`GridSearchCV` (8×8) is also used by the multi-label and federated
  studies (04, 08).
