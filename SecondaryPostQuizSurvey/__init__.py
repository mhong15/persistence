from otree.api import *
import csv
import json


doc = """
Post Experiment Survey aka Secondary Post Quiz Survey
"""
# Extract file_id from the URL


class C(BaseConstants):
    NAME_IN_URL = 'SecondaryPostQuizSurvey'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass

# PAGES
class SecondaryPostQuizSurvey(Page):
    def before_next_page(self, timeout_happened):
        pass


class ResultsWaitPage(WaitPage):
    pass


class Results(Page):
    pass


page_sequence = [SecondaryPostQuizSurvey]
