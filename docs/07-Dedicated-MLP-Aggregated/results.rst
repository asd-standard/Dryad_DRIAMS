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

Aggregate Results (pooled test, 70/15/15)
-----------------------------------------

.. list-table::
   :header-rows: 1

   * - Drug
     - LR BalAcc
     - LR AUC
     - MLP BalAcc
     - MLP AUC
     - RF BalAcc
     - RF AUC
   * - Ciprofloxacin
     - 0.716
     - 0.798
     - 0.733
     - 0.792
     - 0.678
     - 0.795
   * - Gentamicin
     - 0.791
     - 0.859
     - 0.780
     - 0.830
     - 0.767
     - 0.865
   * - Amoxicillin-Clavulanic acid
     - 0.822
     - 0.892
     - 0.830
     - 0.888
     - 0.815
     - 0.883
   * - Piperacillin-Tazobactam
     - 0.730
     - 0.818
     - 0.740
     - 0.800
     - 0.728
     - 0.808
   * - Cefepime
     - 0.835
     - 0.901
     - 0.836
     - 0.898
     - 0.809
     - 0.891
   * - Ceftriaxone
     - 0.786
     - 0.868
     - 0.786
     - 0.847
     - 0.749
     - 0.850
   * - Imipenem
     - 0.892
     - 0.957
     - 0.869
     - 0.938
     - 0.879
     - 0.951
   * - Ceftazidime
     - 0.701
     - 0.776
     - 0.684
     - 0.740
     - 0.686
     - 0.759
   * - Vancomycin
     - 0.886
     - 0.913
     - 0.849
     - 0.882
     - 0.897
     - 0.901
   * - Amikacin
     - 0.723
     - 0.836
     - 0.732
     - 0.869
     - 0.606
     - 0.729
   * - **Mean**
     - **0.788**
     - **0.862**
     - **0.784**
     - **0.848**
     - **0.761**
     - **0.843**

BalAcc values come from ``results_balacc.csv``, AUC-ROC values from
``results_auc.csv``; RF results are read from ``rf_results.pkl``. The Random
Forest is tuned on the same pooled split but with its own
:term:`GridSearchCV` and :term:`Threshold Tuning`.

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

.. figure:: /_static/07-Dedicated-MLP-Aggregated/heatmap_all.svg
   :alt: Dedicated per-drug Balanced Accuracy and AUC-ROC heatmaps for LR, MLP and RF
   :width: 100%

   Pooled test Balanced Accuracy (left) and AUC-ROC (right) per drug for
   LR, MLP and RF.

.. figure:: /_static/07-Dedicated-MLP-Aggregated/barchart_all.svg
   :alt: Pooled test Balanced Accuracy bar chart for LR, MLP and RF
   :width: 100%

   Pooled test Balanced Accuracy per drug for the three model families.

Per-Drug Patterns
-----------------

- LR and MLP are effectively tied on average; the MLP leads on Ciprofloxacin,
  Amoxicillin-Clavulanic acid, Piperacillin-Tazobactam and Amikacin, while LR
  leads on Gentamicin, Imipenem, Ceftazidime and Vancomycin.
- RF stays close in AUC but is weaker in Balanced Accuracy; it is the best
  model on Vancomycin and the weakest on Amikacin, where the few resistant
  samples make the decision threshold fragile.
- The class-imbalanced drugs are the least stable across model families and
  metrics, which is why the aggregated study (08) tracks both BalAcc and AUC.

Threshold Selection
-------------------

Decision thresholds are selected differently per model family: LR and RF
tune the threshold with 3-fold cross-validated predictions within the
training split (``cross_val_predict``), while the MLP tunes it on the
external validation split. The per-site worst-case threshold protocol used
by the federated clients is documented in
:doc:`08 </08-Federated-mlp-lr-rf/methodology>`.

Loss Histories and Model Weights
--------------------------------

07 does not persist per-epoch training histories, and the MLP weights are not
saved (the ``models/`` directory is empty; only the Random Forest checkpoints
in ``rf_checkpoints/`` are kept). The loss curves for the hyperparameters
selected here come from diagnostics that retrain the same configurations:

- :doc:`Loss curves for the 07 hyperparameters <loss-curves>` — pooled
  best-config reruns (02-01, A+B+C+D) and A-only reruns (03-01), with the
  implementation caveats.

The reruns use ``MaldiMLPClassifier`` rather than 07's custom PyTorch loop, so
the curves are representative of the selected configurations, not bit-identical
to the 07 models (whose final training runs up to 100 epochs with cosine
``T_max=90`` and starts from the best grid combination).

Class Weight Ablation
---------------------

:notebook:`07-02-Dedicated-MLP-ClassWeight.ipynb <07-Dedicated-MLP-Aggregated/07-02-Dedicated-MLP-ClassWeight.ipynb>` explores whether inverse-frequency
:term:`Class weight` improves :term:`MLP` performance, particularly for drugs with
highly imbalanced resistance labels (some drugs have <5% resistant
samples).
