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
    quiz = models.StringField(choices=['STEM', 'Lang'])

# PAGES
class ChooseQuiz(Page):
    timeout_seconds = 60
    form_model = 'player'
    form_fields = ['quiz']
    def is_displayed(player):
        return True
    def before_next_page(player, timeout_happened):
        # Flip a coin to determine whether to use the preferred information structure
        player.quiz = player.quiz

class StemQ(Page):
    timeout_seconds = 60
    form_model = 'player'
    def is_displayed(player):
        return player.quiz == 'STEM'
    
    def extract_file_id(url):
        file_id_start = url.find('/d/') + 3
        file_id_end = url.find('/view')
        return url[file_id_start:file_id_end]
    
    def reformat_img_url(url):
        img_id = StemQ.extract_file_id(url)
        print(f'https://drive.google.com/uc?export=view&id={img_id}')
        return f'https://drive.google.com/uc?export=view&id={img_id}'

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
                'image_url': StemQ.reformat_img_url(question['image_url']),  # Assuming 'image_url' is a column in your CSV
                # Add more attributes as per your CSV columns
            }
            parsed_questions.append(parsed_question)

        return {'parsed_questions': parsed_questions}
     
    def before_next_page(self, timeout_happened):
        # Store the parsed questions in the player's session
       # self.player.participant.vars['parsed_questions'] = self.vars['parsed_questions']
        pass

class LangQuiz(Page):
    timeout_seconds = 60
    form_model = 'player'
    def is_displayed(player):
        return player.quiz == 'Lang'
    
    def vars_for_template(self):
        with open('/Users/mimizhcj/OTreeExperiment/Branch2/langQuiz.csv', 'r') as file:
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
    def before_next_page(self, timeout_happened):
        # Store the parsed questions in the player's session
        pass
        #self.player.participant.vars['parsed_questions'] = self.vars['parsed_questions']


class ResultsWaitPage(WaitPage):
    pass


class Results(Page):
    pass


page_sequence = [ChooseQuiz, StemQ, LangQuiz]
