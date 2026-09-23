# Marketing A/B Test: Ad vs. PSA — Conversion Analysis

A retrospective A/B testing project analyzing a real marketing experiment (Kaggle "Marketing A/B
Testing" dataset — 588,101 users), evaluating whether showing users an ad increased purchase
conversion relative to a neutral public service announcement (PSA) control.

## Purpose

This project is a deliberate structural contrast to a companion project analyzing the Giné &
Karlan (Bulak) microfinance RCT. That dataset required **cluster-robust** standard errors and
**cluster-level** permutation, because treatment was randomized at the center level, not the
individual level. This dataset randomizes at the **individual user level**, so the same core
A/B testing workflow can be practiced without clustering — isolating and confirming which parts
of a cluster-robust analysis pipeline are genuinely specific to clustered designs.

The analysis is organized around a 7-step A/B testing framework (problem statement → success
metric/hypothesis → experiment design → run → validity checks → interpret results → launch
decision), applied to a dataset that was already collected — meaning several steps (duration,
instrumentation setup, live A/A testing) cannot be executed the way they would in a prospective,
newly-designed experiment. Each step in the notebook states explicitly whether it was run on real
data, computed from real data with a stated assumption, or could only be addressed conceptually.

## Key findings

- **Sample Ratio Mismatch check:** clean. Observed group split (564,577 ad / 23,524 psa) matches
  the assumed intended 96/4 ratio (chi2 ≈ 7.08e-08, p ≈ 0.9998) — no evidence of broken
  randomization.
- **Primary result:** conversion rate is 2.55% (ad) vs. 1.79% (psa) — an absolute lift of 0.77
  percentage points (~43% relative lift). Two-proportion z-test: p ≈ 1.7×10⁻¹³. Permutation test
  (individual-level shuffle, 10,000 iterations, corrected code): p ≈ 9.999×10⁻⁵ — hitting the
  floor resolvable by 10,000 permutations, consistent with the z-test's far smaller p-value; both
  methods agree the result is not attributable to chance. 95% CI on the lift: approximately
  (0.59pp, 0.94pp).
- **Achieved Minimum Detectable Effect (MDE):** given the actual sample sizes, this design could
  reliably detect a true gap as small as ~0.25 percentage points — the observed 0.77pp lift is
  well above that floor.
- **Covariate balance check (`total ads`):** means and medians are nearly identical between
  groups (24.82 vs 24.76; median 13 vs 12), but a Mann-Whitney test flags this as statistically
  significant (p ≈ 4.69×10⁻¹¹) purely due to the very large sample size — a "statistically
  significant but practically negligible" result, and a direct illustration of why statistical
  and practical significance are evaluated as two separate criteria in this framework, not one.

## Known limitations / what could not be verified from this dataset

- **δ (practical significance threshold)** could not be derived from the data — this dataset has
  no revenue or ad-cost fields. The illustrative $0.02/impression and $15/conversion figures used
  in the notebook are stated assumptions, not real business inputs, and should not be quoted as
  findings.
- **Duration, live A/A testing, Instrumentation Effect, External Factors, and Novelty Effect**
  checks could not be run — the dataset has no date field, no guardrail/performance metrics, and
  no new-vs-returning visitor flag.
- **`total ads`** initially looked like a plausible per-user cost driver for the launch decision,
  but its near-identical distribution across both groups suggests it more likely reflects
  general site-wide ad exposure rather than an outcome caused by this specific test — it was
  ruled out as a cost signal after checking it directly, rather than assumed to work.
- **Permutation test bug, found and corrected.** An earlier draft allocated a results array
  (`stats = np.empty(n_perm)`) but never wrote into it inside the loop, so the originally printed
  p-value was computed from uninitialized memory, not the actual 10,000 shuffles. The bug is
  fixed and the notebook's result (p ≈ 9.999×10⁻⁵) has been re-run and verified against the live
  dataset — see the notebook's Step 6 section for the corrected code.

## Repository structure

```
marketing_ab_test/
├── README.md
├── requirements.txt
├── notebooks/
│   └── marketing_ab_test_analysis.ipynb
├── data/
│   └── README.md          (download instructions — raw CSV not included)
└── outputs/
    ├── srm_results.csv
    ├── hypothesis_test_results.csv
    └── covariate_balance_results.csv
```

## How to run

```bash
pip install -r requirements.txt
```

Download `marketing_AB.csv` from Kaggle (see `data/README.md`) and place it in `data/`, then open
`notebooks/marketing_ab_test_analysis.ipynb`.

## Data source

[Marketing A/B Testing — Kaggle](https://www.kaggle.com/datasets/faviovaz/marketing-ab-testing)
(faviovaz). Not redistributed in this repository; see `data/README.md` for download instructions.
