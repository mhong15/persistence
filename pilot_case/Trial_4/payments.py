import pandas as pd
from scipy.stats import ttest_ind
import random
import os

OTREE_DATA = "Exp1_Trial_3.csv"
DEMOGRAPHIC_DATA = "Exp1_Trial_3_Demographics.csv"

PROLIFIC_ID = "Intro.1.player.prolific_id"
STEM_QUIZ_1 = "Section_1.1.player.question"
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
QUIZ_2_SCORE = "Section_4_5.1.player.quiz_2_score"
PREFERRED_SECOND_SURVEY = "Section_4_5.1.player.preferred_second_survey"
SECTION_5_NUM_TAB_SWITCHES = "Section_4_5.1.player.num_tab_switches_in_section_5"
SECTION_5_TIME_HIDDEN = "Section_4_5.1.player.total_time_hidden_in_section_5"
RISK_TOLERANCE = "Section_6.1.player.question"
RISK_TOLERANCE_ANSWERS = "Section_6.1.player.risk_tolerance_answers"
BALL_COLOR = "Section_2_3.1.player.ball_color"


class Payment_Calculator:
    SECTION_1 = 1
    SECTION_2 = 2
    SECTION_5 = 5
    SECTION_6 = 6

    bonus_payment_sections = [SECTION_1, SECTION_2, SECTION_5, SECTION_6]
    weights = [0.3125, 0.3125, 0.3125, 0.0625]

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
                case Payment_Calculator.SECTION_5:
                    return (bonus_section, self.calculate_bonus_section_5(index))
                case Payment_Calculator.SECTION_6:
                    return (bonus_section, self.calculate_bonus_section_6(index))
            return -1

    def calculate_bonus_section_1(self, index, question=None):
        '''
        Section 1: The STEM quiz. If this section is selected, then we will randomly select choose a question from the quiz. If the participant correctly answers the question, then they will receive the $2 bonus.
        '''
        if pd.isna(self.df[STEM_QUIZ_1_SCORE][index]):
            return 0
        # For testing purposes, I'm going to pass in a question number.
        if question == None:
            question = random.randint(1, 10)
        #   go back up one directory to find Section_1.csv
        parent_directory = os.path.dirname(os.getcwd())
        section_1_answer_key = pd.read_csv(parent_directory + '/Section_1.csv')

        participant_answer = (self.df[STEM_QUIZ_1 + str(question)][index])
        correct_answer = section_1_answer_key['correct_answer'][question - 1] # csv is 0 indexed
        if participant_answer == correct_answer:
            return 2
        return 0
    
    def calculate_bonus_section_2(self, index):
        # Choose which question to use for the bonus
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
        p = random.randint(0, 100) # Generating p
        overplacement = self.df[OVERPLACEMENT][index]
        if pd.isna(self.df[OVERPLACEMENT][index]):
            return 0
        if p < int(overplacement):
            random_participant = self.df.sample()
            random_participant_score = random_participant[STEM_QUIZ_1_SCORE].values[0]
            
            participant_score = self.df[STEM_QUIZ_1_SCORE][index]

            if  participant_score >= random_participant_score:
                return 2
            return 0
        r = random.randint(0, 100)
        if r < p:
            return 2
        return 0
    
    def calculate_bonus_section_2_question_2(self, index):
        '''
        If question 2 is selected for the bonus question and you successfully guess the number of questions you answered correctly, then you will receive the bonus payment of $2.
        '''
        if pd.isna(self.df[OVERESTIMATION][index]):
            return 0
        if self.df[OVERESTIMATION][index] == self.df[STEM_QUIZ_1_SCORE][index] * 10:
            
            return 2
        return 0
    
    def calculate_bonus_section_2_question_3(self, index):
        '''
        If question 3 is selected for the bonus question, you will earn a (max{100 - |c - g|, 0} / 100) * $2 bonus, where c is the number of questions you answered correctly and g is your answer to question 3. In order to maximize your bonus.
        '''
        if pd.isna(self.df[STEM_QUIZ_1_SCORE][index]):
            return 0
        c = self.df[STEM_QUIZ_1_SCORE][index] * 10 # Num questions answered correctly
        g = self.df[PASSING_THRESHOLD][index] # Your answer to question 3

        if pd.isna(g):
            return 0
        return (max(100 - abs(c - g), 0) / 100) * 2

    
    def calculate_bonus_section_5(self, index):
        if pd.isna(self.df[PREFERRED_SECOND_SURVEY][index]):
            return 0
        if self.df[PREFERRED_SECOND_SURVEY][index] == 'STEM Track':
            if self.df[QUIZ_2_SCORE][index] * 10 >= self.df[PASSING_THRESHOLD][index]:
                return 2
            return 0
        else:
            return self.df[QUIZ_2_SCORE][index] * 2
        
    def calculate_bonus_section_6(self, index, question=None, i=None):
        # Check if question is None (don't check it its not question, b/c question might be 0)
        if pd.isna(self.df[RISK_TOLERANCE_ANSWERS][index]):
            return 0
        if question == None:
            question = random.randint(0, 10) # inclusive range

        # If for the random question, they chose the risky option.
        if list(self.df[RISK_TOLERANCE_ANSWERS][index])[question] == 'R':
            p = random.randint(1, 100)
            if p < 50:
                return 10
            return 0
        # For the nth question, the fixed payment is equal to n.
        return question

df = pd.read_csv('Exp1_Trial_4_cleaned_data.csv')

payment_calculator = Payment_Calculator(df)
all_payments = payment_calculator.calculate_all_payments()

# Save the payments to a csv file
all_payments.to_csv('Exp1_Trial_4_payments.csv', index=False)