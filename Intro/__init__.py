from otree.api import *

class C(BaseConstants):
    NAME_IN_URL = 'Intro'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass

class Player(BasePlayer):
    prolific_id = models.StringField(
        label='Please enter your Prolific ID:',
        blank=True
    )

# PAGES
class Intro(Page):
    form_model = 'player'
    form_fields = ['prolific_id']

    def before_next_page(player, timeout_happened):
        if player.prolific_id:
            player.participant.vars['prolific_id'] = player.prolific_id
        else:
            player.participant.vars['prolific_id'] = 'N/A'

page_sequence = [Intro]
