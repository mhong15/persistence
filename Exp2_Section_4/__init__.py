from otree.api import *
import csv
import json
import os
import random

class C(BaseConstants):
    NAME_IN_URL = 'Exp2_Section_4'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass

class Player(BasePlayer):

    schools_private_independent = models.BooleanField(blank=True, initial=False)
    schools_private_religious = models.BooleanField(blank=True, initial=False)
    schools_public_school = models.BooleanField(blank=True, initial=False)
    schools_homeschool = models.BooleanField(blank=True, initial=False)
    schools_online_school = models.BooleanField(blank=True, initial=False)
    schools_charter_school = models.BooleanField(blank=True, initial=False)
    schools_all_girls_school = models.BooleanField(blank=True, initial=False)
    schools_all_boys_school = models.BooleanField(blank=True, initial=False)
    schools_stem_oriented_school = models.BooleanField(blank=True, initial=False)

    subjects = models.LongStringField(blank=True, initial=False)
    experience = models.LongStringField(blank=True, initial=False)
    

# PAGES
class Section_4(Page):
    form_model = 'player'
    form_fields = ['schools_private_independent', 
                  'schools_private_religious', 
                  'schools_public_school',
                  'schools_homeschool',
                  'schools_online_school',
                  'schools_charter_school',
                  'schools_all_girls_school',
                  'schools_all_boys_school',
                  'schools_stem_oriented_school',
                  'subjects', 
                  'experience']

    def is_displayed(player):
        return True
    
    def before_next_page(player, timeout_happened):
        schools = ["schools_private_independent", "schools_private_religious",
                   "schools_public_school", "schools_homeschool", "schools_online_school",
                   "schools_charter_school", "schools_all_girls_school", "schools_all_boys_school",
                   "schools_stem_oriented_school"]

        for school in schools:
            Section_4.store_check_box(player, school)
    
        player.participant.vars['subjects'] = player.subjects
        player.participant.vars['experience'] = player.experience

        print("End Survey Vars:\n", player.participant.vars)
        Section_4.export_experiment_data(player)

    def store_check_box(player, field):
        field_value = getattr(player, field)
        player.participant.vars[field] = field_value

    def export_experiment_data(player):
        vars = player.participant.vars
        for key in ['stem_quiz_1_answers', 'stem_quiz_1_score', 'num_tab_switches_in_section_1', 'total_time_hidden_in_section_1']:
            if key in vars:
                if type(vars[key]) == float or type(vars[key]) == int or type(vars[key]) == str:
                    vars[key] = str(vars[key])
                else:
                    vars[key] = list(vars[key]) 

        relative_csv_file = 'experiment_data.csv'
        current_directory = os.getcwd()
        absolute_csv_file = os.path.join(current_directory, relative_csv_file)

        if os.path.exists(absolute_csv_file):
            with open(absolute_csv_file, 'a', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=vars.keys(), delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
            
                writer.writerow(vars)
        else:
            with open(absolute_csv_file, 'w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=vars.keys(), delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
        
                writer.writeheader()
                writer.writerow(vars)

class EndSurvey(Page):
    def before_next_page(player, timeout_happened):
        pass

    def vars_for_template(player):
        return {
            'return_url': player.session.config.get('return_url')
        }


page_sequence = [Section_4, EndSurvey]