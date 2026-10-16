06b — Ceftriaxone × *E. coli* — Federated
==========================================

The project's first :term:`Federated learning` experiment. Extends the
methodological foundation established in
:doc:`06a </06a-Ceftazidime-E-coli/index>` to a federation
across 4 hospital sites.

.. toctree::
   :maxdepth: 1
   :caption: Sections

   analysis
   federated
   mask-diagnostic

Why Ceftriaxone
---------------

Ceftriaxone × *E. coli* was selected as the best-populated drug–pathogen
pair (4,506 samples across all 4 :term:`DRIAMS` sites), providing
enough data per site for meaningful local training.

At a Glance
-----------

===================  ===================================================
Drug / Pathogen       Ceftriaxone / *E. coli* (4,506 samples)
Architecture          :term:`MLP`: 6000 → 512 → 256 → 128 → 2
Strategies            :term:`FedAvg` MLP, :term:`FedProx` μ=0.5 & 1.0,
                      :term:`FedLR`, :term:`FedRF`
Rounds                50
Baselines             Centralized MLP (4 :term:`Species masking` variants),
                      Centralized RF, :term:`Cross-site evaluation`
Key Result            FedLR leads the federated runs (0.743); FedProx
                      μ≥0.5 hurts under the corrected squared penalty
===================  ===================================================

Files
-----

- :notebook:`06-03a-Ceftriaxone-E-coli-Federated.ipynb <06b-Ceftriaxone-E-coli/06-03a-Ceftriaxone-E-coli-Federated.ipynb>` — Main federated notebook
- :notebook:`06-03b-Ceftriaxone-E-coli-Federated.ipynb <06b-Ceftriaxone-E-coli/06-03b-Ceftriaxone-E-coli-Federated.ipynb>` — Federated variant B
- :notebook:`06-03b-Re-Run-lr-Ceftriaxone-E-coli-Fed.ipynb <06b-Ceftriaxone-E-coli/06-03b-Re-Run-lr-Ceftriaxone-E-coli-Fed.ipynb>` — Federated LR re-run
- :notebook:`06-03c-Species-Masked-Ceftriaxone-Federated.ipynb <06b-Ceftriaxone-E-coli/06-03c-Species-Masked-Ceftriaxone-Federated.ipynb>` — Species masking variants (**ran 2026-10-15**; source of the :doc:`federated` results)
- :notebook:`06-03d-Site-Masked-Ceftriaxone-Federated.ipynb <06b-Ceftriaxone-E-coli/06-03d-Site-Masked-Ceftriaxone-Federated.ipynb>` — Site/instrument masking companion (**ran 2026-10-15**; see :doc:`mask-diagnostic`)
- :notebook:`retry_fedprox.ipynb <06b-Ceftriaxone-E-coli/retry_fedprox.ipynb>` — :term:`FedProx` μ retry utility
- ``results/`` — Run outputs (CSVs, PDFs)

Related Analyses
----------------

- :doc:`06a </06a-Ceftazidime-E-coli/index>` — Ceftazidime non-federated foundation
- :doc:`08 </08-Federated-mlp-lr-rf/index>` — Full federated study across all 6 drugs
