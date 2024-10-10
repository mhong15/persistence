from otree.api import Page
from otree.api import *
import csv
import json
import random

class C(BaseConstants):
    NAME_IN_URL = 'Exp2_Section_2_3'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass

class Player(BasePlayer):
    track = models.StringField(choices=['noisy'])
    path = models.StringField(choices=['deterministic', 'explanation'])
    preferred_info_structure = models.StringField(
        choices=['Choice A','Choice B'],
        label="Select the choice that you prefer to get feedback from: ")
    performance = models.StringField(choices=['Pass', 'Fail'])
    ball_color = models.StringField(choices=['red', 'black'])
    overplacement = models.IntegerField(min=0, max=100)
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
        player.path = 'explanation'

        print(player.participant.vars['stem_quiz_1_score'], player.passing_threshold)
        if player.participant.vars['stem_quiz_1_score'] * 10 >= player.passing_threshold:
            player.performance = "Pass"
        else:
            player.performance = "Fail"

        player.participant.vars['track'] = player.track
        player.participant.vars['path'] = player.path
        player.participant.vars['performance'] = player.performance



class Conclusion_Section_2(Page):
    form_model = 'player'

class Section_3(Page):
    form_model = 'player'
    form_fields = ['preferred_info_structure']

    def before_next_page(player, timeout_happened):
        if player.preferred_info_structure == 'Choice A':
            if (player.performance == 'Pass'):
                if random.random() < 0.5:
                    player.ball_color = 'red'
                else:
                    player.ball_color = 'black'
            else:
                player.ball_color = 'red'
        else:
            if (player.performance == 'Fail'):
                if random.random() < 0.5:
                    player.ball_color = 'red'
                else:
                    player.ball_color = 'black'
            else:
                player.ball_color = 'red'
    
class Section_3A(Page):
    form_model = 'player'
    form_fields = ["ball_origin_estimation"]

    def is_displayed(player):
        return player.preferred_info_structure == 'Choice A'
    
class Section_3B(Page):
    form_model = 'player'
    form_fields = ["ball_origin_estimation"]

    def is_displayed(player):
        return player.preferred_info_structure == 'Choice B'

class Conclusion_Section_3(Page):
    form_model = 'player'
    def is_displayed(player):
        player.participant.vars['ball_color'] = player.ball_color
        player.participant.vars['ball_origin_estimation'] = player.ball_origin_estimation
    
        return True


page_sequence = [
    Section_2,
    Conclusion_Section_2,
    Section_3,
    Section_3A,
    Section_3B,
    Conclusion_Section_3
]

  