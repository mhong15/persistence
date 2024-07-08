from otree.api import *
import csv
import json


doc = """
Second Optional Stem Quiz to take
"""
# Extract file_id from the URL

class C(BaseConstants):
    NAME_IN_URL = 'StemQuiz2'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1

class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    question1 = models.StringField(
        choices=["A", "B", "C", "D"],
        widget=widgets.RadioSelect
    )
    question2 = models.StringField(
        choices=["A", "B", "C", "D"],
        widget=widgets.RadioSelect
    )
    question3 = models.StringField(
        choices=["A", "B", "C", "D"],
        widget=widgets.RadioSelect
    )
    question4 = models.StringField(
        choices=["A", "B", "C", "D"],
        widget=widgets.RadioSelect
    )
    question5 = models.StringField(
        choices=["A", "B", "C", "D"],
        widget=widgets.RadioSelect
    )
    question6 = models.StringField(
        choices=["A", "B", "C", "D"],
        widget=widgets.RadioSelect
    )
    question7 = models.StringField(
        choices=["A", "B", "C", "D"],
        widget=widgets.RadioSelect
    )
    question8 = models.StringField(
        choices=["A", "B", "C", "D"],
        widget=widgets.RadioSelect
    )
    question9 = models.StringField(
        choices=["A", "B", "C", "D"],
        widget=widgets.RadioSelect
    )
    question10 = models.StringField(
        choices=["A", "B", "C", "D"],
        widget=widgets.RadioSelect
    )

    quiz_2_answers = models.StringField()
    quiz_2_score = models.FloatField()
    preferred_second_survey = models.StringField(choices=['STEM', 'Non-STEM'])
    parsed_questions = models.StringField()
    numTabSwitches2 = models.IntegerField()
    totalTimeHidden2 = models.FloatField()

    def get_quiz_answers(self):
        return [self.question1, self.question2, self.question3, self.question4,
                self.question5, self.question6, self.question7, self.question8,
                self.question9, self.question10]
    
    def calculate_score(self):
        user_answers = self.participant.vars['quiz_2_answers'].split(',')
        if self.participant.vars['preferred_second_survey'] == 'STEM':
            parsed_questions = StemQ.vars_for_template(self)['parsed_questions']
        else:
            parsed_questions = NonStemQuiz.vars_for_template(self)['parsed_questions']

        score = 0
        for i, question in enumerate(parsed_questions):
            print(i, user_answers[i], question['correct_answer'])
            if user_answers[i] == question['correct_answer']:
                score += 1/len(parsed_questions)
        return score

# PAGES
class ChooseQuiz(Page):
    form_model = 'player'
    form_fields = ['preferred_second_survey']

    def is_displayed(player):
        return True
    def before_next_page(player, timeout_happened):
        player.participant.vars['preferred_second_survey'] = player.preferred_second_survey

class StemQ(Page):
    timeout_seconds = 480
    form_model = 'player'
    form_fields = ['question1', 'question2', 'question3', 'question4', 
                   'question5', 'question6', 'question7', 'question8', 
                   'question9', 'question10', 'numTabSwitches2', 'totalTimeHidden2']
    
    def is_displayed(player):
        return player.preferred_second_survey == 'STEM'
    
    def extract_file_id(url):
        file_id_start = url.find('/d/') + 3
        file_id_end = url.find('/view')
        return url[file_id_start:file_id_end]
    
    def reformat_img_url(url, size):
        img_id = StemQ.extract_file_id(url)
        return f'https://drive.google.com/thumbnail?id={img_id}&sz=w{size}'


    def vars_for_template(self):
        with open('/Users/mimizhcj/OTreeExperiment/Branch2/stemQ.csv', 'r') as file:
            questions_data = list(csv.DictReader(file))

        # Process questions and return as a dictionary to the template
        parsed_questions = []
        for question in questions_data:
            # Process each row from CSV to get necessary information
            parsed_question = {
                'question_text': question['question_text'],
                'options': [
                    question['option_1'],
                    question['option_2'],
                    question['option_3'],
                    question['option_4'],
                ],
                'correct_answer': (question['correct_answer']),  # Assuming the correct answer is represented as an integer
                'image_url': StemQ.reformat_img_url(question['image_url'], '1000'),  # Assuming 'image_url' is a column in your CSV
                # Add more attributes as per your CSV columns
            }
            parsed_questions.append(parsed_question)
        return {'parsed_questions': parsed_questions}
     
    def before_next_page(player, timeout_happened):
        # Store the parsed questions in the player's session
        player.participant.vars['quiz_2_answers'] = ",".join(player.get_quiz_answers())
        player.participant.vars['quiz_2_score'] = player.calculate_score()
        player.participant.vars['numTabSwitches2'] = player.numTabSwitches2
        player.participant.vars['totalTimeHidden2'] = player.totalTimeHidden2

class NonStemQuiz(Page):
    timeout_seconds = 480
    form_model = 'player'
    form_fields = ['question1', 'question2', 'question3', 'question4', 
                   'question5', 'question6', 'question7', 'question8', 
                   'question9', 'question10', 'numTabSwitches2', 'totalTimeHidden2']

    def is_displayed(player):
        return player.preferred_second_survey == 'Non-STEM'
    
    def vars_for_template(self):
        with open('/Users/mimizhcj/OTreeExperiment/Branch2/nonStemQuiz.csv', 'r') as file:
            questions_data = list(csv.DictReader(file))

        # Process questions and return as a dictionary to the template
        parsed_questions = []
        for question in questions_data:
            # Process each row from CSV to get necessary information
            parsed_question = {
                'question_text': question['question_text'],
                'options': [
                    question['option_1'],
                    question['option_2'],
                    question['option_3'],
                    question['option_4'],
                ],
                'correct_answer': (question['correct_answer']),  # Assuming the correct answer is represented as an integer
                'image_url': StemQ.reformat_img_url(question['image_url'], '200'),  # Assuming 'image_url' is a column in your CSV
                # Add more attributes as per your CSV columns
            }
            parsed_questions.append(parsed_question)
        return {'parsed_questions': parsed_questions}
    
    def before_next_page(player, timeout_happened):
        # Store the parsed questions in the player's session
        player.participant.vars['quiz_2_answers'] = ",".join(player.get_quiz_answers())
        player.participant.vars['quiz_2_score'] = player.calculate_score()
        player.participant.vars['numTabSwitches2'] = player.numTabSwitches2
        player.participant.vars['totalTimeHidden2'] = player.totalTimeHidden2

class ResultsWaitPage(WaitPage):
    pass

class Results(Page):
    pass

page_sequence = [ChooseQuiz, StemQ, NonStemQuiz]
