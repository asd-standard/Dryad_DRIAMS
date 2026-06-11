# DRIAMS Processing Pipeline

Reproducible pipeline for selecting, filtering, and preparing the
[DRIAMS](https://doi.org/10.1101/2020.07.30.228411) dataset into per-drug,
ML-ready CSV files.

## Overview

**Input:** DRIAMS `binned_6000` spectra (`.txt` files, 6,000 bins at 3 Da
resolution) + antimicrobial resistance metadata.

**Output:** One `data.csv` per drug per site, containing:

| Column              | Description                                  |
|---------------------|----------------------------------------------|
| `code`              | Sample identifier (links to original `.txt`) |
| `species`           | Organism name                                |
| `label`             | 0 = Susceptible, 1 = Resistant               |
| `bin_0` … `bin_5999` | 6,000 binned m/z intensity features          |

## Dataset

**DRIAMS** = Database of ResIstance against Antimicrobials with MALDI-TOF Mass
Spectrometry. MALDI-TOF spectra from clinical bacterial isolates linked to
AMR profiles from four Swiss hospitals (2018).

| Site  | Hospital                        | Binned spectra | Metadata rows |
|-------|---------------------------------|----------------|---------------|
| A     | University Hospital of Basel    | 30,069         | 30,069        |
| B     | Canton Hospital Basel-Land      | 2,386          | 5,897         |
| C     | Canton Hospital Aarau           | 4,737          | 4,696         |
| D     | Viollier AG laboratory          | 10,436         | 10,436        |

Each `.txt` file in `binned_6000/2018/` contains 6,000 rows
(bin_index, binned_intensity) with 3 Da bin width, spanning the full
m/z range.

## Prerequisites

### Environment

```bash
conda create -n driams python=3.12 -y
conda activate driams
pip install numpy pandas tqdm
```

### Data layout

The script expects this directory structure:

```
Dryad-DataSet/
├── DRIAMS-A/
│   ├── binned_6000/2018/   # {code}.txt files
│   └── id/2018/2018_clean.csv
├── DRIAMS-B/
│   ├── binned_6000/2018/
│   └── id/2018/2018_clean.csv
├── DRIAMS-C/
│   ├── binned_6000/2018/
│   └── id/2018/2018_clean.csv
└── DRIAMS-D/
    ├── binned_6000/2018/
    └── id/2018/2018_clean.csv
```

## Usage

### Basic run

```bash
python process_driams.py
```

This processes all four sites with default filters (S ≥ 500, R ≥ 10).

### Filtering drugs

The script selects drugs that meet **two thresholds**:

| Parameter | Variable   | Default | Meaning                            |
|-----------|------------|---------|------------------------------------|
| Min S     | `MIN_S`    | 500     | At least this many susceptible     |
| Min R     | `MIN_R`    | 10      | At least this many resistant       |

To change thresholds, edit the constants at the top of `process_driams.py`:

```python
MIN_S = 500      # minimum susceptible count per drug
MIN_R = 10       # minimum resistant count
```

### Configuration

Site paths are configured in the `SITES` dictionary:

```python
SITES = {
    "DRIAMS-A": {
        "binned": DRYAD / "DRIAMS-A/binned_6000/2018",
        "meta":   DRYAD / "DRIAMS-A/id/2018/2018_clean.csv",
    },
    "DRIAMS-B": {
        "binned": DRYAD / "DRIAMS-B/binned_6000/2018",
        "meta":   DRYAD / "DRIAMS-B/id/2018/2018_clean.csv",
    },
    # ... C, D
}
```

Set `DRYAD` and `OUTPUT` to point to your own paths.

## Output Structure

```
Processed/
├── Processing/                  # This directory (scripts + docs)
│   ├── README.md
│   ├── process_driams.py
│   ├── 01-LogisticAnalysis-Aggregated.ipynb
│   └── 02-MLPClassifier-Aggregated.ipynb
├── global_summary.csv           # All drug-site results
├── Proc_DRIAMS-A/
│   ├── summary.csv              # Per-site stats
│   └── Ciprofloxacin/
│       └── data.csv             # (N, 6003) feature matrix
├── Proc_DRIAMS-B/
│   └── {drug}/data.csv
├── Proc_DRIAMS-C/
│   └── {drug}/data.csv
└── Proc_DRIAMS-D/
    └── {drug}/data.csv
```

### `global_summary.csv` columns

| Column            | Description                     |
|-------------------|---------------------------------|
| `site`            | DRIAMS-A, B, C, or D          |
| `drug`            | Antibiotic name                 |
| `n_samples`       | Total R+S samples               |
| `n_susceptible`   | Susceptible count               |
| `n_resistant`     | Resistant count                 |
| `resistance_rate` | R / (R+S) × 100                 |
| `n_features`      | Always 6000                     |
| `output_path`     | Directory containing data.csv   |

### `data.csv` columns

| Column              | Type   | Description                        |
|---------------------|--------|------------------------------------|
| `code`              | str    | Sample UUID, links to original file |
| `species`           | str    | Organism name                      |
| `label`             | int    | 0=S, 1=R                          |
| `bin_0` … `bin_5999` | float | Binned spectral intensities        |

## Loading Data for ML

### Single drug, single site

```python
import pandas as pd

df = pd.read_csv("Processed/Proc_DRIAMS-D/Ciprofloxacin/data.csv")
X = df.filter(like="bin_").values        # (n_samples, 6000)
y = df["label"].values                    # (n_samples,)
species = df["species"].values

print(f"Shape: {X.shape}, S={sum(y==0)}, R={sum(y==1)}")
```

### With sklearn

```python
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

pipe = Pipeline([
    ("scaler", StandardScaler()),
    ("clf", RandomForestClassifier(n_estimators=100, random_state=42)),
])

scores = cross_val_score(pipe, X, y, cv=5, scoring="balanced_accuracy")
print(f"Balanced accuracy: {scores.mean():.3f} ± {scores.std():.3f}")
```

### Stratified splitting by species

```python
from maldiamrkit.evaluation import stratified_species_drug_split

X_train, X_test, y_train, y_test = stratified_species_drug_split(
    X, y, species=species, test_size=0.2, random_state=42
)
```

## Results Summary

**97 drug-site combinations** generated with default thresholds.

### DRIAMS-A — 34 drugs

| Drug                         | Samples  | S      | R     | Resist% |
|------------------------------|----------|--------|-------|---------|
| Ciprofloxacin                | 8,094    | 6,450  | 1,644 | 20.3%   |
| Meropenem                    | 7,956    | 6,787  | 1,169 | 14.7%   |
| Imipenem                     | 7,700    | 6,283  | 1,417 | 18.4%   |
| Piperacillin-Tazobactam      | 7,698    | 6,115  | 1,583 | 20.6%   |
| Cefepime                     | 7,564    | 6,247  | 1,317 | 17.4%   |
| Ampicillin-Amoxicillin       | 7,366    | 1,440  | 5,926 | 80.5%   |
| Cotrimoxazole                | 7,176    | 5,907  | 1,269 | 17.7%   |
| Ceftriaxone                  | 7,040    | 5,302  | 1,738 | 24.7%   |
| Amoxicillin-Clavulanic acid  | 6,858    | 4,191  | 2,667 | 38.9%   |
| Levofloxacin                 | 5,704    | 4,711  | 993   | 17.4%   |
| Colistin                     | 5,028    | 4,215  | 813   | 16.2%   |
| Tobramycin                   | 5,020    | 4,660  | 360   | 7.2%    |
| Ceftazidime                  | 4,684    | 4,167  | 517   | 11.0%   |
| Amikacin                     | 4,674    | 4,627  | 47    | 1.0%    |
| Ertapenem                    | 4,029    | 3,976  | 53    | 1.3%    |
| Vancomycin                   | 3,994    | 3,909  | 85    | 2.1%    |
| Tigecycline                  | 3,367    | 3,349  | 18    | 0.5%    |
| Linezolid                    | 3,366    | 3,354  | 12    | 0.4%    |
| Penicillin                   | 3,299    | 862    | 2,437 | 73.9%   |
| Daptomycin                   | 3,068    | 3,038  | 30    | 1.0%    |
| Clindamycin                  | 3,048    | 2,200  | 848   | 27.8%   |
| Oxacillin                    | 2,984    | 1,859  | 1,125 | 37.7%   |
| Rifampicin                   | 2,946    | 2,868  | 78    | 2.6%    |
| Fusidic acid                 | 2,891    | 2,026  | 865   | 29.9%   |
| Erythromycin                 | 2,878    | 1,779  | 1,099 | 38.2%   |
| Gentamicin                   | 2,762    | 2,239  | 523   | 18.9%   |
| Cefuroxime                   | 2,744    | 1,712  | 1,032 | 37.6%   |
| Cefazolin                    | 2,740    | 1,708  | 1,032 | 37.7%   |
| Tetracycline                 | 2,686    | 1,998  | 688   | 25.6%   |
| Teicoplanin                  | 2,113    | 2,091  | 22    | 1.0%    |
| Cefpodoxime                  | 1,949    | 1,272  | 677   | 34.7%   |
| Fosfomycin-Trometamol        | 1,720    | 1,349  | 371   | 21.6%   |
| Norfloxacin                  | 1,667    | 1,472  | 195   | 11.7%   |
| Nitrofurantoin               | 551      | 515    | 36    | 6.5%    |

### DRIAMS-B — 24 drugs

| Drug                         | Samples  | S      | R     | Resist% |
|------------------------------|----------|--------|-------|---------|
| Ampicillin                   | 1,348    | 634    | 714   | 53.0%   |
| Ciprofloxacin                | 1,982    | 1,680  | 302   | 15.2%   |
| Amoxicillin-Clavulanic acid  | 1,969    | 1,454  | 515   | 26.2%   |
| Cotrimoxazol                 | 1,748    | 1,553  | 195   | 11.2%   |
| Cefepime                     | 1,675    | 1,420  | 255   | 15.2%   |
| Gentamicin                   | 1,544    | 1,414  | 130   | 8.4%    |
| Fosfomycin                   | 1,535    | 1,242  | 293   | 19.1%   |
| Vancomycin                   | 1,236    | 1,220  | 16    | 1.3%    |
| Imipenem                     | 1,173    | 1,123  | 50    | 4.3%    |
| Levofloxacin                 | 1,179    | 1,007  | 172   | 14.6%   |
| Piperacillin-Tazobactam      | 1,159    | 987    | 172   | 14.8%   |
| Ceftriaxone                  | 1,082    | 970    | 112   | 10.4%   |
| Clindamycin                  | 1,031    | 822    | 209   | 20.3%   |
| Erythromycin                 | 947      | 714    | 233   | 24.6%   |
| Ceftazidime                  | 933      | 834    | 99    | 10.6%   |
| Amikacin                     | 911      | 900    | 11    | 1.2%    |
| Tetracycline                 | 877      | 747    | 130   | 14.8%   |
| Ertapenem                    | 804      | 785    | 19    | 2.4%    |
| Rifampicin                   | 801      | 789    | 12    | 1.5%    |
| Norfloxacin                  | 793      | 657    | 136   | 17.2%   |
| Teicoplanin                  | 746      | 736    | 10    | 1.3%    |
| Cefoxitin                    | 742      | 566    | 176   | 23.7%   |
| Fusidic acid                 | 736      | 560    | 176   | 23.9%   |
| Oxacillin                    | 731      | 545    | 186   | 25.4%   |

### DRIAMS-C — 22 drugs

| Drug                         | Samples  | S      | R     | Resist% |
|------------------------------|----------|--------|-------|---------|
| Ampicillin                   | 4,547    | 1,523  | 3,024 | 66.5%   |
| Amoxicillin-Clavulanic acid  | 4,544    | 3,150  | 1,394 | 30.7%   |
| Gentamicin                   | 3,980    | 3,441  | 539   | 13.5%   |
| Ciprofloxacin                | 3,769    | 3,385  | 384   | 10.2%   |
| Cotrimoxazole                | 3,729    | 2,822  | 907   | 24.3%   |
| Ceftriaxone                  | 2,868    | 2,159  | 709   | 24.7%   |
| Cefuroxime                   | 2,840    | 1,766  | 1,074 | 37.8%   |
| Polymyxin B                  | 2,790    | 2,305  | 485   | 17.4%   |
| Ceftazidime                  | 2,757    | 2,420  | 337   | 12.2%   |
| Piperacillin-Tazobactam      | 2,462    | 2,185  | 277   | 11.3%   |
| Imipenem                     | 1,850    | 1,812  | 38    | 2.1%    |
| Amikacin                     | 1,842    | 1,813  | 29    | 1.6%    |
| Cefepime                     | 1,820    | 1,582  | 238   | 13.1%   |
| Nitrofurantoin               | 1,751    | 1,426  | 325   | 18.6%   |
| Oxacillin                    | 1,561    | 851    | 710   | 45.5%   |
| Norfloxacin                  | 1,322    | 1,140  | 182   | 13.8%   |
| Fosfomycin                   | 1,255    | 752    | 503   | 40.1%   |
| Clindamycin                  | 1,223    | 826    | 397   | 32.5%   |
| Vancomycin                   | 1,124    | 1,108  | 16    | 1.4%    |
| Clarithromycin               | 973      | 835    | 138   | 14.2%   |
| Doxycycline                  | 837      | 793    | 44    | 5.3%    |
| Fusidic acid                 | 745      | 714    | 31    | 4.2%    |

### DRIAMS-D — 17 drugs

| Drug                         | Samples  | S      | R     | Resist% |
|------------------------------|----------|--------|-------|---------|
| Gentamicin                   | 10,026   | 9,531  | 495   | 4.9%    |
| Ciprofloxacin                | 9,817    | 8,676  | 1,141 | 11.6%   |
| Fosfomycin                   | 9,616    | 8,156  | 1,460 | 15.2%   |
| Ceftazidime                  | 6,889    | 6,375  | 514   | 7.5%    |
| Ampicillin                   | 6,877    | 2,037  | 4,840 | 70.4%   |
| Piperacillin-Tazobactam      | 6,857    | 6,284  | 573   | 8.4%    |
| Imipenem                     | 6,815    | 6,263  | 552   | 8.1%    |
| Cefepime                     | 6,767    | 6,607  | 160   | 2.4%    |
| Ceftriaxone                  | 6,618    | 6,089  | 529   | 8.0%    |
| Amoxicillin-Clavulanic acid  | 6,596    | 5,080  | 1,516 | 23.0%   |
| Ertapenem                    | 6,597    | 6,478  | 119   | 1.8%    |
| Vancomycin                   | 3,331    | 3,314  | 17    | 0.5%    |
| Tetracycline                 | 3,046    | 2,747  | 299   | 9.8%    |
| Rifampicin                   | 3,008    | 2,987  | 21    | 0.7%    |
| Erythromycin                 | 2,431    | 1,729  | 702   | 28.9%   |
| Amikacin                     | 2,015    | 1,981  | 34    | 1.7%    |
| Meropenem                    | 1,936    | 1,919  | 17    | 0.9%    |

## Cross-Site Analysis — 10 Drugs Present in All 4 Sites

These 10 drugs have processed data in all four hospitals, making them suitable
for cross-site generalisation experiments (train on A, test on B/C/D).

| Drug                          | Total Sp. | Samples | A sp. | B sp. | C sp. | D sp. |
|-------------------------------|-----------|---------|-------|-------|-------|-------|
| Amoxicillin-Clavulanic acid   | 222       | 19,967  | 97    | 65    | 106   | 28    |
| Ciprofloxacin                 | 214       | 23,662  | 145   | 62    | 71    | 44    |
| Ceftriaxone                   | 214       | 17,608  | 132   | 48    | 59    | 29    |
| Imipenem                      | 170       | 17,538  | 100   | 52    | 44    | 41    |
| Piperacillin-Tazobactam       | 168       | 18,176  | 119   | 32    | 52    | 31    |
| Gentamicin                    | 160       | 18,312  | 42    | 38    | 83    | 47    |
| Vancomycin                    | 146       | 9,685   | 99    | 50    | 39    | 13    |
| Cefepime                      | 139       | 17,826  | 104   | 39    | 39    | 33    |
| Ceftazidime                   | 114       | 15,263  | 73    | 23    | 44    | 32    |
| Amikacin                      | 104       | 9,442   | 57    | 30    | 41    | 32    |

## Reproducing from Scratch

1. Download the DRIAMS dataset from Dryad:
   `https://doi.org/10.5061/dryad.bzkh1899q`

2. Extract each site archive maintaining the directory structure:
   ```bash
   tar -xzf DRIAMS_A.tar.gz
   tar -xzf DRIAMS_B.tar.gz
   tar -xzf DRIAMS_C.tar.gz
   tar -xzf DRIAMS_D.tar.gz
   ```

3. Ensure the layout matches the expected structure described above.

4. Activate the conda environment and run:
   ```bash
   conda activate driams
   python Processing/process_driams.py
   ```

5. Output lands in `Processed/Proc_{SITE}/{drug}/data.csv`.

## Using MaldiAMRKit for Downstream Tasks

The output CSVs are ready for [MaldiAMRKit](https://github.com/EttoreRocchi/MaldiAMRKit)
pipelines:

```python
from maldiamrkit import MaldiSet
from maldiamrkit.alignment import Warping
from maldiamrkit.detection import MaldiPeakDetector
from maldiamrkit.evaluation import stratified_species_drug_split, amr_classification_report
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline

# Load data with MaldiAMRKit
df = pd.read_csv("Proc_DRIAMS-D/Ciprofloxacin/data.csv")
X = df.filter(like="bin_").values
y = df["label"].values
species = df["species"].values

# Species-stratified split
X_train, X_test, y_train, y_test = stratified_species_drug_split(
    X, y, species=species, test_size=0.2, random_state=42
)

# Train
pipe = Pipeline([
    ("detect", MaldiPeakDetector(method="local", prominence=0.01)),
    ("warp", Warping(method="shift")),
    ("clf", RandomForestClassifier(n_estimators=100, random_state=42)),
])
pipe.fit(X_train, y_train)
y_pred = pipe.predict(X_test)

# Report
print(amr_classification_report(y_test, y_pred))
```

## Notes

- Only samples with `R` or `S` labels are included; `I` (Intermediate) and
  `NaN` (not tested) are excluded.
- The `binned_6000` stage was chosen because the spectra are already
  preprocessed (smoothing, baseline correction, normalization) and QC-filtered,
  matching the published DRIAMS pipeline exactly.
- For raw-to-binned reprocessing with custom parameters, use MaldiAMRKit's
  `PreprocessingPipeline` on the `raw/` or `preprocessed/` directories.
- Species-stratified splitting is recommended to prevent data leakage, as
  spectra from the same species tend to be more similar.
