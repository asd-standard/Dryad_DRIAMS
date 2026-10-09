#!/usr/bin/env python3
"""Aggregated 70/15/15 comparison: OneVsRest LR vs shared MLP vs shared CNN.

Reads the exported per-drug Balanced Accuracy from the current runs:

- ``01-results_multilabel/aggregated_lr_val_tuned.csv`` (04-00b: ``Test_BalAcc``,
  the corrected validation-tuned LR baseline)
- ``01-results_multilabel/multilabel_results.csv`` (04-00: ``AGG_MLP_BalAcc``)
- ``../04-01-MultiLabel-Cnn-Classifier/results_multilabel_cnn/cnn_results.csv``
  (04-01: ``CNN_Shared_BalAcc``)

All three models use the same species-stratified 70/15/15 split of the pooled
A+B+C+D data (seed 42) and per-drug decision thresholds tuned on the
validation split, so the bars are directly comparable. The original 04-00
aggregated LR export is deliberately not used: its thresholds are tuned on
the test set.

Writes:
- ``01-results_multilabel/aggregated_lr_mlp_cnn.pdf`` (next to the results)
- ``docs/_static/04-Multi-Label-mlp/04_aggregated_lr_mlp_cnn.svg`` (for Sphinx)
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
ANALYSIS_ROOT = HERE.parents[1]

LR_CSV = HERE / "01-results_multilabel" / "aggregated_lr_val_tuned.csv"
MLP_CSV = HERE / "01-results_multilabel" / "multilabel_results.csv"
CNN_CSV = (
    ANALYSIS_ROOT
    / "04-Multi-Label-mlp"
    / "04-01-MultiLabel-Cnn-Classifier"
    / "results_multilabel_cnn"
    / "cnn_results.csv"
)
PDF_OUT = HERE / "01-results_multilabel" / "aggregated_lr_mlp_cnn.pdf"
SVG_OUT = ANALYSIS_ROOT / "docs" / "_static" / "04-Multi-Label-mlp" / "04_aggregated_lr_mlp_cnn.svg"

lr = pd.read_csv(LR_CSV)[["Drug", "Test_BalAcc"]].rename(columns={"Test_BalAcc": "LR_BalAcc"})
ml = pd.read_csv(MLP_CSV)
cnn = pd.read_csv(CNN_CSV)
df = lr.merge(ml[["Drug", "AGG_MLP_BalAcc"]], on="Drug", how="left",
              validate="one_to_one").merge(
    cnn[["Drug", "CNN_Shared_BalAcc"]], on="Drug", how="left", validate="one_to_one"
)

series = [
    ("OneVsRest LR", "LR_BalAcc", "#aec7e8"),
    ("Shared MLP", "AGG_MLP_BalAcc", "#ff7f0e"),
    ("Shared CNN", "CNN_Shared_BalAcc", "#1f77b4"),
]

fig, ax = plt.subplots(figsize=(12, 5))
x = np.arange(len(df))
width = 0.27
for i, (label, col, color) in enumerate(series):
    offset = (i - 1) * width
    ax.bar(x + offset, df[col], width,
           label=f"{label} (mean {df[col].mean():.3f})", color=color)

ax.set_xticks(x)
ax.set_xticklabels(df["Drug"], fontsize=8, rotation=45, ha="right")
ax.set_ylabel("Test Balanced Accuracy")
ax.set_title("Aggregated 70/15/15 — LR vs shared MLP vs shared CNN")
ax.set_ylim(0, 1.0)
ax.axhline(0.5, color="gray", ls="--", alpha=0.4)
ax.grid(True, ls="--", lw=0.5, color="gray", alpha=0.7)
ax.legend(fontsize=9)
fig.tight_layout()

PDF_OUT.parent.mkdir(parents=True, exist_ok=True)
SVG_OUT.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(PDF_OUT, bbox_inches="tight")
fig.savefig(SVG_OUT, bbox_inches="tight")

print(df.round(4).to_string(index=False))
print()
for label, col, _ in series:
    print(f"{label:14s} mean={df[col].mean():.4f}")
print(f"\nSaved: {PDF_OUT}\nSaved: {SVG_OUT}")
