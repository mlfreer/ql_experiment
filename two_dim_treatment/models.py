from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency as c,
    currency_range,
)
from array import *

import decimal
import random

author = 'Mikhail Freer'

doc = """
This is the treatment for two dimensional treatment of the qlt experiment, where subjects make decisions on the non-linear contracts.
"""


class Constants(BaseConstants):
    name_in_url = 'two_dim_treatment'
    players_per_group = None
    num_rounds = 6

    # maximum number of tasks:
    num_tasks = 6

    # number of budgets:
    num_budgets = 15

    # defining the budgets:
    #wages = {}
    #wages[1,1] = 4.02
    #wages[1,2] = 6.51
    #wages[1,3] = 8.09

    wages = [[0 for x in range(0,6)]  for x in range(0,15)]
    wages[0] = [4.02, 6.51, 8.09, 9.35, 10.34, 11.00]
    wages[1] = [5.51, 7.26, 8.56, 9.39, 9.94, 10.33]
    wages[2] = [5.76, 7.38, 8.37, 9.15, 9.71, 10.13]
    wages[3] = [4.01, 6.51, 8.15, 9.37, 10.26, 10.93]
    wages[4] = [5.02, 7.01, 8.40, 9.40, 10.18, 10.78]
    wages[5] = [5.19, 7.10, 8.35, 9.25, 9.96, 10.41]

    temp_wage = wages[1][2]


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    choice = models.IntegerField(min=1,max=Constants.num_tasks)




