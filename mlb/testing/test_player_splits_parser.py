import unittest
from mlb.constants.mlb_constants import MLBConstants
from mlb.parsers.player_splits_parser import PlayerSplitsParser

__author__ = 'dan'


class TestPlayerSplitsParser(unittest.TestCase):
	def setUp(self):
		self.player_splits_parser = PlayerSplitsParser()

	def tearDown(self):
		self.player_splits_parser = None

	def test_parse_batter_splits(self):
		self.player_splits_parser.player_data = {MLBConstants.PLAYER_ID: "cabremi01", MLBConstants.POSITION: "Third base"}
		self.player_splits_parser.parse(open('../test_files/batter_splits.html'))

		pd = self.player_splits_parser.player_data
		self.assertTrue(pd[MLBConstants.BATTER_SPLITS]["2014"]["2014 Totals"][
							MLBConstants.GAMES_PLAYED] == 4)
		self.assertTrue(pd[MLBConstants.BATTER_SPLITS]["2014"]["2014 Totals"][
							MLBConstants.GAMES_STARTED] == 4)
		self.assertTrue(pd[MLBConstants.BATTER_SPLITS]["2014"]["2014 Totals"][
							MLBConstants.PLATE_APPEARANCES] == 17)
		self.assertTrue(pd[MLBConstants.BATTER_SPLITS]["2014"]["2014 Totals"][
							MLBConstants.AT_BATS] == 16)
		self.assertTrue(pd[MLBConstants.BATTER_SPLITS]["2014"]["2014 Totals"][
							MLBConstants.RUNS] == 1)
		self.assertTrue(pd[MLBConstants.BATTER_SPLITS]["2014"]["2014 Totals"][
							MLBConstants.HITS] == 6)
		self.assertTrue(pd[MLBConstants.BATTER_SPLITS]["2014"]["2014 Totals"][
							MLBConstants.DOUBLES] == 2)
		self.assertTrue(pd[MLBConstants.BATTER_SPLITS]["2014"]["2014 Totals"][
							MLBConstants.TRIPLES] == 0)
		self.assertTrue(pd[MLBConstants.BATTER_SPLITS]["2014"]["2014 Totals"][
							MLBConstants.HOME_RUNS] == 1)
		self.assertTrue(pd[MLBConstants.BATTER_SPLITS]["2014"]["2014 Totals"][
							MLBConstants.RBI] == 3)
		self.assertTrue(pd[MLBConstants.BATTER_SPLITS]["2014"]["2014 Totals"][
							MLBConstants.STOLEN_BASES] == 0)
		self.assertTrue(pd[MLBConstants.BATTER_SPLITS]["2014"]["2014 Totals"][
							MLBConstants.CAUGHT_STEALING] == 0)
		self.assertTrue(pd[MLBConstants.BATTER_SPLITS]["2014"]["2014 Totals"][
							MLBConstants.WALKS] == 1)
		self.assertTrue(pd[MLBConstants.BATTER_SPLITS]["2014"]["2014 Totals"][
							MLBConstants.STRIKE_OUTS] == 4)
		self.assertTrue(pd[MLBConstants.BATTER_SPLITS]["2014"]["2014 Totals"][
							MLBConstants.BATTING_AVERAGE] == 0.375)
		self.assertTrue(pd[MLBConstants.BATTER_SPLITS]["2014"]["2014 Totals"][
							MLBConstants.ON_BASE_PERCENTAGE] == 0.412)
		self.assertTrue(pd[MLBConstants.BATTER_SPLITS]["2014"]["2014 Totals"][
							MLBConstants.SLUGGING_PERCENTAGE] == 0.688)
		self.assertTrue(pd[MLBConstants.BATTER_SPLITS]["2014"]["2014 Totals"][
							MLBConstants.OPS] == 1.099)
		self.assertTrue(pd[MLBConstants.BATTER_SPLITS]["2014"]["2014 Totals"][
							MLBConstants.TOTAL_BASES] == 11)
		self.assertTrue(pd[MLBConstants.BATTER_SPLITS]["2014"]["2014 Totals"][
							MLBConstants.DOUBLE_PLAYS_GROUNDED_INTO] == 0)
		self.assertTrue(pd[MLBConstants.BATTER_SPLITS]["2014"]["2014 Totals"][
							MLBConstants.HIT_BY_PITCH] == 0)
		self.assertTrue(pd[MLBConstants.BATTER_SPLITS]["2014"]["2014 Totals"][
							MLBConstants.SACRIFICE_HITS] == 0)
		self.assertTrue(pd[MLBConstants.BATTER_SPLITS]["2014"]["2014 Totals"][
							MLBConstants.SACRIFICE_FLIES] == 0)
		self.assertTrue(pd[MLBConstants.BATTER_SPLITS]["2014"]["2014 Totals"][
							MLBConstants.INTENTIONAL_WALKS] == 0)
		self.assertTrue(pd[MLBConstants.BATTER_SPLITS]["2014"]["2014 Totals"][
							MLBConstants.REACHED_ON_ERROR] == 0)
		self.assertTrue(pd[MLBConstants.BATTER_SPLITS]["2014"]["2014 Totals"][
							MLBConstants.BABIP] == 0.455)
		self.assertTrue(pd[MLBConstants.BATTER_SPLITS]["2014"]["2014 Totals"][
							MLBConstants.T_OPS_PLUS] == 100)
		self.assertTrue(pd[MLBConstants.BATTER_SPLITS]["2014"]["2014 Totals"][
							MLBConstants.S_OPS_PLUS] == 209)

		self.assertTrue(pd[MLBConstants.BATTER_SPLITS]["2014"][MLBConstants.SPLITS_VS_RHP][
							MLBConstants.GAMES_PLAYED] == 4)
		self.assertTrue(pd[MLBConstants.BATTER_SPLITS]["2014"][MLBConstants.SPLITS_VS_RHP][
							MLBConstants.GAMES_STARTED] == 0)
		self.assertTrue(pd[MLBConstants.BATTER_SPLITS]["2014"][MLBConstants.SPLITS_VS_RHP][
							MLBConstants.PLATE_APPEARANCES] == 13)
		self.assertTrue(pd[MLBConstants.BATTER_SPLITS]["2014"][MLBConstants.SPLITS_VS_RHP][
							MLBConstants.AT_BATS] == 12)
		self.assertTrue(pd[MLBConstants.BATTER_SPLITS]["2014"][MLBConstants.SPLITS_VS_RHP][
							MLBConstants.RUNS] == 1)
		self.assertTrue(pd[MLBConstants.BATTER_SPLITS]["2014"][MLBConstants.SPLITS_VS_RHP][
							MLBConstants.HITS] == 6)
		self.assertTrue(pd[MLBConstants.BATTER_SPLITS]["2014"][MLBConstants.SPLITS_VS_RHP][
							MLBConstants.DOUBLES] == 2)
		self.assertTrue(pd[MLBConstants.BATTER_SPLITS]["2014"][MLBConstants.SPLITS_VS_RHP][
							MLBConstants.TRIPLES] == 0)
		self.assertTrue(pd[MLBConstants.BATTER_SPLITS]["2014"][MLBConstants.SPLITS_VS_RHP][
							MLBConstants.HOME_RUNS] == 1)
		self.assertTrue(pd[MLBConstants.BATTER_SPLITS]["2014"][MLBConstants.SPLITS_VS_RHP][
							MLBConstants.RBI] == 3)
		self.assertTrue(pd[MLBConstants.BATTER_SPLITS]["2014"][MLBConstants.SPLITS_VS_RHP][
							MLBConstants.STOLEN_BASES] == 0)
		self.assertTrue(pd[MLBConstants.BATTER_SPLITS]["2014"][MLBConstants.SPLITS_VS_RHP][
							MLBConstants.CAUGHT_STEALING] == 0)
		self.assertTrue(pd[MLBConstants.BATTER_SPLITS]["2014"][MLBConstants.SPLITS_VS_RHP][
							MLBConstants.WALKS] == 1)
		self.assertTrue(pd[MLBConstants.BATTER_SPLITS]["2014"][MLBConstants.SPLITS_VS_RHP][
							MLBConstants.STRIKE_OUTS] == 2)
		self.assertTrue(pd[MLBConstants.BATTER_SPLITS]["2014"][MLBConstants.SPLITS_VS_RHP][
							MLBConstants.BATTING_AVERAGE] == 0.5)
		self.assertTrue(pd[MLBConstants.BATTER_SPLITS]["2014"][MLBConstants.SPLITS_VS_RHP][
							MLBConstants.ON_BASE_PERCENTAGE] == 0.538)
		self.assertTrue(pd[MLBConstants.BATTER_SPLITS]["2014"][MLBConstants.SPLITS_VS_RHP][
							MLBConstants.SLUGGING_PERCENTAGE] == 0.917)
		self.assertTrue(pd[MLBConstants.BATTER_SPLITS]["2014"][MLBConstants.SPLITS_VS_RHP][
							MLBConstants.OPS] == 1.455)
		self.assertTrue(pd[MLBConstants.BATTER_SPLITS]["2014"][MLBConstants.SPLITS_VS_RHP][
							MLBConstants.TOTAL_BASES] == 11)
		self.assertTrue(pd[MLBConstants.BATTER_SPLITS]["2014"][MLBConstants.SPLITS_VS_RHP][
							MLBConstants.DOUBLE_PLAYS_GROUNDED_INTO] == 0)
		self.assertTrue(pd[MLBConstants.BATTER_SPLITS]["2014"][MLBConstants.SPLITS_VS_RHP][
							MLBConstants.HIT_BY_PITCH] == 0)
		self.assertTrue(pd[MLBConstants.BATTER_SPLITS]["2014"][MLBConstants.SPLITS_VS_RHP][
							MLBConstants.SACRIFICE_HITS] == 0)
		self.assertTrue(pd[MLBConstants.BATTER_SPLITS]["2014"][MLBConstants.SPLITS_VS_RHP][
							MLBConstants.SACRIFICE_FLIES] == 0)
		self.assertTrue(pd[MLBConstants.BATTER_SPLITS]["2014"][MLBConstants.SPLITS_VS_RHP][
							MLBConstants.INTENTIONAL_WALKS] == 0)
		self.assertTrue(pd[MLBConstants.BATTER_SPLITS]["2014"][MLBConstants.SPLITS_VS_RHP][
							MLBConstants.REACHED_ON_ERROR] == 0)
		self.assertTrue(pd[MLBConstants.BATTER_SPLITS]["2014"][MLBConstants.SPLITS_VS_RHP][
							MLBConstants.BABIP] == 0.556)
		self.assertTrue(pd[MLBConstants.BATTER_SPLITS]["2014"][MLBConstants.SPLITS_VS_RHP][
							MLBConstants.T_OPS_PLUS] == 164)
		self.assertTrue(pd[MLBConstants.BATTER_SPLITS]["2014"][MLBConstants.SPLITS_VS_RHP][
							MLBConstants.S_OPS_PLUS] == 299)


if __name__ == '__main__':
	unittest.main()