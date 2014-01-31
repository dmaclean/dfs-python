import sys
sys.path.append('..')

from datetime import date,timedelta

import unittest
import BBRTestUtility
from projections import Projections
from models.injury_manager import InjuryManager, Injury
from fantasy_point_calculator import FantasyPointCalculator
from dfs_constants import DFSConstants

class TestProjections(unittest.TestCase):
	def setUp(self):
		self.testUtil = BBRTestUtility.BBRTestUtility()
		self.projections = Projections(self.testUtil.conn)
		self.injury_manager = InjuryManager(self.testUtil.conn)
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
		
		self.game_totals_advanced_info = {
			"player_id": "",
			"game_number": 0,
			"season": date.today().year,
			"date": date.today(),
			"age": 0,
			"team": "BOS",
			"home": True,
			"opponent": "NYK",
			"result": "",
			"games_started": 0,
			"minutes_played": 0,
			"true_shooting_pct": 0,
			"effective_field_goal_pct": 0,
			"offensive_rebound_pct": 0,
			"defensive_rebound_pct": 0,
			"total_rebound_pct": 0,
			"assist_pct": 0,
			"steal_pct": 0,
			"block_pct": 0,
			"turnover_pct": 0,
			"usage_pct": 0,
			"offensive_rating": 0,
			"defensive_rating": 0,
			"game_score": 0
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
		
		self.schedule_info = {
			"date": date.today(),
			"season": date.today().year,
			"visitor": "",
			"home": ""
		}
		
		self.salary_info = {
			"player_id": "",
			"site": "",
			"salary": 0,
			"date": date.today()
		}
		
		self.dfs_position_info = {
			"player_id": "",
			"site": "",
			"position": ""
		}
		
		self.vegas_info = {
			"date": date.today(),
			"road_team": "",
			"home_team": "",
			"spread_road": 0,
			"spread_home": 0,
			"over_under": 0,
			"projection_road": 0,
			"projection_home": 0
		}
		
		self.fantasy_points_info = self.testUtil.generate_default_fantasy_points_info()
	
	def tearDown(self):
		self.testUtil.conn.close()
		
		self.player_info = {}
	
	####################################################################################
	# Tests retrieval of player information from the players table, given a player_id.
	####################################################################################
	def test_get_player_info(self):
		self.player_info["id"] = "macleda01"
		self.player_info["name"] = "Dan"
		self.player_info["position"] = "G"
		self.player_info["height"] = 69
		self.player_info["weight"] = 175
		self.player_info["url"] = "something"
				
		self.testUtil.insert_into_players(self.player_info)
		info = self.projections.get_player_info("macleda01")
		
		self.assertTrue(len(info) > 0)
		self.assertTrue(info["id"] == self.player_info["id"])
	
	###############################################################################
	# Test the retrieval of the team that a player is on as of a particular date.
	###############################################################################
	def test_get_team(self):
		# Player is on Miami for game 1 of 2012
		self.game_totals_basic_info["player_id"] = "macleda01"
		self.game_totals_basic_info["season"] = 2012
		self.game_totals_basic_info["game_number"] = 1
		self.game_totals_basic_info["team"] = "MIA"
		self.game_totals_basic_info["date"] = date(2012,11,1)
		
		# Player is on Philly for game 1 of 2013
		self.game_totals_basic_info["player_id"] = "macleda01"
		self.game_totals_basic_info["season"] = 2013
		self.game_totals_basic_info["game_number"] = 1
		self.game_totals_basic_info["team"] = "PHI"
		self.game_totals_basic_info["date"] = date(2013,11,1)
		
		self.testUtil.insert_into_game_totals_basic(self.game_totals_basic_info)
		self.assertTrue(self.projections.get_team("macleda01", 2013, date(2013,11,1)) == "PHI")
		
		# Player is on Boston for game 2 of 2013
		self.game_totals_basic_info["game_number"] = 2
		self.game_totals_basic_info["team"] = "BOS"
		self.game_totals_basic_info["date"] = date(2013,11,2)
				
		self.testUtil.insert_into_game_totals_basic(self.game_totals_basic_info)
		
		self.assertTrue(self.projections.get_team("macleda01", 2013, date(2013,11,1)) == "PHI")
		self.assertTrue(self.projections.get_team("macleda01", 2013, date(2013,11,2)) == "BOS")

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

			points_vs_position = self.projections.calculate_defense_vs_position("points", p, "BOS", 2013, date(2013,11,2))
			offensive_rebs_vs_position = self.projections.calculate_defense_vs_position("offensive_rebounds", p, "BOS", 2013, date(2013,11,2))
			defensive_rebs_vs_position = self.projections.calculate_defense_vs_position("defensive_rebounds", p, "BOS", 2013, date(2013,11,2))
			assists_vs_position = self.projections.calculate_defense_vs_position("assists", p, "BOS", 2013, date(2013,11,2))
			steals_vs_position = self.projections.calculate_defense_vs_position("steals", p, "BOS", 2013, date(2013,11,2))
			blocks_vs_position = self.projections.calculate_defense_vs_position("blocks", p, "BOS", 2013, date(2013,11,2))
			turnovers_vs_position = self.projections.calculate_defense_vs_position("turnovers", p, "BOS", 2013, date(2013,11,2))

			self.assertTrue(points_vs_position == 15)
			self.assertTrue(offensive_rebs_vs_position == 6)
			self.assertTrue(defensive_rebs_vs_position == 11)
			self.assertTrue(assists_vs_position == 6)
			self.assertTrue(steals_vs_position == 2)
			self.assertTrue(blocks_vs_position == 1)
			self.assertTrue(turnovers_vs_position == 4)

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

			points_vs_position = self.projections.calculate_defense_vs_position("points", p, "BOS", 2013, date(2013,11,2))
			offensive_rebs_vs_position = self.projections.calculate_defense_vs_position("offensive_rebounds", p, "BOS", 2013, date(2013,11,2))
			defensive_rebs_vs_position = self.projections.calculate_defense_vs_position("defensive_rebounds", p, "BOS", 2013, date(2013,11,2))
			assists_vs_position = self.projections.calculate_defense_vs_position("assists", p, "BOS", 2013, date(2013,11,2))
			steals_vs_position = self.projections.calculate_defense_vs_position("steals", p, "BOS", 2013, date(2013,11,2))
			blocks_vs_position = self.projections.calculate_defense_vs_position("blocks", p, "BOS", 2013, date(2013,11,2))
			turnovers_vs_position = self.projections.calculate_defense_vs_position("turnovers", p, "BOS", 2013, date(2013,11,2))

			self.assertTrue(points_vs_position == 20)
			self.assertTrue(offensive_rebs_vs_position == 5)
			self.assertTrue(defensive_rebs_vs_position == 10)
			self.assertTrue(assists_vs_position == 4)
			self.assertTrue(steals_vs_position == 3)
			self.assertTrue(blocks_vs_position == 2)
			self.assertTrue(turnovers_vs_position == 5)

	def test_calculate_league_avg(self):
		positions = ["SG","SF","PF","C"]
		
		for p in positions:
			# Set up three players that played against a team on separate days
			self.player_info["id"] = p + "1"
			self.player_info["name"] = p + " 1"
			self.player_info["rg_position"] = p
			self.testUtil.insert_into_players(self.player_info)
		
			self.player_info["id"] = p + "2"
			self.player_info["name"] = p +" 2"
			self.testUtil.insert_into_players(self.player_info)
			
			self.player_info["id"] = p + "3"
			self.player_info["name"] = p +" 3"
			self.testUtil.insert_into_players(self.player_info)
			
			self.player_info["id"] = p + "4"
			self.player_info["name"] = p + " 4"
			if p == "SG":
				self.player_info["rg_position"] = "PG"
			elif p == "SF":
				self.player_info["rg_position"] = "SG"
			elif p == "PF":
				self.player_info["rg_position"] = "SF"
			elif p == "C":
				self.player_info["rg_position"] = "PF"
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
			self.game_totals_basic_info["team"] = "LAL"
			self.game_totals_basic_info["opponent"] = "ATL"
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
			self.game_totals_basic_info["team"] = "DET"
			self.game_totals_basic_info["opponent"] = "BOS"
			self.game_totals_basic_info["date"] = date(2013,11,5)
			self.game_totals_basic_info["points"] = 30
			self.game_totals_basic_info["offensive_rebounds"] = 7
			self.game_totals_basic_info["defensive_rebounds"] = 12
			self.game_totals_basic_info["assists"] = 8
			self.game_totals_basic_info["steals"] = 1
			self.game_totals_basic_info["blocks"] = 0
			self.game_totals_basic_info["turnovers"] = 3
			self.testUtil.insert_into_game_totals_basic(self.game_totals_basic_info)
			
			self.game_totals_basic_info["player_id"] = p+"4"
			self.game_totals_basic_info["season"] = 2013
			self.game_totals_basic_info["game_number"] = 3
			self.game_totals_basic_info["team"] = "DET"
			self.game_totals_basic_info["opponent"] = "BOS"
			self.game_totals_basic_info["date"] = date(2013,11,6)
			self.game_totals_basic_info["points"] = 30
			self.game_totals_basic_info["offensive_rebounds"] = 7
			self.game_totals_basic_info["defensive_rebounds"] = 12
			self.game_totals_basic_info["assists"] = 8
			self.game_totals_basic_info["steals"] = 1
			self.game_totals_basic_info["blocks"] = 0
			self.game_totals_basic_info["turnovers"] = 3
			self.testUtil.insert_into_game_totals_basic(self.game_totals_basic_info)
		
			# Team game totals for ATL and BOS
			self.team_game_totals_info["team"] = "BOS"
			self.team_game_totals_info["season"] = 2013
			self.team_game_totals_info["game"] = 1
			self.team_game_totals_info["date"] = date(2013,11,1)
			self.team_game_totals_info["opponent"] = "PHI"
			self.testUtil.insert_into_team_game_totals(self.team_game_totals_info)
			
			self.team_game_totals_info["team"] = "BOS"
			self.team_game_totals_info["season"] = 2013
			self.team_game_totals_info["game"] = 2
			self.team_game_totals_info["date"] = date(2013,11,5)
			self.team_game_totals_info["opponent"] = "DET"
			self.testUtil.insert_into_team_game_totals(self.team_game_totals_info)
			
			self.team_game_totals_info["team"] = "ATL"
			self.team_game_totals_info["season"] = 2013
			self.team_game_totals_info["game"] = 3
			self.team_game_totals_info["date"] = date(2013,11,4)
			self.team_game_totals_info["opponent"] = "LAL"
			self.testUtil.insert_into_team_game_totals(self.team_game_totals_info)
			
			# BOS had 50 pts scored against them over 2 games = 25/ppg
			# ATL had 10 pts scored against them over 3 games = 3.3/ppg
			#
			# 2 teams, yielding 25+3.3 ppg = 28.3/2 = ~14
			points = self.projections.calculate_league_avg("points", p, 2013)
			self.assertTrue(points == 14)
	
	def test_calculate_league_avg_with_date(self):
		positions = ["SG","SF","PF","C"]
		
		for p in positions:
			# Set up three players that played against a team on separate days
			self.player_info["id"] = p + "1"
			self.player_info["name"] = p + " 1"
			self.player_info["rg_position"] = p
			self.testUtil.insert_into_players(self.player_info)
		
			self.player_info["id"] = p + "2"
			self.player_info["name"] = p +" 2"
			self.testUtil.insert_into_players(self.player_info)
			
			self.player_info["id"] = p + "3"
			self.player_info["name"] = p +" 3"
			self.testUtil.insert_into_players(self.player_info)
			
			self.player_info["id"] = p + "4"
			self.player_info["name"] = p + " 4"
			if p == "SG":
				self.player_info["rg_position"] = "PG"
			elif p == "SF":
				self.player_info["rg_position"] = "SG"
			elif p == "PF":
				self.player_info["rg_position"] = "SF"
			elif p == "C":
				self.player_info["rg_position"] = "PF"
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
			self.game_totals_basic_info["team"] = "LAL"
			self.game_totals_basic_info["opponent"] = "ATL"
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
			self.game_totals_basic_info["team"] = "DET"
			self.game_totals_basic_info["opponent"] = "BOS"
			self.game_totals_basic_info["date"] = date(2013,11,5)
			self.game_totals_basic_info["points"] = 30
			self.game_totals_basic_info["offensive_rebounds"] = 7
			self.game_totals_basic_info["defensive_rebounds"] = 12
			self.game_totals_basic_info["assists"] = 8
			self.game_totals_basic_info["steals"] = 1
			self.game_totals_basic_info["blocks"] = 0
			self.game_totals_basic_info["turnovers"] = 3
			self.testUtil.insert_into_game_totals_basic(self.game_totals_basic_info)
			
			self.game_totals_basic_info["player_id"] = p+"4"
			self.game_totals_basic_info["season"] = 2013
			self.game_totals_basic_info["game_number"] = 3
			self.game_totals_basic_info["team"] = "DET"
			self.game_totals_basic_info["opponent"] = "BOS"
			self.game_totals_basic_info["date"] = date(2013,11,3)
			self.game_totals_basic_info["points"] = 30
			self.game_totals_basic_info["offensive_rebounds"] = 7
			self.game_totals_basic_info["defensive_rebounds"] = 12
			self.game_totals_basic_info["assists"] = 8
			self.game_totals_basic_info["steals"] = 1
			self.game_totals_basic_info["blocks"] = 0
			self.game_totals_basic_info["turnovers"] = 3
			self.testUtil.insert_into_game_totals_basic(self.game_totals_basic_info)
		
			# Team game totals for ATL and BOS
			self.team_game_totals_info["team"] = "BOS"
			self.team_game_totals_info["season"] = 2013
			self.team_game_totals_info["game"] = 1
			self.team_game_totals_info["date"] = date(2013,11,1)
			self.team_game_totals_info["opponent"] = "PHI"
			self.testUtil.insert_into_team_game_totals(self.team_game_totals_info)
			
			self.team_game_totals_info["team"] = "BOS"
			self.team_game_totals_info["season"] = 2013
			self.team_game_totals_info["game"] = 2
			self.team_game_totals_info["date"] = date(2013,11,5)
			self.team_game_totals_info["opponent"] = "DET"
			self.testUtil.insert_into_team_game_totals(self.team_game_totals_info)
			
			self.team_game_totals_info["team"] = "ATL"
			self.team_game_totals_info["season"] = 2013
			self.team_game_totals_info["game"] = 3
			self.team_game_totals_info["date"] = date(2013,11,4)
			self.team_game_totals_info["opponent"] = "LAL"
			self.testUtil.insert_into_team_game_totals(self.team_game_totals_info)
			
			# BOS had 20 pts scored against them over 1 game on or before 11/4 = 20/ppg
			# ATL had 10 pts scored against them over 3 games on or before 11/4 = 3.3/ppg
			#
			# 2 teams, yielding 25+3.3 ppg = 23.3/2 = ~11
			points = self.projections.calculate_league_avg("points", p, 2013, date(2013,11,4))
			self.assertTrue(points == 11)
		
	def test_get_baseline(self):
		# Write basic game totals for player
		self.game_totals_basic_info["player_id"] = "macleda01"
		self.game_totals_basic_info["season"] = 2013
		self.game_totals_basic_info["game_number"] = 1
		self.game_totals_basic_info["team"] = "LAL"
		self.game_totals_basic_info["opponent"] = "ATL"
		self.game_totals_basic_info["date"] = date(2013,11,4)
		self.game_totals_basic_info["points"] = 10
		self.game_totals_basic_info["minutes_played"] = 30
		self.testUtil.insert_into_game_totals_basic(self.game_totals_basic_info)
		
		self.game_totals_basic_info["game_number"] = 2
		self.game_totals_basic_info["date"] = date(2013,11,5)
		self.game_totals_basic_info["points"] = 20
		self.game_totals_basic_info["minutes_played"] = 32
		self.testUtil.insert_into_game_totals_basic(self.game_totals_basic_info)
		
		# Write advanced game totals for player
		self.game_totals_advanced_info["player_id"] = "macleda01"
		self.game_totals_advanced_info["date"] = date(2013,11,4)
		self.game_totals_advanced_info["season"] = 2013
		self.game_totals_advanced_info["usage_pct"] = 10.6
		self.game_totals_advanced_info["offensive_rating"] = 100
		self.game_totals_advanced_info["defensive_rating"] = 101
		self.testUtil.insert_into_game_totals_advanced(self.game_totals_advanced_info)
		
		self.game_totals_advanced_info["date"] = date(2013,11,5)
		self.game_totals_advanced_info["season"] = 2013
		self.game_totals_advanced_info["usage_pct"] = 12.6
		self.game_totals_advanced_info["offensive_rating"] = 104
		self.game_totals_advanced_info["defensive_rating"] = 103
		self.testUtil.insert_into_game_totals_advanced(self.game_totals_advanced_info)
		
		baseline = self.projections.get_baseline("macleda01", 2013)
		self.assertTrue(baseline[0] == 15)	        # avg points
		self.assertTrue(baseline[12] == 31)         # minutes played
		self.assertTrue(baseline[13] == 11.6)	    # usage
		self.assertTrue(baseline[14] == 102)	    # off rating
		self.assertTrue(baseline[15] == 102)	    # def rating

	def test_get_baseline_fantasy_points(self):
		# Write basic game totals for player
		self.game_totals_basic_info["player_id"] = "macleda01"
		self.game_totals_basic_info["season"] = 2013
		self.game_totals_basic_info["game_number"] = 1
		self.game_totals_basic_info["team"] = "LAL"
		self.game_totals_basic_info["opponent"] = "ATL"
		self.game_totals_basic_info["date"] = date(2013,11,4)
		self.game_totals_basic_info["points"] = 10
		self.game_totals_basic_info["minutes_played"] = 30
		self.testUtil.insert_into_game_totals_basic(self.game_totals_basic_info)

		self.game_totals_basic_info["game_number"] = 2
		self.game_totals_basic_info["date"] = date(2013,11,5)
		self.game_totals_basic_info["points"] = 20
		self.game_totals_basic_info["minutes_played"] = 32
		self.testUtil.insert_into_game_totals_basic(self.game_totals_basic_info)

		# Write advanced game totals for player
		self.game_totals_advanced_info["player_id"] = "macleda01"
		self.game_totals_advanced_info["date"] = date(2013,11,4)
		self.game_totals_advanced_info["season"] = 2013
		self.game_totals_advanced_info["usage_pct"] = 10.6
		self.game_totals_advanced_info["offensive_rating"] = 100
		self.game_totals_advanced_info["defensive_rating"] = 101
		self.testUtil.insert_into_game_totals_advanced(self.game_totals_advanced_info)

		self.game_totals_advanced_info["date"] = date(2013,11,5)
		self.game_totals_advanced_info["season"] = 2013
		self.game_totals_advanced_info["usage_pct"] = 12.6
		self.game_totals_advanced_info["offensive_rating"] = 104
		self.game_totals_advanced_info["defensive_rating"] = 103
		self.testUtil.insert_into_game_totals_advanced(self.game_totals_advanced_info)

		self.fantasy_points_info["points"] = 10
		self.fantasy_points_info["game_number"] = 1
		self.fantasy_points_info["player_id"] = "macleda01"
		self.fantasy_points_info["season"] = 2013
		self.fantasy_points_info["site"] = DFSConstants.FAN_DUEL
		self.testUtil.insert_into_fantasy_points(self.fantasy_points_info)

		self.fantasy_points_info["points"] = 20
		self.fantasy_points_info["game_number"] = 2
		self.testUtil.insert_into_fantasy_points(self.fantasy_points_info)

		self.projections.site = DFSConstants.FAN_DUEL
		baseline = self.projections.get_baseline("macleda01", 2013)
		self.assertTrue(baseline[0] == 15)          # avg points
		self.assertTrue(baseline[12] == 31)         # minutes played
		self.assertTrue(baseline[13] == 11.6)	    # usage
		self.assertTrue(baseline[14] == 102)	    # off rating
		self.assertTrue(baseline[15] == 102)	    # def rating
		self.assertTrue(baseline[16] == 15)         # Fantasy points
	
	def test_get_baseline_with_date(self):
		# Write basic game totals for player
		self.game_totals_basic_info["player_id"] = "macleda01"
		self.game_totals_basic_info["season"] = 2013
		self.game_totals_basic_info["game_number"] = 1
		self.game_totals_basic_info["team"] = "LAL"
		self.game_totals_basic_info["opponent"] = "ATL"
		self.game_totals_basic_info["date"] = date(2013,11,4)
		self.game_totals_basic_info["points"] = 10
		self.testUtil.insert_into_game_totals_basic(self.game_totals_basic_info)
		
		self.game_totals_basic_info["game_number"] = 2
		self.game_totals_basic_info["date"] = date(2013,11,5)
		self.game_totals_basic_info["points"] = 20
		self.testUtil.insert_into_game_totals_basic(self.game_totals_basic_info)
		
		# Write advanced game totals for player
		self.game_totals_advanced_info["player_id"] = "macleda01"
		self.game_totals_advanced_info["date"] = date(2013,11,4)
		self.game_totals_advanced_info["season"] = 2013
		self.game_totals_advanced_info["usage_pct"] = 10.6
		self.game_totals_advanced_info["offensive_rating"] = 100
		self.game_totals_advanced_info["defensive_rating"] = 101
		self.testUtil.insert_into_game_totals_advanced(self.game_totals_advanced_info)
		
		self.game_totals_advanced_info["date"] = date(2013,11,5)
		self.game_totals_advanced_info["usage_pct"] = 12.6
		self.game_totals_advanced_info["offensive_rating"] = 104
		self.game_totals_advanced_info["defensive_rating"] = 103
		self.testUtil.insert_into_game_totals_advanced(self.game_totals_advanced_info)
		
		baseline = self.projections.get_baseline("macleda01", 2013, date(2013,11,4))
		self.assertTrue(baseline[0] == 10)	        # avg points
		self.assertTrue(baseline[13] == 10.6)	    # usage
		self.assertTrue(baseline[14] == 100)	    # off rating
		self.assertTrue(baseline[15] == 101)	    # def rating
	
	def test_get_baseline_total_rebounds(self):
		# Write basic game totals for player
		self.game_totals_basic_info["player_id"] = "macleda01"
		self.game_totals_basic_info["season"] = 2013
		self.game_totals_basic_info["game_number"] = 1
		self.game_totals_basic_info["team"] = "LAL"
		self.game_totals_basic_info["opponent"] = "ATL"
		self.game_totals_basic_info["date"] = date(2013,11,4)
		self.game_totals_basic_info["total_rebounds"] = 10
		self.testUtil.insert_into_game_totals_basic(self.game_totals_basic_info)
		
		self.game_totals_basic_info["game_number"] = 2
		self.game_totals_basic_info["date"] = date(2013,11,5)
		self.game_totals_basic_info["total_rebounds"] = 20
		self.testUtil.insert_into_game_totals_basic(self.game_totals_basic_info)
		
		# Write advanced game totals for player
		self.game_totals_advanced_info["player_id"] = "macleda01"
		self.game_totals_advanced_info["date"] = date(2013,11,4)
		self.game_totals_advanced_info["season"] = 2013
		self.game_totals_advanced_info["usage_pct"] = 10.6
		self.game_totals_advanced_info["offensive_rating"] = 100
		self.game_totals_advanced_info["defensive_rating"] = 101
		self.testUtil.insert_into_game_totals_advanced(self.game_totals_advanced_info)
		
		self.game_totals_advanced_info["date"] = date(2013,11,5)
		self.game_totals_advanced_info["usage_pct"] = 12.6
		self.game_totals_advanced_info["offensive_rating"] = 104
		self.game_totals_advanced_info["defensive_rating"] = 103
		self.testUtil.insert_into_game_totals_advanced(self.game_totals_advanced_info)
		
		baseline = self.projections.get_baseline("macleda01", 2013)
		self.assertTrue(baseline[7] == 15)	        # avg total rebounds
		self.assertTrue(baseline[13] == 11.6)	    # usage
		self.assertTrue(baseline[14] == 102)	    # off rating
		self.assertTrue(baseline[15] == 102)	    # def rating
	
	def test_get_baseline_total_rebounds_with_date(self):
		# Write basic game totals for player
		self.game_totals_basic_info["player_id"] = "macleda01"
		self.game_totals_basic_info["season"] = 2013
		self.game_totals_basic_info["game_number"] = 1
		self.game_totals_basic_info["team"] = "LAL"
		self.game_totals_basic_info["opponent"] = "ATL"
		self.game_totals_basic_info["date"] = date(2013,11,4)
		self.game_totals_basic_info["total_rebounds"] = 10
		self.testUtil.insert_into_game_totals_basic(self.game_totals_basic_info)
		
		self.game_totals_basic_info["game_number"] = 2
		self.game_totals_basic_info["date"] = date(2013,11,5)
		self.game_totals_basic_info["total_rebounds"] = 20
		self.testUtil.insert_into_game_totals_basic(self.game_totals_basic_info)
		
		# Write advanced game totals for player
		self.game_totals_advanced_info["player_id"] = "macleda01"
		self.game_totals_advanced_info["date"] = date(2013,11,4)
		self.game_totals_advanced_info["season"] = 2013
		self.game_totals_advanced_info["usage_pct"] = 10.6
		self.game_totals_advanced_info["offensive_rating"] = 100
		self.game_totals_advanced_info["defensive_rating"] = 101
		self.testUtil.insert_into_game_totals_advanced(self.game_totals_advanced_info)
		
		self.game_totals_advanced_info["date"] = date(2013,11,5)
		self.game_totals_advanced_info["usage_pct"] = 12.6
		self.game_totals_advanced_info["offensive_rating"] = 104
		self.game_totals_advanced_info["defensive_rating"] = 103
		self.testUtil.insert_into_game_totals_advanced(self.game_totals_advanced_info)
		
		baseline = self.projections.get_baseline("macleda01", 2013, date(2013,11,4))
		self.assertTrue(baseline[7] == 10)	        # avg total_rebounds
		self.assertTrue(baseline[13] == 10.6)	    # usage
		self.assertTrue(baseline[14] == 100)	    # off rating
		self.assertTrue(baseline[15] == 101)	    # def rating
	
	def test_normalize_player_avg_stat(self):
		p = "G"
	
		# Create four players
		self.player_info["id"] = p + "1"
		self.player_info["name"] = p + " 1"
		self.player_info["position"] = p
		self.testUtil.insert_into_players(self.player_info)
	
		self.player_info["id"] = p + "2"
		self.player_info["name"] = p +" 2"
		self.testUtil.insert_into_players(self.player_info)
		
		self.player_info["id"] = p + "3"
		self.player_info["name"] = p +" 3"
		self.testUtil.insert_into_players(self.player_info)
		
		self.player_info["id"] = p + "4"
		self.player_info["name"] = p +" 4"
		self.testUtil.insert_into_players(self.player_info)
		
		self.game_totals_basic_info["player_id"] = p+"1"
		self.game_totals_basic_info["season"] = 2013
		self.game_totals_basic_info["game_number"] = 1
		self.game_totals_basic_info["team"] = "LAL"
		self.game_totals_basic_info["opponent"] = "ATL"
		self.game_totals_basic_info["date"] = date(2013,11,1)
		self.game_totals_basic_info["points"] = 10
		self.testUtil.insert_into_game_totals_basic(self.game_totals_basic_info)
		
		self.game_totals_basic_info["player_id"] = p+"1"
		self.game_totals_basic_info["game_number"] = 2
		self.game_totals_basic_info["date"] = date(2013,11,2)
		self.game_totals_basic_info["points"] = 12
		self.testUtil.insert_into_game_totals_basic(self.game_totals_basic_info)
		
		self.game_totals_basic_info["player_id"] = p+"2"
		self.game_totals_basic_info["game_number"] = 1
		self.game_totals_basic_info["date"] = date(2013,11,1)
		self.game_totals_basic_info["points"] = 20
		self.testUtil.insert_into_game_totals_basic(self.game_totals_basic_info)
		
		self.game_totals_basic_info["player_id"] = p+"2"
		self.game_totals_basic_info["game_number"] = 2
		self.game_totals_basic_info["date"] = date(2013,11,2)
		self.game_totals_basic_info["points"] = 22
		self.testUtil.insert_into_game_totals_basic(self.game_totals_basic_info)
		
		self.game_totals_basic_info["player_id"] = p+"3"
		self.game_totals_basic_info["game_number"] = 1
		self.game_totals_basic_info["date"] = date(2013,11,1)
		self.game_totals_basic_info["points"] = 30
		self.testUtil.insert_into_game_totals_basic(self.game_totals_basic_info)
		
		self.game_totals_basic_info["player_id"] = p+"3"
		self.game_totals_basic_info["game_number"] = 2
		self.game_totals_basic_info["date"] = date(2013,11,2)
		self.game_totals_basic_info["points"] = 32
		self.testUtil.insert_into_game_totals_basic(self.game_totals_basic_info)
		
		self.game_totals_basic_info["player_id"] = p+"4"
		self.game_totals_basic_info["game_number"] = 1
		self.game_totals_basic_info["date"] = date(2013,11,1)
		self.game_totals_basic_info["points"] = 0
		self.testUtil.insert_into_game_totals_basic(self.game_totals_basic_info)
		
		self.game_totals_basic_info["player_id"] = p+"4"
		self.game_totals_basic_info["game_number"] = 2
		self.game_totals_basic_info["date"] = date(2013,11,2)
		self.game_totals_basic_info["points"] = 2
		self.testUtil.insert_into_game_totals_basic(self.game_totals_basic_info)
		
		# p1 = 10+12 = 22
		# p2 = 20+22 = 42
		# p3 = 30+32 = 62
		# p4 = 0+2   = 2
		# avg = p1+p2+p3+p4/8 = 16
		#
		# p1 game 1 normalized = (10/16)*10 = 6.25
		# p1 game 2 normalized = (12/16)*12 = 9
		# p2 game 1 normalized = (20/16)*20 = 25
		# p2 game 2 normalized = (22/16)*22 = 30.25
		# p3 game 1 normalized = (30/16)*30 = 56.25
		# p3 game 2 normalized = (32/16)*32 = 64
		# p4 game 1 normalized = (0/16)*0 = 0.0
		# p4 game 2 normalized = (2/16)*2 = 0.125
		self.assertTrue(self.projections.normalize_player_avg_stat(p+"1", "points", 2013) == 7.625)
		self.assertTrue(self.projections.normalize_player_avg_stat(p+"2", "points", 2013) == 27.625)
		self.assertTrue(self.projections.normalize_player_avg_stat(p+"3", "points", 2013) == 60.125)
		self.assertTrue(self.projections.normalize_player_avg_stat(p+"4", "points", 2013) == 0.125)
	
	def test_get_game_list_today(self):
		self.schedule_info["home"] = "BOS"
		self.schedule_info["visitor"] = "NYK"
		self.testUtil.insert_into_schedules(self.schedule_info)
		
		self.schedule_info["date"] = date(2012,11,1)
		self.schedule_info["season"] = 2012
		self.schedule_info["home"] = "PHI"
		self.schedule_info["visitor"] = "BKN"
		self.testUtil.insert_into_schedules(self.schedule_info)
		
		result = self.projections.get_game_list()
		self.assertTrue(len(result) == 1)
#		self.assertTrue(result[0]["date"] == date.today())
		#self.assertTrue(result[0]["id"] == 1)
		self.assertTrue(result[0]["season"] == date.today().year)
		self.assertTrue(result[0]["visitor"] == "NYK")
		self.assertTrue(result[0]["home"] == "BOS")
	
	def test_get_game_list_2012_11_1(self):
		self.schedule_info["home"] = "BOS"
		self.schedule_info["visitor"] = "NYK"
		self.testUtil.insert_into_schedules(self.schedule_info)
		
		self.schedule_info["date"] = date(2012,11,1)
		self.schedule_info["season"] = 2012
		self.schedule_info["home"] = "PHI"
		self.schedule_info["visitor"] = "BKN"
		self.testUtil.insert_into_schedules(self.schedule_info)
		
		result = self.projections.get_game_list(date(2012,11,1))
		self.assertTrue(len(result) == 1)
#		self.assertTrue(result[0]["date"] == date(2012,11,1))
		#self.assertTrue(result[0]["id"] == 2)
		self.assertTrue(result[0]["season"] == 2012)
		self.assertTrue(result[0]["visitor"] == "BKN")
		self.assertTrue(result[0]["home"] == "PHI")
	
	def test_get_players_in_game(self):
		self.player_info["id"] = "player1"
		self.player_info["name"] =  "Player 1"
		self.player_info["position"] = "G"
		self.player_info["rg_position"] = "PG"
		self.player_info["height"] = 80
		self.player_info["weight"] = 200
		self.player_info["url"] = "something"
		self.testUtil.insert_into_players(self.player_info)
		
		self.player_info["id"] = "player2"
		self.player_info["name"] =  "Player 2"
		self.player_info["position"] = "C"
		self.player_info["rg_position"] = "C"
		self.player_info["height"] = 88
		self.player_info["weight"] = 250
		self.testUtil.insert_into_players(self.player_info)

		self.player_info["id"] = "player3"
		self.player_info["name"] =  "Player 3"
		self.player_info["position"] = "C"
		self.player_info["height"] = 88
		self.player_info["weight"] = 250
		self.testUtil.insert_into_players(self.player_info)
	
		# Set up players
		self.game_totals_basic_info["player_id"] = "player1"
		self.game_totals_basic_info["season"] = 2013
		self.game_totals_basic_info["team"] = "BKN"
		self.game_totals_basic_info["opponent"] = "BOS"
		self.game_totals_basic_info["date"] = date(2013,12,1)
		self.testUtil.insert_into_game_totals_basic(self.game_totals_basic_info)
		
		self.game_totals_basic_info["player_id"] = "player2"
		self.game_totals_basic_info["season"] = 2013
		self.game_totals_basic_info["game_number"] = 1
		self.game_totals_basic_info["team"] = "PHI"
		self.game_totals_basic_info["opponent"] = "NYK"
		self.game_totals_basic_info["date"] = date(2013,11,30)
		self.testUtil.insert_into_game_totals_basic(self.game_totals_basic_info)

		# Player 3 has a game with PHI but was traded to WAS
		self.game_totals_basic_info["player_id"] = "player3"
		self.game_totals_basic_info["season"] = 2013
		self.game_totals_basic_info["game_number"] = 1
		self.game_totals_basic_info["team"] = "PHI"
		self.game_totals_basic_info["opponent"] = "NYK"
		self.game_totals_basic_info["date"] = date(2013,12,1)
		self.testUtil.insert_into_game_totals_basic(self.game_totals_basic_info)

		self.game_totals_basic_info["player_id"] = "player3"
		self.game_totals_basic_info["season"] = 2013
		self.game_totals_basic_info["game_number"] = 1
		self.game_totals_basic_info["team"] = "WAS"
		self.game_totals_basic_info["opponent"] = "NYK"
		self.game_totals_basic_info["date"] = date(2013,12,2)
		self.testUtil.insert_into_game_totals_basic(self.game_totals_basic_info)
		
		# Set up game on schedule
		self.schedule_info["date"] = date(2013,12,3)
		self.schedule_info["season"] = 2013
		self.schedule_info["home"] = "PHI"
		self.schedule_info["visitor"] = "BKN"
		self.testUtil.insert_into_schedules(self.schedule_info)
		
		game = self.projections.get_game_list(self.schedule_info["date"])[0]
		players = self.projections.get_players_in_game(game)

		self.assertTrue(len(players) == 2)
		self.assertTrue(players[0]["player_id"] == "player2")
		self.assertTrue(players[0]["player_info"]["id"] == "player2")
		self.assertTrue(players[0]["player_info"]["name"] == "Player 2")
		self.assertTrue(players[0]["player_info"]["position"] == "C")
		self.assertTrue(players[0]["player_info"]["height"] == 88)
		self.assertTrue(players[0]["player_info"]["weight"] == 250)
		self.assertTrue(players[0]["player_info"]["url"] == "something")

		self.assertTrue(players[1]["player_id"] == "player1")
		self.assertTrue(players[1]["player_info"]["id"] == "player1")
		self.assertTrue(players[1]["player_info"]["name"] == "Player 1")
		self.assertTrue(players[1]["player_info"]["position"] == "G")
		self.assertTrue(players[1]["player_info"]["height"] == 80)
		self.assertTrue(players[1]["player_info"]["weight"] == 200)
		self.assertTrue(players[1]["player_info"]["url"] == "something")
	
	def test_get_salary(self):
		self.salary_info["player_id"] = "macleda01"
		self.salary_info["site"] = "DRAFT_KINGS"
		self.salary_info["salary"] = 9500
		self.testUtil.insert_into_salaries(self.salary_info)
		
		self.salary_info["player_id"] = "macleda01"
		self.salary_info["site"] = "DRAFT_DAY"
		self.salary_info["salary"] = 8000
		self.testUtil.insert_into_salaries(self.salary_info)
		
		self.assertTrue(self.projections.get_salary("macleda01", "DRAFT_KINGS") == 9500)
		self.assertTrue(self.projections.get_salary("macleda01", "DRAFT_DAY") == 8000)
	
	def test_get_salary_with_date(self):
		self.salary_info["player_id"] = "macleda01"
		self.salary_info["site"] = "DRAFT_KINGS"
		self.salary_info["salary"] = 9500
		self.testUtil.insert_into_salaries(self.salary_info)
		
		self.salary_info["player_id"] = "macleda01"
		self.salary_info["site"] = "DRAFT_KINGS"
		self.salary_info["salary"] = 8000
		self.salary_info["date"] = date(2013,12,1)
		self.testUtil.insert_into_salaries(self.salary_info)
		
		self.assertTrue(self.projections.get_salary("macleda01", "DRAFT_KINGS", date(2013,12,1)) == 8000)
		
	def test_get_position_on_site(self):
		self.dfs_position_info["player_id"] = "macleda01"
		self.dfs_position_info["site"] = "DRAFT_KINGS"
		self.dfs_position_info["position"] = "PG"
		self.testUtil.insert_into_dfs_site_positions(self.dfs_position_info)
		
		self.assertTrue(self.projections.get_position_on_site("macleda01", "DRAFT_KINGS") == "PG")
	
	###############################################################################
	# Tests a player that has played two games, both of which produced floor FPs.
	###############################################################################
	def test_calculate_floor_consistency_ceiling_all_floor(self):
		self.game_totals_basic_info["player_id"] = "test"
		self.game_totals_basic_info["season"] = 2013
		self.game_totals_basic_info["game_number"] = 1
		self.game_totals_basic_info["field_goals"] = 2
		self.game_totals_basic_info["field_goal_attempts"] = 3
		self.game_totals_basic_info["three_point_field_goals"] = 0
		self.game_totals_basic_info["three_point_field_goal_attempts"] = 2
		self.game_totals_basic_info["free_throws"] = 1
		self.game_totals_basic_info["free_throw_attempts"] = 2
		self.game_totals_basic_info["total_rebounds"] = 0
		self.game_totals_basic_info["assists"] = 0
		self.game_totals_basic_info["steals"] = 0
		self.game_totals_basic_info["blocks"] = 0
		self.game_totals_basic_info["turnovers"] = 1
		self.game_totals_basic_info["points"] = 5
		self.testUtil.insert_into_game_totals_basic(self.game_totals_basic_info)
		
		self.game_totals_basic_info["game_number"] = 2
		self.game_totals_basic_info["field_goals"] = 3
		self.game_totals_basic_info["field_goal_attempts"] = 3
		self.game_totals_basic_info["three_point_field_goals"] = 0
		self.game_totals_basic_info["three_point_field_goal_attempts"] = 2
		self.game_totals_basic_info["free_throws"] = 1
		self.game_totals_basic_info["free_throw_attempts"] = 2
		self.game_totals_basic_info["total_rebounds"] = 0
		self.game_totals_basic_info["assists"] = 0
		self.game_totals_basic_info["steals"] = 0
		self.game_totals_basic_info["blocks"] = 0
		self.game_totals_basic_info["turnovers"] = 1
		self.game_totals_basic_info["points"] = 7
		self.testUtil.insert_into_game_totals_basic(self.game_totals_basic_info)
		
		values = self.projections.calculate_floor_consistency_ceiling_pct("test", 2013, FantasyPointCalculator.STAR_STREET)
		
		self.assertTrue(values[0] == 1)
		self.assertTrue(values[1] == 0)
		self.assertTrue(values[2] == 0)
		self.assertTrue(values[3] == 0)
	
	####################################################################################
	# Tests a player that has played two games, both of which produced consistent FPs.
	####################################################################################
	def test_calculate_floor_consistency_ceiling_all_consistent(self):
		self.game_totals_basic_info["player_id"] = "test"
		self.game_totals_basic_info["season"] = 2013
		self.game_totals_basic_info["game_number"] = 1
		self.game_totals_basic_info["field_goals"] = 2
		self.game_totals_basic_info["field_goal_attempts"] = 3
		self.game_totals_basic_info["three_point_field_goals"] = 0
		self.game_totals_basic_info["three_point_field_goal_attempts"] = 2
		self.game_totals_basic_info["free_throws"] = 1
		self.game_totals_basic_info["free_throw_attempts"] = 2
		self.game_totals_basic_info["total_rebounds"] = 0
		self.game_totals_basic_info["assists"] = 0
		self.game_totals_basic_info["steals"] = 0
		self.game_totals_basic_info["blocks"] = 0
		self.game_totals_basic_info["turnovers"] = 1
		self.game_totals_basic_info["points"] = 25
		self.testUtil.insert_into_game_totals_basic(self.game_totals_basic_info)
		
		self.game_totals_basic_info["game_number"] = 2
		self.game_totals_basic_info["field_goals"] = 3
		self.game_totals_basic_info["field_goal_attempts"] = 3
		self.game_totals_basic_info["three_point_field_goals"] = 0
		self.game_totals_basic_info["three_point_field_goal_attempts"] = 2
		self.game_totals_basic_info["free_throws"] = 1
		self.game_totals_basic_info["free_throw_attempts"] = 2
		self.game_totals_basic_info["total_rebounds"] = 0
		self.game_totals_basic_info["assists"] = 0
		self.game_totals_basic_info["steals"] = 0
		self.game_totals_basic_info["blocks"] = 0
		self.game_totals_basic_info["turnovers"] = 1
		self.game_totals_basic_info["points"] = 30
		self.testUtil.insert_into_game_totals_basic(self.game_totals_basic_info)
		
		values = self.projections.calculate_floor_consistency_ceiling_pct("test", 2013, FantasyPointCalculator.STAR_STREET)
		
		self.assertTrue(values[0] == 0)
		self.assertTrue(values[1] == 1)
		self.assertTrue(values[2] == 0)
		self.assertTrue(values[3] == 0)
	
	###############################################################################
	# Tests a player that has played two games, both of which produced ceiling FPs.
	###############################################################################
	def test_calculate_floor_consistency_ceiling_all_ceiling(self):
		self.game_totals_basic_info["player_id"] = "test"
		self.game_totals_basic_info["season"] = 2013
		self.game_totals_basic_info["game_number"] = 1
		self.game_totals_basic_info["field_goals"] = 2
		self.game_totals_basic_info["field_goal_attempts"] = 3
		self.game_totals_basic_info["three_point_field_goals"] = 0
		self.game_totals_basic_info["three_point_field_goal_attempts"] = 2
		self.game_totals_basic_info["free_throws"] = 1
		self.game_totals_basic_info["free_throw_attempts"] = 2
		self.game_totals_basic_info["total_rebounds"] = 0
		self.game_totals_basic_info["assists"] = 0
		self.game_totals_basic_info["steals"] = 0
		self.game_totals_basic_info["blocks"] = 0
		self.game_totals_basic_info["turnovers"] = 1
		self.game_totals_basic_info["points"] = 47
		self.testUtil.insert_into_game_totals_basic(self.game_totals_basic_info)
		
		self.game_totals_basic_info["game_number"] = 2
		self.game_totals_basic_info["field_goals"] = 3
		self.game_totals_basic_info["field_goal_attempts"] = 3
		self.game_totals_basic_info["three_point_field_goals"] = 0
		self.game_totals_basic_info["three_point_field_goal_attempts"] = 2
		self.game_totals_basic_info["free_throws"] = 1
		self.game_totals_basic_info["free_throw_attempts"] = 2
		self.game_totals_basic_info["total_rebounds"] = 0
		self.game_totals_basic_info["assists"] = 0
		self.game_totals_basic_info["steals"] = 0
		self.game_totals_basic_info["blocks"] = 0
		self.game_totals_basic_info["turnovers"] = 1
		self.game_totals_basic_info["points"] = 45
		self.testUtil.insert_into_game_totals_basic(self.game_totals_basic_info)
		
		values = self.projections.calculate_floor_consistency_ceiling_pct("test", 2013, FantasyPointCalculator.STAR_STREET)
		
		self.assertTrue(values[0] == 0)
		self.assertTrue(values[1] == 1)
		self.assertTrue(values[2] == 1)
		self.assertTrue(values[3] == 0)
	
	###############################################################################
	# Tests a player that has played two games, both of which produced ceiling FPs.
	###############################################################################
	def test_calculate_floor_consistency_ceiling_all_super_ceiling(self):
		self.game_totals_basic_info["player_id"] = "test"
		self.game_totals_basic_info["season"] = 2013
		self.game_totals_basic_info["game_number"] = 1
		self.game_totals_basic_info["field_goals"] = 2
		self.game_totals_basic_info["field_goal_attempts"] = 3
		self.game_totals_basic_info["three_point_field_goals"] = 0
		self.game_totals_basic_info["three_point_field_goal_attempts"] = 2
		self.game_totals_basic_info["free_throws"] = 1
		self.game_totals_basic_info["free_throw_attempts"] = 2
		self.game_totals_basic_info["total_rebounds"] = 0
		self.game_totals_basic_info["assists"] = 0
		self.game_totals_basic_info["steals"] = 0
		self.game_totals_basic_info["blocks"] = 0
		self.game_totals_basic_info["turnovers"] = 1
		self.game_totals_basic_info["points"] = 52
		self.testUtil.insert_into_game_totals_basic(self.game_totals_basic_info)
		
		self.game_totals_basic_info["game_number"] = 2
		self.game_totals_basic_info["field_goals"] = 3
		self.game_totals_basic_info["field_goal_attempts"] = 3
		self.game_totals_basic_info["three_point_field_goals"] = 0
		self.game_totals_basic_info["three_point_field_goal_attempts"] = 2
		self.game_totals_basic_info["free_throws"] = 1
		self.game_totals_basic_info["free_throw_attempts"] = 2
		self.game_totals_basic_info["total_rebounds"] = 0
		self.game_totals_basic_info["assists"] = 0
		self.game_totals_basic_info["steals"] = 0
		self.game_totals_basic_info["blocks"] = 0
		self.game_totals_basic_info["turnovers"] = 1
		self.game_totals_basic_info["points"] = 55
		self.testUtil.insert_into_game_totals_basic(self.game_totals_basic_info)
		
		values = self.projections.calculate_floor_consistency_ceiling_pct("test", 2013, FantasyPointCalculator.STAR_STREET)
		
		self.assertTrue(values[0] == 0)
		self.assertTrue(values[1] == 1)
		self.assertTrue(values[2] == 1)
		self.assertTrue(values[3] == 1)
	
	###############################################################################
	# Tests a player that has played four games - 1 floor, 1 consistent, 1 ceiling
	# and 1 super-ceiling
	###############################################################################
	def test_calculate_floor_consistency_ceiling_one_each(self):
		self.game_totals_basic_info["player_id"] = "test"
		self.game_totals_basic_info["season"] = 2013
		self.game_totals_basic_info["game_number"] = 1
		self.game_totals_basic_info["field_goals"] = 2
		self.game_totals_basic_info["field_goal_attempts"] = 3
		self.game_totals_basic_info["three_point_field_goals"] = 0
		self.game_totals_basic_info["three_point_field_goal_attempts"] = 2
		self.game_totals_basic_info["free_throws"] = 1
		self.game_totals_basic_info["free_throw_attempts"] = 2
		self.game_totals_basic_info["total_rebounds"] = 0
		self.game_totals_basic_info["assists"] = 0
		self.game_totals_basic_info["steals"] = 0
		self.game_totals_basic_info["blocks"] = 0
		self.game_totals_basic_info["turnovers"] = 1
		self.game_totals_basic_info["points"] = 10
		self.testUtil.insert_into_game_totals_basic(self.game_totals_basic_info)
		
		self.game_totals_basic_info["game_number"] = 2
		self.game_totals_basic_info["field_goals"] = 3
		self.game_totals_basic_info["field_goal_attempts"] = 3
		self.game_totals_basic_info["three_point_field_goals"] = 0
		self.game_totals_basic_info["three_point_field_goal_attempts"] = 2
		self.game_totals_basic_info["free_throws"] = 1
		self.game_totals_basic_info["free_throw_attempts"] = 2
		self.game_totals_basic_info["total_rebounds"] = 0
		self.game_totals_basic_info["assists"] = 0
		self.game_totals_basic_info["steals"] = 0
		self.game_totals_basic_info["blocks"] = 0
		self.game_totals_basic_info["turnovers"] = 1
		self.game_totals_basic_info["points"] = 25
		self.testUtil.insert_into_game_totals_basic(self.game_totals_basic_info)
		
		self.game_totals_basic_info["game_number"] = 3
		self.game_totals_basic_info["field_goals"] = 3
		self.game_totals_basic_info["field_goal_attempts"] = 3
		self.game_totals_basic_info["three_point_field_goals"] = 0
		self.game_totals_basic_info["three_point_field_goal_attempts"] = 2
		self.game_totals_basic_info["free_throws"] = 1
		self.game_totals_basic_info["free_throw_attempts"] = 2
		self.game_totals_basic_info["total_rebounds"] = 0
		self.game_totals_basic_info["assists"] = 0
		self.game_totals_basic_info["steals"] = 0
		self.game_totals_basic_info["blocks"] = 0
		self.game_totals_basic_info["turnovers"] = 1
		self.game_totals_basic_info["points"] = 45
		self.testUtil.insert_into_game_totals_basic(self.game_totals_basic_info)
		
		self.game_totals_basic_info["game_number"] = 4
		self.game_totals_basic_info["field_goals"] = 3
		self.game_totals_basic_info["field_goal_attempts"] = 3
		self.game_totals_basic_info["three_point_field_goals"] = 0
		self.game_totals_basic_info["three_point_field_goal_attempts"] = 2
		self.game_totals_basic_info["free_throws"] = 1
		self.game_totals_basic_info["free_throw_attempts"] = 2
		self.game_totals_basic_info["total_rebounds"] = 0
		self.game_totals_basic_info["assists"] = 0
		self.game_totals_basic_info["steals"] = 0
		self.game_totals_basic_info["blocks"] = 0
		self.game_totals_basic_info["turnovers"] = 1
		self.game_totals_basic_info["points"] = 55
		self.testUtil.insert_into_game_totals_basic(self.game_totals_basic_info)
		
		values = self.projections.calculate_floor_consistency_ceiling_pct("test", 2013, FantasyPointCalculator.STAR_STREET)
		
		self.assertTrue(values[0] == 0.25)
		self.assertTrue(values[1] == 0.75)
		self.assertTrue(values[2] == 0.50)
		self.assertTrue(values[3] == 0.25)
	
	######################################################################
	# Tests the retrieval of vegas odds for a team, either home or road.
	######################################################################
	def test_get_vegas_odds(self):
		self.vegas_info["road_team"] = "PHI"
		self.vegas_info["home_team"] = "BOS"
		self.vegas_info["spread_road"] = -2
		self.vegas_info["spread_home"] = 2
		self.vegas_info["over_under"] = 200
		self.vegas_info["projection_road"] = 101
		self.vegas_info["projection_home"] = 99
		self.testUtil.insert_into_vegas(self.vegas_info)
		
		v = self.projections.get_vegas_odds("BOS")
		#self.assertTrue(v[1] == "PHI")
		#self.assertTrue(v[2] == "BOS")
		self.assertTrue(v["spread"] == 2)
		#self.assertTrue(v[4] == 2)
		self.assertTrue(v["over_under"] == 200)
		#self.assertTrue(v[6] == 101)
		self.assertTrue(v["projection"] == 99)
		
		v = self.projections.get_vegas_odds("PHI")
		#self.assertTrue(v[1] == "PHI")
		#self.assertTrue(v[2] == "BOS")
		self.assertTrue(v["spread"] == -2)
		#self.assertTrue(v[4] == 2)
		self.assertTrue(v["over_under"] == 200)
		#self.assertTrue(v[6] == 101)
		self.assertTrue(v["projection"] ==101)
	
	def test_calculate_defense_vs_position_ranking_PG_fantasy_points(self):
		# Set up player 1
		self.player_info["id"] = "test"
		self.player_info["rg_position"] = "PG"
		self.testUtil.insert_into_players(self.player_info)
		
		# Set up player 2
		self.player_info["id"] = "test2"
		self.player_info["rg_position"] = "PG"
		self.testUtil.insert_into_players(self.player_info)
		
		# Set up game for player 1 against Boston
		self.game_totals_basic_info["player_id"] = "test"
		self.game_totals_basic_info["season"] = 2013
		self.game_totals_basic_info["date"] = date(2013,11,1)
		self.game_totals_basic_info["game_number"] = 1
		self.game_totals_basic_info["opponent"] = "BOS"
		gtb_p1_bos_id = self.testUtil.insert_into_game_totals_basic(self.game_totals_basic_info)
		
		# Set up game for player 2 against Boston
		self.game_totals_basic_info["player_id"] = "test2"
		self.game_totals_basic_info["season"] = 2013
		self.game_totals_basic_info["date"] = date(2013,11,1)
		self.game_totals_basic_info["game_number"] = 2
		self.game_totals_basic_info["opponent"] = "BOS"
		gtb_p2_bos_id = self.testUtil.insert_into_game_totals_basic(self.game_totals_basic_info)
		
		# Set up game for player 1 against Atlanta
		self.game_totals_basic_info["player_id"] = "test"
		self.game_totals_basic_info["season"] = 2013
		self.game_totals_basic_info["date"] = date(2013,11,1)
		self.game_totals_basic_info["game_number"] = 3
		self.game_totals_basic_info["opponent"] = "ATL"
		gtb_p1_atl_id = self.testUtil.insert_into_game_totals_basic(self.game_totals_basic_info)
		
		# Set up game for player 2 against Atlanta
		self.game_totals_basic_info["player_id"] = "test2"
		self.game_totals_basic_info["season"] = 2013
		self.game_totals_basic_info["date"] = date(2013,11,1)
		self.game_totals_basic_info["game_number"] = 4
		self.game_totals_basic_info["opponent"] = "ATL"
		gtb_p2_atl_id = self.testUtil.insert_into_game_totals_basic(self.game_totals_basic_info)
		
		# Establish a 2nd game for Boston so we divide by 2.
		self.team_game_totals_info["team"] = "BOS"
		self.team_game_totals_info["season"] = 2013
		self.team_game_totals_info["game"] = 2
		self.team_game_totals_info["date"] = date(2013,11,1)
		self.team_game_totals_info["opponent"] = "PHI"
		self.testUtil.insert_into_team_game_totals(self.team_game_totals_info)
		
		# Establish a 2nd game for Atlanta so we divide by 2.
		self.team_game_totals_info["team"] = "ATL"
		self.team_game_totals_info["season"] = 2013
		self.team_game_totals_info["game"] = 2
		self.team_game_totals_info["date"] = date(2013,11,1)
		self.team_game_totals_info["opponent"] = "PHI"
		self.testUtil.insert_into_team_game_totals(self.team_game_totals_info)
		
		# Set up fantasy points for player 1 against Boston
		self.fantasy_points_info["game_totals_basic_id"] = gtb_p1_bos_id
		self.fantasy_points_info["player_id"] = "test"
		self.fantasy_points_info["site"] = DFSConstants.FAN_DUEL
		self.fantasy_points_info["season"] = 2013
		self.fantasy_points_info["game_number"] = 1
		self.fantasy_points_info["points"] = 10
		self.testUtil.insert_into_fantasy_points(self.fantasy_points_info)
		
		# Set up fantasy points for player 2 against Boston
		self.fantasy_points_info["game_totals_basic_id"] = gtb_p2_bos_id
		self.fantasy_points_info["player_id"] = "test2"
		self.fantasy_points_info["site"] = DFSConstants.FAN_DUEL
		self.fantasy_points_info["season"] = 2013
		self.fantasy_points_info["game_number"] = 2
		self.fantasy_points_info["points"] = 20
		self.testUtil.insert_into_fantasy_points(self.fantasy_points_info)
		
		# Set up fantasy points for player 1 against Atlanta
		self.fantasy_points_info["game_totals_basic_id"] = gtb_p1_atl_id
		self.fantasy_points_info["player_id"] = "test"
		self.fantasy_points_info["site"] = DFSConstants.FAN_DUEL
		self.fantasy_points_info["season"] = 2013
		self.fantasy_points_info["game_number"] = 3
		self.fantasy_points_info["points"] = 20
		self.testUtil.insert_into_fantasy_points(self.fantasy_points_info)
		
		# Set up fantasy points for player 2 against Atlanta
		self.fantasy_points_info["game_totals_basic_id"] = gtb_p2_atl_id
		self.fantasy_points_info["player_id"] = "test2"
		self.fantasy_points_info["site"] = DFSConstants.FAN_DUEL
		self.fantasy_points_info["season"] = 2013
		self.fantasy_points_info["game_number"] = 4
		self.fantasy_points_info["points"] = 30
		self.testUtil.insert_into_fantasy_points(self.fantasy_points_info)
		
		# self.projections.site =
		bos_rank = self.projections.calculate_defense_vs_position_ranking(
			DFSConstants.FANTASY_POINTS, "PG", "BOS", 2013, DFSConstants.FAN_DUEL, date(2013, 11, 1))
		atl_rank = self.projections.calculate_defense_vs_position_ranking(
			DFSConstants.FANTASY_POINTS, "PG", "ATL", 2013, DFSConstants.FAN_DUEL, date(2013, 11, 1))
		
		self.assertTrue(bos_rank == 1)
		self.assertTrue(atl_rank == 2)

	def test_get_avg_stat_past_n_games_points(self):
		# Set up games for player "test"
		self.game_totals_basic_info["player_id"] = "test"
		self.game_totals_basic_info["season"] = 2013
		self.game_totals_basic_info["date"] = date(2013,11,1)
		self.game_totals_basic_info["game_number"] = 1
		self.game_totals_basic_info["opponent"] = "ATL"
		self.game_totals_basic_info["points"] = 10
		id1 = self.testUtil.insert_into_game_totals_basic(self.game_totals_basic_info)

		self.game_totals_basic_info["player_id"] = "test"
		self.game_totals_basic_info["season"] = 2013
		self.game_totals_basic_info["date"] = date(2013,11,2)
		self.game_totals_basic_info["game_number"] = 2
		self.game_totals_basic_info["opponent"] = "ATL"
		self.game_totals_basic_info["points"] = 12
		id2 = self.testUtil.insert_into_game_totals_basic(self.game_totals_basic_info)

		self.game_totals_basic_info["player_id"] = "test"
		self.game_totals_basic_info["season"] = 2013
		self.game_totals_basic_info["date"] = date(2013,11,3)
		self.game_totals_basic_info["game_number"] = 3
		self.game_totals_basic_info["opponent"] = "ATL"
		self.game_totals_basic_info["points"] = 14
		id3 = self.testUtil.insert_into_game_totals_basic(self.game_totals_basic_info)

		self.assertTrue(self.projections.get_avg_stat_past_n_games("test", "points", 2013, 3) == 12)
		self.assertTrue(self.projections.get_avg_stat_past_n_games("test", "points", 2013, 2) == 13)
		self.assertTrue(self.projections.get_avg_stat_past_n_games("test", "points", 2013, 1) == 14)

	def test_determine_depth_chart_player_missing_games(self):
		##################
		# Set up players
		##################
		self.player_info["id"] = "PG"
		self.player_info["name"] = "Point Guard"
		self.player_info["rg_position"] = "PG"
		self.testUtil.insert_into_players(self.player_info)

		self.player_info["id"] = "PG2"
		self.player_info["name"] = "Point Guard 2"
		self.player_info["rg_position"] = "PG"
		self.testUtil.insert_into_players(self.player_info)

		self.player_info["id"] = "PG3"
		self.player_info["name"] = "Point Guard 3"
		self.player_info["rg_position"] = "PG"
		self.testUtil.insert_into_players(self.player_info)

		###########################
		# Set up player game logs
		###########################
		self.game_totals_basic_info["player_id"] = "PG"
		self.game_totals_basic_info["team"] = "BOS"
		self.game_totals_basic_info["season"] = 2013
		self.game_totals_basic_info["minutes_played"] = 30
		self.game_totals_basic_info["date"] = date(2014, 1, 30)
		self.testUtil.insert_into_game_totals_basic(self.game_totals_basic_info)

		self.game_totals_basic_info["player_id"] = "PG"
		self.game_totals_basic_info["team"] = "BOS"
		self.game_totals_basic_info["season"] = 2013
		self.game_totals_basic_info["minutes_played"] = 28
		self.game_totals_basic_info["date"] = date(2014, 1, 31)
		self.testUtil.insert_into_game_totals_basic(self.game_totals_basic_info)

		self.game_totals_basic_info["player_id"] = "PG2"
		self.game_totals_basic_info["team"] = "BOS"
		self.game_totals_basic_info["season"] = 2013
		self.game_totals_basic_info["minutes_played"] = 24
		self.game_totals_basic_info["date"] = date(2014, 1, 1)
		self.testUtil.insert_into_game_totals_basic(self.game_totals_basic_info)

		# self.game_totals_basic_info["player_id"] = "PG2"
		# self.game_totals_basic_info["team"] = "BOS"
		# self.game_totals_basic_info["season"] = 2013
		# self.game_totals_basic_info["minutes_played"] = 20
		# self.testUtil.insert_into_game_totals_basic(self.game_totals_basic_info)

		self.game_totals_basic_info["player_id"] = "PG3"
		self.game_totals_basic_info["team"] = "BOS"
		self.game_totals_basic_info["season"] = 2013
		self.game_totals_basic_info["minutes_played"] = 12
		self.game_totals_basic_info["date"] = date(2014, 1, 30)
		self.testUtil.insert_into_game_totals_basic(self.game_totals_basic_info)

		self.game_totals_basic_info["player_id"] = "PG3"
		self.game_totals_basic_info["team"] = "BOS"
		self.game_totals_basic_info["season"] = 2013
		self.game_totals_basic_info["minutes_played"] = 8
		self.game_totals_basic_info["date"] = date(2014, 1, 31)
		self.testUtil.insert_into_game_totals_basic(self.game_totals_basic_info)

		#########################
		# Set up team game logs
		#########################
		self.team_game_totals_info["team"] = "BOS"
		self.team_game_totals_info["opponent"] = "MIA"
		self.team_game_totals_info["season"] = 2013
		self.team_game_totals_info["date"] = date(2014, 1, 1)
		self.testUtil.insert_into_team_game_totals(self.team_game_totals_info)

		self.team_game_totals_info["team"] = "BOS"
		self.team_game_totals_info["opponent"] = "MIA"
		self.team_game_totals_info["season"] = 2013
		self.team_game_totals_info["date"] = date(2014, 1, 30)
		self.testUtil.insert_into_team_game_totals(self.team_game_totals_info)

		self.team_game_totals_info["team"] = "BOS"
		self.team_game_totals_info["opponent"] = "MIA"
		self.team_game_totals_info["season"] = 2013
		self.team_game_totals_info["date"] = date(2014, 1, 31)
		self.testUtil.insert_into_team_game_totals(self.team_game_totals_info)

		depth_chart, depth_chart_by_player_id = self.projections.determine_depth_chart(2013, date(2014, 1, 31))

		# Tests for first chart
		self.assertTrue(len(depth_chart) == 1)
		self.assertTrue(len(depth_chart["BOS"]) == 1) # PG position
		self.assertTrue("PG" in depth_chart["BOS"] and "C" not in depth_chart["BOS"])
		self.assertTrue(len(depth_chart["BOS"]["PG"]) == 2)
		self.assertTrue(depth_chart["BOS"]["PG"][0][0] == 29 and
		                depth_chart["BOS"]["PG"][0][1] == "PG" and
						depth_chart["BOS"]["PG"][0][2] == "Point Guard")
		self.assertTrue(depth_chart["BOS"]["PG"][1][0] == 10 and
		                depth_chart["BOS"]["PG"][1][1] == "PG3" and
						depth_chart["BOS"]["PG"][1][2] == "Point Guard 3")

		# Tests for second chart
		self.assertTrue(depth_chart_by_player_id["PG"][0] == "Point Guard" and
						depth_chart_by_player_id["PG"][1] == 29 and
						depth_chart_by_player_id["PG"][2] == 1 and
						depth_chart_by_player_id["PG"][3] >= 0.74 and depth_chart_by_player_id["PG"][3] <= 0.75)
		self.assertTrue("PG2" not in depth_chart_by_player_id)
		self.assertTrue(depth_chart_by_player_id["PG3"][0] == "Point Guard 3" and
						depth_chart_by_player_id["PG3"][1] == 10 and
						depth_chart_by_player_id["PG3"][2] == 2 and
						depth_chart_by_player_id["PG3"][3] >= 0.255 and depth_chart_by_player_id["PG3"][3] <= 0.26)

	def test_determine_depth_chart(self):
		self.player_info["id"] = "PG"
		self.player_info["name"] = "Point Guard"
		self.player_info["rg_position"] = "PG"
		self.testUtil.insert_into_players(self.player_info)

		self.player_info["id"] = "PG2"
		self.player_info["name"] = "Point Guard 2"
		self.player_info["rg_position"] = "PG"
		self.testUtil.insert_into_players(self.player_info)

		self.player_info["id"] = "C"
		self.player_info["name"] = "Center"
		self.player_info["rg_position"] = "C"
		self.testUtil.insert_into_players(self.player_info)

		self.player_info["id"] = "C2"
		self.player_info["name"] = "Center 2"
		self.player_info["rg_position"] = "C"
		self.testUtil.insert_into_players(self.player_info)

		self.game_totals_basic_info["player_id"] = "PG"
		self.game_totals_basic_info["team"] = "BOS"
		self.game_totals_basic_info["season"] = 2013
		self.game_totals_basic_info["minutes_played"] = 30
		self.testUtil.insert_into_game_totals_basic(self.game_totals_basic_info)

		self.game_totals_basic_info["player_id"] = "PG"
		self.game_totals_basic_info["team"] = "BOS"
		self.game_totals_basic_info["season"] = 2013
		self.game_totals_basic_info["minutes_played"] = 28
		self.testUtil.insert_into_game_totals_basic(self.game_totals_basic_info)

		self.game_totals_basic_info["player_id"] = "C"
		self.game_totals_basic_info["team"] = "ATL"
		self.game_totals_basic_info["season"] = 2013
		self.game_totals_basic_info["minutes_played"] = 15
		self.testUtil.insert_into_game_totals_basic(self.game_totals_basic_info)

		self.game_totals_basic_info["player_id"] = "C"
		self.game_totals_basic_info["team"] = "ATL"
		self.game_totals_basic_info["season"] = 2013
		self.game_totals_basic_info["minutes_played"] = 13
		self.testUtil.insert_into_game_totals_basic(self.game_totals_basic_info)

		self.game_totals_basic_info["player_id"] = "PG2"
		self.game_totals_basic_info["team"] = "BOS"
		self.game_totals_basic_info["season"] = 2013
		self.game_totals_basic_info["minutes_played"] = 15
		self.testUtil.insert_into_game_totals_basic(self.game_totals_basic_info)

		self.game_totals_basic_info["player_id"] = "PG2"
		self.game_totals_basic_info["team"] = "BOS"
		self.game_totals_basic_info["season"] = 2013
		self.game_totals_basic_info["minutes_played"] = 17
		self.testUtil.insert_into_game_totals_basic(self.game_totals_basic_info)

		self.game_totals_basic_info["player_id"] = "C2"
		self.game_totals_basic_info["team"] = "ATL"
		self.game_totals_basic_info["season"] = 2013
		self.game_totals_basic_info["minutes_played"] = 30
		self.testUtil.insert_into_game_totals_basic(self.game_totals_basic_info)

		self.game_totals_basic_info["player_id"] = "C2"
		self.game_totals_basic_info["team"] = "ATL"
		self.game_totals_basic_info["season"] = 2013
		self.game_totals_basic_info["minutes_played"] = 32
		self.testUtil.insert_into_game_totals_basic(self.game_totals_basic_info)

		depth_chart, depth_chart_by_player_id = self.projections.determine_depth_chart(2013)

		# Tests for first chart
		self.assertTrue(len(depth_chart) == 2)  # 2 teams - BOS and ATL
		self.assertTrue(len(depth_chart["ATL"]) == 1) # C position
		self.assertTrue("C" in depth_chart["ATL"] and "PF" not in depth_chart["ATL"])
		self.assertTrue(len(depth_chart["BOS"]) == 1) # PG position
		self.assertTrue("PG" in depth_chart["BOS"] and "C" not in depth_chart["BOS"])
		self.assertTrue(depth_chart["ATL"]["C"][0][0] == 31 and
		                depth_chart["ATL"]["C"][0][1] == "C2" and
						depth_chart["ATL"]["C"][0][2] == "Center 2")
		self.assertTrue(depth_chart["ATL"]["C"][1][0] == 14 and
		                depth_chart["ATL"]["C"][1][1] == "C" and
						depth_chart["ATL"]["C"][1][2] == "Center")
		self.assertTrue(depth_chart["BOS"]["PG"][0][0] == 29 and
		                depth_chart["BOS"]["PG"][0][1] == "PG" and
						depth_chart["BOS"]["PG"][0][2] == "Point Guard")
		self.assertTrue(depth_chart["BOS"]["PG"][1][0] == 16 and
		                depth_chart["BOS"]["PG"][1][1] == "PG2" and
						depth_chart["BOS"]["PG"][1][2] == "Point Guard 2")

		# Tests for second chart
		self.assertTrue(depth_chart_by_player_id["C"][0] == "Center" and
						depth_chart_by_player_id["C"][1] == 14 and
						depth_chart_by_player_id["C"][2] == 2 and
						depth_chart_by_player_id["C"][3] >= 0.31 and depth_chart_by_player_id["C"][3] <= 0.312)
		self.assertTrue(depth_chart_by_player_id["C2"][0] == "Center 2" and
						depth_chart_by_player_id["C2"][1] == 31 and
						depth_chart_by_player_id["C2"][2] == 1 and
						depth_chart_by_player_id["C2"][3] >= 0.68 and depth_chart_by_player_id["C2"][3] <= 0.69)
		self.assertTrue(depth_chart_by_player_id["PG"][0] == "Point Guard" and
						depth_chart_by_player_id["PG"][1] == 29 and
						depth_chart_by_player_id["PG"][2] == 1 and
						depth_chart_by_player_id["PG"][3] >= 0.64 and depth_chart_by_player_id["PG"][3] <= 0.65)
		self.assertTrue(depth_chart_by_player_id["PG2"][0] == "Point Guard 2" and
						depth_chart_by_player_id["PG2"][1] == 16 and
						depth_chart_by_player_id["PG2"][2] == 2 and
						depth_chart_by_player_id["PG2"][3] >= 0.35 and depth_chart_by_player_id["PG2"][3] <= 0.36)

	def test_determine_depth_chart_with_injury(self):
		self.player_info["id"] = "PG"
		self.player_info["name"] = "Point Guard"
		self.player_info["rg_position"] = "PG"
		self.testUtil.insert_into_players(self.player_info)

		self.player_info["id"] = "PG2"
		self.player_info["name"] = "Point Guard 2"
		self.player_info["rg_position"] = "PG"
		self.testUtil.insert_into_players(self.player_info)

		self.player_info["id"] = "PG3"
		self.player_info["name"] = "Point Guard 3"
		self.player_info["rg_position"] = "PG"
		self.testUtil.insert_into_players(self.player_info)

		self.game_totals_basic_info["player_id"] = "PG"
		self.game_totals_basic_info["team"] = "BOS"
		self.game_totals_basic_info["season"] = 2013
		self.game_totals_basic_info["minutes_played"] = 30
		self.testUtil.insert_into_game_totals_basic(self.game_totals_basic_info)

		self.game_totals_basic_info["player_id"] = "PG2"
		self.game_totals_basic_info["team"] = "BOS"
		self.game_totals_basic_info["season"] = 2013
		self.game_totals_basic_info["minutes_played"] = 10
		self.testUtil.insert_into_game_totals_basic(self.game_totals_basic_info)

		self.game_totals_basic_info["player_id"] = "PG3"
		self.game_totals_basic_info["team"] = "BOS"
		self.game_totals_basic_info["season"] = 2013
		self.game_totals_basic_info["minutes_played"] = 40
		self.testUtil.insert_into_game_totals_basic(self.game_totals_basic_info)

		one_day = timedelta(days=1)
		tomorrow = date.today() + one_day
		injury = Injury(player_id="PG3", injury_date=date(2014,1,1), return_date=tomorrow, details="test")
		self.injury_manager.insert(injury)

		depth_chart, depth_chart_by_player_id = self.projections.determine_depth_chart(2013)

		# Tests for first chart
		self.assertTrue(len(depth_chart) == 1)
		self.assertTrue(len(depth_chart["BOS"]) == 1)
		self.assertTrue(depth_chart["BOS"]["PG"][0][0] == 40 and
						depth_chart["BOS"]["PG"][0][1] == "PG3" and
						depth_chart["BOS"]["PG"][0][2] == "Point Guard 3")
		self.assertTrue(depth_chart["BOS"]["PG"][1][0] == 30 and
						depth_chart["BOS"]["PG"][1][1] == "PG" and
						depth_chart["BOS"]["PG"][1][2] == "Point Guard")
		self.assertTrue(depth_chart["BOS"]["PG"][2][0] == 10 and
						depth_chart["BOS"]["PG"][2][1] == "PG2" and
						depth_chart["BOS"]["PG"][2][2] == "Point Guard 2")

		# Tests for second chart
		self.assertTrue(depth_chart_by_player_id["PG"][0] == "Point Guard" and
						depth_chart_by_player_id["PG"][1] == 35 and
						depth_chart_by_player_id["PG"][2] == 1 and
						depth_chart_by_player_id["PG"][3] == 0.75)
		self.assertTrue(depth_chart_by_player_id["PG2"][0] == "Point Guard 2" and
						depth_chart_by_player_id["PG2"][1] == 20 and
						depth_chart_by_player_id["PG2"][2] == 2 and
						depth_chart_by_player_id["PG2"][3] == 0.25)
		self.assertTrue(depth_chart_by_player_id["PG3"][0] == "Point Guard 3" and
						depth_chart_by_player_id["PG3"][1] == 0 and
						depth_chart_by_player_id["PG3"][2] == -1 and
						depth_chart_by_player_id["PG3"][3] == 0.0)

	def test_calculate_expected_team_points(self):
		# expected pace is 96.693431372549 (From BOS game on 1/13/2014)
		self.team_game_totals_info["team"] = "BOS"
		self.team_game_totals_info["opponent"] = "PHI"
		self.team_game_totals_info["season"] = 2013
		self.team_game_totals_info["date"] = date(2014,1,1)
		self.team_game_totals_info["points"] = 100
		self.team_game_totals_info["opp_points"] = 90
		self.team_game_totals_info["field_goal_attempts"] = 101
		self.team_game_totals_info["free_throw_attempts"] = 14
		self.team_game_totals_info["offensive_rebounds"] = 15
		self.team_game_totals_info["opp_total_rebounds"] = 46
		self.team_game_totals_info["opp_offensive_rebounds"] = 10
		self.team_game_totals_info["field_goals"] = 38
		self.team_game_totals_info["turnovers"] = 13
		self.team_game_totals_info["opp_field_goal_attempts"] = 79
		self.team_game_totals_info["opp_free_throw_attempts"] = 34
		self.team_game_totals_info["total_rebounds"] = 50
		self.team_game_totals_info["opp_field_goals"] = 37
		self.team_game_totals_info["opp_turnovers"] = 11
		self.testUtil.insert_into_team_game_totals(self.team_game_totals_info)

		# Expected pace is 89.135004 (from BOS game on 1/11/2014)
		self.team_game_totals_info["team"] = "BOS"
		self.team_game_totals_info["opponent"] = "TOR"
		self.team_game_totals_info["season"] = 2013
		self.team_game_totals_info["date"] = date(2014,1,2)
		self.team_game_totals_info["points"] = 98
		self.team_game_totals_info["opp_points"] = 92
		self.team_game_totals_info["field_goal_attempts"] = 95
		self.team_game_totals_info["free_throw_attempts"] = 17
		self.team_game_totals_info["offensive_rebounds"] = 20
		self.team_game_totals_info["opp_total_rebounds"] = 49
		self.team_game_totals_info["opp_offensive_rebounds"] = 20
		self.team_game_totals_info["field_goals"] = 44
		self.team_game_totals_info["turnovers"] = 9
		self.team_game_totals_info["opp_field_goal_attempts"] = 93
		self.team_game_totals_info["opp_free_throw_attempts"] = 26
		self.team_game_totals_info["total_rebounds"] = 46
		self.team_game_totals_info["opp_field_goals"] = 40
		self.team_game_totals_info["opp_turnovers"] = 11
		self.testUtil.insert_into_team_game_totals(self.team_game_totals_info)

		# Expected pace is 95.87561 (from NYK game on 1/13/2014)
		self.team_game_totals_info["team"] = "NYK"
		self.team_game_totals_info["opponent"] = "MIA"
		self.team_game_totals_info["season"] = 2013
		self.team_game_totals_info["date"] = date(2014,1,1)
		self.team_game_totals_info["points"] = 100
		self.team_game_totals_info["opp_points"] = 90
		self.team_game_totals_info["field_goal_attempts"] = 81
		self.team_game_totals_info["free_throw_attempts"] = 27
		self.team_game_totals_info["offensive_rebounds"] = 12
		self.team_game_totals_info["opp_total_rebounds"] = 49
		self.team_game_totals_info["opp_offensive_rebounds"] = 17
		self.team_game_totals_info["field_goals"] = 35
		self.team_game_totals_info["turnovers"] = 18
		self.team_game_totals_info["opp_field_goal_attempts"] = 93
		self.team_game_totals_info["opp_free_throw_attempts"] = 28
		self.team_game_totals_info["total_rebounds"] = 53
		self.team_game_totals_info["opp_field_goals"] = 33
		self.team_game_totals_info["opp_turnovers"] = 10
		self.testUtil.insert_into_team_game_totals(self.team_game_totals_info)

		# Expected pace is 89.704090 (from NYK game on 1/14/2014)
		self.team_game_totals_info["team"] = "NYK"
		self.team_game_totals_info["opponent"] = "MIA"
		self.team_game_totals_info["season"] = 2013
		self.team_game_totals_info["date"] = date(2014,1,2)
		self.team_game_totals_info["points"] = 102
		self.team_game_totals_info["opp_points"] = 100
		self.team_game_totals_info["field_goal_attempts"] = 81
		self.team_game_totals_info["free_throw_attempts"] = 18
		self.team_game_totals_info["offensive_rebounds"] = 4
		self.team_game_totals_info["opp_total_rebounds"] = 37
		self.team_game_totals_info["opp_offensive_rebounds"] = 5
		self.team_game_totals_info["field_goals"] = 39
		self.team_game_totals_info["turnovers"] = 9
		self.team_game_totals_info["opp_field_goal_attempts"] = 75
		self.team_game_totals_info["opp_free_throw_attempts"] = 33
		self.team_game_totals_info["total_rebounds"] = 32
		self.team_game_totals_info["opp_field_goals"] = 38
		self.team_game_totals_info["opp_turnovers"] = 5
		self.testUtil.insert_into_team_game_totals(self.team_game_totals_info)

		# BOS offensive efficiency = (avg_points/avg_pace) * 100 = 99/92.9142117 * 100 = 106.549893
		# BOS defensive efficiency = (avg_opp_points/avg_pace) * 100 = 91/92.9142117 * 100 = 97.939807
		# NYK offensive efficiency = 101/92.78985 * 100 = 108.848112
		# NYK defensive efficiency = 95/92.78985 * 100 = 102.381888

		bos_points = self.projections.calculate_expected_team_points("BOS", "NYK", 2013)
		nyk_points = self.projections.calculate_expected_team_points("NYK", "BOS", 2013)

		# ((BOS_off_eff + NYK_def_eff)/2 * (NYK_pace + BOS_pace)/2) / 100 =
		#       ((106.549893 + 102.381888)/2 * (92.78985 + 92.9142117)/2) / 100 =
		#       ((208.931781)/2) * (185.7040617)/2) / 100 =
		#       (104.4658905 * 92.85203085) / 100 = 96.99870087478722
		self.assertTrue(bos_points <= 97 and bos_points >= 96.9987)

		# ((NYK_off_eff + BOS_def_eff)/2 * (NYK_pace + BOS_pace)/2) / 100 =
		#       ((108.848112 + 97.939807)/2 * (92.78985 + 92.9142117)/2) * 100 =
		#       ((206.787919)/2) * (185.7040617)/2) / 100 =
		#       (103.3939595 * 92.85203085) / 100 = 96.00339117197651
		self.assertTrue(nyk_points >= 96 and nyk_points <= 96.00339)

	def test_calculate_scoring_stddev(self):
		# Unfortunately, Sqlite doesn't have a stddev function so we can't test this right now.
		# Just pass it automatically.
		self.assertTrue(True)

		# # Add a player
		# self.player_info["id"] = "macleda01"
		# self.player_info["name"] = "Dan"
		# self.player_info["position"] = "G"
		# self.player_info["height"] = 69
		# self.player_info["weight"] = 175
		# self.player_info["url"] = "something"
		# self.testUtil.insert_into_players(self.player_info)
		#
		# # Add game_total_basic and fantasy_point pairs
		# self.game_totals_basic_info["player_id"] = "macleda01"
		# self.game_totals_basic_info["team"] = "BOS"
		# self.game_totals_basic_info["season"] = 2013
		# self.game_totals_basic_info["date"] = date(2014, 1, 1)
		# self.game_totals_basic_info["game_number"] = 1
		# id = self.testUtil.insert_into_game_totals_basic(self.game_totals_basic_info)
		#
		# self.fantasy_points_info["game_totals_basic_id"] = id
		# self.fantasy_points_info["player_id"] = "macleda01"
		# self.fantasy_points_info["site"] = DFSConstants.FAN_DUEL
		# self.fantasy_points_info["season"] = 2013
		# self.fantasy_points_info["game_number"] = 1
		# self.fantasy_points_info["points"] = 10
		# self.testUtil.insert_into_fantasy_points(self.fantasy_points_info)
		#
		# self.game_totals_basic_info["player_id"] = "macleda01"
		# self.game_totals_basic_info["team"] = "BOS"
		# self.game_totals_basic_info["season"] = 2013
		# self.game_totals_basic_info["date"] = date(2014, 1, 2)
		# self.game_totals_basic_info["game_number"] = 2
		# id = self.testUtil.insert_into_game_totals_basic(self.game_totals_basic_info)
		#
		# self.fantasy_points_info["game_totals_basic_id"] = id
		# self.fantasy_points_info["player_id"] = "macleda01"
		# self.fantasy_points_info["site"] = DFSConstants.FAN_DUEL
		# self.fantasy_points_info["season"] = 2013
		# self.fantasy_points_info["game_number"] = 2
		# self.fantasy_points_info["points"] = 12
		# self.testUtil.insert_into_fantasy_points(self.fantasy_points_info)
		#
		# self.game_totals_basic_info["player_id"] = "macleda01"
		# self.game_totals_basic_info["team"] = "BOS"
		# self.game_totals_basic_info["season"] = 2013
		# self.game_totals_basic_info["date"] = date(2014, 1, 3)
		# self.game_totals_basic_info["game_number"] = 3
		# id = self.testUtil.insert_into_game_totals_basic(self.game_totals_basic_info)
		#
		# self.fantasy_points_info["game_totals_basic_id"] = id
		# self.fantasy_points_info["player_id"] = "macleda01"
		# self.fantasy_points_info["site"] = DFSConstants.FAN_DUEL
		# self.fantasy_points_info["season"] = 2013
		# self.fantasy_points_info["game_number"] = 3
		# self.fantasy_points_info["points"] = 20
		# self.testUtil.insert_into_fantasy_points(self.fantasy_points_info)
		#
		# fp_data = self.projections.calculate_scoring_stddev("macleda01", 2013, DFSConstants.FAN_DUEL)
		# self.assertTrue(fp_data[0] == 14)
		# self.assertTrue(fp_data[1] == 5.2915)


	#def test_get_avg_contribution_to_team_stat(self):
		

if __name__ == '__main__':
	unittest.main()