import logging
import sys
import time
from datetime import date, timedelta

from mlb.constants.mlb_constants import MLBConstants
from mlb.models.player_manager import PlayerManager
from mlb.parsers.rotoworld_lineup_scraper import RotoworldLineupScraper
from mlb.models.lineup_manager import LineupManager
from mlb.scrapers.bbr_scraper import BaseballReferenceScraper
from mlb.parsers.rotogrinders_ballpark_factors_parser import RotogrindersBallparkFactorsParser
from mlb.utilities.mlb_utilities import MLBUtilities


__author__ = 'dan'


class LineupScraper:
	def __init__(self):
		self.source = "site"
		self.scrape_yesterdays_players = True
		self.scrape_bvp = False
		self.sleep_time = 2
		self.player_manager = PlayerManager()
		self.lineup_manager = LineupManager()
		self.bbr_scraper = BaseballReferenceScraper()
		self.bbr_scraper.sleep_time = self.sleep_time

	def readCLI(self):
		for arg in sys.argv:
			pieces = arg.split("=")
			if pieces[0] == "source":
				self.source = pieces[1]
			elif pieces[0] == "sleep":
				self.sleep_time = int(pieces[1])
			elif pieces[0] == "scrape_yesterdays_players":
				self.scrape_yesterdays_players = pieces[1] == "true"
			elif pieces[0] == "scrape_bvp":
				self.scrape_yesterdays_players = pieces[1] == "true"

	def scrape_ballpark_factors(self):
		"""
		Scrapes the ballpark factors from Rotogrinders.com.
		"""
		data = MLBUtilities.fetch_data("rotogrinders.com", "/pages/Ballpark_Factors-49556", True)
		ballpark_factors_parser = RotogrindersBallparkFactorsParser()
		ballpark_factors_parser.parse(data)

	def scrape_yesterdays_lineups(self):
		"""
		Expedite the process of collecting data by getting stats for yesterday's lineups.  There's likely
		little that's going to change in terms of who is in the lineup (their exact spot could change) so
		this will give us a good head start.
		"""

		# Reset the sleep on BBR scraper, in case what was passed in from the CLI is different.
		self.bbr_scraper.sleep_time = self.sleep_time

		# Reset the scrape_bvp flag, in case what was passed in from the CLI is different.
		self.bbr_scraper.scrape_bvp = self.scrape_bvp

		one_day = timedelta(days=1)
		yesterday = date.today()-one_day

		# print "Fetching data for yesterday's lineups ({})".format(yesterday)

		# players = self.lineup_manager.lineups_collection.find_one({"date": str(yesterday)})
		#
		# if players is None:
		# 	logging.info("Looks like we didn't run this yesterday. Going to look for today's lineups...")
		# 	return

		rotoworld_scraper = RotoworldLineupScraper(sleep_time=self.sleep_time)
		data = MLBUtilities.fetch_data("www.rotowire.com", "/baseball/daily_lineups.htm", True)
		teams, team_details = rotoworld_scraper.parse_teams_only(data)

		for team in teams:
			players = self.lineup_manager.find_team_last_game(team)
			for player in players:
			# for player in players["players"]:
				player_id = player[MLBConstants.PLAYER_ID]
				unescaped_player = player_id.replace("_", ".")

				# Skip player if they've already been processed.
				if self.lineup_manager.is_processed(player_id):
					logging.info("Skipping {}, already processed.".format(player_id))
					continue

				# Skip player if they didn't end up in yesterday's lineup.  This can happen
				# if we do prefetching on a player from a previous day and they have an off day.
				# if len(players["players"][player]) == 0:
				# 	logging.info("Skipping {}, wasn't in yesterday's lineup.".format(player))
				# 	continue

				# Skip player if their team isn't playing today.
				# if players["players"][player][MLBConstants.TEAM] not in teams:
				# 	logging.info("Skipping {}, {} are not playing today.".format(player, players["players"][player][MLBConstants.TEAM]))
				# 	continue

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
				player_data = team_details[team]
				if len(player[MLBConstants.POSITION]) == 0:
					self.lineup_manager.find_player_position_last_game(player_id)
				else:
					player_data[MLBConstants.POSITION] = player[MLBConstants.POSITION]

				self.lineup_manager.add_player_to_lineup(player[MLBConstants.PLAYER_ID], player_data)

				end = time.time()
				print "Processed {} in {} seconds".format(player, end-start)

	def process(self):
		while True:
			start = time.time()

			if self.source == "site":
				data = MLBUtilities.fetch_data("www.rotowire.com", "/baseball/daily_lineups.htm", True)
			else:
				data = open(self.source)
			rotoworld_scraper = RotoworldLineupScraper(sleep_time=self.sleep_time)
			rotoworld_scraper.parse(data)

			end = time.time()
			print "Scraped starting line-ups in {} minutes".format((end-start)/60.0)

			print "All done.  Sleeping for 10 minutes then re-evaluating..."
			time.sleep(60*10)

if __name__ == '__main__':
	logging.basicConfig(level=logging.INFO)
	scraper = LineupScraper()
	scraper.readCLI()

	if scraper.scrape_yesterdays_players:
		start = time.time()
		scraper.scrape_yesterdays_lineups()
		end = time.time()
		print "Completed scraping yesterday's lineups in {} minutes".format((end-start)/60)
	scraper.scrape_ballpark_factors()
	scraper.process()