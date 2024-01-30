from otree.api import *
import csv
import json


doc = """
first STEM Quiz players take.
"""
# Extract file_id from the URL


class C(BaseConstants):
    NAME_IN_URL = 'stemQuiz1'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # Section 1, Math Questions
    math1 = models.StringField(
        choices = [['A', '2^3'],
            ['B', '\\sqrt{16}'],
            ['C', '\\frac{1}{2} \\times 4']],
        label='What is the value of \(2^3\), \(\\sqrt{16}\), or \(\frac{1}{2} \\times 4\)?',
        widget=widgets.RadioSelect,
    )



# PAGES
class MyPage(Page):
    form_model = 'player'
    form_fields = ['math1']


class StemQ(Page):
    def before_next_page(self, timeout_happened):
        # Store the parsed questions in the player's vars
        #self.player.vars['parsed_questions'] = self.vars['parsed_questions']
        pass

    def extract_file_id(url):
        file_id_start = url.find('/d/') + 3
        file_id_end = url.find('/view')
        return url[file_id_start:file_id_end]
    
    def reformat_img_url(url):
        img_id = StemQ.extract_file_id(url)
        return f'https://drive.google.com/uc?export=view&id={img_id}'

    def vars_for_template(self):
        with open('/Users/mimizhcj/OTreeExperiment/stemQuiz1/stemQ.csv', 'r') as file:
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
            print(parsed_question)
            parsed_questions.append(parsed_question)

        return {'parsed_questions': parsed_questions}

class ResultsWaitPage(WaitPage):
    pass


class Results(Page):
    pass


page_sequence = [StemQ]
