# 06-03d Phase-1 site-mask diagnostic

Outputs of `06-03d-Phase1-SiteMask-Diagnostic.ipynb` (Sep 2026):
`site_mask_drop_vs_k.csv` / `.pdf` — how species-classification accuracy
degrades as the top-k species bins are masked. Documents that zeroing the top
500 bins removes almost no species signal (the "masking-drop" is +0.0127,
down to +0.002 with higher `max_features`).

Feeds the docs page `06b/mask-diagnostic` and report §5.8. Archive:
`../06-03d-Phase1-SiteMask-Diagnostic.zip`.
