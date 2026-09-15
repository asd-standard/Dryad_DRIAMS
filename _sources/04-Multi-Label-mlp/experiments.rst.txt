Sub-Experiments
===============

Six progressive experiments explore variations of the multi-label MLP.

00 — Base Multi-Label MLP
--------------------------

**Notebook**: ``04-00-MultiLabel-CLassifier/04-MultiLabel-Classifier.ipynb``

The baseline: :term:`Shared backbone` with 10 sigmoid heads,
:term:`Masked BCE loss`, 6×6 grid search on lr×dropout. Compared against
:term:`OneVsRest` :term:`LogisticRegression`.

01 — CNN Classifier
-------------------

**Notebook**: ``04-01-MultiLabel-Cnn-Classifier/04-01-MultiLabel-Cnn-Classifier.ipynb``

Replaces the MLP backbone with a 1D convolutional architecture over the
6000-bin spectrum. Tests whether local spectral patterns (adjacent m/z
bins) are more informative than a fully-connected first layer.

02 — MLP with Attention
------------------------

**Notebook**: ``04-02-MultiLabel-MLP-Attention/04-02-MultiLabel-MLP-Attention.ipynb``

Adds a :term:`sigmoid-gated attention` mechanism to the 512-dim hidden layer.
The model learns to dynamically weight spectral features per sample.
Tests whether attention, which helped in the per-drug MLP (02), also
helps in the multi-label setting.

03 — Wider Backbone Ablation
----------------------------

**Notebook**: ``04-03-Wider-Backbone-Ablation/04-03-Wider-Backbone-Ablation.ipynb``

Explores wider hidden dimensions: 1024 and 2048 instead of 512. Tests
whether a larger backbone helps with the multi-task learning setup or
simply overfits.

04 — Class Weight
-----------------

**Notebook**: ``04-04-MultiLabel-ClassWeight/04-04-MultiLabel-ClassWeight.ipynb``

Applies inverse-frequency :term:`Class weight` to address label imbalance
(typically ~80% susceptible / ~20% resistant). Per-drug weights are
computed from the training set.

05 — Adaptive Class Weight
---------------------------

**Notebook**: ``04-05-MultiLabel-AdaptiveClassWeight/04-05-MultiLabel-AdaptiveClassWeight.ipynb``

Class weights are updated dynamically during training based on current
predictions, penalising drugs/classes where the model is performing
poorly. Aims to balance optimisation across all 10 drugs simultaneously.
