Loss Curves for the 07 Hyperparameters
======================================

07 does not persist per-epoch training histories or MLP weights. To visualise
how the configurations selected in 07 behave, two diagnostics retrain the same
hyperparameters with ``MaldiMLPClassifier`` and log every epoch:

- **Pooled** (:notebook:`02-01-Loss-Curves.ipynb <02-MLPClassifier-Aggregated/02-01-Loss-Curves.ipynb>`): pooled A+B+C+D, 70/15/15, 50
  epochs with a 10-epoch warmup.
- **A-only** (:notebook:`03-01-Loss-Curves.ipynb <03-CrossSite-Classifier/03-01-Loss-Curves.ipynb>`): DRIAMS-A only, 80/20, for the
  cross-site diagnostic.

The curves are representative of the selected configurations, not
bit-identical to the 07 models, whose custom PyTorch loop trains up to 100
epochs with cosine ``T_max=90`` and starts from the best grid combination.

Pooled (02-01)
--------------

.. figure:: /_static/07-Dedicated-MLP-Aggregated/02_loss_curves.svg
   :alt: Per-epoch loss and AUROC for the pooled best-config MLP runs
   :width: 100%

   Per-epoch train/val cross-entropy (top) and AUROC (bottom) for the pooled
   best-config runs; the dotted line marks the best-validation epoch.

.. list-table:: Best-config pooled runs (07 hyperparameters)
   :header-rows: 1

   * - Drug
     - lr
     - dropout
     - Epochs
     - Best epoch
     - Val BalAcc
     - Val AUC
     - Final gap
   * - Ciprofloxacin
     - 7.8e-5
     - 0.8
     - 17
     - 7
     - 0.700
     - 0.765
     - +0.196
   * - Amoxicillin-Clavulanic acid
     - 7.5e-5
     - 0.7
     - 21
     - 11
     - 0.823
     - 0.896
     - +0.174
   * - Gentamicin
     - 7.5e-5
     - 0.8
     - 23
     - 13
     - 0.785
     - 0.856
     - +0.247

- Overfitting starts early (best epoch 7–13) and the final gap reaches
  0.17–0.25; the best-validation checkpoint is therefore the model actually
  used.
- The AUROC panel peaks later than the loss minimum for Ciprofloxacin
  (0.766 at the best-loss epoch vs 0.808 at epoch 15) and Gentamicin
  (0.849 vs 0.863), while for Amoxicillin-Clavulanic acid the two coincide
  (0.897): checkpoint selection based on loss can stop slightly before the
  best-ranking model.
- The best-config models match the grid-searched 02 models on validation
  Balanced Accuracy (0.700 / 0.823 / 0.785 vs 0.707 / 0.819 / 0.784) while
  training for fewer epochs (17/21/23 vs 24/26/40). The 07 hyperparameters
  transfer well to the pooled setting.

A-only (03-01)
--------------

.. figure:: /_static/07-Dedicated-MLP-Aggregated/03_loss_curves.svg
   :alt: Per-epoch train and validation loss for the ten A-only MLP runs
   :width: 100%

   Per-epoch cross-entropy for the ten drugs trained on A (blue = train,
   orange = validation; both solid lines), with the best-validation epoch
   marked.

.. list-table:: Per-drug loss dynamics (03-01)
   :header-rows: 1

   * - Drug
     - Best epoch
     - Stopped
     - Gap at best
     - Final gap
     - AUROC at best
   * - Ciprofloxacin
     - 18
     - 28
     - +0.061
     - +0.156
     - 0.753
   * - Gentamicin
     - 38
     - 48
     - +0.132
     - +0.186
     - 0.874
   * - Amoxicillin-Clavulanic acid
     - 16
     - 26
     - +0.044
     - +0.191
     - 0.890
   * - Piperacillin-Tazobactam
     - 21
     - 31
     - +0.079
     - +0.162
     - 0.860
   * - Cefepime
     - 29
     - 39
     - +0.113
     - +0.221
     - 0.920
   * - Ceftriaxone
     - 37
     - 47
     - +0.186
     - +0.234
     - 0.854
   * - Imipenem
     - 45
     - 50
     - +0.124
     - +0.142
     - 0.943
   * - Ceftazidime
     - 25
     - 35
     - +0.162
     - +0.235
     - 0.770
   * - Vancomycin
     - 48
     - 50
     - +0.017
     - +0.017
     - 0.999
   * - Amikacin
     - 45
     - 50
     - +0.015
     - +0.016
     - 0.970

Gap = validation − train cross-entropy. Amikacin, Imipenem and Vancomycin run
to the 50-epoch budget with the best epoch at 45/45/48; the smallest gaps
(Amikacin, Vancomycin) rest on very few resistant isolates (47 and 85 on A),
so their internal AUROC is unreliable.

Where the Curves Belong
-----------------------

The 03 configuration used by the cross-site study has its own per-epoch
histories (regularised and attention), logged by the main 03 notebook and
documented in :doc:`03 loss curves </03-CrossSite-Classifier/loss-curves>`.
