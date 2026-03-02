# Checkpoint 2 Responses

## Prompt 1: For step 4, what are two hypotheses you have tested, and what were the results?

### Hypothesis Test 1: First dragon impact in close games
- **Null (H0):** In close games (|gold diff at 15| <= 1000), first-dragon and non-first-dragon teams have equal win rates.
- **Alternative (HA):** In close games, first-dragon teams have higher win rates.
- **Test statistic:** Difference in win rates: WinRate(first dragon) - WinRate(no first dragon) in close games.
- **Observed result:** 13.16 percentage points (56.58% - 43.42%).
- **Method:** Permutation test with 10,000 shuffles.
- **p-value:** < 0.0001 (empirical p rounded to 0 with 10,000 permutations).
- **Conclusion:** Reject H0; evidence suggests first dragon provides a measurable advantage even after controlling for close gold states.

### Hypothesis Test 2: Early gold-gap size vs game length
- **Null (H0):** Mean game length is the same for small-gap and large-gap games at 15 minutes.
- **Alternative (HA):** Small-gap games last longer than large-gap games.
- **Groups:**
  - Small gap: bottom quartile of |gold diff at 15| (<= 922)
  - Large gap: top quartile of |gold diff at 15| (>= 3458)
- **Test statistic:** Mean game length (small-gap) - mean game length (large-gap).
- **Observed result:** 5.34 minutes.
- **Method:** Permutation test with 10,000 shuffles.
- **p-value:** < 0.0001.
- **Conclusion:** Reject H0; games with close early gold states last significantly longer.

---

## Prompt 2: Briefly explain your baseline model and plans for improving the model.

### Baseline model
- **Task:** Binary classification predicting `result`.
- **Features at minute 15:** `golddiffat15`, `xpdiffat15`, `csdiffat15`, `firstblood`, `firstdragon`, `firsttower`, `side`.
- **Pipeline:**
  - Numeric median imputation
  - One-hot encoding for `side`
  - Logistic Regression (`max_iter=2000`)
- **Train/test split:** 80/20, stratified.
- **Test performance:**
  - Accuracy: **0.7505**
  - F1: **0.7517**
  - Precision: **0.7481**
  - Recall: **0.7552**

### Improvement plan
- Engineer richer features (`abs_golddiffat15`, `early_obj_count`, interaction terms).
- Tune hyperparameters via `GridSearchCV`.
- Compare logistic regression with nonlinear models (e.g., Random Forest / Gradient Boosting).
- Select final model by F1, then verify precision/recall trade-offs and stability.

---

## Prompt 3: Working GitHub page URL
Expected URL after enabling Pages from `main` branch:

**https://harsh5559.github.io/259_FINAL/**

(If it does not load yet, enable GitHub Pages in repository Settings -> Pages -> Source: Deploy from branch, Branch: `main`, folder: `/ (root)`.)
