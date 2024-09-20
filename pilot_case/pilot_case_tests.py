
def t_tests(df, alpha):
    ground_persistence = df[df['info_structure'] == 'ground']['preferred_second_survey'].apply(lambda x: 1 if x == 'STEM Track' else 0)
    positive_persistence = df[df['info_structure'] == 'positive']['preferred_second_survey'].apply(lambda x: 1 if x == 'STEM Track' else 0)
    negative_persistence = df[df['info_structure'] == 'negative']['preferred_second_survey'].apply(lambda x: 1 if x == 'STEM Track' else 0)

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


        