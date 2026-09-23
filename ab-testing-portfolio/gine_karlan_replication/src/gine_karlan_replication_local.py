"""
Gine & Karlan (Bulak)

USAGE
-----
1. Put the raw Harvard Dataverse .dta files in a folder, e.g.:
     ./data/bulak_t1a_b.dta
     ./data/bulak_t1b.dta
     ./data/bulak_figure3.dta
     ... (and the rest listed in REQUIRED_FILES below)

2. Install dependencies (see requirements.txt alongside this file):
     pip install -r requirements.txt

3. Run:
     python gine_karlan_replication_local.py --data-dir ./data --out-dir ./outputs

   If you omit --data-dir, it defaults to ./data next to this script.
   If you omit --out-dir, it defaults to ./outputs next to this script.
"""

from pathlib import Path
import argparse
import sys
import warnings
import json
import numpy as np
import pandas as pd
import statsmodels.api as sm

SEED = 20260901
N_PERM = 10_000

# Only these two files are actually read by the analysis (see build_bridge /
# prepare_analysis / balance_check below). The rest of the archive isn't
# touched, so we only hard-require these.
REQUIRED_FILES = ['bulak_t1a_b.dta', 'bulak_figure3.dta', 'bulak_t1b.dta']


def read_stata(path):
    """Read Stata files robustly, retaining numeric codes and handling legacy encodings."""
    with warnings.catch_warnings():
        warnings.simplefilter('ignore', UnicodeWarning)
        try:
            return pd.read_stata(path, convert_categoricals=False)
        except UnicodeDecodeError:
            return pd.read_stata(path, encoding='latin-1', convert_categoricals=False)


def load_all(data_dir: Path, out_dir: Path):
    dta_files = sorted(data_dir.glob('*.dta'))
    if not dta_files:
        sys.exit(
            f"No .dta files found in {data_dir}.\n"
            f"Point --data-dir at the folder containing the Harvard Dataverse "
            f"files, at minimum: {', '.join(REQUIRED_FILES)}"
        )

    missing = [f for f in REQUIRED_FILES if not (data_dir / f).exists()]
    if missing:
        sys.exit(
            f"Missing required file(s) in {data_dir}: {', '.join(missing)}\n"
            f"Found instead: {', '.join(p.name for p in dta_files)}"
        )

    inventory = []
    data = {}
    for path in dta_files:
        df = read_stata(path)
        data[path.stem] = df
        inventory.append({'file': path.name, 'rows': len(df), 'columns': len(df.columns), 'column_list': list(df.columns)})
        print(f'{path.name}: shape={df.shape}')
        print('  columns=', list(df.columns))
    pd.DataFrame([{k: v for k, v in x.items() if k != 'column_list'} for x in inventory]).to_csv(out_dir / 'file_inventory.csv', index=False)
    (out_dir / 'file_inventory_columns.json').write_text(json.dumps(inventory, indent=2, default=str))
    return data


def build_bridge(data, out_dir: Path):
    fig = data['bulak_figure3'].copy()
    loan = data['bulak_t1a_b'].copy()
    pair = fig[['center', 'cntid']].drop_duplicates()
    print(f'figure3 unique center-cntid pairs={len(pair)}; unique centers={pair.center.nunique()}; unique cntid={pair.cntid.nunique()}')
    center_multiplicity = pair.groupby('center').cntid.nunique()
    print('center->cntid multiplicity:', center_multiplicity.value_counts().sort_index().to_dict())
    # The supplied archive does not contain a direct grpname=center key: center is numeric in figure3,
    # whereas grpname is a string in t1a_b. Perform and record the literal requested merge diagnostic.
    fig_key = fig.assign(center_key=fig['center'].astype(str).str.strip())[['center_key', 'cntid']].drop_duplicates()
    loan_key = loan.assign(center_key=loan['grpname'].astype(str).str.strip())
    literal = loan_key.merge(fig_key, on='center_key', how='left', indicator=True)
    print('literal grpname=center merge:', literal['_merge'].value_counts(dropna=False).to_dict())
    pd.DataFrame({
        'metric': ['figure3_pair_rows', 'figure3_unique_centers', 'figure3_unique_cntid', 'literal_merge_rows', 'literal_merge_orphans'],
        'value': [len(pair), fig.center.nunique(), fig.cntid.nunique(), len(literal), int((literal._merge == 'left_only').sum())]
    }).to_csv(out_dir / 'bridge_quality.csv', index=False)
    return pair, literal


def prepare_analysis(data, out_dir: Path):
    loan = data['bulak_t1a_b'].copy()
    d = loan.loc[(loan['old'] == 1) & (loan['cycle'] == 1)].copy()
    d['treat'] = pd.to_numeric(d['treat'], errors='coerce')
    d['dummypastdue30d'] = pd.to_numeric(d['dummypastdue30d'], errors='coerce')
    d['prop_misswk_cycle_d'] = pd.to_numeric(d['prop_misswk_cycle_d'], errors='coerce')
    d = d.loc[d.treat.isin([0, 1])].copy()
    # Archive-compatible cluster fallback. grpname is the only repeated key in t1a_b itself;
    # retain only groups with a single treatment status so permutation labels are well-defined.
    d['grpname_clean'] = d['grpname'].astype(str).str.strip()
    d['cluster_treat_nunique'] = d.groupby('grpname_clean')['treat'].transform('nunique')
    d['cluster_id'] = d['grpname_clean'].where(d['cluster_treat_nunique'] == 1)
    d['cluster_assignment_valid'] = d['cluster_id'].notna()
    d.to_csv(out_dir / 'analysis_dataset.csv', index=False)
    print('filtered rows:', len(d), 'valid complete-treatment clusters:', d.loc[d.cluster_assignment_valid, 'cluster_id'].nunique())
    print('rows with missing outcomes:', d[['dummypastdue30d', 'prop_misswk_cycle_d']].isna().sum().to_dict())
    return d


def balance_check(data, d, out_dir: Path):
    base = data['bulak_t1b'].copy()
    # cid is not present in t1a_b, so a lossless baseline merge cannot be performed.
    out = pd.DataFrame([{'variable': 'baseline_merge', 'n_t1b_cid_nonmissing': int(base.cid.notna().sum()), 'status': 'not estimable: cid absent from t1a_b'}])
    out.to_csv(out_dir / 'balance_table.csv', index=False)
    print('Balance check:', out.to_dict('records'))
    return out


def ols_cluster(d, outcome):
    x = d[[outcome, 'treat', 'grpname_clean']].dropna().copy()
    model = sm.OLS(x[outcome], sm.add_constant(x['treat'])).fit(cov_type='cluster', cov_kwds={'groups': x['grpname_clean']})
    return {'outcome': outcome, 'n': len(x), 'clusters': x.grpname_clean.nunique(), 'control_mean': x.loc[x.treat == 0, outcome].mean(), 'treatment_mean': x.loc[x.treat == 1, outcome].mean(), 'ate': model.params['treat'], 'se_cluster': model.bse['treat'], 'p_cluster': model.pvalues['treat']}


def permutation_pvalue(d, outcome, n_perm=N_PERM, seed=SEED):
    x = d.loc[d.cluster_assignment_valid, [outcome, 'treat', 'cluster_id']].dropna().copy()
    observed = x.loc[x.treat == 1, outcome].mean() - x.loc[x.treat == 0, outcome].mean()
    cluster = x[['cluster_id', 'treat']].drop_duplicates().sort_values('cluster_id')
    labels = cluster.treat.to_numpy().astype(int)
    n_treat = int(labels.sum())
    rng = np.random.default_rng(seed)
    by_cluster = x.groupby('cluster_id')[outcome].agg(['sum', 'count'])
    vals = by_cluster.index.to_numpy()
    sums = by_cluster['sum'].to_numpy()
    counts = by_cluster['count'].to_numpy()
    stats = np.empty(n_perm)
    for i in range(n_perm):
        assign = np.zeros(len(vals), dtype=bool)
        assign[rng.choice(len(vals), size=n_treat, replace=False)] = True
        tm = sums[assign].sum() / counts[assign].sum()
        cm = sums[~assign].sum() / counts[~assign].sum()
        stats[i] = tm - cm
    p = (np.sum(np.abs(stats) >= abs(observed)) + 1) / (n_perm + 1)
    return observed, p


def estimate(d, out_dir: Path):
    rows = []
    for outcome in ['dummypastdue30d', 'prop_misswk_cycle_d']:
        r = ols_cluster(d, outcome)
        r['permutation_p'] = permutation_pvalue(d, outcome)[1]
        rows.append(r)
    res = pd.DataFrame(rows)
    res.to_csv(out_dir / 'results.csv', index=False)
    print(res.to_string(index=False))
    sample = d.loc[d.cluster_assignment_valid].groupby('treat').agg(rows=('treat', 'size'), clusters=('cluster_id', 'nunique')).reset_index()
    sample.to_csv(out_dir / 'sample_sizes.csv', index=False)
    means = d.loc[d.cluster_assignment_valid].groupby('treat')[['dummypastdue30d', 'prop_misswk_cycle_d']].mean().reset_index()
    means.to_csv(out_dir / 'outcome_means.csv', index=False)
    return res


def parse_args():
    script_dir = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--data-dir', type=Path, default=script_dir / 'data',
                         help='Folder containing the raw .dta files (default: ./data next to this script)')
    parser.add_argument('--out-dir', type=Path, default=script_dir / 'outputs',
                         help='Folder to write output CSVs/JSON into (default: ./outputs next to this script)')
    return parser.parse_args()


def main():
    args = parse_args()
    data_dir = args.data_dir.resolve()
    out_dir = args.out_dir.resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    data = load_all(data_dir, out_dir)
    build_bridge(data, out_dir)
    d = prepare_analysis(data, out_dir)
    balance_check(data, d, out_dir)
    results = estimate(d, out_dir)
    print('\nNOTE: Because the supplied archive lacks a direct grpname=center key and t1a_b has no cntid, reported inference uses only t1a_b grpname clusters with constant treatment. This is a transparent archive-compatible fallback, not a literal center-level cntid replication.')
    return results


if __name__ == '__main__':
    main()
