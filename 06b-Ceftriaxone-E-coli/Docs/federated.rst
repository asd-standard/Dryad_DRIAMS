Federated Ceftriaxone × *E. coli* — Results
============================================

:term:`Flower (flwr)`-based :term:`Federated learning` across 4
:term:`DRIAMS` sites (A/B/C/D), 30 rounds, 4 strategies.

These results were produced by ``06-03c-Species-Masked-Ceftriaxone-Federated.ipynb``
— see `06-03c: How It Works`_ for the 4-phase pipeline. The Ceftazidime
counterpart lives in
:doc:`06a </06a-Ceftazidime-E-coli/Docs/federated>`. 


Final Results
-------------

.. list-table:: Final Results — Ceftriaxone × *E. coli* 30-round federated run
   :header-rows: 1

   * - Method
     - BalAcc
     - AUC
     - Peak
   * - Centralized MLP (unmasked)
     - 0.761
     - 0.826
     - \-
   * - Centralized MLP (union)
     - 0.747
     - 0.829
     - \-
   * - Centralized MLP (majority)
     - 0.760
     - 0.822
     - \-
   * - Centralized MLP (persite)
     - 0.742
     - 0.805
     - \-
   * - Centralized RF (unmasked)
     - 0.659
     - 0.819
     - \-
   * - **FL FedAvg MLP**
     - 0.745
     - 0.807
     - r12
   * - **FL FedProx μ=0.1**
     - 0.746
     - 0.810
     - r19
   * - FL FedAvg LR
     - 0.710
     - 0.803
     - r30
   * - FL FedRF (Trees)
     - 0.500
     - 0.808
     - r2
   * - Cross-Site MLP
     - 0.608
     - 0.634
     - \-
   * - Cross-Site RF
     - 0.506
     - 0.753
     - \-

Key Findings
------------

FedAvg / FedProx Close the Gap
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Both FedAvg MLP (BalAcc 0.745) and FedProx μ=0.1 (BalAcc 0.746) land
within ~1.6% of the best centralized MLP (0.761). The :term:`Federated
learning` approach recovers ~96% of the pooled-data ceiling while
keeping all raw spectra private.

FedProx provides a marginal improvement (+0.001 BalAcc) over standard
FedAvg, but plateaus more slowly — its peak is at round 19 vs. round
12 for FedAvg.

Species Masking in Centralized Baselines
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Four variants of the centralized baseline control for species
distribution differences between sites. This ensures the centralized
comparison uses a species composition comparable to what federated
clients see locally.

``none``
   Full training set, no species filtering — the true upper bound.

``union``
   Only species present in at least one test site. Prevents the
   centralized model from benefiting from species it never evaluates on.

``majority``
   Only *E. coli* (the species being predicted). The purest comparison
   — all models see only E. coli.

``persite``
   Per-site species filtering. Simulates per-client local species
   distributions.

The ``none`` and ``majority`` variants produce the strongest results;
the federated models approach their performance.

These mask variants were computed by ``06-03c`` via per-site species RF
classifiers — see `06-03c: How It Works`_ for the full pipeline.

06-03c: How It Works
~~~~~~~~~~~~~~~~~~~~

The results on this page come from ``06-03c-Species-Masked-Ceftriaxone-Federated.ipynb``,
a 4-phase notebook that works on **all species** (not just *E. coli*):

1. **Per-site species RF classifiers** — Identifies the top 500 m/z bins
   most predictive of species on each site
2. **Mask computation** — Three strategies (union/majority/persite) plus
   unmasked baseline. Each mask zeroes out species-specific bins
3. **Mask comparison** — FedAvg MLP trained on all 4 masked variants;
   winning mask = highest worst-site improvement over unmasked
4. **Full FL pipeline** — Best mask applied, then FedAvg, FedProx μ=0.1,
   FedLR, FedRF, and cross-site baselines all run

**Output**: ``mask_delta.pdf`` (per-site improvement per mask vs. unmasked),
the results table above, saved RF species classifiers for potential reuse in 08,
and per-round CSV files with validation metrics and training loss.

``fedprox_mu{mu}_per_round.csv`` — Per-round validation metrics (BalAcc, AUC) per site.
``fedprox_mu{mu}_train_loss_per_round.csv`` — Per-site + aggregated training loss per round.
``fedavg_train_loss_per_round.csv`` — Aggregated training loss from FedAvg MLP (best mask).

The winning mask for this Ceftriaxone × *E. coli* run was **`none`**
(no masking), meaning species-filtering did not improve worst-site
performance on this drug–pathogen pair. This may differ for Ceftazidime
(:doc:`06a </06a-Ceftazidime-E-coli/Docs/federated>`).

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

FedRF Threshold Issue
~~~~~~~~~~~~~~~~~~~~~

FedRF records :term:`AUC-ROC` 0.808 — competitive with FedAvg — but
:term:`Balanced Accuracy` is stuck at exactly 0.500 across all 5 rounds.
The ``n_trees`` correctly grows from 1200 to 6000, confirming tree
accumulation works. The likely cause: the decision threshold selected
during tuning (0.5) causes all predictions to land in a single class
on the imbalanced test set. This highlights the sensitivity of
ensemble threshold tuning in the federated setting. The 08 study
addresses this by tuning per-site thresholds via cross-validation
(Option A: worst-site optimisation).

FedLR Steady Convergence
~~~~~~~~~~~~~~~~~~~~~~~~

Federated LR climbs steadily from BalAcc 0.655 (round 1) to 0.710
(round 30), never plateauing but also never reaching the MLP-based
strategies. The linear model cannot capture the non-linear structure
in MALDI-TOF spectra, consistent with findings from 01 and 02.

Cross-Site as Lower Bound
~~~~~~~~~~~~~~~~~~~~~~~~~

Training on DRIAMS-A alone and testing on B/C/D yields BalAcc 0.608
— a ~15% drop from centralized. This is the cost of not sharing data
at all. Federated learning recovers most of this gap (0.745 vs. 0.608,
a 14-point improvement), demonstrating the value of collaborative
model training without data centralization.

Notebooks
---------

- ``06-03a-Ceftriaxone-E-coli-Federated.ipynb`` — Basic FL (E. coli only):
  FedAvg + FedProx + FedLR + FedRF
- ``06-03b-Ceftriaxone-E-coli-Federated.ipynb`` — FL variant B
- ``06-03c-Species-Masked-Ceftriaxone-Federated.ipynb`` — **Ran to produce**
  these results: 4-phase pipeline with per-site species RF, data-driven
  mask selection, and full FL pipeline. Produces the centralized MLP
  (none/union/majority/persite) baselines and ``mask_delta.pdf``.
- ``06-03b-Re-Run-lr-Ceftriaxone-E-coli-Fed.ipynb`` — FedLR re-run
- ``retry_fedprox.ipynb`` — :term:`FedProx` μ retry utility
