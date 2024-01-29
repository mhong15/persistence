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

class PostQuizSurvey(Page):
    timeout_seconds = 300

    def before_next_page(player, timeout_happened):
        # Randomly assign the participant to a track
        player.track = 'noisy'
        player.path = 'explanation'
        # self.track = random.choice(['noisy', 'comparative'])
        # self.path = random.choice(['random', 'explanation'])
        # if (self.path == 'random'):
        #     self.info_structure = random.choice(['ground', 'positive', 'negative'])
        #     self.participant.vars['info_structure'] = self.info_structure

        # # Store the tracks in the player's session
        # self.participant.vars['track'] = self.track
        # self.participant.vars['path'] = self.path
        print("END of PostQuizSurvey", player.track, player.path)

# If player is on explanation path, then we need an additional page to explain the game
class NoisyExplanation(Page):
    timeout_seconds = 60
    form_model = 'player'
    form_fields = ['preferred_info_structure']
    preferred_info_structure = models.StringField(label="What is your preferred information structure?")
    preferred_info_structure.widget = widgets.RadioSelect
    
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
    timeout_seconds = 60
    def is_displayed(player):
        print(player.track, player.path)
        return player.track == 'comparative' and player.path == 'explanation'

    def before_next_page(self, timeout_happened):
        # Get the preferred information structure from the HTML form
        preferred_info_structure = self.request.POST.get('preferred_info_structure')

        # Store the preferred information structure in the player
        self.player.preferred_info_structure = preferred_info_structure

        # Flip a coin to determine whether to use the preferred information structure
        if random.random() < 0.5:
            self.player.info_structure = preferred_info_structure
        elif self.player.preferred_info_structure == "positive":
            self.player.info_structure = "negative"
        else:
            self.player.info_structure = "positive"
    
# Information treatments
class NoisyGround(Page):
    timeout_seconds = 60
    def is_displayed(player):
        print(player.track, player.path)
        return player.track == 'noisy' and player.info_structure == 'ground'
    
class NoisyPositive(Page):
    timeout_seconds = 60
    def is_displayed(player):
        print(player.track, player.path)
        return player.track == 'noisy' and player.info_structure == 'positive'
    
class NoisyNegative(Page):
    timeout_seconds = 60
    def is_displayed(player):
        print(player.track, player.path)
        return player.track == 'noisy'  and player.info_structure == 'negative'
    
class ComparativeGround(Page):
    timeout_seconds = 60
    def is_displayed(player):
        return player.track == 'comparative' and player.info_structure == 'ground'
    
class ComparativePositive(Page):
    timeout_seconds = 60
    def is_displayed(player):
        return player.track == 'comparative' and player.info_structure == 'positive'
    
class ComparativeNegative(Page):
    timeout_seconds = 60
    def is_displayed(player):
        return player.track == 'comparative' and player.info_structure == 'negative'

class Feedback(Page):
    pass

page_sequence = [
    PostQuizSurvey,
    NoisyExplanation,
    ComparativeExplanation,
]

    # NoisyGround,
    # NoisyPositive,
    # NoisyNegative,
    # ComparativeGround,
    # ComparativePositive,
    # ComparativeNegative,
    # Feedback