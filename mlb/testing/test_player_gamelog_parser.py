import unittest

from time import strftime
from mlb.constants.mlb_constants import MLBConstants

from mlb.parsers.player_gamelog_parser import PlayerGamelogParser

__author__ = 'dan'


class TestPlayerGamelogParser(unittest.TestCase):
	def setUp(self):
		self.player_gamelog_parser = PlayerGamelogParser()

	def tearDown(self):
		self.player_gamelog_parser = None

	def test_parse_pitcher(self):
		self.player_gamelog_parser.season = "2013"
		self.player_gamelog_parser.type = MLBConstants.PITCHER_TYPE
		self.player_gamelog_parser.player_data = {MLBConstants.PLAYER_ID: "aardsda01"}
		self.player_gamelog_parser.parse(open('../test_files/gamelog_pitcher.html'))

		self.assertTrue(strftime("%b %d %Y", self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_PITCHING]["2013"]["57"][MLBConstants.DATE]) == "Jun 08 2013")
		self.assertTrue(self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_PITCHING]["2013"]["57"][
								MLBConstants.TEAM] == "NYM")
		self.assertTrue(self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_PITCHING]["2013"]["57"][
								MLBConstants.OPPONENT] == "MIA")
		self.assertTrue(self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_PITCHING]["2013"]["57"][
								MLBConstants.HOME_GAME])
		self.assertTrue(self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_PITCHING]["2013"]["57"][
								MLBConstants.RESULT] == "L")
		self.assertTrue(self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_PITCHING]["2013"]["57"][
								MLBConstants.TEAM_SCORE] == 1)
		self.assertTrue(self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_PITCHING]["2013"]["57"][
								MLBConstants.OPPONENT_SCORE] == 2)
		self.assertTrue(self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_PITCHING]["2013"]["57"][
								MLBConstants.INNINGS] == "12-12")
		self.assertTrue(self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_PITCHING]["2013"]["57"][
								MLBConstants.DECISION] == "")
		self.assertTrue(self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_PITCHING]["2013"]["57"][
								MLBConstants.DAYS_REST] == 99)
		self.assertTrue(self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_PITCHING]["2013"]["57"][
								MLBConstants.INNINGS_PITCHED] == 1)
		self.assertTrue(self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_PITCHING]["2013"]["57"][
								MLBConstants.HITS] == 0)
		self.assertTrue(self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_PITCHING]["2013"]["57"][
								MLBConstants.RUNS] == 0)
		self.assertTrue(self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_PITCHING]["2013"]["57"][
								MLBConstants.EARNED_RUNS] == 0)
		self.assertTrue(self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_PITCHING]["2013"]["57"][
								MLBConstants.WALKS] == 0)
		self.assertTrue(self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_PITCHING]["2013"]["57"][
								MLBConstants.STRIKE_OUTS] == 1)
		self.assertTrue(self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_PITCHING]["2013"]["57"][
								MLBConstants.HOME_RUNS] == 0)
		self.assertTrue(self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_PITCHING]["2013"]["57"][
								MLBConstants.HIT_BY_PITCH] == 0)
		self.assertTrue(self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_PITCHING]["2013"]["57"][
								MLBConstants.ERA] == 0.0)
		self.assertTrue(self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_PITCHING]["2013"]["57"][
								MLBConstants.BATTERS_FACED] == 3)
		self.assertTrue(self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_PITCHING]["2013"]["57"][
								MLBConstants.NUM_PITCHES] == 14)
		self.assertTrue(self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_PITCHING]["2013"]["57"][
								MLBConstants.STRIKES] == 9)
		self.assertTrue(self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_PITCHING]["2013"]["57"][
								MLBConstants.STRIKES_LOOKING] == 2)
		self.assertTrue(self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_PITCHING]["2013"]["57"][
								MLBConstants.STRIKES_SWINGING] == 2)
		self.assertTrue(self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_PITCHING]["2013"]["57"][
								MLBConstants.GROUND_BALLS] == 1)
		self.assertTrue(self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_PITCHING]["2013"]["57"][
								MLBConstants.FLY_BALLS] == 1)
		self.assertTrue(self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_PITCHING]["2013"]["57"][
								MLBConstants.LINE_DRIVES] == 0)
		self.assertTrue(self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_PITCHING]["2013"]["57"][
								MLBConstants.POP_UPS] == 0)
		self.assertTrue(self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_PITCHING]["2013"]["57"][
								MLBConstants.UNKNOWN_BATTED_BALLS] == 0)
		self.assertTrue(self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_PITCHING]["2013"]["57"][
								MLBConstants.PLAYER_GAME_SCORE] == "")
		self.assertTrue(self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_PITCHING]["2013"]["57"][
								MLBConstants.INHERITED_RUNNERS] == 0)
		self.assertTrue(self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_PITCHING]["2013"]["57"][
								MLBConstants.INHERITED_SCORE] == 0)
		self.assertTrue(self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_PITCHING]["2013"]["57"][
								MLBConstants.STOLEN_BASES] == 0)
		self.assertTrue(self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_PITCHING]["2013"]["57"][
								MLBConstants.CAUGHT_STEALING] == 0)
		self.assertTrue(self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_PITCHING]["2013"]["57"][
								MLBConstants.PICK_OFFS] == 0)
		self.assertTrue(self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_PITCHING]["2013"]["57"][
								MLBConstants.AT_BATS] == 3)
		self.assertTrue(self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_PITCHING]["2013"]["57"][
								MLBConstants.DOUBLES] == 0)
		self.assertTrue(self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_PITCHING]["2013"]["57"][
								MLBConstants.TRIPLES] == 0)
		self.assertTrue(self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_PITCHING]["2013"]["57"][
								MLBConstants.INTENTIONAL_WALKS] == 0)
		self.assertTrue(self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_PITCHING]["2013"]["57"][
								MLBConstants.DOUBLE_PLAYS_GROUNDED_INTO] == 0)
		self.assertTrue(self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_PITCHING]["2013"]["57"][
								MLBConstants.SACRIFICE_FLIES] == 0)
		self.assertTrue(self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_PITCHING]["2013"]["57"][
								MLBConstants.REACHED_ON_ERROR] == 0)
		self.assertTrue(self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_PITCHING]["2013"]["57"][
								MLBConstants.AVERAGE_LEVERAGE_INDEX] == 1.67)
		self.assertTrue(self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_PITCHING]["2013"]["57"][
								MLBConstants.WIN_PROBABILITY_ADDED_BY_PITCHER] == 0.12)
		self.assertTrue(self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_PITCHING]["2013"]["57"][
								MLBConstants.BASE_OUT_RUNS_SAVED] == 0.42)
		self.assertTrue(self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_PITCHING]["2013"]["57"][
								MLBConstants.ENTRY_SITUATION] == "12t --- 0 out tie")
		self.assertTrue(self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_PITCHING]["2013"]["57"][
								MLBConstants.EXIT_SITUATION] == "12t 3 out tie")

		# Game 161
		self.assertTrue(strftime("%b %d %Y", self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_PITCHING]["2013"]["161"][MLBConstants.DATE]) == "Sep 28 2013")
		self.assertTrue(self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_PITCHING]["2013"]["161"][
								MLBConstants.TEAM] == "NYM")
		self.assertTrue(self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_PITCHING]["2013"]["161"][
								MLBConstants.OPPONENT] == "MIL")
		self.assertTrue(self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_PITCHING]["2013"]["161"][
								MLBConstants.HOME_GAME])
		self.assertTrue(self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_PITCHING]["2013"]["161"][
								MLBConstants.RESULT] == "L")
		self.assertTrue(self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_PITCHING]["2013"]["161"][
								MLBConstants.TEAM_SCORE] == 2)
		self.assertTrue(self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_PITCHING]["2013"]["161"][
								MLBConstants.OPPONENT_SCORE] == 4)
		self.assertTrue(self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_PITCHING]["2013"]["161"][
								MLBConstants.INNINGS] == "7-7")
		self.assertTrue(self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_PITCHING]["2013"]["161"][
								MLBConstants.DECISION] == "")
		self.assertTrue(self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_PITCHING]["2013"]["161"][
								MLBConstants.DAYS_REST] == 1)
		self.assertTrue(self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_PITCHING]["2013"]["161"][
								MLBConstants.INNINGS_PITCHED] == 0.1)
		self.assertTrue(self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_PITCHING]["2013"]["161"][
								MLBConstants.HITS] == 1)
		self.assertTrue(self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_PITCHING]["2013"]["161"][
								MLBConstants.RUNS] == 0)
		self.assertTrue(self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_PITCHING]["2013"]["161"][
								MLBConstants.EARNED_RUNS] == 0)
		self.assertTrue(self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_PITCHING]["2013"]["161"][
								MLBConstants.WALKS] == 0)
		self.assertTrue(self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_PITCHING]["2013"]["161"][
								MLBConstants.STRIKE_OUTS] == 0)
		self.assertTrue(self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_PITCHING]["2013"]["161"][
								MLBConstants.HOME_RUNS] == 0)
		self.assertTrue(self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_PITCHING]["2013"]["161"][
								MLBConstants.HIT_BY_PITCH] == 0)
		self.assertTrue(self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_PITCHING]["2013"]["161"][
								MLBConstants.ERA] == 4.31)
		self.assertTrue(self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_PITCHING]["2013"]["161"][
								MLBConstants.BATTERS_FACED] == 2)
		self.assertTrue(self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_PITCHING]["2013"]["161"][
								MLBConstants.NUM_PITCHES] == 7)
		self.assertTrue(self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_PITCHING]["2013"]["161"][
								MLBConstants.STRIKES] == 5)
		self.assertTrue(self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_PITCHING]["2013"]["161"][
								MLBConstants.STRIKES_LOOKING] == 1)
		self.assertTrue(self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_PITCHING]["2013"]["161"][
								MLBConstants.STRIKES_SWINGING] == 1)
		self.assertTrue(self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_PITCHING]["2013"]["161"][
								MLBConstants.GROUND_BALLS] == 0)
		self.assertTrue(self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_PITCHING]["2013"]["161"][
								MLBConstants.FLY_BALLS] == 2)
		self.assertTrue(self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_PITCHING]["2013"]["161"][
								MLBConstants.LINE_DRIVES] == 2)
		self.assertTrue(self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_PITCHING]["2013"]["161"][
								MLBConstants.POP_UPS] == 0)
		self.assertTrue(self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_PITCHING]["2013"]["161"][
								MLBConstants.UNKNOWN_BATTED_BALLS] == 0)
		self.assertTrue(self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_PITCHING]["2013"]["161"][
								MLBConstants.PLAYER_GAME_SCORE] == "")
		self.assertTrue(self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_PITCHING]["2013"]["161"][
								MLBConstants.INHERITED_RUNNERS] == 0)
		self.assertTrue(self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_PITCHING]["2013"]["161"][
								MLBConstants.INHERITED_SCORE] == 0)
		self.assertTrue(self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_PITCHING]["2013"]["161"][
								MLBConstants.STOLEN_BASES] == 0)
		self.assertTrue(self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_PITCHING]["2013"]["161"][
								MLBConstants.CAUGHT_STEALING] == 0)
		self.assertTrue(self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_PITCHING]["2013"]["161"][
								MLBConstants.PICK_OFFS] == 0)
		self.assertTrue(self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_PITCHING]["2013"]["161"][
								MLBConstants.AT_BATS] == 2)
		self.assertTrue(self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_PITCHING]["2013"]["161"][
								MLBConstants.DOUBLES] == 0)
		self.assertTrue(self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_PITCHING]["2013"]["161"][
								MLBConstants.TRIPLES] == 0)
		self.assertTrue(self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_PITCHING]["2013"]["161"][
								MLBConstants.INTENTIONAL_WALKS] == 0)
		self.assertTrue(self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_PITCHING]["2013"]["161"][
								MLBConstants.DOUBLE_PLAYS_GROUNDED_INTO] == 0)
		self.assertTrue(self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_PITCHING]["2013"]["161"][
								MLBConstants.SACRIFICE_FLIES] == 0)
		self.assertTrue(self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_PITCHING]["2013"]["161"][
								MLBConstants.REACHED_ON_ERROR] == 0)
		self.assertTrue(self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_PITCHING]["2013"]["161"][
								MLBConstants.AVERAGE_LEVERAGE_INDEX] == 1.09)
		self.assertTrue(self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_PITCHING]["2013"]["161"][
								MLBConstants.WIN_PROBABILITY_ADDED_BY_PITCHER] == 0.018)
		self.assertTrue(self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_PITCHING]["2013"]["161"][
								MLBConstants.BASE_OUT_RUNS_SAVED] == 0.08)
		self.assertTrue(self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_PITCHING]["2013"]["161"][
								MLBConstants.ENTRY_SITUATION] == "7t --- 2 out tie")
		self.assertTrue(self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_PITCHING]["2013"]["161"][
								MLBConstants.EXIT_SITUATION] == "7t 3 out tie")

	def test_parse_batter(self):
		self.player_gamelog_parser.season = "2013"
		self.player_gamelog_parser.type = MLBConstants.BATTER_TYPE
		self.player_gamelog_parser.player_data = {MLBConstants.PLAYER_ID: "cabremi01"}
		self.player_gamelog_parser.parse(open('../test_files/gamelog_batter.html'))

		self.assertTrue(strftime("%b %d %Y", self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_BATTING]["2013"]["1"][MLBConstants.DATE]) == "Apr 01 2013")
		self.assertTrue(self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_BATTING]["2013"]["1"][
								MLBConstants.TEAM] == "DET")
		self.assertTrue(self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_BATTING]["2013"]["1"][
								MLBConstants.OPPONENT] == "MIN")
		self.assertTrue(not self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_BATTING]["2013"]["1"][
								MLBConstants.HOME_GAME])
		self.assertTrue(self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_BATTING]["2013"]["1"][
								MLBConstants.RESULT] == "W")
		self.assertTrue(self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_BATTING]["2013"]["1"][
								MLBConstants.TEAM_SCORE] == 4)
		self.assertTrue(self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_BATTING]["2013"]["1"][
								MLBConstants.OPPONENT_SCORE] == 2)
		self.assertTrue(self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_BATTING]["2013"]["1"][
								MLBConstants.INNINGS] == "CG")
		self.assertTrue(self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_BATTING]["2013"]["1"][
								MLBConstants.PLATE_APPEARANCES] == 5)
		self.assertTrue(self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_BATTING]["2013"]["1"][
								MLBConstants.AT_BATS] == 5)
		self.assertTrue(self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_BATTING]["2013"]["1"][
								MLBConstants.RUNS] == 1)
		self.assertTrue(self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_BATTING]["2013"]["1"][
								MLBConstants.HITS] == 0)
		self.assertTrue(self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_BATTING]["2013"]["1"][
								MLBConstants.DOUBLES] == 0)
		self.assertTrue(self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_BATTING]["2013"]["1"][
								MLBConstants.TRIPLES] == 0)
		self.assertTrue(self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_BATTING]["2013"]["1"][
								MLBConstants.HOME_RUNS] == 0)
		self.assertTrue(self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_BATTING]["2013"]["1"][
								MLBConstants.RBI] == 1)
		self.assertTrue(self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_BATTING]["2013"]["1"][
								MLBConstants.WALKS] == 0)
		self.assertTrue(self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_BATTING]["2013"]["1"][
								MLBConstants.INTENTIONAL_WALKS] == 0)
		self.assertTrue(self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_BATTING]["2013"]["1"][
								MLBConstants.STRIKE_OUTS] == 2)
		self.assertTrue(self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_BATTING]["2013"]["1"][
								MLBConstants.HIT_BY_PITCH] == 0)
		self.assertTrue(self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_BATTING]["2013"]["1"][
								MLBConstants.SACRIFICE_HITS] == 0)
		self.assertTrue(self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_BATTING]["2013"]["1"][
								MLBConstants.SACRIFICE_FLIES] == 0)
		self.assertTrue(self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_BATTING]["2013"]["1"][
								MLBConstants.REACHED_ON_ERROR] == 0)
		self.assertTrue(self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_BATTING]["2013"]["1"][
								MLBConstants.DOUBLE_PLAYS_GROUNDED_INTO] == 0)
		self.assertTrue(self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_BATTING]["2013"]["1"][
								MLBConstants.STOLEN_BASES] == 0)
		self.assertTrue(self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_BATTING]["2013"]["1"][
								MLBConstants.CAUGHT_STEALING] == 0)
		self.assertTrue(self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_BATTING]["2013"]["1"][
								MLBConstants.BATTING_AVERAGE] == 0.0)
		self.assertTrue(self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_BATTING]["2013"]["1"][
								MLBConstants.ON_BASE_PERCENTAGE] == 0.0)
		self.assertTrue(self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_BATTING]["2013"]["1"][
								MLBConstants.SLUGGING_PERCENTAGE] == 0.0)
		self.assertTrue(self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_BATTING]["2013"]["1"][
								MLBConstants.OPS] == 0.0)
		self.assertTrue(self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_BATTING]["2013"]["1"][
								MLBConstants.BATTING_ORDER_POSITION] == 3)
		self.assertTrue(self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_BATTING]["2013"]["1"][
								MLBConstants.AVERAGE_LEVERAGE_INDEX] == .71)
		self.assertTrue(self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_BATTING]["2013"]["1"][
								MLBConstants.WIN_PROBABILITY_ADDED] == -0.037)
		self.assertTrue(self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_BATTING]["2013"]["1"][
								MLBConstants.BASE_OUT_RUNS_ADDED] == -0.76)
		self.assertTrue(self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_BATTING]["2013"]["1"][
								MLBConstants.POSITION] == "3B")

		# Game 161
		self.assertTrue(strftime("%b %d %Y", self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_BATTING]["2013"]["161"][MLBConstants.DATE]) == "Sep 28 2013")
		self.assertTrue(self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_BATTING]["2013"]["161"][
								MLBConstants.TEAM] == "DET")
		self.assertTrue(self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_BATTING]["2013"]["161"][
								MLBConstants.OPPONENT] == "MIA")
		self.assertTrue(not self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_BATTING]["2013"]["161"][
								MLBConstants.HOME_GAME])
		self.assertTrue(self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_BATTING]["2013"]["161"][
								MLBConstants.RESULT] == "L")
		self.assertTrue(self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_BATTING]["2013"]["161"][
								MLBConstants.TEAM_SCORE] == 1)
		self.assertTrue(self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_BATTING]["2013"]["161"][
								MLBConstants.OPPONENT_SCORE] == 2)
		self.assertTrue(self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_BATTING]["2013"]["161"][
								MLBConstants.INNINGS] == "GS-8")
		self.assertTrue(self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_BATTING]["2013"]["161"][
								MLBConstants.PLATE_APPEARANCES] == 4)
		self.assertTrue(self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_BATTING]["2013"]["161"][
								MLBConstants.AT_BATS] == 4)
		self.assertTrue(self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_BATTING]["2013"]["161"][
								MLBConstants.RUNS] == 0)
		self.assertTrue(self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_BATTING]["2013"]["161"][
								MLBConstants.HITS] == 2)
		self.assertTrue(self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_BATTING]["2013"]["161"][
								MLBConstants.DOUBLES] == 0)
		self.assertTrue(self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_BATTING]["2013"]["161"][
								MLBConstants.TRIPLES] == 0)
		self.assertTrue(self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_BATTING]["2013"]["161"][
								MLBConstants.HOME_RUNS] == 0)
		self.assertTrue(self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_BATTING]["2013"]["161"][
								MLBConstants.RBI] == 0)
		self.assertTrue(self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_BATTING]["2013"]["161"][
								MLBConstants.WALKS] == 0)
		self.assertTrue(self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_BATTING]["2013"]["161"][
								MLBConstants.INTENTIONAL_WALKS] == 0)
		self.assertTrue(self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_BATTING]["2013"]["161"][
								MLBConstants.STRIKE_OUTS] == 1)
		self.assertTrue(self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_BATTING]["2013"]["161"][
								MLBConstants.HIT_BY_PITCH] == 0)
		self.assertTrue(self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_BATTING]["2013"]["161"][
								MLBConstants.SACRIFICE_HITS] == 0)
		self.assertTrue(self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_BATTING]["2013"]["161"][
								MLBConstants.SACRIFICE_FLIES] == 0)
		self.assertTrue(self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_BATTING]["2013"]["161"][
								MLBConstants.REACHED_ON_ERROR] == 0)
		self.assertTrue(self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_BATTING]["2013"]["161"][
								MLBConstants.DOUBLE_PLAYS_GROUNDED_INTO] == 0)
		self.assertTrue(self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_BATTING]["2013"]["161"][
								MLBConstants.STOLEN_BASES] == 0)
		self.assertTrue(self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_BATTING]["2013"]["161"][
								MLBConstants.CAUGHT_STEALING] == 0)
		self.assertTrue(self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_BATTING]["2013"]["161"][
								MLBConstants.BATTING_AVERAGE] == 0.348)
		self.assertTrue(self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_BATTING]["2013"]["161"][
								MLBConstants.ON_BASE_PERCENTAGE] == 0.442)
		self.assertTrue(self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_BATTING]["2013"]["161"][
								MLBConstants.SLUGGING_PERCENTAGE] == 0.636)
		self.assertTrue(self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_BATTING]["2013"]["161"][
								MLBConstants.OPS] == 1.078)
		self.assertTrue(self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_BATTING]["2013"]["161"][
								MLBConstants.BATTING_ORDER_POSITION] == 3)
		self.assertTrue(self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_BATTING]["2013"]["161"][
								MLBConstants.AVERAGE_LEVERAGE_INDEX] == .82)
		self.assertTrue(self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_BATTING]["2013"]["161"][
								MLBConstants.WIN_PROBABILITY_ADDED] == 0.025)
		self.assertTrue(self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_BATTING]["2013"]["161"][
								MLBConstants.BASE_OUT_RUNS_ADDED] == 0.27)
		self.assertTrue(self.player_gamelog_parser.player_data[MLBConstants.PLAYER_GAMELOG_BATTING]["2013"]["161"][
								MLBConstants.POSITION] == "3B")

if __name__ == '__main__':
	unittest.main()