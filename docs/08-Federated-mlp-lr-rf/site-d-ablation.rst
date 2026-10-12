Site-D Ablation — Training without DRIAMS-D
===========================================

Do the federated models get dragged down by DRIAMS-D? Site D is the largest
site (~39 % of the pooled spectra) and has the weakest per-site
:term:`Balanced Accuracy` in five of the six drugs (see :doc:`drugs`). This
page reports the **leave-D-out pilot**: three drugs re-run with clients A/B/C
only, everything else matched to the archived with-D runs.

**Result in one line:** removing D does *not* improve the other sites —
aggregate performance is essentially unchanged, A/C are flat, and the apparent
B decline does not survive a round-selection robustness check. D itself is the
site that loses most from exclusion, and even unseen it remains in the
cross-site baseline's range. D is not dragging the federation down; its
per-site weakness is a transfer cost, not D poisoning the model.

Design
------

.. list-table:: Ablation runs (all six strategies re-run, no other changes)
   :header-rows: 1

   * - Drug
     - no-D arm
     - with-D mirror
     - Rounds
   * - Ceftriaxone
     - ``Site-D-Ablation/Ceftriaxone/federated_noD.ipynb``
     - ``07-Run``
     - 50
   * - Ciprofloxacin
     - ``Site-D-Ablation/Ciprofloxacin/federated_noD.ipynb``
     - ``04-Run``
     - 50
   * - Ceftazidime
     - ``Site-D-Ablation/Ceftazidime/federated_noD.ipynb``
     - ``03-Run``
     - 30

The no-D arm trains three clients (A/B/C) with the same seed (42), per-site
species-stratified 90/10 splits, hyperparameters, thresholds and rounds as the
with-D run; Centralized MLP/RF pool A/B/C only. FedProx is skipped (unstable at
tuned μ in the with-D runs) and the cross-site arm is not re-run. Site D stays
**in evaluation** as an unseen site. Strategy set: Centralized MLP/RF,
:term:`FedAvg` MLP, :term:`FedLR`, :term:`FedRF`.

Because the splits are computed per site with a fixed seed, the A/B/C (and D)
test sets are identical to the archived runs — every per-site Δ below is a
paired comparison on the same test data. Client-local training (data, seeds,
hyperparameters) is unchanged; the no-D arm differs only in **which clients
participate in aggregation**.

Results
-------

Does D hurt the other sites?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table:: FedAvg (MLP) per-site Balanced Accuracy — Δ = no-D − with-D
   :header-rows: 1

   * - Drug
     - ΔA
     - ΔB
     - ΔC
     - ΔD (unseen)
   * - Ceftriaxone
     - ±0.000
     - −0.051
     - +0.005
     - −0.060
   * - Ciprofloxacin
     - +0.017
     - −0.021
     - −0.004
     - −0.031
   * - Ceftazidime
     - +0.058
     - −0.061
     - −0.011
     - −0.007
   * - **Mean**
     - **+0.025**
     - **−0.044**
     - **−0.004**
     - **−0.033**

.. figure:: /_static/08-Federated-mlp-lr-rf/08_nod_fedavg_per_site.svg
   :alt: FedAvg per-site Balanced Accuracy with D in training versus D dropped, per drug
   :width: 100%

   FedAvg (MLP) per-site Balanced Accuracy, with-D run versus no-D arm (Δ
   annotated at each run's selected peak round). A edges up in two of three
   drugs and C is flat; B's point estimates fall in all three drugs, but that
   pattern is not robust (see below).

Robustness: peak vs final round
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The per-site numbers above are taken at each run's peak round (highest All-site
Balanced Accuracy, the 08 convention). That selection is itself round-sensitive
— the Ceftriaxone with-D FedAvg peaks at round 39, the no-D arm at round 14 —
so the comparison is repeated at the **final round** of each run:

.. list-table:: FedAvg (MLP) Δ at the final round (no-D − with-D)
   :header-rows: 1

   * - Drug
     - ΔA
     - ΔB
     - ΔC
     - ΔD (unseen)
     - ΔAll
   * - Ceftriaxone
     - −0.003
     - −0.117
     - −0.009
     - −0.087
     - −0.023
   * - Ciprofloxacin
     - +0.020
     - −0.012
     - −0.019
     - −0.024
     - −0.001
   * - Ceftazidime
     - +0.012
     - +0.006
     - +0.010
     - −0.028
     - −0.002
   * - **Mean**
     - **+0.010**
     - **−0.041**
     - **−0.006**
     - **−0.046**
     - **−0.009**

Two things become clear. First, **D is the only site with a stable sign**: the
unseen model is behind the trained one in all six drug × round comparisons.
Second, **B's direction is not stable** — it flips to +0.006 for Ceftazidime,
and its largest effect (Ceftriaxone, −0.117) comes with the smallest test set.
Site B holds only 94–199 test spectra, and its round-to-round swings (±0.15)
dwarf every arm difference:

.. figure:: /_static/08-Federated-mlp-lr-rf/08_nod_B_trajectories.svg
   :alt: Site B per-round Balanced Accuracy for both arms, per drug
   :width: 100%

   Site B per-round Balanced Accuracy for both arms (dotted lines: each arm's
   selected peak round). The apparent arm difference is within the training
   noise of this small site.

An exploratory species-mix check (cosine similarity of the per-site species
shares) hints at why B *might* feel D's absence: of the three drugs, only
Ceftriaxone has B's composition closest to D's (B↔D 0.89, versus B↔A 0.67 and
B↔C 0.85); for Ciprofloxacin and Ceftazidime the closest site is A. With three
single-seed runs this is a hypothesis, not evidence.

Site D as an unseen site
~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table:: Site D Balanced Accuracy — trained vs unseen vs cross-site
   :header-rows: 1

   * - Drug
     - FedAvg (trained on D)
     - FedAvg (D unseen)
     - D AUC (no-D)
     - Cross-site MLP
     - Cross-site RF
   * - Ceftriaxone
     - 0.673
     - 0.613
     - 0.642
     - 0.540
     - 0.595
   * - Ciprofloxacin
     - 0.668
     - 0.636
     - 0.666
     - 0.576
     - 0.587
   * - Ceftazidime
     - 0.625
     - 0.619
     - 0.648
     - 0.549
     - 0.572

.. figure:: /_static/08-Federated-mlp-lr-rf/08_nod_siteD_transfer.svg
   :alt: Site D Balanced Accuracy — trained, unseen (no-D), and cross-site transfer
   :width: 100%

   Site D when it is trained, when it is only evaluated (no-D arm), and under
   the archived cross-site baselines (A→D). Training with D is ahead of the
   unseen model at both selection rules (by 0.01–0.09); the comparison with the
   cross-site baseline is round-dependent — above it at the selected peak round
   in all three drugs, mixed at the final round.

Secondary strategies
~~~~~~~~~~~~~~~~~~~~

.. list-table:: Mean Δ across the three drugs (no-D − with-D)
   :header-rows: 1

   * - Method
     - ΔA
     - ΔB
     - ΔC
     - ΔD
   * - Centralized MLP (pooled A/B/C)
     - +0.023
     - −0.042
     - +0.042
     - +0.013
   * - Centralized RF (pooled A/B/C)
     - −0.022
     - −0.034
     - −0.032
     - −0.038
   * - FedAvg (MLP)
     - +0.025
     - −0.044
     - −0.004
     - −0.033
   * - FedLR
     - +0.019
     - +0.017
     - +0.014
     - −0.038
   * - FedRF (trees)
     - −0.039
     - −0.038
     - −0.048
     - −0.074

- **FedLR** is mildly *positive* on A/B/C without D (B +0.017), the clearest
  counter-pattern to FedAvg MLP; it also loses the most on D (−0.038).
- **Centralized MLP** is heterogeneous: Ciprofloxacin improves substantially
  (B +0.143, C +0.129, D +0.083), while Ceftriaxone B collapses (−0.187). Three
  single-seed drugs are not enough to call this a trend.
- **Centralized RF and FedRF** decline nearly everywhere. For FedRF this is
  partly mechanical: the no-D ensemble grows with 3 clients instead of 4
  (200 × 3 vs 200 × 4 trees per round), so its drop is not evidence about D.
- All values here use the peak-round convention; the same selection sensitivity
  applies, so read the means as descriptive.

Reading
-------

- **No evidence that D hurts the federation.** If D's client updates were
  degrading the global model, removing them should lift A/B/C. Instead
  aggregate performance on the shared test pool is unchanged (mean ΔAll
  ≈ −0.01) and no per-site shift is robust to round selection; the pooled
  (Centralized) arm agrees on A and C.
- **D benefits from participation.** Excluding D costs D under both selection
  rules (trained ahead by 0.02–0.09); unseen, D stays in the cross-site
  baseline's range (above it at the selected peak round in all three drugs,
  mixed at the final round).
- **The B question stays open.** B's point estimates decline in all three drugs
  under FedAvg MLP, but the sign flips with round selection, its test sets hold
  94–199 spectra, and the pooled arm flips sign across drugs. Treat it as a
  candidate for seed replication, not a conclusion.
- This matches the :doc:`umap-diagnostic` conclusion: site D is not an isolated
  geometric island, and its weakness in per-site metrics reflects
  cross-site transfer difficulty — not a site that should be dropped from a
  federation.

Caveats
-------

- **Single seed per arm.** No run-to-run variance estimate; deltas of this size
  cannot be separated from seed noise.
- **Test-set sizes differ per site** (A 469–810, B 94–199, C 276–377,
  D 662–982 spectra): one spectrum moves B's Balanced Accuracy by ≈0.01, so
  B's deltas are a handful of spectra.
- **Peak-round selection.** Per-site values follow the 08 convention (each
  run's best All-site round), but the arms can peak at different rounds
  (Ceftriaxone FedAvg: r39 vs r14). The robustness table gives the final-round
  view.
- **Weight shift.** :term:`FedAvg` aggregates clients proportional to sample
  count. Removing D changes the shares (A 33 % → 52 %, C 18 % → 28 %,
  B 9 % → 14 %), so the arm tests "D's presence and its weight" jointly.
- **Thresholds and hyperparameters were reused** from the with-D runs
  (worst-site-optimal with D present). This is deliberate — it isolates the
  training effect — but threshold-dependent Balanced Accuracy could shift with
  A/B/C-only tuning.
- **FedRF is not an equal comparison**: fewer clients means a smaller global
  ensemble for the same rounds.
- **Three of six drugs** (pilot). The positive Ciprofloxacin centralized deltas
  and negative Ceftriaxone ones show the heterogeneity; treat means as
  descriptive only.

Files and Notebooks
-------------------

- ``Site-D-Ablation/{Drug}/federated_noD.ipynb`` — the no-D run for each drug,
  generated from ``Drugs/{Drug}/federated.ipynb`` (``TRAIN_SITES = ["A","B","C"]``,
  archived tuning loaded verbatim, checkpointing disabled, ``AllABC`` metric
  added). See ``Site-D-Ablation/README.md``.
- ``Site-D-Ablation/compare_noD.ipynb`` — builds the comparison tables
  (peak-round and final-round), the transfer table, and the three figures above
  (``Site-D-Ablation/comparison_results/``, local-only).
- Executed copies are archived as ``results/notebook.ipynb`` inside each no-D
  run folder (local-only).

Related
-------

- :doc:`drugs` — per-drug results of the with-D runs
- :doc:`umap-diagnostic` — site/species structure and separability behind D
- :doc:`aggregated` — cross-drug strategy comparison
