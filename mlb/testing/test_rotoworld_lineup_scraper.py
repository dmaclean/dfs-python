import unittest

from mlb.parsers.rotoworld_lineup_scraper import RotoworldLineupScraper

__author__ = 'dan'

class TestRotoworldLinupScraper(unittest.TestCase):
	player_list_parser = None

	def setUp(self):
		self.parser = RotoworldLineupScraper(testing=True)

	def tearDown(self):
		self.parser = None

	def test_parse(self):
		f = open('../test_files/rotowire_daily_lineups.html')
		self.parser.parse(f.read())

if __name__ == '__main__':
	unittest.main()