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

#---------------------------------------------------
# CONSTANTS
#---------------------------------------------------
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
	wages[0] = [8.11, 11.66, 13.74, 15.77, 16.98, 17.92, 18.45, 18.75, 19.01, 19.23]
	wages[1] = [8.17, 9.99, 11.44, 12.59, 13.67, 14.30, 14.93, 15.35, 15.58, 15.79]
	wages[2] = [5.45, 7.60, 9.39, 10.38, 10.90, 11.18, 11.43, 11.64, 11.84, 12.03]
	wages[3] = [5.20, 9.40, 12.20, 13.64, 14.67, 15.53, 15.97, 16.30, 16.47, 16.64]
	wages[4] = [5.39, 9.81, 13.51, 15.95, 17.67, 19.04, 20.24, 21.22, 21.83, 22.42]
	wages[5] = [5.81, 9.06, 11.42, 13.26, 14.66, 15.97, 17.12, 17.74, 18.30, 18.78]
	wages[6] = [3.65, 5.75, 6.83, 7.86, 8.58, 8.97, 9.31, 9.62, 9.81, 9.92]
	wages[7] = [4.36, 6.12, 7.75, 9.28, 10.40, 11.32, 11.90, 12.23, 12.43, 12.62]
	wages[8] = [4.29, 8.92, 11.30, 13.35, 14.55, 15.71, 16.31, 16.61, 16.77, 16.88]
	wages[9] = [6.64, 9.51, 11.77, 12.95, 14.01, 14.61, 14.95, 15.12, 15.28, 15.39]
	wages[10] = [4.37, 5.08, 5.51, 5.80, 6.00, 6.20, 6.38, 6.38, 6.55, 6.60]
	wages[11] = [7.47, 10.39, 12.26, 13.21, 14.04, 14.75, 15.24, 15.56, 15.84, 15.99]
	wages[12] = [7.81, 9.85, 11.56, 13.04, 14.26, 15.30, 15.95, 16.34, 16.54, 16.73]
	wages[13] = [8.50, 11.02, 13.07, 14.92, 16.76, 18.48, 19.43, 20.29, 21.01, 21.51]
	wages[14] = [5.74, 7.44, 8.49, 9.11, 9.52, 9.73, 9.91, 10.01, 10.09, 10.13]
	wages[15] = [6.47, 10.79, 14.53, 17.65, 20.37, 22.17, 23.53, 24.88, 25.78, 26.63]
	wages[16] = [3.26, 7.05, 9.52, 11.77, 13.18, 14.49, 15.67, 16.61, 17.44, 18.09]
	wages[17] = [4.77, 8.90, 11.62, 13.79, 15.87, 17.86, 19.15, 19.87, 20.41, 20.75]
	wages[18] = [7.27, 7.70, 8.11, 8.42, 8.72, 8.92, 9.03, 9.11, 9.18, 9.22]
	wages[19] = [3.88, 6.33, 8.75, 11.13, 12.84, 14.25, 15.57, 16.85, 17.84, 18.36]

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


#---------------------------------------------------
# MODELS:
#---------------------------------------------------
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






#---------------------------------------------------
# METHODS:
#---------------------------------------------------

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
		p.paying_round = player.paying_round

	# making sure payoff variable is defined correctly:
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
                if temp.value == 0:
                    errors[0]=False
                    errors[i]=True

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
class TaskGenerator(Page):
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
	def before_next_page(player: Player, timeout_happened):
		set_task(player)


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


class ContractInstructions(Page):
	def is_displayed(player):
		if (player.round_number==Constants.num_training_rounds):
			return True
		else:
			return False

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


page_sequence = [
				WelcomePage,
				TaskGenerator,
				PracticeTask,
				ContractInstructions,
				ContractDecision,
				PreResults,
				Results,
				FinalResults
				]









