from otree.api import *
import csv
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.urls import path, re_path
import json

doc = """
first STEM Quiz players take.
"""

class C(BaseConstants):
    NAME_IN_URL = 'stemQuiz1'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass

class Player(BasePlayer):
    question_1 = models.StringField(
        choices=["A", "B", "C", "D"],
        widget=widgets.RadioSelect
    )
    question_2 = models.StringField(
        choices=["A", "B", "C", "D"],
        widget=widgets.RadioSelect
    )
    question_3 = models.StringField(
        choices=["A", "B", "C", "D"],
        widget=widgets.RadioSelect
    )
    question_4 = models.StringField(
        choices=["A", "B", "C", "D"],
        widget=widgets.RadioSelect
    )
    question_5 = models.StringField(
        choices=["A", "B", "C", "D"],
        widget=widgets.RadioSelect
    )
    question_6 = models.StringField(
        choices=["A", "B", "C", "D"],
        widget=widgets.RadioSelect
    )
    question_7 = models.StringField(
        choices=["A", "B", "C", "D"],
        widget=widgets.RadioSelect
    )
    question_8 = models.StringField(
        choices=["A", "B", "C", "D"],
        widget=widgets.RadioSelect
    )
    question_9 = models.StringField(
        choices=["A", "B", "C", "D"],
        widget=widgets.RadioSelect
    )
    question_10 = models.StringField(
        choices=["A", "B", "C", "D"],
        widget=widgets.RadioSelect
    )

    stem_quiz_1_answers = models.StringField()
    stem_quiz_1_score = models.FloatField()
    numTabSwitches = models.IntegerField()
    totalTimeHidden = models.FloatField()

    def get_quiz_answers(self):
        return [self.question_1, self.question_2, self.question_3, self.question_4,
                self.question_5, self.question_6, self.question_7, self.question_8,
                self.question_9, self.question_10]
    
    def calculate_score(self):
        user_answers = self.participant.vars['stem_quiz_1_answers']
        parsed_questions = StemQ.vars_for_template(self)['parsed_questions']
        score = 0
        for i, question in enumerate(parsed_questions):
            if user_answers[i] == question['correct_answer']:
                score += 1/len(parsed_questions)
        return score
        
# PAGES
class StemQ(Page):
    form_model = 'player'
    form_fields = ['question_1', 'question_2', 'question_3', 'question_4', 
                   'question_5', 'question_6', 'question_7', 'question_8', 
                   'question_9', 'question_10', 'numTabSwitches', 'totalTimeHidden']
    timeout_seconds = 480
    
    def before_next_page(player, timeout_happened):
        player.participant.vars['stem_quiz_1_answers'] = player.get_quiz_answers()  
        player.participant.vars['stem_quiz_1_score'] = player.calculate_score()
        player.participant.vars['numTabSwitches'] = player.numTabSwitches
        player.participant.vars['totalTimeHidden'] = player.totalTimeHidden

    def extract_file_id(url):
        file_id_start = url.find('/d/') + 3
        file_id_end = url.find('/view')
        return url[file_id_start:file_id_end]
    
    def reformat_img_url(url):
        img_id = StemQ.extract_file_id(url)
        return f'https://drive.google.com/thumbnail?id={img_id}&sz=w1000'

    def vars_for_template(self):
        with open('/Users/mimizhcj/OTreeExperiment/stemQuiz1/stemQ.csv', 'r') as file:
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
                'image_url': StemQ.reformat_img_url(question['image_url']), 
            }
            parsed_questions.append(parsed_question)
        return {'parsed_questions': parsed_questions}
    
class ResultsWaitPage(WaitPage):
    pass

class Results(Page):
    pass

page_sequence = [StemQ]
