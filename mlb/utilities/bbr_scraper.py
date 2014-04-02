from mlb.constants.mlb_constants import MLBConstants
from mlb.models.player_manager import PlayerManager

__author__ = 'dan'

from httplib import HTTPConnection
from mlb.parsers.player_list_parser import PlayerListParser
from mlb.parsers.player_season_stats_parser import PlayerSeasonStatsParser

import logging
import random
import time


class BaseballReferenceScraper:
	"""
	Scraper for baseball-reference.com
	"""

	def __init__(self):
		self.source = "site"

		self.player_list_parser = PlayerListParser()
		self.player_season_stats_parser = PlayerSeasonStatsParser()
		self.player_manager = PlayerManager()

	def process(self):
		self.process_players()

	def fetch_data(self, url, log_to_console):
		"""
		Makes connection to baseball-reference and downloads data from URL.
		"""
		successful = False
		data = ""

		while not successful:
			try:
				conn = HTTPConnection("www.baseball-reference.com", timeout=5)
				conn.request("GET", url)
				resp = conn.getresponse()
				content_type = resp.getheader("content-type")

				encoding = None
				if content_type.find("charset=") > -1:
					encoding = content_type.split("charset=")[1]

				if log_to_console:
					print "{} for {}".format(resp.status, url)

				if encoding:
					data = resp.read().decode(encoding, 'ignore')
				else:
					data = resp.read()

				conn.close()
				successful = True
			except Exception, err:
				logging.error("Issue connecting to basketball-reference ({}).  Retrying in 10 seconds...".format(err))
				time.sleep(10)

		time.sleep(5 + (5 * random.random()))
		return data

	def process_players(self):
		"""
		Performs fetching of player data.
		"""
		alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o",
					"p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
		#alphabet = ["a"]

		# Go through all players by letter
		for letter in alphabet:
			url = "/players/{}/".format(letter)
			data = self.fetch_data(url, True)

			self.player_list_parser.parse(data)

			# Go through each player id for each letter
			for player_id in self.player_list_parser.player_ids:
				player = self.player_manager.read({MLBConstants.PLAYER_ID: player_id})
				if player is None:
					player = {MLBConstants.PLAYER_ID: player_id}

				player_url = "{}{}.shtml".format(url, player_id)

				player_page_data = self.fetch_data(player_url, True)

				self.player_season_stats_parser.player_data = player
				self.player_season_stats_parser.parse(player_page_data)

				if self.player_season_stats_parser.player_data[MLBConstants.POSITION] == "Pitcher":
					player_season_stats_detail_url = "/players/{}/{}-pitch.shtml".format(letter, player_id)
				else:
					player_season_stats_detail_url = "/players/{}/{}-bat.shtml".format(letter, player_id)

				player_season_stats_detail_data = self.fetch_data(player_season_stats_detail_url, True)
				self.player_season_stats_parser.parse(player_season_stats_detail_data)

				self.player_manager.save(player)



if __name__ == '__main__':
	scraper = BaseballReferenceScraper()
	scraper.process()