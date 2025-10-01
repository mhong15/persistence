# Persistence: Feedback Structures and Gender Gap in STEM

## Overview
This project studies how **positively and negatively skewed feedback** affects persistence in STEM tasks, focusing on potential gender and ethnic differences. Participants completed STEM quizzes, received feedback, and decided whether to continue or switch to non-STEM tasks.  

The experiment **automates evaluation of quiz performance, calculation of bonuses, and tracking of persistence and risk behavior**, ensuring consistent and scalable data collection.

## Experiment Design
1. **Setup**: STEM and estimation quizzes.  
2. **Feedback**: Random assignment to positively skewed, negatively skewed, or unskewed feedback.  
3. **Persistence**: Option to continue with STEM or switch to non-STEM.  
4. **Risk Assessment**: Measures individual risk tolerance.  
5. **Demographics**: Collect background info (gender, ethnicity, education).  
6. **Automated Evaluation**: Quiz scores, bonuses, and persistence metrics are automatically computed, allowing precise and consistent analysis.  

## Results
- **Total participants**: 1,004  
- **Gender persistence**: No significant difference overall or within feedback types (p ≈ 0.24). Women persist slightly more than men with positively skewed or "Pass" signals.  
- **Overconfidence**: Controlling for performance, men show higher overplacement and overestimation than women.  
- **Ethnicity & persistence**: Asians show significant differences compared to other ethnicities under certain feedback types and signals.  
- **Risk preference**: Male participants are generally more risk-tolerant; Asian females show high risk tolerance (~70%).  
- **Feedback preference**: Participants generally favor positively skewed feedback. Notably, Asian females strongly prefer positively skewed feedback; Asian males prefer negatively skewed feedback.  

## Analysis Methods
- Two-tailed t-tests for persistence and overconfidence across demographics.  
- Regression analysis controlling for performance.  
- Chi-squared tests for persistence vs. risk preference.  
- Automated calculation of payments, persistence scores, and incentive-based bonuses ensures reproducibility and scalability.  

## Tools & Technologies
- **OTree**, **Qualtrics**, **Python / Pandas**

## Conclusion
- Positively skewed feedback can slightly enhance persistence, particularly for women and certain demographic groups.  
- Gender differences in persistence are minimal, but overconfidence differs by gender.  
- Ethnic group differences suggest nuanced effects of feedback on persistence.  
- Automation of evaluation and payment allows reliable, reproducible results and reduces human error.  

## References
- Kogelnik, Maria. *Performance Feedback and Gender Differences in Persistence*, 2022  
- Masatlioglu, Yusufcan et al. *Intrinsic Information Preferences and Skewness*, 2017  
