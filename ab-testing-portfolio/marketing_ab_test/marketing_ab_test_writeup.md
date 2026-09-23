# Should We Keep Advertising? — A/B Test Findings

**Prepared for:** Decision makers evaluating ad spend effectiveness
**Data:** 588,101 users, randomly shown either an ad or a neutral placeholder (PSA)
**Bottom line:** The ad increased purchases. The evidence for this is very strong. Whether it's
*worth the spend* depends on cost numbers this dataset doesn't contain — see "What We Still Need
to Know" below.

---

## Recommendation

**Keep showing the ad, conditional on confirming actual cost-per-impression and profit-per-sale
figures with Finance.** The measured effect is large enough that it would need to be paired with
an unusually high ad cost or unusually low profit margin to *not* be worth it — but we cannot
confirm that without real numbers, which this dataset does not include.

---

## What We Found

Users who saw the ad converted (made a purchase) at **2.55%**. Users who saw the neutral PSA
converted at **1.79%**. That's a **0.77 percentage point increase** — or put differently, users
shown the ad were **about 43% more likely** to convert than users who weren't.

| | Saw the Ad | Saw the PSA |
|---|---|---|
| Users | 564,577 | 23,524 |
| Conversion rate | 2.55% | 1.79% |
| **Difference** | **+0.77 percentage points (+43% relative)** | |

## How Confident Are We This Is Real, and Not Luck?

Very confident. We ran two independent statistical checks — a standard test and a second,
belt-and-suspenders method that doesn't rely on the same assumptions as the first. Both came back
with the same verdict: if the ad genuinely made no difference, a result this large would show up
by pure chance roughly **once in several trillion tries.** That is about as close to certain as
statistics gets.

We also calculated a likely range for the true effect, not just a single number: we're 95%
confident the real lift is somewhere between **0.6 and 0.9 percentage points**. Even the low end
of that range is a meaningful increase.

## Data Quality — Can We Trust the Test Itself?

Before trusting any result, we checked whether the experiment itself was run cleanly:

- **Was the split between groups fair?** Yes. The way users landed in each group matched what
  we'd expect from a properly randomized test — no sign of a broken or biased split.
- **Were the two groups otherwise similar?** The one other behavior we could measure (how many
  ads a user was generally exposed to) was nearly identical between groups, which is a good sign
  the two groups were comparable going in.

No red flags found in either check.

## What We Still Need to Know

This dataset tells us the ad changes *behavior*. It does not tell us whether that behavior change
is *profitable*, because it contains no information on:

- What it actually costs to show one ad
- The actual profit made per converted sale
- Whether results would hold up at a larger scale, or fade over a longer time period

**Any dollar-figure recommendation attached to this test should be treated as illustrative until
Finance confirms real cost and margin numbers.** As a rough illustration only: if an ad costs a
couple of cents to show and a converted sale is worth several dollars in profit, this result
clears that bar several times over — but that is an example calculation, not a verified one.

## Recommended Next Step

Before scaling this up further:
1. Confirm actual cost-per-impression and profit-per-conversion with Finance.
2. If possible, re-check whether this same lift holds for users seen more recently, since this
   snapshot doesn't tell us if the effect is stable over time.

---

## Appendix — For the Technically Curious

- **Method:** Two-proportion z-test (p ≈ 1.7×10⁻¹³) cross-checked with a 10,000-iteration
  permutation test (p ≈ 9.999×10⁻⁵ — the smallest value that many iterations can report; the true
  value is almost certainly smaller). Both methods agree.
- **Sample size adequacy:** with 588,101 users split unevenly (96% ad / 4% PSA), this test could
  reliably detect a true effect as small as ~0.25 percentage points. The observed 0.77pp effect
  is roughly 3x that floor.
- **Sample Ratio Mismatch check:** chi-square goodness-of-fit against an assumed 96/4 intended
  split, chi2 ≈ 7.08×10⁻⁸, p ≈ 0.9998 — no evidence of misallocation.
- **Covariate balance check:** `total ads` exposure nearly identical across groups (mean 24.82 vs
  24.76); a statistically significant Mann-Whitney result (p ≈ 4.69×10⁻¹¹) is attributable to the
  very large sample size rather than a meaningful practical difference.
- **Full technical notebook and code:** see `marketing_ab_test/notebooks/marketing_ab_test_analysis.ipynb`
  in the accompanying repository.
