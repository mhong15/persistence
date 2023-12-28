from otree.api import *
import csv
import json


doc = """
Optional language quiz
"""


class C(BaseConstants):
    NAME_IN_URL = 'langQuiz'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    quiz_score = models.IntegerField(initial=0)

# PAGES
class csvTest(Page):
    def vars_for_template(self):
        with open('/Users/mimizhcj/OTreeExperiment/langQuiz/langQ.csv', 'r') as file:
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
                'correct_answer': int(question['correct_answer']),  # Assuming the correct answer is represented as an integer
                'image_url': question['image_url'],  # Assuming 'image_url' is a column in your CSV
                # Add more attributes as per your CSV columns
            }
            parsed_questions.append(parsed_question)

        return {'parsed_questions': parsed_questions}
    def before_next_page(self):
        # Store the parsed questions in the player's session
        self.player.participant.vars['parsed_questions'] = self.vars['parsed_questions']

class PartB(Page):
    form_model = 'player'
    form_fields = ['lang20', 'lang21', 'lang22', 'lang23', 'lang24', 'lang25', 'lang26',
                    'lang27', 'lang28', 'lang29', 'lang30']


class Results(Page):
    pass


page_sequence = [csvTest]
