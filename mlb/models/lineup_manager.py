from datetime import date
from pymongo import MongoClient
from mlb.constants.mlb_constants import MLBConstants
from mlb.models.player_manager import PlayerManager

__author__ = 'dan'


class LineupManager:
	"""
	Manager class for lineups.
	"""
	def __init__(self, testing=False):
		self.testing_mode = testing

		"""
		Initialization for the LineupManager.  Here we make a connection to MongoDB, grab a database handle,
		and also a handle on the lineups collection.
		"""
		self.client = MongoClient('localhost', 27017)

		# Get a database handle.  It'll either be live data or the testing database
		# depending on the "testing" flag that gets passed in.
		if testing:
			self.db = self.client[MLBConstants.MONGO_MLB_TEST_DB_NAME]
		else:
			self.db = self.client[MLBConstants.MONGO_MLB_DB_NAME]

		# Get a handle on the players collection.
		self.lineups_collection = self.db[MLBConstants.MONGO_MLB_LINEUPS_COLLECTION]

		self.player_manager = PlayerManager(testing=self.testing_mode)

		self.processed_players = None

	def is_processed(self, player_id, d=str(date.today())):
		if self.processed_players is None:
			self.processed_players = []
			lineups = self.lineups_collection.find_one({'date': d})

			if lineups is not None:
				for player in lineups["players"]:
					self.processed_players.append(player)

		#if lineups is None or player_id not in lineups["players"]:
		return player_id in self.processed_players

	def add_player_to_lineup(self, player_id, player_lineup_data, d=str(date.today())):
		lineups = self.lineups_collection.find_one({'date': d})
		if lineups is None:
			lineups = {
				"date": d,
			    "players": {}
			}

		lineups["players"][player_id] = player_lineup_data

		try:
			self.lineups_collection.save(lineups)
		except:
			print "WTF?"

		if player_id not in self.processed_players:
			self.processed_players.append(player_id)

	def get_id_for_player_name(self, name):
		player_data = self.player_manager.players_collection.find_one({"name": name}, {"player_id": 1})

		if player_data is None or "player_id" not in player_data:
			return None
		else:
			return player_data["player_id"].replace(".", "_")