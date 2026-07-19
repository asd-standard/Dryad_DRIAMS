# ── SAVE CELL for 07-01 ── Copy-paste this into 07-01 after the LR+MLP loop ──
# This saves per-drug preprocessed data + LR results + MLP results
# so 07-02 can skip data loading and LR training.

import pickle

SAVE_DIR = OUT_DIR  # saves alongside 07-01 outputs

# 1. Save per-drug preprocessed splits, preprocessing state, and raw data
for drug in DRUGS_10:
    if drug not in all_results: continue
    safe_name = drug.replace(" ", "_").replace("-", "_")
    
    # Re-load and re-split to capture raw data (since the loop variables are overwritten)
    X, y, species = load_drug_data(drug)
    idx = np.arange(len(y)).reshape(-1, 1)
    idx_trval, idx_test, _, _ = stratified_species_drug_split(
        idx, y, species=species, test_size=0.15, random_state=SEED)
    idx_trval = idx_trval.flatten().astype(int)
    idx_test = idx_test.flatten().astype(int)
    val_frac = 0.15 / 0.85
    idx_train, idx_val, _, _ = stratified_species_drug_split(
        idx_trval.reshape(-1, 1), y[idx_trval], species=species[idx_trval],
        test_size=val_frac, random_state=SEED)
    idx_train = idx_train.flatten().astype(int)
    idx_val = idx_val.flatten().astype(int)
    
    X_train_raw, y_train = X[idx_train], y[idx_train]
    X_val_raw,   y_val   = X[idx_val], y[idx_val]
    X_test_raw,  y_test  = X[idx_test], y[idx_test]
    
    # Preprocessing (same as in loop)
    state = fit_input_transform(X_train_raw, "log1p+standardize")
    X_train_pp = apply_input_transform(X_train_raw, state)
    X_val_pp   = apply_input_transform(X_val_raw, state)
    X_test_pp  = apply_input_transform(X_test_raw, state)
    
    saved = {
        "X_train_pp": X_train_pp, "y_train": y_train,
        "X_val_pp": X_val_pp,     "y_val": y_val,
        "X_test_pp": X_test_pp,   "y_test": y_test,
        "state": state, "idx_train": idx_train, "idx_val": idx_val, "idx_test": idx_test,
    }
    with open(SAVE_DIR / f"data_{safe_name}.pkl", "wb") as f:
        pickle.dump(saved, f)
    print(f"  Saved preprocessed data: {drug}")

# 2. Save LR results
lr_results_saved = {}
for drug in DRUGS_10:
    if drug in all_results and "LR" in all_results[drug]:
        lr_results_saved[drug] = all_results[drug]["LR"]
with open(SAVE_DIR / "lr_results.pkl", "wb") as f:
    pickle.dump(lr_results_saved, f)
print(f"\\nSaved LR results for {len(lr_results_saved)} drugs")

# 3. Save MLP results from 07-01 (for comparison in 07-02)
mlp_results_saved = {}
for drug in DRUGS_10:
    if drug in all_results and "MLP" in all_results[drug]:
        mlp_results_saved[drug] = all_results[drug]["MLP"]
with open(SAVE_DIR / "mlp_results.pkl", "wb") as f:
    pickle.dump(mlp_results_saved, f)
print(f"Saved MLP results for {len(mlp_results_saved)} drugs")

print("\\nReady for 07-02.")
