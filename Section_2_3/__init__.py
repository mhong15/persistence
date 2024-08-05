from otree.api import Page
from otree.api import *
import csv
import json
import random

class C(BaseConstants):
    NAME_IN_URL = 'Section_2_3'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass

class Player(BasePlayer):
    track = models.StringField(choices=['noisy'])
    path = models.StringField(choices=['deterministic', 'explanation'])
    info_structure = models.StringField(choices=['ground', 'positive', 'negative'])
    preferred_info_structure = models.StringField(choices=['positive','negative'])
    performance = models.StringField(choices=['Pass', 'Fail'])
    ball_color = models.StringField(choices=['red', 'black'])
    overplacement = models.IntegerField(min=1, max=500)
    overestimation = models.IntegerField(min=0, max=10)
    passing_threshold = models.IntegerField(min=0, max=10)
    ball_origin_estimation = models.StringField(
        choices=['Pass Box', 'Fail Box', 'Not Sure'],
        label="Please select the box that you think the hint came from:")

class Section_2(Page):
    form_model = 'player'
    form_fields = ['overplacement', 'overestimation', 'passing_threshold']

    def before_next_page(player, timeout_happened):
        player.participant.vars['overplacement'] = player.overplacement
        player.participant.vars['overestimation'] = player.overestimation
        player.participant.vars['passing_threshold'] = player.passing_threshold

        player.track = 'noisy'
        player.path = 'random'

        if player.participant.vars['stem_quiz_1_score'] >= player.passing_threshold:
            player.performance = "Pass"
        else:
            player.performance = "Fail"

        if (player.path == 'random'):
            player.info_structure = random.choice(['ground', 'positive', 'negative'])
            player.participant.vars['info_structure'] = player.info_structure

        player.participant.vars['track'] = player.track
        player.participant.vars['path'] = player.path
        player.participant.vars['performance'] = player.performance

class Conclusion_Section_2(Page):
    form_model = 'player'

class Section_3A(Page):
    form_model = 'player'
    form_fields = ['ball_origin_estimation']
    
    def is_displayed(player):
        if (player.performance == 'Pass'):   
            player.ball_color = 'red'
        else:
            player.ball_color = 'black'
        return player.track == 'noisy' and player.info_structure == 'ground'

class Section_3B(Page):
    form_model = 'player'
    form_fields = ['ball_origin_estimation']

    def is_displayed(player):
        if (player.performance == 'Fail'):
            if random.random() < 0.5:
                player.ball_color = 'red'
            else:
                player.ball_color = 'black'
        else:
            player.ball_color = 'red'
        return player.track == 'noisy' and player.info_structure == 'negative'
    

class Section_3C(Page):
    form_model = 'player'
    form_fields = ['ball_origin_estimation']

    def is_displayed(player):
        if (player.performance == 'Pass'):
            if random.random() < 0.5:
                player.ball_color = 'red'
            else:
                player.ball_color = 'black'
        else:
            player.ball_color = 'red'
        return player.track == 'noisy' and player.info_structure == 'positive'
    

class Conclusion_Section_3(Page):
    form_model = 'player'
    def is_displayed(player):
        player.participant.vars['ball_color'] = player.ball_color
        player.participant.vars['ball_origin_estimation'] = player.ball_origin_estimation
    
        return True


page_sequence = [
    Section_2,
    Conclusion_Section_2,
    Section_3A,
    Section_3B,
    Section_3C,
    Conclusion_Section_3
]

  