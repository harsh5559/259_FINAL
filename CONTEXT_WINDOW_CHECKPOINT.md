# CONTEXT WINDOW CHECKPOINT

> **Purpose**: This document is a handoff for the next AI model (or future session) to pick up work on this project seamlessly. It explains everything that has been done, the current state of all files, and what remains to be completed.

---

## Project Overview

**Course**: DSC 259R — Data Science (UCSD)
**Assignment**: Final Project — "The Data Science Lifecycle"
**Dataset chosen**: League of Legends 2022 professional match data (Oracle's Elixir)
**Notebook title**: *Snowball or Comeback? How Early Objectives Shape Professional League of Legends*
**Research question**: In professional League of Legends, do early-game objectives provide a genuine strategic advantage independent of a team's overall gold position, and how reliably can match outcomes be predicted from the first 15 minutes of play?

The project is broken into 8 steps across two deliverables:
- **Part 1**: A Jupyter Notebook (`template.ipynb`) with the full analysis
- **Part 2**: A public GitHub Pages website (not yet started)

---

## Repository & File Layout

All project files live at `F:\259_final\`. The GitHub repo is `git@github.com:harsh5559/259_FINAL.git` (not yet initialized as a git repo locally).

```
F:\259_final\
├── 2022_LoL_esports_match_data_from_OraclesElixir.csv   # ~96 MB dataset
├── template.ipynb          # Main analysis notebook (Steps 1-8, Steps 1-2 complete)
├── dsc259r_utils.py        # Course utility file (plotting helpers, display_df, etc.)
├── checkpoint1.pdf         # Checkpoint 1 Gradescope PDF (regenerated with new hypothesis)
├── generate_checkpoint1.py # Script to regenerate the checkpoint 1 PDF
├── CHECKPOINT1_INSTRUCTIONS.txt
├── FINAL_INSTRUCTIONS.txt
├── DATASET_INSTRUCTIONS.txt  (empty)
├── assets/
│   ├── winrate_by_side.html      # Plotly interactive chart (for future website)
│   ├── gamelength_dist.html      # Plotly interactive chart (for future website)
│   ├── winrate_chart.png         # Old matplotlib PNG (no longer used)
│   └── objective_stacking_chart.png  # Matplotlib PNG used in checkpoint1.pdf
└── __pycache__/
```

---

## Python Environment

- **Python version**: 3.13 at `C:\Python313\python.exe`
- **WARNING**: There are multiple Python installs on this machine (3.10 at `C:\Users\harsh\AppData\Local\Programs\Python\Python310\` and Miniconda at `C:\Users\harsh\miniconda3\`). The Python 3.10 Jupyter install is broken (IPython `typing_extensions` conflict). **Always use `C:\Python313\python.exe` explicitly** or the `python` command (which resolves to 3.13 first on PATH).
- **Installed packages** (all under Python 3.13): pandas 2.3.3, numpy 2.2.6, plotly 6.5.2, scikit-learn 1.7.2, jupyter, fpdf2, matplotlib, ipykernel
- **Registered kernel**: `python313` — registered via `python -m ipykernel install --user --name python313`
- **Running notebooks**: Open `template.ipynb` in VS Code/Cursor and select the **Python 3.13** kernel. Do NOT use `jupyter nbconvert --execute` from the command line (it picks up the broken Python 3.10 Jupyter).

---

## What Has Been Done

### Checkpoint 1 (COMPLETE — ready to submit)

**`checkpoint1.pdf`** is the Gradescope submission for Checkpoint 1. It answers all 4 prompts:

1. **Dataset choice**: League of Legends 2022 Oracle's Elixir — 12,415 games, 55 regions, rich early-game state data + objective flags.
2. **Plotly visualization**: Bar chart of win rate by number of early objectives secured (0→24.1%, 1→41.9%, 2→61.1%, 3→79.9%).
3. **Hypothesis test plan**: Permutation test — does first dragon boost win rate even in close games (|golddiffat15| ≤ 1000)? Null = no independent effect, Alternative = first dragon boosts win rate in close games. Test stat = difference in win rates. Observed ≈ 13.2 pp.
4. **Prediction problem**: Predict `result` (win/loss) as binary classification using early-game stats at 15 min.

### Notebook (`template.ipynb`) — Steps 1 and 2 Complete

The notebook has 31 cells. Steps 1 and 2 are fully implemented; Steps 3-8 are TODO placeholders.

**Cell 0 (markdown)**: Title, name placeholder, website link placeholder.

**Cell 1 (code)**: Imports — pandas, numpy, plotly, `from dsc259r_utils import *`

**Step 1 (Cells 2-5)**:
- Loads the full CSV with `low_memory=False` (needed because the `url` column has mixed types)
- Filters to `position == 'team'` rows only (24,830 rows = 2 per game × 12,415 games)
- Prints dataset stats: 148,980 total rows, 165 columns, 55 leagues, date range Jan-Dec 2022
- Markdown cell with the research question and a table of relevant column descriptions
- `display_df()` preview of relevant columns

**Step 2 (Cells 6-17)**:
- **Cleaning cell**: Parses `date` to datetime, creates `gamelength_min` (seconds → minutes), converts `result` to bool, checks missingness in `golddiffat15`/`xpdiffat15`/`csdiffat15` (15.2% missing = games that ended before 15 min), creates `teams_15` (21,044 rows with complete 15-min data)
- **Cleaned preview**: `display_df()` of cleaned data
- **Univariate 1**: Plotly histogram of `gamelength_min` — saves to `assets/gamelength_dist.html`
- **Univariate 2**: Plotly bar chart of win rate by side (Blue 52.4% vs Red 47.6%) — saves to `assets/winrate_by_side.html`
- **Bivariate 1**: Plotly box plot of `golddiffat15` by win/loss — saves to `assets/golddiff_by_outcome.html`
- **Bivariate 2**: Plotly scatter of `golddiffat15` vs `kills` colored by outcome (samples 3,000 rows for clarity)
- **Aggregate 1**: Pivot table of win rates by `league` and `side` (top 15 leagues by game count). Note: pivot columns come out alphabetically (`games` before `win_rate`), so columns are manually reordered after creation.
- **Aggregate 2**: First-objective rates (firstblood, firstdragon, firstbaron, firsttower) by side, printed as markdown

**Cell 18 (markdown)**: Checkpoint 1 Answers summary — all 4 answers written out inline in the notebook for easy reference.

**Steps 3-8 (Cells 19-30)**: Markdown headers + `# TODO` code cells only.

---

## Key Dataset Facts

| Fact | Value |
|------|-------|
| File | `2022_LoL_esports_match_data_from_OraclesElixir.csv` |
| Total rows | 148,980 (players + teams) |
| Team rows (`position == 'team'`) | 24,830 |
| Unique games | 12,415 |
| Leagues | 55 |
| Date range | Jan 10 – Dec 27, 2022 |
| Blue side win rate | 52.4% |
| Red side win rate | 47.6% |
| Win rate with 0 early objectives | 24.1% |
| Win rate with all 3 early objectives | 79.9% |
| First dragon win rate in close games | 56.6% vs 43.4% |
| Missing `golddiffat15` (team rows) | 3,786 (15.2%) — games ended before 15 min |
| Columns | 165 |

**Important structural note**: Each game produces 12 rows — 10 player rows (one per player, positions: top/jng/mid/bot/sup) and 2 team rows (one per team, position = 'team'). Most analysis should use `position == 'team'` rows only.

---

## What Remains To Be Done

### Checkpoint 2 (due Monday of Week 10)

Submit on Gradescope:
1. Two hypotheses tested in Step 4 and results
2. Brief explanation of baseline model and improvement plans
3. Working GitHub Pages URL with at least a project title

### Step 3: Assessment of Missingness
- Pick a column with non-trivial missingness to analyze (suggestion: `golddiffat15`)
- Write NMAR reasoning (no code needed for NMAR section)
- Permutation tests: find one column the missingness depends on, one it does not
- Use `create_kde_plotly()` or `multiple_hists()` from `dsc259r_utils` to visualize

### Step 4: Hypothesis Testing
- **Planned test 1**: Permutation test for first dragon's independent effect in close games
  - Null: Among close games (|golddiffat15| ≤ 1000), first dragon teams win at the same rate as non-first-dragon teams
  - Alternative: First dragon teams win at a higher rate even in close games
  - Test statistic: Win rate (first dragon, close) − Win rate (no first dragon, close), observed ≈ 13.2 pp
  - Run 10,000 permutations, shuffle `firstdragon` labels within close games
- **Planned test 2 (for Checkpoint 2)**: Consider testing whether the gold lead at 15 min affects game duration (larger leads → shorter games), or whether objective stacking is synergistic vs additive

### Steps 5-8: Predictive Modeling
- **Column to predict**: `result` (binary classification)
- **Features available at 15 min**: `golddiffat15`, `xpdiffat15`, `csdiffat15`, `firstblood`, `firstdragon`, `side` (encode Blue=1/Red=0)
- **Step 6 baseline**: sklearn Pipeline with at least 2 features, handle categorical `side` with OneHotEncoder
- **Step 7 final**: Engineer 2+ new features, GridSearchCV for hyperparameter tuning
- **Step 8 fairness**: Permutation test comparing model performance (e.g. precision) across two groups (suggestion: major regions like LCK/LPL vs minor regions)

### Part 2: GitHub Pages Website
- Create a new GitHub repo (different from `harsh5559/259_FINAL` — that's the code repo)
- URL format: `<username>.github.io/<reponame>`
- Use Jekyll with a non-default theme (`_config.yml` with `remote_theme`)
- Website `README.md` must have all 8 section headings (exactly as: Introduction, Data Cleaning and Exploratory Data Analysis, Assessment of Missingness, Hypothesis Testing, Framing a Prediction Problem, Baseline Model, Final Model, Fairness Analysis)
- Embed interactive Plotly charts using `<iframe src="assets/file.html">` syntax (use `fig.write_html(..., include_plotlyjs='cdn')`)
- The `assets/` folder in `F:\259_final\` already has `winrate_by_side.html` and `gamelength_dist.html` ready

---

## dsc259r_utils.py — Available Helpers

Key functions available after `from dsc259r_utils import *`:

| Function | Purpose |
|----------|---------|
| `display_df(df)` | Display DataFrame with row/col limits |
| `dfs_side_by_side(*dfs)` | Display multiple DataFrames side by side |
| `create_kde_plotly(data1, data2, col, labels)` | KDE plot comparing two groups |
| `multiple_hists(*datasets, col)` | Overlaid histograms |
| `multiple_kdes(*datasets, col)` | Overlaid KDE plots |
| `multiple_describe(*datasets)` | Summary stats for multiple datasets |

The module also sets a custom Plotly template `"dsc259r"` (white background, grid lines, centered titles). Use `template='dsc259r'` in Plotly calls for consistent styling.

---

## Grading Rubric Reference

| Step | Points |
|------|--------|
| Step 1: Introduction | 8 |
| Step 2: Data Cleaning and EDA | 24 |
| Step 3: Assessment of Missingness | 20 |
| Step 4: Hypothesis Testing | 28 |
| Step 5: Framing a Prediction Problem | 15 |
| Step 6: Baseline Model | 35 |
| Step 7: Final Model | 35 |
| Step 8: Fairness Analysis | 15 |
| Website completeness | 20 |
| **Total** | **200** |

Checkpoint 1 is worth 20 points (2% of overall grade). Checkpoint 2 is also worth 20 points.
Final submission deadline is **Monday of Finals Week** — hard deadline, no extensions.

---

## Notes on the Linux Question

The user originally had to use Linux/Ubuntu to clone the class repo (`dsc259r-2026-wi`) to get `template.ipynb` and `dsc259r_utils.py`. Those files are now present locally at `F:\259_final\` and **do not need to be retrieved again**. All remaining work can be done entirely on Windows.
