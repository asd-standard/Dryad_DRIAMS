Data Processing
===============

How the raw :term:`DRIAMS` archives become the per-drug, ML-ready CSV
files consumed by every analysis (01–08). This page covers dataset
provenance, the local ``process_driams.py`` pipeline, and the derived
artifacts shared between notebooks. The long-form version with complete
per-drug statistics lives in ``Processed/Processing/README.md`` in the
data tree.

Source Dataset
--------------

:term:`DRIAMS` (Database of ResIstance against Antimicrobials with
MALDI-TOF Mass Spectrometry) links clinical MALDI-TOF spectra to
antimicrobial susceptibility results from four Swiss sites (2018).

- Publication preprint: https://doi.org/10.1101/2020.07.30.228411
- Dryad archive: https://doi.org/10.5061/dryad.bzkh1899q

.. list-table::
   :header-rows: 1
   :widths: 10 45 45

   * - Site
     - Hospital
     - Processed drugs
   * - A
     - University Hospital of Basel
     - 34
   * - B
     - Canton Hospital Basel-Land
     - 24
   * - C
     - Canton Hospital Aarau
     - 22
   * - D
     - Viollier AG laboratory
     - 17

Each site archive contains four directories:

::

   DRIAMS-{A,B,C,D}/
   ├── raw/                  # spectra as extracted from the MALDI-TOF instrument
   ├── preprocessed/         # QC + smoothing + baseline correction + normalisation
   ├── binned_6000/2018/     # {code}.txt — 6000 bins at 3 Da m/z resolution
   └── id/2018/              # 2018_clean.csv — species + AMR metadata per code

The published DRIAMS pipeline performs quality control, spectral
preprocessing, and binning along the m/z axis (3 Da width → 6000
features). This project uses the :term:`binned_6000` stage to match the
published pipeline exactly and avoid reimplementing spectral
preprocessing.

.. note::

   Drug names were unified during DRIAMS curation (anglicised, spelling
   variants merged) and carry suffixes such as ``_high_level``,
   ``_screen``, or ``_meningitis`` for EUCAST context-specific
   breakpoints. See the dataset ``README.md`` for the full nomenclature.

Running the Pipeline
--------------------

Script: ``process_driams.py`` in the data tree (identical copy under
``Processed/Processing/``). Configuration at the top of the file:

- ``DRYAD`` — path to the extracted DRIAMS root
- ``OUTPUT`` — output root (``Processed/``)
- ``SITES`` — per-site ``binned`` and ``meta`` paths
- ``MIN_S = 500``, ``MIN_R = 10`` — minimum susceptible / resistant counts

Processing steps:

1. Load the site metadata (``id/2018/2018_clean.csv``) as strings.
2. Match ``code`` values to the ``{code}.txt`` files in ``binned_6000/2018/``.
3. Identify drug columns: all metadata columns except ``code``,
   ``species``, ``genus``, ``combined_code``, ``laboratory_species``,
   and unnamed index columns.
4. Count ``S`` and ``R`` labels per drug; keep drugs with at least
   ``MIN_S`` susceptible and ``MIN_R`` resistant samples.
5. Load each needed spectrum once (second column of the ``.txt`` file,
   skipping the header row) and build the site-wide feature matrix.
6. Write one ``data.csv`` per qualifying drug plus site and global
   summaries.

Labels are encoded as ``R = 1``, ``S = 0``; ``I`` (intermediate) and
untested (``NaN``) entries are excluded, so every row contributes a
binary label for that drug.

Output Layout
-------------

::

   Processed/
   ├── global_summary.csv                  # all drug-site results
   ├── Proc_DRIAMS-A/ … Proc_DRIAMS-D/
   │   ├── summary.csv                     # per-site statistics
   │   └── {drug}/
   │       └── data.csv                    # code, species, label, bin_0 … bin_5999

``data.csv`` columns:

.. list-table::
   :header-rows: 1
   :widths: 22 12 66

   * - Column
     - Type
     - Description
   * - ``code``
     - str
     - :term:`spectra code` linking back to the original ``{code}.txt`` spectrum
   * - ``species``
     - str
     - Organism name from the DRIAMS metadata
   * - ``label``
     - int
     - ``0`` = susceptible, ``1`` = resistant
   * - ``bin_0`` … ``bin_5999``
     - float
     - Binned spectral intensities (6000 m/z features)

Drug directory names replace spaces and slashes with underscores
(``Amoxicillin-Clavulanic_acid``).

Results
-------

**97 drug–site combinations** are generated with the default thresholds.
Per-drug sample counts, resistance rates, and full tables are maintained
in ``Processed/Processing/README.md``; the totals are:

.. list-table::
   :header-rows: 1
   :widths: 15 15 70

   * - Site
     - Drugs
     - Examples
   * - DRIAMS-A
     - 34
     - Penicillin, Ceftriaxone, Ciprofloxacin, Meropenem
   * - DRIAMS-B
     - 24
     - Ampicillin, Ciprofloxacin, Amoxicillin-Clavulanic acid
   * - DRIAMS-C
     - 22
     - Ampicillin, Gentamicin, Ciprofloxacin
   * - DRIAMS-D
     - 17
     - Gentamicin, Ciprofloxacin, Fosfomycin

Ten drugs have data at **all four sites** and drive the cross-site and
federated experiments:

::

   Amikacin · Amoxicillin-Clavulanic acid · Cefepime · Ceftazidime
   Ceftriaxone · Ciprofloxacin · Gentamicin · Imipenem
   Piperacillin-Tazobactam · Vancomycin

Derived Artifacts
-----------------

.. list-table::
   :header-rows: 1
   :widths: 42 22 36

   * - Artifact
     - Built by
     - Consumed by
   * - ``Proc_DRIAMS-*/{drug}/data.csv``
     - ``process_driams.py``
     - 01, 02, 03, 05, 06a, 06b, 07, 08
   * - :term:`aggregated_multilabel_data.npz`
     - 04-00
     - 04-01 … 04-05
   * - :term:`best_params.csv`, ``rf_results.pkl``
     - 07
     - 08 (federated hyperparameters and pooled baselines)
   * - ``shared_masks/*.npy``, ``rf_species_models/*.joblib``
     - 08 ``compute_masks.ipynb``
     - 08 federated notebooks

The multi-label cache concatenates all four sites into ``X_all``
(26,642 × 6000), ``Y_all`` (26,642 × 10, ``NaN`` for untested drugs),
and ``sp_all`` (species), deduplicating spectra that appear in several
per-drug CSVs. Species masks are described in
:doc:`08 </08-Federated-mlp-lr-rf/Species-Masking/index>`.

.. note::

   Analysis-time preprocessing is separate from this pipeline: notebooks
   apply :term:`log1p transform` and :term:`Standardize to zero mean`
   after splitting, fitting on the training set only. The processed CSVs
   contain the raw binned intensities.

Paths and Environment
---------------------

- Notebooks define their data root per file (a local path and a Colab
  Google Drive path); ``process_driams.py`` defines ``DRYAD``/``OUTPUT``
  constants. ``global_summary.csv`` records the absolute ``output_path``
  used when the data was generated, so the CSVs are
  location-independent but those summary paths may need updating after
  moving the tree.
- Processing requirements: Python ≥ 3.12 with ``numpy``, ``pandas``,
  ``tqdm``.

Reproduce
---------

.. code-block:: bash

   conda create -n driams python=3.12 -y
   conda activate driams
   pip install numpy pandas tqdm
   python process_driams.py

See ``Processed/Processing/README.md`` for download and extraction steps,
filter thresholds, and complete per-drug tables.
