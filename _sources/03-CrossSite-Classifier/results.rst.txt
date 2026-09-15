Cross-Site Results
==================

Results are generated as heatmaps showing :term:`Balanced Accuracy` and :term:`AUC-ROC`
for each model × target site combination.

Model Configuration (per drug)
------------------------------

Both LR and MLP are evaluated with per-drug hyperparameters found via
internal cross-validation on Site A's training data. Thresholds are
tuned per site.

Files
-----

- ``lr_cross_site_heatmap.pdf`` — LR (L2 and PCA+L2) per drug × per site
- ``mlp_cross_site_heatmap.pdf`` — MLP (Regularised and Attention) per drug × per site
- ``LR-Cross-Site-Summary.txt`` — Text summary of LR results
- ``MLP-Cross-Site-Summary.txt`` — Text summary of MLP results
- ``cross_site_best_per_drug.pdf`` — Best-performing method per drug

Interpretation
--------------

- Performance drops 10–30% compared to :term:`Aggregated (pooled) training` (01/02)
- Site D (Viollier) is consistently hardest: different instrument
  calibration, broader patient population, different species distribution
- The gap between :term:`Cross-site evaluation` and :term:`Aggregated (pooled) training`
  provides an upper bound on the benefit of pooling data — and therefore an
  upper bound on what :term:`Federated learning` can theoretically recover
