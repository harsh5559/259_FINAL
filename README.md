# Snowball or Comeback? How Early Objectives Shape Professional League of Legends

**DSC 259R Final Project - League of Legends (Oracle's Elixir, 2022)**

## Checkpoint 1 Responses

### 1) Which dataset did you choose? Why?
We chose the **League of Legends** dataset (2022 Oracle's Elixir). It contains 12,415 professional matches across 55 regions and includes rich early-game features (gold/XP/CS differentials and objective control), making it a strong fit for both hypothesis testing and predictive modeling.

### 2) Plotly visualization from Step 2
We created a Plotly bar chart showing **win rate by number of early objectives secured** (first blood, first dragon, first tower):

- 0 objectives: 24.1%
- 1 objective: 41.9%
- 2 objectives: 61.1%
- 3 objectives: 79.9%

<iframe
  src="assets/objective_stacking.html"
  width="900"
  height="550"
  frameborder="0"
></iframe>

### 3) Planned hypotheses for Step 4 and test statistic
- **Null (H0):** In close games (|gold diff at 15| <= 1000), first-dragon teams and non-first-dragon teams have equal win rates.
- **Alternative (HA):** In close games, first-dragon teams have a higher win rate.
- **Test statistic:** Difference in win rates: WinRate(first dragon) - WinRate(no first dragon), within the close-game subset.

### 4) Planned prediction problem (Steps 5-8)
- **Response column:** `result`
- **Problem type:** Binary classification

---

## Checkpoint 2 Responses

### 1) For Step 4, what are two hypotheses tested, and what were the results?

#### Hypothesis Test 1: First dragon impact in close games
- **H0:** In close games (|gold diff at 15| <= 1000), first-dragon and non-first-dragon teams have equal win rates.
- **HA:** First-dragon teams have higher win rates in close games.
- **Observed statistic:** 13.16 percentage points (56.58% - 43.42%).
- **Method:** Permutation test, 10,000 shuffles.
- **Result:** p-value < 0.0001 (empirical p rounded to 0 in 10,000 permutations). Reject H0.

#### Hypothesis Test 2: Early gold-gap size vs game length
- **H0:** Mean game length is the same for small-gap and large-gap games at 15 minutes.
- **HA:** Small-gap games last longer than large-gap games.
- **Groups:** Small gap = bottom quartile (|gold diff at 15| <= 922), Large gap = top quartile (|gold diff at 15| >= 3458).
- **Observed statistic:** 5.34 minutes (small-gap minus large-gap average game length).
- **Method:** Permutation test, 10,000 shuffles.
- **Result:** p-value < 0.0001. Reject H0.

### 2) Baseline model + plans for improvement

#### Baseline model
- **Model:** Logistic Regression in a single sklearn `Pipeline`.
- **Features:** `golddiffat15`, `xpdiffat15`, `csdiffat15`, `firstblood`, `firstdragon`, `firsttower`, `side`.
- **Preprocessing:** median imputation for numeric, one-hot encoding for `side`, imputation for binary objective flags.
- **Split:** 80/20 train-test with stratification.
- **Performance (test):**
  - Accuracy: **0.7505**
  - F1: **0.7517**
  - Precision: **0.7481**
  - Recall: **0.7552**

#### Improvement plan
- Engineer new features (`abs_golddiffat15`, `early_obj_count`, interaction terms).
- Tune hyperparameters with `GridSearchCV` (e.g., `C`, regularization, class weights; and tree-model depth/estimators for nonlinear alternatives).
- Compare logistic regression with nonlinear models and select final model by F1 + precision/recall tradeoff.

---

## Project Title
**Snowball or Comeback? How Early Objectives Shape Professional League of Legends**
