from otree.api import *
import csv
import json

class C(BaseConstants):
    NAME_IN_URL = 'Section_1'
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

    stem_quiz_1_answers = models.StringField()
    stem_quiz_1_score = models.FloatField()
    num_tab_switches_in_section_1 = models.IntegerField()
    total_time_hidden_in_section_1 = models.FloatField()

    def get_quiz_answers(self):
        return "".join([self.question1, self.question2, self.question3, self.question4,
                self.question5, self.question6, self.question7, self.question8,
                self.question9, self.question10])
    
    def calculate_score(self):
        user_answers = self.participant.vars['stem_quiz_1_answers']
        parsed_questions = Section_1.vars_for_template(self)['parsed_questions']
        score = 0
        for i, question in enumerate(parsed_questions):
            if user_answers[i] == question['correct_answer']:
                score += 1/len(parsed_questions)
        return score.__round__(2)
        
class Intro(Page):
    form_model = 'player'
    
class Section_1(Page):
    form_model = 'player'
    form_fields = ['question1', 'question2', 'question3', 'question4', 
                   'question5', 'question6', 'question7', 'question8', 
                   'question9', 'question10', 'num_tab_switches_in_section_1', 'total_time_hidden_in_section_1']
    timeout_seconds = 480

    def vars_for_template(self):
        with open('Section_1/static/Section_1.csv', 'r') as file:
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
                'image_url': f'Section_1/{question["question_text"]}.png', 
            }
            parsed_questions.append(parsed_question)
        return {'parsed_questions': parsed_questions}

class Conclusion(Page):
    form_model = 'player'
    
    def is_displayed(player):
        player.stem_quiz_1_answers = player.get_quiz_answers()
        player.participant.vars['stem_quiz_1_answers'] = player.stem_quiz_1_answers
        player.stem_quiz_1_score = player.calculate_score()
        player.participant.vars['stem_quiz_1_score'] = player.stem_quiz_1_score
        player.participant.vars['stem_quiz_1_score'] = player.calculate_score()
        player.participant.vars['num_tab_switches_in_section_1'] = player.num_tab_switches_in_section_1
        player.participant.vars['total_time_hidden_in_section_1'] = player.total_time_hidden_in_section_1

        return True

page_sequence = [Intro, Section_1, Conclusion]
