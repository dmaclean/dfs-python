import logging
import re
from bs4 import BeautifulSoup
from mlb.models.lineup_manager import LineupManager
from mlb.models.player_manager import PlayerManager
from mlb.utilities.bbr_scraper import BaseballReferenceScraper

__author__ = 'dan'


class RotoworldLineupScraper:
	def __init__(self, sleep_time=2):
		self.source = "site"
		self.player_regex = re.compile("/baseball/player.htm\?id=\d+")
		self.player_manager = PlayerManager()
		self.lineup_manager = LineupManager()
		self.bbr_scraper = BaseballReferenceScraper()
		self.bbr_scraper.sleep_time = sleep_time

	def parse(self, data):
		data = data.replace("\r", "").replace("\n", "").replace("\t", "")
		soup = BeautifulSoup(data)

		players = soup.find_all(href=self.player_regex)
		for player in players:
			player_name = None

			# Pitcher
			if "title" not in player.attrs:
				print "{} (Starting pitcher)".format(player.text)
				player_name = player.text
			# Position player
			else:
				print "{}".format(player.text)
				player_name = player.attrs["title"]

			player_data = self.player_manager.players_collection.find_one({'name': player_name})
			if player_data is None:
				logging.critical("Could not find record for {}".format(player_name))
				continue

			player_id = player_data["player_id"]
			escaped_player_id = self.lineup_manager.get_id_for_player_name(player_name)
			if self.lineup_manager.is_processed(escaped_player_id):
				print "{} already processed.".format(player_name)
				continue

			# Found a player.  Let's update their stuff.
			url = "/players/{}/".format(player_id[0:1])
			self.bbr_scraper.process_player(player_id, url, active=True)

			# Mark the player as processed (write to the lineup) once their stats have been updated.
			self.lineup_manager.add_player_to_lineup(escaped_player_id)