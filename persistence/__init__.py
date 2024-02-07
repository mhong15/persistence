from otree.api import *

class C(BaseConstants):
    NAME_IN_URL = 'risktolerance'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass

class Player(BasePlayer):
    # Risk Tolerance Quiz: Would you rather?
    question1 = models.StringField(
        choices=[['R', '50% chance of $10'], ['C', 'Guaranteed $0']],
        label='50% chance of winning $10 or receive a guaranteed $0?',
        widget=widgets.RadioSelect,
    )
    question2 = models.StringField(
        choices=[['R', '50% chance of $10'], ['C', 'Guaranteed $1']],
        label='50% chance of winning $10 or receive a guaranteed $1?',
        widget=widgets.RadioSelect,
    )
    question3 = models.StringField(
        choices=[['R', '50% chance of $10'], ['C', 'Guaranteed $2']],
        label='50% chance of winning $10 or receive a guaranteed $2?',
        widget=widgets.RadioSelect,
    )
    question4 = models.StringField(
        choices=[['R', '50% chance of $10'], ['C', 'Guaranteed $3']],
        label='50% chance of winning $10 or receive a guaranteed $3?',
        widget=widgets.RadioSelect,
    )
    question5 = models.StringField(
        choices=[['R', '50% chance of $10'], ['C', 'Guaranteed $4']],
        label='50% chance of winning $10 or receive a guaranteed $4?',
        widget=widgets.RadioSelect,
    )
    question6 = models.StringField(
        choices=[['R', '50% chance of $10'], ['C', 'Guaranteed $5']],
        label='50% chance of winning $10 or receive a guaranteed $5?',
        widget=widgets.RadioSelect,
    )
    question7 = models.StringField(
        choices=[['R', '50% chance of $10'], ['C', 'Guaranteed $6']],
        label='50% chance of winning $10 or receive a guaranteed $6?',
        widget=widgets.RadioSelect,
    )
    question8 = models.StringField(
        choices=[['R', '50% chance of $10'], ['C', 'Guaranteed $7']],
        label='50% chance of winning $10 or receive a guaranteed $7?',
        widget=widgets.RadioSelect,
    )
    question9 = models.StringField(
        choices=[['R', '50% chance of $10'], ['C', 'Guaranteed $8']],
        label='50% chance of winning $10 or receive a guaranteed $8?',
        widget=widgets.RadioSelect,
    )
    question10 = models.StringField(
        choices=[['R', '50% chance of $10'], ['C', 'Guaranteed $9']],
        label='50% chance of winning $10 or receive a guaranteed $9?',
        widget=widgets.RadioSelect,
    )
    question11 = models.StringField(
        choices=[['R', '50% chance of $10'], ['C', 'Guaranteed $10']],
        label='50% chance of winning $10 or receive a guaranteed $10?',
        widget=widgets.RadioSelect,
    )

    risk_tolerance_answers = models.StringField()

    def get_form_fields(self):
        return [self.question1, self.question2, self.question3, self.question4, 
                self.question5, self.question6, self.question7, self.question8, 
                self.question9, self.question10, self.question11]


    def check_answer(self):
        # Implement logic to check if the answer is correct and record the result
        pass    

# PAGES
class RiskToleranceQuiz(Page):
    form_model = 'player'
    form_fields = ['question1', 'question2', 'question3', 'question4', 
                   'question5', 'question6', 'question7', 'question8', 
                   'question9', 'question10', 'question11']

    def before_next_page(self, timeout_happened):
        self.participant.vars['risk_tolerance_answers'] = "".join(self.get_form_fields())


class ResultsWaitPage(WaitPage):
    def after_all_players_arrive(self):
        pass  # You can use this if you need to do something after all players have finished the page

page_sequence = [RiskToleranceQuiz, ResultsWaitPage]
