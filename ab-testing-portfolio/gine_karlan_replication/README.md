# Gine & Karlan (Bulak) Replication — Group vs. Individual Liability Microfinance RCT

A partial, archive-constrained replication of Gine & Karlan's "Group versus Individual Liability"
field experiment, analyzing whether switching borrowers from group-liability to
individual-liability lending changed repayment behavior.

## Purpose

This project is a test randomized at 
the **center** level (a center = several borrower groups meeting together) so valid inference
here requires cluster-robust standard errors and cluster-level permutation, not the simpler
row-level methods used in the marketing project.

## The central data limitation — stated upfront, not buried

**The publicly released archive does not contain a direct key linking the client-level `grpname`
field in the loan data to the true center-level randomization unit.** This is documented with an
actual diagnostic (see notebook Step 1), not assumed: a literal merge attempt between `grpname`
and `center` produces **zero matches out of 26,234 rows**. Separately, `center` alone maps to
multiple `cntid` values (163 `cntid` across only 44 centers), so even a working bridge wouldn't
uniquely identify the randomization unit.

**Fallback used, and why it's valid:** since the true cluster can't be recovered, the analysis
falls back to `grpname` — the only repeated key actually present in the loan-level file — but
only keeps `grpname` groups where treatment status is constant across all members
(`cluster_treat_nunique == 1`). Mixed groups are excluded from cluster-robust and permutation
inference, since both methods require treatment to be constant within a cluster to produce valid
results. This is a transparent, documented compromise — **the results below are a
same-direction diagnostic on a degraded cluster definition, not a literal reproduction of the
paper's own center-level estimate**, and are reported as such throughout.

## Key findings

| Outcome | Control mean | Treatment mean | ATE | Cluster-robust p | Permutation p |
|---|---|---|---|---|---|
| 30-day delinquency (`dummypastdue30d`) | 0.0004 | 0.0000 | -0.0004 | 0.314 | 1.000 |
| Missed weekly payments (`prop_misswk_cycle_d`) | 0.0466 | 0.0690 | +0.0224 | 0.0020 | 0.0125 |

- **30-day delinquency:** no detectable effect — the outcome is near-zero for both groups in this
  filtered sample, so this reads as a floor effect rather than a meaningful null result.
- **Missed weekly payments:** individual-liability clients missed noticeably more scheduled
  payments than group-liability clients in this fallback-cluster sample. Both the parametric
  (cluster-robust regression) and non-parametric (cluster-level permutation) methods agree the
  difference is unlikely to be chance — subject to the cluster-definition caveat above.
- **Baseline balance check:** not estimable from this archive — `t1b` links to loan records via
  `cid`, which is absent from `t1a_b`. Reported honestly as a limitation rather than skipped
  silently.

## Repository structure

```
gine_karlan_replication/
├── README.md
├── requirements.txt
├── notebooks/
│   └── gine_karlan_replication.ipynb
├── src/
│   └── gine_karlan_replication_local.py   (CLI-runnable version, configurable --data-dir/--out-dir)
├── data/
│   └── README.md                          
└── outputs/
    ├── bridge_quality.csv                 (grpname=center merge diagnostic)
    ├── analysis_dataset.csv               (filtered, cluster-labeled analysis sample)
    ├── balance_table.csv                  (baseline balance — not estimable, documented)
    ├── results.csv                        (main ATE, SEs, p-values for both outcomes)
    ├── sample_sizes.csv
    ├── outcome_means.csv
    └── file_inventory_columns.json        (schema of all Bulak files inspected)
```

All files in `outputs/` were produced by an actual execution of this pipeline against the real
dataset — none are placeholders.

## How to run

```bash
pip install -r requirements.txt
```

- Open and run `notebooks/gine_karlan_replication.ipynb`, or
- Run from the command line:
  ```bash
  python src/gine_karlan_replication_local.py --data-dir ./data --out-dir ./outputs
  ```

## Data source

Gine, X. and Karlan, D. — "Group versus Individual Liability" replication data (Bulak),
Harvard Dataverse.