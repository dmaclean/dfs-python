__author__ = 'ap'

class Injury():

	def __init__(self, id=None, player_id=None, injury_date=None, return_date=None, details=None):
		self.id = id
		self.player_id = player_id
		self.injury_date = injury_date
		self.return_date = return_date
		self.details = details