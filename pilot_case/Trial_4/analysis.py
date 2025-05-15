import pandas as pd
from scipy.stats import ttest_ind
from scipy.stats import chi2_contingency
import numpy as np

OTREE_DATA = "Exp1_Trial_4.csv"
DEMOGRAPHIC_DATA = "Exp1_Trial_4_Demographics.csv"

PROLIFIC_ID = "Intro.1.player.prolific_id"
STEM_QUIZ_1 = "Section_1.1.player.question"
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

otree_df = pd.read_csv(OTREE_DATA)
demographic_df = pd.read_csv(DEMOGRAPHIC_DATA)

# Merge the two dataframes by matching on prolific_id
df = pd.merge(otree_df, demographic_df, left_on=PROLIFIC_ID, right_on="Participant id")

# Remove any participants who returned the survey and did not complete it
df = df[df["Status"] == "APPROVED"]
df = df[df["Completion code"] == "C1BTHULB"]

# Remove any column starting with "pg"
df = df.loc[:, ~df.columns.str.startswith('pg')]
df = df.loc[:, ~df.columns.str.startswith('Cold')]

# Save the data to a new csv file
df.to_csv("Exp1_Trial_4_cleaned_data.csv")

# Print number of participants in the study
print(f'The number of participants in the Trial 4 is {df.shape[0]}')

# Remove participants who cheated: had more than 5 tab switches and more than 30 seconds of hidden pages.
df[SECTION_1_NUM_TAB_SWITCHES] = pd.to_numeric(df[SECTION_1_NUM_TAB_SWITCHES], errors='coerce')
df[SECTION_1_TIME_HIDDEN] = pd.to_numeric(df[SECTION_1_TIME_HIDDEN], errors='coerce')
df[SECTION_5_NUM_TAB_SWITCHES] = pd.to_numeric(df[SECTION_5_NUM_TAB_SWITCHES], errors='coerce')
df[SECTION_5_TIME_HIDDEN] = pd.to_numeric(df[SECTION_5_TIME_HIDDEN], errors='coerce')

df = df[(df[SECTION_1_NUM_TAB_SWITCHES] <= 5.0) & 
        (df[SECTION_1_TIME_HIDDEN] <= 30.0) & 
        (df[SECTION_5_NUM_TAB_SWITCHES] <= 5.0) & 
        (df[SECTION_5_TIME_HIDDEN] <= 30.0)]

"""
 Remove participants who answer incorrectly on ball 
    origin estimation questions in Section 3A, 3B, and 3C.
    Ground: 
        - If their on the ground path, their ball was red, and they answered  Fail box - remove them.
        - If their on the ground path, their ball was black, and they answered  Pass box - remove them.
    Positive:
        - If their on the positive path, their ball is black, and they answered Fail box - remove them.
    Negative:
        - If their on the negative path, their ball is black, and they answered Pass box - remove them.
 """

df = df[~((df[INFO_STRUCTURE] == 'ground') & (df[BALL_COLOR] == 'red') & (df[BALL_ORIGIN_ESTIMATION] == 'Fail'))]

df = df[~((df[INFO_STRUCTURE] == 'ground') & (df[BALL_COLOR] == 'black') & (df[BALL_ORIGIN_ESTIMATION] == 'Pass'))]

df = df[~((df[INFO_STRUCTURE] == 'positive') & (df[BALL_COLOR] == 'black') & (df[BALL_ORIGIN_ESTIMATION] == 'Fail'))]

df = df[~((df[INFO_STRUCTURE] == 'negative') & (df[BALL_COLOR] == 'black') & (df[BALL_ORIGIN_ESTIMATION] == 'Pass'))]

# Conduct t_tests: Is 
section_1_cols = [
    "Intro.1.player.prolific_id", 
    "Section_1.1.player.question1",
    "Section_1.1.player.question2", 
    "Section_1.1.player.question3", 
    "Section_1.1.player.question4", 
    "Section_1.1.player.question5", 
    "Section_1.1.player.question6", 
    "Section_1.1.player.question7", 
    "Section_1.1.player.question8", 
    "Section_1.1.player.question9", 
    "Section_1.1.player.question10", 
    "Section_1.1.player.stem_quiz_1_answers", 
    "Section_1.1.player.stem_quiz_1_score", 
    "Section_1.1.player.num_tab_switches_in_section_1", "Section_1.1.player.total_time_hidden_in_section_1"
                  ]
section_2_3_cols = [
    "Section_2_3.1.player.track",
    "Section_2_3.1.player.path",
    "Section_2_3.1.player.info_structure",
    "Section_2_3.1.player.performance",
    "Section_2_3.1.player.ball_color",
    "Section_2_3.1.player.overplacement",
    "Section_2_3.1.player.overestimation",
    "Section_2_3.1.player.passing_threshold",
    "Section_2_3.1.player.ball_origin_estimation"
    ]
section_4_5_cols = [
    "Section_4_5.1.player.question1",
    "Section_4_5.1.player.question2",
    "Section_4_5.1.player.question3",
    "Section_4_5.1.player.question4",
    "Section_4_5.1.player.question5",
    "Section_4_5.1.player.question6",
    "Section_4_5.1.player.question7",
    "Section_4_5.1.player.question8",
    "Section_4_5.1.player.question9",
    "Section_4_5.1.player.question10",
    "Section_4_5.1.player.quiz_2_answers",
    "Section_4_5.1.player.quiz_2_score",
    "Section_4_5.1.player.preferred_second_survey",
    "Section_4_5.1.player.num_tab_switches_in_section_5",
    "Section_4_5.1.player.total_time_hidden_in_section_5"
]
section_6_cols = [
    "Section_6.1.player.question1",
    "Section_6.1.player.question2",
    "Section_6.1.player.question3",
    "Section_6.1.player.question4",
    "Section_6.1.player.question5",
    "Section_6.1.player.question6",
    "Section_6.1.player.question7",
    "Section_6.1.player.question8",
    "Section_6.1.player.question9",
    "Section_6.1.player.question10",
    "Section_6.1.player.question11",
    "Section_6.1.player.risk_tolerance_answers"
]

section_7_cols = [
    "Section_7.1.player.schools_private_independent",
    "Section_7.1.player.schools_private_religious",
    "Section_7.1.player.schools_public_school",
    "Section_7.1.player.schools_homeschool",
    "Section_7.1.player.schools_online_school",
    "Section_7.1.player.schools_charter_school",
    "Section_7.1.player.schools_all_girls_school",
    "Section_7.1.player.schools_all_boys_school",
    "Section_7.1.player.schools_stem_oriented_school",
    "Section_7.1.player.track_decision",
    "Section_7.1.player.experience",
    "Section_7.1.player.preferred_second_survey"
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
columns = section_1_cols + section_2_3_cols + section_4_5_cols + section_6_cols + section_7_cols + demographic_cols

df = df[columns]

df.to_csv("Exp1_Trial_4_analysis_data.csv")

def t_tests(df, alpha):
    ground_persistence = df[df[INFO_STRUCTURE] == 'ground'][PREFERRED_SECOND_SURVEY].apply(lambda x: 1 if x == 'Continue STEM Track - Proceed to STEM Quiz' else 0)
    positive_persistence = df[df[INFO_STRUCTURE] == 'positive'][PREFERRED_SECOND_SURVEY].apply(lambda x: 1 if x == 'Continue STEM Track - Proceed to STEM Quiz' else 0)
    negative_persistence = df[df[INFO_STRUCTURE] == 'negative'][PREFERRED_SECOND_SURVEY].apply(lambda x: 1 if x == 'Continue STEM Track - Proceed to STEM Quiz' else 0)

    t_statistic, p_value = ttest_ind(ground_persistence, positive_persistence)
    print("NULL HYPOTHESIS: There is no significant difference in the average persistence of participants in the ground truth group compared to the average persistence of participants in the positively skewed group.")
    print(f'(Ground Truth, Positively Skewed) p-value: {p_value}')
    if p_value <= alpha:
        print('Reject the null hypothesisd\n')
    else:
        print('Fail to reject the null hypothesis\n')

    t_statistic, p_value = ttest_ind(ground_persistence, negative_persistence)
    print(f'(Ground Truth, Negatively Skewed) p-value: {p_value}')
    print("NULL HYPOTHESIS: There is no significant difference in the average persistence of participants in the ground group compared to the average persistence of participants in the negatively skewed group.")
    if p_value <= alpha:
        print('Reject the null hypothesis\n')
    else:
        print('Fail to reject the null hypothesis\n')

t_tests(df, 0.05)


'''
As part of our secondary analysis, we want to determine if ones persistence in Stage 3 is independent of risk preference in Stage 4. To do this, we will employ a Chi-squared test to see if there is a significant correlation between persistence (continue or quit) and risk preference (fixed payment or bet). Our null hypothesis is that persistence and risk preference are not significantly associated. Our alternative hypothesis is that persistence and risk preference are significantly associated. We will create a contingency table where the rows represent the bet versus fixed categorical options and the columns represent continue or quit. We will fill each cell of the contingency table with the frequencies of each contingency.
'''
# Calculate when each participant switches over from the risky payment to the constant payment

def risk_tolerant_or_averse(risk_quiz):
    for i, c in enumerate(risk_quiz):
        if c == "C":
            if i <= 5: # Would you rather have 50% chance of $10 or $5?
                return 'risk_averse'
            return 'risk_tolerant'
    return 'risk_tolerant'

def risk_tolerant_or_averse(row):
    for i in range(1, 11):
        question_name = RISK_TOLERANCE + str(i)
        if row[question_name] == "C":
            if i <= 5: # Would you rather have 50% chance of $10 or $5?
                return 'risk_averse'
            return 'risk_tolerant'
    return 'risk_tolerant'


def chi_squared_test(df, alpha):
    df['risk_averse_or_tolerant'] = df.apply(lambda row: risk_tolerant_or_averse(row), axis=1)
    df['continue_or_quit'] = df[PREFERRED_SECOND_SURVEY].apply(lambda x: 'Continue' if x == 'Continue STEM Track - Proceed to STEM Quiz' else 'Quit')

    continue_and_bet = sum((df['continue_or_quit'] == 'Continue') & (df['risk_averse_or_tolerant'] == 'risk_tolerant'))
    continue_and_fixed = sum((df['continue_or_quit'] == 'Continue') & (df['risk_averse_or_tolerant'] == 'risk_averse'))
    quit_and_bet = sum((df['continue_or_quit'] == 'Quit') & (df['risk_averse_or_tolerant'] == 'risk_tolerant'))
    quit_and_fixed = sum((df['continue_or_quit'] == 'Quit') & (df['risk_averse_or_tolerant'] == 'risk_averse'))

    contingency_table = np.array([[continue_and_bet, quit_and_bet], [continue_and_fixed, quit_and_fixed]])

    print(contingency_table)

    chi2, p, dof, expected = chi2_contingency(contingency_table)
    print(f'The p-value for the Chi-squared test is {p}')
    if p <= alpha:
        print('Reject the null hypothesis - there is no signficant association between persistence and risk preference')
    else:
        print('Fail to reject the null hypothesis - there is a significant association between persistence and risk preference')

chi_squared_test(df, 0.05)


# Persistence by gender
df['continue_or_quit_numeric'] = df['continue_or_quit'].map({'Continue': 1, 'Quit': 0})

persistence_by_gender = df.groupby('Sex')['continue_or_quit_numeric'].mean()
print(persistence_by_gender)

# Persistence by ethnicity
persistence_by_ethnicity = df.groupby('Ethnicity simplified')['continue_or_quit_numeric'].mean()
print(persistence_by_ethnicity)

# Persistence by ethnicity and sex
peristence_by_ethnicity_and_sex = df.groupby(['Sex', 'Ethnicity simplified'])['continue_or_quit_numeric'].mean()
print(peristence_by_ethnicity_and_sex)
