

class PlayByPlayGame:
	GAME_DATE = "GAME_DATE"
	HOME = "HOME"
	AWAY = "AWAY"

	def __init__(self, _id=None, game_date=None, home=None, away=None, pbp_data=None):
		self._id = _id
		self.game_date = game_date
		self.home = home
		self.away = away
		self.pbp_data = pbp_data

	def to_json(self):
		"""
		Convert the PBP object to its JSON representation.  For PyMongo, the JSON rep will just
		be a dictionary.
		"""
		json_rep = {}
		for k in self.__dict__.keys():
			if self.__dict__[k] is not None:
				json_rep[k] = self.__dict__[k]