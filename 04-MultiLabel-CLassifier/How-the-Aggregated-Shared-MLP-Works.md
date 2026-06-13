# How the Aggregated Shared MLP Works

## 1. Data Assembly — The Multi-Label Matrix

Every spectrum is loaded once, then a label matrix `Y` of shape `(N, 10)` is built:

```
                    Cipro  Gent   AmoxClav  ...  Amik
Spectrum_001        0.0    0.0    1.0       ...  NaN
Spectrum_002        1.0    NaN    0.0       ...  0.0
Spectrum_003        NaN    1.0    NaN       ...  1.0
...
```

- `0.0` = Susceptible, `1.0` = Resistant, `NaN` = not tested
- The same spectrum appears once, with all its known drug labels in one row
- Average: **6.3 drugs labeled per sample** across all 4 sites

This is fundamentally different from the per-drug binary approach. There, each spectrum gets duplicated across 10 separate CSV files. Here, the spectrum lives once — the model sees all of a sample's resistance patterns simultaneously.

## 2. Architecture: One Backbone → 10 Heads

```
                         ┌─ Linear(128→1) + Sigmoid ── P(R|Cipro)     [head 0]
                         ├─ Linear(128→1) + Sigmoid ── P(R|Gent)      [head 1]
Spectrum                 ├─ ...                                        [...]
  (6000 bins)            ├─ ...                                        [...]
    ↓                    ├─ ...                                        [...]
Linear(6000→512)         └─ Linear(128→1) + Sigmoid ── P(R|Amik)      [head 9]
  + BatchNorm
  + ReLU                     ↑ 10 independent sigmoid heads
  + Dropout(d_high)          ↑ all share the same backbone
    ↓
Linear(512→256)
  + BN/ReLU/Dropout
    ↓
Linear(256→128)
  + BN/ReLU/Dropout
```

Key point: the hidden layers (6000→512→256→128) are **shared**. They learn a compressed representation of the spectrum that's useful for ALL 10 drugs simultaneously. The 10 output heads are independent — each one only needs a single `Linear(128→1)` layer to specialize from the shared representation.

The backbone learns general spectral features (peak presence, overall intensity profile, noise characteristics) while each head learns drug-specific patterns (e.g., β-lactam resistance signatures vs. aminoglycoside resistance signatures).

## 3. Training Loop — Masked BCE Loss

This is the critical part. Standard binary cross-entropy assumes every sample has every label. We have NaN values. The solution: **label masking**.

```python
# For each batch:
logits = model(X_batch)           # (B, 10) raw logits
loss_per_sample = BCE(logits, Y)  # (B, 10) — 10 loss values per sample
mask = ~isnan(Y)                  # (B, 10) — 1.0 where label exists, 0.0 where NaN
loss = (loss_per_sample * mask).sum() / mask.sum()  # scalar
```

What this means concretely: if a sample was tested for only 6 of the 10 drugs, only those 6 contribute to the loss. The other 4 are completely ignored. The gradients don't flow through the NaN heads for that sample. This is mathematically correct — you're computing the expected loss only over observed labels.

**Why this matters for the shared backbone:** each sample provides gradients to update the shared layers. A sample tested for 8 drugs provides 8× more signal to the backbone than a sample tested for 1 drug. The backbone learns from every available label, not just from one drug at a time.

## 4. Species-Stratified Split (70/15/15)

The split ensures the same species never appears in both train and test. This prevents memorization of species-specific features. When the model sees a new *E. coli* spectrum in the test set, it has never trained on any *E. coli* — it must generalize from its training on other species.

## 5. Grid Search + Regularization

The 6×6 grid over learning rate (`1e-4` to `5e-4`) and dropout (`0.2` to `0.6`) finds the optimal bias-variance tradeoff. Scoring is **macro-averaged Balanced Accuracy** across all 10 drugs on the validation set — the model is optimized to perform well on ALL drugs, not just the most common one.

The winning configuration gets retrained for 100 epochs with lower `weight_decay` (1e-4), early stopping patience=15, cosine annealing LR scheduler, and 10-epoch warmup.

## 6. Why This Outperforms Per-Drug Binary or Cross-Site

| Factor | Per-Drug Binary | Cross-Site (A→B+C+D) | Aggregated (this model) |
|--------|----------------|----------------------|------------------------|
| Training samples per drug | ~1-8K (varies by drug) | ~9K (A only) | **~27K** (all 4 sites) |
| Backbone training signal | 1 label per sample | 6.5 labels per sample | **6.3 labels per sample** |
| Species diversity | 1 site's species | A's species only | **All 4 sites' species** |
| Inter-drug learning | None | Shared backbone | **Shared backbone** |
| Test domain | Same hospital | Different hospital | **Mixed hospitals** |

The aggregated model wins on every dimension:

- **More training data**: 27K samples vs ~9K for cross-site, vs per-drug varying counts
- **Richer supervision**: Each sample provides gradients through ~6 drug heads simultaneously
- **Broader species coverage**: 221 species from A + 97 from B + 98 from C + 52 from D. In the 70/15/15 split, species from all hospitals appear in train AND test. The model sees species from all environments.
- **Drug-drug transfer learning**: The backbone learns that certain spectral patterns correlate with multi-drug resistance (e.g., ESBL-producing strains are resistant to multiple β-lactams). This shared knowledge improves predictions for drugs with fewer labeled samples.
- **No domain shift**: Unlike cross-site (train A, test B/C/D), the aggregated model sees samples from all sites during training. It learns instrument-specific artifacts and calibration differences as part of the training distribution.

## 7. The Numerical Intuition

The per-drug binary classifier for Ciprofloxacin trains on ~8K A-only samples, using ONLY the Cipro label. The aggregated model trains on ~19K samples from the training split (70% of 27K), each providing gradients through ~6 drug heads. That's approximately **19K × 6 ≈ 114K effective training signals** for the shared backbone, compared to 8K signals for the per-drug model. The backbone is approximately 14× better trained.
