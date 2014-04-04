import re

from bs4 import BeautifulSoup
from time import strptime
from mlb.constants.mlb_constants import MLBConstants
from mlb.utilities.mlb_utilities import MLBUtilities

__author__ = 'dan'


class PlayerGamelogParser:
	"""
	Parser for the player gamelogs.
	"""

	def __init__(self, player_data=None, season=None, type=None):
		self.player_data = player_data
		self.season = season
		self.type = type

		self.pitching_gamelog_regex = re.compile("pitching_gamelogs\.\d+")
		self.batting_gamelog_regex = re.compile("batting_gamelogs\.\d+")
		self.result_regex = re.compile("([W|L]),(\d+)-(\d+)")

	def parse(self, data):
		"""
		Parse data from the player's gamelog for a particular season.
		"""
		soup = BeautifulSoup(data)

		if self.type == MLBConstants.PITCHER_TYPE:
			self.parse_pitching_stats(soup)
		else:
			self.parse_batting_stats(soup)

	def parse_pitching_stats(self, soup):
		"""
		Parse gamelog pitching stats.
		"""
		pitching_gamelog_entries = soup.find_all(id=self.pitching_gamelog_regex)

		for entry in pitching_gamelog_entries:
			tds = entry.find_all("td")

			i = 0
			game_number = 0
			for td in tds:
				if i == 2:
					game_number = td.text

					if MLBConstants.PLAYER_GAMELOG_PITCHING not in self.player_data:
						self.player_data[MLBConstants.PLAYER_GAMELOG_PITCHING] = {}

					if self.season not in self.player_data[MLBConstants.PLAYER_GAMELOG_PITCHING]:
						self.player_data[MLBConstants.PLAYER_GAMELOG_PITCHING][self.season] = {}

					if game_number not in self.player_data[MLBConstants.PLAYER_GAMELOG_PITCHING][self.season]:
						self.player_data[MLBConstants.PLAYER_GAMELOG_PITCHING][self.season][game_number] = {}
				elif i == 3:
					self.player_data[MLBConstants.PLAYER_GAMELOG_PITCHING][self.season][game_number][
						MLBConstants.DATE] = strptime("{} {}".format(td.a.text.replace(u'\xa0', u' '), self.season), "%b %d %Y")
				elif i == 4:
					self.player_data[MLBConstants.PLAYER_GAMELOG_PITCHING][self.season][game_number][
						MLBConstants.TEAM] = td.a.text
				elif i == 5:
					self.player_data[MLBConstants.PLAYER_GAMELOG_PITCHING][self.season][game_number][
						MLBConstants.HOME_GAME] = False if td.text == "@" else True
				elif i == 6:
					self.player_data[MLBConstants.PLAYER_GAMELOG_PITCHING][self.season][game_number][
						MLBConstants.OPPONENT] = td.a.text
				elif i == 7:
					m = self.result_regex.match(td.text)
					self.player_data[MLBConstants.PLAYER_GAMELOG_PITCHING][self.season][game_number][
						MLBConstants.RESULT] = m.group(1)
					self.player_data[MLBConstants.PLAYER_GAMELOG_PITCHING][self.season][game_number][
						MLBConstants.TEAM_SCORE] = int(m.group(2))
					self.player_data[MLBConstants.PLAYER_GAMELOG_PITCHING][self.season][game_number][
						MLBConstants.OPPONENT_SCORE] = int(m.group(3))
				elif i == 8:
					self.player_data[MLBConstants.PLAYER_GAMELOG_PITCHING][self.season][game_number][
						MLBConstants.INNINGS] = td.text
				elif i == 9:
					self.player_data[MLBConstants.PLAYER_GAMELOG_PITCHING][self.season][game_number][
						MLBConstants.DECISION] = td.text
				elif i == 10:
					self.player_data[MLBConstants.PLAYER_GAMELOG_PITCHING][self.season][game_number][
						MLBConstants.DAYS_REST] = MLBUtilities.resolve_value(td.text, "int")
				elif i == 11:
					self.player_data[MLBConstants.PLAYER_GAMELOG_PITCHING][self.season][game_number][
						MLBConstants.INNINGS_PITCHED] = MLBUtilities.resolve_value(td.span.text, "float")
				elif i == 12:
					self.player_data[MLBConstants.PLAYER_GAMELOG_PITCHING][self.season][game_number][
						MLBConstants.HITS] = MLBUtilities.resolve_value(td.text, "int")
				elif i == 13:
					self.player_data[MLBConstants.PLAYER_GAMELOG_PITCHING][self.season][game_number][
						MLBConstants.RUNS] = MLBUtilities.resolve_value(td.text, "int")
				elif i == 14:
					self.player_data[MLBConstants.PLAYER_GAMELOG_PITCHING][self.season][game_number][
						MLBConstants.EARNED_RUNS] = MLBUtilities.resolve_value(td.text, "int")
				elif i == 15:
					self.player_data[MLBConstants.PLAYER_GAMELOG_PITCHING][self.season][game_number][
						MLBConstants.WALKS] = MLBUtilities.resolve_value(td.text, "int")
				elif i == 16:
					self.player_data[MLBConstants.PLAYER_GAMELOG_PITCHING][self.season][game_number][
						MLBConstants.STRIKE_OUTS] = MLBUtilities.resolve_value(td.text, "int")
				elif i == 17:
					self.player_data[MLBConstants.PLAYER_GAMELOG_PITCHING][self.season][game_number][
						MLBConstants.HOME_RUNS] = MLBUtilities.resolve_value(td.text, "int")
				elif i == 18:
					self.player_data[MLBConstants.PLAYER_GAMELOG_PITCHING][self.season][game_number][
						MLBConstants.HIT_BY_PITCH] = MLBUtilities.resolve_value(td.text, "int")
				elif i == 19:
					self.player_data[MLBConstants.PLAYER_GAMELOG_PITCHING][self.season][game_number][
						MLBConstants.ERA] = MLBUtilities.resolve_value(td.text, "float")
				elif i == 20:
					self.player_data[MLBConstants.PLAYER_GAMELOG_PITCHING][self.season][game_number][
						MLBConstants.BATTERS_FACED] = MLBUtilities.resolve_value(td.text, "int")
				elif i == 21:
					self.player_data[MLBConstants.PLAYER_GAMELOG_PITCHING][self.season][game_number][
						MLBConstants.NUM_PITCHES] = MLBUtilities.resolve_value(td.a.text, "int")
				elif i == 22:
					self.player_data[MLBConstants.PLAYER_GAMELOG_PITCHING][self.season][game_number][
						MLBConstants.STRIKES] = MLBUtilities.resolve_value(td.text, "int")
				elif i == 23:
					self.player_data[MLBConstants.PLAYER_GAMELOG_PITCHING][self.season][game_number][
						MLBConstants.STRIKES_LOOKING] = MLBUtilities.resolve_value(td.text, "int")
				elif i == 24:
					self.player_data[MLBConstants.PLAYER_GAMELOG_PITCHING][self.season][game_number][
						MLBConstants.STRIKES_SWINGING] = MLBUtilities.resolve_value(td.text, "int")
				elif i == 25:
					self.player_data[MLBConstants.PLAYER_GAMELOG_PITCHING][self.season][game_number][
						MLBConstants.GROUND_BALLS] = MLBUtilities.resolve_value(td.text, "int")
				elif i == 26:
					self.player_data[MLBConstants.PLAYER_GAMELOG_PITCHING][self.season][game_number][
						MLBConstants.FLY_BALLS] = MLBUtilities.resolve_value(td.text, "int")
				elif i == 27:
					self.player_data[MLBConstants.PLAYER_GAMELOG_PITCHING][self.season][game_number][
						MLBConstants.LINE_DRIVES] = MLBUtilities.resolve_value(td.text, "int")
				elif i == 28:
					self.player_data[MLBConstants.PLAYER_GAMELOG_PITCHING][self.season][game_number][
						MLBConstants.POP_UPS] = MLBUtilities.resolve_value(td.text, "int")
				elif i == 29:
					self.player_data[MLBConstants.PLAYER_GAMELOG_PITCHING][self.season][game_number][
						MLBConstants.UNKNOWN_BATTED_BALLS] = MLBUtilities.resolve_value(td.text, "int")
				elif i == 30:
					self.player_data[MLBConstants.PLAYER_GAMELOG_PITCHING][self.season][game_number][
						MLBConstants.PLAYER_GAME_SCORE] = td.text
				elif i == 31:
					self.player_data[MLBConstants.PLAYER_GAMELOG_PITCHING][self.season][game_number][
						MLBConstants.INHERITED_RUNNERS] = MLBUtilities.resolve_value(td.text, "int")
				elif i == 32:
					self.player_data[MLBConstants.PLAYER_GAMELOG_PITCHING][self.season][game_number][
						MLBConstants.INHERITED_SCORE] = MLBUtilities.resolve_value(td.text, "int")
				elif i == 33:
					self.player_data[MLBConstants.PLAYER_GAMELOG_PITCHING][self.season][game_number][
						MLBConstants.STOLEN_BASES] = MLBUtilities.resolve_value(td.text, "int")
				elif i == 34:
					self.player_data[MLBConstants.PLAYER_GAMELOG_PITCHING][self.season][game_number][
						MLBConstants.CAUGHT_STEALING] = MLBUtilities.resolve_value(td.text, "int")
				elif i == 35:
					self.player_data[MLBConstants.PLAYER_GAMELOG_PITCHING][self.season][game_number][
						MLBConstants.PICK_OFFS] = MLBUtilities.resolve_value(td.text, "int")
				elif i == 36:
					self.player_data[MLBConstants.PLAYER_GAMELOG_PITCHING][self.season][game_number][
						MLBConstants.AT_BATS] = MLBUtilities.resolve_value(td.text, "int")
				elif i == 37:
					self.player_data[MLBConstants.PLAYER_GAMELOG_PITCHING][self.season][game_number][
						MLBConstants.DOUBLES] = MLBUtilities.resolve_value(td.text, "int")
				elif i == 38:
					self.player_data[MLBConstants.PLAYER_GAMELOG_PITCHING][self.season][game_number][
						MLBConstants.TRIPLES] = MLBUtilities.resolve_value(td.text, "int")
				elif i == 39:
					self.player_data[MLBConstants.PLAYER_GAMELOG_PITCHING][self.season][game_number][
						MLBConstants.INTENTIONAL_WALKS] = MLBUtilities.resolve_value(td.text, "int")
				elif i == 40:
					self.player_data[MLBConstants.PLAYER_GAMELOG_PITCHING][self.season][game_number][
						MLBConstants.DOUBLE_PLAYS_GROUNDED_INTO] = MLBUtilities.resolve_value(td.text, "int")
				elif i == 41:
					self.player_data[MLBConstants.PLAYER_GAMELOG_PITCHING][self.season][game_number][
						MLBConstants.SACRIFICE_FLIES] = MLBUtilities.resolve_value(td.text, "int")
				elif i == 42:
					self.player_data[MLBConstants.PLAYER_GAMELOG_PITCHING][self.season][game_number][
						MLBConstants.REACHED_ON_ERROR] = MLBUtilities.resolve_value(td.text, "int")
				elif i == 43:
					self.player_data[MLBConstants.PLAYER_GAMELOG_PITCHING][self.season][game_number][
						MLBConstants.AVERAGE_LEVERAGE_INDEX] = MLBUtilities.resolve_value(td.text, "float")
				elif i == 44:
					self.player_data[MLBConstants.PLAYER_GAMELOG_PITCHING][self.season][game_number][
						MLBConstants.WIN_PROBABILITY_ADDED_BY_PITCHER] = MLBUtilities.resolve_value(td.text, "float")
				elif i == 45:
					self.player_data[MLBConstants.PLAYER_GAMELOG_PITCHING][self.season][game_number][
						MLBConstants.BASE_OUT_RUNS_SAVED] = MLBUtilities.resolve_value(td.text, "float")
				elif i == 46:
					self.player_data[MLBConstants.PLAYER_GAMELOG_PITCHING][self.season][game_number][
						MLBConstants.ENTRY_SITUATION] = td.span.text.strip()
				elif i == 47:
					self.player_data[MLBConstants.PLAYER_GAMELOG_PITCHING][self.season][game_number][
						MLBConstants.EXIT_SITUATION] = td.text.strip()

				i += 1

	def parse_batting_stats(self, soup):
		"""
		Parse gamelog batting stats.
		"""
		battinging_gamelog_entries = soup.find_all(id=self.batting_gamelog_regex)

		for entry in battinging_gamelog_entries:
			tds = entry.find_all("td")

			i = 0
			game_number = 0
			for td in tds:
				if i == 2:
					game_number = td.text

					if MLBConstants.PLAYER_GAMELOG_BATTING not in self.player_data:
						self.player_data[MLBConstants.PLAYER_GAMELOG_BATTING] = {}

					if self.season not in self.player_data[MLBConstants.PLAYER_GAMELOG_BATTING]:
						self.player_data[MLBConstants.PLAYER_GAMELOG_BATTING][self.season] = {}

					if game_number not in self.player_data[MLBConstants.PLAYER_GAMELOG_BATTING][self.season]:
						self.player_data[MLBConstants.PLAYER_GAMELOG_BATTING][self.season][game_number] = {}
				elif i == 3:
					self.player_data[MLBConstants.PLAYER_GAMELOG_BATTING][self.season][game_number][
						MLBConstants.DATE] = strptime("{} {}".format(td.a.text.replace(u'\xa0', u' '), self.season), "%b %d %Y")
				elif i == 4:
					self.player_data[MLBConstants.PLAYER_GAMELOG_BATTING][self.season][game_number][
						MLBConstants.TEAM] = td.a.text
				elif i == 5:
					self.player_data[MLBConstants.PLAYER_GAMELOG_BATTING][self.season][game_number][
						MLBConstants.HOME_GAME] = False if td.text == "@" else True
				elif i == 6:
					self.player_data[MLBConstants.PLAYER_GAMELOG_BATTING][self.season][game_number][
						MLBConstants.OPPONENT] = td.a.text
				elif i == 7:
					m = self.result_regex.match(td.text)
					self.player_data[MLBConstants.PLAYER_GAMELOG_BATTING][self.season][game_number][
						MLBConstants.RESULT] = m.group(1)
					self.player_data[MLBConstants.PLAYER_GAMELOG_BATTING][self.season][game_number][
						MLBConstants.TEAM_SCORE] = int(m.group(2))
					self.player_data[MLBConstants.PLAYER_GAMELOG_BATTING][self.season][game_number][
						MLBConstants.OPPONENT_SCORE] = int(m.group(3))
				elif i == 8:
					self.player_data[MLBConstants.PLAYER_GAMELOG_BATTING][self.season][game_number][
						MLBConstants.INNINGS] = td.text
				elif i == 9:
					self.player_data[MLBConstants.PLAYER_GAMELOG_BATTING][self.season][game_number][
						MLBConstants.PLATE_APPEARANCES] = MLBUtilities.resolve_value(td.span.text, "int")
				elif i == 10:
					self.player_data[MLBConstants.PLAYER_GAMELOG_BATTING][self.season][game_number][
						MLBConstants.AT_BATS] = MLBUtilities.resolve_value(td.text, "int")
				elif i == 11:
					self.player_data[MLBConstants.PLAYER_GAMELOG_BATTING][self.season][game_number][
						MLBConstants.RUNS] = MLBUtilities.resolve_value(td.text, "int")
				elif i == 12:
					self.player_data[MLBConstants.PLAYER_GAMELOG_BATTING][self.season][game_number][
						MLBConstants.HITS] = MLBUtilities.resolve_value(td.text, "int")
				elif i == 13:
					self.player_data[MLBConstants.PLAYER_GAMELOG_BATTING][self.season][game_number][
						MLBConstants.DOUBLES] = MLBUtilities.resolve_value(td.text, "int")
				elif i == 14:
					self.player_data[MLBConstants.PLAYER_GAMELOG_BATTING][self.season][game_number][
						MLBConstants.TRIPLES] = MLBUtilities.resolve_value(td.text, "int")
				elif i == 15:
					self.player_data[MLBConstants.PLAYER_GAMELOG_BATTING][self.season][game_number][
						MLBConstants.HOME_RUNS] = MLBUtilities.resolve_value(td.text, "int")
				elif i == 16:
					self.player_data[MLBConstants.PLAYER_GAMELOG_BATTING][self.season][game_number][
						MLBConstants.RBI] = MLBUtilities.resolve_value(td.text, "int")
				elif i == 17:
					self.player_data[MLBConstants.PLAYER_GAMELOG_BATTING][self.season][game_number][
						MLBConstants.WALKS] = MLBUtilities.resolve_value(td.text, "int")
				elif i == 18:
					self.player_data[MLBConstants.PLAYER_GAMELOG_BATTING][self.season][game_number][
						MLBConstants.INTENTIONAL_WALKS] = MLBUtilities.resolve_value(td.text, "int")
				elif i == 19:
					self.player_data[MLBConstants.PLAYER_GAMELOG_BATTING][self.season][game_number][
						MLBConstants.STRIKE_OUTS] = MLBUtilities.resolve_value(td.text, "int")
				elif i == 20:
					self.player_data[MLBConstants.PLAYER_GAMELOG_BATTING][self.season][game_number][
						MLBConstants.HIT_BY_PITCH] = MLBUtilities.resolve_value(td.text, "int")
				elif i == 21:
					self.player_data[MLBConstants.PLAYER_GAMELOG_BATTING][self.season][game_number][
						MLBConstants.SACRIFICE_HITS] = MLBUtilities.resolve_value(td.text, "int")
				elif i == 22:
					self.player_data[MLBConstants.PLAYER_GAMELOG_BATTING][self.season][game_number][
						MLBConstants.SACRIFICE_FLIES] = MLBUtilities.resolve_value(td.text, "int")
				elif i == 23:
					self.player_data[MLBConstants.PLAYER_GAMELOG_BATTING][self.season][game_number][
						MLBConstants.REACHED_ON_ERROR] = MLBUtilities.resolve_value(td.text, "int")
				elif i == 24:
					self.player_data[MLBConstants.PLAYER_GAMELOG_BATTING][self.season][game_number][
						MLBConstants.DOUBLE_PLAYS_GROUNDED_INTO] = MLBUtilities.resolve_value(td.text, "int")
				elif i == 25:
					self.player_data[MLBConstants.PLAYER_GAMELOG_BATTING][self.season][game_number][
						MLBConstants.STOLEN_BASES] = MLBUtilities.resolve_value(td.text, "int")
				elif i == 26:
					self.player_data[MLBConstants.PLAYER_GAMELOG_BATTING][self.season][game_number][
						MLBConstants.CAUGHT_STEALING] = MLBUtilities.resolve_value(td.text, "int")
				elif i == 27:
					self.player_data[MLBConstants.PLAYER_GAMELOG_BATTING][self.season][game_number][
						MLBConstants.BATTING_AVERAGE] = MLBUtilities.resolve_value(td.text, "float")
				elif i == 28:
					self.player_data[MLBConstants.PLAYER_GAMELOG_BATTING][self.season][game_number][
						MLBConstants.ON_BASE_PERCENTAGE] = MLBUtilities.resolve_value(td.text, "float")
				elif i == 29:
					self.player_data[MLBConstants.PLAYER_GAMELOG_BATTING][self.season][game_number][
						MLBConstants.SLUGGING_PERCENTAGE] = MLBUtilities.resolve_value(td.text, "float")
				elif i == 30:
					self.player_data[MLBConstants.PLAYER_GAMELOG_BATTING][self.season][game_number][
						MLBConstants.OPS] = MLBUtilities.resolve_value(td.text, "float")
				elif i == 31:
					self.player_data[MLBConstants.PLAYER_GAMELOG_BATTING][self.season][game_number][
						MLBConstants.BATTING_ORDER_POSITION] = MLBUtilities.resolve_value(td.text, "int")
				elif i == 32:
					self.player_data[MLBConstants.PLAYER_GAMELOG_BATTING][self.season][game_number][
						MLBConstants.AVERAGE_LEVERAGE_INDEX] = MLBUtilities.resolve_value(td.text, "float")
				elif i == 33:
					self.player_data[MLBConstants.PLAYER_GAMELOG_BATTING][self.season][game_number][
						MLBConstants.WIN_PROBABILITY_ADDED] = MLBUtilities.resolve_value(td.text, "float")
				elif i == 34:
					self.player_data[MLBConstants.PLAYER_GAMELOG_BATTING][self.season][game_number][
						MLBConstants.BASE_OUT_RUNS_ADDED] = MLBUtilities.resolve_value(td.text, "float")
				elif i == 35:
					self.player_data[MLBConstants.PLAYER_GAMELOG_BATTING][self.season][game_number][
						MLBConstants.POSITION] = td.text

				i += 1