import pandas as pd
from scipy.stats import ttest_ind
import random
import os
from payments import Payment_Calculator

OTREE_DATA = "Exp2_Trial_1.csv"
DEMOGRAPHIC_DATA = "Exp2_Trial_1_Demographics.csv"

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

payments = pd.read_csv("Exp2_Pilot_case_payments.csv")
data = pd.read_csv("Exp2_Pilot_case_cleaned_data.csv")
data.head(5).to_csv("Exp2_Pilot_case_payments_test.csv", index=False)
ten_payments = pd.read_csv("Exp2_Pilot_case_payments_test.csv")
payment_calculator = Payment_Calculator(ten_payments)

def test_payment_frequencies():
    payment_frequencies = payments['bonus_payment_section'].value_counts(normalize=True)
    print(payment_frequencies)
test_payment_frequencies()

def test_section_1():
    expected_payments = ['0', '0', '0', '2', '2']
    for index in range(1, 5):
        bonus = payment_calculator.calculate_bonus_section_1(index=index, question=2)
        assert str(bonus) == str(expected_payments[index]), f"Expected {expected_payments[index]}, but got {bonus}"

def test_section_2_question_1():
    for index in range(1, 5):
        bonus = payment_calculator.calculate_bonus_section_2_question_1(index=index)

def test_section_2_question_2():
    for index in range(1, 5):
        expected_payment = [0, 0, 0, 0, 0]
        bonus = payment_calculator.calculate_bonus_section_2_question_2(index=index)
        assert bonus == expected_payment[index], f"Expected {expected_payment[index]}, but got {bonus}"

def test_section_2_question_3():
    for index in range(1, 5):
        expected_payment = [1.96, 1.96, 1.96, 1.96, 2]
        bonus = payment_calculator.calculate_bonus_section_2_question_3(index=index)
        assert bonus == expected_payment[index], f"Expected {expected_payment[index]}, but got {bonus}"

test_section_1()
test_section_2_question_1()
test_section_2_question_2()
test_section_2_question_3()


