import sys
import mysql.connector

class FantasyPointCalculator():
	DRAFT_DAY = "DRAFT_DAY"
	DRAFT_KINGS = "DRAFT_KINGS"
	STAR_STREET = "STAR_STREET"

	def __init__(self, cnx = None, site=None):
		self.site = site
		
		# Use dependency injection to determine where the database connection comes from.
		if(not cnx):
			self.cnx = mysql.connector.connect(user='fantasy', password='fantasy', host='localhost', database='basketball_reference')
		else:
			self.cnx = cnx

	def calculate(self, stats):
		fantasy_points = 0
	
		if self.site == self.DRAFT_DAY:
			missed_shots = (stats["field_goal_attempts"] - stats["field_goals"]) + (stats["three_point_field_goal_attempts"] - stats["three_point_field_goals"]) + (stats["free_throw_attempts"] - stats["free_throws"])
			
			fantasy_points = stats["points"] + (stats["total_rebounds"] * 1.25) + (stats["assists"] * 1.5) + (stats["steals"] * 2) + (stats["blocks"] * 2) - (stats["turnovers"] * 1) - (missed_shots * 0.25)
			
			# 1 point bonus for 3 pointer made
			fantasy_points = fantasy_points + stats["three_point_field_goals"]

			triple_or_double_double = 0
			criteria = [stats["points"], stats["total_rebounds"], stats["assists"], stats["steals"], stats["blocks"]]
			for c in criteria:
				if c >= 10:
					triple_or_double_double = triple_or_double_double + 1

			if triple_or_double_double == 2:
				fantasy_points = fantasy_points + 2
			elif triple_or_double_double == 3:
				fantasy_points = fantasy_points + 2
		
		elif self.site == self.DRAFT_KINGS:
			fantasy_points = stats["points"] + (stats["total_rebounds"] * 1.25) + (stats["assists"] * 1.5) + (stats["steals"] * 2) + (stats["blocks"] * 2) - (stats["turnovers"] * 0.5)
			
			# 1 point bonus for 3 pointer made
			fantasy_points = fantasy_points + (stats["three_point_field_goals"] * 0.5)

			triple_or_double_double = 0
			criteria = [stats["points"], stats["total_rebounds"], stats["assists"], stats["steals"], stats["blocks"]]
			for c in criteria:
				if c >= 10:
					triple_or_double_double = triple_or_double_double + 1

			if triple_or_double_double == 2:
				fantasy_points = fantasy_points + 1.5
			elif triple_or_double_double == 3:
				fantasy_points = fantasy_points + 3
		
		elif self.site == self.STAR_STREET:
			fantasy_points = stats["points"] + (stats["total_rebounds"] * 1.25) + (stats["assists"] * 1.5) + (stats["steals"] * 2) + (stats["blocks"] * 2) - (stats["turnovers"] * 1)
			
		return fantasy_points
	
	#################################################################################################
	# This function gets executed as a stand-alone script.
	#
	# It will query all entries in game_totals_basic that don't have a corresponding fantasy_points
	# row, compute the fantasy points for each, and insert a row into the fantasy_points table.
	#################################################################################################
	def run(self):
		cursor = self.cnx.cursor()
		stat_list = []
		try:
			query = ("Select * from game_totals_basic t left join fantasy_points p on t.id = p.id where p.id is NULL;")
			cursor.execute(query)

			# Collect list of stat lines that don't have fantasy points computed.
			for (result) in cursor:
				stats = {}
			
				stats["player_id"] = result[1]
				stats["season"] = result[2]
				stats["game_number"] = result[3]
				stats["field_goals"] = result[12]
				stats["field_goal_attempts"] = result[13]
				stats["three_point_field_goals"] = result[15]
				stats["three_point_field_goal_attempts"] = result[16]
				stats["free_throws"] = result[18]
				stats["free_throw_attempts"] = result[19]
				stats["total_rebounds"] = result[23]
				stats["assists"] = result[24]
				stats["steals"] = result[25]
				stats["blocks"] = result[26]
				stats["turnovers"] = result[27]
				stats["points"] = result[29]
			
				stat_list.append(stats)
		finally:
			cursor.close()
		
		# Calculate fantasy points and insert into the database.
		cursor = self.cnx.cursor()
		try:
			for s in stat_list:
				fantasy_points = self.calculate(s)
	
				insert_query = ("insert into fantasy_points (player_id, site, season, game_number, points) values ('%s','%s',%d,%d,%f)") % (s["player_id"], self.site, s["season"], s["game_number"], fantasy_points)
				cursor.execute(insert_query)
		finally:
			cursor.close()

if __name__ == '__main__':
	fpc = FantasyPointCalculator()
	fpc.run()