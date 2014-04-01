from bs4 import BeautifulSoup
import re


class BasketballReferenceTeamGameLogParser():
	"""
	Parses a team's game log.
	"""
	def __init__(self):
		self.game_stats = {}

	def process(self, data):
		soup = BeautifulSoup(data)

		game_number = 1
		trs = soup.find_all(attrs={"id": re.compile("tgl_basic\.\d+")})
		for tr in trs:
			td_count = 0
			for td in tr.find_all("td"):
				td_count += 1

				# Game number
				if td_count == 2:
					game_number = int(td.span.get_text())
					self.game_stats[game_number] = {
						"minutes_played": 240,
						"result": "",
						"opp_free_throws": 0,
						"opp_free_throw_attempts": 0
					}
				# Date
				elif td_count == 3:
					self.game_stats[game_number]["date"] = td.a.string
				# # Home or Away
				elif td_count == 4:
					self.game_stats[game_number]["home"] = td.string != "@"
				# # Opponent
				elif td_count == 5:
					self.game_stats[game_number]["opponent"] = td.string
				# # Game Result (Win or loss)
				elif td_count == 6:
					self.game_stats[game_number]["result"] = "W" if td.text.startswith("W") else "L"
				# # Team points
				elif td_count == 7:
					self.game_stats[game_number]["points"] = int(td.string)
				# # Opponent points
				elif td_count == 8:
					self.game_stats[game_number]["opp_points"] = int(td.string)
				# # Field goals
				elif td_count == 9:
					self.game_stats[game_number]["field_goals"] = int(td.string)
				# # Field goal attempts
				elif td_count == 10:
					self.game_stats[game_number]["field_goal_attempts"] = int(td.string)
				# # Field goal pct
				elif td_count == 11:
					self.game_stats[game_number]["field_goal_pct"] = float(td.string)
				# # 3 pointers
				elif td_count == 12:
					self.game_stats[game_number]["three_point_field_goals"] = int(td.string)
				# # 3 point attempts
				elif td_count == 13:
					self.game_stats[game_number]["three_point_field_goal_attempts"] = int(td.string)
				# # 3 point field goal pct
				elif td_count == 14:
					self.game_stats[game_number]["three_point_field_goal_pct"] = float(td.string)
				# # Free throws
				elif td_count == 15:
					self.game_stats[game_number]["free_throws"] = int(td.string)
				# # Free throws attempted
				elif td_count == 16:
					self.game_stats[game_number]["free_throw_attempts"] = int(td.string)
				# # Free throw pct
				elif td_count == 17:
					self.game_stats[game_number]["free_throw_pct"] = float(td.string)
				# # Offensive rebounds
				elif td_count == 18:
					self.game_stats[game_number]["offensive_rebounds"] = int(td.string)
				# # Total rebounds
				elif td_count == 19:
					self.game_stats[game_number]["total_rebounds"] = int(td.string)
				# # Assists
				elif td_count == 20:
					self.game_stats[game_number]["assists"] = int(td.string)
				# # Steals
				elif td_count == 21:
					self.game_stats[game_number]["steals"] = int(td.string)
				# # Blocks
				elif td_count == 22:
					self.game_stats[game_number]["blocks"] = int(td.string)
				# # Turnovers
				elif td_count == 23:
					self.game_stats[game_number]["turnovers"] = int(td.string)
				# # Personal fouls
				elif td_count == 24:
					self.game_stats[game_number]["personal_fouls"] = int(td.string)
				#
				# ## Skip the spacer TD
				#
				# # Opponent Field goals
				elif td_count == 26:
					self.game_stats[game_number]["opp_field_goals"] = int(td.string)
				# # Opponent Field goal attempts
				elif td_count == 27:
					self.game_stats[game_number]["opp_field_goal_attempts"] = int(td.string)
				# # Opponent field goal pct
				elif td_count == 28:
					self.game_stats[game_number]["opp_field_goal_pct"] = float(td.string)
				# # Opponent 3 pointers
				elif td_count == 29:
					self.game_stats[game_number]["opp_three_point_field_goals"] = int(td.string)
				# # Opponent 3 point attempts
				elif td_count == 30:
					self.game_stats[game_number]["opp_three_point_field_goal_attempts"] = int(td.string)
				# # Opponent 3 point field goal pct
				elif td_count == 31:
					self.game_stats[game_number]["opp_three_point_field_goal_pct"] = float(td.string)
				# # Opponent Free throws
				elif td_count == 32:
					self.game_stats[game_number]["opp_free_throws"] = int(td.string)
				# # Opponent Free throws attempted
				elif td_count == 33:
					self.game_stats[game_number]["opp_free_throw_attempts"] = int(td.string)
				# # Opponent free throw pct
				elif td_count == 34:
					self.game_stats[game_number]["opp_free_throw_pct"] = float(td.string)
				# # Opponent Offensive rebounds
				elif td_count == 35:
					self.game_stats[game_number]["opp_offensive_rebounds"] = int(td.string)
				# # Opponent Total rebounds
				elif td_count == 36:
					self.game_stats[game_number]["opp_total_rebounds"] = int(td.string)
				# # Opponent Assists
				elif td_count == 37:
					self.game_stats[game_number]["opp_assists"] = int(td.string)
				# # Opponent Steals
				elif td_count == 38:
					self.game_stats[game_number]["opp_steals"] = int(td.string)
				# # Opponent Blocks
				elif td_count == 39:
					self.game_stats[game_number]["opp_blocks"] = int(td.string)
				# # Opponent Turnovers
				elif td_count == 40:
					self.game_stats[game_number]["opp_turnovers"] = int(td.string)
				# # Opponent Personal fouls
				elif td_count == 41:
					self.game_stats[game_number]["opp_personal_fouls"] = int(td.string)
