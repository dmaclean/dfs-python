import sys
sys.path.append('..')

from datetime import date
import sqlite3
import unittest
import BBRTestUtility
import fantasy_point_calculator

class TestFantasyPointCalculator(unittest.TestCase):
	def setUp(self):
		self.testUtil = BBRTestUtility.BBRTestUtility()
		self.fpc = fantasy_point_calculator.FantasyPointCalculator(self.testUtil.conn)
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
	
	def tearDown(self):
		self.testUtil.conn.close()
		
		self.player_info = {}
	
	##################################################
	# DraftDay - player with no double/triple-double
	#
	# 8/10 field goals
	# 1/2 three pointers
	# 5/6 free throws
	# 5 rebounds
	# 2 assists
	# 1 steal
	# 2 blocks
	# 1 turnover
	# 24 points
	#
	# 24 fantasy points from points
	# 1 on 3pt bonus
	# -1 on 4 missed shots
	# 6.25 on rebounds
	# 3 on assists
	# 2 on steals
	# 4 on blocks
	# -1 on turnovers
	# 0 for double-double
	# 0 for triple-double
	# 38.25 total fantasy points
	##################################################
	def test_calculate_draft_day(self):
		stats = {
			"player_id": "dmaclean",
			"season": date.today(),
			"game_number": 1,
			"field_goals": 8,
			"field_goal_attempts": 10,
			"three_point_field_goals": 1,
			"three_point_field_goal_attempts": 2,
			"free_throws": 5,
			"free_throw_attempts": 6,
			"total_rebounds": 5,
			"assists": 2,
			"steals": 1,
			"blocks": 2,
			"turnovers": 1,
			"points": 24
		}
		
		self.fpc.site = self.fpc.DRAFT_DAY
		points = self.fpc.calculate(stats)
		
		self.assertTrue(points == 38.25)
	
	##################################################
	# DraftDay - player with double-double
	#
	# 8/10 field goals
	# 1/2 three pointers
	# 5/6 free throws
	# 10 rebounds
	# 2 assists
	# 1 steal
	# 2 blocks
	# 1 turnover
	# 24 points
	#
	# 24 fantasy points from points
	# 1 on 3pt bonus
	# -1 on 4 missed shots
	# 12.5 on rebounds
	# 3 on assists
	# 2 on steals
	# 4 on blocks
	# -1 on turnovers
	# 2 for double-double
	# 0 for triple-double
	# 46.5 total fantasy points
	##################################################
	def test_calculate_draft_day_double_double(self):
		stats = {
			"player_id": "dmaclean",
			"season": date.today(),
			"game_number": 1,
			"field_goals": 8,
			"field_goal_attempts": 10,
			"three_point_field_goals": 1,
			"three_point_field_goal_attempts": 2,
			"free_throws": 5,
			"free_throw_attempts": 6,
			"total_rebounds": 10,
			"assists": 2,
			"steals": 1,
			"blocks": 2,
			"turnovers": 1,
			"points": 24
		}
		
		self.fpc.site = self.fpc.DRAFT_DAY
		points = self.fpc.calculate(stats)
		
		self.assertTrue(points == 46.5)
	
	##################################################
	# DraftDay - player with triple-double
	#
	# 8/10 field goals
	# 1/2 three pointers
	# 5/6 free throws
	# 10 rebounds
	# 10 assists
	# 1 steal
	# 2 blocks
	# 1 turnover
	# 24 points
	#
	# 24 fantasy points from points
	# 1 on 3pt bonus
	# -1 on 4 missed shots
	# 12.5 on rebounds
	# 15 on assists
	# 2 on steals
	# 4 on blocks
	# -1 on turnovers
	# 0 for double-double
	# 2 for triple-double
	# 58.5 total fantasy points
	##################################################
	def test_calculate_draft_day_triple_double(self):
		stats = {
			"player_id": "dmaclean",
			"season": date.today(),
			"game_number": 1,
			"field_goals": 8,
			"field_goal_attempts": 10,
			"three_point_field_goals": 1,
			"three_point_field_goal_attempts": 2,
			"free_throws": 5,
			"free_throw_attempts": 6,
			"total_rebounds": 10,
			"assists": 10,
			"steals": 1,
			"blocks": 2,
			"turnovers": 1,
			"points": 24
		}
		
		self.fpc.site = self.fpc.DRAFT_DAY
		points = self.fpc.calculate(stats)
		
		self.assertTrue(points == 58.5)
	
	##################################################
	# DraftKings - player with no double/triple-double
	#
	# 8/10 field goals
	# 1/2 three pointers
	# 5/6 free throws
	# 5 rebounds
	# 2 assists
	# 1 steal
	# 2 blocks
	# 1 turnover
	# 24 points
	#
	# 24 fantasy points from points
	# 0.5 on 3pt bonus
	# 0 on 4 missed shots
	# 6.25 on rebounds
	# 3 on assists
	# 2 on steals
	# 4 on blocks
	# -0.5 on turnovers
	# 0 for double-double
	# 0 for triple-double
	# 38.25 total fantasy points
	##################################################
	def test_calculate_draft_kings(self):
		stats = {
			"player_id": "dmaclean",
			"season": date.today(),
			"game_number": 1,
			"field_goals": 8,
			"field_goal_attempts": 10,
			"three_point_field_goals": 1,
			"three_point_field_goal_attempts": 2,
			"free_throws": 5,
			"free_throw_attempts": 6,
			"total_rebounds": 5,
			"assists": 2,
			"steals": 1,
			"blocks": 2,
			"turnovers": 1,
			"points": 24
		}
		
		self.fpc.site = self.fpc.DRAFT_KINGS
		points = self.fpc.calculate(stats)
		
		self.assertTrue(points == 39.25)
	
	##################################################
	# DraftKings - player with double-double
	#
	# 8/10 field goals
	# 1/2 three pointers
	# 5/6 free throws
	# 10 rebounds
	# 2 assists
	# 1 steal
	# 2 blocks
	# 1 turnover
	# 24 points
	#
	# 24 fantasy points from points
	# 0.5 on 3pt bonus
	# 0 on 4 missed shots
	# 12.5 on rebounds
	# 3 on assists
	# 2 on steals
	# 4 on blocks
	# -0.5 on turnovers
	# 1.5 for double-double
	# 0 for triple-double
	# 46.5 total fantasy points
	##################################################
	def test_calculate_draft_kings_double_double(self):
		stats = {
			"player_id": "dmaclean",
			"season": date.today(),
			"game_number": 1,
			"field_goals": 8,
			"field_goal_attempts": 10,
			"three_point_field_goals": 1,
			"three_point_field_goal_attempts": 2,
			"free_throws": 5,
			"free_throw_attempts": 6,
			"total_rebounds": 10,
			"assists": 2,
			"steals": 1,
			"blocks": 2,
			"turnovers": 1,
			"points": 24
		}
		
		self.fpc.site = self.fpc.DRAFT_KINGS
		points = self.fpc.calculate(stats)
		
		self.assertTrue(points == 47)
	
	##################################################
	# DraftKings - player with triple-double
	#
	# 8/10 field goals
	# 1/2 three pointers
	# 5/6 free throws
	# 10 rebounds
	# 10 assists
	# 1 steal
	# 2 blocks
	# 1 turnover
	# 24 points
	#
	# 24 fantasy points from points
	# 0.5 on 3pt bonus
	# 0 on 4 missed shots
	# 12.5 on rebounds
	# 15 on assists
	# 2 on steals
	# 4 on blocks
	# -0.5 on turnovers
	# 0 for double-double
	# 3 for triple-double
	# 58.5 total fantasy points
	##################################################
	def test_calculate_draft_kings_triple_double(self):
		stats = {
			"player_id": "dmaclean",
			"season": date.today(),
			"game_number": 1,
			"field_goals": 8,
			"field_goal_attempts": 10,
			"three_point_field_goals": 1,
			"three_point_field_goal_attempts": 2,
			"free_throws": 5,
			"free_throw_attempts": 6,
			"total_rebounds": 10,
			"assists": 10,
			"steals": 1,
			"blocks": 2,
			"turnovers": 1,
			"points": 24
		}
		
		self.fpc.site = self.fpc.DRAFT_KINGS
		points = self.fpc.calculate(stats)
		
		self.assertTrue(points == 60.5)
	
	##################################################
	# StarStreet
	#
	# 8/10 field goals
	# 1/2 three pointers
	# 5/6 free throws
	# 5 rebounds
	# 2 assists
	# 1 steal
	# 2 blocks
	# 1 turnover
	# 24 points
	#
	# 24 fantasy points from points
	# 0 on 3pt bonus
	# 0 on 4 missed shots
	# 6.25 on rebounds
	# 3 on assists
	# 2 on steals
	# 4 on blocks
	# -1 on turnovers
	# 0 for double-double
	# 0 for triple-double
	# 38.25 total fantasy points
	##################################################
	def test_calculate_starstreet(self):
		stats = {
			"player_id": "dmaclean",
			"season": date.today(),
			"game_number": 1,
			"field_goals": 8,
			"field_goal_attempts": 10,
			"three_point_field_goals": 1,
			"three_point_field_goal_attempts": 2,
			"free_throws": 5,
			"free_throw_attempts": 6,
			"total_rebounds": 5,
			"assists": 2,
			"steals": 1,
			"blocks": 2,
			"turnovers": 1,
			"points": 24
		}
		
		self.fpc.site = self.fpc.STAR_STREET
		points = self.fpc.calculate(stats)
		
		self.assertTrue(points == 38.25)
	
if __name__ == '__main__':
	unittest.main()