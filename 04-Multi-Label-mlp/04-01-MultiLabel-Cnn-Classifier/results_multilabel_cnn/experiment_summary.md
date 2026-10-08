# Experiment Summary: Multi-Label CNN vs Logistic Regression

## Data Pipeline & Preprocessing
- **Data Source**: DRIAMS (Sites A, B, C, D) aggregated into a single dataset.
- **Feature Engineering**: Raw MALDI-TOF spectra binned into 6,000 intensity bins.
- **Transformations**:
    - `log1p`: Logarithmic transformation applied to handle intensity variance.
    - `Standardization`: Features scaled to zero mean and unit variance based on training set statistics.
- **Data Splitting**:
    - **Strategy**: Species-stratified 70/15/15 split.
    - **Distribution**: Train=18648, Val=3997, Test=3997.
    - **Seed**: 42.

## Model & Training Configuration
- **Architecture**: 1D Convolutional Neural Network with 4 Conv layers, BatchNorm, ReLU, Adaptive Average Pooling (16), and 10 independent Sigmoid output heads.
- **Optimization Strategy**:
    - **Optimizer**: AdamW (Weight Decay: 1e-4).
    - **Scheduler**: CosineAnnealingLR with 10-epoch linear warmup.
    - **Loss Function**: Masked Binary Cross-Entropy (handling missing labels per sample).
    - **Early Stopping**: Patience of 15 epochs on validation loss.
- **Hyperparameter Search**:
    - **LR Grid**: [np.float64(5e-05), np.float64(0.00024), np.float64(0.00043), np.float64(0.00062), np.float64(0.00081), np.float64(0.001)]
    - **Dropout Grid**: [np.float64(0.1), np.float64(0.18), np.float64(0.26), np.float64(0.34), np.float64(0.42), np.float64(0.5)]
    - **Selected Best**: LR=5.0e-05, Dropout=0.50.
- **Threshold Tuning**: Optimal per-drug decision thresholds determined on the validation set using a 91-step grid search (0.05 to 0.95).

## Test Results (Balanced Accuracy)

| Drug            |   LR_OneVsRest |   CNN_Shared |
|:----------------|---------------:|-------------:|
| Ciprofloxacin   |       0.704104 |     0.704678 |
| Gentamicin      |       0.796816 |     0.78478  |
| Amoxicillin-Cla |     nan        |   nan        |
| Piperacillin-Ta |       0.714743 |     0.698742 |
| Cefepime        |       0.820748 |     0.769126 |
| Ceftriaxone     |       0.764884 |     0.750048 |
| Imipenem        |       0.890088 |     0.866598 |
| Ceftazidime     |       0.668783 |     0.629304 |
| Vancomycin      |       0.870313 |     0.827698 |
| Amikacin        |       0.715107 |     0.56883  |

## Visual Comparison
![CNN vs LR Comparison](cnn_vs_lr_comparison.png)

## Per-Drug CNN Thresholds

| Drug                        |   Threshold |
|:----------------------------|------------:|
| Ciprofloxacin               |        0.17 |
| Gentamicin                  |        0.23 |
| Amoxicillin-Clavulanic acid |        0.5  |
| Piperacillin-Tazobactam     |        0.11 |
| Cefepime                    |        0.13 |
| Ceftriaxone                 |        0.35 |
| Imipenem                    |        0.13 |
| Ceftazidime                 |        0.16 |
| Vancomycin                  |        0.08 |
| Amikacin                    |        0.06 |