import pandas as pd
from scipy.stats import ttest_ind
from scipy.stats import chi2_contingency
import numpy as np

OTREE_DATA = "Exp2_Pilot_Case.csv"
DEMOGRAPHIC_DATA = "Exp2_Pilot_Case_demographics.csv"

PROLIFIC_ID = "Exp2_Intro.1.player.prolific_id"
STEM_QUIZ_1 = "Exp2_Section_1.1.player.question"
STEM_QUIZ_1_ANSWERS = "Exp2_Section_1.1.player.stem_quiz_1_answers"
STEM_QUIZ_1_SCORE = "Exp2_Section_1.1.player.stem_quiz_1_score"
SECTION_1_NUM_TAB_SWITCHES = "Exp2_Section_1.1.player.num_tab_switches_in_section_1"
PREFERRED_INFO_STRUCTURE = "Exp2_Section_2_3.1.player.preferred_info_structure"
SECTION_1_TIME_HIDDEN = "Exp2_Section_1.1.player.total_time_hidden_in_section_1"

PLAYER_PERFORMANCE = "Exp2_Section_2_3.1.player.performance"
OVERPLACEMENT = "Exp2_Section_2_3.1.player.overplacement"
OVERESTIMATION = "Exp2_Section_2_3.1.player.overestimation"
PASSING_THRESHOLD = "Exp2_Section_2_3.1.player.passing_threshold"
BALL_ORIGIN_ESTIMATION = "Exp2_Section_2_3.1.player.ball_origin_estimation"
BALL_COLOR = "Exp2_Section_2_3.1.player.ball_color"

otree_df = pd.read_csv(OTREE_DATA)
demographic_df = pd.read_csv(DEMOGRAPHIC_DATA)

# Merge the two dataframes by matching on prolific_id
df = pd.merge(otree_df, demographic_df, left_on=PROLIFIC_ID, right_on="Participant id")

# Remove any participants who returned the survey and did not complete it
df = df[df["Status"] == "APPROVED"]
df = df[df["Completion code"] == "C1BTHULB"]

# Remove any column starting with "pg"
df = df.loc[:, ~df.columns.str.startswith('pg')]

# Save the data to a new csv file
df.to_csv("Exp2_Pilot_Case_cleaned_data.csv")

# Print number of participants in the study
print(f'The number of participants in the Trial 1 is {df.shape[0]}')

# Remove participants who cheated: had more than 5 tab switches and more than 30 seconds of hidden pages.
df[SECTION_1_NUM_TAB_SWITCHES] = pd.to_numeric(df[SECTION_1_NUM_TAB_SWITCHES], errors='coerce')
df[SECTION_1_TIME_HIDDEN] = pd.to_numeric(df[SECTION_1_TIME_HIDDEN], errors='coerce')

df = df[(df[SECTION_1_NUM_TAB_SWITCHES] <= 5.0) & 
        (df[SECTION_1_TIME_HIDDEN] <= 30.0)]

df = df[~((df[PREFERRED_INFO_STRUCTURE] == 'Choice A') & (df[BALL_COLOR] == 'black') & (df[BALL_ORIGIN_ESTIMATION] == 'Fail'))]

df = df[~((df[PREFERRED_INFO_STRUCTURE] == 'Choice B') & (df[BALL_COLOR] == 'black') & (df[BALL_ORIGIN_ESTIMATION] == 'Pass'))]

# Conduct t_tests: Is 
section_1_cols = [
    "Exp2_Intro.1.player.prolific_id", 
    "Exp2_Section_1.1.player.question1",
    "Exp2_Section_1.1.player.question2",
    "Exp2_Section_1.1.player.question3",
    "Exp2_Section_1.1.player.question4",
    "Exp2_Section_1.1.player.question5",
    "Exp2_Section_1.1.player.question6",
    "Exp2_Section_1.1.player.question7",
    "Exp2_Section_1.1.player.question8",
    "Exp2_Section_1.1.player.question9",
    "Exp2_Section_1.1.player.question10",
    "Exp2_Section_1.1.player.stem_quiz_1_answers", 
    "Exp2_Section_1.1.player.stem_quiz_1_score", 
    "Exp2_Section_1.1.player.num_tab_switches_in_section_1", "Exp2_Section_1.1.player.total_time_hidden_in_section_1"
                  ]
section_2_3_cols = [
    "Exp2_Section_2_3.1.player.preferred_info_structure",
    "Exp2_Section_2_3.1.player.performance",
    "Exp2_Section_2_3.1.player.ball_color",
    "Exp2_Section_2_3.1.player.overplacement",
    "Exp2_Section_2_3.1.player.overestimation",
    "Exp2_Section_2_3.1.player.passing_threshold",
    "Exp2_Section_2_3.1.player.ball_origin_estimation",
    ]
section_4_cols = [
   "Exp2_Section_4.1.player.schools_private_independent",
   "Exp2_Section_4.1.player.schools_private_religious",
   "Exp2_Section_4.1.player.schools_public_school",
   "Exp2_Section_4.1.player.schools_homeschool",
   "Exp2_Section_4.1.player.schools_online_school",
   "Exp2_Section_4.1.player.schools_charter_school",
   "Exp2_Section_4.1.player.schools_all_girls_school",
   "Exp2_Section_4.1.player.schools_all_boys_school",
   "Exp2_Section_4.1.player.schools_stem_oriented_school",
   "Exp2_Section_4.1.player.subjects",
   "Exp2_Section_4.1.player.experience",

]
demographic_cols = [
    "Time taken",
    "Total approvals",
    "Ethnicity",
    "Highest education level completed",
    "Age",
    "Sex",
    "Ethnicity simplified",
    "Country of birth",
    "Country of residence",
    "Nationality",
    "Language",
    "Student status",
    "Employment status"
]
columns = section_1_cols + section_2_3_cols + section_4_cols + demographic_cols
