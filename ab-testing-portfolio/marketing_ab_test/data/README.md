# Data

The raw dataset is not included in this repository (not redistributed, and too large for a
typical git repo without LFS).

**Source:** [Marketing A/B Testing — Kaggle](https://www.kaggle.com/datasets/faviovaz/marketing-ab-testing)

1. Download `marketing_AB.csv` from the link above (requires a free Kaggle account).
2. Place it in this `data/` folder so the notebook's relative path
   (`../data/marketing_AB.csv`) resolves correctly.

**Expected shape:** 588,101 rows × 7 columns (`Unnamed: 0`, `user id`, `test group`, `converted`,
`total ads`, `most ads day`, `most ads hour`).
