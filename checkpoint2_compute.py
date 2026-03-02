import json
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score

RNG = np.random.default_rng(42)

# Load data
full = pd.read_csv('2022_LoL_esports_match_data_from_OraclesElixir.csv', low_memory=False)
teams = full[full['position'] == 'team'].copy()
teams['result'] = teams['result'].astype(int)
teams_15 = teams.dropna(subset=['golddiffat15', 'xpdiffat15', 'csdiffat15']).copy()

# -----------------------------
# Hypothesis Test 1: First dragon in close games
# -----------------------------
close_games = teams_15[teams_15['golddiffat15'].abs() <= 1000].copy()
obs1 = (
    close_games.loc[close_games['firstdragon'] == 1, 'result'].mean()
    - close_games.loc[close_games['firstdragon'] == 0, 'result'].mean()
)

stats1 = np.empty(10000)
fd_vals = close_games['firstdragon'].to_numpy().copy()
res_vals = close_games['result'].to_numpy()
for i in range(10000):
    RNG.shuffle(fd_vals)
    m1 = res_vals[fd_vals == 1].mean()
    m0 = res_vals[fd_vals == 0].mean()
    stats1[i] = m1 - m0

pval1 = np.mean(stats1 >= obs1)

# -----------------------------
# Hypothesis Test 2: Early gold gap and game length
# -----------------------------
teams_15['abs_gd15'] = teams_15['golddiffat15'].abs()
teams_15['gamelength_min'] = teams_15['gamelength'] / 60
q25 = teams_15['abs_gd15'].quantile(0.25)
q75 = teams_15['abs_gd15'].quantile(0.75)

groups = teams_15[(teams_15['abs_gd15'] <= q25) | (teams_15['abs_gd15'] >= q75)].copy()
groups['gap_group'] = np.where(groups['abs_gd15'] >= q75, 'large', 'small')

obs2 = (
    groups.loc[groups['gap_group'] == 'small', 'gamelength_min'].mean()
    - groups.loc[groups['gap_group'] == 'large', 'gamelength_min'].mean()
)

stats2 = np.empty(10000)
label_vals = groups['gap_group'].to_numpy().copy()
len_vals = groups['gamelength_min'].to_numpy()
for i in range(10000):
    RNG.shuffle(label_vals)
    ms = len_vals[label_vals == 'small'].mean()
    ml = len_vals[label_vals == 'large'].mean()
    stats2[i] = ms - ml

pval2 = np.mean(stats2 >= obs2)

# -----------------------------
# Baseline model (Step 6)
# -----------------------------
features = ['golddiffat15', 'xpdiffat15', 'csdiffat15', 'firstblood', 'firstdragon', 'firsttower', 'side']
target = 'result'
model_df = teams_15[features + [target]].copy()

X = model_df[features]
y = model_df[target]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

num_cols = ['golddiffat15', 'xpdiffat15', 'csdiffat15']
cat_cols = ['side']
binary_cols = ['firstblood', 'firstdragon', 'firsttower']

preprocess = ColumnTransformer(
    transformers=[
        ('num', Pipeline([('imputer', SimpleImputer(strategy='median'))]), num_cols),
        ('cat', Pipeline([
            ('imputer', SimpleImputer(strategy='most_frequent')),
            ('onehot', OneHotEncoder(drop='if_binary', handle_unknown='ignore'))
        ]), cat_cols),
        ('bin', Pipeline([('imputer', SimpleImputer(strategy='most_frequent'))]), binary_cols),
    ],
    remainder='drop'
)

baseline = Pipeline([
    ('preprocess', preprocess),
    ('model', LogisticRegression(max_iter=2000))
])

baseline.fit(X_train, y_train)
pred = baseline.predict(X_test)

results = {
    'hypothesis_1': {
        'n_close_rows': int(len(close_games)),
        'obs_diff_winrate': float(obs1),
        'p_value': float(pval1),
        'winrate_firstdragon_close': float(close_games.loc[close_games['firstdragon'] == 1, 'result'].mean()),
        'winrate_no_firstdragon_close': float(close_games.loc[close_games['firstdragon'] == 0, 'result'].mean())
    },
    'hypothesis_2': {
        'n_group_rows': int(len(groups)),
        'q25_abs_gd15': float(q25),
        'q75_abs_gd15': float(q75),
        'obs_diff_mean_length_min_small_minus_large': float(obs2),
        'p_value': float(pval2),
        'mean_length_small_gap': float(groups.loc[groups['gap_group'] == 'small', 'gamelength_min'].mean()),
        'mean_length_large_gap': float(groups.loc[groups['gap_group'] == 'large', 'gamelength_min'].mean())
    },
    'baseline_model': {
        'n_train': int(len(X_train)),
        'n_test': int(len(X_test)),
        'accuracy': float(accuracy_score(y_test, pred)),
        'f1': float(f1_score(y_test, pred)),
        'precision': float(precision_score(y_test, pred)),
        'recall': float(recall_score(y_test, pred))
    }
}

with open('checkpoint2_results.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=2)

print(json.dumps(results, indent=2))
