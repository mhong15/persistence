import pandas as pd
from scipy.stats import ttest_ind
from scipy.stats import chi2_contingency
import numpy as np

# Data formatting
# Renaming Columns from the Otree csv
OTREE_DATA = "all_apps_wide-2024-09-24.csv"
df = pd.read_csv(OTREE_DATA)

count = df[(df["Section_1.1.player.stem_quiz_1_answers"].str.len() < 10) & (df["Section_6.1.player.risk_tolerance_answers"].str.len() == 11)].shape[0]

print(count)
print(df.columns.__len__()) 
print(df.__len__())