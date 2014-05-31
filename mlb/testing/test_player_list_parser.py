__author__ = 'dan'

import unittest

from mlb.parsers.player_list_parser import PlayerListParser


class TestPlayerListParser(unittest.TestCase):
    player_list_parser = None

    def setUp(self):
        self.player_list_parser = PlayerListParser()

    def tearDown(self):
        self.player_list_parser = None

    def test_parse_all(self):
        self.player_list_parser.active_only = False
        self.player_list_parser.parse(open('test_files/players_a.html'))

        self.assertTrue(self.player_list_parser.player_ids[0] == 'aardsda01')
        self.assertTrue(self.player_list_parser.player_ids[len(self.player_list_parser.player_ids)-1] == 'azocaos01')

    def test_parse_active_only(self):
        self.player_list_parser.active_only = True
        self.player_list_parser.parse(open('test_files/players_a.html'))

        self.assertTrue(self.player_list_parser.player_ids[0] == 'aardsda01')
        self.assertTrue(self.player_list_parser.player_ids[len(self.player_list_parser.player_ids)-1] == 'aybarer01')

if __name__ == '__main__':
	unittest.main()