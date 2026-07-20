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

The four centralized baseline variants above are produced by
``06-03c`` via a 4-phase pipeline (see `06-03c: Species-Masked Federated Learning`_).

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

06-03c: Species-Masked Federated Learning
-----------------------------------------

``06-03c`` is the most sophisticated notebook in the 06a pipeline.
Unlike ``06-03a/03b`` which operate on *E. coli* only, 06-03c works on
**all species** and uses a data-driven approach to find the fairest
centralized-vs-federated comparison. The notebook runs in four phases:

**Phase 1 — Per-site species RF classifiers**
   Trains a :term:`Random Forest` on each :term:`DRIAMS` site to
   identify which m/z bins are predictive of *species* (not drug
   resistance). The top 500 most important bins become that site's
   "species signature" — bins strongly associated with the site's
   bacterial ecology.

**Phase 2 — Three mask strategies computed**
   Each strategy produces a set of bins to **zero out** from the
   training data, removing species-specific spectral information:

   ==============  =======================================================
   `none`          No masking — full 6000 bins. The true upper bound.
   `union`         Bins flagged by **any** site's species RF. Removes
                   species-identifiable bins across all sites.
   `majority`      Bins flagged by **≥2** sites. Removes broadly
                   informative species bins (more conservative).
   `persite`       Per-site masking — each site removes **its own**
                   flagged bins. Simulates per-client local species
                   distributions.
   ==============  =======================================================

**Phase 3 — Mask comparison and selection**
   Trains a :term:`FedAvg` MLP on each of the 4 masked datasets. For
   each strategy, computes the **per-site improvement over unmasked**.
   Selects the mask with the highest **worst-site** delta:

   ::

      best_strategy = argmax( min_site(BalAcc_masked - BalAcc_unmasked) )

   This ensures the chosen mask helps the site that needs it most.

**Phase 4 — Full FL pipeline with best mask**
   Switches all active data to the winning mask and runs:

   - :term:`FedAvg` MLP (30 rounds)
   - :term:`FedProx` μ=0.1, 0.5 (30 rounds)
   - :term:`FedLR` with per-site tuned C (Option B)
   - :term:`FedRF` tree collection (5 rounds)
   - Cross-Site MLP + RF (train on mask-filtered A data)

**Output**:
   ``mask_delta.pdf`` — bar chart showing per-site improvement of each mask
   vs. unmasked. Saved RF species classifiers are reusable by 08.

   ``fedprox_mu{mu}_per_round.csv`` — Per-round validation metrics (BalAcc, AUC) per site.
   ``fedprox_mu{mu}_train_loss_per_round.csv`` — Per-site + aggregated training loss per round.
   ``fedavg_train_loss_per_round.csv`` — Aggregated training loss from FedAvg MLP (best mask).

**Key difference from 06-03a**:
   =========  ========================  =========================
   Aspect     06-03a                    06-03c
   =========  ========================  =========================
   Species    *E. coli* only             All species
   Masking    Pre-configured mask        Data-driven mask selection
   Purpose    Baseline FL experiment     Fair comparison accounting
                                          for species distribution
   Loss data  Validation only            Training + validation per site, per round
   =========  ========================  =========================

Training Loss Monitoring
~~~~~~~~~~~~~~~~~~~~~~~~

The ``06-03c`` notebook captures **per-site training loss** (cross-entropy)
at every round alongside the existing validation metrics. This enables:

* **Overfitting diagnosis** — comparing train vs. validation loss curves to
  detect when the model starts memorizing local data
* **Site-specific training dynamics** — identifying which hospitals learn
  fastest/slowest, revealing data quality or size differences
* **Proximal regularisation effect** — quantifying how :term:`FedProx` μ
  influences local optimisation vs. standard :term:`FedAvg`

Training loss is extracted directly from each client's ``fit()`` return
value (which already computes per-epoch cross-entropy). For :term:`FedProx`,
this is captured via the custom ``CheckpointFedProx.aggregate_fit``
override, which records per-site and aggregated losses before model
aggregation. For :term:`FedAvg`, a ``fit_metrics_aggregation_fn`` is
registered on the strategy to collect the mean training loss across clients.

Notebooks
---------

- ``06-03a-Ceftazidime-E-coli-Federated.ipynb`` — Basic FL (E. coli only):
  FedAvg + FedProx + FedLR + FedRF
- ``06-03b-Ceftazidime-E-coli-Federated.ipynb`` — FL variant B
- ``06-03c-Species-Masked-Ceftazidime-Federated.ipynb`` — Species-masked FL
  (all species): 4-phase pipeline with data-driven mask selection. Produces
  the centralized MLP (none/union/majority/persite) baselines.
- ``retry_fedprox.ipynb`` — :term:`FedProx` μ retry utility
