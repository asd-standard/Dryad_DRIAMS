Non-Federated Baselines
========================

Ceftriaxone was studied through its federated runs; unlike Ceftazidime
(:doc:`06a analysis </06a-Ceftazidime-E-coli/analysis>`) there is no dedicated
06-00 / 06-01 / 06-02-style non-federated notebook. The non-federated
evidence comes from the **centralized and cross-site baselines computed inside
the federated runs**:

- **E. coli-only run** (2026-07-17, ``results_e_coli_only/``) — the
  ``06-03a``/``06-03b`` lineage, restricted to *E. coli* spectra.
- **All-species run** (2026-07-19, ``results/``) — the ``06-03c`` species-masked
  pipeline documented on :doc:`federated`.

Baseline Results
----------------

.. list-table:: Ceftriaxone non-federated baselines (BalAcc / AUC, pooled)
   :header-rows: 1

   * - Baseline
     - *E. coli*-only (Jul 17)
     - All-species (Jul 19)
   * - Centralized MLP
     - 0.670 / 0.750
     - **0.761 / 0.826** :sup:`*`
   * - Centralized RF
     - 0.702 / 0.783
     - 0.659 / 0.819
   * - Cross-Site MLP (train A)
     - 0.591 / 0.661
     - 0.608 / 0.634
   * - Cross-Site RF (train A)
     - not recorded
     - 0.506 / 0.753

:sup:`*` Unmasked variant; the species-masked variants (union / majority /
persite) are on :doc:`federated`.

Ceftriaxone vs Ceftazidime
--------------------------

*E. coli*-only basic runs — Ceftazidime from
:doc:`06a </06a-Ceftazidime-E-coli/index>` (``Results/02-Run``), Ceftriaxone
from ``results_e_coli_only/``:

.. list-table::
   :header-rows: 1

   * - Baseline
     - Ceftazidime
     - Ceftriaxone
   * - Centralized MLP
     - 0.683 / 0.744
     - 0.670 / 0.750
   * - Centralized RF
     - 0.660 / 0.724
     - **0.702 / 0.783**
   * - Cross-Site MLP (train A)
     - 0.538 / 0.498
     - **0.591 / 0.661**

All-species ``06-03c`` pipeline (same protocol on both pairs):

.. list-table::
   :header-rows: 1

   * - Baseline
     - Ceftazidime
     - Ceftriaxone
   * - Centralized MLP (unmasked)
     - 0.615 / 0.733
     - **0.761 / 0.826**
   * - Centralized RF
     - 0.626 / 0.728
     - 0.659 / 0.819
   * - Cross-Site MLP (train A)
     - 0.552 / 0.583
     - **0.608 / 0.634**
   * - Cross-Site RF (train A)
     - 0.500 / 0.678
     - 0.506 / 0.753

Findings
--------

- **Ceftriaxone is the easier pair centrally.** All-species, the centralized
  MLP gains +0.146 BalAcc over Ceftazidime (0.761 vs 0.615); in the
  *E. coli*-only comparison the RF is clearly stronger on Ceftriaxone
  (+0.042 BalAcc, +0.059 AUC), with a notably high Site B score (0.912).
- **Cross-site transfer is poor for both pairs** (pooled BalAcc 0.50–0.61,
  AUC 0.50–0.68): the :term:`Domain shift` cost is not specific to one drug,
  and single-site training is insufficient in both 06a and 06b.
- **The gap is one of packaging, not data.** Ceftriaxone's non-federated
  numbers exist as baselines inside its federated runs; Ceftazidime
  additionally has a dedicated non-federated program (06-00/06-01/06-02).

Scope
-----

There is **no 06-02-style aggregated iterative comparison** (LR / MLP / RF
with warm starts on a fixed test set) for Ceftriaxone; the tables above are
the complete existing non-federated evidence. Producing the iterative
counterpart would require a new run.

Files
-----

- ``results_e_coli_only/`` — 2026-07-17 *E. coli*-only run:
  ``final_results.csv``, ``best_params_used.txt``, per-round CSVs,
  ``convergence.pdf``, ``heatmap_balacc.pdf``, ``heatmap_auc.pdf``
- ``results/`` — 2026-07-19 all-species run (see :doc:`federated`)
- ``results-20260718T081728Z-1-001.zip`` — source archive of the extracted
  *E. coli*-only run
