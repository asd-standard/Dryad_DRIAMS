Loss-Curve Diagnostics (04)
===========================

Per-epoch training histories for the three reported runs:

- **04-00 cross-site MLP** — trained on A only with the best grid
  configuration (lr 1e-4, dropout 0.36), retrained for up to 100 epochs
- **04-00 aggregated MLP** — pooled A+B+C+D, species-stratified 70/15/15,
  best configuration (lr 1.8e-4, dropout 0.44)
- **04-01 shared CNN** — pooled 70/15/15, best configuration (lr 1e-5,
  dropout 0.2)

Setup
-----

- **Internal validation**: 10% of the training split, species-stratified,
  logs masked-BCE loss and validation macro :term:`Balanced Accuracy` at the
  default 0.5 threshold. It selects the best-validation-loss checkpoint
  (patience 15 in the final runs).
- **External validation**: A-val or the aggregated validation split; used for
  grid scoring and per-drug :term:`Threshold Tuning` only.
- **Outputs**: ``history_crosssite.csv``, ``history_aggregated.csv``,
  ``history_cnn.csv`` in the two results folders.
- Exported test metrics always come from the best-validation-loss checkpoint,
  not from the final epoch or the epoch with the highest Balanced Accuracy.

Cross-Site Shared MLP
---------------------

.. figure:: /_static/04-Multi-Label-mlp/04_loss_curves_crosssite.svg
   :alt: Per-epoch train and validation loss and validation macro Balanced Accuracy for the cross-site shared MLP
   :width: 100%

   Cross-site shared MLP: masked-BCE loss (left) and validation macro
   Balanced Accuracy at 0.5 (right). Dotted line marks the best-val-loss
   epoch (14).

Aggregated Shared MLP
---------------------

.. figure:: /_static/04-Multi-Label-mlp/04_loss_curves_aggregated.svg
   :alt: Per-epoch train and validation loss and validation macro Balanced Accuracy for the aggregated shared MLP
   :width: 100%

   Aggregated shared MLP: same layout; best-val-loss epoch 10.

Shared CNN
----------

.. figure:: /_static/04-Multi-Label-mlp/04_cnn_loss_curves.svg
   :alt: Per-epoch train and validation loss and validation macro Balanced Accuracy for the shared CNN
   :width: 100%

   Shared CNN: best-val-loss epoch 35; training stops at 50 after patience 15.

Per-Run Summary
---------------

.. list-table::
   :header-rows: 1

   * - Run
     - Best epoch (val loss)
     - Val macro BalAcc at best
     - Max val macro BalAcc (epoch)
     - Gap at best
     - Final gap
     - Epochs trained
   * - 04-00 MLP cross-site
     - 14
     - 0.742
     - 0.776 (29)
     - +0.079
     - +0.224
     - 29
   * - 04-00 MLP aggregated
     - 10
     - 0.703
     - 0.730 (24)
     - +0.047
     - +0.237
     - 25
   * - 04-01 CNN aggregated
     - 35
     - 0.640
     - 0.689 (41)
     - +0.129
     - +0.201
     - 50

Gap = validation − train masked BCE. Validation macro Balanced Accuracy is
recorded at the default 0.5 threshold (the exported metrics use per-drug
tuned thresholds instead).

Interpretation
--------------

- **Calibration drift vs ranking.** The cross-site MLP reaches its lowest
  validation loss at epoch 14 (0.252) and then overfits: train loss continues
  to 0.069 while validation loss rises to 0.293. Validation Balanced Accuracy
  nevertheless keeps improving, ending at 0.776 on epoch 29. Loss and ranking
  quality therefore point at different epochs, and the exported model is the
  epoch-14 checkpoint (validation Balanced Accuracy 0.742), not the
  curve maximum.
- **Aggregated MLP overfits after epoch 10.** The gap at the best epoch is
  small (+0.047) and grows to +0.237 by epoch 25; validation Balanced
  Accuracy creeps from 0.703 to 0.730 against the rising loss.
- **CNN training is noisier and slower.** The validation loss bottoms at
  epoch 35, and validation Balanced Accuracy oscillates in a 0.60–0.69 band
  without a clear trend; early stopping ends the run at epoch 50. The
  checkpoint score (0.640) is well below the curve maximum (0.689, epoch 41),
  another instance of the checkpoint/curve-max mismatch.
- **Validation does not predict transfer.** For the cross-site MLP, validation
  macro Balanced Accuracy reaches 0.776 while the same model scores 0.635 on
  B+C+D — a validation-to-transfer gap of ~0.14. Combined with 03's
  correlation of 0.59–0.68 between A-val and cross-site scores, model
  selection on a single validation split is weak evidence for generalisation.
  For the aggregated runs the logged validation curve (max 0.730 MLP, 0.689
  CNN) sits *below* the test scores (0.775, 0.762), because the curve uses the
  default 0.5 threshold while the test metrics use per-drug thresholds tuned
  on the validation split — the two are not directly comparable.
- **Reproducibility.** Histories come from single-seed runs (seed 42); no
  confidence intervals are available. The standalone diagnostic 04-06
  (``04-06-Loss-Curves``) is deprecated — the main notebooks now log histories
  directly.
