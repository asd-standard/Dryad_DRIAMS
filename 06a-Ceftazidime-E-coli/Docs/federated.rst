Federated Ceftazidime × *E. coli* — Results
================================================

:term:`Flower (flwr)`-based :term:`Federated learning` across 4
:term:`DRIAMS` sites (A/B/C/D), 30 rounds, 4 strategies.
Extends the non-federated Ceftazidime analysis
(:doc:`analysis`) to a federation setting.

This is the Ceftazidime counterpart of the Ceftriaxone federated experiment
documented in :doc:`06b </06b-Ceftriaxone-E-coli/Docs/federated>`.

Final Results
-------------

.. list-table::
   :header-rows: 1

   * - Method
     - BalAcc
     - AUC
     - Peak
   * - Centralized MLP (unmasked)
     - —
     - —
     - —
   * - Centralized MLP (union)
     - —
     - —
     - —
   * - Centralized MLP (majority)
     - —
     - —
     - —
   * - Centralized MLP (persite)
     - —
     - —
     - —
   * - Centralized RF (unmasked)
     - —
     - —
     - —
   * - **FL FedAvg MLP**
     - —
     - —
     - —
   * - **FL FedProx**
     - —
     - —
     - —
   * - FL FedAvg LR
     - —
     - —
     - —
   * - FL FedRF (Trees)
     - —
     - —
     - —
   * - Cross-Site MLP
     - —
     - —
     - —
   * - Cross-Site RF
     - —
     - —
     - —

Run the ``06-03a/b/c`` notebooks to populate results.

Strategy Overview
-----------------

===================  ===================================================
Drug / Pathogen       Ceftazidime / *Escherichia coli*
Architecture          :term:`MLP`: 6000 → 512 → 256 → 128 → 2
Strategies            :term:`FedAvg` MLP, :term:`FedProx` (μ=0.1, 0.5),
                      :term:`FedLR`, :term:`FedRF`
Rounds                30
Baselines             Centralized MLP (4 :term:`Species masking` variants),
                      Centralized RF, :term:`Cross-site evaluation`
===================  ===================================================

Species Masking Variants
------------------------

Four centralized baseline variants control for species distribution
differences between sites:

``none``
   Full training set, no species filtering — the true upper bound.

``union``
   Only species present in at least one test site.

``majority``
   Only *E. coli* (the target species). The purest comparison.

``persite``
   Per-site species filtering, simulating local client distributions.

See :term:`Species masking` for full descriptions.

For the Ceftriaxone results that informed these expectations, see
:doc:`06b </06b-Ceftriaxone-E-coli/Docs/federated>`.

Notebooks
---------

- ``06-03a-Ceftazidime-E-coli-Federated.ipynb`` — Main federated notebook
- ``06-03b-Ceftazidime-E-coli-Federated.ipynb`` — Federated variant B
- ``06-03c-Species-Masked-Ceftazidime-Federated.ipynb`` — Species masking
  variants for centralized baselines
- ``retry_fedprox.ipynb`` — :term:`FedProx` μ retry utility
