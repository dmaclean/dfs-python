from pymongo import MongoClient
from mlb.constants.mlb_constants import MLBConstants

__author__ = 'dan'

class NameMappingManager:
	"""
	Manager for the name_mapping collection
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
		self.name_mapping_collection = self.db[MLBConstants.MONGO_MLB_NAME_MAPPING_COLLECTION]

		# self.player_manager = PlayerManager(testing=self.testing_mode)

		# self.processed_players = None

	def get_player_name(self, source, target, name):
		result = self.name_mapping_collection.find_one({ source: name }, { target: 1 })
		if result is not None:
			return result[target]

		return None
