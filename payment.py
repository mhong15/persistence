import pandas as pd
from scipy.stats import ttest_ind
import random

'''
Every participant will receive a base payment of $10. Every participant will have the opportunity to earn an additional bonus of up to $2. When determining the bonus, we will randomly choose one of the following sections to determine which section will be used to calculate the bonus:

0: Section 1: The STEM quiz. If this section is selected, then we will randomly select choose a question from the quiz. If the participant correctly answers the question, then they will receive the $2 bonus.

1: Section 2: Overestimation, overplacement, and the threshold quiz. If this section is selected, then we will randomly select one of the three questions from the quiz. The bonus for the 3 questions will be calcualted in the following manner:
    - Question 1: We will generate a random number (p) between 0 and 100. If p is lower than your answer to question 1, we will compare your score with a randomly selected participant. If your score is equal to or greater than the score of the randomly selected participant, then you will gain a $2 bonus. Otherwise, you will receive a $0 bonus. If p is greater than or equal to your answer, then we will randomly choose a number (r) between 0 and 100. If r < p, then you will receive a $2 bonus. Otherwise, you will receive a $0 bonus.
    - Question 2: If question 2 is selected for the bonus question and you successfully guess the number of questions you answered correctly, then you will receive the bonus payment of $2.
    - Question 3: If question 3 is selected for the bonus question, you will earn a (max{100 - |c - g|, 0} / 100) * $2 bonus, where c is the number of questions you answered correctly and g is your answer to question 3. In order to maximize your bonus, you should guess the median of your belief distribution. In other words, it is in your best interest to choose the value of X for which you think it is equally likely that you scored higher or lower than X number of questions correctly.

2: Section 5: For Section 5, the participant will either be on the STEM Track or the Non-STEM Track. Each quiz will be incentivized differently:
    - STEM Track: If the participant "passes" their second STEM quiz by answering more than their passing_threshold correctly, then they will receive a $2 bonus. Their passing_threshold is determined by the number of questions they recorded for Question 3 of Section 2.
    - Non-STEM Track: Participants will receive $0.20 per each question they answer correctly in the Non-STEM quiz.

3: Section 6: For the Risk Tolerance Quiz, we will randomly select one of the 10 questions. The questions are structured as "Would you rather have a 50% chance of winning $10 or receive a guarenteed $0?". For the randomly selected question, if the participant answers that they would rather have a 50% chance of winning $10, then we will pick a random number p between 0 and 100. If p is less than 50, then the participant will receive a $2 bonus. Otherwise, they will receive a $0 bonus. Otherwise, they will receive a $X bonus if they choose the constant option.
'''

class Payment_Calculator:
    SECTION_1 = 0
    SECTION_2 = 1
    SECTION_5 = 2
    SECTION_6 = 3
    BASE = 10

    bonus_payment_sections = [SECTION_1, SECTION_2, SECTION_5, SECTION_6]

    def __init__(self, df):
        self.df = df
        self.payment_df = None

    def calculate_all_payments(self):
        # Create a new data frame with all of the payment information
        self.payment_df = pd.DataFrame(columns=['participant_id', 'bonus_payment_section', 'payment'])
        for row in range(self.df.index.size):
            (section, bonus) = self.calculate_bonus_section(row)
            self.payment_df = self.payment_df._append({'participant_id': row, 'bonus_payment_section': section, 'payment': bonus + Payment_Calculator.BASE}, ignore_index=True)
        return self.payment_df
    
    def calculate_bonus_section(self, index):
            bonus_section = random.choice(self.bonus_payment_sections)
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
        # For testing purposes, I'm going to pass in a question number.
        if question == None:
            question = random.randint(0, 9)

        section_1_answer_key = pd.read_csv('Section_1/Section_1.csv')
        participant_answer = list(self.df['stem_quiz_1_answers'][index])[question]
        correct_answer = section_1_answer_key['correct_answer'][question]
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
        p = random.randint(0, 99) # Generating p
        overplacement = self.df['overplacement'][index]
        if p < int(overplacement):
            random_participant = self.df.sample()
            random_participant_score = random_participant['stem_quiz_1_score']
            
            participant_score = self.df['stem_quiz_1_score'][index]
            if  participant_score >= random_participant_score:
                return 2
            return 0
        r = random.randint(0, 99)
        if r < p:
            return 2
        return 0
    
    def calculate_bonus_section_2_question_2(self, index):
        '''
        If question 2 is selected for the bonus question and you successfully guess the number of questions you answered correctly, then you will receive the bonus payment of $2.
        '''
        if self.df['overestimation'][index] == self.df['stem_quiz_1_score'][index] * 10:
            return 2
        return 0
    
    def calculate_bonus_section_2_question_3(self, index):
        '''
        If question 3 is selected for the bonus question, you will earn a (max{100 - |c - g|, 0} / 100) * $2 bonus, where c is the number of questions you answered correctly and g is your answer to question 3. In order to maximize your bonus.
        '''
        c = self.df['stem_quiz_1_score'][index] * 10 # Num questions answered correctly
        g = self.df['passing_threshold'][index] # Your answer to question 3
        return (max(100 - abs(c - g), 0) / 100) * 2


    
    def calculate_bonus_section_5(self, index):
        if self.df['preferred_second_survey'][index] == 'Continue STEM Track - Proceed to STEM Quiz':
            if self.df['quiz_2_score'][index] > self.df['passing_threshold'][index]:
                return 2
            return 0
        else:
            return self.df['quiz_2_score'][index] * 2
        
    def calculate_bonus_section_6(self, index, question=None, i=None):
        # Check if question is None (don't check it its not question, b/c question might be 0)
        if question == None:
            question = random.randint(0, 10)

        # If for the random question, they chose the risky option.
        if list(self.df['risk_tolerance_answers'][index])[question] == 'R':
            p = random.randint(0, 99)
            if p < 50:
                return 10
            return 0
        # For the nth question, the fixed payment is equal to n.
        return question

df = pd.read_csv('experiment_data.csv')
payment_calculator = Payment_Calculator(df)
all_payments = payment_calculator.calculate_all_payments()
print(all_payments)