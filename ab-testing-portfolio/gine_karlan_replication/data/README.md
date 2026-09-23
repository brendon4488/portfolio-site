# Data

**Source:** Giné, X. and Karlan, D., "Group versus Individual Liability" replication data,
Harvard Dataverse (Bulak dataset).

Place the following files in this `data/` folder before running the notebook or script:
- `bulak_t1a_b.dta` (loan-level panel, ~26,234 rows)
- `bulak_figure3.dta` (center/cntid lookup, ~1,139 rows)
- `bulak_t1b.dta` (baseline survey, ~43,747 rows)

The notebook and `src/gine_karlan_replication_local.py` both check for these files on startup
and will raise a clear error naming exactly what's missing if the folder isn't set up correctly.
