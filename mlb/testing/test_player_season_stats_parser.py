__author__ = 'dan'

from mlb.constants.mlb_constants import MLBConstants
from mlb.parsers.player_season_stats_parser import PlayerSeasonStatsParser

from bs4 import BeautifulSoup

import unittest


class TestPlayerSeasonStatsParser(unittest.TestCase):
	player_season_stat_parser = None

	def setUp(self):
		self.player_season_stat_parser = PlayerSeasonStatsParser()

	def tearDown(self):
		self.player_season_stat_parser = None

	def test_parse_pitcher(self):
		self.player_season_stat_parser.player_data = {MLBConstants.PLAYER_ID: "aardsda01"}
		self.player_season_stat_parser.parse(open('../test_files/season_stats_pitcher.html'))

		# Name and position
		self.assertTrue(self.player_season_stat_parser.player_data[MLBConstants.PLAYER_ID] == "aardsda01")
		self.assertTrue(self.player_season_stat_parser.player_data[MLBConstants.NAME] == "David Aardsma")
		self.assertTrue(self.player_season_stat_parser.player_data[MLBConstants.POSITION] == "Pitcher")

		###########################
		# Standard pitching table
		###########################
		self.assertTrue(self.player_season_stat_parser.player_data[MLBConstants.STANDARD_PITCHING]["2004"]
							[MLBConstants.AGE] == 22)
		self.assertTrue(self.player_season_stat_parser.player_data[MLBConstants.STANDARD_PITCHING]["2004"]
							[MLBConstants.TEAM] == "SFG")
		self.assertTrue(self.player_season_stat_parser.player_data[MLBConstants.STANDARD_PITCHING]["2004"]
							[MLBConstants.LEAGUE] == "NL")
		self.assertTrue(self.player_season_stat_parser.player_data[MLBConstants.STANDARD_PITCHING]["2004"]
							[MLBConstants.WINS] == 1)
		self.assertTrue(self.player_season_stat_parser.player_data[MLBConstants.STANDARD_PITCHING]["2004"]
							[MLBConstants.LOSSES] == 0)
		self.assertTrue(self.player_season_stat_parser.player_data[MLBConstants.STANDARD_PITCHING]["2004"]
							[MLBConstants.WIN_LOSS_PCT] == 1.0)
		self.assertTrue(self.player_season_stat_parser.player_data[MLBConstants.STANDARD_PITCHING]["2004"]
							[MLBConstants.ERA] == 6.75)
		self.assertTrue(self.player_season_stat_parser.player_data[MLBConstants.STANDARD_PITCHING]["2004"]
							[MLBConstants.GAMES] == 11)
		self.assertTrue(self.player_season_stat_parser.player_data[MLBConstants.STANDARD_PITCHING]["2004"]
							[MLBConstants.GAMES_STARTED] == 0)
		self.assertTrue(self.player_season_stat_parser.player_data[MLBConstants.STANDARD_PITCHING]["2004"]
							[MLBConstants.GAMES_FINISHED] == 5)
		self.assertTrue(self.player_season_stat_parser.player_data[MLBConstants.STANDARD_PITCHING]["2004"]
							[MLBConstants.COMPLETE_GAMES] == 0)
		self.assertTrue(self.player_season_stat_parser.player_data[MLBConstants.STANDARD_PITCHING]["2004"]
							[MLBConstants.SHUT_OUTS] == 0)
		self.assertTrue(self.player_season_stat_parser.player_data[MLBConstants.STANDARD_PITCHING]["2004"]
							[MLBConstants.SAVES] == 0)
		self.assertTrue(self.player_season_stat_parser.player_data[MLBConstants.STANDARD_PITCHING]["2004"]
							[MLBConstants.INNINGS_PITCHED] == 10.2)
		self.assertTrue(self.player_season_stat_parser.player_data[MLBConstants.STANDARD_PITCHING]["2004"]
							[MLBConstants.HITS] == 20)
		self.assertTrue(self.player_season_stat_parser.player_data[MLBConstants.STANDARD_PITCHING]["2004"]
							[MLBConstants.RUNS] == 8)
		self.assertTrue(self.player_season_stat_parser.player_data[MLBConstants.STANDARD_PITCHING]["2004"]
							[MLBConstants.EARNED_RUNS] == 8)
		self.assertTrue(self.player_season_stat_parser.player_data[MLBConstants.STANDARD_PITCHING]["2004"]
							[MLBConstants.HOME_RUNS] == 1)
		self.assertTrue(self.player_season_stat_parser.player_data[MLBConstants.STANDARD_PITCHING]["2004"]
							[MLBConstants.WALKS] == 10)
		self.assertTrue(self.player_season_stat_parser.player_data[MLBConstants.STANDARD_PITCHING]["2004"]
							[MLBConstants.INTENTIONAL_WALKS] == 0)
		self.assertTrue(self.player_season_stat_parser.player_data[MLBConstants.STANDARD_PITCHING]["2004"]
							[MLBConstants.STRIKE_OUTS] == 5)
		self.assertTrue(self.player_season_stat_parser.player_data[MLBConstants.STANDARD_PITCHING]["2004"]
							[MLBConstants.HIT_BY_PITCH] == 2)
		self.assertTrue(self.player_season_stat_parser.player_data[MLBConstants.STANDARD_PITCHING]["2004"]
							[MLBConstants.BALKS] == 0)
		self.assertTrue(self.player_season_stat_parser.player_data[MLBConstants.STANDARD_PITCHING]["2004"]
							[MLBConstants.WILD_PITCHES] == 0)
		self.assertTrue(self.player_season_stat_parser.player_data[MLBConstants.STANDARD_PITCHING]["2004"]
							[MLBConstants.BATTERS_FACED] == 61)
		self.assertTrue(self.player_season_stat_parser.player_data[MLBConstants.STANDARD_PITCHING]["2004"]
							[MLBConstants.ERA_PLUS] == 67)
		self.assertTrue(self.player_season_stat_parser.player_data[MLBConstants.STANDARD_PITCHING]["2004"]
							[MLBConstants.WHIP] == 2.813)
		self.assertTrue(self.player_season_stat_parser.player_data[MLBConstants.STANDARD_PITCHING]["2004"]
							[MLBConstants.HITS_PER_9_INNINGS] == 16.9)
		self.assertTrue(self.player_season_stat_parser.player_data[MLBConstants.STANDARD_PITCHING]["2004"]
							[MLBConstants.HOME_RUNS_PER_9_INNINGS] == 0.8)
		self.assertTrue(self.player_season_stat_parser.player_data[MLBConstants.STANDARD_PITCHING]["2004"]
							[MLBConstants.WALKS_PER_9_INNINGS] == 8.4)
		self.assertTrue(self.player_season_stat_parser.player_data[MLBConstants.STANDARD_PITCHING]["2004"]
							[MLBConstants.STRIKE_OUTS_PER_9_INNINGS] == 4.2)
		self.assertTrue(self.player_season_stat_parser.player_data[MLBConstants.STANDARD_PITCHING]["2004"]
							[MLBConstants.STRIKE_OUT_TO_WALK_RATIO] == 0.5)


		self.assertTrue(self.player_season_stat_parser.player_data[MLBConstants.STANDARD_PITCHING]["2013"]
							[MLBConstants.AGE] == 31)
		self.assertTrue(self.player_season_stat_parser.player_data[MLBConstants.STANDARD_PITCHING]["2013"]
							[MLBConstants.TEAM] == "NYM")
		self.assertTrue(self.player_season_stat_parser.player_data[MLBConstants.STANDARD_PITCHING]["2013"]
							[MLBConstants.LEAGUE] == "NL")
		self.assertTrue(self.player_season_stat_parser.player_data[MLBConstants.STANDARD_PITCHING]["2013"]
							[MLBConstants.WINS] == 2)
		self.assertTrue(self.player_season_stat_parser.player_data[MLBConstants.STANDARD_PITCHING]["2013"]
							[MLBConstants.LOSSES] == 2)
		self.assertTrue(self.player_season_stat_parser.player_data[MLBConstants.STANDARD_PITCHING]["2013"]
							[MLBConstants.WIN_LOSS_PCT] == 0.5)
		self.assertTrue(self.player_season_stat_parser.player_data[MLBConstants.STANDARD_PITCHING]["2013"]
							[MLBConstants.ERA] == 4.31)
		self.assertTrue(self.player_season_stat_parser.player_data[MLBConstants.STANDARD_PITCHING]["2013"]
							[MLBConstants.GAMES] == 43)
		self.assertTrue(self.player_season_stat_parser.player_data[MLBConstants.STANDARD_PITCHING]["2013"]
							[MLBConstants.GAMES_STARTED] == 0)
		self.assertTrue(self.player_season_stat_parser.player_data[MLBConstants.STANDARD_PITCHING]["2013"]
							[MLBConstants.GAMES_FINISHED] == 7)
		self.assertTrue(self.player_season_stat_parser.player_data[MLBConstants.STANDARD_PITCHING]["2013"]
							[MLBConstants.COMPLETE_GAMES] == 0)
		self.assertTrue(self.player_season_stat_parser.player_data[MLBConstants.STANDARD_PITCHING]["2013"]
							[MLBConstants.SHUT_OUTS] == 0)
		self.assertTrue(self.player_season_stat_parser.player_data[MLBConstants.STANDARD_PITCHING]["2013"]
							[MLBConstants.SAVES] == 0)
		self.assertTrue(self.player_season_stat_parser.player_data[MLBConstants.STANDARD_PITCHING]["2013"]
							[MLBConstants.INNINGS_PITCHED] == 39.2)
		self.assertTrue(self.player_season_stat_parser.player_data[MLBConstants.STANDARD_PITCHING]["2013"]
							[MLBConstants.HITS] == 39)
		self.assertTrue(self.player_season_stat_parser.player_data[MLBConstants.STANDARD_PITCHING]["2013"]
							[MLBConstants.RUNS] == 20)
		self.assertTrue(self.player_season_stat_parser.player_data[MLBConstants.STANDARD_PITCHING]["2013"]
							[MLBConstants.EARNED_RUNS] == 19)
		self.assertTrue(self.player_season_stat_parser.player_data[MLBConstants.STANDARD_PITCHING]["2013"]
							[MLBConstants.HOME_RUNS] == 7)
		self.assertTrue(self.player_season_stat_parser.player_data[MLBConstants.STANDARD_PITCHING]["2013"]
							[MLBConstants.WALKS] == 19)
		self.assertTrue(self.player_season_stat_parser.player_data[MLBConstants.STANDARD_PITCHING]["2013"]
							[MLBConstants.INTENTIONAL_WALKS] == 6)
		self.assertTrue(self.player_season_stat_parser.player_data[MLBConstants.STANDARD_PITCHING]["2013"]
							[MLBConstants.STRIKE_OUTS] == 36)
		self.assertTrue(self.player_season_stat_parser.player_data[MLBConstants.STANDARD_PITCHING]["2013"]
							[MLBConstants.HIT_BY_PITCH] == 4)
		self.assertTrue(self.player_season_stat_parser.player_data[MLBConstants.STANDARD_PITCHING]["2013"]
							[MLBConstants.BALKS] == 1)
		self.assertTrue(self.player_season_stat_parser.player_data[MLBConstants.STANDARD_PITCHING]["2013"]
							[MLBConstants.WILD_PITCHES] == 1)
		self.assertTrue(self.player_season_stat_parser.player_data[MLBConstants.STANDARD_PITCHING]["2013"]
							[MLBConstants.BATTERS_FACED] == 178)
		self.assertTrue(self.player_season_stat_parser.player_data[MLBConstants.STANDARD_PITCHING]["2013"]
							[MLBConstants.ERA_PLUS] == 83)
		self.assertTrue(self.player_season_stat_parser.player_data[MLBConstants.STANDARD_PITCHING]["2013"]
							[MLBConstants.WHIP] == 1.462)
		self.assertTrue(self.player_season_stat_parser.player_data[MLBConstants.STANDARD_PITCHING]["2013"]
							[MLBConstants.HITS_PER_9_INNINGS] == 8.8)
		self.assertTrue(self.player_season_stat_parser.player_data[MLBConstants.STANDARD_PITCHING]["2013"]
							[MLBConstants.HOME_RUNS_PER_9_INNINGS] == 1.6)
		self.assertTrue(self.player_season_stat_parser.player_data[MLBConstants.STANDARD_PITCHING]["2013"]
							[MLBConstants.WALKS_PER_9_INNINGS] == 4.3)
		self.assertTrue(self.player_season_stat_parser.player_data[MLBConstants.STANDARD_PITCHING]["2013"]
							[MLBConstants.STRIKE_OUTS_PER_9_INNINGS] == 8.2)
		self.assertTrue(self.player_season_stat_parser.player_data[MLBConstants.STANDARD_PITCHING]["2013"]
							[MLBConstants.STRIKE_OUT_TO_WALK_RATIO] == 1.89)

	def test_parse_player_value_pitchers(self):
		soup = BeautifulSoup(open('../test_files/season_stats_pitcher.html'))

		self.player_season_stat_parser.player_data = {}
		self.player_season_stat_parser.parse_player_value_pitchers(soup)

		self.assertTrue(self.player_season_stat_parser.player_data[MLBConstants.PLAYER_VALUE_PITCHING]["2004"]
							[MLBConstants.RUNS_ALLOWED_PER_9_INNINGS] == 6.75)
		self.assertTrue(self.player_season_stat_parser.player_data[MLBConstants.PLAYER_VALUE_PITCHING]["2004"]
							[MLBConstants.RUNS_ALLOWED_PER_9_INNINGS_OPP] == 5.02)
		self.assertTrue(self.player_season_stat_parser.player_data[MLBConstants.PLAYER_VALUE_PITCHING]["2004"]
							[MLBConstants.RUNS_PER_9_INNINGS_IN_SUPPORT_FROM_DEFENSE] == -0.37)
		self.assertTrue(self.player_season_stat_parser.player_data[MLBConstants.PLAYER_VALUE_PITCHING]["2004"]
							[MLBConstants.RUNS_PER_9_INNINGS_BY_ROLE] == -0.37)
		self.assertTrue(self.player_season_stat_parser.player_data[MLBConstants.PLAYER_VALUE_PITCHING]["2004"]
							[MLBConstants.PARK_FACTORS] == 99.2)
		self.assertTrue(self.player_season_stat_parser.player_data[MLBConstants.PLAYER_VALUE_PITCHING]["2004"]
							[MLBConstants.RUNS_PER_9_INNINGS_FOR_AVG_PITCHER] == 4.98)
		self.assertTrue(self.player_season_stat_parser.player_data[MLBConstants.PLAYER_VALUE_PITCHING]["2004"]
							[MLBConstants.RUNS_BETTER_THAN_AVG] == -2)
		self.assertTrue(self.player_season_stat_parser.player_data[MLBConstants.PLAYER_VALUE_PITCHING]["2004"]
							[MLBConstants.WINS_ABOVE_AVG] == -0.2)
		self.assertTrue(self.player_season_stat_parser.player_data[MLBConstants.PLAYER_VALUE_PITCHING]["2004"]
							[MLBConstants.GAME_ENTERING_LEVERAGE_INDEX] == 1.1)
		self.assertTrue(self.player_season_stat_parser.player_data[MLBConstants.PLAYER_VALUE_PITCHING]["2004"]
							[MLBConstants.WINS_ABOVE_AVG_ADJUSTMENT] == 0.0)
		self.assertTrue(self.player_season_stat_parser.player_data[MLBConstants.PLAYER_VALUE_PITCHING]["2004"]
							[MLBConstants.WINS_ABOVE_REPLACEMENT] == -0.2)
		self.assertTrue(self.player_season_stat_parser.player_data[MLBConstants.PLAYER_VALUE_PITCHING]["2004"]
							[MLBConstants.RUNS_BETTER_THAN_REPLACEMENT] == -1)
		self.assertTrue(self.player_season_stat_parser.player_data[MLBConstants.PLAYER_VALUE_PITCHING]["2004"]
							[MLBConstants.WIN_LOSS_PCT_WITH_AVG_TEAM] == .480)
		self.assertTrue(self.player_season_stat_parser.player_data[MLBConstants.PLAYER_VALUE_PITCHING]["2004"]
							[MLBConstants.WIN_LOSS_PCT_WITH_AVG_TEAM_SEASON] == .499)
		self.assertTrue(self.player_season_stat_parser.player_data[MLBConstants.PLAYER_VALUE_PITCHING]["2004"]
							[MLBConstants.SALARY] == 300000)

		self.assertTrue(self.player_season_stat_parser.player_data[MLBConstants.PLAYER_VALUE_PITCHING]["2013"]
							[MLBConstants.RUNS_ALLOWED_PER_9_INNINGS] == 4.54)
		self.assertTrue(self.player_season_stat_parser.player_data[MLBConstants.PLAYER_VALUE_PITCHING]["2013"]
							[MLBConstants.RUNS_ALLOWED_PER_9_INNINGS_OPP] == 4.14)
		self.assertTrue(self.player_season_stat_parser.player_data[MLBConstants.PLAYER_VALUE_PITCHING]["2013"]
							[MLBConstants.RUNS_PER_9_INNINGS_IN_SUPPORT_FROM_DEFENSE] == -0.04)
		self.assertTrue(self.player_season_stat_parser.player_data[MLBConstants.PLAYER_VALUE_PITCHING]["2013"]
							[MLBConstants.RUNS_PER_9_INNINGS_BY_ROLE] == -0.31)
		self.assertTrue(self.player_season_stat_parser.player_data[MLBConstants.PLAYER_VALUE_PITCHING]["2013"]
							[MLBConstants.PARK_FACTORS] == 92.9)
		self.assertTrue(self.player_season_stat_parser.player_data[MLBConstants.PLAYER_VALUE_PITCHING]["2013"]
							[MLBConstants.RUNS_PER_9_INNINGS_FOR_AVG_PITCHER] == 3.6)
		self.assertTrue(self.player_season_stat_parser.player_data[MLBConstants.PLAYER_VALUE_PITCHING]["2013"]
							[MLBConstants.RUNS_BETTER_THAN_AVG] == -4)
		self.assertTrue(self.player_season_stat_parser.player_data[MLBConstants.PLAYER_VALUE_PITCHING]["2013"]
							[MLBConstants.WINS_ABOVE_AVG] == -0.4)
		self.assertTrue(self.player_season_stat_parser.player_data[MLBConstants.PLAYER_VALUE_PITCHING]["2013"]
							[MLBConstants.GAME_ENTERING_LEVERAGE_INDEX] == 0.8)
		self.assertTrue(self.player_season_stat_parser.player_data[MLBConstants.PLAYER_VALUE_PITCHING]["2013"]
							[MLBConstants.WINS_ABOVE_AVG_ADJUSTMENT] == -0.1)
		self.assertTrue(self.player_season_stat_parser.player_data[MLBConstants.PLAYER_VALUE_PITCHING]["2013"]
							[MLBConstants.WINS_ABOVE_REPLACEMENT] == -0.2)
		self.assertTrue(self.player_season_stat_parser.player_data[MLBConstants.PLAYER_VALUE_PITCHING]["2013"]
							[MLBConstants.RUNS_BETTER_THAN_REPLACEMENT] == -1)
		self.assertTrue(self.player_season_stat_parser.player_data[MLBConstants.PLAYER_VALUE_PITCHING]["2013"]
							[MLBConstants.WIN_LOSS_PCT_WITH_AVG_TEAM] == .490)
		self.assertTrue(self.player_season_stat_parser.player_data[MLBConstants.PLAYER_VALUE_PITCHING]["2013"]
							[MLBConstants.WIN_LOSS_PCT_WITH_AVG_TEAM_SEASON] == .497)
		self.assertTrue(self.player_season_stat_parser.player_data[MLBConstants.PLAYER_VALUE_PITCHING]["2013"]
							[MLBConstants.SALARY] == 0)


if __name__ == '__main__':
	unittest.main()