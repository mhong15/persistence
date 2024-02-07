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

    stem_quiz_1_answers = models.StringField()
    stem_quiz_1_score = models.FloatField()

    def get_quiz_answers(self):
        return [self.question1, self.question2, self.question3, self.question4,
                self.question5, self.question6, self.question7, self.question8,
                self.question9, self.question10]
    
    def calculate_score(self):
        user_answers = self.participant.vars['stem_quiz_1_answers'].split(',')
        parsed_questions = StemQ.vars_for_template(self)['parsed_questions']
        score = 0
        for i, question in enumerate(parsed_questions):
            if user_answers[i] == question['correct_answer']:
                score += 1/len(parsed_questions)
        return score
        

# PAGES
class StemQ(Page):
    form_model = 'player'
    form_fields = ['question1', 'question2', 'question3', 'question4', 
                   'question5', 'question6', 'question7', 'question8', 
                   'question9', 'question10']
    timeout_seconds = 600

    def before_next_page(player, timeout_happened):
        print(player.get_quiz_answers())
    # Store the selected answers in participant.vars
        player.participant.vars['stem_quiz_1_answers'] = [getattr(player, f'question{i}') for i in range(1, 11)]
    # You can also calculate the score here if needed
    # self.participant.vars['stem_quiz_1_score'] = self.calculate_score()

        # self.participant.vars['stem_quiz_1_answers'] = "".join(self.get_quiz_answers())
        # self.participant.vars['stem_quiz_1_score'] = self.calculate_score()

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
        print(parsed_questions)
        return {'parsed_questions': parsed_questions}

class ResultsWaitPage(WaitPage):
    pass


class Results(Page):
    pass

page_sequence = [StemQ]
