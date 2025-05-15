import pandas as pd
from scipy.stats import ttest_ind
from scipy.stats import chi2_contingency
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
import statsmodels.formula.api as smf


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
SEXES = ['Female', 'Male']
INFO_STRUCTURES = ['all', 'ground', 'positive', 'negative']
BALL_SIGNALS = ['black', 'red']

# Combine the cleaned data for all trials
df = pd.concat([pd.read_csv("Exp1_Trial_4_analysis_data.csv"),
                  pd.read_csv("Exp1_Trial_2_analysis_data.csv"),
                  pd.read_csv("Exp1_Trial_3_analysis_data.csv")])

# Add a new column for persistence where 1-> STEM Track and 0-> Quit
df['continue_or_quit'] = df[PREFERRED_SECOND_SURVEY].apply(lambda x: 1 if x == 'Continue STEM Track - Proceed to STEM Quiz' else 0)

# Save the combined data to a new file
df.to_csv("Exp1_Combined_analysis_data.csv", index=False)

print(f"There are {df.shape[0]} out of 600 participants left after excluding people who cheated or incorrectly answered the ball origin estimation question.")

def print_header(header):
    print(f"\n{header}\n{'-' * (50)}")

def t_tests_between_sexes(df, alpha):
    df['continue_or_quit'] = df[PREFERRED_SECOND_SURVEY].apply(lambda x: 1 if x == 'Continue STEM Track - Proceed to STEM Quiz' else 0)
    print_header("T-TESTS BETWEEN SEXES")
    for info_structure in INFO_STRUCTURES:
        print(f"\n{info_structure}:")
        if info_structure == 'all':
            data = df
        else:
            data = df[df[INFO_STRUCTURE] == info_structure]

        female_persistence = data[data['Sex'] == "Female"][PREFERRED_SECOND_SURVEY].apply(lambda x: 1 if x == 'Continue STEM Track - Proceed to STEM Quiz' else 0)
        male_persistence = data[data['Sex'] == "Male"][PREFERRED_SECOND_SURVEY].apply(lambda x: 1 if x == 'Continue STEM Track - Proceed to STEM Quiz' else 0)

        (_, p_value) = ttest_ind(female_persistence, male_persistence)
        print(f'(Female, Male) Persistence for {info_structure} info structure p-value: {round(p_value, 2)}')
        if p_value <= alpha:
            print(f'Reject: Significant difference between (Female, Male) Persistence for {info_structure}\n')
        else:
            print(f'Fail to reject: No significant difference between (Female, Male) Persistence for {info_structure}')

        print(female_persistence.mean(), male_persistence.mean())

def t_test_between_ethnicities(df, alpha):
    print_header("T-TESTS ACROSS ETHNICITY")
    for ethnicity in ETHNICITIES_SIMPLIFIED:
        for i in range(1, len(ETHNICITIES_SIMPLIFIED)):
            ethnicity2 = ETHNICITIES_SIMPLIFIED[i]
            if ethnicity != ethnicity2:
                for info_structure in INFO_STRUCTURES:
                    if info_structure == 'all':
                        data = df
                    else:
                        data = df[df[INFO_STRUCTURE] == info_structure]
                        
                    ethnicity_persistence = data[data["Ethnicity simplified"] == ethnicity]['continue_or_quit']
                    ethnicity2_persistence = data[data["Ethnicity simplified"] == ethnicity2]['continue_or_quit']
                    (_, p_value) = ttest_ind(ethnicity_persistence, ethnicity2_persistence)
                    if p_value <= alpha:
                        print(f'{info_structure} - ({ethnicity}, {ethnicity2}) p-value: {p_value}')
                        print(f'Reject: Significant difference between (ground, positive)\n')

def persistence_by_signal(df, alpha):
    df = pd.concat([pd.read_csv("Exp1_Trial_2_analysis_data.csv"),
                  pd.read_csv("Exp1_Trial_3_analysis_data.csv"),
                  pd.read_csv("Exp1_Trial_4_analysis_data.csv")])
    df['continue_or_quit'] = df[PREFERRED_SECOND_SURVEY].apply(lambda x: 1 if x == 'Continue STEM Track - Proceed to STEM Quiz' else 0)
    persistence_by_gender = df.groupby('Sex')['continue_or_quit'].mean()
    print(persistence_by_gender)

    print_header("PERSISTENCE BY SIGNAL")

    for info_structure in INFO_STRUCTURES[1:]:
        for signal in BALL_SIGNALS:
            print(f"\n({info_structure}, {signal}):")
            data = df[(df[INFO_STRUCTURE] == info_structure) & (df[BALL_COLOR] == signal)]
            female_persistence = data[data['Sex'] == 'Female']['continue_or_quit']
            male_persistence = data[data['Sex'] == 'Male']['continue_or_quit']

            (_, p_value) = ttest_ind(female_persistence, male_persistence)
            print(f'(Female, Male) persistence when given a {signal} ball signal for a {info_structure} info structure, p-value: {p_value}')
            if p_value <= alpha:
                print(f'Reject: Significant difference between (Female, Male) persistence\n')
            else:
                print(f'Fail to reject: No significant difference between (Female, Male) Persistence for {info_structure} and {signal} ball signal')
            print(f"Female: {female_persistence.mean()}, Male: {male_persistence.mean()}")
            print(f"# female participants: {female_persistence.shape[0]}, # male participants: {male_persistence.shape[0]}")

    num_red_pos = df[(df[INFO_STRUCTURE] == 'positive') & (df[BALL_COLOR] == 'red')].shape[0]
    num_black_pos = df[(df[INFO_STRUCTURE] == 'positive') & (df[BALL_COLOR] == 'black')].shape[0]
    num_red_neg = df[(df[INFO_STRUCTURE] == 'negative') & (df[BALL_COLOR] == 'red')].shape[0]
    num_black_neg = df[(df[INFO_STRUCTURE] == 'negative') & (df[BALL_COLOR] == 'black')].shape[0]
    num_red_ground = df[(df[INFO_STRUCTURE] == 'ground') & (df[BALL_COLOR] == 'red')].shape[0]
    num_black_ground = df[(df[INFO_STRUCTURE] == 'ground') & (df[BALL_COLOR] == 'black')].shape[0]

    print(f"(Positive skew) Number of red signals: {num_red_pos}, Number of black signals: {num_black_pos}")
    print(f"(Negative skew) Number of red signals: {num_red_neg}, Number of black signals: {num_black_neg}")
    print(f"(Ground truth) Number of red signals: {num_red_ground}, Number of black signals: {num_black_ground}")

def t_tests(df, alpha, filter_by=None):
    if filter_by is None:
        data = df
    else:
        data = df[filter_by]
    ground_persistence = data[data[INFO_STRUCTURE] == 'ground']['continue_or_quit']
    positive_persistence = data[data[INFO_STRUCTURE] == 'positive']['continue_or_quit']
    negative_persistence = data[data[INFO_STRUCTURE] == 'negative']['continue_or_quit']

    (_, p_value) = ttest_ind(ground_persistence, positive_persistence)
    print(f'(Ground Truth, Positively Skewed) p-value: {p_value}')
    if p_value <= alpha:
        print(f'Reject: Significant difference between (ground, positive)\n')

    (_, p_value) = ttest_ind(ground_persistence, negative_persistence)
    print(f'(Ground Truth, Negatively Skewed) p-value: {p_value}')
    if p_value <= alpha:
        print('Reject: Significant difference between (ground, negative)\n')

    (_, p_value) = ttest_ind(positive_persistence, negative_persistence)
    print(f'(Positively Skewed, Negatively Skewed) p-value: {p_value}')
    if p_value <= alpha:
        print('Reject: Significant difference between (positive, negative)\n')

# OVERCONFIDENCE
def t_test_overplacement_between_genders(df, alpha):
    print_header("OVERPLACEMENT BETWEEN GENDERS")

    total_participants = df.shape[0]
    df['rank'] = df[STEM_QUIZ_1_SCORE].rank(ascending=False, method='min')
    df['P_i'] = (total_participants - df['rank'] + 1) / total_participants * 100
    df['O_i'] = df[OVERPLACEMENT] - df['P_i']

    # Split data into male and female groups
    O_M = df[df['Sex'] == 'Male']['O_i']
    O_F = df[df['Sex'] == 'Female']['O_i']

    # Perform t-test
    (_, p_value) = ttest_ind(O_M, O_F)
    print(f'(Female, Male) Overplacement, p-value: {p_value} w/ average Female Overplacment = {O_F.mean()} and average Male Overplacement = {O_M.mean()}')
    if p_value <= alpha:
        print(f'Reject: Significant difference between (Female, Male) Overplacement \n')
    else:
        print(f'Fail to reject: No significant difference between (Female, Male) Overplacment')


    # Regression analysis
    df['Binary_Gender'] = df['Sex'].map({'Male': 1, 'Female': 0})
    df = df.rename(columns={'Section_1.1.player.stem_quiz_1_score': 'STEM_QUIZ_1_SCORE'})

    model = smf.ols(formula=f"O_i ~ Binary_Gender + STEM_QUIZ_1_SCORE", data=df).fit()
    
    print(model.summary())

def t_test_performance_between_genders(df, alpha):
    print_header("PERFORMANCE BETWEEN GENDERS")
    female_scores = df[df['Sex'] == 'Female'][STEM_QUIZ_1_SCORE]
    male_scores = df[df['Sex'] == 'Male'][STEM_QUIZ_1_SCORE]
    (_, p_value) = ttest_ind(female_scores, male_scores)

    print(f'(Female, Male) STEM Quiz 1 Score, p-value: {p_value} w/ average Female Score = {female_scores.mean()} and average Male Score = {male_scores.mean()}')
    if p_value <= alpha:
        print(f'Reject: Significant difference between (Female, Male) Scores \n')
    else:
        print(f'Fail to reject: No significant difference between (Female, Male) Scores')

def t_test_overestimation_between_genders(df, alpha):
    print_header("OVERESTIMATION BETWEEN GENDERS")
    
    df['Overestimation_i'] = df[OVERESTIMATION] - (df[STEM_QUIZ_1_SCORE] * 10)

    # Split data into male and female groups
    Overestimation_Male = df[df['Sex'] == 'Male']['Overestimation_i']
    Overestimation_Female = df[df['Sex'] == 'Female']['Overestimation_i']

    # Perform t-test
    (_, p_value) = ttest_ind(Overestimation_Male, Overestimation_Female)
    print(f'(Female, Male) Overestimation, p-value: {p_value} w/ average Female Overestimation = {Overestimation_Female.mean()} and average Male Overestimation = {Overestimation_Male.mean()}')
    if p_value <= alpha:
        print(f'Reject: Significant difference between (Female, Male) Overestimation \n')
    else:
        print(f'Fail to reject: No significant difference between (Female, Male) Overestimation')

    # Regression analysis
    df = df.rename(columns={'Section_1.1.player.stem_quiz_1_score': 'STEM_QUIZ_1_SCORE'})

    model = smf.ols(formula=f"Overestimation_i ~ Binary_Gender + STEM_QUIZ_1_SCORE", data=df).fit()
    
    print(model.summary())

def overestimation(df):
    female = df[df['Sex'] == 'Female']
    male = df[df['Sex'] == 'Male']
    overestimation_female = female[OVERESTIMATION] - male[STEM_QUIZ_1_SCORE]
    overestimation_male = male[OVERESTIMATION] - male[STEM_QUIZ_1_SCORE]
    print(f"On average female participants overestimate their score by: {overestimation_female.mean()}")
    print(f"On average male participants overestimate their score by: {overestimation_male.mean()}")

def run_t_tests(df, alpha):
    print_header("T-TESTS")
    t_tests(df, alpha)
    for sex in SEXES:
        print(f"\n{sex}: ")
        t_tests(df, alpha, filter_by=(df['Sex'] == sex))
    for ethnicity in ETHNICITIES_SIMPLIFIED:
        print(f"\n{ethnicity}:")
        t_tests(df, alpha, filter_by=(df['Ethnicity simplified'] == ethnicity))
    for ethnicity in ETHNICITIES_SIMPLIFIED:
        for sex in SEXES:
            print(f"\n({ethnicity}, {sex}): ")
            t_tests(df, alpha, filter_by=(df['Ethnicity simplified'] == ethnicity) & (df['Sex'] == sex))

    t_test_overplacement_between_genders(df, alpha)
    t_test_performance_between_genders(df, alpha)
    t_test_overestimation_between_genders(df, alpha)
    overestimation(df)
    t_test_between_ethnicities(df, alpha)

def run_average_persistence_per_info_structure(ax):
    print_header("AVERAGE PERSISTENCE PER INFO STRUCTURE")
    
    average_persistence_by_info_structure = df.groupby(INFO_STRUCTURE)[PREFERRED_SECOND_SURVEY].apply(lambda x: (x == 'Continue STEM Track - Proceed to STEM Quiz').mean())
    # print(average_persistence_by_info_structure)

    avg_persistence = pd.DataFrame(columns=['Group', 'Ground', 'Positive', 'Negative'])

    for sex in SEXES:
        persistence_per_structure = df[df['Sex'] == sex].groupby(INFO_STRUCTURE)[PREFERRED_SECOND_SURVEY].apply(lambda x: (x == 'Continue STEM Track - Proceed to STEM Quiz').mean())

        new_row = pd.DataFrame([{
            'Group': sex,
            'Ground': persistence_per_structure['ground'] if 'ground' in persistence_per_structure else None,
            'Positive': persistence_per_structure['positive'] if 'positive' in persistence_per_structure else None,
            'Negative':persistence_per_structure['negative'] if 'negative' in persistence_per_structure else None,
        }])

        avg_persistence = pd.concat([avg_persistence, new_row], ignore_index=True)

    for ethnicity in ETHNICITIES_SIMPLIFIED:
        persistence_per_structure = df[df['Ethnicity simplified'] == ethnicity].groupby(INFO_STRUCTURE)['continue_or_quit'].mean()
        new_row = pd.DataFrame([{
            'Group': ethnicity,
            'Ground': persistence_per_structure['ground'] if 'ground' in persistence_per_structure else None,
            'Positive': persistence_per_structure['positive'] if 'positive' in persistence_per_structure else None,
            'Negative':persistence_per_structure['negative'] if 'negative' in persistence_per_structure else None,
        }])

        avg_persistence = pd.concat([avg_persistence, new_row], ignore_index=True)

    for ethnicity in ETHNICITIES_SIMPLIFIED:
        for sex in SEXES:
            persistence_per_structure = df[((df['Sex'] == sex) & (df['Ethnicity simplified'] == ethnicity))].groupby(INFO_STRUCTURE)['continue_or_quit'].mean()

            new_row = pd.DataFrame([{
                'Group': f"{ethnicity}, {sex}",
                'Ground': persistence_per_structure['ground'] if 'ground' in persistence_per_structure else None,
                'Positive': persistence_per_structure['positive'] if 'positive' in persistence_per_structure else None,
                'Negative':persistence_per_structure['negative'] if 'negative' in persistence_per_structure else None,
            }])

            avg_persistence = pd.concat([avg_persistence, new_row], ignore_index=True)
    
    avg_persistence.replace(0, 0.005, inplace=True)
    groups = avg_persistence['Group']
    ground = avg_persistence['Ground']
    positive = avg_persistence['Positive']
    negative = avg_persistence['Negative']

    n_groups = len(groups)

    index = np.arange(n_groups)

    bar_width = 0.2

    ax.bar(index, ground, bar_width, color='b', label='Ground')
    ax.bar(index + bar_width, positive, bar_width, color='g', label='Positive')
    ax.bar(index + 2 * bar_width, negative, bar_width, color='r', label='Negative')

    ax.set_xlabel('Group', fontsize=8)
    ax.set_ylabel('Persistence', fontsize=8)
    ax.set_title('Persistence by Group and Type', fontsize=8)
    ax.set_xticks(index + bar_width, groups, rotation=90, fontsize=8)
    ax.legend()

def risk_tolerant_level(row):
    for i in range(1, 12):
        question_name = RISK_TOLERANCE + str(i)
        if row[question_name] == "C":
            return i
    return 12

def risk_tolerant_or_averse(row):
    for i in range(1, 12):
        question_name = RISK_TOLERANCE + str(i)
        if row[question_name] == "C":
            if i <= 5: # Would you rather have 50% chance of $10 or $5?
                return 'risk_averse'
            return 'risk_tolerant'
    return 'risk_tolerant'

def chi_squared_test(df, alpha):
    df['risk_averse_or_tolerant'] = df.apply(lambda row: risk_tolerant_or_averse(row), axis=1)
    df['risk_tolerance_level'] = df.apply(lambda row: risk_tolerant_level(row), axis=1)
    continue_and_bet = sum((df['continue_or_quit'] == 1) & (df['risk_averse_or_tolerant'] == 'risk_tolerant'))
    continue_and_fixed = sum((df['continue_or_quit'] == 1) & (df['risk_averse_or_tolerant'] == 'risk_averse'))
    quit_and_bet = sum((df['continue_or_quit'] == 0) & (df['risk_averse_or_tolerant'] == 'risk_tolerant'))
    quit_and_fixed = sum((df['continue_or_quit'] == 0) & (df['risk_averse_or_tolerant'] == 'risk_averse'))

    contingency_table = np.array([[continue_and_bet, quit_and_bet], [continue_and_fixed, quit_and_fixed]])

    print(contingency_table)

    chi2, p, dof, expected = chi2_contingency(contingency_table)
    print(f'The p-value for the Chi-squared test is {p}')
    if p <= alpha:
        print('Reject the null hypothesis - there is no signficant association between persistence and risk preference')
    else:
        print('Fail to reject the null hypothesis - there is a significant association between persistence and risk preference')

# RISK TOLERANCE
def risk_tolerance(ax):
    print_header("RISK TOLERANCE")
    risk = pd.DataFrame(columns=['Group', 'Ground', 'Positive', 'Negative'])

    for sex in SEXES:
        persistence_per_structure = df[df['Sex'] == sex].groupby('risk_averse_or_tolerant')

        num_risk = persistence_per_structure['risk_averse_or_tolerant'].count()
        mean_risk_averse = num_risk['risk_averse'] / (num_risk['risk_averse'] + num_risk['risk_tolerant'])
        mean_risk_tolerant = 1 - mean_risk_averse

        new_row = pd.DataFrame([{
            'Group': sex,
            'Risk Averse': mean_risk_averse,
            'Risk Tolerant': mean_risk_tolerant
        }])

        risk = pd.concat([risk, new_row], ignore_index=True)

    for ethnicity in ETHNICITIES_SIMPLIFIED:
        persistence_per_structure = df[df['Ethnicity simplified'] == ethnicity].groupby('risk_averse_or_tolerant')

        num_risk = persistence_per_structure['risk_averse_or_tolerant'].count()
        mean_risk_averse = num_risk['risk_averse'] / (num_risk['risk_averse'] + num_risk['risk_tolerant'])
        mean_risk_tolerant = 1 - mean_risk_averse

        new_row = pd.DataFrame([{
            'Group': ethnicity,
            'Risk Averse': mean_risk_averse,
            'Risk Tolerant': mean_risk_tolerant
        }])

        risk = pd.concat([risk, new_row], ignore_index=True)

    for ethnicity in ETHNICITIES_SIMPLIFIED:
        for sex in SEXES:
            persistence_per_structure = df[(df['Ethnicity simplified'] == ethnicity) & (df['Sex'] == sex)].groupby('risk_averse_or_tolerant')
            
            num_risk = persistence_per_structure['risk_averse_or_tolerant'].count()
            mean_risk_averse = num_risk['risk_averse'] / (num_risk['risk_averse'] + num_risk['risk_tolerant'])
            mean_risk_tolerant = 1 - mean_risk_averse
            new_row = pd.DataFrame([{
                'Group': f'{ethnicity}, {sex}',
                'Risk Averse': mean_risk_averse,
                'Risk Tolerant': mean_risk_tolerant
            }])
            risk = pd.concat([risk, new_row], ignore_index=True)
    # print each row in the risk dataframe with the group and the risk averse and risk tolerant values

    risk.replace(0, 0.005, inplace=True)
    groups = risk['Group']
    risk_tolerant = risk['Risk Tolerant']
    risk_averse = risk['Risk Averse']

    n_groups = len(groups)

    index = np.arange(n_groups)

    bar_width = 0.2

    ax.bar(index, risk_tolerant, bar_width, color='b', label='Risk Tolerant')
    ax.bar(index + bar_width, risk_averse, bar_width, color='g', label='Risk Averse')

    ax.set_xlabel('Group', fontsize=8)
    ax.set_ylabel('Risk Preference', fontsize=8)
    ax.set_title('Risk Preferences by Demographic', fontsize=8)
    ax.set_xticks(index + bar_width, groups, rotation=90, fontsize=8)
    ax.legend(fontsize=8)
    ax.legend()
    
def risk_tolerance_persistence(ax):
    risk_level = pd.DataFrame(columns=['Risk Level', 'Persistence Rate'])
    for i in range(1, 12):
        # For each risk level, calculate the persistence rate
        persistence_rate = df[df['risk_tolerance_level'] == i].groupby('continue_or_quit')['continue_or_quit'].count().get(1, 0) / df[df['risk_tolerance_level'] == i].shape[0]
       
        risk_level = risk_level._append({'Risk Level': i, 'Persistence Rate': persistence_rate}, ignore_index=True)

    risk_level.replace(0, 0.005, inplace=True)

    risk_levels = risk_level['Risk Level']
    persistence_rate = risk_level['Persistence Rate']

    n_groups = len(risk_levels)

    index = np.arange(n_groups)

    bar_width = 0.2

    ax.bar(index, persistence_rate, bar_width, color='b')

    ax.set_xlabel('Risk Level', fontsize=8)
    ax.set_ylabel('Persistence Rate', fontsize=8)
    ax.set_title('Persistence Rate by Risk Level', fontsize=8)
    ax.set_xticks(index + bar_width / 2, risk_levels, rotation=90, fontsize=8)
    ax.legend(fontsize=8)
    ax.legend()

def risk_tolerance_by_group(ax):
    risk_level = pd.DataFrame(columns=['Group', 'Risk Tolerant'])

    for sex in SEXES:
        num_risk = df[df['Sex'] == sex].groupby('risk_averse_or_tolerant').size()
        mean_risk_tolerant = num_risk.get('risk_tolerant', 0) / num_risk.sum()
        risk_level = risk_level._append({'Group': sex, 'Risk Tolerant': mean_risk_tolerant}, ignore_index=True)

    for ethnicity in ETHNICITIES_SIMPLIFIED:
        num_risk = df[df['Ethnicity simplified'] == ethnicity].groupby('risk_averse_or_tolerant').size()
        mean_risk_tolerant = num_risk.get('risk_tolerant', 0) / num_risk.sum()
        risk_level = risk_level._append({'Group': ethnicity, 'Risk Tolerant': mean_risk_tolerant}, ignore_index=True)

    for ethnicity in ETHNICITIES_SIMPLIFIED:
        for sex in SEXES:
            num_risk = df[(df['Sex'] == sex) & (df['Ethnicity simplified'] == ethnicity)].groupby('risk_averse_or_tolerant').size()
            mean_risk_tolerant = num_risk.get('risk_tolerant', 0) / num_risk.sum()
            risk_level = risk_level._append({'Group': f'{ethnicity}, {sex}', 'Risk Tolerant': mean_risk_tolerant}, ignore_index=True)

    groups = risk_level['Group']
    risk_tolerant = risk_level['Risk Tolerant']

    n_groups = len(groups)

    index = np.arange(n_groups)

    bar_width = 0.2

    ax.bar(index, risk_tolerant, bar_width, color='b', label='Risk Tolerant')

    ax.set_xlabel('Group', fontsize=8)
    ax.set_ylabel('Risk Preference', fontsize=8)
    ax.set_title('Risk Preferences by Demographic', fontsize=8)
    ax.set_xticks(index + bar_width, groups, rotation=90, fontsize=8)
    ax.legend(fontsize=8)
    ax.legend()

def run_all_tests(df):  
    persistence_by_gender = df.groupby('Sex')['continue_or_quit'].mean()
    print(persistence_by_gender)

    # Persistence by ethnicity
    persistence_by_ethnicity = df.groupby('Ethnicity simplified')['continue_or_quit'].mean()
    print(persistence_by_ethnicity)

    # Persistence by ethnicity and sex
    peristence_by_ethnicity_and_sex = df.groupby(['Sex', 'Ethnicity simplified'])['continue_or_quit'].mean()
    print(peristence_by_ethnicity_and_sex)

    # t_tests_between_sexes(df, 0.05)
    persistence_by_signal(df, 0.05)
    run_t_tests(df, 0.05)
    # chi_squared_test(df, 0.05)

    # fig, axs = plt.subplots(2, 2, figsize=(10, 8))
    # plt.rcParams.update({'font.size': 8})
    # run_average_persistence_per_info_structure(axs[0, 0])
    # risk_tolerance(axs[0, 1])
    # risk_tolerance_persistence(axs[1, 0])
    # risk_tolerance_by_group(axs[1, 1])

    # fig.subplots_adjust(hspace=0.5, wspace=0.5)
    # plt.show()

run_all_tests(df)