# Final Multi-Label AMR Classifier Analysis Report

## 1. Data Pipeline & Reproducibility

### Data Sourcing
- **Source Sites:** DRIAMS-A (Train/Val), DRIAMS-B, C, D (External Test).
- **Features:** 6,000 bins representing MALDI-TOF spectra intensities.
- **Labels:** 10 drugs selected: Ciprofloxacin, Gentamicin, Amoxicillin-Clavulanic acid, Piperacillin-Tazobactam, Cefepime, Ceftriaxone, Imipenem, Ceftazidime, Vancomycin, Amikacin.

### Preprocessing Flow
- **Transformation:** `log1p(x)` followed by `StandardScaler`.
- **Consistency:** Scaling parameters are always fitted on the specific training set and applied to validation/test sets to prevent leakage.
- **Handling Missing Labels:** Multi-label Binary Cross Entropy loss with masking. NaN values in the label matrix are ignored during backpropagation.

### Training & Evaluation Protocol
- **Splitting:** Species-stratified splitting using `stratified_species_drug_split`.
- **Metric:** Balanced Accuracy (average of Sensitivity and Specificity).
- **Threshold Tuning:** Per-drug thresholds tuned on validation set (0.05 to 0.95).

## 2. Model Parameters & Grids

### Architecture
- **Model Type:** `SpectralAttentionMLP` (Multi-head MLP).
- **Optimizer:** AdamW with Weight Decay (1e-4) and Cosine Annealing.

### Best Found Parameters
- **Cross-Site Model (Train A):** LR=1.8e-04, Dropout=0.20.
- **Aggregated Model (Train A+B+C+D):** LR=2.6e-04, Dropout=0.36.

## 3. Results Summary

### Performance Comparison (Test set: B+C+D combined)

| Drug            |   Cross-Site MLP (A->B+C+D) |   Aggregated MLP (70/15/15) |   OneVsRest LR (Baseline) |
|:----------------|----------------------------:|----------------------------:|--------------------------:|
| Ciprofloxacin   |                    0.617254 |                    0.705732 |                  0.767577 |
| Gentamicin      |                    0.568299 |                    0.802992 |                  0.806152 |
| Amoxicillin-Cla |                  nan        |                  nan        |                nan        |
| Piperacillin-Ta |                    0.519218 |                    0.746737 |                  0.736142 |
| Cefepime        |                    0.600688 |                    0.82954  |                  0.875691 |
| Ceftriaxone     |                    0.650722 |                    0.778749 |                  0.728744 |
| Imipenem        |                    0.646657 |                    0.888598 |                  0.915668 |
| Ceftazidime     |                    0.572988 |                    0.663878 |                  0.741373 |
| Vancomycin      |                    0.808262 |                    0.771379 |                  0.887325 |
| Amikacin        |                    0.629878 |                    0.691031 |                  0.865815 |

## 4. Artifacts & Visualizations
All graphs saved to `/content/drive/MyDrive/Flower/DRIAMS-DataSet/Processed/Processing/Analysis/04-MultiLabel-CLassifier`:
- `multilabel_final_comparison.pdf`: Primary comparison chart.
- `mlp_multilabel_heatmap.pdf`: Site-by-site breakdown (MLP).
- `lr_multilabel_heatmap.pdf`: Site-by-site breakdown (LR Baseline).