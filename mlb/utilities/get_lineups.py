import logging
import random
import sys
import time

from datetime import date, timedelta
from httplib import HTTPConnection
from mlb.constants.mlb_constants import MLBConstants
from mlb.models.player_manager import PlayerManager
from mlb.parsers.rotoworld_lineup_scraper import RotoworldLineupScraper
from mlb.models.lineup_manager import LineupManager
from mlb.utilities.bbr_scraper import BaseballReferenceScraper

__author__ = 'dan'


class LineupScraper:
	def __init__(self):
		self.source = "site"
		self.scrape_yesterdays_players = True
		self.sleep_time = 2
		self.player_manager = PlayerManager()
		self.lineup_manager = LineupManager()
		self.bbr_scraper = BaseballReferenceScraper()
		self.bbr_scraper.sleep_time = self.sleep_time

	def fetch_data(self, url, log_to_console):
		"""
		Makes connection to baseball-reference and downloads data from URL.
		"""
		successful = False
		data = ""

		while not successful:
			try:
				conn = HTTPConnection("www.rotowire.com", timeout=5)
				conn.request("GET", url)
				resp = conn.getresponse()
				if resp.status == 301:
					resp = self.resolve_http_redirect(url, 3)

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
				logging.error("Issue connecting to rotowire ({}).  Retrying in 10 seconds...".format(err))
				time.sleep(10)

		#time.sleep(5 + (5 * random.random()))
		return data

	def readCLI(self):
		for arg in sys.argv:
			pieces = arg.split("=")
			if pieces[0] == "source":
				self.source = pieces[1]
			elif pieces[0] == "sleep":
				self.sleep_time = int(pieces[1])
			elif pieces[0] == "scrape_yesterdays_players":
				self.scrape_yesterdays_players = pieces[1] == "true"

	def scrape_yesterdays_lineups(self):
		"""
		Expedite the process of collecting data by getting stats for yesterday's lineups.  There's likely
		little that's going to change in terms of who is in the lineup (their exact spot could change) so
		this will give us a good head start.
		"""

		# Reset the sleep on BBR scraper, in case what was passed in from the CLI is different.
		self.bbr_scraper.sleep_time = self.sleep_time

		one_day = timedelta(days=1)
		yesterday = date.today()-one_day

		print "Fetching data for yesterday's lineups ({})".format(yesterday)

		players = self.lineup_manager.lineups_collection.find_one({"date": str(yesterday)})

		for player in players["players"]:
			unescaped_player = player.replace("_", ".")
			if self.lineup_manager.is_processed(player):
				continue

			start = time.time()

			# Ignore pitchers
			player_record = self.player_manager.players_collection.find_one({"player_id": unescaped_player})
			if player_record[MLBConstants.POSITION].lower() == MLBConstants.PITCHER_TYPE:
				logging.info("{} is a pitcher.  Skipping...".format(player))
				continue

			# Found a player.  Let's update their stuff.
			url = "/players/{}/".format(unescaped_player[0:1])
			self.bbr_scraper.process_player(unescaped_player, url, active=True)

			# Mark the player as processed (write to the lineup) once their stats have been updated.
			self.lineup_manager.add_player_to_lineup(player, {})

			end = time.time()
			print "Processed {} in {} seconds".format(player, end-start)

	def process(self):
		while True:
			start = time.time()

			if self.source == "site":
				data = self.fetch_data("/baseball/daily_lineups.htm", True)
			else:
				data = open(self.source)
			rotoworld_scraper = RotoworldLineupScraper(sleep_time=self.sleep_time)
			rotoworld_scraper.parse(data)

			end = time.time()
			print "Scraped starting line-ups in {} minutes".format((end-start)/60.0)

			print "All done.  Sleeping for 10 minutes then re-evaluating..."
			time.sleep(60*10)

if __name__ == '__main__':
	scraper = LineupScraper()
	scraper.readCLI()

	if scraper.scrape_yesterdays_players:
		start = time.time()
		scraper.scrape_yesterdays_lineups()
		end = time.time()
		print "Completed scraping yesterday's lineups in {} minutes".format((end-start)/60)
	scraper.process()