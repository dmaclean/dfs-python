__author__ = 'ap'

from datetime import date
from unittest import TestCase
import BBRTestUtility
from dfs_constants import DFSConstants
from projections import Projections
from models.defense_vs_position import DefenseVsPosition
from models.defense_vs_position_manager import DefenseVsPositionManager

class TestDefenseVsPosition(TestCase):
	def setUp(self):
		self.testUtil = BBRTestUtility.BBRTestUtility()
		self.projections = Projections(cnx=self.testUtil.conn)
		self.dvpManager = DefenseVsPositionManager(cnx=self.testUtil.conn)
		self.testUtil.runSQL()

		# Initialize the player info map.
		self.player_info = {
			"id": "",
			"name": "Test",
			"position": "G",
			"height": 0,
			"weight": 0,
			"url": "something"
		}

		# Initialize the player game totals map.
		self.game_totals_basic_info = {
			"player_id": "test",
			"season": date.today().year,
			"game_number": 0,
			"date": date.today(),
			"age": 0,
			"team": "BOS",
			"home": True,
			"opponent": "BOS",
			"result": "",
			"games_started": 0,
			"minutes_played": 0,
			"field_goals": 0,
			"field_goal_attempts": 0,
			"field_goal_pct": 0,
			"three_point_field_goals": 0,
			"three_point_field_goal_attempts": 0,
			"three_point_field_goal_pct": 0,
			"free_throws": 0,
			"free_throw_attempts": 0,
			"free_throw_pct": 0,
			"offensive_rebounds": 0,
			"defensive_rebounds": 0,
			"total_rebounds": 0,
			"assists": 0,
			"steals": 0,
			"blocks": 0,
			"turnovers": 0,
			"personal_fouls": 0,
			"points": 0,
			"game_score": 0,
			"plus_minus": 0
		}

		# Initialize the team game totals map.
		self.team_game_totals_info = {
			"team": "",
			"season": date.today().year,
			"game": 0,
			"date": date.today(),
			"home": True,
			"opponent": "",
			"result": "",
			"minutes_played": 240,
			"field_goals": 0,
			"field_goal_attempts": 0,
			"three_point_field_goals": 0,
			"three_point_field_goal_attempts": 0,
			"free_throws": 0,
			"free_throw_attempts": 0,
			"offensive_rebounds": 0,
			"total_rebounds": 0,
			"assists": 0,
			"steals": 0,
			"blocks": 0,
			"turnovers": 0,
			"personal_fouls": 0,
			"points": 0,
			"opp_field_goals": 0,
			"opp_field_goal_attempts": 0,
			"opp_three_point_field_goals": 0,
			"opp_three_point_field_goal_attempts": 0,
			"opp_free_throws": 0,
			"opp_free_throw_attempts": 0,
			"opp_offensive_rebounds": 0,
			"opp_total_rebounds": 0,
			"opp_assists": 0,
			"opp_steals": 0,
			"opp_blocks": 0,
			"opp_turnovers": 0,
			"opp_personal_fouls": 0,
			"opp_points": 0
		}

		self.fantasy_points_info = self.testUtil.generate_default_fantasy_points_info()

	def tearDown(self):
		self.testUtil = None
		self.dvpManager = None

	def test_db_operations(self):
		dvp = DefenseVsPosition()
		dvp.stat = "field_goals"
		dvp.position = "PG"
		dvp.team = "BOS"
		dvp.season = 2013
		dvp.value = 10.5
		dvp.date = date(2014,1,1)

		self.assertTrue(not self.dvpManager.exists(dvp))

		self.dvpManager.insert(dvp)

		self.assertTrue(self.dvpManager.exists(dvp))

		dvps = self.dvpManager.get(dvp)
		self.assertTrue(len(dvps) == 1)
		self.assertTrue(dvps[0].stat == "field_goals" and dvps[0].position == "PG" and dvps[0].value == 10.5)

		dvp2 = dvps[0]
		dvp2.value = 30

		self.dvpManager.update(dvp2)
		dvps = self.dvpManager.get(dvp2)

		self.assertTrue(len(dvps) == 1 and dvps[0].value == 30)

		# Test get with no id
		dvp_no_id = DefenseVsPosition(stat="field_goals", position="PG", team="BOS", season=2013, date=date(2014,1,1))
		dvps = self.dvpManager.get(dvp_no_id)

		self.assertTrue(len(dvps) == 1 and dvps[0].value == 30)

	def test_db_operations_with_site(self):
		dvp = DefenseVsPosition()
		dvp.stat = "field_goals"
		dvp.position = "PG"
		dvp.team = "BOS"
		dvp.season = 2013
		dvp.value = 10.5
		dvp.date = date(2014,1,1)
		dvp.site = DFSConstants.FAN_DUEL

		self.assertTrue(not self.dvpManager.exists(dvp))

		self.dvpManager.insert(dvp)

		self.assertTrue(self.dvpManager.exists(dvp))

		dvps = self.dvpManager.get(dvp)
		self.assertTrue(len(dvps) == 1)
		self.assertTrue(dvps[0].stat == "field_goals" and dvps[0].position == "PG" and dvps[0].value == 10.5 and
						dvps[0].site == DFSConstants.FAN_DUEL)

		dvp2 = dvps[0]
		dvp2.value = 30
		dvp2.site = DFSConstants.DRAFT_KINGS

		self.dvpManager.update(dvp2)
		dvps = self.dvpManager.get(dvp2)

		self.assertTrue(len(dvps) == 1 and dvps[0].value == 30 and dvps[0].site == DFSConstants.DRAFT_KINGS)

		# Test get with no id
		dvp_no_id = DefenseVsPosition(stat="field_goals", position="PG", team="BOS", season=2013, date=date(2014,1,1))
		dvps = self.dvpManager.get(dvp_no_id)

		self.assertTrue(len(dvps) == 1 and dvps[0].value == 30)


	###################################################################################
	# Tests the computation of the stats compiled against a team by its opponents
	#  at a position, starting from the beginning of the season to a particular date.
	###################################################################################
	def test_calculate_defense_vs_position(self):
		positions = ["PG", "SG", "SF", "PF", "C"]

		for p in positions:
			# Set up two guards that played against a team on separate days
			self.player_info["id"] = p + "1"
			self.player_info["name"] = p + " 1"
#			self.player_info["position"] = p
			self.player_info["rg_position"] = p
			self.testUtil.insert_into_players(self.player_info)

			self.player_info["id"] = p + "2"
			self.player_info["name"] = p +" 2"
			self.testUtil.insert_into_players(self.player_info)

			# Another player, PG if p=SG, SG if p=PG, SF if p=PF, PF if p=SF
			self.player_info["id"] = p + "3"
			self.player_info["name"] = p + " 3"
			if p == "PG":
				self.player_info["rg_position"] = "SG"
			elif p == "SG":
				self.player_info["rg_position"] = "PG"
			elif p == "SF":
				self.player_info["rg_position"] = "PF"
			elif p == "PF":
				self.player_info["rg_position"] = "SF"
			elif p == "C":
				self.player_info["rg_position"] = "PG"
			self.testUtil.insert_into_players(self.player_info)

			self.game_totals_basic_info["player_id"] = p+"1"
			self.game_totals_basic_info["season"] = 2013
			self.game_totals_basic_info["game_number"] = 1
			self.game_totals_basic_info["team"] = "PHI"
			self.game_totals_basic_info["opponent"] = "BOS"
			self.game_totals_basic_info["date"] = date(2013,11,1)
			self.game_totals_basic_info["points"] = 20
			self.game_totals_basic_info["offensive_rebounds"] = 5
			self.game_totals_basic_info["defensive_rebounds"] = 10
			self.game_totals_basic_info["assists"] = 4
			self.game_totals_basic_info["steals"] = 3
			self.game_totals_basic_info["blocks"] = 2
			self.game_totals_basic_info["turnovers"] = 5
			self.testUtil.insert_into_game_totals_basic(self.game_totals_basic_info)

			self.game_totals_basic_info["player_id"] = p+"2"
			self.game_totals_basic_info["season"] = 2013
			self.game_totals_basic_info["game_number"] = 2
			self.game_totals_basic_info["team"] = "PHI"
			self.game_totals_basic_info["opponent"] = "BOS"
			self.game_totals_basic_info["date"] = date(2013,11,2)
			self.game_totals_basic_info["points"] = 10
			self.game_totals_basic_info["offensive_rebounds"] = 7
			self.game_totals_basic_info["defensive_rebounds"] = 12
			self.game_totals_basic_info["assists"] = 8
			self.game_totals_basic_info["steals"] = 1
			self.game_totals_basic_info["blocks"] = 0
			self.game_totals_basic_info["turnovers"] = 3
			self.testUtil.insert_into_game_totals_basic(self.game_totals_basic_info)

			self.game_totals_basic_info["player_id"] = p+"3"
			self.game_totals_basic_info["season"] = 2013
			self.game_totals_basic_info["game_number"] = 3
			self.game_totals_basic_info["team"] = "PHI"
			self.game_totals_basic_info["opponent"] = "BOS"
			self.game_totals_basic_info["date"] = date(2013,11,3)
			self.game_totals_basic_info["points"] = 10
			self.game_totals_basic_info["offensive_rebounds"] = 7
			self.game_totals_basic_info["defensive_rebounds"] = 12
			self.game_totals_basic_info["assists"] = 8
			self.game_totals_basic_info["steals"] = 1
			self.game_totals_basic_info["blocks"] = 0
			self.game_totals_basic_info["turnovers"] = 3
			self.testUtil.insert_into_game_totals_basic(self.game_totals_basic_info)

			# Set up team game total for 2nd game.
			self.team_game_totals_info["team"] = "BOS"
			self.team_game_totals_info["season"] = 2013
			self.team_game_totals_info["game"] = 2
			self.team_game_totals_info["date"] = date(2013,11,2)
			self.team_game_totals_info["opponent"] = "PHI"
			self.testUtil.insert_into_team_game_totals(self.team_game_totals_info)

			points_vs_position = self.dvpManager.calculate_defense_vs_position("points", p, "BOS", 2013, date=date(2013, 11, 2))
			offensive_rebs_vs_position = self.dvpManager.calculate_defense_vs_position("offensive_rebounds", p, "BOS",
																						2013, site=DFSConstants.FAN_DUEL,
																						date=date(2013, 11, 2))
			defensive_rebs_vs_position = self.dvpManager.calculate_defense_vs_position("defensive_rebounds", p, "BOS",
																						2013, site=DFSConstants.FAN_DUEL,
																						date=date(2013, 11, 2))
			assists_vs_position = self.dvpManager.calculate_defense_vs_position("assists", p, "BOS", 2013, date=date(2013, 11, 2))
			steals_vs_position = self.dvpManager.calculate_defense_vs_position("steals", p, "BOS", 2013, date=date(2013, 11, 2))
			blocks_vs_position = self.dvpManager.calculate_defense_vs_position("blocks", p, "BOS", 2013, date=date(2013, 11, 2))
			turnovers_vs_position = self.dvpManager.calculate_defense_vs_position("turnovers", p, "BOS", 2013, date=date(2013, 11, 2))

			self.assertTrue(points_vs_position.value == 15)
			self.assertTrue(offensive_rebs_vs_position.value == 6)
			self.assertTrue(defensive_rebs_vs_position.value == 11)
			self.assertTrue(assists_vs_position.value == 6)
			self.assertTrue(steals_vs_position.value == 2)
			self.assertTrue(blocks_vs_position.value == 1)
			self.assertTrue(turnovers_vs_position.value == 4)

			# Make sure the rank is saved.
			result = self.dvpManager.get(DefenseVsPosition(stat="points"))
			result[0].rank = 1
			self.dvpManager.update(result[0])

			new_result = self.dvpManager.get(result[0])
			self.assertTrue(new_result[0].rank == result[0].rank)

	def test_calculate_defense_vs_position_fantasy_points(self):
		positions = ["PG", "SG", "SF", "PF", "C"]

		for p in positions:
			# Set up two guards that played against a team on separate days
			self.player_info["id"] = p + "1"
			self.player_info["name"] = p + " 1"
#			self.player_info["position"] = p
			self.player_info["rg_position"] = p
			self.testUtil.insert_into_players(self.player_info)

			self.player_info["id"] = p + "2"
			self.player_info["name"] = p + " 2"
			self.testUtil.insert_into_players(self.player_info)

			# Another player, PG if p=SG, SG if p=PG, SF if p=PF, PF if p=SF
			self.player_info["id"] = p + "3"
			self.player_info["name"] = p + " 3"
			if p == "PG":
				self.player_info["rg_position"] = "SG"
			elif p == "SG":
				self.player_info["rg_position"] = "PG"
			elif p == "SF":
				self.player_info["rg_position"] = "PF"
			elif p == "PF":
				self.player_info["rg_position"] = "SF"
			elif p == "C":
				self.player_info["rg_position"] = "PG"
			self.testUtil.insert_into_players(self.player_info)

			self.game_totals_basic_info["player_id"] = p+"1"
			self.game_totals_basic_info["season"] = 2013
			self.game_totals_basic_info["game_number"] = 1
			self.game_totals_basic_info["team"] = "PHI"
			self.game_totals_basic_info["opponent"] = "BOS"
			self.game_totals_basic_info["date"] = date(2013, 11, 1)
			self.game_totals_basic_info["points"] = 20
			self.game_totals_basic_info["offensive_rebounds"] = 5
			self.game_totals_basic_info["defensive_rebounds"] = 10
			self.game_totals_basic_info["assists"] = 4
			self.game_totals_basic_info["steals"] = 3
			self.game_totals_basic_info["blocks"] = 2
			self.game_totals_basic_info["turnovers"] = 5
			gtb_id1 = self.testUtil.insert_into_game_totals_basic(self.game_totals_basic_info)

			self.game_totals_basic_info["player_id"] = p+"2"
			self.game_totals_basic_info["season"] = 2013
			self.game_totals_basic_info["game_number"] = 2
			self.game_totals_basic_info["team"] = "PHI"
			self.game_totals_basic_info["opponent"] = "BOS"
			self.game_totals_basic_info["date"] = date(2013, 11, 2)
			self.game_totals_basic_info["points"] = 10
			self.game_totals_basic_info["offensive_rebounds"] = 7
			self.game_totals_basic_info["defensive_rebounds"] = 12
			self.game_totals_basic_info["assists"] = 8
			self.game_totals_basic_info["steals"] = 1
			self.game_totals_basic_info["blocks"] = 0
			self.game_totals_basic_info["turnovers"] = 3
			gtb_id2 = self.testUtil.insert_into_game_totals_basic(self.game_totals_basic_info)

			self.game_totals_basic_info["player_id"] = p+"3"
			self.game_totals_basic_info["season"] = 2013
			self.game_totals_basic_info["game_number"] = 3
			self.game_totals_basic_info["team"] = "PHI"
			self.game_totals_basic_info["opponent"] = "BOS"
			self.game_totals_basic_info["date"] = date(2013, 11, 3)
			self.game_totals_basic_info["points"] = 10
			self.game_totals_basic_info["offensive_rebounds"] = 7
			self.game_totals_basic_info["defensive_rebounds"] = 12
			self.game_totals_basic_info["assists"] = 8
			self.game_totals_basic_info["steals"] = 1
			self.game_totals_basic_info["blocks"] = 0
			self.game_totals_basic_info["turnovers"] = 3
			gtb_id3 = self.testUtil.insert_into_game_totals_basic(self.game_totals_basic_info)

			# Set up team game total for 2nd game.
			self.team_game_totals_info["team"] = "BOS"
			self.team_game_totals_info["season"] = 2013
			self.team_game_totals_info["game"] = 2
			self.team_game_totals_info["date"] = date(2013, 11, 2)
			self.team_game_totals_info["opponent"] = "PHI"
			self.testUtil.insert_into_team_game_totals(self.team_game_totals_info)

			# Set up fantasy points
			self.fantasy_points_info["game_totals_basic_id"] = gtb_id1
			self.fantasy_points_info["player_id"] = p + "1"
			self.fantasy_points_info["site"] = DFSConstants.FAN_DUEL
			self.fantasy_points_info["season"] = 2013
			self.fantasy_points_info["game_number"] = 1
			self.fantasy_points_info["points"] = 10
			self.testUtil.insert_into_fantasy_points(self.fantasy_points_info)

			self.fantasy_points_info["game_totals_basic_id"] = gtb_id2
			self.fantasy_points_info["player_id"] = p + "2"
			self.fantasy_points_info["site"] = DFSConstants.FAN_DUEL
			self.fantasy_points_info["season"] = 2013
			self.fantasy_points_info["game_number"] = 2
			self.fantasy_points_info["points"] = 20
			self.testUtil.insert_into_fantasy_points(self.fantasy_points_info)

			points_vs_position = self.dvpManager.calculate_defense_vs_position("points", p, "BOS", 2013, date=date(2013, 11, 2))
			offensive_rebs_vs_position = self.dvpManager.calculate_defense_vs_position("offensive_rebounds", p, "BOS",
																						2013, site=DFSConstants.FAN_DUEL,
																						date=date(2013, 11, 2))
			defensive_rebs_vs_position = self.dvpManager.calculate_defense_vs_position("defensive_rebounds", p, "BOS",
																						2013, site=DFSConstants.FAN_DUEL,
																						date=date(2013, 11, 2))
			assists_vs_position = self.dvpManager.calculate_defense_vs_position("assists", p, "BOS", 2013, date=date(2013, 11, 2))
			steals_vs_position = self.dvpManager.calculate_defense_vs_position("steals", p, "BOS", 2013, date=date(2013, 11, 2))
			blocks_vs_position = self.dvpManager.calculate_defense_vs_position("blocks", p, "BOS", 2013, date=date(2013, 11, 2))
			turnovers_vs_position = self.dvpManager.calculate_defense_vs_position("turnovers", p, "BOS", 2013, date=date(2013, 11, 2))

			self.assertTrue(points_vs_position.value == 15)
			self.assertTrue(offensive_rebs_vs_position.value == 6)
			self.assertTrue(defensive_rebs_vs_position.value == 11)
			self.assertTrue(assists_vs_position.value == 6)
			self.assertTrue(steals_vs_position.value == 2)
			self.assertTrue(blocks_vs_position.value == 1)
			self.assertTrue(turnovers_vs_position.value == 4)

			fps = self.dvpManager.calculate_defense_vs_position(DFSConstants.FANTASY_POINTS, p, "BOS", 2013,
																site=DFSConstants.FAN_DUEL,
																date=date(2013, 11, 2))

			self.assertTrue(fps.value == 15)

	####################################################################################
	# Same test as above, except we specify a date that would exclude the second game.
	# This date should eliminate the second player's stats from the computation.
	####################################################################################
	def test_calculate_defense_vs_position_date_subset(self):
		positions = ["PG", "SG", "SF", "PF", "C"]

		for p in positions:
			# Set up two guards that played against a team on separate days
			self.player_info["id"] = p + "1"
			self.player_info["name"] = p + " 1"
			self.player_info["rg_position"] = p
			self.testUtil.insert_into_players(self.player_info)

			self.player_info["id"] = p + "2"
			self.player_info["name"] = p +" 2"
			self.testUtil.insert_into_players(self.player_info)

			# Another player, PG if p=SG, SG if p=PG, SF if p=PF, PF if p=SF
			self.player_info["id"] = p + "3"
			self.player_info["name"] = p + " 3"
			if p == "PG":
				self.player_info["rg_position"] = "SG"
			elif p == "SG":
				self.player_info["rg_position"] = "PG"
			elif p == "SF":
				self.player_info["rg_position"] = "PF"
			elif p == "PF":
				self.player_info["rg_position"] = "SF"
			elif p == "C":
				self.player_info["rg_position"] = "PG"
			self.testUtil.insert_into_players(self.player_info)

			self.game_totals_basic_info["player_id"] = p+"1"
			self.game_totals_basic_info["season"] = 2013
			self.game_totals_basic_info["game_number"] = 1
			self.game_totals_basic_info["team"] = "PHI"
			self.game_totals_basic_info["opponent"] = "BOS"
			self.game_totals_basic_info["date"] = date(2013,11,1)
			self.game_totals_basic_info["points"] = 20
			self.game_totals_basic_info["offensive_rebounds"] = 5
			self.game_totals_basic_info["defensive_rebounds"] = 10
			self.game_totals_basic_info["assists"] = 4
			self.game_totals_basic_info["steals"] = 3
			self.game_totals_basic_info["blocks"] = 2
			self.game_totals_basic_info["turnovers"] = 5
			self.testUtil.insert_into_game_totals_basic(self.game_totals_basic_info)

			self.game_totals_basic_info["player_id"] = p+"2"
			self.game_totals_basic_info["season"] = 2013
			self.game_totals_basic_info["game_number"] = 2
			self.game_totals_basic_info["team"] = "PHI"
			self.game_totals_basic_info["opponent"] = "BOS"
			self.game_totals_basic_info["date"] = date(2013,11,4)
			self.game_totals_basic_info["points"] = 10
			self.game_totals_basic_info["offensive_rebounds"] = 7
			self.game_totals_basic_info["defensive_rebounds"] = 12
			self.game_totals_basic_info["assists"] = 8
			self.game_totals_basic_info["steals"] = 1
			self.game_totals_basic_info["blocks"] = 0
			self.game_totals_basic_info["turnovers"] = 3
			self.testUtil.insert_into_game_totals_basic(self.game_totals_basic_info)

			self.game_totals_basic_info["player_id"] = p+"3"
			self.game_totals_basic_info["season"] = 2013
			self.game_totals_basic_info["game_number"] = 3
			self.game_totals_basic_info["team"] = "PHI"
			self.game_totals_basic_info["opponent"] = "BOS"
			self.game_totals_basic_info["date"] = date(2013,11,3)
			self.game_totals_basic_info["points"] = 10
			self.game_totals_basic_info["offensive_rebounds"] = 7
			self.game_totals_basic_info["defensive_rebounds"] = 12
			self.game_totals_basic_info["assists"] = 8
			self.game_totals_basic_info["steals"] = 1
			self.game_totals_basic_info["blocks"] = 0
			self.game_totals_basic_info["turnovers"] = 3
			self.testUtil.insert_into_game_totals_basic(self.game_totals_basic_info)

			# Set up team game total for 2nd game.
			self.team_game_totals_info["team"] = "BOS"
			self.team_game_totals_info["season"] = 2013
			self.team_game_totals_info["game"] = 1
			self.team_game_totals_info["date"] = date(2013,11,1)
			self.team_game_totals_info["opponent"] = "PHI"
			self.testUtil.insert_into_team_game_totals(self.team_game_totals_info)

			self.team_game_totals_info["team"] = "BOS"
			self.team_game_totals_info["season"] = 2013
			self.team_game_totals_info["game"] = 2
			self.team_game_totals_info["date"] = date(2013,11,4)
			self.team_game_totals_info["opponent"] = "PHI"
			self.testUtil.insert_into_team_game_totals(self.team_game_totals_info)

			points_vs_position = self.dvpManager.calculate_defense_vs_position("points", p, "BOS", 2013, date=date(2013, 11, 2))
			offensive_rebs_vs_position = self.dvpManager.calculate_defense_vs_position("offensive_rebounds", p, "BOS",
																						2013, date=date(2013, 11, 2))
			defensive_rebs_vs_position = self.dvpManager.calculate_defense_vs_position("defensive_rebounds", p, "BOS",
																						2013, date=date(2013, 11, 2))
			assists_vs_position = self.dvpManager.calculate_defense_vs_position("assists", p, "BOS", 2013, date=date(2013, 11, 2))
			steals_vs_position = self.dvpManager.calculate_defense_vs_position("steals", p, "BOS", 2013, date=date(2013, 11, 2))
			blocks_vs_position = self.dvpManager.calculate_defense_vs_position("blocks", p, "BOS", 2013, date=date(2013, 11, 2))
			turnovers_vs_position = self.dvpManager.calculate_defense_vs_position("turnovers", p, "BOS", 2013, date=date(2013, 11, 2))

			self.assertTrue(points_vs_position.value == 20)
			self.assertTrue(offensive_rebs_vs_position.value == 5)
			self.assertTrue(defensive_rebs_vs_position.value == 10)
			self.assertTrue(assists_vs_position.value == 4)
			self.assertTrue(steals_vs_position.value == 3)
			self.assertTrue(blocks_vs_position.value == 2)
			self.assertTrue(turnovers_vs_position.value == 5)