Multi-Label Architectures
=========================

Shared Backbone → 10 Drug Outputs
---------------------------------

::

   Spectrum (6000 bins)
     ↓
   ┌─────────────────────────────────────────┐
   │  Linear(6000 → 512) + BN + ReLU + Drop  │
   │  Linear(512  → 256) + BN + ReLU + Drop  │
   │  Linear(256  → 128) + BN + ReLU + Drop  │  ← SHARED BACKBONE
   └─────────────────────────────────────────┘
     ↓
   Linear(128 → 10 logits)                    ← one logit per drug
     ↓
   sigmoid → P(resistant | drug), 10 drugs

The model is MaldiDeepKit's ``SpectralAttentionMLP`` with
``use_attention=False``, i.e. a plain MLP of the same depth. The 10 logits
are produced by a single ``Linear(128 → 10)`` layer, which is mathematically
equivalent to ten independent ``Linear(128 → 1)`` heads. The exact layout is:

::

   proj:  Linear(6000 → 512) + BatchNorm + ReLU + Dropout(d_high)
   head:  Linear(512  → 256) + BatchNorm + ReLU + Dropout(d_high)
          Linear(256  → 128) + BatchNorm + ReLU + Dropout(d_low)
          Linear(128  → 10)

with ``d_low = d_high / 2`` throughout, so a single dropout value controls
the whole network. The backbone is shared; each output logit sees the same
learned representation and specialises through its own weights.

:term:`Label masking` (:term:`Masked BCE loss`)
-----------------------------------------------

Not every sample is tested for every drug. A mask matrix tracks which labels
exist, and the loss is averaged over known labels only:

.. code-block::

   For each batch:
     logits = model(X_batch)                           # (B, 10)
     loss_per_sample = BCEWithLogitsLoss(logits, Y)    # (B, 10), reduction="none"
     mask = ~isnan(Y)                                  # (B, 10) — 1.0 where label exists
     loss = (loss_per_sample * mask).sum() / mask.sum()

Untested drugs contribute zero gradient for that sample. Each sample provides
gradients through all its known drug outputs simultaneously — ~6.3 known
labels per spectrum on average across DRIAMS.

Species-Stratified Splits
-------------------------

Both settings keep every bacterial species in exactly one partition
(:term:`species-stratified split`), so no species-specific spectral signature
can be memorised across the train/test boundary:

- **Cross-site (04-00)**: A is split 80/20 into train (7,554) and validation
  (1,889); B, C, D and their union B+C+D are test sets used as-is.
  Preprocessing is fitted on A train only.
- **Aggregated (04-00, 04-01)**: A+B+C+D (26,781 spectra) are pooled and
  split 70/15/15 (18,745 / 4,018 / 4,018). Preprocessing is fitted on the
  train split only.
- **Internal early-stopping split**: 10% of each training split, again
  species-stratified, selects the best-validation checkpoint. The external
  validation split (A-val or aggregated val) is only used for grid scoring
  and :term:`Threshold Tuning`.

Training
--------

- **Optimiser**: :term:`AdamW`, batch size 64
- **Schedule**: :term:`Cosine annealing` with a 10-epoch linear warmup
- **Loss**: masked BCE (above)
- **Grid search**: 6×6 over learning rate × dropout. MLP: lr 1e-4–5e-4,
  dropout 0.2–0.6, weight decay 1e-3, 50 epochs, patience 10. CNN: lr 1e-5–5e-4
  (log scale), dropout 0.1–0.6, otherwise identical.
- **Scoring**: per-drug thresholds are tuned on the external validation split
  (91 values, 0.05–0.95) and the resulting macro-averaged
  :term:`Balanced Accuracy` across the 10 drugs selects the configuration.
- **Final run**: the winning configuration is retrained for up to 100 epochs
  with weight decay 1e-4 and patience 15; the best-validation-loss checkpoint
  is kept, and per-drug thresholds are tuned once more on the same external
  validation split. See :doc:`loss-curves` for the per-epoch dynamics.

Shared CNN (04-01)
------------------

The CNN replaces the fully-connected first layer with four 1D convolution
blocks that preserve the m/z axis, then pools it spatially:

::

   Spectrum (6000 bins)                                       → (B, 1, 6000)
     Conv1D(1→64,   k=7, pad=3) + BN + ReLU + MaxPool(2)      → (B, 64, 3000)
     Conv1D(64→128, k=7, pad=3) + BN + ReLU + MaxPool(2)      → (B, 128, 1500)
     Conv1D(128→256,k=5, pad=2) + BN + ReLU + MaxPool(2)      → (B, 256, 750)
     Conv1D(256→512,k=5, pad=2) + BN + ReLU                   → (B, 512, 750)
     AdaptiveAvgPool1d(16)                                    → (B, 512, 16)
     Flatten                                                  → (B, 8192)
     Linear(8192→256) + BN + ReLU + Dropout(d)                → (B, 256)
     Linear(256→128)  + BN + ReLU + Dropout(d/2)              → (B, 128)
     Linear(128→10 logits)                                    → (B, 10)

It uses the same masked BCE loss, the same 10-output head and the same
aggregated 70/15/15 split as the MLP, so the two backbones are compared under
identical conditions. The convolution kernels (7 and 5 bins ≈ 21 and 15 Da)
test whether local peak structure carries information that a global dense
projection misses.

What Multi-Label Changes
------------------------

+-----------------------------------+------------------+----------------------+
| Factor                            | Per-Drug Binary  | Multi-Label (10 out) |
+===================================+==================+======================+
| Training samples per drug         | ~1–8K (varies)   | 9.4K × ~6.3 labels   |
+-----------------------------------+------------------+----------------------+
| Backbone training signal          | 1 label/sample   | ~6.3 labels/sample   |
+-----------------------------------+------------------+----------------------+
| Inter-drug transfer learning      | None             | Shared backbone      |
+-----------------------------------+------------------+----------------------+
| Effective training signals        | ~8K (Cipro)      | ~60K (9.4K × 6.3)    |
+-----------------------------------+------------------+----------------------+

The backbone sees roughly an order of magnitude more label signal than a
single per-drug model, and it can exploit multi-drug resistance patterns
(e.g. ESBL-producing strains resistant to multiple β-lactams). In practice
this does not translate into higher accuracy: on pooled and cross-site data
the multi-label models land level with the per-drug baseline (see
:doc:`results`). More labels per sample do not compensate for the domain
shift between sites, and each head still sees only the samples tested for
that drug.
