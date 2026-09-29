#!/usr/bin/env python3
"""Process DRIAMS binned_6000 data into per-drug ML-ready CSV files.

Uses maldiamrkit for loading + pandas/numpy for filtering and saving.
Outputs go to Dryad-DataSet/Processed/Proc_{SITE}/{drug}/ with:
  - data.csv   : feature matrix (N x 6000) + label column
  - summary.csv: per-drug statistics
"""

import os
import sys
import time
import json
from pathlib import Path

import numpy as np
import pandas as pd
from tqdm import tqdm

# ── Configuration ──────────────────────────────────────────────────────────

DRYAD = Path("/media/asd/8f69beed-e984-445f-b8b3-abbb6a1a4b3f/Dryad-DataSet")
OUTPUT = DRYAD / "Processed"

SITES = {
    "DRIAMS-A": {
        "binned": DRYAD / "DRIAMS-A/binned_6000/2018",
        "meta":   DRYAD / "DRIAMS-A/id/2018/2018_clean.csv",
    },
    "DRIAMS-B": {
        "binned": DRYAD / "DRIAMS-B/binned_6000/2018",
        "meta":   DRYAD / "DRIAMS-B/id/2018/2018_clean.csv",
    },
    "DRIAMS-C": {
        "binned": DRYAD / "DRIAMS-C/binned_6000/2018",
        "meta":   DRYAD / "DRIAMS-C/id/2018/2018_clean.csv",
    },
    "DRIAMS-D": {
        "binned": DRYAD / "DRIAMS-D/binned_6000/2018",
        "meta":   DRYAD / "DRIAMS-D/id/2018/2018_clean.csv",
    },
}

MIN_S = 500      # minimum susceptible count per drug
MIN_R = 10       # minimum resistant count (need at least some to classify)

NON_DRUG_COLS = {"code", "species", "genus", "combined_code", "laboratory_species", "Unnamed: 0", "Unnamed: 0.1"}


# ── Helpers ────────────────────────────────────────────────────────────────

def load_binned_spectra(codes, binned_dir):
    """Load binned spectra for given codes from the binned directory."""
    spectra = {}
    missing = 0
    for code in tqdm(codes, desc="  Loading spectra", leave=False):
        fpath = binned_dir / f"{code}.txt"
        if fpath.exists():
            arr = np.loadtxt(fpath, skiprows=1, usecols=1)
            spectra[code] = arr
        else:
            missing += 1
    if missing:
        print(f"  Warning: {missing} spectra not found")
    return spectra


def process_site(site_name, paths):
    """Process one DRIAMS site, saving per-drug data."""
    print(f"\n{'='*70}")
    print(f"  Processing {site_name}")
    print(f"{'='*70}")

    # ── Load metadata ──
    meta = pd.read_csv(paths["meta"], dtype=str)
    print(f"  Metadata: {len(meta)} rows, {len(meta.columns)} columns")

    # ── Find matching binned files ──
    binned_dir = Path(paths["binned"])
    binned_codes = {f.stem for f in binned_dir.glob("*.txt")}
    meta_matched = meta[meta["code"].isin(binned_codes)].copy()
    print(f"  Binned files found: {len(binned_codes)}")
    print(f"  Codes matched to binned: {len(meta_matched)}/{len(meta)}")

    # ── Identify drug columns ──
    drug_cols = [c for c in meta.columns if c not in NON_DRUG_COLS]
    print(f"  Drug columns: {len(drug_cols)}")

    # ── Pre-compile per-drug filter info ──
    drug_info = {}
    for drug in drug_cols:
        vals = meta_matched[drug]
        s_mask = vals == "S"
        r_mask = vals == "R"
        s_count = s_mask.sum()
        r_count = r_mask.sum()
        if s_count >= MIN_S and r_count >= MIN_R:
            drug_info[drug] = {
                "s_count": s_count,
                "r_count": r_count,
                "indices": meta_matched.index[s_mask | r_mask].tolist(),
            }

    print(f"  Drugs meeting S>={MIN_S} and R>={MIN_R}: {len(drug_info)}")

    if not drug_info:
        print("  No drugs meet criteria. Skipping.")
        return []

    # ── Load spectra once for all qualifying codes ──
    all_codes_needed = set()
    for info in drug_info.values():
        all_codes_needed.update(meta_matched.loc[info["indices"], "code"])
    all_codes_needed = sorted(all_codes_needed)

    print(f"  Loading {len(all_codes_needed)} unique spectra...")
    spectra_map = load_binned_spectra(all_codes_needed, binned_dir)

    # ── Build code → feature index mapping ──
    code_to_idx = {code: i for i, code in enumerate(all_codes_needed)}

    # ── Build full feature matrix ──
    X_full = np.array([spectra_map[c] for c in all_codes_needed])
    print(f"  Feature matrix: {X_full.shape}")

    # ── Per-drug output ──
    out_base = OUTPUT / f"Proc_{site_name}"
    report = []

    for drug, info in tqdm(drug_info.items(), desc="  Saving drugs"):
        drug_dir = out_base / drug.replace("/", "_").replace(" ", "_")
        drug_dir.mkdir(parents=True, exist_ok=True)

        subset = meta_matched.loc[info["indices"]]
        codes = subset["code"].values
        idxs = [code_to_idx[c] for c in codes]
        X = X_full[idxs]
        y = (subset[drug].values == "R").astype(int)

        s_count = int(info["s_count"])
        r_count = int(info["r_count"])
        n_total = s_count + r_count

        # Save data matrix
        df_data = pd.DataFrame({
            "code": codes,
            "species": subset["species"].values,
            "label": y,
        })
        bin_df = pd.DataFrame(X, columns=[f"bin_{i}" for i in range(X.shape[1])])
        df_data = pd.concat([df_data, bin_df], axis=1)
        df_data.to_csv(drug_dir / "data.csv", index=False)

        report.append({
            "site": site_name,
            "drug": drug,
            "n_samples": n_total,
            "n_susceptible": s_count,
            "n_resistant": r_count,
            "resistance_rate": round(r_count / n_total * 100, 1),
            "n_features": X.shape[1],
            "output_path": str(drug_dir),
        })

    # ── Write site-level summary ──
    df_report = pd.DataFrame(report)
    df_report.to_csv(out_base / "summary.csv", index=False)
    print(f"\n  Site summary saved to {out_base / 'summary.csv'}")
    print(f"  Total drugs saved: {len(report)}")

    return report


# ── Main ───────────────────────────────────────────────────────────────────

def main():
    OUTPUT.mkdir(exist_ok=True)
    print(f"Output root: {OUTPUT}")
    print(f"Filter: S >= {MIN_S}, R >= {MIN_R}")

    all_reports = []
    for site_name, paths in SITES.items():
        if not paths["binned"].exists():
            print(f"\n  SKIP {site_name}: binned dir not found")
            continue
        report = process_site(site_name, paths)
        all_reports.extend(report)

    # ── Write global summary ──
    if all_reports:
        df_global = pd.DataFrame(all_reports)
        df_global.to_csv(OUTPUT / "global_summary.csv", index=False)
        print(f"\n{'='*70}")
        print(f"  COMPLETE: {len(all_reports)} drug-site combinations saved")
        print(f"  Global summary: {OUTPUT / 'global_summary.csv'}")
        print(f"\n  Per-site breakdown:")
        for site_name in SITES:
            count = sum(1 for r in all_reports if r["site"] == site_name)
            print(f"    Proc_{site_name}: {count} drugs")
    else:
        print("\n  No data saved.")

if __name__ == "__main__":
    main()
