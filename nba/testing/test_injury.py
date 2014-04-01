from datetime import date, timedelta
from unittest import TestCase
import unittest
from BBRTestUtility import BBRTestUtility
from models.injury import Injury
from models.injury_manager import InjuryManager


class TestInjury(TestCase):
	def setUp(self):
		self.test_util = BBRTestUtility()
		self.injury_manager = InjuryManager(cnx=self.test_util.conn)
		self.test_util.runSQL()

		self.player_info = self.test_util.generate_default_player_info()

		self.injury_info = self.test_util.generate_default_injury_info()

		# Initialize the player game totals map.
		self.game_totals_basic_info = self.test_util.generate_default_game_totals_basic_info()

		# Initialize the team game totals map.
		self.team_game_totals_info = self.test_util.generate_default_team_game_totals_info()

		self.one_day = timedelta(days=1)
		self.today = date.today()
		self.tomorrow = self.today + self.one_day

	def test_db_operations(self):
		injury = Injury(player_id="dan", injury_date=date(2014,1,1), return_date=date(2014,1,10), details="broken leg")

		self.assertTrue(not self.injury_manager.exists(injury))

		self.injury_manager.insert(injury)

		self.assertTrue(self.injury_manager.exists(injury) and injury.id == 1)

		injuries = self.injury_manager.get(injury)
		self.assertTrue(len(injuries) == 1)
		self.assertTrue(injuries[0].player_id == "dan" and injuries[0].injury_date == "2014-01-01" and
						injuries[0].return_date == "2014-01-10" and injuries[0].details == "broken leg")

		injury2 = injuries[0]
		injury2.return_date = date(2014,1,2)

		self.injury_manager.update(injury2)
		injuries = self.injury_manager.get(injury2)

		self.assertTrue(len(injuries) == 1 and injuries[0].return_date == "2014-01-02")

		# Test get with no id
		injury_no_id = Injury(player_id="dan", injury_date=date(2014,1,1), return_date=date(2014,1,2), details="broken leg")
		injuries = self.injury_manager.get(injury_no_id)

		self.assertTrue(len(injuries) == 1 and injuries[0].return_date == "2014-01-02")

		# Test for currently-injured
		new_injury = Injury(player_id="later injury", injury_date=date(2014,1,10), return_date=date(2014,1,14), details="sick")
		self.injury_manager.insert(new_injury)
		injuries = self.injury_manager.get_currently_injured_players(date=date(2014,1,12))

		self.assertTrue(len(injuries) == 1)
		self.assertTrue(injuries[new_injury.player_id].player_id == "later injury" and
						injuries[new_injury.player_id].injury_date == "2014-01-10" and
						injuries[new_injury.player_id].return_date == "2014-01-14" and
						injuries[new_injury.player_id].details == "sick")

	def test_exists(self):
		injury = Injury(player_id="dan", injury_date=date(2014,1,1), return_date=date(2014,1,10), details="broken leg")
		self.injury_manager.insert(injury)

		# Dates within injury/return for first one
		injury2 = Injury(player_id="dan", injury_date=date(2014,1,2), return_date=date(2014,1,9), details="broken leg")
		self.assertTrue(self.injury_manager.exists(injury2))

		# Injury date before first one
		injury3 = Injury(player_id="dan", injury_date=date(2013,12,31), return_date=date(2014,1,9), details="broken leg")
		self.assertTrue(not self.injury_manager.exists(injury3))

		# Return date outside of first one
		injury4 = Injury(player_id="dan", injury_date=date(2014,1,2), return_date=date(2014,1,11), details="broken leg")
		self.assertTrue(not self.injury_manager.exists(injury4))

	def test_calculate_injuries_from_gamelogs_no_injuries(self):
		# self.assertTrue(False)

		# Set up three games
		self.team_game_totals_info["team"] = "BOS"
		self.team_game_totals_info["season"] = 2013
		self.team_game_totals_info["game"] = 1
		self.team_game_totals_info["date"] = date(2014,1,1)
		self.test_util.insert_into_team_game_totals(self.team_game_totals_info)

		self.team_game_totals_info["game"] = 2
		self.team_game_totals_info["date"] = date(2014,1,2)
		self.test_util.insert_into_team_game_totals(self.team_game_totals_info)

		self.team_game_totals_info["game"] = 3
		self.team_game_totals_info["date"] = date(2014,1,3)
		self.test_util.insert_into_team_game_totals(self.team_game_totals_info)

		# Set up a player who has played in two of the games above.
		self.player_info["id"] = "1"
		self.player_info["name"] = "1"
		self.player_info["position"] = "PG"
		self.player_info["rg_position"] = "PG"
		self.test_util.insert_into_players(self.player_info)

		self.game_totals_basic_info["player_id"] = self.player_info["id"]
		self.game_totals_basic_info["season"] = 2013
		self.game_totals_basic_info["game_number"] = 1
		self.game_totals_basic_info["team"] = "BOS"
		self.game_totals_basic_info["opponent"] = "PHI"
		self.game_totals_basic_info["date"] = date(2014,1,1)
		self.test_util.insert_into_game_totals_basic(self.game_totals_basic_info)

		self.game_totals_basic_info["player_id"] = self.player_info["id"]
		self.game_totals_basic_info["season"] = 2013
		self.game_totals_basic_info["game_number"] = 2
		self.game_totals_basic_info["team"] = "BOS"
		self.game_totals_basic_info["opponent"] = "PHI"
		self.game_totals_basic_info["date"] = date(2014,1,2)
		self.test_util.insert_into_game_totals_basic(self.game_totals_basic_info)

		self.game_totals_basic_info["player_id"] = self.player_info["id"]
		self.game_totals_basic_info["season"] = 2013
		self.game_totals_basic_info["game_number"] = 3
		self.game_totals_basic_info["team"] = "BOS"
		self.game_totals_basic_info["opponent"] = "PHI"
		self.game_totals_basic_info["date"] = date(2014,1,3)
		self.test_util.insert_into_game_totals_basic(self.game_totals_basic_info)

		self.injury_manager.calculate_injuries_from_gamelogs(2013)
		injuries = self.injury_manager.get(Injury(player_id="1"))
		self.assertTrue(len(injuries) == 0)

	def test_calculate_injuries_from_gamelogs_one_injury_last_game(self):
		# self.assertTrue(False)

		# Set up three games
		self.team_game_totals_info["team"] = "BOS"
		self.team_game_totals_info["season"] = 2013
		self.team_game_totals_info["game"] = 1
		self.team_game_totals_info["date"] = date(2014,1,1)
		self.test_util.insert_into_team_game_totals(self.team_game_totals_info)

		self.team_game_totals_info["game"] = 2
		self.team_game_totals_info["date"] = date(2014,1,2)
		self.test_util.insert_into_team_game_totals(self.team_game_totals_info)

		self.team_game_totals_info["game"] = 3
		self.team_game_totals_info["date"] = date(2014,1,3)
		self.test_util.insert_into_team_game_totals(self.team_game_totals_info)

		# Set up a player who has played in two of the games above.
		self.player_info["id"] = "1"
		self.player_info["name"] = "1"
		self.player_info["position"] = "PG"
		self.player_info["rg_position"] = "PG"
		self.test_util.insert_into_players(self.player_info)

		self.game_totals_basic_info["player_id"] = self.player_info["id"]
		self.game_totals_basic_info["season"] = 2013
		self.game_totals_basic_info["game_number"] = 1
		self.game_totals_basic_info["team"] = "BOS"
		self.game_totals_basic_info["opponent"] = "PHI"
		self.game_totals_basic_info["date"] = date(2014,1,1)
		self.test_util.insert_into_game_totals_basic(self.game_totals_basic_info)

		self.game_totals_basic_info["player_id"] = self.player_info["id"]
		self.game_totals_basic_info["season"] = 2013
		self.game_totals_basic_info["game_number"] = 2
		self.game_totals_basic_info["team"] = "BOS"
		self.game_totals_basic_info["opponent"] = "PHI"
		self.game_totals_basic_info["date"] = date(2014,1,2)
		self.test_util.insert_into_game_totals_basic(self.game_totals_basic_info)

		# self.game_totals_basic_info["player_id"] = self.player_info["id"]
		# self.game_totals_basic_info["season"] = 2013
		# self.game_totals_basic_info["game_number"] = 3
		# self.game_totals_basic_info["team"] = "BOS"
		# self.game_totals_basic_info["opponent"] = "PHI"
		# self.game_totals_basic_info["date"] = date(2014,1,3)
		# self.test_util.insert_into_game_totals_basic(self.game_totals_basic_info)

		self.injury_manager.calculate_injuries_from_gamelogs(2013)
		injuries = self.injury_manager.get(Injury(player_id="1"))
		self.assertTrue(len(injuries) == 1)
		self.assertTrue(injuries[0].player_id == "1" and
						injuries[0].injury_date == "2014-01-03" and
						injuries[0].return_date == "2014-01-04" and
						injuries[0].details == "from calculate_injuries_from_gamelogs")

	def test_calculate_injuries_from_gamelogs_one_injury_second_game(self):
		# self.assertTrue(False)

		# Set up three games
		self.team_game_totals_info["team"] = "BOS"
		self.team_game_totals_info["season"] = 2013
		self.team_game_totals_info["game"] = 1
		self.team_game_totals_info["date"] = date(2014,1,1)
		self.test_util.insert_into_team_game_totals(self.team_game_totals_info)

		self.team_game_totals_info["game"] = 2
		self.team_game_totals_info["date"] = date(2014,1,2)
		self.test_util.insert_into_team_game_totals(self.team_game_totals_info)

		self.team_game_totals_info["game"] = 3
		self.team_game_totals_info["date"] = date(2014,1,3)
		self.test_util.insert_into_team_game_totals(self.team_game_totals_info)

		# Set up a player who has played in two of the games above.
		self.player_info["id"] = "1"
		self.player_info["name"] = "1"
		self.player_info["position"] = "PG"
		self.player_info["rg_position"] = "PG"
		self.test_util.insert_into_players(self.player_info)

		self.game_totals_basic_info["player_id"] = self.player_info["id"]
		self.game_totals_basic_info["season"] = 2013
		self.game_totals_basic_info["game_number"] = 1
		self.game_totals_basic_info["team"] = "BOS"
		self.game_totals_basic_info["opponent"] = "PHI"
		self.game_totals_basic_info["date"] = date(2014,1,1)
		self.test_util.insert_into_game_totals_basic(self.game_totals_basic_info)

		# self.game_totals_basic_info["player_id"] = self.player_info["id"]
		# self.game_totals_basic_info["season"] = 2013
		# self.game_totals_basic_info["game_number"] = 2
		# self.game_totals_basic_info["team"] = "BOS"
		# self.game_totals_basic_info["opponent"] = "PHI"
		# self.game_totals_basic_info["date"] = date(2014,1,2)
		# self.test_util.insert_into_game_totals_basic(self.game_totals_basic_info)

		self.game_totals_basic_info["player_id"] = self.player_info["id"]
		self.game_totals_basic_info["season"] = 2013
		self.game_totals_basic_info["game_number"] = 3
		self.game_totals_basic_info["team"] = "BOS"
		self.game_totals_basic_info["opponent"] = "PHI"
		self.game_totals_basic_info["date"] = date(2014,1,3)
		self.test_util.insert_into_game_totals_basic(self.game_totals_basic_info)

		self.injury_manager.calculate_injuries_from_gamelogs(2013)
		injuries = self.injury_manager.get(Injury(player_id="1"))
		self.assertTrue(len(injuries) == 1)

	def test_calculate_injuries_from_gamelogs_one_injury_first_game(self):
		# self.assertTrue(False)

		# Set up three games
		self.team_game_totals_info["team"] = "BOS"
		self.team_game_totals_info["season"] = 2013
		self.team_game_totals_info["game"] = 1
		self.team_game_totals_info["date"] = date(2014,1,1)
		self.test_util.insert_into_team_game_totals(self.team_game_totals_info)

		self.team_game_totals_info["game"] = 2
		self.team_game_totals_info["date"] = date(2014,1,2)
		self.test_util.insert_into_team_game_totals(self.team_game_totals_info)

		self.team_game_totals_info["game"] = 3
		self.team_game_totals_info["date"] = date(2014,1,3)
		self.test_util.insert_into_team_game_totals(self.team_game_totals_info)

		# Set up a player who has played in two of the games above.
		self.player_info["id"] = "1"
		self.player_info["name"] = "1"
		self.player_info["position"] = "PG"
		self.player_info["rg_position"] = "PG"
		self.test_util.insert_into_players(self.player_info)

		# self.game_totals_basic_info["player_id"] = self.player_info["id"]
		# self.game_totals_basic_info["season"] = 2013
		# self.game_totals_basic_info["game_number"] = 1
		# self.game_totals_basic_info["team"] = "BOS"
		# self.game_totals_basic_info["opponent"] = "PHI"
		# self.game_totals_basic_info["date"] = date(2014,1,1)
		# self.test_util.insert_into_game_totals_basic(self.game_totals_basic_info)

		self.game_totals_basic_info["player_id"] = self.player_info["id"]
		self.game_totals_basic_info["season"] = 2013
		self.game_totals_basic_info["game_number"] = 2
		self.game_totals_basic_info["team"] = "BOS"
		self.game_totals_basic_info["opponent"] = "PHI"
		self.game_totals_basic_info["date"] = date(2014,1,2)
		self.test_util.insert_into_game_totals_basic(self.game_totals_basic_info)

		self.game_totals_basic_info["player_id"] = self.player_info["id"]
		self.game_totals_basic_info["season"] = 2013
		self.game_totals_basic_info["game_number"] = 3
		self.game_totals_basic_info["team"] = "BOS"
		self.game_totals_basic_info["opponent"] = "PHI"
		self.game_totals_basic_info["date"] = date(2014,1,3)
		self.test_util.insert_into_game_totals_basic(self.game_totals_basic_info)

		self.injury_manager.calculate_injuries_from_gamelogs(2013)
		injuries = self.injury_manager.get(Injury(player_id="1"))
		self.assertTrue(len(injuries) == 1)

	def test_calculate_injuries_from_gamelogs_two_injuries(self):
		# Set up three games
		self.team_game_totals_info["team"] = "BOS"
		self.team_game_totals_info["season"] = 2013
		self.team_game_totals_info["game"] = 1
		self.team_game_totals_info["date"] = date(2014,1,1)
		self.test_util.insert_into_team_game_totals(self.team_game_totals_info)

		self.team_game_totals_info["game"] = 2
		self.team_game_totals_info["date"] = date(2014,1,2)
		self.test_util.insert_into_team_game_totals(self.team_game_totals_info)

		self.team_game_totals_info["game"] = 3
		self.team_game_totals_info["date"] = date(2014,1,3)
		self.test_util.insert_into_team_game_totals(self.team_game_totals_info)

		# Set up a player who has played in two of the games above.
		self.player_info["id"] = "1"
		self.player_info["name"] = "1"
		self.player_info["position"] = "PG"
		self.player_info["rg_position"] = "PG"
		self.test_util.insert_into_players(self.player_info)

		# self.game_totals_basic_info["player_id"] = self.player_info["id"]
		# self.game_totals_basic_info["season"] = 2013
		# self.game_totals_basic_info["game_number"] = 1
		# self.game_totals_basic_info["team"] = "BOS"
		# self.game_totals_basic_info["opponent"] = "PHI"
		# self.game_totals_basic_info["date"] = date(2014,1,1)
		# self.test_util.insert_into_game_totals_basic(self.game_totals_basic_info)

		# self.game_totals_basic_info["player_id"] = self.player_info["id"]
		# self.game_totals_basic_info["season"] = 2013
		# self.game_totals_basic_info["game_number"] = 2
		# self.game_totals_basic_info["team"] = "BOS"
		# self.game_totals_basic_info["opponent"] = "PHI"
		# self.game_totals_basic_info["date"] = date(2014,1,2)
		# self.test_util.insert_into_game_totals_basic(self.game_totals_basic_info)

		self.game_totals_basic_info["player_id"] = self.player_info["id"]
		self.game_totals_basic_info["season"] = 2013
		self.game_totals_basic_info["game_number"] = 3
		self.game_totals_basic_info["team"] = "BOS"
		self.game_totals_basic_info["opponent"] = "PHI"
		self.game_totals_basic_info["date"] = date(2014,1,3)
		self.test_util.insert_into_game_totals_basic(self.game_totals_basic_info)

		self.injury_manager.calculate_injuries_from_gamelogs(2013)
		injuries = self.injury_manager.get(Injury(player_id="1"))
		self.assertTrue(len(injuries) == 2)

	def test_calculate_injuries_from_gamelogs_player_traded(self):
		# Set up six games, three for each team
		self.team_game_totals_info["team"] = "BOS"
		self.team_game_totals_info["season"] = 2013
		self.team_game_totals_info["game"] = 1
		self.team_game_totals_info["date"] = date(2014,1,1)
		self.test_util.insert_into_team_game_totals(self.team_game_totals_info)

		self.team_game_totals_info["game"] = 2
		self.team_game_totals_info["date"] = date(2014,1,3)
		self.test_util.insert_into_team_game_totals(self.team_game_totals_info)

		self.team_game_totals_info["game"] = 3
		self.team_game_totals_info["date"] = date(2014,1,5)
		self.test_util.insert_into_team_game_totals(self.team_game_totals_info)

		self.team_game_totals_info["team"] = "PHI"
		self.team_game_totals_info["season"] = 2013
		self.team_game_totals_info["game"] = 1
		self.team_game_totals_info["date"] = date(2014,1,2)
		self.test_util.insert_into_team_game_totals(self.team_game_totals_info)

		self.team_game_totals_info["game"] = 2
		self.team_game_totals_info["date"] = date(2014,1,4)
		self.test_util.insert_into_team_game_totals(self.team_game_totals_info)

		self.team_game_totals_info["game"] = 3
		self.team_game_totals_info["date"] = date(2014,1,6)
		self.test_util.insert_into_team_game_totals(self.team_game_totals_info)

		# Set up a player who has played in two of the games above.
		self.player_info["id"] = "1"
		self.player_info["name"] = "1"
		self.player_info["position"] = "PG"
		self.player_info["rg_position"] = "PG"
		self.test_util.insert_into_players(self.player_info)

		self.game_totals_basic_info["player_id"] = self.player_info["id"]
		self.game_totals_basic_info["season"] = 2013
		self.game_totals_basic_info["game_number"] = 1
		self.game_totals_basic_info["team"] = "BOS"
		self.game_totals_basic_info["opponent"] = "PHI"
		self.game_totals_basic_info["date"] = date(2014,1,1)
		self.test_util.insert_into_game_totals_basic(self.game_totals_basic_info)

		self.game_totals_basic_info["player_id"] = self.player_info["id"]
		self.game_totals_basic_info["season"] = 2013
		self.game_totals_basic_info["game_number"] = 2
		self.game_totals_basic_info["team"] = "PHI"
		self.game_totals_basic_info["opponent"] = "LAL"
		self.game_totals_basic_info["date"] = date(2014,1,4)
		self.test_util.insert_into_game_totals_basic(self.game_totals_basic_info)

		self.game_totals_basic_info["player_id"] = self.player_info["id"]
		self.game_totals_basic_info["season"] = 2013
		self.game_totals_basic_info["game_number"] = 3
		self.game_totals_basic_info["team"] = "PHI"
		self.game_totals_basic_info["opponent"] = "TOR"
		self.game_totals_basic_info["date"] = date(2014,1,6)
		self.test_util.insert_into_game_totals_basic(self.game_totals_basic_info)

		self.injury_manager.calculate_injuries_from_gamelogs(2013)
		injuries = self.injury_manager.get(Injury(player_id="1"))
		self.assertTrue(len(injuries) == 2)
		self.assertTrue(injuries[0].injury_date == "2014-01-02" and injuries[1].injury_date == "2014-01-03")

	def test_calculate_injuries_from_gamelogs_player_traded2(self):
		# Set up six games, three for each team
		self.team_game_totals_info["team"] = "BOS"
		self.team_game_totals_info["season"] = 2013
		self.team_game_totals_info["game"] = 1
		self.team_game_totals_info["date"] = date(2014,1,1)
		self.test_util.insert_into_team_game_totals(self.team_game_totals_info)

		self.team_game_totals_info["game"] = 2
		self.team_game_totals_info["date"] = date(2014,1,3)
		self.test_util.insert_into_team_game_totals(self.team_game_totals_info)

		self.team_game_totals_info["game"] = 3
		self.team_game_totals_info["date"] = date(2014,1,5)
		self.test_util.insert_into_team_game_totals(self.team_game_totals_info)

		self.team_game_totals_info["team"] = "PHI"
		self.team_game_totals_info["season"] = 2013
		self.team_game_totals_info["game"] = 1
		self.team_game_totals_info["date"] = date(2014,1,2)
		self.test_util.insert_into_team_game_totals(self.team_game_totals_info)

		self.team_game_totals_info["game"] = 2
		self.team_game_totals_info["date"] = date(2014,1,4)
		self.test_util.insert_into_team_game_totals(self.team_game_totals_info)

		self.team_game_totals_info["game"] = 3
		self.team_game_totals_info["date"] = date(2014,1,6)
		self.test_util.insert_into_team_game_totals(self.team_game_totals_info)

		# Set up a player who has played in two of the games above.
		self.player_info["id"] = "1"
		self.player_info["name"] = "1"
		self.player_info["position"] = "PG"
		self.player_info["rg_position"] = "PG"
		self.test_util.insert_into_players(self.player_info)

		self.game_totals_basic_info["player_id"] = self.player_info["id"]
		self.game_totals_basic_info["season"] = 2013
		self.game_totals_basic_info["game_number"] = 1
		self.game_totals_basic_info["team"] = "BOS"
		self.game_totals_basic_info["opponent"] = "PHI"
		self.game_totals_basic_info["date"] = date(2014,1,1)
		self.test_util.insert_into_game_totals_basic(self.game_totals_basic_info)

		self.game_totals_basic_info["player_id"] = self.player_info["id"]
		self.game_totals_basic_info["season"] = 2013
		self.game_totals_basic_info["game_number"] = 2
		self.game_totals_basic_info["team"] = "BOS"
		self.game_totals_basic_info["opponent"] = "LAL"
		self.game_totals_basic_info["date"] = date(2014,1,3)
		self.test_util.insert_into_game_totals_basic(self.game_totals_basic_info)

		self.game_totals_basic_info["player_id"] = self.player_info["id"]
		self.game_totals_basic_info["season"] = 2013
		self.game_totals_basic_info["game_number"] = 3
		self.game_totals_basic_info["team"] = "PHI"
		self.game_totals_basic_info["opponent"] = "TOR"
		self.game_totals_basic_info["date"] = date(2014,1,6)
		self.test_util.insert_into_game_totals_basic(self.game_totals_basic_info)

		self.injury_manager.calculate_injuries_from_gamelogs(2013)
		injuries = self.injury_manager.get(Injury(player_id="1"))
		self.assertTrue(len(injuries) == 2)
		self.assertTrue(injuries[0].injury_date == "2014-01-04" and injuries[1].injury_date == "2014-01-05")

	def test_calculate_injuries_from_gamelogs_player_traded_twice(self):
		"""
		Creates a player that has played six games for three different teams.  This tests the
		abilities of the function to detect multiple trades, as well as detecting injury days
		in the middle of a stretch where the player is with the same team.
		"""
		# Set up nine games, three for each team
		self.team_game_totals_info["team"] = "BOS"
		self.team_game_totals_info["season"] = 2013
		self.team_game_totals_info["game"] = 1
		self.team_game_totals_info["date"] = date(2014,1,1)
		self.test_util.insert_into_team_game_totals(self.team_game_totals_info)

		self.team_game_totals_info["game"] = 2
		self.team_game_totals_info["date"] = date(2014,1,2)
		self.test_util.insert_into_team_game_totals(self.team_game_totals_info)

		self.team_game_totals_info["game"] = 3
		self.team_game_totals_info["date"] = date(2014,1,3)
		self.test_util.insert_into_team_game_totals(self.team_game_totals_info)

		self.team_game_totals_info["game"] = 4
		self.team_game_totals_info["date"] = date(2014,1,4)
		self.test_util.insert_into_team_game_totals(self.team_game_totals_info)

		self.team_game_totals_info["team"] = "PHI"
		self.team_game_totals_info["season"] = 2013
		self.team_game_totals_info["game"] = 1
		self.team_game_totals_info["date"] = date(2014,1,2)
		self.test_util.insert_into_team_game_totals(self.team_game_totals_info)

		self.team_game_totals_info["game"] = 2
		self.team_game_totals_info["date"] = date(2014,1,3)
		self.test_util.insert_into_team_game_totals(self.team_game_totals_info)

		self.team_game_totals_info["game"] = 3
		self.team_game_totals_info["date"] = date(2014,1,4)
		self.test_util.insert_into_team_game_totals(self.team_game_totals_info)

		self.team_game_totals_info["game"] = 4
		self.team_game_totals_info["date"] = date(2014,1,5)
		self.test_util.insert_into_team_game_totals(self.team_game_totals_info)

		self.team_game_totals_info["game"] = 5
		self.team_game_totals_info["date"] = date(2014,1,6)
		self.test_util.insert_into_team_game_totals(self.team_game_totals_info)

		self.team_game_totals_info["game"] = 6
		self.team_game_totals_info["date"] = date(2014,1,7)
		self.test_util.insert_into_team_game_totals(self.team_game_totals_info)

		self.team_game_totals_info["team"] = "LAL"
		self.team_game_totals_info["season"] = 2013
		self.team_game_totals_info["game"] = 1
		self.team_game_totals_info["date"] = date(2014,1,6)
		self.test_util.insert_into_team_game_totals(self.team_game_totals_info)

		self.team_game_totals_info["game"] = 2
		self.team_game_totals_info["date"] = date(2014,1,7)
		self.test_util.insert_into_team_game_totals(self.team_game_totals_info)

		self.team_game_totals_info["game"] = 3
		self.team_game_totals_info["date"] = date(2014,1,8)
		self.test_util.insert_into_team_game_totals(self.team_game_totals_info)

		self.team_game_totals_info["game"] = 4
		self.team_game_totals_info["date"] = date(2014,1,9)
		self.test_util.insert_into_team_game_totals(self.team_game_totals_info)

		# Set up a player
		self.player_info["id"] = "1"
		self.player_info["name"] = "1"
		self.player_info["position"] = "PG"
		self.player_info["rg_position"] = "PG"
		self.test_util.insert_into_players(self.player_info)

		# Set up player participating in games
		self.game_totals_basic_info["player_id"] = self.player_info["id"]
		self.game_totals_basic_info["season"] = 2013
		self.game_totals_basic_info["game_number"] = 1
		self.game_totals_basic_info["team"] = "BOS"
		self.game_totals_basic_info["opponent"] = "PHI"
		self.game_totals_basic_info["date"] = date(2014,1,1)
		self.test_util.insert_into_game_totals_basic(self.game_totals_basic_info)

		self.game_totals_basic_info["game_number"] = 2
		self.game_totals_basic_info["team"] = "BOS"
		self.game_totals_basic_info["opponent"] = "LAL"
		self.game_totals_basic_info["date"] = date(2014,1,2)
		self.test_util.insert_into_game_totals_basic(self.game_totals_basic_info)

		self.game_totals_basic_info["game_number"] = 3
		self.game_totals_basic_info["team"] = "PHI"
		self.game_totals_basic_info["opponent"] = "TOR"
		self.game_totals_basic_info["date"] = date(2014,1,4)
		self.test_util.insert_into_game_totals_basic(self.game_totals_basic_info)

		# self.game_totals_basic_info["game_number"] = 4
		# self.game_totals_basic_info["team"] = "PHI"
		# self.game_totals_basic_info["opponent"] = "TOR"
		# self.game_totals_basic_info["date"] = date(2014,1,5)
		# self.test_util.insert_into_game_totals_basic(self.game_totals_basic_info)

		self.game_totals_basic_info["game_number"] = 5
		self.game_totals_basic_info["team"] = "PHI"
		self.game_totals_basic_info["opponent"] = "TOR"
		self.game_totals_basic_info["date"] = date(2014,1,6)
		self.test_util.insert_into_game_totals_basic(self.game_totals_basic_info)

		self.game_totals_basic_info["game_number"] = 6
		self.game_totals_basic_info["team"] = "LAL"
		self.game_totals_basic_info["opponent"] = "TOR"
		self.game_totals_basic_info["date"] = date(2014,1,8)
		self.test_util.insert_into_game_totals_basic(self.game_totals_basic_info)

		self.game_totals_basic_info["game_number"] = 7
		self.game_totals_basic_info["team"] = "LAL"
		self.game_totals_basic_info["opponent"] = "TOR"
		self.game_totals_basic_info["date"] = date(2014,1,9)
		self.test_util.insert_into_game_totals_basic(self.game_totals_basic_info)

		self.injury_manager.calculate_injuries_from_gamelogs(2013)
		injuries = self.injury_manager.get(Injury(player_id="1"))
		self.assertTrue(len(injuries) == 3)
		self.assertTrue(injuries[0].injury_date == "2014-01-03" and
						injuries[1].injury_date == "2014-01-05" and
						injuries[2].injury_date == "2014-01-07")

	def test_scrape_injury_report_update_injured_player(self):
		"""
		Test that a day-to-day player whose previous return date was today has it updated to tomorrow.
		"""
		# Set up a player
		self.player_info["id"] = "teaguje01"
		self.player_info["name"] = "Jeff Teague"
		self.player_info["position"] = "PG"
		self.player_info["rg_position"] = "PG"
		self.test_util.insert_into_players(self.player_info)

		one_day = timedelta(days=1)
		today = date.today()
		tomorrow = today + one_day

		injury = Injury(player_id="teaguje01", injury_date=date(2014, 1, 24), return_date=today, details="ankle")
		self.injury_manager.insert(injury)

		self.injury_manager.scrape_injury_report(season=2013, source="file")

		injuries = self.injury_manager.get(Injury(player_id="teaguje01"))
		self.assertTrue(len(injuries) == 1)
		self.assertTrue(injuries[0].injury_date == "2014-01-24" and injuries[0].return_date == str(tomorrow))

	def test_scrape_injury_report_update_injured_player_out_for_season(self):
		"""
		Make sure that the return date (beginning of next season) for an existing injury is not
		updated to tomorrow by the script.  It should be left alone.
		"""
		# Set up a player
		self.player_info["id"] = "teaguje01"
		self.player_info["name"] = "Jeff Teague"
		self.player_info["position"] = "PG"
		self.player_info["rg_position"] = "PG"
		self.test_util.insert_into_players(self.player_info)

		injury = Injury(player_id="teaguje01", injury_date=date(2014, 1, 24), return_date=date(2014, 11, 01), details="ankle")
		self.injury_manager.insert(injury)

		self.injury_manager.scrape_injury_report(season=2013, source="file")

		injuries = self.injury_manager.get(Injury(player_id="teaguje01"))
		self.assertTrue(len(injuries) == 1)
		self.assertTrue(injuries[0].injury_date == "2014-01-24" and injuries[0].return_date == "2014-11-01")

	def test_scrape_injury_report_add_new_injury(self):
		"""
		Make sure that a newly injured player is inserted into the database.
		"""
		# Set up a player
		self.player_info["id"] = "teaguje01"
		self.player_info["name"] = "Jeff Teague"
		self.player_info["position"] = "PG"
		self.player_info["rg_position"] = "PG"
		self.test_util.insert_into_players(self.player_info)

		self.injury_manager.scrape_injury_report(season=2013, source="file")

		injuries = self.injury_manager.get(Injury(player_id="teaguje01"))
		self.assertTrue(len(injuries) == 1)
		self.assertTrue(injuries[0].injury_date == "2014-01-24" and injuries[0].return_date == str(self.tomorrow))

	def test_scrape_injury_report_unknown_player(self):
		"""
		Make sure we don't modify the database when we encounter an unknown player.  Instead, just
		alert the user running the script to resolve this manually.
		"""
		self.injury_manager.scrape_injury_report(season=2013, source="file")

		injuries = self.injury_manager.get(Injury(player_id="teaguje01"))
		self.assertTrue(len(injuries) == 0)

	def test_scrape_injury_report_old_and_new_player_with_same_name(self):
		"""
		Make sure that a newly injured player is inserted into the database.
		"""
		# Set up a player
		self.player_info["id"] = "teaguje01"
		self.player_info["name"] = "Jeff Teague"
		self.player_info["position"] = "PG"
		self.test_util.insert_into_players(self.player_info)

		self.player_info["id"] = "teaguje02"
		self.player_info["name"] = "Jeff Teague"
		self.player_info["position"] = "PG"
		self.player_info["rg_position"] = "PG"
		self.test_util.insert_into_players(self.player_info)

		self.injury_manager.scrape_injury_report(season=2013, source="file")

		injuries = self.injury_manager.get(Injury(player_id="teaguje01"))
		self.assertTrue(len(injuries) == 0)

		injuries = self.injury_manager.get(Injury(player_id="teaguje02"))
		self.assertTrue(len(injuries) == 1)
		self.assertTrue(injuries[0].injury_date == "2014-01-24" and injuries[0].return_date == str(self.tomorrow))

	def test_fix_injury_entry_first_day_not_injury(self):
		"""
		Create a three-day injury, where the first day is actually not the first day
		the player missed time.

		In this case, the injury should be shortened to two days, with the previously-middle
		day becoming the first.
		"""
		injury = Injury(id=1, player_id="test", injury_date=date(2014, 1, 1), return_date=date(2014, 1, 4), details="testing")
		self.injury_manager.insert(injury)
		self.injury_manager.fix_injury_entry(injury, date(2014, 1, 1))

		result = self.injury_manager.get(Injury(player_id="test"))
		self.assertTrue(result[0].injury_date == "2014-01-02" and result[0].return_date == "2014-01-04")

	def test_fix_injury_entry_last_day_not_injury(self):
		"""
		Create a three-day injury, where the last day is actually not the first day
		the player missed time.

		In this case, the injury should be shortened to two days, with the previously-middle
		day becoming the last.
		"""
		injury = Injury(id=1, player_id="test", injury_date=date(2014, 1, 1), return_date=date(2014, 1, 4), details="testing")
		self.injury_manager.insert(injury)
		self.injury_manager.fix_injury_entry(injury, date(2014, 1, 3))

		result = self.injury_manager.get(Injury(player_id="test"))
		self.assertTrue(result[0].injury_date == "2014-01-01" and result[0].return_date == "2014-01-03")

	def test_fix_injury_entry_middle_day_not_injury(self):
		"""
		Create a three-day injury, where the middle day is actually not the first day
		the player missed time.

		In this case, the injury will be split in two.  The existing injury will be shortened
		so the return date is the original middle injury day.  Then, a second injury will be
		created with the injury_date set as the last injury day and the return date of the day after.
		"""
		injury = Injury(id=1, player_id="test", injury_date=date(2014, 1, 1), return_date=date(2014, 1, 4), details="testing")
		self.injury_manager.insert(injury)
		self.injury_manager.fix_injury_entry(injury, date(2014, 1, 2))

		result = self.injury_manager.get(Injury(player_id="test"))
		self.assertTrue(len(result) == 2)
		self.assertTrue(result[0].injury_date == "2014-01-01" and result[0].return_date == "2014-01-02")
		self.assertTrue(result[1].injury_date == "2014-01-03" and result[1].return_date == "2014-01-04")

	def test_fix_injury_entry_single_day_not_injury(self):
		"""
		Create a single-day injury, where that day is actually not a day that the player missed time.

		In this case, the injury will just be deleted.
		"""
		injury = Injury(id=1, player_id="test", injury_date=date(2014, 1, 1), return_date=date(2014, 1, 2), details="testing")
		self.injury_manager.insert(injury)
		self.injury_manager.fix_injury_entry(injury, date(2014, 1, 1))

		result = self.injury_manager.get(Injury(player_id="test"))
		self.assertTrue(len(result) == 0)

	def test_is_player_injured(self):
		"""
		Create an injury that spans one day and call is_player_injured with one date that is within the
		injury range and one that is not.
		Also do this with a string since both are accepted.
		"""
		injury = Injury(id=1, player_id="test", injury_date=date(2014, 1, 1), return_date=date(2014, 1, 2), details="testing")
		self.injury_manager.insert(injury)

		self.assertTrue(self.injury_manager.is_player_injured("test", date(2014, 1, 1)))
		self.assertFalse(self.injury_manager.is_player_injured("test", date(2014, 1, 2)))

		self.assertTrue(self.injury_manager.is_player_injured("test", "2014-01-01"))
		self.assertFalse(self.injury_manager.is_player_injured("test", "2014-01-02"))

	def test_fix_injuries_three_game_between_injury_span(self):
		injury = Injury(player_id="dan", injury_date=date(2014, 2, 10), return_date=date(2014, 3, 2), details="test")

		self.injury_manager.insert(injury)

		gtb_info = self.test_util.generate_default_game_totals_basic_info()
		gtb_info["player_id"] = "dan"
		gtb_info["season"] = 2013
		gtb_info["date"] = "2014-02-12"
		self.test_util.insert_into_game_totals_basic(gtb_info)

		gtb_info["date"] = "2014-02-18"
		self.test_util.insert_into_game_totals_basic(gtb_info)

		gtb_info["date"] = "2014-02-19"
		self.test_util.insert_into_game_totals_basic(gtb_info)

		self.injury_manager.fix_injuries(2013)

		injuries = self.injury_manager.get(Injury())
		self.assertTrue(len(injuries) == 3)

		self.assertTrue(injuries[0].injury_date == "2014-02-10" and injuries[0].return_date == "2014-02-12")
		self.assertTrue(injuries[1].injury_date == "2014-02-13" and injuries[1].return_date == "2014-02-18")
		self.assertTrue(injuries[2].injury_date == "2014-02-20" and injuries[2].return_date == "2014-03-02")

	def test_fix_injuries_first_day_and_middle_day(self):
		injury = Injury(player_id="dan", injury_date="2014-02-09", return_date="2014-03-04", details="test")

		self.injury_manager.insert(injury)

		gtb_info = self.test_util.generate_default_game_totals_basic_info()
		gtb_info["player_id"] = "dan"
		gtb_info["season"] = 2013
		gtb_info["date"] = "2014-02-09"
		self.test_util.insert_into_game_totals_basic(gtb_info)

		gtb_info["date"] = "2014-02-11"
		self.test_util.insert_into_game_totals_basic(gtb_info)

		self.injury_manager.fix_injuries(2013)

		injuries = self.injury_manager.get(Injury())
		self.assertTrue(len(injuries) == 2)

		self.assertTrue(injuries[0].injury_date == "2014-02-10" and injuries[0].return_date == "2014-02-11")
		self.assertTrue(injuries[1].injury_date == "2014-02-12" and injuries[1].return_date == "2014-03-04")

	def test_fix_injuries_middle_day_and_last_day(self):
		injury = Injury(player_id="dan", injury_date="2014-02-09", return_date="2014-02-11", details="test")

		self.injury_manager.insert(injury)

		gtb_info = self.test_util.generate_default_game_totals_basic_info()
		gtb_info["player_id"] = "dan"
		gtb_info["season"] = 2013
		gtb_info["date"] = "2014-02-10"
		self.test_util.insert_into_game_totals_basic(gtb_info)

		self.injury_manager.fix_injuries(2013)

		injuries = self.injury_manager.get(Injury())
		self.assertTrue(len(injuries) == 1)

		self.assertTrue(injuries[0].injury_date == "2014-02-09" and injuries[0].return_date == "2014-02-10")

	def test_fix_injuries_duplicates(self):
		injury = Injury(player_id="dan", injury_date=date(2014, 2, 10), return_date=date(2014, 3, 2), details="test")
		injury2 = Injury(player_id="dan", injury_date=date(2014, 2, 10), return_date=date(2014, 3, 2), details="test")
		injury3 = Injury(player_id="dan", injury_date=date(2014, 2, 9), return_date=date(2014, 3, 2), details="test")

		self.injury_manager.insert(injury)
		self.injury_manager.insert(injury2)
		self.injury_manager.insert(injury3)

		self.injury_manager.fix_injuries(2013)

		injuries = self.injury_manager.get(Injury())
		self.assertTrue(len(injuries) == 2)

		self.assertTrue(injuries[0].injury_date == "2014-02-10" and injuries[0].return_date == "2014-03-02")
		self.assertTrue(injuries[1].injury_date == "2014-02-09" and injuries[1].return_date == "2014-03-02")

if __name__ == '__main__':
	unittest.main()