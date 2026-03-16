# Snowball or Comeback? How Early Objectives Shape Professional League of Legends

**Name(s)**: Harsh

**DSC 259R Final Project — League of Legends (Oracle's Elixir, 2022)**

---

## Introduction

In professional League of Legends, the first 15 minutes of a match are often called the "laning phase" — a critical window where teams jockey for gold, experience, and map objectives. Analysts and players constantly debate whether early objectives like *first dragon* are truly game-changing or merely symptoms of a team that is already ahead. Our project investigates:

> **Do early-game objectives provide a genuine strategic advantage independent of a team's overall gold position, and how reliably can match outcomes be predicted from the first 15 minutes of play?**

We use the **2022 Oracle's Elixir dataset**, which contains **24,830 team-level rows** (two per match) from **12,415 professional matches** across **55 leagues** worldwide. The dataset spans the entire 2022 competitive season (January–December) and includes detailed early-game state data alongside objective flags.

**Relevant columns:**

| Column | Description |
|--------|-------------|
| `result` | Match outcome (1 = win, 0 = loss) |
| `golddiffat15` | Gold lead/deficit at 15 minutes |
| `xpdiffat15` | XP lead/deficit at 15 minutes |
| `csdiffat15` | Creep score lead/deficit at 15 minutes |
| `firstblood` | Whether this team secured first blood (1/0) |
| `firstdragon` | Whether this team claimed the first dragon (1/0) |
| `firsttower` | Whether this team destroyed the first tower (1/0) |
| `gamelength` | Total game duration in seconds |
| `side` | Blue or Red side |
| `league` | Tournament/region (e.g. LCK, LPL, LEC) |

---

## Data Cleaning and Exploratory Data Analysis

### Data Cleaning

We performed the following cleaning steps on the raw dataset:

1. **Filtered to team-level rows**: The raw dataset contains 148,980 rows (12 per game: 10 player rows + 2 team summary rows). We kept only the `position == 'team'` rows (24,830 rows), since our analysis focuses on team-level outcomes and aggregate early-game statistics.

2. **Parsed dates**: Converted the `date` column from strings to proper datetime objects.

3. **Created readable game length**: Converted `gamelength` from seconds to minutes (`gamelength_min = gamelength / 60`).

4. **Assessed missingness in 15-minute columns**: The columns `golddiffat15`, `xpdiffat15`, and `csdiffat15` are missing for 15.2% of team rows — these correspond to games that ended before the 15-minute mark. We created a clean subset `teams_15` (21,044 rows) with complete 15-minute data for modeling.

5. **Engineered early objective count**: Created `early_obj_count` as the sum of `firstblood`, `firstdragon`, and `firsttower` (range 0–3), capturing how many early objectives each team secured.

**Head of the cleaned DataFrame:**

| gameid                | league   | side   |   result |   gamelength_min |   golddiffat15 |   firstblood |   firstdragon |   firsttower |
|:----------------------|:---------|:-------|---------:|-----------------:|---------------:|-------------:|--------------:|-------------:|
| ESPORTSTMNT01_2690210 | LCKC     | Blue   |        0 |             28.6 |            107 |            1 |             0 |            1 |
| ESPORTSTMNT01_2690210 | LCKC     | Red    |        1 |             28.6 |           -107 |            0 |             1 |            0 |
| ESPORTSTMNT01_2690219 | LCKC     | Blue   |        0 |             35.2 |          -1763 |            0 |             0 |            0 |
| ESPORTSTMNT01_2690219 | LCKC     | Red    |        1 |             35.2 |           1763 |            1 |             1 |            1 |
| 8401-8401_game_1      | LPL      | Blue   |        1 |             22.8 |            NaN |            0 |             0 |            1 |

### Univariate Analysis

The distribution of professional game lengths is roughly normal with a right skew, centered around 30–32 minutes. Most games last between 25 and 40 minutes, with very few ending before 20 minutes or lasting beyond 45 minutes.

<iframe
  src="assets/gamelength_dist.html"
  width="800"
  height="600"
  frameborder="0"
></iframe>

The gold differential at 15 minutes (`golddiffat15`) follows a roughly symmetric, bell-shaped distribution centered at zero, with most values falling between −3,000 and +3,000 gold. The symmetry is expected — every positive gold lead for one team is a matching deficit for the opponent. The tails extend to ±8,000+, representing rare blowout early games.

### Bivariate Analysis

The box plot below shows that teams with a positive gold differential at 15 minutes are far more likely to win. The median gold differential for winning teams is roughly +1,500 gold, while losing teams sit at approximately −1,500 gold. However, there is significant overlap — many teams with early deficits still win, motivating our investigation into whether specific objectives matter beyond raw gold.

<iframe
  src="assets/golddiff_by_outcome.html"
  width="800"
  height="600"
  frameborder="0"
></iframe>

Win rate also varies by early objective control. The chart below shows that teams securing more early objectives (first blood, first dragon, first tower) win at dramatically higher rates — from 24.1% with zero objectives to 79.9% with all three. This compounding effect suggests that early objectives have a reinforcing strategic impact.

<iframe
  src="assets/objective_stacking.html"
  width="800"
  height="600"
  frameborder="0"
></iframe>

### Interesting Aggregates

The table below shows first dragon's win-rate impact in *close* games (gold differential at 15 min within ±1,000) versus *decisive* games (gold differential > 3,000). Crucially, first dragon still confers a 13.2 percentage-point advantage even in close games, suggesting an independent strategic value rather than simply being a byproduct of an existing gold lead.

| Game Type              | First Dragon     |   Win Rate (%) |   Games |
|:-----------------------|:-----------------|---------------:|--------:|
| Close (\|GD15\| ≤ 1k)    | Got First Dragon |           56.6 |    2849 |
| Close (\|GD15\| ≤ 1k)    | No First Dragon  |           43.4 |    2849 |
| Decisive (\|GD15\| > 3k) | Got First Dragon |           60.3 |    3313 |
| Decisive (\|GD15\| > 3k) | No First Dragon  |           39.7 |    3317 |

---

## Assessment of Missingness

### NMAR Analysis

We believe that `golddiffat15` is **not NMAR**. Its missingness is almost entirely explained by `gamelength` — games that ended before the 15-minute mark simply have no 15-minute statistics to record. Since game duration is observed, this makes the missingness **MAR** (Missing At Random), conditional on game length.

A column that could plausibly be **NMAR** is `url` (the match replay link). Whether a replay URL is recorded might depend on factors intrinsic to the match itself — for instance, replays from games with technical issues or controversial rulings may be less likely to be archived. Since these factors relate to the *content* of the missing data rather than other observed columns, this would constitute NMAR. Obtaining additional data about tournament broadcast and archival policies could explain the missingness and reclassify it as MAR.

### Missingness Dependency

We tested the missingness of `golddiffat15` against two other columns using permutation tests (10,000 permutations, α = 0.05).

**Test 1: Missingness depends on `gamelength` (p < 0.0001)**

Games with missing `golddiffat15` have a mean length of 30.91 minutes, compared to 31.74 minutes for games without missing values. The observed difference of −0.83 minutes is highly significant (p < 0.0001), confirming that shorter games drive the missingness — games ending before 15 minutes cannot produce 15-minute statistics.

<iframe
  src="assets/missingness_gamelength.html"
  width="800"
  height="600"
  frameborder="0"
></iframe>

**Test 2: Missingness does NOT depend on `side` (p = 1.0)**

Blue and Red sides have identical missing rates for `golddiffat15` (15.25% each). The observed difference is 0.0, with a p-value of 1.0. This makes sense: when a game ends before 15 minutes, both teams (Blue and Red) have missing stats, so the missingness cannot depend on side.

<iframe
  src="assets/missingness_side_perm.html"
  width="800"
  height="600"
  frameborder="0"
></iframe>

---

## Hypothesis Testing

We test whether first dragon provides a genuine strategic advantage, independent of overall gold state, using a permutation test.

**Null Hypothesis (H₀):** In close games (absolute gold differential at 15 min ≤ 1,000), teams that secured first dragon win at the same rate as teams that did not. Any observed difference is due to random chance.

**Alternative Hypothesis (H₁):** In close games, teams that secured first dragon win at a significantly higher rate, indicating that first dragon provides a genuine strategic advantage independent of gold state.

**Test Statistic:** Difference in win rates: WinRate(first dragon) − WinRate(no first dragon), among the 5,698 close-game team rows.

**Significance Level:** α = 0.05

**Results:** The observed difference is **13.16 percentage points** (56.58% vs 43.42%). After 10,000 permutations of the `firstdragon` labels within close games, the p-value is **< 0.0001**. We **reject the null hypothesis** — there is strong evidence that first dragon provides a measurable competitive advantage even after controlling for close gold states at 15 minutes.

This is consistent with the game's design: securing first dragon grants permanent stat bonuses (dragon soul stacks) that compound over time, providing a genuine strategic edge beyond the gold value of the objective itself.

<iframe
  src="assets/hypothesis_test_1.html"
  width="800"
  height="600"
  frameborder="0"
></iframe>

---

## Framing a Prediction Problem

We frame a **binary classification** problem: predict whether a team wins (`result = 1`) or loses (`result = 0`) using only information available at the **15-minute mark**.

**Response variable:** `result` (1 = win, 0 = loss)

**Features known at minute 15:** `golddiffat15`, `xpdiffat15`, `csdiffat15`, `firstblood`, `firstdragon`, `firsttower`, and `side`. All of these are observable during a live broadcast at exactly 15 minutes into the game.

**Evaluation metric:** We use **F1-score** as our primary metric. F1 balances precision and recall, which is appropriate here because both types of errors matter: incorrectly predicting a win (false positive) and incorrectly predicting a loss (false negative) are equally costly for analysts trying to assess a team's position. We also report accuracy, precision, and recall for completeness.

---

## Baseline Model

Our baseline model is a **Logistic Regression** classifier implemented in a single sklearn `Pipeline`.

**Features (7 total):**
- **Quantitative (3):** `golddiffat15`, `xpdiffat15`, `csdiffat15` — continuous numeric values representing early-game resource differentials.
- **Nominal (4):** `side` (Blue/Red, one-hot encoded), `firstblood`, `firstdragon`, `firsttower` — categorical features. `side` is encoded via `OneHotEncoder(drop='if_binary')`; the three binary flags are already 0/1.
- **Ordinal (0):** None of our features have a natural ordering with more than two levels.

**Preprocessing:** Median imputation for numeric columns, most-frequent imputation for binary flags, one-hot encoding for `side`.

**Train/test split:** 80/20 with stratification on `result` (train: 16,835 rows, test: 4,209 rows).

**Performance (test set):**

| Metric | Score |
|--------|-------|
| Accuracy | 0.7505 |
| F1 | 0.7517 |
| Precision | 0.7481 |
| Recall | 0.7552 |

The baseline model achieves ~75% accuracy, which is reasonable given that we only use 15-minute features. However, there is room for improvement by engineering features that capture *how* the early-game advantages interact (e.g., teams ahead in both gold and XP may be in a fundamentally different position than teams ahead in only one).

---

## Final Model

### Feature Engineering

We added three new features on top of the baseline's seven, all computable at minute 15:

1. **`abs_golddiffat15`** — the absolute value of the gold differential. This captures the *magnitude* of the gold gap regardless of direction. A team with a very large lead or deficit at 15 minutes is in a qualitatively different situation than a team in a close game, and this feature lets the model distinguish "lopsided" games from "close" games without knowing which side is ahead.

2. **`early_obj_count`** — the sum of `firstblood + firstdragon + firsttower` (0–3). As our EDA showed, win rate scales dramatically with the number of early objectives secured (24.1% with 0, up to 79.9% with all 3). This aggregate feature captures the compounding effect of objective control that individual binary flags cannot represent alone.

3. **`gold_xp_interaction`** — the product of `golddiffat15 × xpdiffat15`. Teams that lead in *both* gold and XP have reinforcing advantages (more items AND higher-level abilities), while teams ahead in one but behind in the other are in a more contested position. This interaction term captures that synergy.

### Preprocessing

Numeric features (including the new engineered ones) are standardized with `StandardScaler`, which is important for logistic regression since it ensures regularization treats all features equally. Binary features and one-hot encoded `side` are imputed but not scaled.

### Hyperparameter Tuning

We tuned the regularization strength `C` ∈ {0.01, 0.1, 1, 10, 100} with L2 penalty using 5-fold `GridSearchCV` scored by F1. We also evaluated Random Forest and Gradient Boosting classifiers, but the enhanced Logistic Regression outperformed both on cross-validation F1.

**Best hyperparameters:** C = 1, penalty = L2

**Performance comparison (test set):**

| Metric | Baseline | Final Model | Change |
|--------|----------|-------------|--------|
| Accuracy | 0.7505 | **0.7515** | +0.0010 |
| F1 | 0.7517 | **0.7532** | +0.0015 |
| Precision | 0.7481 | **0.7479** | −0.0002 |
| Recall | 0.7552 | **0.7586** | +0.0034 |

The final model improves F1 by 0.0015 and recall by 0.0034 over the baseline. While the improvement is modest, it reflects the inherent ceiling of 15-minute predictions — the gold differential alone captures most of the predictable signal, and the engineered features extract the remaining marginal information from objective interactions and gap magnitude.

<iframe
  src="assets/confusion_matrix.html"
  width="800"
  height="600"
  frameborder="0"
></iframe>

---

## Fairness Analysis

We investigate whether the final model performs equally well across different competition tiers.

**Group X:** Major leagues (LCK, LPL, LEC, LCS) — the four most prestigious professional leagues with the highest levels of competition (n = 410 test rows).

**Group Y:** Minor/regional leagues — all other leagues in the dataset (n = 3,799 test rows).

**Evaluation metric:** F1-score

**Null Hypothesis:** The model is fair — its F1-score for major-league games and minor-league games are roughly the same, and any differences are due to random chance.

**Alternative Hypothesis:** The model is unfair — its F1-score differs significantly between major and minor leagues.

**Test statistic:** F1(major) − F1(minor)

**Significance level:** α = 0.05

**Results:**
- F1 (Major leagues): **0.7560**
- F1 (Minor leagues): **0.7529**
- Observed F1 difference: **0.0031**
- p-value (1,000 permutations): **0.911**

We **fail to reject the null hypothesis**. The observed F1 difference of 0.003 between major and minor leagues is well within the range expected under random chance (p = 0.91). There is no evidence that the model performs unfairly across league tiers — it predicts match outcomes with roughly equal reliability regardless of the competition level.

<iframe
  src="assets/fairness_test.html"
  width="800"
  height="600"
  frameborder="0"
></iframe>
