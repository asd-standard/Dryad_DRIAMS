Results and Outputs
====================

Grid Results
------------

The 8×8 :term:`GridSearchCV` over learning rate and dropout produces
per-drug optimal configurations. Results are stored in:

- ``07-01-results_dedicated_lr_mlp/best_params.csv`` — Optimal LR(C) and
  MLP(lr, dropout) per drug (:term:`best_params.csv`)
- ``07-01-results_dedicated_lr_mlp/results_balacc.csv`` — :term:`Balanced Accuracy`
  per drug × per model
- ``07-01-results_dedicated_lr_mlp/results_auc.csv`` — :term:`AUC-ROC` per drug ×
  per model

RF Checkpoints
--------------

- ``results_dedicated_lr_mlp/rf_results.pkl`` — Serialised RF test-set
  results (BalAcc, AUC) per drug
- ``rf_checkpoints/`` — Trained RF models per drug (joblib format)

Heatmaps
--------

Model × drug heatmaps provide an at-a-glance comparison of all three
model families across all drugs for both :term:`Balanced Accuracy` and
:term:`AUC-ROC`.

Class Weight Ablation
---------------------

``07-02-Dedicated-MLP-ClassWeight.ipynb`` explores whether inverse-frequency
:term:`Class weight` improves :term:`MLP` performance, particularly for drugs with
highly imbalanced resistance labels (some drugs have <5% resistant
samples).
