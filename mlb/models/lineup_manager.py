from datetime import date, timedelta
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
		except Exception as e:
			print "WTF? - {}".format(str(e))

		if player_id not in self.processed_players:
			self.processed_players.append(player_id)

	def get_id_for_player_name(self, name):
		player_data = self.player_manager.players_collection.find_one({"name": name}, {"player_id": 1})

		if player_data is None or "player_id" not in player_data:
			return None
		else:
			return player_data["player_id"].replace(".", "_")

	def find_team_last_game(self, team):
		"""
		Determine the last date that the provided team played and return their starting lineup.
		:param team:    The team of interest
		:return:        A list of player ids representing the starting lineup of the last game they played.
		"""
		one_day = timedelta(days=1)
		today = date.today()
		curr_day = today

		found = False
		players_list = []
		while not found:
			curr_day = curr_day - one_day
			lineups = self.lineups_collection.find_one({"date": str(curr_day)})
			players = lineups["players"]

			for player in players:
				if "team" in players[player] and players[player]["team"] == team:
					found = True
					player_data = {
						MLBConstants.PLAYER_ID: player,
					    MLBConstants.POSITION: players[player][MLBConstants.POSITION]
					}
					players_list.append(player_data)

		return players_list

	def find_player_position_last_game(self, player_id):
		"""
		Return the position that the provided player started at in their last game.

		:param player_id:   The id of the player of interest.
		:return:            A string representing the player's position.
		"""
		one_day = timedelta(days=1)
		today = date.today()
		curr_day = today

		found = False
		while not found:
			curr_day = curr_day - one_day
			player_data = self.lineups_collection.find_one({"date": str(curr_day)})
			if player_id not in player_data["players"]:
				continue
			return player_data["players"][player_id][MLBConstants.POSITION]

		return None