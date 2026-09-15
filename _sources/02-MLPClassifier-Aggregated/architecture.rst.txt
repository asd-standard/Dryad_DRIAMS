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
- **Dropout** applied after BatchNorm (typical range 0.3–0.8, tuned per drug)

   See :term:`ReLU`, :term:`BatchNorm`, :term:`Dropout`.
- Output is raw logits; ``CrossEntropyLoss`` is used during training

Optional Attention (introduced in 02, used in 04+07+08)
-------------------------------------------------------

When ``use_attention=True``, a :term:`sigmoid-gated attention` mechanism is
applied to the 512-dimensional hidden representation. The gating vector
(element-wise sigmoid) is learned from the same hidden state, allowing
the model to suppress or amplify individual features.

Training
--------

- **Optimiser**: :term:`AdamW` with weight decay (1e-4 to 1e-3)
- **LR schedule**: :term:`Cosine annealing` (T_max=90, eta_min=1e-6) with
  10-epoch linear warmup
- **Early stopping**: :term:`Early stopping` with patience 10–15 on
  internal validation loss
- **Batch size**: 64

Hyperparameter Search
---------------------

- **Learning rate**: :term:`GridSearchCV` 8×8 over lr × dropout (07+08)
- **Dropout**: 0.2–0.8 (tuned per drug, per model)
- Best params saved to :term:`best_params.csv`, reused by federated
  notebooks (08)
