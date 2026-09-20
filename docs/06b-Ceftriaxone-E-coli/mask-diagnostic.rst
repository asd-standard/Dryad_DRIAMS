Species-Mask Diagnostic — Why Masking Doesn't Help
==================================================

The Ceftriaxone 06-03c run selected the ``none`` mask — zeroing
species-predictive bins did not improve worst-site :term:`Balanced Accuracy`.
This page documents a follow-up diagnostic that isolates *why*.

Question
--------

06-03c builds each site's mask from the top-500 bins of a per-site
:term:`Random Forest` trained to classify bacterial species. That RF uses the
default ``max_features="sqrt"`` (~77 of 6000 bins per split), which dilutes
:term:`Feature importance` across correlated bins — the top-500 captured only
~70% of the importance mass. Was this "weak" mask an artifact of the RF
configuration, and would a better RF (higher ``max_features``) produce a mask
that removes more species signal?

Method
------

``06-03c-Phase1-Mask-Diagnostic.ipynb`` reuses the exact 06-03c data pipeline
(same species-stratified split, downsampling, preprocessing, seed) and sweeps
the per-site species RF over three configurations:

.. list-table:: Species-RF configurations
   :header-rows: 1

   * - Name
     - n_estimators
     - max_depth
     - min_samples_leaf
     - max_features
   * - baseline
     - 300
     - 20
     - 5
     - sqrt (default)
   * - mf_0.2
     - 300
     - 20
     - 5
     - 0.2
   * - mf_0.5
     - 500
     - 20
     - 5
     - 0.5

For each configuration, per site, it records:

* out-of-bag (OOB) species classification accuracy,
* importance concentration at top-100/500/1000,
* ``union``/``majority`` mask sizes and pairwise site overlap,
* the **masking-drop**: the OOB drop when the top-500 bins are zeroed before
  retraining — a direct measure of how much species signal the mask removes.

Results
-------

.. list-table:: Mean across sites (per configuration)
   :header-rows: 1

   * - config
     - OOB
     - masking-drop
     - top-100
     - top-500
     - top-1000
     - overlap
   * - baseline
     - 0.944
     - +0.0127
     - 34.1%
     - 73.9%
     - 89.2%
     - 51%
   * - mf_0.2
     - 0.941
     - +0.0022
     - 73.5%
     - 93.6%
     - 97.1%
     - 46%
   * - mf_0.5
     - 0.937
     - +0.0029
     - 84.2%
     - 95.4%
     - 97.6%
     - 42%

Three observations:

1. **Importance concentrates** — raising ``max_features`` pushes top-500
   concentration from 74% to 95% (and top-100 from 34% to 84%), confirming the
   default ``sqrt`` was smearing importance across correlated bins.
2. **The masking-drop stays near zero** — and *shrinks* from +1.3% to +0.2%,
   with several sites going negative (zeroing the bins slightly *helps* species
   classification). The concentrated bins are not more informative.
3. **OOB is flat and overlap drops** — species classification stays ~0.94 in all
   configs, while pairwise mask overlap falls 51% to 42% (concentrated masks are
   more site-specific).

Interpretation
--------------

:term:`Feature importance` concentration is not the same as unique information.
Even with 95% of the Gini importance packed into the top-500, zeroing those bins
removes essentially no species signal — the RF re-learns it from the remaining
5,500 correlated bins. Species information is **redundant across the whole
spectrum** and cannot be localized to a few hundred m/z bins.

Conclusion
----------

* The 06-03c ``none`` result is **robust**: it reflects spectral redundancy plus
  species/resistance entanglement, not a weak mask.
* There is no value in re-running 06-03c with a higher ``max_features`` — a more
  concentrated, more site-specific mask would be, if anything, worse.
* Species masking by zeroing top-K bins is fundamentally limited for MALDI-TOF
  spectra.

Files
-----

* ``06-03c-Phase1-Mask-Diagnostic.ipynb`` — the diagnostic notebook
* ``mask_diagnostic.csv`` / ``mask_concentration.pdf`` — outputs
