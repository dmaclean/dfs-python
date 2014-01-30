from datetime import date

import logging
import sys
import mysql.connector

class FantasyPointCalculator():
	DRAFT_DAY = "DRAFT_DAY"
	DRAFT_KINGS = "DRAFT_KINGS"
	FAN_DUEL = "FAN_DUEL"
	STAR_STREET = "STAR_STREET"
	
	ALL_SITES = [DRAFT_DAY, DRAFT_KINGS, STAR_STREET]

	def __init__(self, cnx = None, site=None, season=None):
		self.site = site
		self.season = season
		
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
		
		elif self.site == self.FAN_DUEL:
			fantasy_points = stats["points"] + (stats["total_rebounds"] * 1.2) + (stats["assists"] * 1.5) + (stats["steals"] * 2) + (stats["blocks"] * 2) - (stats["turnovers"] * 1)
		
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
		all_ids = {}
		from_fantasy_points = {}

		if self.season:
			query = "select id from game_totals_basic where season = {}".format(self.season)
		else:
			query = "select id from game_totals_basic"

		try:
			logging.info("Querying for all ids in game_totals_basic")
			cursor.execute(query)
			for result in cursor:
				all_ids[result[0]] = 1
			
			logging.info("Querying for game_totals_basic_ids in fantasy_points for {}".format(self.site))
			if self.season:
				query = "select game_totals_basic_id from fantasy_points where site = '{}' and season = {}".format(
					self.site, self.season)
			else:
				query = "select game_totals_basic_id from fantasy_points where site = '{}'".format(self.site)

			cursor.execute(query)
			for result in cursor:
				from_fantasy_points[result[0]] = 1
			
			logging.info("Filtering out existing ids")
			valid_ids = []
			for k in from_fantasy_points:
				del all_ids[k]
			
			for k in all_ids:
				valid_ids.append(k)
			
			logging.info("Retrieving game_totals_basic rows that have not yet been computed for fantasy points.")
			
			count = 1
			total = len(valid_ids)
			for id in valid_ids:
				if count % 10 == 0:
					logging.info("Retrieved %d of %d" % (count, total))
				cursor.execute("select * from game_totals_basic where id = {}".format(id))

				# Collect list of stat lines that don't have fantasy points computed.
				for (result) in cursor:
					stats = {}
				
					stats["id"] = result[0]
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
				
				count += 1
		finally:
			cursor.close()
		
		# Calculate fantasy points and insert into the database.
		count = 0
		cursor = self.cnx.cursor()
		try:
			for s in stat_list:
				fantasy_points = self.calculate(s)
	
				insert_query = ("""insert into fantasy_points (game_totals_basic_id, player_id, site, season, game_number, points) 
				values ({},'{}','{}',{},{},{})""").format(s["id"], s["player_id"], self.site, s["season"], s["game_number"], fantasy_points)
				cursor.execute(insert_query)
				
				count += 1
				
				if count % 10 == 0:
					logging.info("Processed {} games".format(count))
		finally:
			cursor.close()

if __name__ == '__main__':
	curr_site = ""
	season = date.today().year

	for arg in sys.argv:
		if arg == "fantasy_point_calculator.py":
			pass
		else:
			pieces = arg.split("=")
			if pieces[0] == "site":
				curr_site = pieces[1]
			elif pieces[0] == "season":
				season = int(pieces[1])
	fpc = FantasyPointCalculator(site=curr_site, season=season)
	fpc.run()
	