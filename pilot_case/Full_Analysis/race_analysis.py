import pandas as pd
from scipy.stats import ttest_ind
from scipy.stats import chi2_contingency
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
import statsmodels.formula.api as smf
from itertools import combinations


PROLIFIC_ID = "Intro.1.player.prolific_id"
STEM_QUIZ_1 = "Section_1.1.player.question"
STEM_QUIZ_1_ANSWERS = "Section_1.1.player.stem_quiz_1_answers"
STEM_QUIZ_1_SCORE = "Section_1.1.player.stem_quiz_1_score"
SECTION_1_NUM_TAB_SWITCHES = "Section_1.1.player.num_tab_switches_in_section_1"
SECTION_1_TIME_HIDDEN = "Section_1.1.player.total_time_hidden_in_section_1"
INFO_STRUCTURE = "Section_2_3.1.player.info_structure"
PLAYER_PERFORMANCE = "Section_2_3.1.player.performance"
OVERPLACEMENT = "Section_2_3.1.player.overplacement"
OVERESTIMATION = "Section_2_3.1.player.overestimation"
PASSING_THRESHOLD = "Section_2_3.1.player.passing_threshold"
BALL_ORIGIN_ESTIMATION = "Section_2_3.1.player.ball_origin_estimation"
QUIZ_2 = "Section_4_5.1.player.question"
PREFERRED_SECOND_SURVEY = "Section_4_5.1.player.preferred_second_survey"
SECTION_5_NUM_TAB_SWITCHES = "Section_4_5.1.player.num_tab_switches_in_section_5"
SECTION_5_TIME_HIDDEN = "Section_4_5.1.player.total_time_hidden_in_section_5"
RISK_TOLERANCE = "Section_6.1.player.question"
BALL_COLOR = "Section_2_3.1.player.ball_color"

ETHNICITIES_SIMPLIFIED = ['Asian', 'White', 'Black', 'Mixed', 'Other']
ETHNICITIES_PAIRED = list(combinations(ETHNICITIES_SIMPLIFIED, 2))
SEXES = ['Female', 'Male']
INFO_STRUCTURES = ['all', 'ground', 'positive', 'negative']
BALL_SIGNALS = ['black', 'red']
INFO_STRUCTURE_STRING = {'all': 'a', 'ground': 'g', 'positive': '+', 'negative': '-'}
INFO_STRUCTURE_PAIRS = [('ground', 'positive'), ('ground', 'negative'), ('positive','negative')]

def print_header(header):
    print(f"\n{header}\n{'-' * (50)}")

df = pd.concat([  pd.read_csv("Exp1_Trial_2_analysis_data.csv"),
                pd.read_csv("Exp1_Trial_3_analysis_data.csv"),
                pd.read_csv("Exp1_Trial_4_analysis_data.csv"),
                pd.read_csv("Exp1_Trial_5_analysis_data.csv"),
                pd.read_csv("Exp1_Trial_6_analysis_data.csv")])

df['continue_or_quit'] = df[PREFERRED_SECOND_SURVEY].apply(lambda x: 1 if x == 'Continue STEM Track - Proceed to STEM Quiz' else 0)

df.to_csv("Exp1_Combined_analysis_data.csv", index=False)

print(f"There are {df.shape[0]} out of 1004 participants left after excluding people who cheated or incorrectly answered the ball origin estimation question.")

# Calculate the difference between average persistence of Asians and other

