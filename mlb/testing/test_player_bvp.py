import unittest
from mlb.constants.mlb_constants import MLBConstants
from mlb.parsers.player_bvp_parser import PlayerBvPParser

__author__ = 'dan'


class TestPlayerBvPParser(unittest.TestCase):
	def setUp(self):
		self.player_bvp_parser = PlayerBvPParser()

	def tearDown(self):
		self.player_bvp_parser = None

	def test_parse_batter(self):
		self.player_bvp_parser.player_data = {MLBConstants.PLAYER_ID: "cabremi01"}
		self.player_bvp_parser.type = MLBConstants.BATTER_TYPE
		self.player_bvp_parser.parse(open('test_files/batter_bvp.html'))

		self.assertTrue(self.player_bvp_parser.player_data[MLBConstants.BATTER_VS_PITCHER]["hernali01"][MLBConstants.NAME] == "Livan Hernandez")
		self.assertTrue(self.player_bvp_parser.player_data[MLBConstants.BATTER_VS_PITCHER]["hernali01"][MLBConstants.PLATE_APPEARANCES] == 61)
		self.assertTrue(self.player_bvp_parser.player_data[MLBConstants.BATTER_VS_PITCHER]["hernali01"][MLBConstants.AT_BATS] == 56)
		self.assertTrue(self.player_bvp_parser.player_data[MLBConstants.BATTER_VS_PITCHER]["hernali01"][MLBConstants.HITS] == 15)
		self.assertTrue(self.player_bvp_parser.player_data[MLBConstants.BATTER_VS_PITCHER]["hernali01"][MLBConstants.DOUBLES] == 5)
		self.assertTrue(self.player_bvp_parser.player_data[MLBConstants.BATTER_VS_PITCHER]["hernali01"][MLBConstants.TRIPLES] == 0)
		self.assertTrue(self.player_bvp_parser.player_data[MLBConstants.BATTER_VS_PITCHER]["hernali01"][MLBConstants.HOME_RUNS] == 1)
		self.assertTrue(self.player_bvp_parser.player_data[MLBConstants.BATTER_VS_PITCHER]["hernali01"][MLBConstants.RBI] == 10)
		self.assertTrue(self.player_bvp_parser.player_data[MLBConstants.BATTER_VS_PITCHER]["hernali01"][MLBConstants.WALKS] == 4)
		self.assertTrue(self.player_bvp_parser.player_data[MLBConstants.BATTER_VS_PITCHER]["hernali01"][MLBConstants.STRIKE_OUTS] == 13)
		self.assertTrue(self.player_bvp_parser.player_data[MLBConstants.BATTER_VS_PITCHER]["hernali01"][MLBConstants.BATTING_AVERAGE] == 0.268)
		self.assertTrue(self.player_bvp_parser.player_data[MLBConstants.BATTER_VS_PITCHER]["hernali01"][MLBConstants.ON_BASE_PERCENTAGE] == 0.311)
		self.assertTrue(self.player_bvp_parser.player_data[MLBConstants.BATTER_VS_PITCHER]["hernali01"][MLBConstants.SLUGGING_PERCENTAGE] == 0.411)
		self.assertTrue(self.player_bvp_parser.player_data[MLBConstants.BATTER_VS_PITCHER]["hernali01"][MLBConstants.OPS] == 0.722)
		self.assertTrue(self.player_bvp_parser.player_data[MLBConstants.BATTER_VS_PITCHER]["hernali01"][MLBConstants.SACRIFICE_HITS] == 0)
		self.assertTrue(self.player_bvp_parser.player_data[MLBConstants.BATTER_VS_PITCHER]["hernali01"][MLBConstants.SACRIFICE_FLIES] == 1)
		self.assertTrue(self.player_bvp_parser.player_data[MLBConstants.BATTER_VS_PITCHER]["hernali01"][MLBConstants.INTENTIONAL_WALKS] == 0)
		self.assertTrue(self.player_bvp_parser.player_data[MLBConstants.BATTER_VS_PITCHER]["hernali01"][MLBConstants.HIT_BY_PITCH] == 0)
		self.assertTrue(self.player_bvp_parser.player_data[MLBConstants.BATTER_VS_PITCHER]["hernali01"][MLBConstants.DOUBLE_PLAYS_GROUNDED_INTO] == 0)

		self.assertTrue(self.player_bvp_parser.player_data[MLBConstants.BATTER_VS_PITCHER]["yabutya01"][MLBConstants.NAME] == "Yasuhiko Yabuta")
		self.assertTrue(self.player_bvp_parser.player_data[MLBConstants.BATTER_VS_PITCHER]["yabutya01"][MLBConstants.PLATE_APPEARANCES] == 1)
		self.assertTrue(self.player_bvp_parser.player_data[MLBConstants.BATTER_VS_PITCHER]["yabutya01"][MLBConstants.AT_BATS] == 1)
		self.assertTrue(self.player_bvp_parser.player_data[MLBConstants.BATTER_VS_PITCHER]["yabutya01"][MLBConstants.HITS] == 0)
		self.assertTrue(self.player_bvp_parser.player_data[MLBConstants.BATTER_VS_PITCHER]["yabutya01"][MLBConstants.DOUBLES] == 0)
		self.assertTrue(self.player_bvp_parser.player_data[MLBConstants.BATTER_VS_PITCHER]["yabutya01"][MLBConstants.TRIPLES] == 0)
		self.assertTrue(self.player_bvp_parser.player_data[MLBConstants.BATTER_VS_PITCHER]["yabutya01"][MLBConstants.HOME_RUNS] == 0)
		self.assertTrue(self.player_bvp_parser.player_data[MLBConstants.BATTER_VS_PITCHER]["yabutya01"][MLBConstants.RBI] == 0)
		self.assertTrue(self.player_bvp_parser.player_data[MLBConstants.BATTER_VS_PITCHER]["yabutya01"][MLBConstants.WALKS] == 0)
		self.assertTrue(self.player_bvp_parser.player_data[MLBConstants.BATTER_VS_PITCHER]["yabutya01"][MLBConstants.STRIKE_OUTS] == 0)
		self.assertTrue(self.player_bvp_parser.player_data[MLBConstants.BATTER_VS_PITCHER]["yabutya01"][MLBConstants.BATTING_AVERAGE] == 0.0)
		self.assertTrue(self.player_bvp_parser.player_data[MLBConstants.BATTER_VS_PITCHER]["yabutya01"][MLBConstants.ON_BASE_PERCENTAGE] == 0.0)
		self.assertTrue(self.player_bvp_parser.player_data[MLBConstants.BATTER_VS_PITCHER]["yabutya01"][MLBConstants.SLUGGING_PERCENTAGE] == 0.0)
		self.assertTrue(self.player_bvp_parser.player_data[MLBConstants.BATTER_VS_PITCHER]["yabutya01"][MLBConstants.OPS] == 0.0)
		self.assertTrue(self.player_bvp_parser.player_data[MLBConstants.BATTER_VS_PITCHER]["yabutya01"][MLBConstants.SACRIFICE_HITS] == 0)
		self.assertTrue(self.player_bvp_parser.player_data[MLBConstants.BATTER_VS_PITCHER]["yabutya01"][MLBConstants.SACRIFICE_FLIES] == 0)
		self.assertTrue(self.player_bvp_parser.player_data[MLBConstants.BATTER_VS_PITCHER]["yabutya01"][MLBConstants.INTENTIONAL_WALKS] == 0)
		self.assertTrue(self.player_bvp_parser.player_data[MLBConstants.BATTER_VS_PITCHER]["yabutya01"][MLBConstants.HIT_BY_PITCH] == 0)
		self.assertTrue(self.player_bvp_parser.player_data[MLBConstants.BATTER_VS_PITCHER]["yabutya01"][MLBConstants.DOUBLE_PLAYS_GROUNDED_INTO] == 0)

	def test_parse_pitcher(self):
		self.player_bvp_parser.player_data = {MLBConstants.PLAYER_ID: "sabatc.01"}
		self.player_bvp_parser.type = MLBConstants.PITCHER_TYPE
		self.player_bvp_parser.parse(open('test_files/pitcher_bvp.html'))

		self.assertTrue(self.player_bvp_parser.player_data[MLBConstants.BATTER_VS_PITCHER]["konerpa01"][MLBConstants.NAME] == "Paul Konerko")
		self.assertTrue(self.player_bvp_parser.player_data[MLBConstants.BATTER_VS_PITCHER]["konerpa01"][MLBConstants.PLATE_APPEARANCES] == 94)
		self.assertTrue(self.player_bvp_parser.player_data[MLBConstants.BATTER_VS_PITCHER]["konerpa01"][MLBConstants.AT_BATS] == 81)
		self.assertTrue(self.player_bvp_parser.player_data[MLBConstants.BATTER_VS_PITCHER]["konerpa01"][MLBConstants.HITS] == 19)
		self.assertTrue(self.player_bvp_parser.player_data[MLBConstants.BATTER_VS_PITCHER]["konerpa01"][MLBConstants.DOUBLES] == 5)
		self.assertTrue(self.player_bvp_parser.player_data[MLBConstants.BATTER_VS_PITCHER]["konerpa01"][MLBConstants.TRIPLES] == 0)
		self.assertTrue(self.player_bvp_parser.player_data[MLBConstants.BATTER_VS_PITCHER]["konerpa01"][MLBConstants.HOME_RUNS] == 3)
		self.assertTrue(self.player_bvp_parser.player_data[MLBConstants.BATTER_VS_PITCHER]["konerpa01"][MLBConstants.RBI] == 9)
		self.assertTrue(self.player_bvp_parser.player_data[MLBConstants.BATTER_VS_PITCHER]["konerpa01"][MLBConstants.WALKS] == 13)
		self.assertTrue(self.player_bvp_parser.player_data[MLBConstants.BATTER_VS_PITCHER]["konerpa01"][MLBConstants.STRIKE_OUTS] == 15)
		self.assertTrue(self.player_bvp_parser.player_data[MLBConstants.BATTER_VS_PITCHER]["konerpa01"][MLBConstants.BATTING_AVERAGE] == 0.235)
		self.assertTrue(self.player_bvp_parser.player_data[MLBConstants.BATTER_VS_PITCHER]["konerpa01"][MLBConstants.ON_BASE_PERCENTAGE] == 0.340)
		self.assertTrue(self.player_bvp_parser.player_data[MLBConstants.BATTER_VS_PITCHER]["konerpa01"][MLBConstants.SLUGGING_PERCENTAGE] == 0.407)
		self.assertTrue(self.player_bvp_parser.player_data[MLBConstants.BATTER_VS_PITCHER]["konerpa01"][MLBConstants.OPS] == 0.748)
		self.assertTrue(self.player_bvp_parser.player_data[MLBConstants.BATTER_VS_PITCHER]["konerpa01"][MLBConstants.SACRIFICE_HITS] == 0)
		self.assertTrue(self.player_bvp_parser.player_data[MLBConstants.BATTER_VS_PITCHER]["konerpa01"][MLBConstants.SACRIFICE_FLIES] == 0)
		self.assertTrue(self.player_bvp_parser.player_data[MLBConstants.BATTER_VS_PITCHER]["konerpa01"][MLBConstants.INTENTIONAL_WALKS] == 0)
		self.assertTrue(self.player_bvp_parser.player_data[MLBConstants.BATTER_VS_PITCHER]["konerpa01"][MLBConstants.HIT_BY_PITCH] == 0)
		self.assertTrue(self.player_bvp_parser.player_data[MLBConstants.BATTER_VS_PITCHER]["konerpa01"][MLBConstants.DOUBLE_PLAYS_GROUNDED_INTO] == 2)

		self.assertTrue(self.player_bvp_parser.player_data[MLBConstants.BATTER_VS_PITCHER]["zambrca01"][MLBConstants.NAME] == "Carlos Zambrano")
		self.assertTrue(self.player_bvp_parser.player_data[MLBConstants.BATTER_VS_PITCHER]["zambrca01"][MLBConstants.PLATE_APPEARANCES] == 1)
		self.assertTrue(self.player_bvp_parser.player_data[MLBConstants.BATTER_VS_PITCHER]["zambrca01"][MLBConstants.AT_BATS] == 1)
		self.assertTrue(self.player_bvp_parser.player_data[MLBConstants.BATTER_VS_PITCHER]["zambrca01"][MLBConstants.HITS] == 0)
		self.assertTrue(self.player_bvp_parser.player_data[MLBConstants.BATTER_VS_PITCHER]["zambrca01"][MLBConstants.DOUBLES] == 0)
		self.assertTrue(self.player_bvp_parser.player_data[MLBConstants.BATTER_VS_PITCHER]["zambrca01"][MLBConstants.TRIPLES] == 0)
		self.assertTrue(self.player_bvp_parser.player_data[MLBConstants.BATTER_VS_PITCHER]["zambrca01"][MLBConstants.HOME_RUNS] == 0)
		self.assertTrue(self.player_bvp_parser.player_data[MLBConstants.BATTER_VS_PITCHER]["zambrca01"][MLBConstants.RBI] == 0)
		self.assertTrue(self.player_bvp_parser.player_data[MLBConstants.BATTER_VS_PITCHER]["zambrca01"][MLBConstants.WALKS] == 0)
		self.assertTrue(self.player_bvp_parser.player_data[MLBConstants.BATTER_VS_PITCHER]["zambrca01"][MLBConstants.STRIKE_OUTS] == 1)
		self.assertTrue(self.player_bvp_parser.player_data[MLBConstants.BATTER_VS_PITCHER]["zambrca01"][MLBConstants.BATTING_AVERAGE] == 0.0)
		self.assertTrue(self.player_bvp_parser.player_data[MLBConstants.BATTER_VS_PITCHER]["zambrca01"][MLBConstants.ON_BASE_PERCENTAGE] == 0.0)
		self.assertTrue(self.player_bvp_parser.player_data[MLBConstants.BATTER_VS_PITCHER]["zambrca01"][MLBConstants.SLUGGING_PERCENTAGE] == 0.0)
		self.assertTrue(self.player_bvp_parser.player_data[MLBConstants.BATTER_VS_PITCHER]["zambrca01"][MLBConstants.OPS] == 0.0)
		self.assertTrue(self.player_bvp_parser.player_data[MLBConstants.BATTER_VS_PITCHER]["zambrca01"][MLBConstants.SACRIFICE_HITS] == 0)
		self.assertTrue(self.player_bvp_parser.player_data[MLBConstants.BATTER_VS_PITCHER]["zambrca01"][MLBConstants.SACRIFICE_FLIES] == 0)
		self.assertTrue(self.player_bvp_parser.player_data[MLBConstants.BATTER_VS_PITCHER]["zambrca01"][MLBConstants.INTENTIONAL_WALKS] == 0)
		self.assertTrue(self.player_bvp_parser.player_data[MLBConstants.BATTER_VS_PITCHER]["zambrca01"][MLBConstants.HIT_BY_PITCH] == 0)
		self.assertTrue(self.player_bvp_parser.player_data[MLBConstants.BATTER_VS_PITCHER]["zambrca01"][MLBConstants.DOUBLE_PLAYS_GROUNDED_INTO] == 0)

if __name__ == '__main__':
	unittest.main()