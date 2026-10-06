Loss-Curve and Parameter-Selection Diagnostics
==============================================

Standalone diagnostic implemented in ``03-01-Loss-Curves.ipynb``. The main
:doc:`03 notebook <index>` grid-searches lr × dropout per drug on A and
reports BalAcc/AUC, but does not persist the per-epoch loss history. The
03-01 notebook retrains **one MLP per drug** on DRIAMS-A using the best
hyperparameters from 07 (:term:`best_params.csv`), with the same
:term:`species-stratified split` (80/20, seed 42), and logs per-epoch
metrics.

.. note::

   The 03-01 models use 07's hyperparameters, which need not coincide with
   the configurations selected by 03's own narrow grid (lr 7.5e-5–9.5e-5,
   dropout 0.5–0.8). The loss curves are therefore diagnostic of the
   07-configuration models, not of the exact models reported in
   :doc:`results`.

Setup
-----

- Train site: DRIAMS-A, species-stratified 80/20, seed 42
- Per-epoch log: train/val cross-entropy, learning rate, gradient norm, AUROC
- Internal validation: 10% of the training split (used for early stopping);
  the reported A-val metrics use the external 20% split
- Outputs: ``results_loss_curves_03/metrics_<drug>.csv``,
  ``results_loss_curves_03/summary_loss_curves_03.csv``,
  ``results_loss_curves_03/03_loss_curves.pdf``

Training Dynamics
-----------------

- **7 of 10 drugs trigger early stopping** (best epoch between 16 and 47);
  Amikacin, Imipenem and Vancomycin run the full 50 epochs with their best
  epoch at 45/45/48, i.e. still improving when the budget ends
- **Overfitting is systematic**: the val−train CE gap at the best epoch
  ranges from 0.015 (Amikacin) to 0.186 (Ceftriaxone), reaching 0.235 at the
  end of training. Example Ciprofloxacin: best at epoch 18 (val loss 0.493),
  after which val loss rises to 0.537 while train loss falls to 0.381
- **Metric instability with few resistant samples**: Amikacin shows internal
  AUROC 0.970 vs external A-val AUROC 0.742; Vancomycin reaches internal
  AUROC 0.999 with only 85 resistant isolates on A

Parameter-Selection Fragility
-----------------------------

.. list-table:: A-val Balanced Accuracy: 03-01 (07 params) vs 03 (own grid)
   :header-rows: 1

   * - Drug
     - 03-01
     - 03
     - Delta
   * - Ciprofloxacin
     - 0.718
     - 0.780
     - -0.063
   * - Gentamicin
     - 0.824
     - 0.853
     - -0.029
   * - Amoxicillin-Clavulanic acid
     - 0.815
     - 0.833
     - -0.017
   * - Piperacillin-Tazobactam
     - 0.798
     - 0.787
     - +0.011
   * - Cefepime
     - 0.869
     - 0.870
     - -0.001
   * - Ceftriaxone
     - 0.818
     - 0.815
     - +0.003
   * - Imipenem
     - 0.911
     - 0.907
     - +0.004
   * - Ceftazidime
     - 0.755
     - 0.754
     - +0.001
   * - Vancomycin
     - 0.929
     - 0.930
     - -0.001
   * - Amikacin
     - 0.763
     - 0.652
     - **+0.110**

Nine of ten drugs agree within ±0.06, but Amikacin improves by +0.110 with
07's configuration while Ciprofloxacin worsens by -0.063. Selecting
hyperparameters on a single A validation split is therefore fragile; the
attention MLP selects an even worse Amikacin model (A-val 0.500).

A-Validation Does Not Predict Transfer
--------------------------------------

- The correlation between A-val Balanced Accuracy and B+C+D is 0.59–0.64
  across the two runs
- Piperacillin-Tazobactam: 0.798 on A validation → 0.545 cross-site
- Amikacin: 0.763 on A validation (AUROC 0.742) → 0.554 cross-site
- The internal-vs-external metric gaps (Amikacin AUROC 0.970 vs 0.742)
  show that the model-selection signal is noisy with few resistant samples

Practical Implication
---------------------

A-only loss curves confirm overfitting but do not explain the cross-site
gap: models optimise well on A while transfer fails. Robust conclusions
require multiple seeds and confidence intervals plus cross-site evaluation
of the same model configurations, not finer hyperparameter search on a
single validation split.
