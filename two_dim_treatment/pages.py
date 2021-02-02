from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class ContractDecision(Page):
	template_name ='two_dim_treatment/ContractDecision.html'
	form_model = 'player'
	form_fields = ['choice']

	def vars_for_template(self):
		i = self.player.subsession.round_number
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

	#timeout_seconds = 180

	#def before_next_page(player):
	#	i = player.subsession.round_number
		#player.wage1 = Constants.wages[i-1][0]



class ResultsWaitPage(WaitPage):
	pass
	#def after_all_players_arrive(group):
		#p = group.get_players()
		#p.get_wages()


class Results(Page):
	def is_displayed(self):
		return self.player.subsession.round_number == Constants.num_rounds




page_sequence = [ContractDecision, ResultsWaitPage, Results]
