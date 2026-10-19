# DRIAMS — Federated AMR Prediction from MALDI-TOF Spectra

Predicting antimicrobial resistance (susceptible/resistant) directly from
MALDI-TOF mass spectra across four Swiss hospitals — from logistic-regression
baselines to federated learning with [Flower](https://flower.ai/).

[Documentation](https://asd-standard.github.io/Dryad_DRIAMS/) ·
[DRIAMS dataset](https://doi.org/10.5061/dryad.bzkh1899q) ·
[Processing pipeline](00-Data-Processing/README.md) ·
[DRIAMS paper](https://doi.org/10.1038/s41591-021-01619-9)

---

## Overview

This repository contains the analysis code and full documentation for an
antimicrobial-resistance (AMR) prediction study on the
[DRIAMS](https://doi.org/10.5061/dryad.bzkh1899q) dataset:

- **Task** — predict resistance (S/R) to **10 antibiotics** from 6000-bin
  MALDI-TOF spectra (3 Da bins), using species-stratified evaluation.
- **Models** — logistic regression, MLP, random forest, a shared-backbone
  multi-label network, a 1D CNN, and federated learning (FedAvg, FedProx,
  FedLR, FedRF) across the four hospital sites.
- **Focus** — pooled baselines (01/02/07), cross-site generalisation A→B/C/D
  (03/04), multi-label and CNN variants (04), random-forest case studies
  (05/06a/06b), and the main federated study (06b/08).

Everything is documented — methodology, per-drug tables, loss curves and
caveats — at
**[asd-standard.github.io/Dryad_DRIAMS](https://asd-standard.github.io/Dryad_DRIAMS/)**.

## Key results

Macro means over the ten drugs unless noted; full tables and caveats in the
documentation.

- **Pooled 10-drug baselines** ([07](docs/07-Dedicated-MLP-Aggregated/index.rst)):
  logistic regression **0.788 BalAcc / 0.862 AUC**, MLP 0.784 / 0.848,
  random forest 0.761 / 0.843.
- **Cross-site generalisation** ([03](docs/03-CrossSite-Classifier/index.rst) /
  [04](docs/04-Multi-Label-mlp/index.rst)): training on Site A and testing on
  B/C/D drops Balanced Accuracy to ~0.64; pooling the four sites recovers
  ~+0.14 — domain shift, not model capacity, is the bottleneck.
- **Multi-label** ([04](docs/04-Multi-Label-mlp/index.rst)): one
  shared-backbone network predicting all 10 drugs simultaneously ties the
  per-drug models (~0.775 pooled) and OneVsRest LR (~0.78); a 1D CNN adds
  nothing, and the 0.5-threshold effect is quantified.
- **Random forest case studies**
  ([05](docs/05-RandomForest-Ceftazidime-Ecoli/index.rst),
  [06a](docs/06a-Ceftazidime-E-coli/index.rst),
  [06b](docs/06b-Ceftriaxone-E-coli/index.rst)): RF lags LR/MLP on average;
  on *E. coli* × ceftazidime, cross-site transfer collapses while pooled
  ranking reaches ~0.74 AUC.
- **Federated learning**
  ([08](docs/08-Federated-mlp-lr-rf/index.rst)): Flower-based FedAvg MLP/LR
  recover **60–94%** of the cross-site → pooled gap; mean all-site Balanced
  Accuracy **0.729 ± 0.049** (FedAvg LR) and 0.728 ± 0.054 (FedAvg MLP) vs
  0.759 ± 0.051 for the pooled MLP; FedRF (tree collection) reaches
  0.675 ± 0.053 vs 0.705 ± 0.068 centralized RF. A site-D ablation shows
  removing the largest site changes aggregate performance by ≤0.02.

## Dataset

**DRIAMS** = Database of ResIstance against Antimicrobials with MALDI-TOF Mass
Spectrometry — clinical MALDI-TOF spectra linked to AMR phenotypes from four
Swiss institutions (2018):

| Site | Hospital | Binned spectra |
|------|----------|---------------:|
| A | University Hospital Basel | 30,069 |
| B | Canton Hospital Basel-Land | 2,386 |
| C | Canton Hospital Aarau | 4,737 |
| D | Viollier AG (private laboratory) | 10,436 |

- Spectra are binned at 3 Da resolution → 6000 features per sample; only
  susceptible/resistant labels are kept (intermediate and untested dropped).
- The processing pipeline produced **97 drug–site combinations**; the ten
  drugs present at all four sites (Ciprofloxacin, Gentamicin,
  Amoxicillin-Clavulanic acid, Piperacillin-Tazobactam, Cefepime, Ceftriaxone,
  Imipenem, Ceftazidime, Vancomycin, Amikacin) are used for the cross-site and
  federated studies. Full tables in
  [00-Data-Processing/README.md](00-Data-Processing/README.md).
- **The dataset is not stored in this repository**: download it from Dryad
  (144.84 GB, four site archives), extract it, and run the 00 pipeline (below).

## Repository layout

| Path | Contents |
|------|----------|
| [`00-Data-Processing/`](00-Data-Processing/) | Selection/filtering pipeline → per-drug ML-ready CSVs |
| [`01-LogisticAnalysis-Aggregated/`](01-LogisticAnalysis-Aggregated/) | LR baseline: raw / L2-regularised / PCA on pooled data |
| [`02-MLPClassifier-Aggregated/`](02-MLPClassifier-Aggregated/) | MLP baseline, architecture and loss-curve diagnostics |
| [`03-CrossSite-Classifier/`](03-CrossSite-Classifier/) | Train on A, test on B/C/D (LR + MLP) |
| [`04-Multi-Label-mlp/`](04-Multi-Label-mlp/) | 10-drug shared backbone, CNN variant, cross-site + pooled |
| [`05-RandomForest-Ceftazidime-Ecoli/`](05-RandomForest-Ceftazidime-Ecoli/) | RF on *E. coli* × ceftazidime + feature importance |
| [`06a-Ceftazidime-E-coli/`](06a-Ceftazidime-E-coli/) | Ceftazidime × *E. coli* case study (LR/MLP/RF) |
| [`06b-Ceftriaxone-E-coli/`](06b-Ceftriaxone-E-coli/) | Ceftriaxone × *E. coli* — first federated prototype |
| [`07-Dedicated-MLP-Aggregated/`](07-Dedicated-MLP-Aggregated/) | Per-drug LR/MLP/RF on pooled data; emits hyperparameters for 08 |
| [`08-Federated-mlp-lr-rf/`](08-Federated-mlp-lr-rf/) | Main federated study + species masking, UMAP and site-D diagnostics |
| [`docs/`](docs/) | Sphinx documentation sources (published above) |

### What is (and isn't) versioned

Only code and prose live in git: `*.ipynb`, `*.py`, `*.rst`, `*.md` and
`Makefile`. Generated artifacts — result CSVs, PDF figures, pickles, cached
arrays and the dataset itself — are gitignored and stay local in each
analysis folder (`results_*`). Cloning the repository gives you the analysis
code and notebooks, not the trained results.

## Models & evaluation protocol

- **Model families** — logistic regression, MLP, random forest,
  shared-backbone multi-label network, 1D CNN, and federated learning
  (FedAvg, FedProx, FedLR, FedRF with [Flower](https://flower.ai/)).
- **Splits** — species-stratified 70/15/15 (pooled) and 80/20 (cross-site);
  no species crosses a train/test boundary.
- **Preprocessing** — `log1p` + standardisation, fitted on the training split
  only.
- **Metrics** — Balanced Accuracy (primary) and AUC-ROC (threshold-free);
  per-drug decision thresholds are tuned on held-out validation data.
- Runs are single-seed; confidence-interval limitations and per-analysis
  caveats are documented on each page.

## Installation

Python 3.12 is recommended.

```bash
# pip / venv
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# or conda
conda env create -f environment.yml
conda activate driams
```

`requirements.txt` is the pip package list; `environment.yml` is the conda
counterpart (environment name, channels and dependencies, including pip-only
packages such as MaldiDeepKit/MaldiAMRKit). Both list the same stack.

## Reproducing the analyses

1. **Download the dataset** from Dryad:
   <https://doi.org/10.5061/dryad.bzkh1899q> — extract the four site archives
   preserving the `DRIAMS-A…D` directory layout.
2. **Build the processed CSVs**:
   `python 00-Data-Processing/process_driams.py` (defaults: ≥500 susceptible
   and ≥10 resistant per drug) → `Processed/Proc_DRIAMS-{A..D}/{drug}/data.csv`.
3. **Run the analyses** in the numbered folders — each documentation page
   lists its notebooks and outputs. Notebooks run on Google Colab (Drive
   paths) or locally (data paths are auto-detected); some grids take hours,
   so a Colab GPU is recommended.
4. **Build the documentation** locally (optional): `make -C docs html`.

## Documentation

The full study documentation — motivation, data processing, validation
protocol, all analyses, glossary — is published at
**<https://asd-standard.github.io/Dryad_DRIAMS/>** (sources in [`docs/`](docs/)).

```bash
make -C docs html     # build into docs/_build/html
make -C docs deploy   # build + force-push to the gh-pages branch
```

## How to cite

If you use this repository, please cite:

> Silvestri, A., & Rocchi, E. (2026). *DRIAMS — Federated AMR Prediction from
> MALDI-TOF Spectra* [Software].
> <https://github.com/asd-standard/Dryad_DRIAMS>

If you use the DRIAMS dataset, please also cite the dataset and its
publication:

> Weis, C., Cuénod, A., Rieck, B., Dubuis, O., Graf, S., Lang, C., Oberle, M.,
> Brackmann, M., Søgaard, K. K., Osthoff, M., Borgwardt, K., & Egli, A. (2022).
> Direct antimicrobial resistance prediction from clinical MALDI-TOF mass
> spectra using machine learning. *Nature Medicine*, 28(1), 164–174.
> <https://doi.org/10.1038/s41591-021-01619-9>

> Weis, C., Cuénod, A., Rieck, B., et al. (2025). *DRIAMS: Database of
> Resistance Information on Antimicrobials and MALDI-TOF Mass Spectra*
> [Dataset]. Dryad. <https://doi.org/10.5061/dryad.bzkh1899q>

A machine-readable [`CITATION.cff`](CITATION.cff) is provided — GitHub's
"Cite this repository" button reads it.

## Acknowledgements

- **[Ettore Rocchi](https://github.com/EttoreRocchi)** — creator of
  [MaldiDeepKit](https://github.com/EttoreRocchi/MaldiDeepKit) and
  [MaldiAMRKit](https://github.com/EttoreRocchi/MaldiAMRKit), which power the
  preprocessing, training and evaluation utilities used throughout this
  study, and for many helpful consultations.
- The DRIAMS authors and the four contributing institutions (University
  Hospital Basel, Canton Hospital Basel-Land, Canton Hospital Aarau,
  Viollier AG).
- [Flower (flwr)](https://flower.ai/) for the federated-learning framework.
- Google Colab for the compute used to train most models.

## License

© 2026 Andrea Silvestri. Licensed under
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) — free to use,
share and adapt, including commercially, provided you give appropriate credit
("cite as" above). See [`LICENSE`](LICENSE).

## Status

Active research code; documentation last updated October 2026. Questions,
bugs or contributions: please open a
[GitHub issue](https://github.com/asd-standard/Dryad_DRIAMS/issues).
