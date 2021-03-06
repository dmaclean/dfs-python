from datetime import date
import unittest
import BBRTestUtility
from nba.basketball import Processor
from nba.parsers.basketballreference_team_gamelog_parser import BasketballReferenceTeamGameLogParser


class TestBasketballReferenceTeamGameLogParser(unittest.TestCase):
	
	def setUp(self):
		self.testUtil = BBRTestUtility.BBRTestUtility()
		self.processor = Processor()
		self.team_game_log_parser = BasketballReferenceTeamGameLogParser()
		
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
	
	def tearDown(self):
		self.testUtil.conn.close()
		
		self.player_info = {}
	
	def test_team_2013(self):
		data = self.processor.fetchData('/teams/BOS/2014/gamelog/', False)

		self.team_game_log_parser.process(data)

		##########
		# Game 1
		##########
		self.assertTrue(self.team_game_log_parser.game_stats[1]["date"] == "2013-10-30")
		self.assertTrue(not self.team_game_log_parser.game_stats[1]["home"])
		self.assertTrue(self.team_game_log_parser.game_stats[1]["opponent"] == "TOR")
		self.assertTrue(self.team_game_log_parser.game_stats[1]["result"] == "L")
		self.assertTrue(self.team_game_log_parser.game_stats[1]["points"] == 87)
		self.assertTrue(self.team_game_log_parser.game_stats[1]["opp_points"] == 93)
		self.assertTrue(self.team_game_log_parser.game_stats[1]["field_goals"] == 32)
		self.assertTrue(self.team_game_log_parser.game_stats[1]["field_goal_attempts"] == 66)
		# self.assertTrue(self.team_game_log_parser.game_stats[0]["field_goal_pct"] == 93)
		self.assertTrue(self.team_game_log_parser.game_stats[1]["three_point_field_goals"] == 3)
		self.assertTrue(self.team_game_log_parser.game_stats[1]["three_point_field_goal_attempts"] == 13)
		self.assertTrue(self.team_game_log_parser.game_stats[1]["free_throws"] == 20)
		self.assertTrue(self.team_game_log_parser.game_stats[1]["free_throw_attempts"] == 29)
		self.assertTrue(self.team_game_log_parser.game_stats[1]["offensive_rebounds"] == 7)
		self.assertTrue(self.team_game_log_parser.game_stats[1]["total_rebounds"] == 33)
		self.assertTrue(self.team_game_log_parser.game_stats[1]["assists"] == 15)
		self.assertTrue(self.team_game_log_parser.game_stats[1]["steals"] == 10)
		self.assertTrue(self.team_game_log_parser.game_stats[1]["blocks"] == 7)
		self.assertTrue(self.team_game_log_parser.game_stats[1]["turnovers"] == 22)
		self.assertTrue(self.team_game_log_parser.game_stats[1]["personal_fouls"] == 27)
		self.assertTrue(self.team_game_log_parser.game_stats[1]["opp_field_goals"] == 38)
		self.assertTrue(self.team_game_log_parser.game_stats[1]["opp_field_goal_attempts"] == 86)
		# self.assertTrue(self.team_game_log_parser.game_stats[0]["opp_field_goal_pct"] == .442)
		self.assertTrue(self.team_game_log_parser.game_stats[1]["opp_three_point_field_goals"] == 5)
		self.assertTrue(self.team_game_log_parser.game_stats[1]["opp_three_point_field_goal_attempts"] == 17)
		self.assertTrue(self.team_game_log_parser.game_stats[1]["opp_free_throws"] == 12)
		self.assertTrue(self.team_game_log_parser.game_stats[1]["opp_free_throw_attempts"] == 23)
		self.assertTrue(self.team_game_log_parser.game_stats[1]["opp_offensive_rebounds"] == 19)
		self.assertTrue(self.team_game_log_parser.game_stats[1]["opp_total_rebounds"] == 48)
		self.assertTrue(self.team_game_log_parser.game_stats[1]["opp_assists"] == 15)
		self.assertTrue(self.team_game_log_parser.game_stats[1]["opp_steals"] == 9)
		self.assertTrue(self.team_game_log_parser.game_stats[1]["opp_blocks"] == 6)
		self.assertTrue(self.team_game_log_parser.game_stats[1]["opp_turnovers"] == 17)
		self.assertTrue(self.team_game_log_parser.game_stats[1]["opp_personal_fouls"] == 25)

		self.assertTrue(self.team_game_log_parser.game_stats[44]["result"] == "W")

		####################################
		# Game 21 - this is in a new table
		####################################
		self.assertTrue(self.team_game_log_parser.game_stats[21]["date"] == "2013-12-06")
		self.assertTrue(self.team_game_log_parser.game_stats[21]["home"])
		self.assertTrue(self.team_game_log_parser.game_stats[21]["opponent"] == "DEN")
		self.assertTrue(self.team_game_log_parser.game_stats[21]["result"] == "W")
		self.assertTrue(self.team_game_log_parser.game_stats[21]["points"] == 106)
		self.assertTrue(self.team_game_log_parser.game_stats[21]["opp_points"] == 98)
		self.assertTrue(self.team_game_log_parser.game_stats[21]["field_goals"] == 43)
		self.assertTrue(self.team_game_log_parser.game_stats[21]["field_goal_attempts"] == 83)
		# self.assertTrue(self.team_game_log_parser.game_stats[0]["field_goal_pct"] == 93)
		self.assertTrue(self.team_game_log_parser.game_stats[21]["three_point_field_goals"] == 6)
		self.assertTrue(self.team_game_log_parser.game_stats[21]["three_point_field_goal_attempts"] == 20)
		self.assertTrue(self.team_game_log_parser.game_stats[21]["free_throws"] == 14)
		self.assertTrue(self.team_game_log_parser.game_stats[21]["free_throw_attempts"] == 18)
		self.assertTrue(self.team_game_log_parser.game_stats[21]["offensive_rebounds"] == 10)
		self.assertTrue(self.team_game_log_parser.game_stats[21]["total_rebounds"] == 37)
		self.assertTrue(self.team_game_log_parser.game_stats[21]["assists"] == 25)
		self.assertTrue(self.team_game_log_parser.game_stats[21]["steals"] == 5)
		self.assertTrue(self.team_game_log_parser.game_stats[21]["blocks"] == 6)
		self.assertTrue(self.team_game_log_parser.game_stats[21]["turnovers"] == 9)
		self.assertTrue(self.team_game_log_parser.game_stats[21]["personal_fouls"] == 18)
		self.assertTrue(self.team_game_log_parser.game_stats[21]["opp_field_goals"] == 34)
		self.assertTrue(self.team_game_log_parser.game_stats[21]["opp_field_goal_attempts"] == 77)
		# self.assertTrue(self.team_game_log_parser.game_stats[0]["opp_field_goal_pct"] == .442)
		self.assertTrue(self.team_game_log_parser.game_stats[21]["opp_three_point_field_goals"] == 6)
		self.assertTrue(self.team_game_log_parser.game_stats[21]["opp_three_point_field_goal_attempts"] == 17)
		self.assertTrue(self.team_game_log_parser.game_stats[21]["opp_free_throws"] == 24)
		self.assertTrue(self.team_game_log_parser.game_stats[21]["opp_free_throw_attempts"] == 29)
		self.assertTrue(self.team_game_log_parser.game_stats[21]["opp_offensive_rebounds"] == 15)
		self.assertTrue(self.team_game_log_parser.game_stats[21]["opp_total_rebounds"] == 42)
		self.assertTrue(self.team_game_log_parser.game_stats[21]["opp_assists"] == 11)
		self.assertTrue(self.team_game_log_parser.game_stats[21]["opp_steals"] == 4)
		self.assertTrue(self.team_game_log_parser.game_stats[21]["opp_blocks"] == 4)
		self.assertTrue(self.team_game_log_parser.game_stats[21]["opp_turnovers"] == 14)
		self.assertTrue(self.team_game_log_parser.game_stats[21]["opp_personal_fouls"] == 19)

	def test_team_2012(self):
		data = self.processor.fetchData('/teams/BOS/2012/gamelog/', False)
		
		self.team_game_log_parser.process(data)

		##########
		# Game 1
		##########
		self.assertTrue(self.team_game_log_parser.game_stats[1]["date"] == "2011-12-25")
		self.assertTrue(not self.team_game_log_parser.game_stats[1]["home"])
		self.assertTrue(self.team_game_log_parser.game_stats[1]["opponent"] == "NYK")
		self.assertTrue(self.team_game_log_parser.game_stats[1]["result"] == "L")
		self.assertTrue(self.team_game_log_parser.game_stats[1]["points"] == 104)
		self.assertTrue(self.team_game_log_parser.game_stats[1]["opp_points"] == 106)
		self.assertTrue(self.team_game_log_parser.game_stats[1]["field_goals"] == 39)
		self.assertTrue(self.team_game_log_parser.game_stats[1]["field_goal_attempts"] == 76)
		# self.assertTrue(self.team_game_log_parser.game_stats[0]["field_goal_pct"] == 93)
		self.assertTrue(self.team_game_log_parser.game_stats[1]["three_point_field_goals"] == 2)
		self.assertTrue(self.team_game_log_parser.game_stats[1]["three_point_field_goal_attempts"] == 5)
		self.assertTrue(self.team_game_log_parser.game_stats[1]["free_throws"] == 24)
		self.assertTrue(self.team_game_log_parser.game_stats[1]["free_throw_attempts"] == 31)
		self.assertTrue(self.team_game_log_parser.game_stats[1]["offensive_rebounds"] == 13)
		self.assertTrue(self.team_game_log_parser.game_stats[1]["total_rebounds"] == 41)
		self.assertTrue(self.team_game_log_parser.game_stats[1]["assists"] == 28)
		self.assertTrue(self.team_game_log_parser.game_stats[1]["steals"] == 7)
		self.assertTrue(self.team_game_log_parser.game_stats[1]["blocks"] == 5)
		self.assertTrue(self.team_game_log_parser.game_stats[1]["turnovers"] == 18)
		self.assertTrue(self.team_game_log_parser.game_stats[1]["personal_fouls"] == 28)
		self.assertTrue(self.team_game_log_parser.game_stats[1]["opp_field_goals"] == 35)
		self.assertTrue(self.team_game_log_parser.game_stats[1]["opp_field_goal_attempts"] == 74)
		# self.assertTrue(self.team_game_log_parser.game_stats[0]["opp_field_goal_pct"] == .442)
		self.assertTrue(self.team_game_log_parser.game_stats[1]["opp_three_point_field_goals"] == 9)
		self.assertTrue(self.team_game_log_parser.game_stats[1]["opp_three_point_field_goal_attempts"] == 20)
		self.assertTrue(self.team_game_log_parser.game_stats[1]["opp_free_throws"] == 27)
		self.assertTrue(self.team_game_log_parser.game_stats[1]["opp_free_throw_attempts"] == 34)
		self.assertTrue(self.team_game_log_parser.game_stats[1]["opp_offensive_rebounds"] == 8)
		self.assertTrue(self.team_game_log_parser.game_stats[1]["opp_total_rebounds"] == 31)
		self.assertTrue(self.team_game_log_parser.game_stats[1]["opp_assists"] == 17)
		self.assertTrue(self.team_game_log_parser.game_stats[1]["opp_steals"] == 9)
		self.assertTrue(self.team_game_log_parser.game_stats[1]["opp_blocks"] == 11)
		self.assertTrue(self.team_game_log_parser.game_stats[1]["opp_turnovers"] == 16)
		self.assertTrue(self.team_game_log_parser.game_stats[1]["opp_personal_fouls"] == 25)

		####################################
		# Game 66
		####################################
		self.assertTrue(self.team_game_log_parser.game_stats[66]["date"] == "2012-04-26")
		self.assertTrue(self.team_game_log_parser.game_stats[66]["home"])
		self.assertTrue(self.team_game_log_parser.game_stats[66]["opponent"] == "MIL")
		self.assertTrue(self.team_game_log_parser.game_stats[66]["result"] == "W")
		self.assertTrue(self.team_game_log_parser.game_stats[66]["points"] == 87)
		self.assertTrue(self.team_game_log_parser.game_stats[66]["opp_points"] == 74)
		self.assertTrue(self.team_game_log_parser.game_stats[66]["field_goals"] == 35)
		self.assertTrue(self.team_game_log_parser.game_stats[66]["field_goal_attempts"] == 87)
		# self.assertTrue(self.team_game_log_parser.game_stats[0]["field_goal_pct"] == 93)
		self.assertTrue(self.team_game_log_parser.game_stats[66]["three_point_field_goals"] == 8)
		self.assertTrue(self.team_game_log_parser.game_stats[66]["three_point_field_goal_attempts"] == 24)
		self.assertTrue(self.team_game_log_parser.game_stats[66]["three_point_field_goal_pct"] == 0.333)
		self.assertTrue(self.team_game_log_parser.game_stats[66]["free_throws"] == 9)
		self.assertTrue(self.team_game_log_parser.game_stats[66]["free_throw_attempts"] == 11)
		self.assertTrue(self.team_game_log_parser.game_stats[66]["free_throw_pct"] == 0.818)
		self.assertTrue(self.team_game_log_parser.game_stats[66]["offensive_rebounds"] == 6)
		self.assertTrue(self.team_game_log_parser.game_stats[66]["total_rebounds"] == 44)
		self.assertTrue(self.team_game_log_parser.game_stats[66]["assists"] == 27)
		self.assertTrue(self.team_game_log_parser.game_stats[66]["steals"] == 14)
		self.assertTrue(self.team_game_log_parser.game_stats[66]["blocks"] == 7)
		self.assertTrue(self.team_game_log_parser.game_stats[66]["turnovers"] == 15)
		self.assertTrue(self.team_game_log_parser.game_stats[66]["personal_fouls"] == 18)
		self.assertTrue(self.team_game_log_parser.game_stats[66]["opp_field_goals"] == 29)
		self.assertTrue(self.team_game_log_parser.game_stats[66]["opp_field_goal_attempts"] == 78)
		self.assertTrue(self.team_game_log_parser.game_stats[66]["opp_field_goal_pct"] == .372)
		self.assertTrue(self.team_game_log_parser.game_stats[66]["opp_three_point_field_goals"] == 2)
		self.assertTrue(self.team_game_log_parser.game_stats[66]["opp_three_point_field_goal_attempts"] == 9)
		self.assertTrue(self.team_game_log_parser.game_stats[66]["opp_three_point_field_goal_pct"] == .222)
		self.assertTrue(self.team_game_log_parser.game_stats[66]["opp_free_throws"] == 14)
		self.assertTrue(self.team_game_log_parser.game_stats[66]["opp_free_throw_attempts"] == 23)
		self.assertTrue(self.team_game_log_parser.game_stats[66]["opp_free_throw_pct"] == .609)
		self.assertTrue(self.team_game_log_parser.game_stats[66]["opp_offensive_rebounds"] == 11)
		self.assertTrue(self.team_game_log_parser.game_stats[66]["opp_total_rebounds"] == 49)
		self.assertTrue(self.team_game_log_parser.game_stats[66]["opp_assists"] == 17)
		self.assertTrue(self.team_game_log_parser.game_stats[66]["opp_steals"] == 11)
		self.assertTrue(self.team_game_log_parser.game_stats[66]["opp_blocks"] == 4)
		self.assertTrue(self.team_game_log_parser.game_stats[66]["opp_turnovers"] == 23)
		self.assertTrue(self.team_game_log_parser.game_stats[66]["opp_personal_fouls"] == 14)


if __name__ == '__main__':
    unittest.main()