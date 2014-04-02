from mlb.constants.mlb_constants import MLBConstants

__author__ = 'dan'

from pymongo import MongoClient


class PlayerManager:
	"""
	Manager class for players.
	"""

	def __init__(self, testing=False):
		self.testing_mode = testing

		"""
		Initialization for the PlayerManager.  Here we make a connection to MongoDB, grab a database handle,
		and also a handle on the players collection.
		"""
		self.client = MongoClient('localhost', 27017)

		# Get a database handle.  It'll either be live data or the testing database
		# depending on the "testing" flag that gets passed in.
		if testing:
			self.db = self.client[MLBConstants.MONGO_MLB_TEST_DB_NAME]
		else:
			self.db = self.client[MLBConstants.MONGO_MLB_DB_NAME]

		# Get a handle on the players collection.
		self.players_collection = self.db[MLBConstants.MONGO_MLB_PLAYERS_COLLECTION]

	def read(self, query):
		"""
		Reads a document from the players collection based on player_id.
		"""
		return self.players_collection.find_one(query)

	def save(self, doc):
		"""
		Inserts a document into the players collection.
		"""
		self.players_collection.save(doc)

	def drop_collection(self):
		"""
		Convenience method for dropping the players collection when we're testing.
		"""
		if self.testing_mode:
			self.players_collection.drop()