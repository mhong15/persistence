from os import environ
import os

SESSION_CONFIGS = [
    dict(
        name='Quiz',
        app_sequence=['Intro', 'Section_1', 'Section_2_3', 'Section_4_5', 'Section_6', 'Section_7'],
        num_demo_participants=1,
        return_url="https://app.prolific.com/submissions/complete?cc=C1BTHULB" # Create a new page that redirects to the prolific url
    ),
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except thosep that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=0.00, doc=""
)



# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = '5628757875766'

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

STATIC_URL = '/static/'

# Include your custom static directory
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'Section_1/static'),
]