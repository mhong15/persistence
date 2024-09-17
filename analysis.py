# import pandas as pd
# from scipy.stats import ttest_ind
# from scipy.stats import chi2_contingency
# import numpy as np

# df = pd.read_csv('experiment_data.csv')
# print(df.head())

# # Print all of the fields
# print(df.columns)

# # Remove participants who cheated: had more than 5 tab switches and more than 30 seconds of hidden pages.

# df = df[(df['num_tab_switches_in_section_1'] <= 5) & 
#         (df['total_time_hidden_in_section_1'] <= 30) & 
#         (df['num_tab_switches_in_section_5'] <= 5) & 
#         (df['total_time_hidden_in_section_5'] <= 30)]

# """
#  Remove participants who answer incorrectly on ball 
#     origin estimation questions in Section 3A, 3B, and 3C.
#     Ground: 
#         - If their on the ground path, their ball was red, and they answered  Fail box - remove them.
#         - If their on the ground path, their ball was black, and they answered  Pass box - remove them.
#     Positive:
#         - If their on the positive path, their ball is black, and they answered Fail box - remove them.
#     Negative:
#         - If their on the negative path, their ball is black, and they answered Pass box - remove them.
#  """
# df = df[~((df['info_structure'] == 'ground') & (df['ball_color'] == 'red') & (df['ball_origin_estimation'] == 'Fail'))]

# df = df[~((df['info_structure'] == 'ground') & (df['ball_color'] == 'black') & (df['ball_origin_estimation'] == 'Pass'))]

# df = df[~((df['info_structure'] == 'positive') & (df['ball_color'] == 'black') & (df['ball_origin_estimation'] == 'Fail'))]

# df = df[~((df['info_structure'] == 'negative') & (df['ball_color'] == 'black') & (df['ball_origin_estimation'] == 'Pass'))]

# '''
# How does skewness in feedback structures affect persisten in STEM environments?
# Part 1 of analysis:
# To analyze our experiment, we will first use a pair of two-sample t-tests to determine if the average persistence of our unskewed group (ground) is significantly different from the average persistence of our skewed groups (positive and negative). Average persistence within each group will be determined by the average number of participants who chose to continue the experiment in Stage 3. We will use a significance level of 0.05 for all tests and reject the null hypothesis if our p-value is less than or equal to 0.05 and fail to reject the null hypothesis otherwise.

# Null Hypothesis: There is no significant difference in the average persistence of participants in the ground group compared to the average persistence of participants in the positive and negative groups.

# Alternative Hypothesis: There is a significant difference in the average persistence of participants in the ground group compared to the average persistence of participants in the positive and negative groups.
# '''

# def t_tests(df, alpha):
#     ground_persistence = df[df['info_structure'] == 'ground']['preferred_second_survey'].apply(lambda x: 1 if x == 'STEM Track' else 0)
#     positive_persistence = df[df['info_structure'] == 'positive']['preferred_second_survey'].apply(lambda x: 1 if x == 'STEM Track' else 0)
#     negative_persistence = df[df['info_structure'] == 'negative']['preferred_second_survey'].apply(lambda x: 1 if x == 'STEM Track' else 0)

#     t_statistic, p_value = ttest_ind(ground_persistence, positive_persistence)
#     print("NULL HYPOTHESIS: There is no significant difference in the average persistence of participants in the ground truth group compared to the average persistence of participants in the positively skewed group.")
#     print(f'(Ground Truth, Positively Skewed) p-value: {p_value}')
#     if p_value <= alpha:
#         print('Reject the null hypothesisd\n')
#     else:
#         print('Fail to reject the null hypothesis\n')

#     t_statistic, p_value = ttest_ind(ground_persistence, negative_persistence)
#     print(f'(Ground Truth, Negatively Skewed) p-value: {p_value}')
#     print("NULL HYPOTHESIS: There is no significant difference in the average persistence of participants in the ground group compared to the average persistence of participants in the negatively skewed group.")
#     if p_value <= alpha:
#         print('Reject the null hypothesis\n')
#     else:
#         print('Fail to reject the null hypothesis\n')

# '''
# As part of our secondary analysis, we want to determine if ones persistence in Stage 3 is independent of risk preference in Stage 4. To do this, we will employ a Chi-squared test to see if there is a significant correlation between persistence (continue or quit) and risk preference (fixed payment or bet). Our null hypothesis is that persistence and risk preference are not significantly associated. Our alternative hypothesis is that persistence and risk preference are significantly associated. We will create a contingency table where the rows represent the bet versus fixed categorical options and the columns represent continue or quit. We will fill each cell of the contingency table with the frequencies of each contingency.
# '''
# # Calculate when each participant switches over from the risky payment to the constant payment

# def risk_tolerant_or_averse(risk_quiz):
#     for i, c in enumerate(risk_quiz):
#         if c == "C":
#             if i <= 5: # Would you rather have 50% chance of $10 or $5?
#                 return 'risk_averse'
#             return 'risk_tolerant'
#     return 'risk_tolerant'


# def chi_squared_test(df, alpha):
#     df['risk_averse_or_tolerant'] = df['risk_tolerance_answers'].apply(lambda x: risk_tolerant_or_averse(x))
#     # print(df['risk_averse_or_tolerant'])
#     df['continue_or_quit'] = df['preferred_second_survey'].apply(lambda x: 'Continue' if x == 'STEM Track' else 'Quit')

#     continue_and_bet = sum((df['continue_or_quit'] == 'Continue') & (df['risk_averse_or_tolerant'] == 'risk_tolerant'))
#     continue_and_fixed = sum((df['continue_or_quit'] == 'Continue') & (df['risk_averse_or_tolerant'] == 'risk_averse'))
#     quit_and_bet = sum((df['continue_or_quit'] == 'Quit') & (df['risk_averse_or_tolerant'] == 'risk_tolerant'))
#     quit_and_fixed = sum((df['continue_or_quit'] == 'Quit') & (df['risk_averse_or_tolerant'] == 'risk_averse'))

#     contingency_table = np.array([[continue_and_bet, quit_and_bet], [continue_and_fixed, quit_and_fixed]])

#     print(contingency_table)

#     chi2, p, dof, expected = chi2_contingency(contingency_table)
#     print(f'The p-value for the Chi-squared test is {p}')
#     if p <= alpha:
#         print('Reject the null hypothesis - there is no signficant association between persistence and risk preference')
#     else:
#         print('Fail to reject the null hypothesis - there is a significant association between persistence and risk preference')


# # Testing
# alpha = 0.05
# test_df = pd.read_csv('experiment_analysis_test_data.csv')
# print("Part 1: Two Sample T-Tests")
# t_tests(test_df, alpha)
# print("Part 2: Chi-Squared Test")
# chi_squared_test(test_df, alpha)

