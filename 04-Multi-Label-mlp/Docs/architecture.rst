Multi-Label Architecture
========================

:term:`Shared backbone` → 10 Independent Heads
----------------------------------------------

::

   Spectrum (6000 bins)
     ↓
   ┌─────────────────────────────────────────┐
   │  Linear(6000 → 512) + BN + ReLU + Drop  │
   │  Linear(512  → 256) + BN + ReLU + Drop  │
   │  Linear(256  → 128) + BN + ReLU + Drop  │  ← SHARED BACKBONE
   └─────────────────────────────────────────┘
     ↓
   ┌──────┬──────┬──────┬─────┬──────┐
   │ Cipro│ Gent │ Amox │ ... │ Amik │  ← 10 independent heads
   │ 1→1  │ 1→1  │ 1→1  │ ... │ 1→1  │     Linear(128→1) + Sigmoid
   └──────┴──────┴──────┴─────┴──────┘

Each head outputs a scalar probability P(resistant|drug). The
:term:`Shared backbone` is shared; each head learns drug-specific patterns
from the shared representation.

:term:`Label masking` (:term:`Masked BCE loss`)
-------------------------------------------------

Not every sample is tested for every drug. A mask matrix ``M`` of shape
``(N, 10)`` tracks which labels exist:

.. code-block::

   For each batch:
     logits = model(X_batch)                           # (B, 10)
     loss_per_sample = BCEWithLogitsLoss(logits, Y)    # (B, 10)
     mask = ~isnan(Y)                                  # (B, 10) — 1.0 where label exists
     loss = (loss_per_sample * mask).sum() / mask.sum()

Untested drugs contribute zero gradient for that sample. Each sample
provides gradients through all its known drug heads simultaneously,
amplifying the training signal by ~6× compared to per-drug binary.

Species-Stratified Split
------------------------

70/15/15 :term:`species-stratified split` on A's data ensures no species
cross-contamination between train, validation, and test.

Training
--------

- **Optimiser**: :term:`AdamW`
- **Grid search**: 6×6 over learning rate × dropout
- **Scoring**: Macro-averaged :term:`Balanced Accuracy` across all 10 drugs
  on the validation set
- **Best config**: Retrained for 100 epochs with :term:`Cosine annealing` LR,
  10-epoch warmup, weight_decay=1e-4, patience=15 :term:`Early stopping`

Why It Outperforms Per-Drug Binary
-----------------------------------

+-----------------------------------+------------------+------------------+
| Factor                            | Per-Drug Binary  | Multi-Label MLP  |
+===================================+==================+==================+
| Training samples per drug         | ~1–8K (varies)   | 9.4K × ~6 labels |
+-----------------------------------+------------------+------------------+
| Backbone training signal          | 1 label/sample   | ~6.3 labels/samp |
+-----------------------------------+------------------+------------------+
| Inter-drug transfer learning      | None             | Shared backbone  |
+-----------------------------------+------------------+------------------+
| Effective training signals        | ~8K (Cipro)      | ~60K (9.4K × 6)  |
+-----------------------------------+------------------+------------------+

The backbone is approximately 7–14× better trained than a single per-drug
model, and it learns multi-drug resistance patterns (e.g., ESBL-producing
strains resistant to multiple β-lactams).
