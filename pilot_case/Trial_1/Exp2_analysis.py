import pandas as pd
from scipy.stats import ttest_ind
from scipy.stats import chi2_contingency
import numpy as np
import matplotlib.pyplot as plt

DATA = "Exp2_Trial_1_cleaned_data.csv"

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
ETHNICITIES_SIMPLIFIED = ['Asian', 'White', 'Black', 'Mixed', 'Other']
SEXES = ['Female', 'Male']
INFO_STRUCTURES = ['all', 'ground', 'positive', 'negative']
BALL_SIGNALS = ['black', 'red']

df = pd.read_csv = pd.read_csv(DATA)

# Print preference for Choice A or Choice B based on gender
def preferred_info_structure_by_demographic(df):
    choice_A = df[df[PREFERRED_INFO_STRUCTURE] == 'Choice A']
    choice_B = df[df[PREFERRED_INFO_STRUCTURE] == 'Choice B']
   
    df_preferred_info_structure = pd.DataFrame(columns=['Group', 'Choice A', 'Choice B'])

    df_preferred_info_structure = df_preferred_info_structure._append({'Group': 'All', 'Choice A': choice_A.shape[0]/(df.shape[0]), 'Choice B': choice_B.shape[0]/df.shape[0]}, ignore_index=True)

    for sex in SEXES:
        subset_participants = df[df['Sex'] == sex]
        choice_A = subset_participants[subset_participants[PREFERRED_INFO_STRUCTURE] == 'Choice A']
        choice_B = subset_participants[subset_participants[PREFERRED_INFO_STRUCTURE] == 'Choice B']
        group_size = choice_A.shape[0] + choice_B.shape[0]

        df_preferred_info_structure = df_preferred_info_structure._append({'Group': sex, 'Choice A': choice_A.shape[0]/(group_size), 'Choice B': choice_B.shape[0]/group_size}, ignore_index=True)
    
    for ethnicity in ETHNICITIES_SIMPLIFIED:
        subset_participants = df[df['Ethnicity simplified'] == ethnicity]
        choice_A = subset_participants[subset_participants[PREFERRED_INFO_STRUCTURE] == 'Choice A']
        choice_B = subset_participants[subset_participants[PREFERRED_INFO_STRUCTURE] == 'Choice B']
        group_size = choice_A.shape[0] + choice_B.shape[0]

        df_preferred_info_structure = df_preferred_info_structure._append({'Group': ethnicity, 'Choice A': choice_A.shape[0]/(group_size), 'Choice B': choice_B.shape[0]/group_size}, ignore_index=True)
    
    for ethnicity in ETHNICITIES_SIMPLIFIED:
        for sex in SEXES:
            subset_participants = df[(df['Sex'] == sex) & (df['Ethnicity simplified'] == ethnicity)]
            choice_A = subset_participants[subset_participants[PREFERRED_INFO_STRUCTURE] == 'Choice A']
            choice_B = subset_participants[subset_participants[PREFERRED_INFO_STRUCTURE] == 'Choice B']
            group_size = choice_A.shape[0] + choice_B.shape[0]

            df_preferred_info_structure = df_preferred_info_structure._append({'Group': f'{ethnicity}, {sex}', 'Choice A': choice_A.shape[0]/(group_size), 'Choice B': choice_B.shape[0]/group_size}, ignore_index=True)

    
    df_preferred_info_structure = df_preferred_info_structure.round(4)
    df_preferred_info_structure.to_csv("preferred_info_structure_by_demographic.csv")

    df_preferred_info_structure.plot.bar(x='Group', y=['Choice A', 'Choice B'], rot=90, figsize=(10, 5), title='Preferred Info Structure by Demographic', ylabel='% of participants in group', xlabel='Demographic Group')
    plt.legend(loc='upper right', labels=['Positively Skewed', 'Negatively Skewed'])
    plt.tight_layout()
    plt.show()
    
def t_tests(df, alpha):
    print(df[(df['Sex'] == "Female") & (df['Ethnicity simplified'] == 'Asian')].shape[0])
    print(df[(df['Sex'] == "Male") & (df['Ethnicity simplified'] == 'Asian')].shape[0])
    female_preference_A = df[(df['Sex'] == "Female") & (df['Ethnicity simplified'] == 'Asian')][PREFERRED_INFO_STRUCTURE].apply(lambda x: 1 if x == 'Choice A' else 0)
    male_preference_A = df[(df['Sex'] == "Male") & (df['Ethnicity simplified'] == 'Asian')][PREFERRED_INFO_STRUCTURE].apply(lambda x: 1 if x == 'Choice A' else 0)
    print(female_preference_A.mean(), male_preference_A.mean())
    (_, p_value) = ttest_ind(female_preference_A, male_preference_A)
    print(f'(Female, Male) Preference for Choice A p-value: {p_value}')
    if p_value <= alpha:
        print(f'Reject: Significant difference between (Female, Male) Preference for Choice A\n')
    else:
        print(f'Fail to reject: No significant difference between (Female, Male) Persistence for Choice A')

t_tests(df, 0.05)
preferred_info_structure_by_demographic(df)
