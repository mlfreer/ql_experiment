from os import environ

SESSION_CONFIGS = [
    # dict(
    #    name='public_goods',
    #    display_name="Public Goods",
    #    num_demo_participants=3,
    #    app_sequence=['public_goods', 'payment_info']
    # ),
    {
         'name': 'two_dim_treatment',
         'display_name': 'Nonlinear wage experiment',
         'num_demo_participants': 1,
         'app_sequence': ['no_self'],
     },
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=0.00, doc=""
)

ROOMS = [
    dict(
        name='TAMULAB',
        display_name='TAMU ECON LAB',
        participant_label_file='_rooms/TAMULAB.txt',
        use_secure_urls=False
    ),
]

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = ''
USE_POINTS = False

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

OTREE_PRODUCTION = True
DEBUG = False

SECRET_KEY = '4399864929687'

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = ['otree']
