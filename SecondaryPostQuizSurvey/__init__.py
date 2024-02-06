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
    # Post Experiment Survey
    age = models.IntegerField(min=1, max=100)
    years_of_education = models.IntegerField(min=1, max=100)
    gender = models.StringField( 
        choices=['male', 'female', 'non-binary', 'other', 'prefer not to say'],
        widget=widgets.RadioSelect)
    
    race_asian = models.BooleanField(blank=True, initial=False)
    race_black_or_african_american = models.BooleanField(blank=True, initial=False)
    race_white = models.BooleanField(blank=True, initial=False)
    race_hispanic = models.BooleanField(blank=True, initial=False)
    race_native_american_or_alaska_native = models.BooleanField(blank=True, initial=False)

    schools_private_independent = models.BooleanField(blank=True, initial=False)
    schools_private_religious = models.BooleanField(blank=True, initial=False)
    schools_public_school = models.BooleanField(blank=True, initial=False)
    schools_homeschool = models.BooleanField(blank=True, initial=False)
    schools_online_school = models.BooleanField(blank=True, initial=False)
    schools_charter_school = models.BooleanField(blank=True, initial=False)
    schools_all_girls_school = models.BooleanField(blank=True, initial=False)
    schools_all_boys_school = models.BooleanField(blank=True, initial=False)
    schools_stem_oriented_school = models.BooleanField(blank=True, initial=False)

    current_teacher = models.LongStringField(blank=True, initial=False)
    experience = models.LongStringField(blank=True, initial=False)

# PAGES
class SecondaryPostQuizSurvey(Page):
    form_model = 'player'
    form_fields = ['age', 'years_of_education', 'gender', 
                  'race_asian', 
                  'race_black_or_african_american', 
                  'race_white', 
                  'race_hispanic', 
                  'race_native_american_or_alaska_native', 
                  'schools_private_independent', 
                  'schools_private_religious', 
                  'schools_public_school',
                  'schools_homeschool',
                  'schools_online_school',
                  'schools_charter_school',
                  'schools_all_girls_school',
                  'schools_all_boys_school',
                  'schools_stem_oriented_school',
                  'current_teacher', 
                  'experience']

    def before_next_page(player, timeout_happened):
        player.participant.vars['age'] = player.age
        player.participant.vars['years_of_education'] = player.years_of_education
        player.participant.vars['gender'] = player.gender

        races = ["race_asian", "race_black_or_african_american", "race_white",
                 "race_hispanic", "race_native_american_or_alaska_native"]
        schools = ["schools_private_independent", "schools_private_religious",
                   "schools_public_school", "schools_homeschool", "schools_online_school",
                   "schools_charter_school", "schools_all_girls_school", "schools_all_boys_school",
                   "schools_stem_oriented_school"]
        for race in races:
            SecondaryPostQuizSurvey.store_check_box(player, race)
        for school in schools:
            SecondaryPostQuizSurvey.store_check_box(player, school)
    
        player.participant.vars['current_teacher'] = player.current_teacher
        player.participant.vars['experience'] = player.experience

        print("Vars:\n", player.participant.vars)

    def store_check_box(player, field):
        field_value = getattr(player, field)
        player.participant.vars[field] = field_value

class ResultsWaitPage(WaitPage):
    pass


class Results(Page):
    pass


page_sequence = [SecondaryPostQuizSurvey]
