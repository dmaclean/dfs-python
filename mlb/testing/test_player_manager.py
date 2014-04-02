import unittest
from mlb.constants.mlb_constants import MLBConstants
from mlb.models.player_manager import PlayerManager

__author__ = 'dan'


class TestPlayerManager(unittest.TestCase):
	def setUp(self):
		self.player_manager = PlayerManager(testing=True)

	def tearDown(self):
		self.player_manager.drop_collection()
		self.player_manager = None

	def test_db_operations(self):
		self.assertTrue(self.player_manager.players_collection.count() == 0)

		player = self.player_manager.read("dmaclean")
		self.assertTrue(player is None)

		new_player = {
			MLBConstants.PLAYER_ID: "dmaclean",
			MLBConstants.NAME: "Dan MacLean",
			MLBConstants.POSITION: "Pitcher"
		}
		self.player_manager.save(new_player)

		player = self.player_manager.read({MLBConstants.PLAYER_ID: "dmaclean"})
		self.assertTrue(player[MLBConstants.PLAYER_ID] == "dmaclean")
		self.assertTrue(player[MLBConstants.NAME] == "Dan MacLean")
		self.assertTrue(player[MLBConstants.POSITION] == "Pitcher")

		self.assertTrue(self.player_manager.players_collection.count() == 1)

		player[MLBConstants.NAME] = "Steph MacLean"
		self.player_manager.save(player)

		player = self.player_manager.read({MLBConstants.PLAYER_ID: "dmaclean"})
		self.assertTrue(player[MLBConstants.PLAYER_ID] == "dmaclean")
		self.assertTrue(player[MLBConstants.NAME] == "Steph MacLean")
		self.assertTrue(player[MLBConstants.POSITION] == "Pitcher")

		self.assertTrue(self.player_manager.players_collection.count() == 1)

if __name__ == '__main__':
	unittest.main()