Site-D Ablation — Training without DRIAMS-D
===========================================

Do the federated models get dragged down by DRIAMS-D? Site D is the largest
site (~39 % of the pooled spectra) and has the weakest per-site
:term:`Balanced Accuracy` in five of the six drugs (see :doc:`drugs`). This
page reports the **leave-D-out pilot**: three drugs re-run with clients A/B/C
only, everything else matched to the archived with-D runs.

**Result in one line:** removing D does *not* improve the other sites — A and C
are essentially unchanged, B gets worse in all three drugs, and D itself scores
*above* the cross-site baseline even when it is never trained on. D is not
dragging the federation down; it benefits from participating, and the weakness
of a single-site model on D is a transfer cost, not D poisoning the model.

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
paired comparison on the same test data, and the only difference is which
clients participate in training.

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
   annotated). A edges up in two of three drugs and C is flat, but **B falls in
   every drug** — the opposite of "D drags everyone down".

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
   the archived cross-site baselines (A→D). The unseen federated model is
   consistently **better than single-site transfer** and only 0.01–0.06 below
   training with D — D benefits from being in the federation, but multi-site
   training transfers to it even without D's data.

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

Reading
-------

- **No evidence that D hurts the federation.** If D's client updates were
  degrading the global model, removing them should lift A/B/C. Instead the
  deltas are small, B drops consistently, and the pooled (Centralized) arm
  agrees with the federated one.
- **D benefits from participation.** Trained on D: 0.63–0.67; unseen: 0.61–0.64;
  single-site A→D transfer: 0.54–0.58. Excluding D costs D the most and buys
  the other sites nothing.
- This matches the :doc:`umap-diagnostic` conclusion: site D is not an isolated
  geometric island, and its weakness in per-site metrics reflects
  cross-site transfer difficulty — not a site that should be dropped from a
  federation.

Caveats
-------

- **Single seed per arm.** No run-to-run variance estimate; deltas of this size
  cannot be separated from seed noise. B's decline is consistent across the
  three drugs but still a single-seed observation.
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
- ``Site-D-Ablation/compare_noD.ipynb`` — builds the comparison tables and the
  two figures above from the archived runs and the no-D results
  (``Site-D-Ablation/comparison_results/``, local-only).
- Executed copies are archived as ``results/notebook.ipynb`` inside each no-D
  run folder (local-only).

Related
-------

- :doc:`drugs` — per-drug results of the with-D runs
- :doc:`umap-diagnostic` — site/species structure and separability behind D
- :doc:`aggregated` — cross-drug strategy comparison
