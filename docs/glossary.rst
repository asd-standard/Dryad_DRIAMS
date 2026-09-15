Glossary
========

.. glossary::
   :sorted:

   LogisticRegression
      Scikit-learn linear classifier for binary outcomes. Estimates
      :math:`P(\text{resistant} \mid \text{spectrum})` via the logistic
      function. Used with L2 regularisation throughout the DRIAMS analysis
      as the linear baseline.

   L2 regularization
      Penalises large coefficient values in logistic regression.
      Controlled by the ``C`` parameter (inverse regularisation strength).
      Prevents overfitting and improves cross-site generalisation.

   default threshold
      Hard classification boundary at 0.5. A sample is predicted resistant
      if :math:`P(\text{resistant}) \geq 0.5`. Tuning this threshold per-drug
      consistently improves balanced accuracy.

   Threshold Tuning
      Optimising the decision threshold via cross-validation to maximise
      worst-site :term:`Balanced Accuracy`. Evaluated over a grid of thresholds
      (typically 5%–95%) and selecting the one with highest minimum
      per-site performance.

   PCA
      Principal Component Analysis. Linear dimensionality reduction that
      projects data onto orthogonal axes retaining maximum variance. Applied
      to reduce 6000-bin spectra to a lower-dimensional representation before
      classification.

   Dimensionality reduction
      Techniques (PCA, autoencoders, etc.) that project high-dimensional
      input data into fewer dimensions while preserving relevant structure.
      In MALDI-TOF analysis, tested as a denoising step before classification.

   log1p transform
      :math:`\log(1 + x)` applied element-wise to MALDI-TOF intensity values.
      Stabilises heavy-tailed distributions and brings dynamic range into a
      manageable scale.

   Standardize to zero mean
      Z-score normalisation: subtract the training-set mean and divide by the
      training-set standard deviation. Fit on train only; applied to all
      subsequent splits to prevent data leakage.

   species-stratified split
      Train/validation/test split that ensures no bacterial species appears
      in more than one partition. Forces the model to generalise across
      species rather than memorising species-specific spectral signatures.

   Balanced Accuracy
      Arithmetic mean of sensitivity and specificity:
      :math:`\frac{1}{2}(\frac{\text{TP}}{\text{TP}+\text{FN}} + \frac{\text{TN}}{\text{TN}+\text{FP}})`.
      Robust to class imbalance, used as the primary metric throughout the
      DRIAMS analysis.

   AUC-ROC
      Area Under the Receiver Operating Characteristic curve. A
      threshold-independent ranking metric; 1.0 = perfect, 0.5 = random.
      Reported alongside :term:`Balanced Accuracy` for all models.

   MLP
      Multilayer Perceptron. Feedforward neural network of fully-connected
      layers with non-linear activation functions. The DRIAMS MLP uses
      6000→512→256→128→2 architecture.

   SpectralAttentionMLP
      MaldiDeepKit's MLP implementation. Supports :term:`BatchNorm`,
      :term:`Dropout`, and optional :term:`sigmoid-gated attention`.
      Architecture: 6000→512→256→128→2 with :term:`ReLU` activations.

   BatchNorm
      Batch Normalisation. Normalises layer activations to zero mean / unit
      variance per mini-batch. Stabilises training, allows higher learning
      rates, and provides mild regularisation.

   Dropout
      Randomly zeros a fraction of neurons during training (controlled by
      dropout probability ``p``). Prevents co-adaptation of neurons and
      reduces overfitting. At inference time, all neurons are active and
      outputs are scaled by ``1-p``.

   ReLU
      Rectified Linear Unit activation: :math:`\max(0, x)`. Introduces
      non-linearity into the MLP. Used after every :term:`BatchNorm` layer
      in the DRIAMS architecture.

   sigmoid-gated attention
      Learned element-wise gating on hidden representations. A sigmoid
      function generates per-feature weights in (0,1), allowing the model
      to dynamically amplify or suppress specific spectral features.

   AdamW
      Adam optimiser with decoupled weight decay. Separates the
      regularisation term from the adaptive gradient updates, providing
      better generalisation than standard Adam with L2 regularisation.

   Cosine annealing
      Learning rate schedule that follows :math:`\eta(t) = \eta_{\min} +
      \frac{1}{2}(\eta_{\max} - \eta_{\min})(1 + \cos(\pi t / T_{\max}))`.
      Smoothly decays learning rate, aiding convergence to better minima.

   Early stopping
      Halts training when validation loss stops improving. Patience
      (N epochs without improvement) prevents overfitting while giving
      the optimiser time to escape plateaus. Typical patience is 10–15.

   Cross-site evaluation
      Training on data from one hospital site and testing on others.
      Measures a model's ability to generalise across different instruments,
      patient populations, and bacterial ecologies.

   Domain shift
      Distribution mismatch between training and test domains caused by
      different MALDI-TOF instruments, calibration protocols, patient
      demographics, or bacterial species composition across hospital sites.

   DRIAMS
      **D**\Ried **M**\icrobes **A**\nd **M**\ass **S**\pectra dataset.
      Four Swiss hospital sites:
      **A** — University Hospital Basel,
      **B** — Canton Basel-Land,
      **C** — Canton Aarau,
      **D** — Viollier (private diagnostic lab).
      Spectra are binned at 3 Da resolution producing 6000 features.

   Multi-label classification
      Predicting multiple binary outcomes from a single input. One MALDI-TOF
      spectrum → 10 independent resistance probabilities (one per drug).
      Contrasts with :term:`per-drug model` binary classification.

   Shared backbone
      Hidden layers shared across all output heads in a multi-label
      architecture. Learns general spectral features useful for predicting
      resistance to all drugs simultaneously. Enables inter-drug transfer
      learning.

   Masked BCE loss
      Binary Cross-Entropy computed only on known (non-NaN) labels. Each
      sample contributes gradients only through drug heads for which a
      resistance label exists. NaN positions are excluded from the loss sum.

   Label masking
      Multiplying per-sample per-drug loss by a binary mask where known
      labels = 1.0 and untested drugs = 0.0. The mathematically correct way
      to handle partial label matrices with missing entries.

   OneVsRest
      Decomposes a multi-label problem into N independent binary classifiers.
      For 10 drugs, this trains 10 separate binary classifiers. Serves as the
      linear baseline for :term:`multi-label classification`.

   Class weight
      Inverse-frequency weighting applied to the loss function. Rare classes
      (typically resistant samples, ~20% of data) receive higher weight,
      penalising their misclassification more heavily.

   Random Forest
      Ensemble of decision trees, each trained on a bootstrap sample with
      a random subset of features considered at each split. Averages
      predictions across all trees. Robust, interpretable, and handles
      tabular data well.

   n_estimators
      Number of trees in a :term:`Random Forest`. More trees reduce variance
      at the cost of memory and inference time. Typical values: 100–500.

   max_depth
      Maximum depth of each decision tree. Limits overfitting by preventing
      trees from growing too complex. ``None`` = no limit; trees grow until
      leaves are pure or :term:`min_samples_leaf` is reached.

   min_samples_leaf
      Minimum number of samples required to be at a leaf node. Higher values
      enforce simpler trees and stronger regularisation. Typical values:
      2, 5, 10.

   Feature importance
      A ranking of input features (m/z bins) by their contribution to
      prediction accuracy. Computed via mean decrease in impurity (Gini)
      or permutation importance. Reveals which spectral regions are
      predictive of resistance.

   GridSearchCV
      Exhaustive search over all combinations of specified hyperparameter
      values, evaluating each via cross-validation. Returns the combination
      with the best average score. Used for LR, MLP, and RF tuning.

   RandomizedSearchCV
      Random sampling of hyperparameter combinations from specified
      distributions. Faster than :term:`GridSearchCV` when the search
      space is large. Used for RF tuning in 05 and 08.

   Aggregated (pooled) training
      Pooling data from all 4 :term:`DRIAMS` sites into a single training
      set before fitting a model. The centralized upper bound; federated
      learning aims to match or approach this performance without sharing
      raw data.

   Warm-start training
      Initialising model weights from a previously trained run rather than
      from scratch. Preserves learned knowledge across runs, accelerating
      convergence and enabling incremental model evolution.

   Federated learning
      Training machine learning models across decentralised data without
      moving raw data. Each site trains a local model; only model updates
      (weights, coefficients, or trees) are shared and aggregated at a
      central server.

   Per-drug model
      Independent binary classifier trained on a single drug's data. The
      default AMR prediction paradigm: one model per drug, each seeing
      only that drug's resistance labels. Contrasts with
      :term:`multi-label classification`.

   Species masking
      Filtering the training set by species present in the test set before
      fitting a centralized baseline. Variants:

      ``none``
         Full training data, no species filtering — the true upper bound.

      ``union``
         Only species present in at least one test site. Prevents the
         centralized model from benefiting from species it never evaluates on.

      ``majority``
         Only the target species (e.g., *E. coli*). The purest comparison.

      ``persite``
         Per-site species filtering, simulating local client distributions.

      Ensures the centralized baseline uses a species composition comparable
      to what federated clients see locally. Used in 06b for fair
      centralized-vs-federated comparisons.

   best_params.csv
      CSV file produced by 07 containing the optimal ``C`` for
      :term:`LogisticRegression` and ``lr``/``dropout`` for
      :term:`MLP` per drug. Consumed directly by the federated notebooks
      in 08 to set client hyperparameters.

   Flower (flwr)
      Open-source federated learning framework. Provides NumPy-based and
      PyTorch client/server APIs plus :term:`Ray simulation` for local
      testing. Used throughout the DRIAMS federated experiments
      (06b, 08).

   FedAvg
      Federated Averaging. The server aggregates client model weights via
      a weighted average (weighted by local dataset size). The baseline
      federated strategy against which all others are compared.

   FedProx
      Federated Proximal. An extension of :term:`FedAvg` that adds a
      proximal term to each client's loss, penalising weight divergence
      from the global model. Improves stability when client dataset sizes
      are highly imbalanced.

   Proximal term (μ)
      The penalty coefficient in :term:`FedProx`. The client loss becomes
      :math:`\mathcal{L}_{\text{CE}} + \frac{\mu}{2} \|w_{\text{client}} -
      w_{\text{global}}\|^2`. Higher μ enforces stronger adherence to the
      global model. Value tuned per drug.

   FedLR
      Federated Logistic Regression. Warm-started scikit-learn
      :term:`LogisticRegression` clients trained with :term:`FedAvg`.
      Solver: SAGA (supports sparse gradients and warm-starting).

   FedRF
      Federated Random Forest. Each client trains local trees;
      the global model is the union of all client trees via
      :term:`Tree collection`. Grows the ensemble size linearly with
      rounds and client count.

   Tree collection
      Aggregation strategy for :term:`FedRF`. Trees from all clients are
      concatenated into a single growing ensemble. Fundamentally different
      from weight averaging: the ensemble simply accumulates trees across
      rounds.

   Mixing
      Training multiple random-seed copies on small sites and averaging
      their weights before sending to the server. Reduces variance from
      small local datasets. Number of mixes scales inversely with site size.

   Ray simulation
      Flower's local simulation backend using Ray actors to run multiple
      clients in parallel on a single machine. No real network
      communication; clients communicate through in-memory parameter
      exchange.

   Checkpoint
      Per-round save of per-client and global model weights to disk. Enables
      resumption of interrupted runs, post-hoc analysis, and comparison of
      client model divergence across rounds.
