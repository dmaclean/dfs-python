from mlb.constants.mlb_constants import MLBConstants
from mlb.models.stat_calculator import StatCalculator
from mlb.utilities.mlb_utilities import MLBUtilities

__author__ = 'dan'

from bs4 import BeautifulSoup

import re


class PlayerSeasonStatsParser:
	def __init__(self, player_data=None):
		self.player_data = player_data

		self.pitching_standard_season_regex = re.compile("pitching_standard\.(\d+)")
		self.player_value_pitching_regex = re.compile("pitching_value\.(\d+)")

		self.batting_standard_season_regex = re.compile("batting_standard\.(\d+)")
		self.player_value_batting_regex = re.compile("batting_value\.(\d+)")

		self.stat_calculator = StatCalculator()

	def parse(self, data):
		"""
		Parses data from a player's season stats page.
		"""
		soup = BeautifulSoup(data)

		# Find player's name and position
		self.player_data[MLBConstants.NAME] = soup.find("span", attrs={"itemprop": "name"}).text
		self.player_data[MLBConstants.POSITION] = soup.find("span", attrs={"itemprop": "role"}).text

		if self.player_data[MLBConstants.POSITION] == "Pitcher":
			# Parse the Standard Pitching table.
			self.parse_standard_pitching(soup)

			# Parse the Player Value--Pitchers table
			self.parse_player_value_pitchers(soup)
		else:
			# Parse the Standard Batting table
			self.parse_standard_batting(soup)

			# Parse the Player Value--Batters table
			self.parse_player_value_batting(soup)

	def parse_standard_pitching(self, soup):
		"""
		Parses data from the Stanard Pitching table.
		"""
		pitching_standard_entries = soup.find_all(id=re.compile(self.pitching_standard_season_regex))

		for entry in pitching_standard_entries:
			tds = entry.find_all("td")

			i = 0
			season = ""
			for td in tds:
				if i == 0:
					season = td.text

					if MLBConstants.STANDARD_PITCHING not in self.player_data:
						self.player_data[MLBConstants.STANDARD_PITCHING] = {}

					self.player_data[MLBConstants.STANDARD_PITCHING][season] = {}
				elif i == 1:
					self.player_data[MLBConstants.STANDARD_PITCHING][season][MLBConstants.AGE] = MLBUtilities.resolve_value(td.text, "int")
				elif i == 2:
					self.player_data[MLBConstants.STANDARD_PITCHING][season][MLBConstants.TEAM] = td.text
				elif i == 3:
					self.player_data[MLBConstants.STANDARD_PITCHING][season][MLBConstants.LEAGUE] = td.text
				elif i == 4:
					self.player_data[MLBConstants.STANDARD_PITCHING][season][MLBConstants.WINS] = MLBUtilities.resolve_value(td.text, "int")
				elif i == 5:
					self.player_data[MLBConstants.STANDARD_PITCHING][season][MLBConstants.LOSSES] = MLBUtilities.resolve_value(td.text, "int")
				elif i == 6:
					self.player_data[MLBConstants.STANDARD_PITCHING][season][MLBConstants.WIN_LOSS_PCT] = MLBUtilities.resolve_value(td.text, "float")
				elif i == 7:
					self.player_data[MLBConstants.STANDARD_PITCHING][season][MLBConstants.ERA] = MLBUtilities.resolve_value(td.text, "float")
				elif i == 8:
					self.player_data[MLBConstants.STANDARD_PITCHING][season][MLBConstants.GAMES] = MLBUtilities.resolve_value(td.text, "int")
				elif i == 9:
					self.player_data[MLBConstants.STANDARD_PITCHING][season][MLBConstants.GAMES_STARTED] = MLBUtilities.resolve_value(td.text, "int")
				elif i == 10:
					self.player_data[MLBConstants.STANDARD_PITCHING][season][MLBConstants.GAMES_FINISHED] = MLBUtilities.resolve_value(td.text, "int")
				elif i == 11:
					self.player_data[MLBConstants.STANDARD_PITCHING][season][MLBConstants.COMPLETE_GAMES] = MLBUtilities.resolve_value(td.text, "int")
				elif i == 12:
					self.player_data[MLBConstants.STANDARD_PITCHING][season][MLBConstants.SHUT_OUTS] = MLBUtilities.resolve_value(td.text, "int")
				elif i == 13:
					self.player_data[MLBConstants.STANDARD_PITCHING][season][MLBConstants.SAVES] = MLBUtilities.resolve_value(td.text, "int")
				elif i == 14:
					self.player_data[MLBConstants.STANDARD_PITCHING][season][MLBConstants.INNINGS_PITCHED] = MLBUtilities.resolve_value(td.text, "float")
				elif i == 15:
					self.player_data[MLBConstants.STANDARD_PITCHING][season][MLBConstants.HITS] = MLBUtilities.resolve_value(td.text, "int")
				elif i == 16:
					self.player_data[MLBConstants.STANDARD_PITCHING][season][MLBConstants.RUNS] = MLBUtilities.resolve_value(td.text, "int")
				elif i == 17:
					self.player_data[MLBConstants.STANDARD_PITCHING][season][MLBConstants.EARNED_RUNS] = MLBUtilities.resolve_value(td.text, "int")
				elif i == 18:
					self.player_data[MLBConstants.STANDARD_PITCHING][season][MLBConstants.HOME_RUNS] = MLBUtilities.resolve_value(td.text, "int")
				elif i == 19:
					self.player_data[MLBConstants.STANDARD_PITCHING][season][MLBConstants.WALKS] = MLBUtilities.resolve_value(td.text, "int")
				elif i == 20:
					self.player_data[MLBConstants.STANDARD_PITCHING][season][MLBConstants.INTENTIONAL_WALKS] = MLBUtilities.resolve_value(td.text, "int")
				elif i == 21:
					self.player_data[MLBConstants.STANDARD_PITCHING][season][MLBConstants.STRIKE_OUTS] = MLBUtilities.resolve_value(td.text, "int")
				elif i == 22:
					self.player_data[MLBConstants.STANDARD_PITCHING][season][MLBConstants.HIT_BY_PITCH] = MLBUtilities.resolve_value(td.text, "int")
				elif i == 23:
					self.player_data[MLBConstants.STANDARD_PITCHING][season][MLBConstants.BALKS] = MLBUtilities.resolve_value(td.text, "int")
				elif i == 24:
					self.player_data[MLBConstants.STANDARD_PITCHING][season][MLBConstants.WILD_PITCHES] = MLBUtilities.resolve_value(td.text, "int")
				elif i == 25:
					self.player_data[MLBConstants.STANDARD_PITCHING][season][MLBConstants.BATTERS_FACED] = MLBUtilities.resolve_value(td.text, "int")
				elif i == 26:
					self.player_data[MLBConstants.STANDARD_PITCHING][season][MLBConstants.ERA_PLUS] = MLBUtilities.resolve_value(td.text, "float")
				elif i == 27:
					self.player_data[MLBConstants.STANDARD_PITCHING][season][MLBConstants.WHIP] = MLBUtilities.resolve_value(td.text, "float")
				elif i == 28:
					self.player_data[MLBConstants.STANDARD_PITCHING][season][MLBConstants.HITS_PER_9_INNINGS] = MLBUtilities.resolve_value(td.text, "float")
				elif i == 29:
					self.player_data[MLBConstants.STANDARD_PITCHING][season][MLBConstants.HOME_RUNS_PER_9_INNINGS] = MLBUtilities.resolve_value(td.text, "float")
				elif i == 30:
					self.player_data[MLBConstants.STANDARD_PITCHING][season][MLBConstants.WALKS_PER_9_INNINGS] = MLBUtilities.resolve_value(td.text, "float")
				elif i == 31:
					self.player_data[MLBConstants.STANDARD_PITCHING][season][MLBConstants.STRIKE_OUTS_PER_9_INNINGS] = MLBUtilities.resolve_value(td.text, "float")
				elif i == 32:
					self.player_data[MLBConstants.STANDARD_PITCHING][season][MLBConstants.STRIKE_OUT_TO_WALK_RATIO] = MLBUtilities.resolve_value(td.text, "float")

				i += 1

			self.player_data[MLBConstants.STANDARD_PITCHING][season][MLBConstants.FIP] = self.stat_calculator.calculate_fip(self.player_data[MLBConstants.STANDARD_PITCHING][season])

	def parse_player_value_pitchers(self, soup):
		"""
		Parses data in the Player Value--Pitchers table.
		"""
		pitching_value_entries = soup.find_all(id=self.player_value_pitching_regex)

		for entry in pitching_value_entries:
			tds = entry.find_all("td")

			i = 0
			season = ""
			for td in tds:
				if i == 0:
					season = td.text

					if MLBConstants.PLAYER_VALUE_PITCHING not in self.player_data:
						self.player_data[MLBConstants.PLAYER_VALUE_PITCHING] = {}

					self.player_data[MLBConstants.PLAYER_VALUE_PITCHING][season] = {}
				elif i == 8:
					self.player_data[MLBConstants.PLAYER_VALUE_PITCHING][season][MLBConstants.RUNS_ALLOWED_PER_9_INNINGS] = MLBUtilities.resolve_value(td.text, "float")
				elif i == 9:
					self.player_data[MLBConstants.PLAYER_VALUE_PITCHING][season][MLBConstants.RUNS_ALLOWED_PER_9_INNINGS_OPP] = MLBUtilities.resolve_value(td.text, "float")
				elif i == 10:
					self.player_data[MLBConstants.PLAYER_VALUE_PITCHING][season][MLBConstants.RUNS_PER_9_INNINGS_IN_SUPPORT_FROM_DEFENSE] = MLBUtilities.resolve_value(td.text, "float")
				elif i == 11:
					self.player_data[MLBConstants.PLAYER_VALUE_PITCHING][season][MLBConstants.RUNS_PER_9_INNINGS_BY_ROLE] = MLBUtilities.resolve_value(td.text, "float")
				elif i == 12:
					self.player_data[MLBConstants.PLAYER_VALUE_PITCHING][season][MLBConstants.PARK_FACTORS] = MLBUtilities.resolve_value(td.text, "float")
				elif i == 13:
					self.player_data[MLBConstants.PLAYER_VALUE_PITCHING][season][MLBConstants.RUNS_PER_9_INNINGS_FOR_AVG_PITCHER] = MLBUtilities.resolve_value(td.text, "float")
				elif i == 14:
					self.player_data[MLBConstants.PLAYER_VALUE_PITCHING][season][MLBConstants.RUNS_BETTER_THAN_AVG] = MLBUtilities.resolve_value(td.text, "int")
				elif i == 15:
					self.player_data[MLBConstants.PLAYER_VALUE_PITCHING][season][MLBConstants.WINS_ABOVE_AVG] = MLBUtilities.resolve_value(td.text, "float")
				elif i == 16:
					self.player_data[MLBConstants.PLAYER_VALUE_PITCHING][season][MLBConstants.GAME_ENTERING_LEVERAGE_INDEX] = MLBUtilities.resolve_value(td.text, "float")
				elif i == 17:
					self.player_data[MLBConstants.PLAYER_VALUE_PITCHING][season][MLBConstants.WINS_ABOVE_AVG_ADJUSTMENT] = MLBUtilities.resolve_value(td.text, "float")
				elif i == 18:
					self.player_data[MLBConstants.PLAYER_VALUE_PITCHING][season][MLBConstants.WINS_ABOVE_REPLACEMENT] = MLBUtilities.resolve_value(td.text, "float")
				elif i == 19:
					self.player_data[MLBConstants.PLAYER_VALUE_PITCHING][season][MLBConstants.RUNS_BETTER_THAN_REPLACEMENT] = MLBUtilities.resolve_value(td.text, "int")
				elif i == 20:
					self.player_data[MLBConstants.PLAYER_VALUE_PITCHING][season][MLBConstants.WIN_LOSS_PCT_WITH_AVG_TEAM] = MLBUtilities.resolve_value(td.text, "float")
				elif i == 21:
					self.player_data[MLBConstants.PLAYER_VALUE_PITCHING][season][MLBConstants.WIN_LOSS_PCT_WITH_AVG_TEAM_SEASON] = MLBUtilities.resolve_value(td.text, "float")
				elif i == 22:
					self.player_data[MLBConstants.PLAYER_VALUE_PITCHING][season][MLBConstants.SALARY] = MLBUtilities.resolve_value(td.text.replace('$', '').replace(',',''), "int")

				i += 1

	def parse_standard_batting(self, soup):
		"""
		Parses data from the Stanard Batting table.
		"""
		batting_standard_entries = soup.find_all(id=self.batting_standard_season_regex)

		for entry in batting_standard_entries:
			tds = entry.find_all("td")

			i = 0
			season = ""
			for td in tds:
				if i == 0:
					season = td.text

					if MLBConstants.STANDARD_BATTING not in self.player_data:
						self.player_data[MLBConstants.STANDARD_BATTING] = {}

					self.player_data[MLBConstants.STANDARD_BATTING][season] = {}
				elif i == 1:
					self.player_data[MLBConstants.STANDARD_BATTING][season][MLBConstants.AGE] = MLBUtilities.resolve_value(td.text, "int")
				elif i == 2:
					try:
						self.player_data[MLBConstants.STANDARD_BATTING][season][MLBConstants.TEAM] = td.a.text
					except AttributeError:
						self.player_data[MLBConstants.STANDARD_BATTING][season][MLBConstants.TEAM] = td.text
				elif i == 3:
					try:
						self.player_data[MLBConstants.STANDARD_BATTING][season][MLBConstants.LEAGUE] = td.a.text
					except AttributeError:
						self.player_data[MLBConstants.STANDARD_BATTING][season][MLBConstants.LEAGUE] = td.text
				elif i == 4:
					self.player_data[MLBConstants.STANDARD_BATTING][season][MLBConstants.GAMES_PLAYED] = MLBUtilities.resolve_value(td.text, "int")
				elif i == 5:
					self.player_data[MLBConstants.STANDARD_BATTING][season][MLBConstants.PLATE_APPEARANCES] = MLBUtilities.resolve_value(td.text, "int")
				elif i == 6:
					self.player_data[MLBConstants.STANDARD_BATTING][season][MLBConstants.AT_BATS] = MLBUtilities.resolve_value(td.text, "int")
				elif i == 7:
					self.player_data[MLBConstants.STANDARD_BATTING][season][MLBConstants.RUNS] = MLBUtilities.resolve_value(td.text, "int")
				elif i == 8:
					self.player_data[MLBConstants.STANDARD_BATTING][season][MLBConstants.HITS] = MLBUtilities.resolve_value(td.text, "int")
				elif i == 9:
					self.player_data[MLBConstants.STANDARD_BATTING][season][MLBConstants.DOUBLES] = MLBUtilities.resolve_value(td.text, "int")
				elif i == 10:
					self.player_data[MLBConstants.STANDARD_BATTING][season][MLBConstants.TRIPLES] = MLBUtilities.resolve_value(td.text, "int")
				elif i == 11:
					self.player_data[MLBConstants.STANDARD_BATTING][season][MLBConstants.HOME_RUNS] = MLBUtilities.resolve_value(td.text, "int")
				elif i == 12:
					self.player_data[MLBConstants.STANDARD_BATTING][season][MLBConstants.RBI] = MLBUtilities.resolve_value(td.text, "int")
				elif i == 13:
					self.player_data[MLBConstants.STANDARD_BATTING][season][MLBConstants.STOLEN_BASES] = MLBUtilities.resolve_value(td.text, "int")
				elif i == 14:
					self.player_data[MLBConstants.STANDARD_BATTING][season][MLBConstants.CAUGHT_STEALING] = MLBUtilities.resolve_value(td.text, "int")
				elif i == 15:
					self.player_data[MLBConstants.STANDARD_BATTING][season][MLBConstants.WALKS] = MLBUtilities.resolve_value(td.text, "int")
				elif i == 16:
					self.player_data[MLBConstants.STANDARD_BATTING][season][MLBConstants.STRIKE_OUTS] = MLBUtilities.resolve_value(td.text, "int")
				elif i == 17:
					self.player_data[MLBConstants.STANDARD_BATTING][season][MLBConstants.BATTING_AVERAGE] = MLBUtilities.resolve_value(td.text, "float")
				elif i == 18:
					self.player_data[MLBConstants.STANDARD_BATTING][season][MLBConstants.ON_BASE_PERCENTAGE] = MLBUtilities.resolve_value(td.text, "float")
				elif i == 19:
					self.player_data[MLBConstants.STANDARD_BATTING][season][MLBConstants.SLUGGING_PERCENTAGE] = MLBUtilities.resolve_value(td.text, "float")
				elif i == 20:
					self.player_data[MLBConstants.STANDARD_BATTING][season][MLBConstants.OPS] = MLBUtilities.resolve_value(td.text, "float")
				elif i == 21:
					self.player_data[MLBConstants.STANDARD_BATTING][season][MLBConstants.OPS_PLUS] = MLBUtilities.resolve_value(td.text, "float")
				elif i == 22:
					self.player_data[MLBConstants.STANDARD_BATTING][season][MLBConstants.TOTAL_BASES] = MLBUtilities.resolve_value(td.text, "int")
				elif i == 23:
					self.player_data[MLBConstants.STANDARD_BATTING][season][MLBConstants.DOUBLE_PLAYS_GROUNDED_INTO] = MLBUtilities.resolve_value(td.text, "int")
				elif i == 24:
					self.player_data[MLBConstants.STANDARD_BATTING][season][MLBConstants.HIT_BY_PITCH] = MLBUtilities.resolve_value(td.text, "int")
				elif i == 25:
					self.player_data[MLBConstants.STANDARD_BATTING][season][MLBConstants.SACRIFICE_HITS] = MLBUtilities.resolve_value(td.text, "int")
				elif i == 26:
					self.player_data[MLBConstants.STANDARD_BATTING][season][MLBConstants.SACRIFICE_FLIES] = MLBUtilities.resolve_value(td.text, "int")
				elif i == 27:
					self.player_data[MLBConstants.STANDARD_BATTING][season][MLBConstants.INTENTIONAL_WALKS] = MLBUtilities.resolve_value(td.text, "int")
				elif i == 28:
					self.player_data[MLBConstants.STANDARD_BATTING][season][MLBConstants.POSITION] = td.text

				i += 1

			# Compute additional stats
			self.player_data[MLBConstants.STANDARD_BATTING][season][MLBConstants.WOBA] = self.stat_calculator.calculate_woba(self.player_data[MLBConstants.STANDARD_BATTING][season])

	def parse_player_value_batting(self, soup):
		"""
		Parses data from the Stanard Batting table.
		"""
		player_value_batting_entries = soup.find_all(id=self.player_value_batting_regex)

		for entry in player_value_batting_entries:
			tds = entry.find_all("td")

			i = 0
			season = ""
			for td in tds:
				if i == 0:
					season = td.text

					if MLBConstants.PLAYER_VALUE_BATTING not in self.player_data:
						self.player_data[MLBConstants.PLAYER_VALUE_BATTING] = {}

					self.player_data[MLBConstants.PLAYER_VALUE_BATTING][season] = {}
				elif i == 6:
					self.player_data[MLBConstants.PLAYER_VALUE_BATTING][season][MLBConstants.RUNS_BATTING] = MLBUtilities.resolve_value(td.text, "int")
				elif i == 7:
					self.player_data[MLBConstants.PLAYER_VALUE_BATTING][season][MLBConstants.RUNS_FROM_BASERUNNING] = MLBUtilities.resolve_value(td.text, "int")
				elif i == 8:
					self.player_data[MLBConstants.PLAYER_VALUE_BATTING][season][MLBConstants.RUNS_GROUNDED_INTO_DOUBLE_PLAY] = MLBUtilities.resolve_value(td.text, "int")
				elif i == 9:
					self.player_data[MLBConstants.PLAYER_VALUE_BATTING][season][MLBConstants.RUNS_FROM_FIELDING] = MLBUtilities.resolve_value(td.text, "int")
				elif i == 10:
					self.player_data[MLBConstants.PLAYER_VALUE_BATTING][season][MLBConstants.RUNS_FROM_POSITION_SCARCITY] = MLBUtilities.resolve_value(td.text, "int")
				elif i == 11:
					self.player_data[MLBConstants.PLAYER_VALUE_BATTING][season][MLBConstants.RAA] = MLBUtilities.resolve_value(td.text, "int")
				elif i == 12:
					self.player_data[MLBConstants.PLAYER_VALUE_BATTING][season][MLBConstants.WAA] = MLBUtilities.resolve_value(td.text, "float")
				elif i == 13:
					self.player_data[MLBConstants.PLAYER_VALUE_BATTING][season][MLBConstants.RUNS_FROM_REPLACEMENT_LEVEL] = MLBUtilities.resolve_value(td.text, "int")
				elif i == 14:
					self.player_data[MLBConstants.PLAYER_VALUE_BATTING][season][MLBConstants.RAR] = MLBUtilities.resolve_value(td.text, "float")
				elif i == 15:
					self.player_data[MLBConstants.PLAYER_VALUE_BATTING][season][MLBConstants.WAR] = MLBUtilities.resolve_value(td.text, "float")
				elif i == 16:
					self.player_data[MLBConstants.PLAYER_VALUE_BATTING][season][MLBConstants.WIN_LOSS_PCT_WITH_AVG_TEAM] = MLBUtilities.resolve_value(td.text, "float")
				elif i == 17:
					self.player_data[MLBConstants.PLAYER_VALUE_BATTING][season][MLBConstants.WIN_LOSS_PCT_WITH_AVG_TEAM_SEASON] = MLBUtilities.resolve_value(td.text, "float")
				elif i == 18:
					self.player_data[MLBConstants.PLAYER_VALUE_BATTING][season][MLBConstants.OFF_WAR] = MLBUtilities.resolve_value(td.text, "float")
				elif i == 19:
					self.player_data[MLBConstants.PLAYER_VALUE_BATTING][season][MLBConstants.DEF_WAR] = MLBUtilities.resolve_value(td.text, "float")
				elif i == 20:
					self.player_data[MLBConstants.PLAYER_VALUE_BATTING][season][MLBConstants.OFF_RAR] = MLBUtilities.resolve_value(td.text, "float")

				i += 1