import pandas as pd
from scipy.stats import ttest_ind
from scipy.stats import chi2_contingency
from statsmodels.stats.power import tt_ind_solve_power
import numpy as np
import statsmodels.api as sm

ETHNICITIES_SIMPLIFIED = ['Asian', 'White', 'Black', 'Mixed', 'Other']
SEXES = ["Female", "Male"]

def clean_csv(input_file, output_file):
    # Define the columns to keep with their corresponding headers
    columns_to_keep = {
        "Intro.1.player.prolific_id": "prolific_id",
        "Time taken": "time_taken",
        "Total approvals": "total_approvals",
        "Ethnicity": "ethnicity",
        "Highest education level completed": "highest_education",
        "Age": "age",
        "Sex": "sex",
        "Ethnicity simplified": "ethnicity_simplified",
        "Country of birth": "country_of_birth",
        "Country of residence": "country_of_residence",
        "Nationality": "nationality",
        "Language": "language",
        "Student status": "student_status",
        "Employment status": "employment_status",
        "Section_1.1.player.stem_quiz_1_answers": "stem_quiz_1_answers",
        "Section_1.1.player.stem_quiz_1_score": "stem_quiz_1_score",
        "Section_1.1.player.num_tab_switches_in_section_1": "section_1_num_tab_switches",
        "Section_1.1.player.total_time_hidden_in_section_1": "section_1_time_hidden",
        "Section_2_3.1.player.info_structure": "info_structure",
        "Section_2_3.1.player.performance": "player_performance",
        "Section_2_3.1.player.overplacement": "overplacement",
        "Section_2_3.1.player.overestimation": "overestimation",
        "Section_2_3.1.player.passing_threshold": "passing_threshold",
        "Section_2_3.1.player.ball_origin_estimation": "ball_origin_estimation",
        "Section_4_5.1.player.preferred_second_survey": "preferred_second_survey",
        "Section_4_5.1.player.num_tab_switches_in_section_5": "section_5_num_tab_switches",
        "Section_4_5.1.player.total_time_hidden_in_section_5": "section_5_time_hidden",
        "Section_2_3.1.player.ball_color": "ball_color",
        "Section_7.1.player.schools_private_independent": "schools_private_independent",
        "Section_7.1.player.schools_private_religious": "schools_private_religious",
        "Section_7.1.player.schools_public_school": "schools_public_school",
        "Section_7.1.player.schools_homeschool": "schools_homeschool",
        "Section_7.1.player.schools_online_school": "schools_online_school",
        "Section_7.1.player.schools_charter_school": "schools_charter_school",
        "Section_7.1.player.schools_all_girls_school": "schools_all_girls_school",
        "Section_7.1.player.schools_all_boys_school": "schools_all_boys_school",
        "Section_7.1.player.schools_stem_oriented_school": "schools_stem_oriented_school",
        "Section_7.1.player.track_decision": "track_decision",
        "Section_7.1.player.experience": "experience",
        "Section_7.1.player.preferred_second_survey": "preferred_second_survey_explanation"
    }
    
    for i in range(1, 11):
        columns_to_keep[f"Section_1.1.player.question{i}"] = f"stem_quiz_1_{i}"
        columns_to_keep[f"Section_4_5.1.player.question{i}"] = f"quiz_2_{i}"
    
    for i in range(1, 12):
        columns_to_keep[f"Section_6.1.player.question{i}"] = f"risk_tolerance_{i}"

    # Load CSV
    df = pd.read_csv(input_file)
    
    # Keep only specified columns
    df = df[list(columns_to_keep.keys())]
    
    # Rename columns
    df = df.rename(columns=columns_to_keep)

    # continue_or_quit
    df['continue_or_quit'] = df["preferred_second_survey"].apply(lambda x: 1 if x == 'Continue STEM Track - Proceed to STEM Quiz' else 0)
    
    # Save cleaned CSV
    df.to_csv(output_file, index=False)
    
    print(f"Cleaned CSV saved to {output_file}")

def sex_t_test(input_file):
    df = pd.read_csv(input_file)

    # T-test betweeen male and female persistence
    arg1_data = df[df["sex"] == "Female"]['continue_or_quit']
    arg2_data = df[df["sex"] == "Male"]['continue_or_quit']

    print(arg1_data.count())
    print(arg2_data.count())

    (_, p_value) = ttest_ind(arg1_data, arg2_data)

    print(p_value)

def print_header(header):
    print(f"\n{header}\n{'-' * (50)}")

def persistence(group1, group2, desc1, desc2, alpha=0.05, power=0.8):
    # Calculate the difference between average persistence of Asians and other
    print_header(f"Comparing Persistence of {desc1} and {desc2}")
    arg1_data = group1['continue_or_quit']
    arg2_data = group2['continue_or_quit']

    diff = arg1_data.mean() - arg2_data.mean()
    std1 = np.std(arg1_data, ddof=1)
    std2 = np.std(arg2_data, ddof=1)
    count1 = arg1_data.count()
    count2 = arg2_data.count()

    # if "Latino/Hispanic" in desc1:
    print(f"Diff in Persistence: {round(diff, 4)}")
    print(f"Avg. Persistence of {desc1}: {round(arg1_data.mean(), 4)}")
    print(f"Avg. Persistence of {desc2}: {round(arg2_data.mean(), 4)}")
    print(f"Count of {desc1}: {count1}")
    print(f"Count of {desc2}: {count2}")
    print(f"Std of {desc1}: {round(std1, 4)}")
    print(f"Std of {desc2}: {round(std2, 4)}")

    # Compute effect size (Cohen's d)
    pooled_std = np.sqrt(((std1**2 + std2**2) / 2))
    effect_size = abs(diff) / pooled_std
    print(f"Cohen's d: {round(effect_size, 4)}")

    # Compute required sample size per group
    required_n = tt_ind_solve_power(effect_size=effect_size, alpha=alpha, power=power, alternative='two-sided')
    required_n = np.ceil(required_n)

    print(f"Required Sample Size per Group for 5% Significance & 80% Power: {int(required_n)}")

    if count1 >= required_n and count2 >= required_n:
        sampled_group1 = arg1_data.sample(n=int(required_n), random_state=42)
        sampled_group2 = arg2_data.sample(n=int(required_n), random_state=42)

        _, p_value = ttest_ind(sampled_group1, sampled_group2)
        print(f"t-test p-value: {round(p_value, 4)}\n")
    else:
        print("Not enough data to perform the t-test with the required sample size.\n")
        
        print(f"Need to collect: {max(int(required_n) - count1, 0)} more samples for {desc1}")
        print(f"Need to collect: {max(int(required_n) - count2, 0)} more samples for {desc2}")
    
def persistence_sex_regression():
    df['binary_sex'] = df['sex'].map({'Male': 1, 'Female': 0})

    X = df[['binary_sex', 'stem_quiz_1_score']]
    X = sm.add_constant(X)
    y = df['continue_or_quit']

    model = sm.Logit(y, X).fit()

    print(model.summary())

    odds_ratios = pd.DataFrame({'Variable': X.columns, 'Odds Ratio': np.exp(model.params)})
    print(odds_ratios)

def persistence_sex_info_structure_regression(df):
    df['binary_sex'] = df['sex'].map({'Male': 1, 'Female': 0})
    df = pd.get_dummies(df, columns=['info_structure'], drop_first=True)

    df[['info_structure_positive', 'info_structure_negative']] = df[[ 'info_structure_positive', 'info_structure_negative']].astype(int)

    X = df[['binary_sex', 'stem_quiz_1_score'] + [col for col in df.columns if col.startswith('info_structure_')]]

    X = sm.add_constant(X)
    y = df['continue_or_quit']

    model = sm.Logit(y, X).fit()

    print(model.summary())

    odds_ratios = pd.DataFrame({'Variable': X.columns, 'Odds Ratio': np.exp(model.params)})
    print(odds_ratios)

def persistence_sex_ethnicity_regression(df):
    df['sex_ethnicity'] = df['sex'].astype(str) + '_' + df['ethnicity_simplified'].astype(str)
    df_sex_ethnicity_dummies = pd.get_dummies(df['sex_ethnicity'], prefix='sex_ethnicity', drop_first=True)
    print(df_sex_ethnicity_dummies.columns)

    # convert columns to int
    df_sex_ethnicity_dummies[['sex_ethnicity_Female_Black',            'sex_ethnicity_Female_Mixed',
       'sex_ethnicity_Female_Other', 'sex_ethnicity_Female_White',
       'sex_ethnicity_Male_Asian', 'sex_ethnicity_Male_Black',
       'sex_ethnicity_Male_Mixed', 'sex_ethnicity_Male_Other',
       'sex_ethnicity_Male_White']] = df_sex_ethnicity_dummies[['sex_ethnicity_Female_Black', 'sex_ethnicity_Female_Mixed',
       'sex_ethnicity_Female_Other', 'sex_ethnicity_Female_White',
       'sex_ethnicity_Male_Asian', 'sex_ethnicity_Male_Black',
       'sex_ethnicity_Male_Mixed', 'sex_ethnicity_Male_Other',
       'sex_ethnicity_Male_White']].astype(int)

    df = pd.concat([df, df_sex_ethnicity_dummies], axis=1)

    X = df[['stem_quiz_1_score'] + [col for col in df.columns if col.startswith('sex_ethnicity_')]]
    X = sm.add_constant(X)
    y = df['continue_or_quit']

    model = sm.Logit(y, X).fit()

    print(model.summary())

    odds_ratios = pd.DataFrame({'Variable': X.columns, 'Odds Ratio': np.exp(model.params)})
    print(odds_ratios)

def persistence_ethnicity_info_structure_regression(df, ethnicity):
    df = df[df["ethnicity_simplified"] == ethnicity]

    df = pd.get_dummies(df, columns=['info_structure'], drop_first=True)

    df[['info_structure_positive', 'info_structure_negative']] = df[[ 'info_structure_positive', 'info_structure_negative']].astype(int)

    # persistence ~ stem_quiz_1_score + info_structure
    X = df[['stem_quiz_1_score'] + [col for col in df.columns if col.startswith('info_structure_')]]
    X = sm.add_constant(X)
    y = df['continue_or_quit']

    model = sm.Logit(y, X).fit()

    print(model.summary())

    odds_ratios = pd.DataFrame({'Variable': X.columns, 'Odds Ratio': np.exp(model.params)})
    print(odds_ratios)

def persistence_ethnicity_regression(df):
    df = pd.get_dummies(df, columns=['ethnicity_simplified'], drop_first=True)

    df[['ethnicity_simplified_Black', 
    'ethnicity_simplified_Mixed', 
    'ethnicity_simplified_Other', 
    'ethnicity_simplified_White']] = df[['ethnicity_simplified_Black', 
                                        'ethnicity_simplified_Mixed', 
                                        'ethnicity_simplified_Other', 
                                        'ethnicity_simplified_White']].astype(int)

    X = df[['stem_quiz_1_score'] + [col for col in df.columns if col.startswith('ethnicity_simplified_')]]
    X = sm.add_constant(X)
    y = df['continue_or_quit']

    model = sm.Logit(y, X).fit()

    print(model.summary())

    odds_ratios = pd.DataFrame({'Variable': X.columns, 'Odds Ratio': np.exp(model.params)})
    print(odds_ratios)

def avg_rates_persistence_across_gender_ethnicity(df):
    for ethnicity in ETHNICITIES_SIMPLIFIED:
        for sex in SEXES:
            avg_persistence = df[(df["ethnicity_simplified"] == ethnicity) &
                       (df["sex"] == sex)]['continue_or_quit'].mean()
            print(f"Avg. Persistence ({ethnicity, sex}): {round(avg_persistence, 2)}")

#clean_csv("Exp1_Combined_analysis_data.csv", "Exp1_cleaned_analysis_data.csv")
df = pd.read_csv("Exp1_cleaned_analysis_data.csv")

persistence_sex_regression()
persistence_sex_info_structure_regression(df)
persistence_sex_ethnicity_regression(df)
persistence_ethnicity_info_structure_regression(df, "Asian")
# avg_rates_persistence_across_gender_ethnicity(df)
# persistence_ethnicity_regression(df)

def persistence_by_ethnicity():
    # Asian vs. Non-Asian
    # persistence(group1 = df[df["ethnicity_simplified"] == "Asian"], 
    #             group2 = df[df["ethnicity_simplified"] != "Asian"],
    #             desc1= "Asians", 
    #             desc2="Others")

    # # Female Asian vs. Male Asian
    # persistence(group1 = df[(df["ethnicity_simplified"] == "Asian") & 
    #                         (df["sex"] == "Female")], 
    #             group2 = df[(df["ethnicity_simplified"] == "Asian") & 
    #                         (df["sex"] == "Male")],
    #             desc1= "(Female, Asian)", 
    #             desc2="(Male, Asian)")

    # # Female Asian vs. Male Asian - Ground
    # persistence(group1 = df[(df["ethnicity_simplified"] == "Asian") & 
    #                         (df["sex"] == "Female") & 
    #                         (df["info_structure"] == "ground")], 
    #             group2 = df[(df["ethnicity_simplified"] == "Asian") & 
    #                         (df["sex"] == "Male") & 
    #                         (df["info_structure"] == "ground")],
    #             desc1= "(Female, Asian, Ground)", 
    #             desc2="(Male, Asian, Ground)")

    # # Female Asian vs. Male Asian - Negative
    # persistence(group1 = df[(df["ethnicity_simplified"] == "Asian") & 
    #                         (df["sex"] == "Female") & 
    #                         (df["info_structure"] == "negative")], 
    #             group2 = df[(df["ethnicity_simplified"] == "Asian") & 
    #                         (df["sex"] == "Male") & 
    #                         (df["info_structure"] == "negative")],
    #             desc1= "(Female, Asian, Negative)", 
    #             desc2="(Male, Asian, Negative)")

    # Female Asian vs. Male Asian - Positive
    persistence(group1 = df[(df["ethnicity_simplified"] == "Asian") & 
                            (df["sex"] == "Female") & 
                            (df["info_structure"] == "positive")], 
                group2 = df[(df["ethnicity_simplified"] == "Asian") & 
                            (df["sex"] == "Male") & 
                            (df["info_structure"] == "positive")],
                desc1= "(Female, Asian, Positive)", 
                desc2="(Male, Asian, Positive)")

    # # Asian vs. Black
    # persistence(group1 = df[(df["ethnicity_simplified"] == "Asian")], 
    #             group2 = df[(df["ethnicity_simplified"] == "Black")],
    #             desc1= "(Asian)", 
    #             desc2="(Black)")

    # # Asian vs. White
    # persistence(group1 = df[(df["ethnicity_simplified"] == "Asian")], 
    #             group2 = df[(df["ethnicity_simplified"] == "White")],
    #             desc1= "(Asian)", 
    #             desc2="(White)")

    # # Female Black vs. Male Black
    # persistence(group1 = df[(df["ethnicity_simplified"] == "Black") & 
    #                         (df["sex"] == "Female")], 
    #             group2 = df[(df["ethnicity_simplified"] == "Black") & 
    #                         (df["sex"] == "Male")],
    #             desc1= "(Female, Black)", 
    #             desc2="(Male, Black)")

    # # Female Black vs. Male Black - Ground
    # persistence(group1 = df[(df["ethnicity_simplified"] == "Black") & 
    #                         (df["sex"] == "Female") & 
    #                         (df["info_structure"] == "ground")], 
    #             group2 = df[(df["ethnicity_simplified"] == "Black") & 
    #                         (df["sex"] == "Male") & 
    #                         (df["info_structure"] == "ground")],
    #             desc1= "(Female, Black, Ground)", 
    #             desc2="(Male, Black, Ground)")

    # # Female Black vs. Male Black - Negative
    # persistence(group1 = df[(df["ethnicity_simplified"] == "Black") & 
    #                         (df["sex"] == "Female") & 
    #                         (df["info_structure"] == "negative")], 
    #             group2 = df[(df["ethnicity_simplified"] == "Black") & 
    #                         (df["sex"] == "Male") & 
    #                         (df["info_structure"] == "negative")],
    #             desc1= "(Female, Black, Negative)", 
    #             desc2="(Male, Black, Negative)")

    # # Female Black vs. Male Black - Positive
    # persistence(group1 = df[(df["ethnicity_simplified"] == "Black") & 
    #                         (df["sex"] == "Female") & 
    #                         (df["info_structure"] == "positive")], 
    #             group2 = df[(df["ethnicity_simplified"] == "Black") & 
    #                         (df["sex"] == "Male") & 
    #                         (df["info_structure"] == "positive")],
    #             desc1= "(Female, Black, Positive)", 
    #             desc2="(Male, Black, Positive)")

    # # Female White vs. Male White
    # persistence(group1 = df[(df["ethnicity_simplified"] == "White") & 
    #                         (df["sex"] == "Female")], 
    #             group2 = df[(df["ethnicity_simplified"] == "White") & 
    #                         (df["sex"] == "Male")],
    #             desc1= "(Female, White)", 
    #             desc2="(Male, White)")

    # # Female White vs. Male White - Ground
    # persistence(group1 = df[(df["ethnicity_simplified"] == "White") & 
    #                         (df["sex"] == "Female") & 
    #                         (df["info_structure"] == "ground")], 
    #             group2 = df[(df["ethnicity_simplified"] == "White") & 
    #                         (df["sex"] == "Male") & 
    #                         (df["info_structure"] == "ground")],
    #             desc1= "(Female, White, Ground)", 
    #             desc2="(Male, White, Ground)")

    # # Female White vs. Male White - Negative
    # persistence(group1 = df[(df["ethnicity_simplified"] == "White") & 
    #                         (df["sex"] == "Female") & 
    #                         (df["info_structure"] == "negative")], 
    #             group2 = df[(df["ethnicity_simplified"] == "White") & 
    #                         (df["sex"] == "Male") & 
    #                         (df["info_structure"] == "negative")],
    #             desc1= "(Female, White, Negative)", 
    #             desc2="(Male, White, Negative)")

    # # Female White vs. Male White - Positive
    # persistence(group1 = df[(df["ethnicity_simplified"] == "White") & 
    #                         (df["sex"] == "Female") & 
    #                         (df["info_structure"] == "positive")], 
    #             group2 = df[(df["ethnicity_simplified"] == "White") & 
    #                         (df["sex"] == "Male") & 
    #                         (df["info_structure"] == "positive")],
    #             desc1= "(Female, White, Positive)", 
    #             desc2="(Male, White, Positive)")

    # # Female Hispanic vs. Male Hispanic
    # persistence(group1 = df[(df["ethnicity"] == "Latino/Hispanic") & 
    #                         (df["sex"] == "Female")], 
    #             group2 = df[(df["ethnicity"] == "Latino/Hispanic") & 
    #                         (df["sex"] == "Male")],
    #             desc1= "(Female, Latino/Hispanic)", 
    #             desc2="(Male, Latino/Hispanic)")

    # # Female Hispanic vs. Male Hispanic - Ground
    # persistence(group1 = df[(df["ethnicity"] == "Latino/Hispanic") & 
    #                         (df["sex"] == "Female") &
    #                         (df["info_structure"] == "ground")], 
    #             group2 = df[(df["ethnicity"] == "Latino/Hispanic") & 
    #                         (df["sex"] == "Male") &
    #                         (df["info_structure"] == "ground")],
    #             desc1= "(Female, Latino/Hispanic, Ground)", 
    #             desc2="(Male, Latino/Hispanic, Ground)")

    # # Female Hispanic vs. Male Hispanic - Negative
    # persistence(group1 = df[(df["ethnicity"] == "Latino/Hispanic") & 
    #                         (df["sex"] == "Female") &
    #                         (df["info_structure"] == "negative")], 
    #             group2 = df[(df["ethnicity"] == "Latino/Hispanic") & 
    #                         (df["sex"] == "Male") &
    #                         (df["info_structure"] == "negative")],
    #             desc1= "(Female, Latino/Hispanic, Negative)", 
    #             desc2="(Male, Latino/Hispanic, Negative)")

    # # Female Hispanic vs. Male Hispanic - Positive
    # persistence(group1 = df[(df["ethnicity"] == "Latino/Hispanic") & 
    #                         (df["sex"] == "Female") &
    #                         (df["info_structure"] == "positive")], 
    #             group2 = df[(df["ethnicity"] == "Latino/Hispanic") & 
    #                         (df["sex"] == "Male") &
    #                         (df["info_structure"] == "positive")],
    #             desc1= "(Female, Latino/Hispanic, Positive)", 
    #             desc2="(Male, Latino/Hispanic, Positive)")

# persistence_by_ethnicity()