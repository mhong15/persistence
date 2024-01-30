from otree.api import Page
from otree.api import *
import csv
import json
import random
doc = """
Post Quiz Survey that all players take
"""

class C(BaseConstants):
    NAME_IN_URL = 'PostQuizSurvey'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    track = models.StringField(choices=['noisy', 'comparative'])
    path = models.StringField(choices=['deterministic', 'explanation'])
    info_structure = models.StringField(choices=['ground', 'positive', 'negative'])
    preferred_info_structure = models.StringField(choices=['positive','negative'])
    performance = models.StringField(choices=['Top50%', 'Bottom50%', 'Better', 'Worse'])
    ball_color = models.StringField(choices=['red', 'black'])

class PostQuizSurvey(Page):
    timeout_seconds = 300

    def before_next_page(player, timeout_happened):
        # Randomly assign the participant to a track
        # player.track = 'comparative'
        # player.path = 'explanation'
        player.performance = 'Better'
        player.track = 'noisy'
        player.path = 'explanation'
        # player.track = random.choice(['noisy', 'comparative'])
        # player.path = random.choice(['random', 'explanation'])
        if (player.path == 'random'):
            player.info_structure = random.choice(['ground', 'positive', 'negative'])
            player.participant.vars['info_structure'] = player.info_structure

        # Store the tracks in the player's session
        player.participant.vars['track'] = player.track
        player.participant.vars['path'] = player.path
        print("END of PostQuizSurvey", player.track, player.path)

# If player is on explanation path, then we need an additional page to explain the game
class NoisyExplanation(Page):
    #timeout_seconds = 180
    form_model = 'player'
    form_fields = ['preferred_info_structure']
    
    def is_displayed(player):
        print(player.track, player.path)
        return player.track == 'noisy' and player.path == 'explanation'
    
    def before_next_page(player, timeout_happened):
        # Flip a coin to determine whether to use the preferred information structure
        if random.random() < 0.5:
            player.info_structure = player.preferred_info_structure
        elif player.preferred_info_structure == "positive":
            player.info_structure = "negative"
        else:
            player.info_structure = "positive"

class ComparativeExplanation(Page):
    #timeout_seconds = 180
    form_model = 'player'
    form_fields = ['preferred_info_structure']
    def is_displayed(player):
        print(player.track, player.path)
        return player.track == 'comparative' and player.path == 'explanation'

    def before_next_page(player, timeout_happened):
        # Flip a coin to determine whether to use the preferred information structure
        if random.random() < 0.5:
            print(player.preferred_info_structure)
            player.info_structure = player.preferred_info_structure
        elif player.preferred_info_structure == "positive":
            player.info_structure = "negative"
        else:
            player.info_structure = "positive"
    
# Information treatments
class NoisyPositive(Page):
    #timeout_seconds = 180
    def is_displayed(player):
        print(player.track, player.path)
        return player.track == 'noisy' and player.info_structure == 'positive'
    def before_next_page(player, timeout_happened):
        if (player.performance == 'Top50%'):
            if random.random() < 0.5:
                player.ball_color = 'red'
            else:
                player.ball_color = 'black'
        else:
            player.ball_color = 'red'
    
class NoisyNegative(Page):
    timeout_seconds = 180
    def is_displayed(player):
        print(player.track, player.path)
        return player.track == 'noisy'  and player.info_structure == 'negative'
    
    def before_next_page(player, timeout_happened):
        if (player.performance == 'Bottom50%'):
            if random.random() < 0.5:
                player.ball_color = 'red'
            else:
                player.ball_color = 'black'
        else:
            player.ball_color = 'red'
class ComparativePositive(Page):
    #timeout_seconds = 180
    def is_displayed(player):
        return player.track == 'comparative' and player.info_structure == 'positive'
    def before_next_page(player, timeout_happened):
        if (player.performance == 'Better'):
            if random.random() < 0.5:
                player.ball_color = 'red'
            else:
                player.ball_color = 'black'
        else:
            player.ball_color = 'red'
    
class ComparativeNegative(Page):
    #timeout_seconds = 180
    def is_displayed(player):
        return player.track == 'comparative' and player.info_structure == 'negative'
    def before_next_page(player, timeout_happened):
        if (player.performance == 'Worse%'):
            if random.random() < 0.5:
                player.ball_color = 'red'
            else:
                player.ball_color = 'black'
        else:
            player.ball_color = 'red'
    
class Feedback(Page):
    #timeout_seconds = 180
    form_model = 'player'
    def is_displayed(player):
        return True
    
page_sequence = [
    PostQuizSurvey,
    NoisyExplanation,
    ComparativeExplanation,
    NoisyPositive,
    NoisyNegative,
    ComparativePositive,
    ComparativeNegative,
    Feedback
]

  