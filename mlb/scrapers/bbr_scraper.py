import sys
from mlb.constants.mlb_constants import MLBConstants
from mlb.models.player_manager import PlayerManager
from mlb.parsers.player_bvp_parser import PlayerBvPParser
from mlb.parsers.player_gamelog_parser import PlayerGamelogParser
from mlb.parsers.player_splits_parser import PlayerSplitsParser
from mlb.utilities.mlb_utilities import MLBUtilities
from mlb.parsers.player_list_parser import PlayerListParser
from mlb.parsers.player_season_stats_parser import PlayerSeasonStatsParser

import logging
import time


class BaseballReferenceScraper:
	"""
	Scraper for baseball-reference.com
	"""

	def __init__(self):
		self.source = "site"
		self.all_players = False
		self.scrape_bvp = False
		self.player_id = None
		self.url = None

		self.player_list_parser = PlayerListParser()
		self.player_season_stats_parser = PlayerSeasonStatsParser()
		self.player_gamelog_parser = PlayerGamelogParser()
		self.player_splits_parser = PlayerSplitsParser()
		self.player_bvp_parser = PlayerBvPParser()
		self.player_manager = PlayerManager()

	def process(self):
		self.readCLI()

		if self.player_id:
			self.process_player(self.player_id, self.url, True)
		else:
			self.process_players()

	def readCLI(self):
		for arg in sys.argv:
			if arg == "bbr_scraper.py":
				pass
			else:
				pieces = arg.split("=")
				if pieces[0] == "season":
					self.season = int(pieces[1])
				elif pieces[0] == "all_players":
					self.all_players = pieces[1] == "true"
				elif pieces[0] == "yesterday_only":
					self.yesterday_only = pieces[1] == "true"
				elif pieces[0] == "sleep":
					self.sleep_time = int(pieces[1])
				elif pieces[0] == "player_id":
					self.player_id = pieces[1]
				elif pieces[0] == "url":
					self.url = pieces[1]


	def process_players(self):
		"""
		Performs fetching of player data.
		"""
		# alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o",
		# 			"p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
		alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o",
					"p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]

		# Go through all players by letter
		for letter in alphabet:
			url = "/players/{}/".format(letter)
			data = MLBUtilities.fetch_data("www.baseball-reference.com", url, True)

			self.player_list_parser.parse(data, letter)

			# Go through odd player ids
			for player_id in self.player_list_parser.odd_player_ids:
				odd_url = "/players/{}/".format(player_id[0])
				self.process_player(player_id[1], odd_url)

			if self.all_players:
				# Go through retired players
				for player_id in self.player_list_parser.retired_player_ids:
					self.process_player(player_id, url)

			# Go through active players
			for player_id in self.player_list_parser.active_player_ids:
				self.process_player(player_id, url, True)

	def process_player(self, player_id, url, active=False):
		start = time.time()
		player = self.player_manager.read({MLBConstants.PLAYER_ID: player_id})
		end = time.time()
		print "\t\tDEBUG: Read from player_manager in {} seconds".format(end-start)

		if player is None:
			player = {MLBConstants.PLAYER_ID: player_id}
		# We can skip this player
		elif MLBConstants.BATTER_VS_PITCHER in player and not active:
			logging.info("Looks like all info for {} has already been scraped.  Moving on...".format(player_id))
			return

		player_url = "{}{}.shtml".format(url, player_id)

		player_page_data = MLBUtilities.fetch_data("www.baseball-reference.com", player_url, True)

		self.player_season_stats_parser.player_data = player
		self.player_season_stats_parser.parse(player_page_data)

		#############################################
		# Should we get the pitcher or batter page?
		#############################################
		if self.player_season_stats_parser.player_data[MLBConstants.POSITION] == "Pitcher":
			player_season_stats_detail_url = "{}{}-pitch.shtml".format(url, player_id)
		else:
			player_season_stats_detail_url = "{}{}-bat.shtml".format(url, player_id)

		###############################################
		# Fetch detailed season stats for the player.
		###############################################
		start = time.time()
		player_season_stats_detail_data = MLBUtilities.fetch_data("www.baseball-reference.com", player_season_stats_detail_url, True)
		end = time.time()
		print "\t\tDEBUG: Fetched detailed season stats in {} seconds".format(end-start)

		start = time.time()
		self.player_season_stats_parser.parse(player_season_stats_detail_data)
		end = time.time()
		print "\t\tDEBUG: Parsed detailed season stats in {} seconds".format(end-start)

		# start = time.time()
		# self.player_manager.save(player)
		# end = time.time()
		# print "\t\tDEBUG: Saved detailed season stats in {} seconds".format(end-start)

		active_seasons = self.determine_active_seasons(player)
		type = "p" if player[MLBConstants.POSITION] == "Pitcher" else "b"

		#################
		# Grab gamelogs
		#################
		for season in active_seasons:
			if season not in ["2014"]:
				continue
			player_gamelog_url = "/players/gl.cgi?id={}&t={}&year={}".format(player_id, type, season)
			data = MLBUtilities.fetch_data("www.baseball-reference.com", player_gamelog_url, True)
			self.player_gamelog_parser.player_data = player
			self.player_gamelog_parser.type = MLBConstants.PITCHER_TYPE if player[MLBConstants.POSITION] == "Pitcher" else MLBConstants.BATTER_TYPE
			self.player_gamelog_parser.season = season
			self.player_gamelog_parser.parse(data)
		# self.player_manager.save(player)

		###############
		# Grab splits
		###############
		active_seasons.append("Career")
		for season in active_seasons:
			if season not in ["2014", "Career"]:
				continue
			player_split_url = "/players/split.cgi?id={}&t={}&year={}".format(player_id, type, season)
			data = MLBUtilities.fetch_data("www.baseball-reference.com", player_split_url, True)
			self.player_splits_parser.player_data = player
			self.player_splits_parser.season = season
			self.player_splits_parser.parse(data, season)
		# self.player_manager.save(player)

		#####################
		# Grab BvP (or PvB)
		#####################
		if self.scrape_bvp:
			if self.player_season_stats_parser.player_data[MLBConstants.POSITION] == "Pitcher":
				self.player_bvp_parser.type = MLBConstants.PITCHER_TYPE
				bvp_url = "/play-index/batter_vs_pitcher.cgi?pitcher={}".format(player_id)
			else:
				self.player_bvp_parser.type = MLBConstants.BATTER_TYPE
				bvp_url = "/play-index/batter_vs_pitcher.cgi?batter={}".format(player_id)

			data = self.fetch_data(bvp_url, True)
			self.player_bvp_parser.player_data = player
			self.player_bvp_parser.parse(data)

		start = time.time()
		self.player_manager.save(player)
		end = time.time()
		print "\t\tDEBUG: Saved player stats in {} seconds".format(end-start)

	def determine_active_seasons(self, player):
		"""
		Convenience method for determining the seasons that a player has been active.
		"""
		seasons = []

		if player[MLBConstants.POSITION] == "Pitcher" and MLBConstants.STANDARD_PITCHING in player:
			for k in player[MLBConstants.STANDARD_PITCHING]:
				seasons.append(k)
		elif player[MLBConstants.POSITION] != "Pitcher" and MLBConstants.STANDARD_BATTING in player:
			for k in player[MLBConstants.STANDARD_BATTING]:
				seasons.append(k)

		return seasons


if __name__ == '__main__':
	logging.basicConfig(level=logging.INFO)

	scraper = BaseballReferenceScraper()
	scraper.process()