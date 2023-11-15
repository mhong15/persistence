from otree.api import *


doc = """
Optional language quiz
"""


class C(BaseConstants):
    NAME_IN_URL = 'langQuiz'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    lang1 = models.StringField(
        choices=[
            ['A', 'enthusiastic'],
            ['B', 'fortunate'],
            ['C', 'relieved'],
            ['D', 'unpredictable']
        ],
        label='ERRATIC',
        widget=widgets.RadioSelect,
    )
    lang2 = models.StringField(
        choices=[
            ['A', 'stacked'],
            ['B', 'strong'],
            ['C', 'lame'],
            ['D', 'ridiculous']
        ],
        label='VIGOROUS',
        widget=widgets.RadioSelect,
    )
    lang3 = models.StringField(
        choices=[
            ['A', 'confused'],
            ['B', 'disgraced'],
            ['C', 'inspired'],
            ['D', 'neglected']
        ],
        label='PUZZLED',
        widget=widgets.RadioSelect,
    )
    lang4 = models.StringField(
        choices=[
            ['A', 'authentic'],
            ['B', 'intricate'],
            ['C', 'livid'],
            ['D', 'persistent']
        ],
        label='IRATE',
        widget=widgets.RadioSelect,
    )
    lang5 = models.StringField(
        choices=[
            ['A', 'assure'],
            ['B', 'compliment'],
            ['C', 'annoy'],
            ['D', 'resemble']
        ],
        label='FLATTER',
        widget=widgets.RadioSelect,
    )
    lang6 = models.StringField(
        choices=[
            ['A', 'acknowledge'],
            ['B', 'imply'],
            ['C', 'confine'],
            ['D', 'ask']
        ],
        label='INQUIRE',
        widget=widgets.RadioSelect,
    )
    lang7 = models.StringField(
        choices=[
            ['A', 'change'],
            ['B', 'conceal'],
            ['C', 'reject'],
            ['D', 'uproot']
        ],
        label='ALTER',
        widget=widgets.RadioSelect,
    )
    lang8 = models.StringField(
        choices=[
            ['A', 'genuine'],
            ['B', 'spirited'],
            ['C', 'unique'],
            ['D', 'weary']
        ],
        label='FEISTY',
        widget=widgets.RadioSelect,
    )
    lang9 = models.StringField(
        choices=[
            ['A', 'astonish'],
            ['B', 'deceive'],
            ['C', 'reflect'],
            ['D', 'utilize']
        ],
        label='REMINISCE',
        widget=widgets.RadioSelect,
    )
    lang10 = models.StringField(
        choices=[
            ['A', 'lost'],
            ['B', 'hidden'],
            ['C', 'attached'],
            ['D', 'scattered']
        ],
        label='STREWN',
        widget=widgets.RadioSelect,
    )
    lang11 = models.StringField(
        choices=[
            ['A', 'sweat'],
            ['B', 'breathe'],
            ['C', 'encourage'],
            ['D', 'inhale']
        ],
        label='PERSPIRE',
        widget=widgets.RadioSelect,
    )
    lang12 = models.StringField(
        choices=[
            ['A', 'power'],
            ['B', 'produce'],
            ['C', 'spin'],
            ['D', 'burn']
        ],
        label='GENERATE',
        widget=widgets.RadioSelect,
    )
    lang13 = models.StringField(
        choices=[
            ['A', 'aggressively'],
            ['B', 'slowly'],
            ['C', 'cooperatively'],
            ['D', 'strikingly']
        ],
        label='HARMONIOUSLY',
        widget=widgets.RadioSelect,
    )
    lang14 = models.StringField(
        choices=[
            ['A', 'admit'],
            ['B', 'suppose'],
            ['C', 'commit'],
            ['D', 'fail']
        ],
        label='CONFESS',
        widget=widgets.RadioSelect,
    )
    lang15 = models.StringField(
        choices=[
            ['A', 'predator'],
            ['B', 'valley'],
            ['C', 'equator'],
            ['D', 'peak']
        ],
        label='APEX',
        widget=widgets.RadioSelect,
    )
    lang16 = models.StringField(
        choices=[
            ['A', 'complicated'],
            ['B', 'captivated'],
            ['C', 'surrounded'],
            ['D', 'abusive']
        ],
        label='HOOKED',
        widget=widgets.RadioSelect,
    )
    lang17 = models.StringField(
        choices=[
            ['A', 'carlessness'],
            ['B', 'cleverness'],
            ['C', 'daring'],
            ['D', 'haplessness']
        ],
        label='SLOPPINESS',
        widget=widgets.RadioSelect,
    )
    lang18 = models.StringField(
        choices=[
            ['A', 'demonstrably'],
            ['B', 'powerfully'],
            ['C', 'indignantly'],
            ['D', 'unemotionally']
        ],
        label='STOICALLY',
        widget=widgets.RadioSelect,
    )
    lang19 = models.StringField(
        choices=[
            ['A', 'scurry'],
            ['B', 'prowl'],
            ['C', 'activate'],
            ['D', 'hassle']
        ],
        label='SCUTTLE',
        widget=widgets.RadioSelect,
    )


    # Part b
    lang20 = models.StringField(
        choices=[
            ['A', 'removed'],
            ['B', 'distinctive'],
            ['C', 'dismissive'],
            ['D', 'fraudulent']
        ],
        label='Local officials produced _________ reports by inflating the ' \
            'figures so that fisheries appeared more productive.',
        widget=widgets.RadioSelect,
    )
    lang21 = models.StringField(
        choices=[
            ['A', 'proposed]'],
            ['B', 'dismissed'],
            ['C', 'upheld'],
            ['D', 'criticized']
        ],
        label='In a victory for police and law enforcement the Supreme Court ' \
         '_________ a lower court\'s ruling, which allowed the officers to take ' \
        'DNA samples from arrested suspects.',
        widget=widgets.RadioSelect,
    )
    lang22 = models.StringField(
        choices=[
            ['A', 'notorious'],
            ['B', 'copious'],
            ['C', 'comprehensive'],
            ['D', 'prolific']
        ],
        label='Wolfgang Amadeus Mozart published over 600 pieces of music, ' \
             'making him one of the most _________ composers of the Classical era',
        widget=widgets.RadioSelect,
    )
    lang23 = models.StringField(
        choices=[
            ['A', 'peculiar'],
            ['B', 'sensational'],
            ['C', 'wasteful'],
            ['D', 'practical']
        ],
        label='Dean loved his old car, but to admit that it was too small to be, ' \
             'a _________ family vehicle.',
        widget=widgets.RadioSelect,
    )
    lang24 = models.StringField(
        choices=[
            ['A', 'playful'],
            ['B', 'bickering'],
            ['C', 'diligent'],
            ['D', 'bellicose']
        ],
        label='Karen is often described by her coworkers as a  _________ worker ' \
            'who pays careful attention to every detail.',
        widget=widgets.RadioSelect,
    )
    lang25 = models.StringField(
        choices=[
            ['A', 'incautious'],
            ['B', 'overwrought'],
            ['C', 'underfunded'],
            ['D', 'exhaustive']
        ],
        label='Determined to find the exact cause of the accident, forensic ' \
            'engineers conducted a _________ investigation of the wreckage. ',
        widget=widgets.RadioSelect,
    )
    lang26 = models.StringField(
        choices=[
            ['A', 'prefer'],
            ['B', 'atempt'],
            ['C', 'cease'],
            ['D', 'tend']
        ],
        label='Processed foods _________ to contain more artificial ' \
            'perservatives than alternatives, so some dietitians recommend' \
                'avoiding them.',
        widget=widgets.RadioSelect,
    )
    lang27 = models.StringField(
        choices=[
            ['A', 'negotiations'],
            ['B', 'divisions'],
            ['C', 'deficits'],
            ['D', 'increases']
        ],
        label='After projecting steep budget _________, the company was forced ' \
            ' to close under performing stores in an effort to reduce spending ' \
            'and avoid losses.',
        widget=widgets.RadioSelect,
    )
    lang28 = models.StringField(
        choices=[
            ['A', 'dialogue'],
            ['B', 'category'],
            ['C', 'primer'],
            ['D', 'incident']
        ],
        label='A vehicle owner\'s manual can be a useful _________ on maintenance ' \
            ' and simple fixes, but won\'t teach you khow to make major repairs.',
        widget=widgets.RadioSelect,
    )
    lang29 = models.StringField(
        choices=[
            ['A', 'popular'],
            ['B', 'understanding'],
            ['C', 'confrontational'],
            ['D', 'discerning']
        ],
        label='Viewers were unsurprised when the notoriously _________ host ' \
            'began to attack his guest\' political views.',
        widget=widgets.RadioSelect,
    )
    lang30 = models.StringField(
        choices=[
            ['A', 'prudent'],
            ['B', 'frugal'],
            ['C', 'curmudgeonly'],
            ['D', 'extravagant']
        ],
        label='The Student Activities Board considered taking a senior trip to '\
            'France, but determined that it was too_________ rfor their limited ' \
            'budget',
        widget=widgets.RadioSelect,
    )



# PAGES
class PartA(Page):
    form_model = 'player'
    form_fields = ['lang1', 'lang2', 'lang3', 'lang4', 'lang5', 'lang6', 'lang7',
                    'lang8', 'lang9', 'lang10', 'lang11', 'lang12', 'lang13',
                    'lang14', 'lang15', 'lang16', 'lang17', 'lang18', 'lang19']


class PartB(Page):
    form_model = 'player'
    form_fields = ['lang20', 'lang21', 'lang22', 'lang23', 'lang24', 'lang25', 'lang26',
                    'lang27', 'lang28', 'lang29', 'lang30']


class Results(Page):
    pass


page_sequence = [PartA, PartB]
