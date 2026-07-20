Aggregated Cross-Drug Analysis
=================================

.. _notebook: ../Agg-Analysis/aggregated_analysis.ipynb

The ``aggregated_analysis.ipynb`` notebook loads per-drug
``final_results.csv`` files from all available drugs and produces
cross-drug comparisons, strategy rankings, and :term:`Federated learning`
gap analyses. The ``masked_aggregated_analysis.ipynb`` variant does the
same for runs with :term:`Species masking` enabled, adding mask-specific
delta charts.

Masked Aggregated Analysis
--------------------------

``masked_aggregated_analysis.ipynb`` is a configurable variant that
loads per-drug runs filtered by ``MASK_STRATEGY`` (read from each run's
``best_params_used.txt``). It produces the same visualisations as the
main notebook plus:

**Mask Delta Chart**
   Bar chart comparing BalAcc and AUC deltas (masked − unmasked) per
   drug. Positive deltas indicate species masking improved performance;
   negative deltas suggest the mask removed useful signal.

**Unmasked Reference**
   When unmasked runs are available, the notebook loads them in parallel
   as ``df_final_unmasked`` and includes them in comparison plots.

Results are saved to ``masked_aggregated_results/`` instead of the
default ``aggregated_results/``.

See :doc:`../Species-Masking/Docs/index` for mask computation and
usage in per-drug notebooks.

Data Sources
------------

- ``08/Drugs/{drug}/{NN}-Run/results/final_results.csv`` — Latest FL results
- ``08/Drugs/{drug}/{NN}-Run/results/*_per_round.csv`` — Per-round metrics
- ``07/07-01-results_dedicated_lr_mlp/`` — Pooled LR/MLP baselines (from 07,
  see :term:`best_params.csv`)
- ``07/results_dedicated_lr_mlp/rf_results.pkl`` — Pooled :term:`Random Forest`
  baseline (from 07)

Configurable: set ``DRUGS_TO_ANALYZE`` to select drugs; drugs without
results are silently skipped. Set ``TARGET_RUN`` to pin a specific run
(``None`` = latest).

Visualisations
--------------

1. **Heatmap Grid (per drug)**
   :term:`Balanced Accuracy` and :term:`AUC-ROC` heatmaps, one per drug. Rows
   are strategies; columns are sites + All. Centralized and Pooled baselines
   from 07 are included.

2. **Strategy Ranking**
   Horizontal bar chart ranking strategies by mean All-Site
   :term:`Balanced Accuracy` across drugs. Color-coded by model family
   (MLP=orange, FedProx=red, LR=blue, RF=green, Centralized=black).

3. **Convergence Grid**
   Per-drug convergence plots showing per-round All-Site BalAcc for each
   FL strategy. Pooled baselines from 07 shown as horizontal reference
   lines. :term:`FedAvg` MLP is the primary line (solid orange);
   :term:`FedProx` variants are dashed; :term:`FedLR` and :term:`FedRF`
   have distinct styles.

4. **Centralized vs. Federated Gap**
   Bar chart comparing Pooled :term:`MLP` vs. Best FL method per drug, with
   the gap annotated. Shows which drugs benefit most from centralized data
   and where :term:`Federated learning` matches :term:`Aggregated (pooled) training`
   performance.

5. **Master Summary Tables**
   Pivot tables: :term:`Balanced Accuracy` and :term:`AUC-ROC` (rows = drugs,
   columns = methods). Saved as CSV.

Output Directory
----------------

Results are saved to ``aggregated_results/`` (created automatically):

- ``heatmap_grid_balacc.pdf``, ``heatmap_grid_auc.pdf``
- ``strategy_ranking.pdf``
- ``convergence_grid.pdf``
- ``centralized_vs_fl.pdf``
- ``summary_balacc.csv``, ``summary_auc.csv``

Key Takeaways
-------------

- **Federated learning closes 60–80% of the gap** between
  :term:`Cross-site evaluation` and :term:`Aggregated (pooled) training`
  performance
- :term:`FedAvg` MLP is the most reliable strategy across all 6 drugs
- :term:`FedProx` helps most when site sizes are imbalanced
- :term:`FedRF` with 5 rounds achieves competitive results, suggesting
  :term:`Tree collection` is a viable federated strategy for tabular data
- The centralized-vs-federated gap varies by drug (larger for drugs
  where site :term:`DRIAMS`-D has disproportionately many samples)
