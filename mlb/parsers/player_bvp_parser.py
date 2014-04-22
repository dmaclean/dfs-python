import re
from bs4 import BeautifulSoup
from mlb.constants.mlb_constants import MLBConstants
from mlb.utilities.mlb_utilities import MLBUtilities

__author__ = 'dan'


class PlayerBvPParser:
	"""
	Parser for the Batter vs Pitcher page.
	"""

	def __init__(self, player_data=None, type=None):
		self.player_data = player_data
		self.type = type

		self.pitcher_id_regex = re.compile(".*?pitcher=([0-9a-z_\.]+)")
		self.batter_id_regex = re.compile(".*?batter=([0-9a-z_\'\.]+)&.*?")

	def parse(self, data):
		"""
		Parse data from the batter vs pitcher page.
		"""
		soup = BeautifulSoup(data)

		if MLBConstants.BATTER_VS_PITCHER not in self.player_data:
			self.player_data[MLBConstants.BATTER_VS_PITCHER] = {}

		table = soup.find("table", attrs={"id": "ajax_result_table"})
		trs = table.find_all("tr")
		for tr in trs:
			tds = tr.find_all("td")
			i = 0
			opponent_id = ""
			for td in tds:
				if i == 0:
					if self.type == MLBConstants.BATTER_TYPE:
						m = self.pitcher_id_regex.match(td.a.attrs["href"])
					else:
						m = self.batter_id_regex.match(td.a.attrs["href"])

					opponent_id = m.group(1).replace(".", "_")

					if opponent_id not in self.player_data[MLBConstants.BATTER_VS_PITCHER]:
						self.player_data[MLBConstants.BATTER_VS_PITCHER][opponent_id] = {}

					self.player_data[MLBConstants.BATTER_VS_PITCHER][opponent_id][MLBConstants.NAME] = td.a.text
				elif i == 1:
					self.player_data[MLBConstants.BATTER_VS_PITCHER][opponent_id][
						MLBConstants.PLATE_APPEARANCES] = MLBUtilities.resolve_value(td.text, "int")
				elif i == 2:
					self.player_data[MLBConstants.BATTER_VS_PITCHER][opponent_id][
						MLBConstants.AT_BATS] = MLBUtilities.resolve_value(td.text, "int")
				elif i == 3:
					self.player_data[MLBConstants.BATTER_VS_PITCHER][opponent_id][
						MLBConstants.HITS] = MLBUtilities.resolve_value(td.text, "int")
				elif i == 4:
					self.player_data[MLBConstants.BATTER_VS_PITCHER][opponent_id][
						MLBConstants.DOUBLES] = MLBUtilities.resolve_value(td.text, "int")
				elif i == 5:
					self.player_data[MLBConstants.BATTER_VS_PITCHER][opponent_id][
						MLBConstants.TRIPLES] = MLBUtilities.resolve_value(td.text, "int")
				elif i == 6:
					self.player_data[MLBConstants.BATTER_VS_PITCHER][opponent_id][
						MLBConstants.HOME_RUNS] = MLBUtilities.resolve_value(td.text, "int")
				elif i == 7:
					self.player_data[MLBConstants.BATTER_VS_PITCHER][opponent_id][
						MLBConstants.RBI] = MLBUtilities.resolve_value(td.text, "int")
				elif i == 8:
					self.player_data[MLBConstants.BATTER_VS_PITCHER][opponent_id][
						MLBConstants.WALKS] = MLBUtilities.resolve_value(td.text, "int")
				elif i == 9:
					self.player_data[MLBConstants.BATTER_VS_PITCHER][opponent_id][
						MLBConstants.STRIKE_OUTS] = MLBUtilities.resolve_value(td.text, "int")
				elif i == 10:
					self.player_data[MLBConstants.BATTER_VS_PITCHER][opponent_id][
						MLBConstants.BATTING_AVERAGE] = MLBUtilities.resolve_value(td.text, "float")
				elif i == 11:
					self.player_data[MLBConstants.BATTER_VS_PITCHER][opponent_id][
						MLBConstants.ON_BASE_PERCENTAGE] = MLBUtilities.resolve_value(td.text, "float")
				elif i == 12:
					self.player_data[MLBConstants.BATTER_VS_PITCHER][opponent_id][
						MLBConstants.SLUGGING_PERCENTAGE] = MLBUtilities.resolve_value(td.text, "float")
				elif i == 13:
					self.player_data[MLBConstants.BATTER_VS_PITCHER][opponent_id][
						MLBConstants.OPS] = MLBUtilities.resolve_value(td.text, "float")
				elif i == 14:
					self.player_data[MLBConstants.BATTER_VS_PITCHER][opponent_id][
						MLBConstants.SACRIFICE_HITS] = MLBUtilities.resolve_value(td.text, "int")
				elif i == 15:
					self.player_data[MLBConstants.BATTER_VS_PITCHER][opponent_id][
						MLBConstants.SACRIFICE_FLIES] = MLBUtilities.resolve_value(td.text, "int")
				elif i == 16:
					self.player_data[MLBConstants.BATTER_VS_PITCHER][opponent_id][
						MLBConstants.INTENTIONAL_WALKS] = MLBUtilities.resolve_value(td.text, "int")
				elif i == 17:
					self.player_data[MLBConstants.BATTER_VS_PITCHER][opponent_id][
						MLBConstants.HIT_BY_PITCH] = MLBUtilities.resolve_value(td.text, "int")
				elif i == 18:
					self.player_data[MLBConstants.BATTER_VS_PITCHER][opponent_id][
						MLBConstants.DOUBLE_PLAYS_GROUNDED_INTO] = MLBUtilities.resolve_value(td.text, "int")

				i += 1