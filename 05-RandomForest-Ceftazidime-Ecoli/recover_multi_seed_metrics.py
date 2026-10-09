#!/usr/bin/env python3
"""Recover per-seed metrics and the tuning-holdout score for 05.

Re-fits only the five pooled multi-seed kernels of
``05-RandomForest-Ceftazidime-Ecoli.ipynb``, replicating its data loading and
model configuration exactly. This also recovers the unexported tuning-holdout
score: ``GridSearchCV(refit=True)`` refits the winning configuration on the
full tuning split with ``random_state=42``, which is the same fit as
multi-seed seed 42.

Two modes, because the notebook changed after the June 2026 exports:

- ``legacy`` (default): raw spectra, exactly the code that produced
  ``results_rf/report.md`` and the figures.  Writes
  ``results_rf/multi_seed_metrics.csv``.
- ``current``: log1p+standardize preprocessing added by commit ec38c13
  (2026-07-07).  Writes ``results_rf/multi_seed_metrics_current_notebook.csv``.

Note (2026-10-09): the June 2026 exports do not reproduce from this code in
either mode (the closest match was a deep configuration with
``max_depth=None, min_samples_leaf=2``); they are archived in
``results_rf_2026-06-13/``. The current notebook was re-run locally and its
results are documented in the Sphinx page; this script remains as a
reproduction check for the pooled multi-seed loop.

Run:  python recover_multi_seed_metrics.py [--mode legacy|current]
"""

import argparse
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import balanced_accuracy_score, roc_auc_score
from sklearn.model_selection import train_test_split

from maldideepkit.base.data import apply_input_transform, fit_input_transform

SEEDS = [42, 123, 456, 789, 1011]
DRUG = "Ceftazidime"
SPECIES = "Escherichia coli"
BEST_PARAMS = dict(
    n_estimators=100, max_depth=10, min_samples_leaf=10, class_weight="balanced"
)

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--mode", choices=["legacy", "current"], default="legacy",
                    help="legacy = raw spectra (June exports); current = log1p+standardize")
args = parser.parse_args()

HERE = Path(__file__).resolve().parent
OUT_DIR = HERE / "results_rf"
OUT_NAME = ("multi_seed_metrics.csv" if args.mode == "legacy"
            else "multi_seed_metrics_current_notebook.csv")

CANDIDATES = [
    Path("/media/asd/8f69beed-e984-445f-b8b3-abbb6a1a4b3f/Dryad-DataSet/Processed"),
    Path("/mnt/sda-home/asd/Projects/Flower/DataSet/Dryad-DataSet/Processed"),
    Path("/home/asd/Projects/Flower/DataSet/Dryad-DataSet/Processed"),
]
DATA_ROOT = next((p for p in CANDIDATES if p.exists()), None)
assert DATA_ROOT is not None, f"no data root found among {CANDIDATES}"
print(f"mode: {args.mode} | DATA_ROOT: {DATA_ROOT}")

# ---------------------------------------------------------------------------
# Data: Ceftazidime per site, filter to E. coli, pool A -> B -> C -> D
# ---------------------------------------------------------------------------
Xs, ys = [], []
for site in "ABCD":
    df = pd.read_csv(DATA_ROOT / f"Proc_DRIAMS-{site}" / DRUG / "data.csv")
    df = df[df["species"] == SPECIES]
    bin_cols = [c for c in df.columns if c.startswith("bin_")]
    Xs.append(df[bin_cols].to_numpy(dtype="float32"))
    ys.append(df["label"].to_numpy(dtype="int64"))
    print(f"  DRIAMS-{site}: n={len(ys[-1]):5d}  R={int(ys[-1].sum())}")

X_pooled = np.vstack(Xs)
y_pooled = np.hstack(ys)
print(f"pooled: {X_pooled.shape[0]} x {X_pooled.shape[1]}  R={int(y_pooled.sum())}")

# ---------------------------------------------------------------------------
# Five pooled 75/25 splits; seed 42 == the section-3 tuning holdout
# ---------------------------------------------------------------------------
rows = []
for seed in SEEDS:
    X_tr_raw, X_te_raw, y_tr, y_te = train_test_split(
        X_pooled, y_pooled, test_size=0.25, stratify=y_pooled, random_state=seed
    )
    if args.mode == "current":
        state = fit_input_transform(X_tr_raw, "log1p+standardize")
        X_tr = apply_input_transform(X_tr_raw, state)
        X_te = apply_input_transform(X_te_raw, state)
    else:
        X_tr, X_te = X_tr_raw, X_te_raw

    rf = RandomForestClassifier(
        **BEST_PARAMS, oob_score=True, random_state=seed, n_jobs=-1
    )
    rf.fit(X_tr, y_tr)

    preds = rf.predict(X_te)
    proba = rf.predict_proba(X_te)[:, 1]
    row = {
        "seed": seed,
        "role": "tuning holdout (= multi-seed)" if seed == 42 else "multi-seed",
        "n_train": len(y_tr),
        "n_train_R": int(y_tr.sum()),
        "n_test": len(y_te),
        "n_test_R": int(y_te.sum()),
        "BalAcc": balanced_accuracy_score(y_te, preds),
        "AUC": roc_auc_score(y_te, proba),
        "OOB_err": 1 - rf.oob_score_,
    }
    rows.append(row)
    print(
        f"  seed={seed:4d}  BalAcc={row['BalAcc']:.4f}  AUC={row['AUC']:.4f}  "
        f"OOB={row['OOB_err']:.4f}"
    )

res = pd.DataFrame(rows)
OUT_DIR.mkdir(exist_ok=True)
out_path = OUT_DIR / OUT_NAME
res.to_csv(out_path, index=False)

print(f"\nSaved: {out_path}\n")
print(res.round(4).to_string(index=False))

# Population std (ddof=0), as used in report.md
print(
    f"\n5-seed mean±std: BalAcc {np.mean(res.BalAcc):.4f} ± {np.std(res.BalAcc):.4f}  |  "
    f"AUC {np.mean(res.AUC):.4f} ± {np.std(res.AUC):.4f}"
)
if args.mode == "legacy":
    print("report.md:       BalAcc 0.5435 ± 0.0084  |  AUC 0.7273 ± 0.0281")
print(
    f"\nTuning holdout (seed 42): BalAcc {res.BalAcc.iloc[0]:.4f}  "
    f"AUC {res.AUC.iloc[0]:.4f}  OOB {res.OOB_err.iloc[0]:.4f}"
)
