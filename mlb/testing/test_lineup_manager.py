import unittest
from datetime import date, timedelta
from mlb.constants.mlb_constants import MLBConstants
from mlb.models.lineup_manager import LineupManager
from mlb.models.player_manager import PlayerManager

__author__ = 'dan'


class TestLineupManager(unittest.TestCase):
	def setUp(self):
		self.lineup_manager = LineupManager(testing=True)
		self.player_manager = PlayerManager(testing=True)

	def tearDown(self):
		self.lineup_manager.lineups_collection.drop()
		self.player_manager.players_collection.drop()
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

		# Reset the processed map.
		self.lineup_manager.processed_players = None

		self.assertTrue(self.lineup_manager.is_processed("dmaclean"))

	def test_is_processed_false(self):
		self.assertFalse(self.lineup_manager.is_processed("dmaclean"))

	def test_add_player_to_lineup_none_yet(self):
		self.assertFalse(self.lineup_manager.is_processed("dmaclean"))

		self.lineup_manager.add_player_to_lineup("dmaclean", {})
		self.assertTrue(self.lineup_manager.is_processed("dmaclean"))

		self.lineup_manager.add_player_to_lineup("dmaclean2", {})
		self.assertTrue(self.lineup_manager.is_processed("dmaclean2"))

	def test_get_id_for_player_name(self):
		self.assertTrue(self.lineup_manager.get_id_for_player_name("Dan MacLean") is None)

		player_data = {
			"name": "Dan MacLean",
		    "player_id": "dmaclean"
		}
		self.player_manager.save(player_data)

		self.assertTrue(self.lineup_manager.get_id_for_player_name("Dan MacLean") == "dmaclean")

	def test_find_team_last_game(self):
		one_day = timedelta(days=1)
		today = date.today()
		yesterday = today - one_day
		two_days_ago = yesterday - one_day
		three_days_ago = two_days_ago - one_day

		yesterday_lineup = {
			"date": str(yesterday),
		    "players": {
			    "dmaclean": {
				    "team": "BOS",
			        "position": "P"
			    }
		    }
		}
		self.lineup_manager.lineups_collection.save(yesterday_lineup)

		two_days_ago_lineup = {
			"date": str(two_days_ago),
		    "players": {
			    "asmith": {
				    "team": "CLE",
			        "position": "2B"
			    }
		    }
		}
		self.lineup_manager.lineups_collection.save(two_days_ago_lineup)

		three_days_ago_lineup = {
			"date": str(three_days_ago),
		    "players": {
			    "bjohnson": {
				    "team": "CLE",
			        "position": "3B"
			    }
		    }
		}
		self.lineup_manager.lineups_collection.save(three_days_ago_lineup)

		players = self.lineup_manager.find_team_last_game("BOS")
		self.assertTrue(len(players) == 1)
		self.assertTrue(players[0][MLBConstants.PLAYER_ID] == "dmaclean")
		self.assertTrue(players[0][MLBConstants.POSITION] == "P")

		players = self.lineup_manager.find_team_last_game("CLE")
		self.assertTrue(len(players) == 1)
		self.assertTrue(players[0][MLBConstants.PLAYER_ID] == "asmith")
		self.assertTrue(players[0][MLBConstants.POSITION] == "2B")

	def test_find_player_position_last_game(self):
		one_day = timedelta(days=1)
		today = date.today()
		yesterday = today - one_day
		two_days_ago = yesterday - one_day
		three_days_ago = two_days_ago - one_day

		yesterday_lineup = {
			"date": str(yesterday),
		    "players": {
			    "dmaclean": {
				    "team": "BOS",
			        "position": "P"
			    }
		    }
		}
		self.lineup_manager.lineups_collection.save(yesterday_lineup)

		two_days_ago_lineup = {
			"date": str(two_days_ago),
		    "players": {
			    "asmith": {
				    "team": "CLE",
			        "position": "2B"
			    }
		    }
		}
		self.lineup_manager.lineups_collection.save(two_days_ago_lineup)

		three_days_ago_lineup = {
			"date": str(three_days_ago),
		    "players": {
			    "bjohnson": {
				    "team": "CLE",
			        "position": "3B"
			    }
		    }
		}
		self.lineup_manager.lineups_collection.save(three_days_ago_lineup)

		position = self.lineup_manager.find_player_position_last_game("asmith")
		self.assertTrue(position == "2B")

		position = self.lineup_manager.find_player_position_last_game("bjohnson")
		self.assertTrue(position == "3B")

if __name__ == '__main__':
	unittest.main()