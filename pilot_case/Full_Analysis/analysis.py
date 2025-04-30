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

df['continue_or_quit'] = df[PREFERRED_SECOND_SURVEY].apply(lambda x: 1 if x == 'STEM Track' else 0)

df.to_csv("Exp1_Combined_analysis_data.csv", index=False)

print(f"There are {df.shape[0]} out of 600 participants left after excluding people who cheated or incorrectly answered the ball origin estimation question.")

class T_TESTS:
    def __init__(self, df, is_print=False):
        self.df = df
        self.is_print = is_print
        self.alpha = 0.05

    def mean_to_percent(self, mean):
         return f"{round(mean * 100, 2)}%"
    
    def t_test_between_info_structure(self, filter_by, group_description):
        for (info1, info2) in INFO_STRUCTURE_PAIRS:
            data = self.df[filter_by]
            
            info1_persistence = data[data[INFO_STRUCTURE] == info1]['continue_or_quit']
            info2_persistence = data[data[INFO_STRUCTURE] == info2]['continue_or_quit']
            
            (_, p_value) = ttest_ind(info1_persistence, info2_persistence)

            if self.is_print:
                print(f'({group_description}, {INFO_STRUCTURE_STRING[info1]}, {INFO_STRUCTURE_STRING[info2]}) p-value: {round(p_value, 2)}, ({self.mean_to_percent(info1_persistence.mean())}, {self.mean_to_percent(info2_persistence.mean())})')
                
            if p_value <= self.alpha:
                print(f'  - Reject: Significant difference between average persistence({group_description}, {INFO_STRUCTURE_STRING[info1]}, {INFO_STRUCTURE_STRING[info2]}), ({self.mean_to_percent(info1_persistence.mean())}, {self.mean_to_percent(info2_persistence.mean())})\n')

    def t_test_between_groups(self, group, arg1, arg2, info_structure=None, ball_signal=None):
        if info_structure is None or info_structure == 'all':
            data = self.df
        else:
            data = self.df[self.df[INFO_STRUCTURE] == info_structure]

        if ball_signal is not None:
            data = data[data[BALL_COLOR] == ball_signal]
        
        arg1_data = data[data[group] == arg1]['continue_or_quit']
        arg2_data = data[data[group] == arg2]['continue_or_quit']

        (_, p_value) = ttest_ind(arg1_data, arg2_data)

        group_description = arg1 + ", " + arg2 + (f", {info_structure}" if info_structure is not None else "") + (f", {ball_signal}" if ball_signal is not None else "")

        if self.is_print:
            print(f'({group_description}) p-value: {round(p_value, 2)}, ({self.mean_to_percent(arg1_data.mean())}, {self.mean_to_percent(arg2_data.mean())})')
            
        if p_value <= self.alpha:
            print(f'  - Reject: Significant difference between average persistence of ({group_description}), ({self.mean_to_percent(arg1_data.mean())}, {self.mean_to_percent(arg2_data.mean())})\n')
        
    def t_test_between_sexes(self):
        print_header("T-TESTS BETWEEN SEXES")
        for info_structure in INFO_STRUCTURES:
            self.t_test_between_groups(group="Sex", arg1="Female", arg2="Male", info_structure=info_structure)

    def t_test_between_ethnicities(self):
        print_header("T-TESTS BETWEEN ETHNICITY")
        for (ethnicity, ethnicity2) in ETHNICITIES_PAIRED:
            for info_structure in INFO_STRUCTURES:
                self.t_test_between_groups(group="Ethnicity simplified", arg1=ethnicity, arg2=ethnicity2, info_structure=info_structure)

    def t_test_between_sexes_and_ethnicities(self):
        print_header("T-TESTS BETWEEN SEX AND ETHNICITY")

        for ethnicity in ETHNICITIES_SIMPLIFIED:
            for sex in SEXES:
                self.t_test_between_info_structure(((self.df["Ethnicity simplified"] == ethnicity) & (self.df["Sex"] == sex)), group_description=f"{ethnicity} {sex}")
    
    def t_test_persistence_by_signal(self, group, arg1, arg2):
        for info_structure in INFO_STRUCTURES[1:]: # Exclude 'all'
            for signal in BALL_SIGNALS:
                self.t_test_between_groups(group, arg1, arg2, info_structure, signal)

    def t_test_persistence_by_signal_sex(self):
        print_header("PERSISTENCE BY SIGNAL AND SEX")
        self.t_test_persistence_by_signal(group="Sex", arg1="Female", arg2="Male")

    def t_test_persistence_by_signal_ethnicity(self):
        print_header("PERSISTENCE BY SIGNAL and ETHNICITY")
        for (ethnicity, ethnicity2) in ETHNICITIES_PAIRED:
            self.t_test_persistence_by_signal(group="Ethnicity simplified", arg1=ethnicity, arg2=ethnicity2)

    def run_t_tests(self):
        # self.t_test_between_sexes()
        # self.t_test_between_ethnicities()
        # self.t_test_between_sexes_and_ethnicities()
        
        # self.t_test_persistence_by_signal_sex()
        # self.t_test_persistence_by_signal_ethnicity()

        print_header("T-TESTS BETWEEN INFO STRUCTURES")
        for sex in SEXES:
            self.t_test_between_info_structure((self.df["Sex"] == sex), group_description=f"{sex}")
        for ethnicity in ETHNICITIES_SIMPLIFIED:
            self.t_test_between_info_structure((self.df["Ethnicity simplified"] == ethnicity), group_description=f"{ethnicity}")
        for ethnicity in ETHNICITIES_SIMPLIFIED:
            for sex in SEXES:
                self.t_test_between_info_structure(((self.df["Ethnicity simplified"] == ethnicity) & (self.df["Sex"] == sex)), group_description=f"{ethnicity} {sex}")
                                          

class OVERCONFIDENCE:
    def __init__(self, df, is_print=False):
        self.df = df
        self.alpha = 0.05
        self.is_print = is_print

        self.overplacement_setup()
        self.overestimation_setup()

    def mean_to_percent(self, mean):
         return f"{round(mean * 100, 2)}%"
    
    def overplacement_setup(self):
        total_participants = self.df.shape[0]
        self.df['rank'] = self.df[STEM_QUIZ_1_SCORE].rank(ascending=False, method='min')
        self.df['P_i'] = (total_participants - self.df['rank'] + 1) / total_participants * 100
        self.df['Overplacement'] = self.df[OVERPLACEMENT] - self.df['P_i']

        self.df['Binary_Gender'] = self.df['Sex'].map({'Male': 1, 'Female': 0})
        self.df = self.df.rename(columns={'Section_1.1.player.stem_quiz_1_score': 'STEM_QUIZ_1_SCORE'})

    def overestimation_setup(self):
        self.df['Overestimation'] = self.df[OVERESTIMATION] - (self.df['STEM_QUIZ_1_SCORE'] * 10)

    def t_test(self, group, arg1, arg2, overconfidence_measure):
        arg1_data = self.df[self.df[group] == arg1][overconfidence_measure]
        arg2_data = self.df[self.df[group] == arg2][overconfidence_measure]

        (_, p_value) = ttest_ind(arg1_data, arg2_data)

        group_description = arg1 + ", " + arg2

        if self.is_print:
            print(f'({group_description}) p-value: {round(p_value, 2)}, ({round(arg1_data.mean(), 2)}, {round(arg2_data.mean(), 2)})')
            
        if p_value <= self.alpha:
            print(f'  - Reject: Significant difference between average {overconfidence_measure.lower()} of ({group_description}), ({round(arg1_data.mean(), 2)}, {round(arg2_data.mean(), 2)})\n')

    def t_test_overplacement_between_sex(self):
        print_header("OVERPLACEMENT BETWEEN SEX")
        self.t_test(group='Sex', arg1='Female', arg2='Male', overconfidence_measure='Overplacement')

    def t_test_overplacement_between_ethnicity(self):
        print_header("OVERPLACEMENT BETWEEN ETHNICITY")
        for (ethnicity, ethnicity2) in ETHNICITIES_PAIRED:
            self.t_test(group='Ethnicity simplified', arg1=ethnicity, arg2=ethnicity2, overconfidence_measure='Overplacement')

    def regression_analysis_overplacement_between_sex(self):
        model = smf.ols(formula=f"Overplacement ~ Binary_Gender + STEM_QUIZ_1_SCORE", data=self.df).fit()

        print_header(f"OVERPLACEMENT REGRESSION ANALYSIS FOR (FEMALE, MALE):")
        print(model.summary())

    def regression_analysis_overplacement_between_ethnicities(self):
       
       for (ethnicity, ethnicity2) in ETHNICITIES_PAIRED:
            print_header(f"OVERPLACEMENT REGRESSION ANALYSIS FOR ({ethnicity.capitalize()}, {ethnicity2.capitalize()}):")

            self.df['Binary_Ethnicity'] = self.df['Ethnicity simplified'].map({ethnicity: 1, ethnicity2: 0})

            data = self.df[(self.df["Ethnicity simplified"] == ethnicity) |
                            (self.df["Ethnicity simplified"] == ethnicity2)]

            model = smf.ols("Overplacement ~ Binary_Ethnicity + STEM_QUIZ_1_SCORE", data=data).fit()
            
            print(model.summary())
        
    def t_test_overestimation_between_sex(self):
        print_header("OVERESTIMATION BETWEEN SEX")

        self.t_test(group='Sex', arg1='Female', arg2='Male', overconfidence_measure='Overestimation')

    def t_test_overestimation_between_ethnicity(self):
        print_header("OVERESTIMATION BETWEEN ETHNICITY")
        for (ethnicity, ethnicity2) in ETHNICITIES_PAIRED:
            self.t_test(group='Ethnicity simplified', arg1=ethnicity,arg2=ethnicity2, overconfidence_measure='Overestimation')

    def regression_analysis_overestimation_between_sex(self):
        model = smf.ols(formula=f"Overestimation ~ Binary_Gender + STEM_QUIZ_1_SCORE", data=self.df).fit()

        print_header(f"Overestimation Regression Analysis for (Female, Male):")
        print(model.summary())

    def regression_analysis_overestimation_between_ethnicities(self):
        for (ethnicity, ethnicity2) in ETHNICITIES_PAIRED:
            print_header(f"OVERESTIMATION REGRESSION ANALYSIS FOR ({ethnicity.capitalize()}, {ethnicity2.capitalize()}):")

            self.df['Binary_Ethnicity'] = self.df['Ethnicity simplified'].map({ethnicity: 1, ethnicity2: 0})

            data = self.df[(self.df["Ethnicity simplified"] == ethnicity) |
                            (self.df["Ethnicity simplified"] == ethnicity2)]
            
            model = smf.ols("Overestimation ~ Binary_Ethnicity + STEM_QUIZ_1_SCORE", data=data).fit()
            print(model.summary())

    def run_tests(self):
        self.t_test_overplacement_between_sex()
        self.t_test_overplacement_between_ethnicity()
        self.regression_analysis_overplacement_between_sex()
        self.regression_analysis_overplacement_between_ethnicities()

        self.t_test_overestimation_between_sex()
        self.t_test_overestimation_between_ethnicity()
        self.regression_analysis_overestimation_between_sex()
        self.regression_analysis_overestimation_between_ethnicities()

class RISK:
    def __init__(self, df, is_print=False):
        self.df = df
        self.alpha = 0.05
        self.is_print = is_print
        self.bar_width = 0.25

    def risk_tolerant_level(self, row):
        for i in range(1, 12):
            question_name = RISK_TOLERANCE + str(i)
            if row[question_name] == "C":
                return i
        return 12

    def risk_tolerant_or_averse(self, row):
        for i in range(1, 12):
            question_name = RISK_TOLERANCE + str(i)
            if row[question_name] == "C":
                if i <= 5: # Would you rather have 50% chance of $10 or $5?
                    return 'risk_averse'
                return 'risk_tolerant'
        return 'risk_tolerant'

    def chi_squared_test(self, alpha):
        self.df['risk_averse_or_tolerant'] = df.apply(lambda row: self.risk_tolerant_or_averse(row), axis=1)

        self.df['risk_tolerance_level'] = df.apply(lambda row: self.risk_tolerant_level(row), axis=1)

        continue_and_bet = sum((df['continue_or_quit'] == 1) & (df['risk_averse_or_tolerant'] == 'risk_tolerant'))
        continue_and_fixed = sum((df['continue_or_quit'] == 1) & (df['risk_averse_or_tolerant'] == 'risk_averse'))
        quit_and_bet = sum((df['continue_or_quit'] == 0) & (df['risk_averse_or_tolerant'] == 'risk_tolerant'))
        quit_and_fixed = sum((df['continue_or_quit'] == 0) & (df['risk_averse_or_tolerant'] == 'risk_averse'))

        contingency_table = np.array([[continue_and_bet, quit_and_bet], [continue_and_fixed, quit_and_fixed]])

        chi2, p, dof, expected = chi2_contingency(contingency_table)
        print(f'The p-value for the Chi-squared test is {p}')
        if p <= alpha:
            print('Reject the null hypothesis - there is no signficant association between persistence and risk preference')
        else:
            print('Fail to reject the null hypothesis - there is a significant association between persistence and risk preference')

    def construct_risk_tolerance_row(self, group, group_by):
        num_risk_averse_and_tolerant = self.df[group_by].groupby('risk_averse_or_tolerant').size()

        num_risk_averse = num_risk_averse_and_tolerant['risk_averse']
        num_risk_tolerant = num_risk_averse_and_tolerant['risk_tolerant']

        mean_risk_averse = num_risk_averse / (num_risk_averse + num_risk_tolerant)
        mean_risk_tolerant = 1 - mean_risk_averse

        new_row = pd.DataFrame([{
            'Group': group,
            'Risk Averse': mean_risk_averse,
            'Risk Tolerant': mean_risk_tolerant
        }])

        return new_row

    def calculate_risk_tolerance(self):
        risk = pd.DataFrame(columns=['Group', 'Ground', 'Positive', 'Negative'])
        for sex in SEXES:
            risk = pd.concat([risk, self.construct_risk_tolerance_row(
                    group=sex, 
                    group_by=(self.df['Sex']==sex))], ignore_index=True)

        for ethnicity in ETHNICITIES_SIMPLIFIED:
            risk = pd.concat([risk, self.construct_risk_tolerance_row(
                    group=ethnicity, 
                    group_by=(self.df['Ethnicity simplified']==ethnicity))], ignore_index=True)

        for ethnicity in ETHNICITIES_SIMPLIFIED:
            for sex in SEXES:
                risk = pd.concat([risk, self.construct_risk_tolerance_row(
                    group=f"{ethnicity} {sex}",
                    group_by=(self.df["Ethnicity simplified"]==ethnicity) & (self.df["Sex"]==sex))], ignore_index=True)

        risk.replace(0, 0.005, inplace=True)  
        return risk

    def graph_risk_tolerance_by_group(self, ax):
        groups, risk_tolerant, risk_averse = self.risk['Group'], self.risk['Risk Tolerant'], self.risk['Risk Averse']
        n_groups = len(groups)
        index = np.arange(n_groups)

        ax.bar(index, risk_tolerant, self.bar_width, color='b', label='Risk Tolerant')
        ax.bar(
            index + self.bar_width,
            risk_averse,
            self.bar_width,
            color="g",
            label="Risk Averse",
        )

        ax.set_xlabel('Group', fontsize=8)
        ax.set_ylabel('Risk Preference', fontsize=8)
        ax.set_title('Risk Preferences by Demographic', fontsize=8)
        ax.set_xticks(index + self.bar_width, groups, rotation=90, fontsize=8)
        ax.legend(fontsize=8)
        ax.legend()

    def calculate_persistence_at_each_risk_level(self):
        persistence_by_risk_level = pd.DataFrame(
            columns=["Risk Level", "Persistence Rate"]
        )

        for i in range(1, 12):
            participants_at_risk_level = self.df[self.df["risk_tolerance_level"] == i]
            num_participants_at_risk_level = participants_at_risk_level.shape[0]
            num_persisted_participants = participants_at_risk_level.groupby("continue_or_quit")["continue_or_quit"].count().get(1, 0)

            persistence_by_risk_level = persistence_by_risk_level._append(
                {
                    "Risk Level": i,
                    "Persistence Rate": 
                        num_persisted_participants / num_participants_at_risk_level
                },
                ignore_index=True
            )
            persistence_by_risk_level.replace(0, 0.005, inplace=True)

        return persistence_by_risk_level

    def graph_persistence_by_risk_level(self, ax):
        risk_levels = self.persistence_by_risk_level["Risk Level"]
        persistence_rate = self.persistence_by_risk_level["Persistence Rate"]

        n_groups = len(risk_levels)
        index = np.arange(n_groups)

        ax.bar(index, persistence_rate, self.bar_width, color="b")

        ax.set_xlabel("Risk Level", fontsize=8)
        ax.set_ylabel("Persistence Rate", fontsize=8)
        ax.set_title("Persistence Rate by Risk Level", fontsize=8)
        ax.set_xticks(index + self.bar_width / 2, risk_levels, rotation=90, fontsize=8)
        ax.legend(fontsize=8)
        ax.legend()

    def construct_persistence_row(self, group, group_by):
        demographic = self.df[group_by].groupby(INFO_STRUCTURE)[PREFERRED_SECOND_SURVEY].apply(lambda x: (x == "STEM Track").mean())

        new_row = pd.DataFrame([{
                'Group': group,
                'Ground': demographic['ground'] if 'ground' in demographic else None,
                'Positive': demographic['positive'] if 'positive' in demographic else None,
                'Negative':demographic['negative'] if 'negative' in demographic else None,
            }])
        return new_row

    def calculate_persistence_by_group(self):
        persistence_by_group = pd.DataFrame(columns=["Group", "Persistence Rate"])

        for sex in SEXES:
            persistence_by_group = pd.concat([persistence_by_group, self.construct_persistence_row(group=sex, group_by=(self.df['Sex'] == sex))], ignore_index=True)

        for ethnicity in ETHNICITIES_SIMPLIFIED:
            persistence_by_group = pd.concat([persistence_by_group, self.construct_persistence_row(group=ethnicity, group_by=(self.df['Ethnicity simplified'] == ethnicity))], ignore_index=True)

        for ethnicity in ETHNICITIES_SIMPLIFIED:
            for sex in SEXES:
                persistence_by_group = pd.concat([persistence_by_group, self.construct_persistence_row(group=f"{ethnicity} {sex}", group_by=(self.df['Ethnicity simplified'] == ethnicity) & (self.df['Sex'] == sex))], ignore_index=True)

        persistence_by_group.replace(0, 0.005, inplace=True)
        return persistence_by_group

    def graph_persistence_by_group(self, ax):
        groups = self.persistence_by_group["Group"]
        ground = self.persistence_by_group["Ground"]
        positive = self.persistence_by_group["Positive"]
        negative = self.persistence_by_group["Negative"]

        n_groups = len(groups)
        index = np.arange(n_groups)

        ax.bar(index, ground, self.bar_width, color="b", label="Ground")
        ax.bar(
            index + self.bar_width,
            positive,
            self.bar_width,
            color="g",
            label="Positive",
        )
        ax.bar(
            index + 2 * self.bar_width,
            negative,
            self.bar_width,
            color="r",
            label="Negative",
        )

        ax.set_xlabel("Group", fontsize=8)
        ax.set_ylabel("Persistence", fontsize=8)
        ax.set_title("Persistence by Group and Type", fontsize=8)
        ax.set_xticks(index + self.bar_width, groups, rotation=90, fontsize=8)
        ax.legend()

    def run_tests(self):
        self.chi_squared_test(self.alpha)

    def graph(self):
        self.risk = self.calculate_risk_tolerance()
        self.persistence_by_risk_level = self.calculate_persistence_at_each_risk_level()
        self.persistence_by_group = self.calculate_persistence_by_group()

        fig, axs = plt.subplots(2, 2, figsize=(10, 8))
        plt.rcParams.update({'font.size': 8})
        self.graph_persistence_by_group(axs[0, 0])
        self.graph_risk_tolerance_by_group(axs[0, 1])
        self.graph_persistence_by_risk_level(axs[1, 0])

        fig.subplots_adjust(hspace=0.5, wspace=0.5)
        plt.show()


def signal_breakdown(df):
    # Prints a breakdown of the number of participants who received each signal
    # for each info structure (positive, ground, negative)
    print_header("SIGNAL BREAKDOWN")
    for info_structure in INFO_STRUCTURES:
        for signal in BALL_SIGNALS:
            num_participants = df[(df[INFO_STRUCTURE] == info_structure) & (df[BALL_COLOR] == signal)].shape[0]
            print(f"({INFO_STRUCTURE_STRING[info_structure]}, {signal}): {num_participants}")

def demographic_breakdown(df):
    # Prints a breakdown of the number of participants in each demographic group
    print_header("DEMOGRAPHIC BREAKDOWN")
    for ethnicity in ETHNICITIES_SIMPLIFIED:
        for sex in SEXES:
            num_participants = df[(df["Ethnicity simplified"] == ethnicity) & (df["Sex"] == sex)].shape[0]
            print(f"({ethnicity}, {sex}): {num_participants}")

t_tests = T_TESTS(df)
t_tests.run_t_tests()

overconfidence = OVERCONFIDENCE(df)
overconfidence.run_tests()
signal_breakdown(df)
demographic_breakdown(df)

risk_tolerance = RISK(df)
risk_tolerance.run_tests()
risk_tolerance.graph()
