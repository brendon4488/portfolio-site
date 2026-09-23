# A/B Testing Portfolio

Applied A/B testing projects, each built around a real dataset and a real structural constraint,
walked through end-to-end: problem statement, hypothesis design, validity checks, statistical
inference, and an honest account of what the data could and couldn't answer.

## Projects

### [`gine_karlan_replication/`](./gine_karlan_replication)
Partial replication of Gine & Karlan's "Group versus Individual Liability" microfinance RCT
(Bulak, Philippines). Treatment randomized at the **center** level — requires cluster-robust
standard errors and cluster-level permutation. Documents a real data limitation in the released
archive (no direct key linking client records to the true randomization unit) with an actual
diagnostic, rather than assuming it away.

### [`marketing_ab_test/`](./marketing_ab_test)
Analysis of a real marketing experiment (ad vs. PSA, 588k users). Treatment randomized at the
**individual** level — a deliberate structural contrast to the microfinance project, isolating
which parts of a cluster-robust pipeline are specific to clustered designs versus general to any
A/B test. Includes a decision-maker-facing write-up alongside the technical notebook.

## What's consistent across every project here

- Every claim in `results.csv` / `outputs/` is either verified against a real, executed run, or
  explicitly labeled as an illustrative assumption — never presented ambiguously as one or the
  other.
- Data limitations (missing crosswalks, unavailable fields, structural constraints) are documented
  with the diagnostic that revealed them, not glossed over.
- Each project's own README covers setup, methodology, and findings in full; this page is just
  the index.
