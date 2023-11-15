from otree.api import *


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


class ResultsWaitPage(WaitPage):
    pass


class Results(Page):
    pass


page_sequence = [MyPage, ResultsWaitPage, Results]
