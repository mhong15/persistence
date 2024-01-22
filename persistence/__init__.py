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
        choices=[['Risk', '50% chance of $10'], ['Constant', 'Guaranteed $0']],
        label='50% chance of winning $10 or receive a guaranteed $0?',
        widget=widgets.RadioSelect,
    )

    def check_answer(self):
        # Implement logic to check if the answer is correct and record the result
        pass

    def record_response(self, question_number, response):
        # Create a new PlayerResponse object
        # models.PlayerResponse.objects.create(
        #     player=self,
        #     question_number=question_number,
        #     response=response
        # )
        pass

    

# PAGES
class RiskToleranceQuiz(Page):
    form_model = 'player'
    form_fields = ['question1']

    def before_next_page(self, timeout_happened):
        self.check_answer()


class ResultsWaitPage(WaitPage):
    def after_all_players_arrive(self):
        pass  # You can use this if you need to do something after all players have finished the page

page_sequence = [RiskToleranceQuiz, ResultsWaitPage]
