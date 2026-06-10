# DRIAMS

## Database of ResIstance against Antimicrobials with MALDI-TOF Mass Spectrometry

For each site, the data consists of MALDI-TOF mass spectra in the form of `.txt` files and a meta-data file.
(i) The meta-data, incl. species and antimicrobial resistance corresponding to each spectra, is part of the `id` folder
(ii) The remaining folders store the MALDI-TOF mass spectra in various stages of preprocessing: `raw` all spectra as extracted from the MALDI-TOF MS instrument, `preprocessed` all spectra after the application of an established preprocessing pipeline and `binned_6000` all spectra after the application of an established preprocessing pipeline and binning along the mass-to-charge-ratio axis with a bin size of 3Da, resulting in 6000 feature bins.

For details on the dataset extraction, quality control, preprocessing and properties, please refer to the Methods section in the preprint corresponding to the publication [https://doi.org/10.1101/2020.07.30.228411](https://doi.org/10.1101/2020.07.30.228411).

We recommend using our Python package for MALDI-TOF MS preprocessing and machine learning analysis, `maldi-learn` ([https://github.com/BorgwardtLab/maldi-learn](https://github.com/BorgwardtLab/maldi-learn)), to load and analyse DRIAMS data.

The github package comes with an elaborate `README.md` file, which gives details on installation and usage examples. In order to use this package the locations of data files and folder structure must be preserved. Please note that all four downloaded data packages should be kept in one folder, serving as the DRIAMS root folder, which then needs to be set as the `DRIAMS_ROOT` path in the `.env` file.

The DRIAMS folder structure obtained after download is the following:

```
DRIAMS
├── DRIAMS-A
│   ├── binned_6000
│   ├── id
│   ├── preprocessed
│   └── raw
├── DRIAMS-B
│   ├── binned_6000
│   ├── id
│   ├── preprocessed
│   └── raw
├── DRIAMS-C
│   ├── binned_6000
│   ├── id
│   ├── preprocessed
│   └── raw
└── DRIAMS-D
    ├── binned_6000
    ├── id
    ├── preprocessed
    └── raw
```

#### Sites where MALDI-TOF MS and AMR profiles were collected

* DRIAMS-A: University Hospital of Basel, Switzerland
* DRIAMS-B: Canton Hospital Basel-Land, Switzerland
* DRIAMS-C: Canton Hospital Aarau, Switzerland
* DRIAMS-D: Viollier AG laboratory, Switzerland

#### Conversion to DRIAMS

We require a DRIAMS dataset entry to contain (1) a spectra code linking unambiguously to a spectra file, (2) a readable mass spectra fid file (as all of our mass spectra are measured on Bruker Microflex machines), (3) the corresponding species (species reported as 'Organism best match' by the flexControl Software was assigned), and, if available, (4) AMR profiles stating antimicrobial susceptibility results.

#### Workstations

Patient samples processed at the USB microbiological diagnostic laboratory samples are analysed at nine different workstations, split by patient isolation material or procedure. The workstations comprise (i) urine samples, (ii) blood culture samples, (iii) stool samples, (iv) genital tract samples, (v) samples for which a PCR-based test were ordered, (vi) respiratory tract samples, (vii) samples from deep, usually sterile material (viii) samples that were collected for the hospital hygiene department, and (ix) samples that cannot be assigned to any of the other categories. Each workstation employs a predefined set of  growth media, optimizsed to culture the agents of infection with high sensitivity.

#### A note on antimicrobial nomenclature in DRIAMS

Since the naming scheme of antimicrobial drugs was not consistent between sites, due to different spelling variants or the use of several names for the same drug (e.g. cotrimoxazol and trimethoprim/sulfamethoxazole describe the same drug), we unified them during preprocessing. Specifically, we anglicised the names of antimicrobial drugs from their original German version in the DRIAMS ID files as a preprocessing step for our machine learning analysis.
Antimicrobial names were specified by adding suffixes to their names. In the following, we explain our suffix nomenclature for DRIAMS-A: (i) ‘high level’: According to EUCAST, MIC breakpoints vary with the dosage of Gentamycin (standard: 5mg / kg and high level: 7 mg / kg for intravenous administration); (ii) ‘meningitis’, ‘pneumoniae’, ’endocarditis’, ‘uncomplicated urinary tract infection (UTI)’: EUCAST includes infection specific breakpoints for these infections (see suffixes for amoxicillin-clavulanic acid, penicillin and meropenem); (iii) ‘screen’: cefoxitin is used to screen for MRSA in clinical routine diagnostic at University Hospital Basel, using the respectively-defined breakpoints by EUCAST; (iv) ‘GRD’: GRD (glycopeptide resistance detection) is a MIC Strip Test used at the DRIAMS-A site in very rare cases to detect glycopeptide intermediate S. aureus; (v) ‘1mg_l’ indicates the concentration of rifampicin, when MIC are measured in liquid culture as it is routinely done for Mycobacterium tuberculosis (MTB). These entries of non-MTB species were entered incorrectly into the laboratory information system.

## Change Log

**Aug 2025**: A new DRIAMS_C.tar.gz File was uploaded to remove some corrupt information within the files (naming of the raw files). Thereby a more consistent naming of the files was generated.