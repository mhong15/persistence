from otree.api import *
import csv
import json

class C(BaseConstants):
    NAME_IN_URL = 'Section_4_5'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass

class Player(BasePlayer):
    question1 = models.StringField(
        choices=["A", "B", "C", "D"],
        widget=widgets.RadioSelect,
        label=''
    )
    question2 = models.StringField(
        choices=["A", "B", "C", "D"],
        widget=widgets.RadioSelect,
        label=''
    )
    question3 = models.StringField(
        choices=["A", "B", "C", "D"],
        widget=widgets.RadioSelect,
        label=''
    )
    question4 = models.StringField(
        choices=["A", "B", "C", "D"],
        widget=widgets.RadioSelect,
        label=''
    )
    question5 = models.StringField(
        choices=["A", "B", "C", "D"],
        widget=widgets.RadioSelect,
        label=''
    )
    question6 = models.StringField(
        choices=["A", "B", "C", "D"],
        widget=widgets.RadioSelect,
        label=''
    )
    question7 = models.StringField(
        choices=["A", "B", "C", "D"],
        widget=widgets.RadioSelect,
        label=''
    )
    question8 = models.StringField(
        choices=["A", "B", "C", "D"],
        widget=widgets.RadioSelect,
        label=''
    )
    question9 = models.StringField(
        choices=["A", "B", "C", "D"],
        widget=widgets.RadioSelect,
        label=''
    )
    question10 = models.StringField(
        choices=["A", "B", "C", "D"],
        widget=widgets.RadioSelect,
        label=''
    )

    quiz_2_answers = models.StringField()
    quiz_2_score = models.FloatField()
    preferred_second_survey = models.StringField(
        choices=['STEM Track', 'Non-STEM Track'],
        label="Choose your preferred track"
    )
    parsed_questions = models.StringField()
    num_tab_switches_in_section_5 = models.IntegerField()
    total_time_hidden_in_section_5 = models.FloatField()
    passing_threshold = models.IntegerField(min=0, max=10)

    def get_quiz_answers(self):
        return "".join([self.question1, self.question2, self.question3, self.question4,
                self.question5, self.question6, self.question7, self.question8,
                self.question9, self.question10])
    
    def calculate_score(self):
        user_answers = self.participant.vars['quiz_2_answers']
        if self.participant.vars['preferred_second_survey'] == 'STEM Track':
            parsed_questions = Section_5A.vars_for_template(self)['parsed_questions']
        else:
            parsed_questions = Section_5B.vars_for_template(self)['parsed_questions']

        score = 0
        for i, question in enumerate(parsed_questions):
            print(i, user_answers[i], question['correct_answer'])
            if user_answers[i] == question['correct_answer']:
                score += 1/len(parsed_questions)
        return score.__round__(2)

# PAGES
class Section_4(Page):
    form_model = 'player'
    form_fields = ['preferred_second_survey']

    def is_displayed(player):
        player.passing_threshold = player.participant.vars['passing_threshold']
        return True
    
    def before_next_page(player, timeout_happened):
        player.participant.vars['preferred_second_survey'] = player.preferred_second_survey

class Conclusion_Section_4(Page):
    form_model = 'player'

class Section_5A(Page):
    timeout_seconds = 480
    form_model = 'player'
    form_fields = ['question1', 'question2', 'question3', 'question4', 
                   'question5', 'question6', 'question7', 'question8', 
                   'question9', 'question10', 'num_tab_switches_in_section_5', 'total_time_hidden_in_section_5']
    
    def is_displayed(player):
        return player.preferred_second_survey == 'STEM Track'
    
    def vars_for_template(self):
        with open('Section_4_5/static/Section_5A.csv', 'r') as file:
            questions_data = list(csv.DictReader(file))

        parsed_questions = []
        for question in questions_data:
            parsed_question = {
                'question_text': question['question_text'],
                'options': [
                    question['option_1'],
                    question['option_2'],
                    question['option_3'],
                    question['option_4'],
                ],
                'correct_answer': (question['correct_answer']),
                'image_url': f'Section_4_5/Section_5A/{question["question_text"]}.png'
,
            }
            parsed_questions.append(parsed_question)
            print(parsed_questions)
        return {'parsed_questions': parsed_questions}

class Section_5B(Page):
    timeout_seconds = 480
    form_model = 'player'
    form_fields = ['question1', 'question2', 'question3', 'question4', 
                   'question5', 'question6', 'question7', 'question8', 
                   'question9', 'question10', 'num_tab_switches_in_section_5', 'total_time_hidden_in_section_5']

    def is_displayed(player):
        return player.preferred_second_survey == 'Non-STEM Track'

    def vars_for_template(self):
        with open('static/Section_4_5/Section_5B.csv', 'r') as file:
            questions_data = list(csv.DictReader(file))

        parsed_questions = []
        for question in questions_data:
            parsed_question = {
                'question_text': question['question_text'],
                'options': [
                    question['option_1'],
                    question['option_2'],
                    question['option_3'],
                    question['option_4'],
                ],
                'correct_answer': (question['correct_answer']),  
                'image_url': f'Section_4_5/Section_5B/{question["question_text"]}.png', 
            }
            parsed_questions.append(parsed_question)
        return {'parsed_questions': parsed_questions}

class Conclusion_Section_5(Page):
    form_model = 'player'
    
    def is_displayed(player):
        player.participant.vars['quiz_2_answers'] = player.get_quiz_answers()
        player.participant.vars['quiz_2_score'] = player.calculate_score()
        player.participant.vars['num_tab_switches_in_section_5'] = player.num_tab_switches_in_section_5
        player.participant.vars['total_time_hidden_in_section_5'] = player.total_time_hidden_in_section_5
        
        return True

page_sequence = [Section_4, Conclusion_Section_4, Section_5A, Section_5B, Conclusion_Section_5]
