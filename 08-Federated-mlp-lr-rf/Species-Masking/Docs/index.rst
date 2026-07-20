Species Masking
===============

One-time computation of species-predictive m/z bins for fair
centralized-vs-federated comparisons across all 6 drugs.

.. _notebook: ../compute_masks.ipynb

Objective
---------

When comparing :term:`Federated learning` results to a centralized
(pooled data) baseline, the centralized model may have an unfair
advantage: it sees spectra from all 4 :term:`DRIAMS` sites and can
exploit species-specific spectral signatures that individual federated
clients cannot. :term:`Species masking` removes these signatures by
zeroing out bins that predict bacterial species.

How It Works
------------

The notebook ``compute_masks.ipynb`` runs two phases:

**Phase 1 — Per-site RF species classifiers**
   A :term:`Random Forest` is trained on each site's data to classify
   *bacterial species* (not drug resistance). The top 500 most important
   m/z bins per site are identified — these are the bins most predictive
   of which species a spectrum belongs to. Each site's RF model is saved
   as ``shared_masks/rf_species_models/site_{A,B,C,D}_rf_species.joblib``.

**Phase 2 — Mask computation**
   From the per-site bin lists, three mask strategies are computed:

.. list-table:: Mask Strategies
   :header-rows: 1

   * - Strategy
     - Rule
     - Bins removed
     - Best for
   * - ``union``
     - Bins flagged by **any** site
     - ~500–1500
     - Removing all species-specific signal
   * - ``majority``
     - Bins flagged by **≥2** sites
     - ~200–800
     - Removing broadly informative species bins
   * - ``persite``
     - Each site removes **its own** flagged bins
     - 500 per site
     - Per-client local distributions (most natural for FL)

Masks are saved as ``.npy`` files to ``shared_masks/`` along with
``metadata.json`` (compute date, drug used, mask sizes).

Usage in Federated Notebooks
----------------------------

After running ``compute_masks.ipynb`` once, each drug's
``federated.ipynb`` can apply masks via two config variables:

.. code-block:: python

   USE_SPECIES_MASKING = True
   MASK_STRATEGY = "majority"   # "none" | "union" | "majority" | "persite"

When enabled, the preprocessing pipeline zeros out the specified bins
before any model training or evaluation, giving both federated and
centralized baselines the same masked data.

Why Drug-Independent
--------------------

Species labels are identical across all drug CSVs — a sample's species
is the same regardless of which drug resistance is being tested. The
species-predictive bins are therefore intrinsic to the MALDI-TOF
instrument + bacterial ecology of each site, not to any specific drug.
Computing masks once on a single drug (the one with the most samples
per site) and reusing them across all 6 drugs is both valid and
efficient.

Output Files
------------

::

   shared_masks/
   ├── metadata.json                              ← compute config
   ├── union_mask.npy                             ← bins to zero for union
   ├── majority_mask.npy                          ← bins to zero for majority
   ├── persite_site_A_mask.npy                    ← bins to zero for site A
   ├── persite_site_B_mask.npy
   ├── persite_site_C_mask.npy
   ├── persite_site_D_mask.npy
   └── rf_species_models/
       ├── site_A_rf_species.joblib
       ├── site_B_rf_species.joblib
       ├── site_C_rf_species.joblib
       └── site_D_rf_species.joblib

Related
-------

- :term:`Species masking` — glossary entry with full strategy descriptions
- :doc:`06b </06b-Ceftriaxone-E-coli/Docs/federated>` — first use of species
  masking in the Ceftriaxone federated experiment (06-03c notebook)
- :doc:`/08-Federated-mlp-lr-rf/Docs/methodology` — 08 methodology, including Strategy 5:
  Species Masking section
