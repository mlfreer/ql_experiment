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
	num_rounds = 35

	# maximum number of tasks:
	num_tasks = 10

	# number of the decision making problems
	num_decision_rounds = 20
	# number of budgets
	number_of_budgets= 20
	# number of training periods
	num_training_rounds = 1
	

	# number of budgets:
	num_budgets = 20

	# defining the budgets:
	# use exact number of num_tasks
	wages = [[0 for x in range(0, 10)]  for x in range(0, number_of_budgets)]
	wages[0] = [4.02, 6.51, 8.09, 9.35, 10.34, 11.00, 8.09, 9.35, 10.34, 11.00]
	wages[1] = [5.51, 7.26, 8.56, 9.39, 9.94, 10.33, 8.09, 9.35, 10.34, 11.00]
	wages[2] = [5.76, 7.38, 8.37, 9.15, 9.71, 10.13, 8.09, 9.35, 10.34, 11.00]
	wages[3] = [4.01, 6.51, 8.15, 9.37, 10.26, 10.93, 8.09, 9.35, 10.34, 11.00]
	wages[4] = [5.02, 7.01, 8.40, 9.40, 10.18, 10.78, 8.09, 9.35, 10.34, 11.00]
	wages[5] = [5.19, 7.10, 8.35, 9.25, 9.96, 10.41, 8.09, 9.35, 10.34, 11.00]
	wages[6] = [4.30, 6.65, 8.28, 9.28, 9.91, 10.39, 8.09, 9.35, 10.34, 11.00]
	wages[7] = [4.56, 6.78, 8.47, 9.57, 10.29, 10.75, 8.09, 9.35, 10.34, 11.00]
	wages[8] = [5.61, 7.30, 8.42, 9.20, 9.72, 10.06, 8.09, 9.35, 10.34, 11.00]
	wages[9] = [4.39, 6.70, 8.09, 9.13, 9.90, 10.47, 8.09, 9.35, 10.34, 11.00]
	wages[10] = [4.88, 6.94, 8.38, 9.30, 9.88, 10.24, 8.09, 9.35, 10.34, 11.00]
	wages[11] = [4.28, 6.64, 8.29, 9.48, 10.32, 10.92, 8.09, 9.35, 10.34, 11.00]
	wages[12] = [4.24, 6.62, 8.23, 9.46, 10.39, 10.95, 8.09, 9.35, 10.34, 11.00]
	wages[13] = [5.49, 7.24, 8.35, 9.08, 9.52, 9.81, 8.09, 9.35, 10.34, 11.00]
	wages[14] = [4.11, 6.56, 8.05, 9.24, 10.05, 10.62, 8.09, 9.35, 10.34, 11.00]
	wages[15] = [4.11, 6.56, 8.05, 9.24, 10.05, 10.62, 8.09, 9.35, 10.34, 11.00]
	wages[16] = [4.11, 6.56, 8.05, 9.24, 10.05, 10.62, 8.09, 9.35, 10.34, 11.00]
	wages[17] = [4.11, 6.56, 8.05, 9.24, 10.05, 10.62, 8.09, 9.35, 10.34, 11.00]
	wages[18] = [4.11, 6.56, 8.05, 9.24, 10.05, 10.62, 8.09, 9.35, 10.34, 11.00]
	wages[19] = [4.11, 6.56, 8.05, 9.24, 10.05, 10.62, 8.09, 9.35, 10.34, 11.00]

	# pages:
	number_of_pages = 35

	row_numbers = [i for i in range(1,number_of_pages+1)]
	row_numbers[0] = 8
	row_numbers[1] = 8
	row_numbers[2] = 13
	row_numbers[3] = 7
	row_numbers[4] = 8
	row_numbers[5] = 5
	row_numbers[6] = 8
	row_numbers[7] = 6
	row_numbers[8] = 7
	row_numbers[9] = 6
	row_numbers[10] = 6
	row_numbers[11] = 5
	row_numbers[12] = 3
	row_numbers[13] = 4
	row_numbers[14] = 5
	row_numbers[15] = 3
	row_numbers[16] = 9
	row_numbers[17] = 4
	row_numbers[18] = 4
	row_numbers[19] = 4
	row_numbers[20] = 9

	column_numbers = 12



# MODELS:
class Subsession(BaseSubsession):
	pass


class Group(BaseGroup):
	pass


class Player(BasePlayer):
	choice = models.IntegerField()

	# variables determining the final contract:
	paying_round = models.IntegerField(min=1,default=1)
	final_wage = models.FloatField(max_digits=5, decimal_places=2, default=0)
	final_task = models.IntegerField(min=1, max=Constants.num_tasks,default=1)
	
	# parameters for the input task:
	page_number = models.IntegerField(min=1,max=Constants.number_of_pages,default=1)
	num_of_rows = models.IntegerField(min=1,default=1)
	num_of_columns = models.IntegerField(default=Constants.column_numbers)


class DataItem(ExtraModel):
	player = models.Link(Player)
	row = models.IntegerField(min=1,max=10,default=1)
	column = models.IntegerField(min=1,max=10,default=1)
	budget_number = models.IntegerField(min=1,max=Constants.number_of_budgets)
	value = models.IntegerField(min=0,default=0)




#-----------------------------------
# Methods:
#-----------------------------------

# Methods for players
def set_task(player: Player):
	import random
	i=random.randint(1,21)
#        flag=True
#        while flag:
#            flag=False
#            for j in Constants.prohibited_numbers:
#                if i==j:
#                    flag=True
#            if flag:
#                i=random.randint(3,Constants.number_of_pages)
	player.page_number = i
	player.num_of_rows = Constants.row_numbers[i-1]
	player.num_of_columns = Constants.column_numbers
	create_data_inputs(player, player.num_of_rows, player.num_of_columns, i)


def set_final_contract(player: Player):
	player.paying_round = random.randint(Constants.num_training_rounds,Constants.num_training_rounds+Constants.number_of_budgets-1)
	p = player.in_round(player.paying_round)
	player.final_task = p.choice
	player.final_wage = Constants.wages[player.paying_round-2+Constants.num_training_rounds][p.choice-1]
	# making sure data is transferred along all periods:
	for p in player.in_rounds(1,Constants.num_rounds):
		p.final_task = player.final_task
		p.final_wage = player.final_wage
		#p.payoff = player.final_wage
		p.paying_round = player.paying_round

	p = player.in_round(Constants.num_rounds)
	p.payoff = player.final_wage


# methods for data input class
def create_data_inputs(player: Player, n,m, page_num):
	for i in range(1,n+1):
		for j in range(1,m+1):
			DataItem.create(player = player, row = i, column = j, budget_number = page_num, value = i+j)

def get_data_input(player: Player, i, j):
	return DataItem.filter(player = player, row = i, column = j)[0]


def custom_export(players):
	yield ['value', 'row', 'column', 'page_number']
	for p in players:
		#pp = p.participant
		for i in range(1,9):
			for j in range (1,13):
				temp = DataItem.filter(player=p, row = i, column = j)
				for t in temp:
					yield [t.value, t.row, t.column, t.budget_number]

def error_message(player: Player, value):
	if value == True:
		return 'Please check line'+str(value)


def live_method(player: Player, data):
	#print(data)
	errors = [False for i in range(0,player.num_of_rows+2)]
	if data['submitted']==0:
		errors[0]=False
		print('no data submitted')
	else:
		print('data_submitted')
		errors[0]=True
		for i in range(1,player.num_of_rows+1):
			key1 = "a_"+str(i)
			for j in range(1,player.num_of_columns+1):
				key = key1+"_"+str(j)
				temp = get_data_input(player, i, j)
				temp.value = data[key]
				#print(temp.value)

			temp_sum = 0
			for j in range(9,player.num_of_columns):
				temp = get_data_input(player, i, j)
				temp_sum = temp_sum + temp.value
#                if temp.value == 0:
#                    errors[0]=False
#                    errors[i]=True

			temp = get_data_input(player, i, player.num_of_columns)
			if temp_sum != temp.value:
				errors[0]=False
				errors[i]=True
				print('row sums dont match')
				print(temp_sum)
				print(temp.value)

		for i in range(1,player.num_of_columns+1):
			temp_sum = 0
			for j in range(1,player.num_of_rows):
				temp = get_data_input(player, j, i)
				temp_sum = temp_sum + temp.value
			temp = get_data_input(player, player.num_of_rows, i)
			if temp_sum != temp.value:
				errors[0]=False
				errors[player.num_of_rows+1]=True
				print('column sums dont match')

	error_message(player, errors[1])         
	print(errors)
	print('end of data')
	return {
		player.id_in_group: errors
		}




#--------------------------------
# PAGES:
#--------------------------------
class WelcomePage(Page):
	@staticmethod   
	def is_displayed(player: Player):
		return player.subsession.round_number == 1

#	@staticmethod
#	def before_next_page(player: Player,timeout_happened):


# waitpage to generate a task for the player:
class TaskGenerator(WaitPage):
	def after_all_players_arrive(group: Group):
		for p in group.get_players():
			set_task(p)
#	@staticmethod
#	def before_next_page(player: Player, timeout_happened):
#		set_task(player)


# Page responsible for the data input task
class PracticeTask(Page):
	import random
	live_method=live_method
	def is_displayed(player):
		# for the training rounds show the practice tasks
		if (player.round_number<=Constants.num_training_rounds):
			return True
		else:
			# once done with the practice, make sure there theresults are shown appropriately
			if player.round_number> Constants.num_training_rounds + Constants.number_of_budgets and player.round_number<= Constants.num_training_rounds + Constants.number_of_budgets + player.final_task:
				return True
			else:
			# otherwise do not show.
				return False


	@staticmethod
	def vars_for_template(player: Player): 
		return dict(
		image_path='ql_experiment/{}.jpg'.format(player.page_number),
		rows = range(1,player.num_of_rows+1),
		columns = range(1,player.num_of_columns+1)
	)


   
class ContractDecision(Page):
	form_model = 'player'
	form_fields = ['choice']
#   participant.input_task = [0 for i in range(9)]
	
	def is_displayed(player):
		if (player.round_number>=Constants.num_training_rounds) and (player.round_number<=Constants.num_training_rounds + Constants.number_of_budgets-1):
			return True
		else:
			return False
	
	@staticmethod
	def vars_for_template(player: Player):
		i = player.subsession.round_number-Constants.num_training_rounds+1
		w1 = Constants.wages[i-1][0]
		w2 = Constants.wages[i-1][1]
		w3 = Constants.wages[i-1][2]
		w4 = Constants.wages[i-1][3]
		w5 = Constants.wages[i-1][4]
		w6 = Constants.wages[i-1][5]
		w7 = Constants.wages[i-1][6]
		w8 = Constants.wages[i-1][7]
		w9 = Constants.wages[i-1][8]
		w10 = Constants.wages[i-1][9]
		return {
				'budget_number': i,
				'w1': w1,
				'w2': w2,
				'w3': w3,
				'w4': w4,
				'w5': w5,
				'w6': w6,
				'w7': w7,
				'w8': w8,
				'w9': w9,
				'w10': w10
			}


class PreResults(Page):
	@staticmethod
	def is_displayed(player: Player):
		return player.subsession.round_number == (Constants.number_of_budgets+Constants.num_training_rounds)
	@staticmethod
	def before_next_page(player: Player, timeout_happened):
		if player.subsession.round_number == (Constants.number_of_budgets+Constants.num_training_rounds):
			set_final_contract(player)

class Results(Page):
	@staticmethod
	def is_displayed(player: Player):
		return player.subsession.round_number == (Constants.number_of_budgets+Constants.num_training_rounds)
	@staticmethod
	def vars_for_template(player: Player):
		return {
				'period': player.paying_round,
				'wage': player.final_wage,
				'tasks': player.final_task
			}

class FinalResults(Page):
	@staticmethod
	def is_displayed(player: Player):
		return player.subsession.round_number == Constants.num_rounds


page_sequence = [WelcomePage, TaskGenerator, PracticeTask, ContractDecision, PreResults, Results, FinalResults]
