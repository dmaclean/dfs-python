__author__ = 'dan'

from mlb.parsers.player_season_stats_parser import PlayerSeasonStatsParser

import unittest


class TestPlayerSeasonStatsParser(unittest.TestCase):
    player_season_stat_parser = None

    def setUp(self):
        self.player_season_stat_parser = PlayerSeasonStatsParser()

    def tearDown(self):
        self.player_season_stat_parser = None

    def test_parse_pitcher(self):
        self.player_season_stat_parser.parse(open('../test_files/season_stats_pitcher.html'))

        self.assertTrue(self.player_season_stat_parser.player_data["name"] == "David Aardsma")
        self.assertTrue(self.player_season_stat_parser.player_data["position"] == "Pitcher")

if __name__ == '__main__':
    unittest.main()