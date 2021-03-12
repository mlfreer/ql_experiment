#from django.contrib.postgres.fields import ArrayField
from otree.api import *
import json

from array import *

import decimal
import random

#from django.db import models

author = 'Mikhail Freer'

doc = """
This is the code for two dimensional treatment of the qlt experiment, where subjects make decisions on the non-linear contracts.
"""


class Constants(BaseConstants):
    name_in_url = 'two_dim_treatment'
    players_per_group = None
    num_rounds = 2

    # number of the decision making problems
    num_decision_rounds = 2
    # number of training periods
    num_training_rounds = 1
    # max number of the working rounds
    num_working_hours = 0
    # number of budgets
    number_of_budgets=3


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
    def set_payoffs(group):
        for p in group.get_players():
            p.set_final_contract()


class Player(BasePlayer):
    choice = models.IntegerField()

    # variables determining the final contract
    paying_round = models.IntegerField(min=1,default=1)
    final_wage = models.FloatField(max_digits=5, decimal_places=2, default=0)
    final_task = models.IntegerField(min=1, max=Constants.num_tasks,default=1)
    # defining the input task
    #input_task = ArrayField(ArrayField(models.IntegerField(),size=10),size=10)
    
    def set_final_contract(self):
        self.paying_round = random.randint(1,Constants.num_rounds)
        p = self.in_round(self.paying_round)
        self.final_task = p.choice
        self.final_wage = Constants.wages[self.paying_round-1][p.choice-1]

    def create_data_inputs(self):
        for i in range(1,10):
            for j in range(1,10):
                DataItem.create(player = self, row = i, column = j, budget_number = 1, value = i+j)

def custom_export(players):
    yield ['value', 'row','column', 'page_number']
    for p in players:
        #pp = p.participant
        for i in range(1,10):
            for j in range (1,10):
                temp = DataItem.filter(player=p, row = i, column = j)
                for t in temp:
                    yield [t.value, t.row, t.column, t.budget_number]



class DataItem(ExtraModel):
    player = models.Link(Player)
    row = models.IntegerField(min=1,max=10,default=1)
    column = models.IntegerField(min=1,max=10,default=1)
    budget_number = models.IntegerField(min=1,max=Constants.number_of_budgets)
    value = models.IntegerField(min=0,default=0)




#--------------------------
# starting the pages part:
#--------------------------
class WelcomePage(Page):
    import random
    #@staticmethod
    #template_name ='two_dim_treatment/WelcomePage.html'
    #form_model='dataItem'
    #form_fields = ['value']
    def vars_for_template(player: Player):
        i=random.randint(3,12)
        return dict(
        image_path='ql_experiment/{}.png'.format(i)
    )
    #    player.create_data_inputs()
    #    temp = {}
    #    for r in range(1,10):
    #        key1 = "a"+str(r)
    #        for j in range (1,10):
    #            key = key1+str(j)
    #            print(key)
    #            for t in DataItem.filter(player=player,row=r,column=j):
    #                temp[key] = t.value
    #                
    #    return temp

    def is_displayed(player: Player):
        return player.subsession.round_number == 1
    #def before_next_page(self):
    #   self.player.create_data_inputs()

class ContractDecision(Page):
    template_name ='two_dim_treatment/ContractDecision.html'
    form_model = 'player'
    form_fields = ['choice']
#   participant.input_task = [0 for i in range(9)]


    def vars_for_template(player: Player):
        i = player.subsession.round_number
        w1 = Constants.wages[i-1][0]
        w2 = Constants.wages[i-1][1]
        w3 = Constants.wages[i-1][2]
        w4 = Constants.wages[i-1][3]
        w5 = Constants.wages[i-1][4]
        w6 = Constants.wages[i-1][5]
        return {
                'w1': w1,
                'w2': w2,
                'w3': w3,
                'w4': w4,
                'w5': w5,
                'w6': w6
            }

class PreResults(Page):
    template_name ='two_dim_treatment/PreResults.html'  

    def is_displayed(player: Player):
        return player.subsession.round_number == (Constants.num_decision_rounds+Constants.num_training_rounds)

    def before_next_page(player: Player):
        if player.subsession.round_number == (Constants.num_decision_rounds+Constants.num_training_rounds):
            player.set_final_contract()

class Results(Page):
    template_name ='two_dim_treatment/Results.html' 
    
    def is_displayed(player: Player):
        return player.subsession.round_number == (Constants.num_decision_rounds+Constants.num_training_rounds)

    def vars_for_template(self):
        return {
                'period': self.player.paying_round,
                'wage': self.player.final_wage,
                'tasks': self.player.final_task
            }




page_sequence = [WelcomePage, ContractDecision, PreResults, Results]
