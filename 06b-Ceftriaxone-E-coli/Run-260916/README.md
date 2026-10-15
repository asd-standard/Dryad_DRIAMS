# Run-260916 — intermediate 06-03c re-run (Sep 2026)

Re-run of the `06-03c` pipeline on 2026-09-16/17, after adding two-tier S/R
downsampling (`c631264`) and extending the MLP grid (lr ≤ 5e-4, dropout ≤ 0.8;
`5ad5485`) — but still 30 rounds, μ=0.1 and the pre-fix FedProx proximal term.
Not cited in the docs.

Pooled BalAcc: Centralized MLP 0.763; FedAvg 0.715 (r30); FedProx μ=0.1 0.550
(r27); FedLR 0.739 (r28); FedRF 0.500; cross-site MLP 0.592. Best params:
MLP lr=5e-4 and dropout=0.8 (both at the top of the extended grid); RF depth 20.

Superseded as a reference by the final-protocol re-run once it happens
(current notebooks: 50 rounds, μ ∈ {0.5, 1.0}, squared penalty, tuned RF
threshold). Archive: `01-Run-20260917T145548Z-1-001.zip`.
