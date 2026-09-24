# Brendon Makurumure — Data Science Portfolio

BSc Honours in Data Science and Systems, University of Zimbabwe (2026).
Based in Harare, Zimbabwe.

I build end-to-end data pipelines, statistical experiments, and 
analytical tools — with a focus on doing the work rigorously and 
communicating what the data can and cannot claim.

---

## Projects

### 1. MFI SQL Business Intelligence Report
**SQL · Risk Analytics · Microfinance**

A 29-query SQL risk reporting suite over a real microfinance loan 
portfolio. Covers Portfolio at Risk (PAR30), default rate, principal 
reduction, and branch-level segmentation via multi-source joins.

The analysis surfaced a data quality anomaly — outstanding balances 
exceeding funded amounts for a subset of agricultural loans. Rather 
than excluding or smoothing the affected rows, I documented the 
anomaly transparently in the README and disclosed its potential 
effect on PAR calculations.

→ [Repository link]

---

### 2. A/B Testing Portfolio
**Python · Statistical Inference · Experimentation**

Two separate experiments covering different randomization designs 
and real data challenges.

**Marketing A/B Test (Kaggle — 588,101 users)**
Individual-level randomization. Methods: two-proportion z-test 
with permutation test cross-validation, Sample Ratio Mismatch (SRM) 
check, Minimum Detectable Effect analysis (retrospective and 
prospective), and covariate balance check via Mann-Whitney.

Caught and corrected a real permutation-loop bug mid-project. 
The corrected result is documented alongside the original error — 
because how you handle mistakes matters as much as whether you 
catch them.

**Giné & Karlan Bulak Microfinance RCT Replication (Harvard Dataverse)**
Cluster-randomized design. Replicated a published academic 
randomized controlled trial using raw `.dta` files. Diagnosed 
a complete bridge-merge failure producing 26,234 orphaned 
observations, built a documented fallback cluster definition, 
and implemented cluster-robust OLS with a cluster-level 
permutation test.

→ [Repository link]

---

### 3. WikiPulse — Live Edit Stream Consumer
**Python · MySQL · Streamlit · Real-time Data Engineering**

A real-time data pipeline connecting to Wikimedia's public SSE 
`recentchange` stream. Parses and stores live edit events — 
including raw JSON as a safety net — into MySQL using batched 
dual-trigger writes (event threshold OR time threshold), a 
pattern that deliberately mirrors Kafka's `batch.size` / `linger.ms` 
at production scale.

Extended into a live Streamlit dashboard showing geographic and 
language breakdown of edits in real time, built for a portfolio 
viewer doing a 30-second skim.

Design decisions are documented: 60-second tumbling windows, 
WAL mode for concurrent pipeline access, dual-output logging 
for unattended soak testing.

→ [Repository link]

---

## What I'm working on now

Regression and ML skill progression: Ames Housing → Medical Cost 
→ NYC Taxi Trip Duration → Bike Sharing Demand. Each dataset is 
chosen for what it teaches technically, not for sector fit.

The Ames Housing regression reached validation R² 0.9026 / 
RMSE $23,328 using a two-tier Ridge model with CV-tuned 
regularization and a luxury-tier correction above $375k.

---

## Links

GitHub: github.com/brendon4488/ab-testing-portfolio  
LinkedIn: linkedin.com/in/brendon-makurumure-a2469026b
