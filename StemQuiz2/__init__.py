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
    pass

# PAGES
class StemQ(Page):
    def extract_file_id(url):
        file_id_start = url.find('/d/') + 3
        file_id_end = url.find('/view')
        return url[file_id_start:file_id_end]
    
    def reformat_img_url(url):
        img_id = StemQ.extract_file_id(url)
        return f'https://drive.google.com/uc?export=view&id={img_id}'

    def vars_for_template(self):
        with open('/Users/mimizhcj/OTreeExperiment/StemQuiz2/stemQ.csv', 'r') as file:
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


class ResultsWaitPage(WaitPage):
    pass


class Results(Page):
    pass


page_sequence = [StemQ]
