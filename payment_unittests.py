import pandas as pd
import random
import unittest
from payment import Payment_Calculator

df = pd.read_csv('experiment_test_data.csv')
payment_calculator = Payment_Calculator(df)
print(payment_calculator.calculate_all_payments())
'''
AACBBBDCCB,1.0,0,0.0,90,7,7,positive,noisy,random,Fail,red,Fail Box,Non-STEM Track,DBACBDABCD,1.0,0,0.0,"['R', 'R', 'R', 'R', 'R', 'C', 'C', 'C', 'C', 'C', 'C']",False,False,False,False,False,False,False,False,False,,

info_structure,track,path,performance,
Participant Info:
Quiz 1 Answers: "['A', 'A', 'C', 'B', 'B', 'B', 'D', 'C', 'C', 'B']
Quiz 1 Score: 1.0
Overplacement: 90
Overestimation: 7
Passing Threshold: 7
Info Structure: negative
Track: noisy
Path: random
Performance: Fail
Ball Color: red
Ball Origin Estimation: Pass Box
Second Quiz: Non-STEM Track
Second Quiz Answers: ['A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A']"
Second Quiz Score: 0.2
Risk Tolerance: "['R', 'R', 'R', 'R', 'R', 'C', 'C', 'C', 'C', 'C', 'C']"
'''

class TestPaymentMethods(unittest.TestCase):
    # We should have correct answers for the quiz
    def test_calculate_bonus_section_1(self):
        # Test that the bonus for section 1 is calculated correctly
        for i in range(10):
            bonus = payment_calculator.calculate_bonus_section_1(0, question=i)
            self.assertEqual(bonus, 2)

    def test_calculate_bonus_section_2_question_2(self):
        # Should be 0 since they scored a perfect score, but guessed 7
        for i in range(10):
            bonus = payment_calculator.calculate_bonus_section_2_question_2(0)
            self.assertEqual(bonus, 0)

    def test_calculate_bonus_section_2_question_3(self):
        # Passing Threshhold: 7
        # Num Correct: 10
        # Answer: max(100 - abs(10 - 7), 0) / 100 * 2 = 1.94
        bonus = payment_calculator.calculate_bonus_section_2_question_3(0)
        self.assertEqual(bonus, 1.94)

    def test_calculate_bonus_section_5(self):
        # Took the Non-STEM quiz -> answered correctly on all questions
        # Should have a $2 bonus
        bonus = payment_calculator.calculate_bonus_section_5(0)
        self.assertEqual(bonus, 2)

    def test_calculate_bonus_section_6(self):
        # Always answered conservative -> should have i bonus
        for i in range(11):
            bonus = payment_calculator.calculate_bonus_section_6(index=0, question=i, i=i)
            self.assertEqual(bonus, i, f"Failed for question {i}: expected {i}, got {bonus}")


if __name__ == '__main__':
    unittest.main()