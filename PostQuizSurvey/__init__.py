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

class PostQuizSurvey(Page):
    timeout_seconds = 300

    def before_next_page(self, timeout_happened):
        # Randomly assign the participant to a track
        self.track = random.choice(['noisy', 'comparative'])
        self.path = random.choice(['random', 'explanation'])
        if (self.path == 'random'):
            self.info_structure = random.choice(['ground', 'positive', 'negative'])
            self.participant.vars['info_structure'] = self.info_structure

        # Store the tracks in the player's session
        self.participant.vars['track'] = self.track
        self.participant.vars['path'] = self.path
        print(self.track, self.path)

# If player is on explanation path, then we need an additional page to explain the game
class NoisyExplanation(Page):
    timeout_seconds = 60
    def is_displayed(self):
        print(self.player.track, self.player.path)
        return self.player.track == 'noisy' and self.player.path == 'explanation'
    
    def before_next_page(self):
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

class ComparativeExplanation(Page):
    timeout_seconds = 60
    def is_displayed(self):
        print(self.player.track, self.player.path)
        return self.player.track == 'comparative' and self.player.path == 'explanation'

    def before_next_page(self):
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
    def is_displayed(self):
        print(self.player.track, self.player.path)
        return self.player.track == 'noisy' and self.player.info_structure == 'ground'
    
class NoisyPositive(Page):
    timeout_seconds = 60
    def is_displayed(self):
        print(self.player.track, self.player.path)
        return self.player.track == 'noisy' and self.player.info_structure == 'positive'
    
class NoisyNegative(Page):
    timeout_seconds = 60
    def is_displayed(self):
        print(self.player.track, self.player.path)
        return self.player.track == 'noisy'  and self.player.info_structure == 'negative'
    
class ComparativeGround(Page):
    timeout_seconds = 60
    def is_displayed(self):
        return self.player.track == 'comparative' and self.player.info_structure == 'ground'
    
class ComparativePositive(Page):
    timeout_seconds = 60
    def is_displayed(self):
        return self.player.track == 'comparative' and self.player.info_structure == 'positive'
    
class ComparativeNegative(Page):
    timeout_seconds = 60
    def is_displayed(self):
        return self.player.track == 'comparative' and self.player.info_structure == 'negative'

class Feedback(Page):
    pass

page_sequence = [
    PostQuizSurvey,
    NoisyExplanation,
    ComparativeExplanation,
    NoisyGround,
    NoisyPositive,
    NoisyNegative,
    ComparativeGround,
    ComparativePositive,
    ComparativeNegative,
    Feedback
]
    


class ResultsWaitPage(WaitPage):
    pass


class Results(Page):
    pass


page_sequence = [PostQuizSurvey]
