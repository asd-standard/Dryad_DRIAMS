Loss-Curve Diagnostics (02)
===========================

Per-epoch training histories from the main 02 notebook
(:notebook:`02-MLPClassifier-Aggregated.ipynb <02-MLPClassifier-Aggregated/02-MLPClassifier-Aggregated.ipynb>`): pooled A+B+C+D, 70/15/15
:term:`species-stratified split`, seed 42. The three variants are the ones
described on :doc:`index`:

- **Baseline**: no :term:`Dropout`, no weight decay, lr 1e-4, batch size 32,
  100 epochs (Ciprofloxacin only).
- **Regularised**: :term:`Dropout` and weight decay with a 10-epoch warmup;
  the lr × dropout grid (coarse 8×8 + fine 5×5) is searched on Ciprofloxacin
  and the winning configuration is reused for the other two drugs.
- **Attention**: fixed configuration (lr 1e-3, dropout 0.4/0.2, weight decay
  1e-3, batch size 32, 100 epochs), not tuned.

Setup
-----

- Internal validation: 10% of the training split for :term:`Early stopping`
  (patience 10, best-validation weights restored)
- External validation: the 15% split, used for the metrics below
- Outputs: ``results_mlp_aggregated/metrics_*.csv``

Per-Epoch Curves
----------------

.. figure:: /_static/02-MLPClassifier-Aggregated/mlp_loss_curves.svg
   :alt: Per-epoch train and validation loss for the seven logged MLP runs
   :width: 100%

   Per-epoch cross-entropy for the seven logged runs (blue = train,
   orange = validation; both solid lines), with the best-validation epoch
   marked.

Overfitting by Variant
----------------------

.. list-table::
   :header-rows: 1

   * - Run
     - Best epoch
     - Stopped
     - Gap at best
     - Final gap
   * - Ciprofloxacin, baseline
     - 2
     - 12
     - +0.028
     - +0.544
   * - Ciprofloxacin, regularised
     - 14
     - 24
     - +0.123
     - +0.212
   * - Ciprofloxacin, attention
     - 3
     - 13
     - +0.017
     - +0.365
   * - Amoxicillin-Clavulanic acid, regularised
     - 16
     - 26
     - +0.040
     - +0.147
   * - Amoxicillin-Clavulanic acid, attention
     - 2
     - 12
     - -0.010
     - +0.439
   * - Gentamicin, regularised
     - 30
     - 40
     - +0.127
     - +0.190
   * - Gentamicin, attention
     - 2
     - 12
     - -0.001
     - +0.288

Gap = validation − train cross-entropy. The regularised variant trains longer
(best epoch 14–30, stopping at 24–40) and ends with moderate final gaps
(+0.15 to +0.21); baseline and attention overfit by epoch 2–3 and end with
gaps up to +0.54. The slightly negative gaps of the attention models on
Amoxicillin-Clavulanic acid and Gentamicin come from the heavy dropout
(0.4/0.2) combined with a small validation split. Because the best-validation
checkpoint is used, these dynamics do not degrade the reported test metrics.

.. note::

   The standalone diagnostic :notebook:`02-01-Loss-Curves.ipynb <02-MLPClassifier-Aggregated/02-01-Loss-Curves.ipynb>` retrains one MLP per
   drug with the best hyperparameters from 07 (pooled A+B+C+D) and logs
   per-epoch loss and AUROC. Those curves document 07's configurations, not
   the ones above, and live in
   :doc:`07 loss curves </07-Dedicated-MLP-Aggregated/loss-curves>`.
