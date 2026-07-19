04 — Multi-Label MLP Classifier
=================================

Train on :term:`DRIAMS`-A (9,443 samples), test on B, C, D. Predict resistance to
10 drugs simultaneously — :term:`Multi-label classification`.

.. _notebook: 04-00-MultiLabel-CLassifier/04-MultiLabel-Classifier.ipynb

.. toctree::
   :maxdepth: 2
   :caption: Sections

   architecture
   experiments

Objective
---------

Instead of training 10 separate binary classifiers (one per drug), train
a single neural network that predicts all 10 drug resistances at once
from each spectrum. If a sample was not tested for a given drug, that
label is masked and does not contribute to the loss.

Why Multi-Label
---------------

A typical MALDI-TOF spectrum in the :term:`DRIAMS` dataset has been tested for
~6.3 drugs on average. A :term:`Per-drug model` binary approach (01/02/07) uses only
a single label per training sample. The :term:`Multi-label classification` approach gets ~6×
more training signal from the same data.

.. toctree::
   :maxdepth: 1

Key Innovation: :term:`Shared backbone`
---------------------------------------

All 10 drugs share a common :term:`Shared backbone` (6000→512→256→128). Each drug gets
its own independent sigmoid output head. The backbone learns general
spectral features useful for all drugs simultaneously. See
:doc:`architecture` for the full design.

Baseline
---------

**OneVsRest Logistic Regression**: 10 independent :term:`L2 regularization`
:term:`LogisticRegression` models — :term:`OneVsRest` decomposition.
Provides the linear multi-label baseline against which the shared :term:`MLP`
is compared.

Sub-Experiments (6 total)
-------------------------

The 04 directory explores ablation and improvement over the base
multi-label model. See :doc:`experiments` for full details.

References Back
---------------

- :doc:`02 </02-MLPClassifier-Aggregated/Docs/index>` for the MLP architecture fundamentals
- :doc:`03 </03-CrossSite-Classifier/Docs/index>` for the cross-site evaluation pattern
