import unittest
from datetime import date
from mlb.models.lineup_manager import LineupManager
from mlb.models.player_manager import PlayerManager

__author__ = 'dan'


class TestLineupManager(unittest.TestCase):
	def setUp(self):
		self.lineup_manager = LineupManager(testing=True)
		self.player_manager = PlayerManager(testing=True)

	def tearDown(self):
		self.lineup_manager.lineups_collection.drop()
		self.lineup_manager = None
		self.player_manager = None

	def test_is_processed_true(self):
		self.assertFalse(self.lineup_manager.is_processed("dmaclean"))

		d = str(date.today())
		lineup = {
			"date": d,
		    "players": {
			    "dmaclean": True
		    }
		}
		self.lineup_manager.lineups_collection.save(lineup)

		self.assertTrue(self.lineup_manager.is_processed("dmaclean"))

	def test_is_processed_false(self):
		self.assertFalse(self.lineup_manager.is_processed("dmaclean"))

	def test_add_player_to_lineup_none_yet(self):
		self.assertFalse(self.lineup_manager.is_processed("dmaclean"))

		self.lineup_manager.add_player_to_lineup("dmaclean")
		self.assertTrue(self.lineup_manager.is_processed("dmaclean"))

		self.lineup_manager.add_player_to_lineup("dmaclean2")
		self.assertTrue(self.lineup_manager.is_processed("dmaclean2"))

	def test_get_id_for_player_name(self):
		self.assertTrue(self.lineup_manager.get_id_for_player_name("Dan MacLean") is None)

		player_data = {
			"name": "Dan MacLean",
		    "player_id": "dmaclean"
		}
		self.player_manager.save(player_data)

		self.assertTrue(self.lineup_manager.get_id_for_player_name("Dan MacLean") == "dmaclean")

if __name__ == '__main__':
	unittest.main()