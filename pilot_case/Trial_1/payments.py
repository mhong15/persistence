import pandas as pd
from scipy.stats import ttest_ind
import random
import os

OTREE_DATA = "Exp2_Trial_1.csv"
DEMOGRAPHIC_DATA = "Exp2_Trial_1_demographics.csv"

PROLIFIC_ID = "Exp2_Intro.1.player.prolific_id"
STEM_QUIZ_1 = "Exp2_Section_1.1.player.question"
STEM_QUIZ_1_ANSWERS = "Exp2_Section_1.1.player.stem_quiz_1_answers"
STEM_QUIZ_1_SCORE = "Exp2_Section_1.1.player.stem_quiz_1_score"
SECTION_1_NUM_TAB_SWITCHES = "Exp2_Section_1.1.player.num_tab_switches_in_section_11"
PREFERRED_INFO_STRUCTURE = "Exp2_Section_2_3.1.player.preferred_info_structure"
SECTION_1_TIME_HIDDEN = "Exp2_Section_1.1.player.total_time_hidden_in_section_1"

PLAYER_PERFORMANCE = "Exp2_Section_2_3.1.player.performance"
OVERPLACEMENT = "Exp2_Section_2_3.1.player.overplacement"
OVERESTIMATION = "Exp2_Section_2_3.1.player.overestimation"
PASSING_THRESHOLD = "Exp2_Section_2_3.1.player.passing_threshold"
BALL_ORIGIN_ESTIMATION = "Exp2_Section_2_3.1.player.ball_origin_estimation"
BALL_COLOR = "Exp2_Section_2_3.1.player.ball_color"

class Payment_Calculator:
    SECTION_1 = 1
    SECTION_2 = 2

    bonus_payment_sections = [SECTION_1, SECTION_2]
    weights = [0.5, 0.5]

    def __init__(self, df):
        self.df = df
        self.payment_df = None

    def calculate_all_payments(self):
        self.payment_df = pd.DataFrame(columns=['ID', '#'])
        for row in range(self.df.index.size):
            (section, bonus) = self.calculate_bonus_section(row)
            prolific_id = self.df[PROLIFIC_ID][row]
            self.payment_df = self.payment_df._append({'ID': prolific_id, '#': bonus}, ignore_index=True)
        return self.payment_df
    
    def calculate_bonus_section(self, index):
            bonus_section = random.choices(self.bonus_payment_sections, weights=self.weights, k=1)[0]
            match bonus_section:
                case Payment_Calculator.SECTION_1:
                    return (bonus_section, self.calculate_bonus_section_1(index))
                case Payment_Calculator.SECTION_2:
                    return (bonus_section, self.calculate_bonus_section_2(index))
            return -1

    def calculate_bonus_section_1(self, index, question=None):
        if pd.isna(self.df[STEM_QUIZ_1_SCORE][index]):
            return 0
        if question == None:
            question = random.randint(1, 10)
        parent_directory = os.path.dirname(os.getcwd())
        section_1_answer_key = pd.read_csv(parent_directory + '/Exp2_Section_1.csv')

        participant_answer = (self.df[STEM_QUIZ_1 + str(question)][index])
        correct_answer = section_1_answer_key['correct_answer'][question - 1]
        if participant_answer == correct_answer:
            return 2
        return 0
    
    def calculate_bonus_section_2(self, index):
        random_question = random.randint(1, 3)

        match random_question:
            case 1:
                return self.calculate_bonus_section_2_question_1(index)
            case 2:
                return self.calculate_bonus_section_2_question_2(index)
            case 3:
                return self.calculate_bonus_section_2_question_3(index)
        return 0
    
    def calculate_bonus_section_2_question_1(self, index):
        p = random.randint(0, 100)
        overplacement = self.df[OVERPLACEMENT][index]
        if pd.isna(self.df[OVERPLACEMENT][index]):
            return 0
        if p < int(overplacement):
            random_participant = self.df.sample()
            participant_score = self.df[STEM_QUIZ_1_SCORE][index]
            random_participant_score = random_participant[STEM_QUIZ_1_SCORE].values[0]
            if  participant_score >= random_participant_score:
                return 2
            return 0
        r = random.randint(0, 100)
        if r < p:
            return 2
        return 0
    
    def calculate_bonus_section_2_question_2(self, index):
        if pd.isna(self.df[OVERESTIMATION][index]):
            return 0
        if self.df[OVERESTIMATION][index] == self.df[STEM_QUIZ_1_SCORE][index] * 10:
            
            return 2
        return 0
    
    def calculate_bonus_section_2_question_3(self, index):
        if pd.isna(self.df[STEM_QUIZ_1_SCORE][index]):
            return 0
        c = self.df[STEM_QUIZ_1_SCORE][index] * 10
        g = self.df[PASSING_THRESHOLD][index]

        if pd.isna(g):
            return 0
        return (max(100 - abs(c - g), 0) / 100) * 2

df = pd.read_csv('Exp2_Trial_1_cleaned_data.csv')

payment_calculator = Payment_Calculator(df)
all_payments = payment_calculator.calculate_all_payments()

# Save the payments to a csv file
all_payments.to_csv('Exp2_Trial_1_payments.csv', index=False)
df.head(5).to_csv("Exp2_Trial_1_payments_test.csv", index=False)
