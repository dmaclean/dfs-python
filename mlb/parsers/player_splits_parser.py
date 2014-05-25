from bs4 import BeautifulSoup
from mlb.constants.mlb_constants import MLBConstants
from mlb.models.stat_calculator import StatCalculator
from mlb.utilities.mlb_utilities import MLBUtilities

__author__ = 'dan'


class PlayerSplitsParser:
	"""
	Parser for the pitcher and batter splits pages.
	"""

	def __init__(self, player_data=None):
		self.player_data = player_data
		self.stat_calculator = StatCalculator()

	def parse(self, data, season):
		s = data.encode('ascii', 'ignore')

		# Terrible hack to fix bad HTML that uses a tbody close tag instead of an open tag.
		s = s.replace('\n','').replace("</colgroup></tbody>", "</colgroup>")
		soup = BeautifulSoup(s, 'html.parser')

		if self.player_data[MLBConstants.POSITION] == "Pitcher":
			self.parse_pitcher_splits(soup, season)
		else:
			self.parse_batter_splits(soup, season)

	def parse_pitcher_splits(self, soup, season):
		split_divs = soup.find_all("div", attrs={"class": "stw"})

		for split_div in split_divs:
			table = split_div.find("table")

			pitcher_extras = False
			if table.attrs["id"].find("_extra") > -1:
				pitcher_extras = True

			tbody = split_div.find("tbody")

			if(tbody is None):
				print ""

			trs = tbody.find_all("tr")

			for tr in trs:
				tds = tr.find_all("td")
				if len(tds) == 0:
					continue

				i = 0
				split_type = ""
				for td in tds:
					# There are (sometimes) two table for each split type for pitchers - normal and extras.  The id for
					# each extras table ends in "_extras", so when that is detected, we set a flag indicating that we're
					# processing an extras table.
					if not pitcher_extras:
						if i == 0:
							if MLBConstants.PITCHER_SPLITS not in self.player_data:
								self.player_data[MLBConstants.PITCHER_SPLITS] = {}

							if season not in self.player_data[MLBConstants.PITCHER_SPLITS]:
								self.player_data[MLBConstants.PITCHER_SPLITS][season] = {}

							split_type = td.text.replace(".", "_")
							if split_type not in self.player_data[MLBConstants.PITCHER_SPLITS][season]:
								self.player_data[MLBConstants.PITCHER_SPLITS][season][split_type] = {}
						elif i == 1 and not pitcher_extras:
							self.player_data[MLBConstants.PITCHER_SPLITS][season][split_type][
								MLBConstants.GAMES_PLAYED] = MLBUtilities.resolve_value(td.text, "int")
						elif i == 2 and not pitcher_extras:
							self.player_data[MLBConstants.PITCHER_SPLITS][season][split_type][
								MLBConstants.PLATE_APPEARANCES] = MLBUtilities.resolve_value(td.text, "int")
						elif i == 3 and not pitcher_extras:
							self.player_data[MLBConstants.PITCHER_SPLITS][season][split_type][
								MLBConstants.AT_BATS] = MLBUtilities.resolve_value(td.text, "int")
						elif i == 4 and not pitcher_extras:
							self.player_data[MLBConstants.PITCHER_SPLITS][season][split_type][
								MLBConstants.RUNS] = MLBUtilities.resolve_value(td.text, "int")
						elif i == 5 and not pitcher_extras:
							self.player_data[MLBConstants.PITCHER_SPLITS][season][split_type][
								MLBConstants.HITS] = MLBUtilities.resolve_value(td.text, "int")
						elif i == 6 and not pitcher_extras:
							self.player_data[MLBConstants.PITCHER_SPLITS][season][split_type][
								MLBConstants.DOUBLES] = MLBUtilities.resolve_value(td.text, "int")
						elif i == 7 and not pitcher_extras:
							self.player_data[MLBConstants.PITCHER_SPLITS][season][split_type][
								MLBConstants.TRIPLES] = MLBUtilities.resolve_value(td.text, "int")
						elif i == 8 and not pitcher_extras:
							self.player_data[MLBConstants.PITCHER_SPLITS][season][split_type][
								MLBConstants.HOME_RUNS] = MLBUtilities.resolve_value(td.text, "int")
						elif i == 9 and not pitcher_extras:
							self.player_data[MLBConstants.PITCHER_SPLITS][season][split_type][
								MLBConstants.STOLEN_BASES] = MLBUtilities.resolve_value(td.text, "int")
						elif i == 10 and not pitcher_extras:
							self.player_data[MLBConstants.PITCHER_SPLITS][season][split_type][
								MLBConstants.CAUGHT_STEALING] = MLBUtilities.resolve_value(td.text, "int")
						elif i == 11 and not pitcher_extras:
							self.player_data[MLBConstants.PITCHER_SPLITS][season][split_type][
								MLBConstants.WALKS] = MLBUtilities.resolve_value(td.text, "int")
						elif i == 12 and not pitcher_extras:
							self.player_data[MLBConstants.PITCHER_SPLITS][season][split_type][
								MLBConstants.STRIKE_OUTS] = MLBUtilities.resolve_value(td.text, "int")
						elif i == 13 and not pitcher_extras:
							self.player_data[MLBConstants.PITCHER_SPLITS][season][split_type][
								MLBConstants.STRIKE_OUT_TO_WALK_RATIO] = MLBUtilities.resolve_value(td.text, "float")
						elif i == 14 and not pitcher_extras:
							self.player_data[MLBConstants.PITCHER_SPLITS][season][split_type][
								MLBConstants.BATTING_AVERAGE] = MLBUtilities.resolve_value(td.text, "float")
						elif i == 15 and not pitcher_extras:
							self.player_data[MLBConstants.PITCHER_SPLITS][season][split_type][
								MLBConstants.ON_BASE_PERCENTAGE] = MLBUtilities.resolve_value(td.text, "float")
						elif i == 16 and not pitcher_extras:
							self.player_data[MLBConstants.PITCHER_SPLITS][season][split_type][
								MLBConstants.SLUGGING_PERCENTAGE] = MLBUtilities.resolve_value(td.text, "float")
						elif i == 17 and not pitcher_extras:
							self.player_data[MLBConstants.PITCHER_SPLITS][season][split_type][
								MLBConstants.OPS] = MLBUtilities.resolve_value(td.text, "float")
						elif i == 18 and not pitcher_extras:
							self.player_data[MLBConstants.PITCHER_SPLITS][season][split_type][
								MLBConstants.TOTAL_BASES] = MLBUtilities.resolve_value(td.text, "int")
						elif i == 19 and not pitcher_extras:
							self.player_data[MLBConstants.PITCHER_SPLITS][season][split_type][
								MLBConstants.DOUBLE_PLAYS_GROUNDED_INTO] = MLBUtilities.resolve_value(td.text, "int")
						elif i == 20 and not pitcher_extras:
							self.player_data[MLBConstants.PITCHER_SPLITS][season][split_type][
								MLBConstants.HIT_BY_PITCH] = MLBUtilities.resolve_value(td.text, "int")
						elif i == 21 and not pitcher_extras:
							self.player_data[MLBConstants.PITCHER_SPLITS][season][split_type][
								MLBConstants.SACRIFICE_HITS] = MLBUtilities.resolve_value(td.text, "int")
						elif i == 22 and not pitcher_extras:
							self.player_data[MLBConstants.PITCHER_SPLITS][season][split_type][
								MLBConstants.SACRIFICE_FLIES] = MLBUtilities.resolve_value(td.text, "int")
						elif i == 23 and not pitcher_extras:
							self.player_data[MLBConstants.PITCHER_SPLITS][season][split_type][
								MLBConstants.INTENTIONAL_WALKS] = MLBUtilities.resolve_value(td.text, "int")
						elif i == 24 and not pitcher_extras:
							self.player_data[MLBConstants.PITCHER_SPLITS][season][split_type][
								MLBConstants.REACHED_ON_ERROR] = MLBUtilities.resolve_value(td.text, "int")
						elif i == 25 and not pitcher_extras:
							self.player_data[MLBConstants.PITCHER_SPLITS][season][split_type][
								MLBConstants.BABIP] = MLBUtilities.resolve_value(td.text, "float")
						elif i == 26 and not pitcher_extras:
							self.player_data[MLBConstants.PITCHER_SPLITS][season][split_type][
								MLBConstants.T_OPS_PLUS] = MLBUtilities.resolve_value(td.text, "int")
						elif i == 27 and not pitcher_extras:
							self.player_data[MLBConstants.PITCHER_SPLITS][season][split_type][
								MLBConstants.S_OPS_PLUS] = MLBUtilities.resolve_value(td.text, "int")
					else:
						if i == 1 and pitcher_extras:
							if MLBConstants.PITCHER_SPLITS not in self.player_data:
								self.player_data[MLBConstants.PITCHER_SPLITS] = {}

							if season not in self.player_data[MLBConstants.PITCHER_SPLITS]:
								self.player_data[MLBConstants.PITCHER_SPLITS][season] = {}

							split_type = td.text.replace(".", "_")
							if td.text not in self.player_data[MLBConstants.PITCHER_SPLITS][season]:
								self.player_data[MLBConstants.PITCHER_SPLITS][season][split_type] = {}
						elif i == 2 and pitcher_extras:
							self.player_data[MLBConstants.PITCHER_SPLITS][season][split_type][
								MLBConstants.WINS] = MLBUtilities.resolve_value(td.text, "int")
						elif i == 3 and pitcher_extras:
							self.player_data[MLBConstants.PITCHER_SPLITS][season][split_type][
								MLBConstants.LOSSES] = MLBUtilities.resolve_value(td.text, "int")
						elif i == 4 and pitcher_extras:
							self.player_data[MLBConstants.PITCHER_SPLITS][season][split_type][
								MLBConstants.WIN_LOSS_PCT] = MLBUtilities.resolve_value(td.text, "float")
						elif i == 5 and pitcher_extras:
							self.player_data[MLBConstants.PITCHER_SPLITS][season][split_type][
								MLBConstants.ERA] = MLBUtilities.resolve_value(td.text, "float")
						# elif i == 6 and pitcher_extras:
						# 	self.player_data[MLBConstants.PITCHER_SPLITS][season][split_type][
						# 		MLBConstants.GAMES_PLAYED] = MLBUtilities.resolve_value(td.text, "int")
						elif i == 7 and pitcher_extras:
							self.player_data[MLBConstants.PITCHER_SPLITS][season][split_type][
								MLBConstants.GAMES_STARTED] = MLBUtilities.resolve_value(td.text, "int")
						elif i == 8 and pitcher_extras:
							self.player_data[MLBConstants.PITCHER_SPLITS][season][split_type][
								MLBConstants.GAMES_FINISHED] = MLBUtilities.resolve_value(td.text, "int")
						elif i == 9 and pitcher_extras:
							self.player_data[MLBConstants.PITCHER_SPLITS][season][split_type][
								MLBConstants.COMPLETE_GAMES] = MLBUtilities.resolve_value(td.text, "int")
						elif i == 10 and pitcher_extras:
							self.player_data[MLBConstants.PITCHER_SPLITS][season][split_type][
								MLBConstants.SHUT_OUTS] = MLBUtilities.resolve_value(td.text, "int")
						elif i == 11 and pitcher_extras:
							self.player_data[MLBConstants.PITCHER_SPLITS][season][split_type][
								MLBConstants.SAVES] = MLBUtilities.resolve_value(td.text, "int")
						elif i == 12 and pitcher_extras:
							self.player_data[MLBConstants.PITCHER_SPLITS][season][split_type][
								MLBConstants.INNINGS_PITCHED] = MLBUtilities.resolve_value(td.text, "float")
						# elif i == 12 and pitcher_extras:
						# 	self.player_data[MLBConstants.PITCHER_SPLITS][season][split_type][
						# 		MLBConstants.HITS] = MLBUtilities.resolve_value(td.text, "int")
						elif i == 15 and pitcher_extras:
							self.player_data[MLBConstants.PITCHER_SPLITS][season][split_type][
								MLBConstants.EARNED_RUNS] = MLBUtilities.resolve_value(td.text, "int")
						elif i == 21 and pitcher_extras:
							self.player_data[MLBConstants.PITCHER_SPLITS][season][split_type][
								MLBConstants.BALKS] = MLBUtilities.resolve_value(td.text, "int")
						elif i == 22 and pitcher_extras:
							self.player_data[MLBConstants.PITCHER_SPLITS][season][split_type][
								MLBConstants.WILD_PITCHES] = MLBUtilities.resolve_value(td.text, "int")
						elif i == 24 and pitcher_extras:
							self.player_data[MLBConstants.PITCHER_SPLITS][season][split_type][
								MLBConstants.WHIP] = MLBUtilities.resolve_value(td.text, "float")
						elif i == 25 and pitcher_extras:
							self.player_data[MLBConstants.PITCHER_SPLITS][season][split_type][
								MLBConstants.STRIKE_OUTS_PER_9_INNINGS] = MLBUtilities.resolve_value(td.text, "float")

					i += 1

				self.player_data[MLBConstants.PITCHER_SPLITS][season][split_type][
								MLBConstants.FIP] = self.stat_calculator.calculate_fip(self.player_data[MLBConstants.PITCHER_SPLITS][season][split_type])
				self.player_data[MLBConstants.PITCHER_SPLITS][season][split_type][MLBConstants.WOBA] = self.stat_calculator.calculate_woba(self.player_data[MLBConstants.PITCHER_SPLITS][season][split_type])

	def parse_batter_splits(self, soup, season):
		split_divs = soup.find_all("div", attrs={"class": "stw"})

		for split_div in split_divs:
			label = split_div.find("div", attrs={"class": "table_heading"}).a.h4.text
			trs = split_div.find_all("tr")

			for tr in trs:
				tds = tr.find_all("td")
				if len(tds) == 0:
					continue

				i = 0
				split_type = ""
				for td in tds:
					if i == 0:
						if td.text == "":
							continue

						if MLBConstants.BATTER_SPLITS not in self.player_data:
							self.player_data[MLBConstants.BATTER_SPLITS] = {}

						if season not in self.player_data[MLBConstants.BATTER_SPLITS]:
							self.player_data[MLBConstants.BATTER_SPLITS][season] = {}

						split_type = td.text.replace(".", "_")
						if split_type not in self.player_data[MLBConstants.BATTER_SPLITS][season]:
							self.player_data[MLBConstants.BATTER_SPLITS][season][split_type] = {}
					elif i == 1:
						self.player_data[MLBConstants.BATTER_SPLITS][season][split_type][
							MLBConstants.GAMES_PLAYED] = MLBUtilities.resolve_value(td.text, "int")
					elif i == 2:
						self.player_data[MLBConstants.BATTER_SPLITS][season][split_type][
							MLBConstants.GAMES_STARTED] = MLBUtilities.resolve_value(td.text, "int")
					elif i == 3:
						self.player_data[MLBConstants.BATTER_SPLITS][season][split_type][
							MLBConstants.PLATE_APPEARANCES] = MLBUtilities.resolve_value(td.text, "int")
					elif i == 4:
						self.player_data[MLBConstants.BATTER_SPLITS][season][split_type][
							MLBConstants.AT_BATS] = MLBUtilities.resolve_value(td.text, "int")
					elif i == 5:
						self.player_data[MLBConstants.BATTER_SPLITS][season][split_type][
							MLBConstants.RUNS] = MLBUtilities.resolve_value(td.text, "int")
					elif i == 6:
						self.player_data[MLBConstants.BATTER_SPLITS][season][split_type][
							MLBConstants.HITS] = MLBUtilities.resolve_value(td.text, "int")
					elif i == 7:
						self.player_data[MLBConstants.BATTER_SPLITS][season][split_type][
							MLBConstants.DOUBLES] = MLBUtilities.resolve_value(td.text, "int")
					elif i == 8:
						self.player_data[MLBConstants.BATTER_SPLITS][season][split_type][
							MLBConstants.TRIPLES] = MLBUtilities.resolve_value(td.text, "int")
					elif i == 9:
						self.player_data[MLBConstants.BATTER_SPLITS][season][split_type][
							MLBConstants.HOME_RUNS] = MLBUtilities.resolve_value(td.text, "int")
					elif i == 10:
						self.player_data[MLBConstants.BATTER_SPLITS][season][split_type][
							MLBConstants.RBI] = MLBUtilities.resolve_value(td.text, "int")
					elif i == 11:
						self.player_data[MLBConstants.BATTER_SPLITS][season][split_type][
							MLBConstants.STOLEN_BASES] = MLBUtilities.resolve_value(td.text, "int")
					elif i == 12:
						self.player_data[MLBConstants.BATTER_SPLITS][season][split_type][
							MLBConstants.CAUGHT_STEALING] = MLBUtilities.resolve_value(td.text, "int")
					elif i == 13:
						self.player_data[MLBConstants.BATTER_SPLITS][season][split_type][
							MLBConstants.WALKS] = MLBUtilities.resolve_value(td.text, "int")
					elif i == 14:
						self.player_data[MLBConstants.BATTER_SPLITS][season][split_type][
							MLBConstants.STRIKE_OUTS] = MLBUtilities.resolve_value(td.text, "int")
					elif i == 15:
						self.player_data[MLBConstants.BATTER_SPLITS][season][split_type][
							MLBConstants.BATTING_AVERAGE] = MLBUtilities.resolve_value(td.text, "float")
					elif i == 16:
						self.player_data[MLBConstants.BATTER_SPLITS][season][split_type][
							MLBConstants.ON_BASE_PERCENTAGE] = MLBUtilities.resolve_value(td.text, "float")
					elif i == 17:
						self.player_data[MLBConstants.BATTER_SPLITS][season][split_type][
							MLBConstants.SLUGGING_PERCENTAGE] = MLBUtilities.resolve_value(td.text, "float")
					elif i == 18:
						self.player_data[MLBConstants.BATTER_SPLITS][season][split_type][
							MLBConstants.OPS] = MLBUtilities.resolve_value(td.text, "float")
					elif i == 19:
						self.player_data[MLBConstants.BATTER_SPLITS][season][split_type][
							MLBConstants.TOTAL_BASES] = MLBUtilities.resolve_value(td.text, "int")
					elif i == 20:
						self.player_data[MLBConstants.BATTER_SPLITS][season][split_type][
							MLBConstants.DOUBLE_PLAYS_GROUNDED_INTO] = MLBUtilities.resolve_value(td.text, "int")
					elif i == 21:
						self.player_data[MLBConstants.BATTER_SPLITS][season][split_type][
							MLBConstants.HIT_BY_PITCH] = MLBUtilities.resolve_value(td.text, "int")
					elif i == 22:
						self.player_data[MLBConstants.BATTER_SPLITS][season][split_type][
							MLBConstants.SACRIFICE_HITS] = MLBUtilities.resolve_value(td.text, "int")
					elif i == 23:
						self.player_data[MLBConstants.BATTER_SPLITS][season][split_type][
							MLBConstants.SACRIFICE_FLIES] = MLBUtilities.resolve_value(td.text, "int")
					elif i == 24:
						self.player_data[MLBConstants.BATTER_SPLITS][season][split_type][
							MLBConstants.INTENTIONAL_WALKS] = MLBUtilities.resolve_value(td.text, "int")
					elif i == 25:
						self.player_data[MLBConstants.BATTER_SPLITS][season][split_type][
							MLBConstants.REACHED_ON_ERROR] = MLBUtilities.resolve_value(td.text, "int")
					elif i == 26:
						self.player_data[MLBConstants.BATTER_SPLITS][season][split_type][
							MLBConstants.BABIP] = MLBUtilities.resolve_value(td.text, "float")
					elif i == 27:
						self.player_data[MLBConstants.BATTER_SPLITS][season][split_type][
							MLBConstants.T_OPS_PLUS] = MLBUtilities.resolve_value(td.text, "int")
					elif i == 28:
						self.player_data[MLBConstants.BATTER_SPLITS][season][split_type][
							MLBConstants.S_OPS_PLUS] = MLBUtilities.resolve_value(td.text, "int")

					i += 1

				self.player_data[MLBConstants.BATTER_SPLITS][season][split_type][
							MLBConstants.WOBA] = self.stat_calculator.calculate_woba(self.player_data[MLBConstants.BATTER_SPLITS][season][split_type])