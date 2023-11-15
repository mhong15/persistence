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
        choices=[['Risk', '50% chance of $10'], ['Constant', 'Guarenteed $0']],
        label='50% chance of winning 10$ or receive a guarenteed $0?',
        widget=widgets.RadioSelect,
    )
    question2 = models.StringField(
        choices=[['Risk', '50% chance of $10'], ['Constant', 'Guarenteed $1']],
        label='50% chance of winning 10$ or receive a guarenteed $1?',
        widget=widgets.RadioSelect,
    )
    question3 = models.StringField(
        choices=[['Risk', '50% chance of $10'], ['Constant', 'Guarenteed $2']],
        label='50% chance of winning 10$ or receive a guarenteed $2?',
        widget=widgets.RadioSelect,
    )
    question4 = models.StringField(
        choices=[['Risk', '50% chance of $10'], ['Constant', 'Guarenteed $3']],
        label='50% chance of winning 10$ or receive a guarenteed $3?',
        widget=widgets.RadioSelect,
    )
    question5 = models.StringField(
        choices=[['Risk', '50% chance of $10'], ['Constant', 'Guarenteed $4']],
        label='50% chance of winning 10$ or receive a guarenteed $4?',
        widget=widgets.RadioSelect,
    )
    question6 = models.StringField(
        choices=[['Risk', '50% chance of $10'], ['Constant', 'Guarenteed $5']],
        label='50% chance of winning 10$ or receive a guarenteed $5?',
        widget=widgets.RadioSelect,
    )
    question7 = models.StringField(
        choices=[['Risk', '50% chance of $10'], ['Constant', 'Guarenteed $6']],
        label='50% chance of winning 10$ or receive a guarenteed $6?',
        widget=widgets.RadioSelect,
    )
    question8 = models.StringField(
        choices=[['Risk', '50% chance of $10'], ['Constant', 'Guarenteed $7']],
        label='50% chance of winning 10$ or receive a guarenteed $7?',
        widget=widgets.RadioSelect,
    )
    question9 = models.StringField(
        choices=[['Risk', '50% chance of $10'], ['Constant', 'Guarenteed $8']],
        label='50% chance of winning 10$ or receive a guarenteed $8?',
        widget=widgets.RadioSelect,
    )
    question10 = models.StringField(
        choices=[['Risk', '50% chance of $10'], ['Constant', 'Guarenteed $9']],
        label='50% chance of winning 10$ or receive a guarenteed $9?',
        widget=widgets.RadioSelect,
    )
    question11 = models.StringField(
        choices=[['Risk', '50% chance of $10'], ['Constant', 'Guarenteed $10']],
        label='50% chance of winning 10$ or receive a guarenteed $10?',
        widget=widgets.RadioSelect,
    )
    
    def check_answer(self):
        # Implement logic to check if the answer is correct and record the result
        pass


# FUNCTIONS
# PAGES
class RiskToleranceQuiz(Page):
    form_model = 'player'
    form_fields = ['question1', 'question2', 'question3', 'question4','question5', 
                   'question6', 'question7', 'question8', 'question9', 'question10',
                   'question11']
    
class Quiz1(Page):
    form_model = 'player'
    form_fields = ['answer1']

    def before_next_page(self):
        self.player.check_answer()

        # Create a new PlayerResponse object
        models.PlayerResponse.objects.create(
            player=self.player,
            question_number=1,
            response=self.player.answer1
         )


page_sequence = [RiskToleranceQuiz]
