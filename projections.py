import sys
import time
import mysql.connector

from fantasy_point_calculator import FantasyPointCalculator
from dfs_constants import DFSConstants

from datetime import date

class Projections:
	def __init__(self, cnx = None):
		self.league_averages = {}
		self.dvp_cache = {}
		self.pace_cache = {}
		self.player_info_cache = {}
		self.team_cache = {}
		self.baseline_cache = {}
		
		# The calculator of Fantasy Points for each site.
		self.fpc = FantasyPointCalculator()
		
		# Use dependency injection to determine where the database connection comes from.
		if(not cnx):
			self.cnx = mysql.connector.connect(user='fantasy', password='fantasy', host='localhost', database='basketball_reference')
		else:
			self.cnx = cnx

	##########################################################
	# Retrieves the player information in the players table.
	# Returns a dictionary of the values.
	##########################################################
	def get_player_info(self,player_id):
		if player_id in self.player_info_cache:
			return self.player_info_cache[player_id]
	
		cursor = self.cnx.cursor()
		query = """
			select * from players p where id = '%s'
		""" % (player_id)
	
		try:
			cursor.execute(query)
			info = {}
			for result in cursor:
				info["id"] = result[0]
				info["name"] = result[1]
				info["position"] = result[2]
				info["height"] = result[3]
				info["weight"] = result[4]
				info["url"] = result[5]
			
			self.player_info_cache[player_id] = info
		finally:
			cursor.close()
		
		return info
	
	####################################################################
	# Retrieves the position that a player is registered as on a site.
	####################################################################
	def get_position_on_site(self, player_id, site):
		cursor = self.cnx.cursor()
		query = """
			select position from dfs_site_positions where player_id = '%s' and site = '%s'
		""" % (player_id, site)
		
		try:
			cursor.execute(query)
			for result in cursor:
				return result[0]
		finally:
			cursor.close()
		
		return None
	
	####################################################################
	# Retrieves the salary for a player on a particular site and date.
	####################################################################
	def get_salary(self, player_id, site, date=date.today()):
		cursor = self.cnx.cursor()
		query = """
			select salary from salaries where player_id = '%s' and site = '%s' and date = '%s'
		""" % (player_id, site, date)
		
		try:
			cursor.execute(query)
			
			for result in cursor:
				return result[0]
		finally:
			cursor.close()

	####################################################################
	# Determine the team that the player plays for, given the provided
	# season and date.
	####################################################################
	def get_team(self, player_id, season, date=date.today()):
		key = "_".join([player_id, str(season), str(date)])
		if key in self.team_cache:
			return self.team_cache[key]
		
		cursor = self.cnx.cursor()
	
		query = """
			select team from game_totals_basic where player_id = '%s' and season = %d and
				game_number = (select max(game_number) from game_totals_basic 
					where player_id = '%s' and season = %d and date <= '%s')
		""" % (player_id, season, player_id, season, date)
	
		try:
			cursor.execute(query)
			for result in cursor:
				self.team_cache[key] = result[0]
				return result[0]
		finally:
			cursor.close()

	##############################################################################
	# To calculate defensive vs a position we want to get all of the players who
	# played against a team, sum their points, and divide by the number of games
	# the team has played.
	##############################################################################
	def calculate_defense_vs_position(self, metric, position, team, season, date=date.today()):
		key = "_".join([metric, position, team, str(season), str(date)])
		if key in self.dvp_cache:
			return self.dvp_cache[key]
		
		cursor = self.cnx.cursor()
	
		query = ""
		try:
			query = """select sum(b.%s)/(select max(game) from team_game_totals where team = '%s' and season = %d and date <= '%s') 
					from players p inner join game_totals_basic b on p.id = b.player_id 
					where b.season = %d and p.position = '%s' and b.opponent = '%s'
						and date <= '%s'""" % (metric, team, season, date, season, position, team, date)
			cursor.execute(query)
		
			for result in cursor:
				self.dvp_cache[key] = result[0]
				return result[0]
			
		finally:
			cursor.close()

	def calculate_pace(self, team, season):
		key = "_".join([team, str(season)])
		if key in self.pace_cache:
			return self.pace_cache[key]
	
		cursor = self.cnx.cursor()
		query = """
			select minutes_played, 0.5 * ((field_goal_attempts + 0.4 * free_throw_attempts - 1.07 * (offensive_rebounds / (offensive_rebounds + (opp_total_rebounds - opp_offensive_rebounds))) * (field_goal_attempts - field_goals) + turnovers) + (opp_field_goal_attempts + 0.4 * opp_free_throw_attempts - 1.07 * ((opp_offensive_rebounds) / (opp_offensive_rebounds + (total_rebounds - offensive_rebounds))) * (opp_field_goal_attempts - opp_field_goals) + opp_turnovers)) as "pace"
			from team_game_totals t 
			where season = %d and team = '%s'
		""" % (season, team)
	
		total = 0.0
		count = 0
		try:
			cursor.execute(query)
			for result in cursor:
				count = count + 1
				if result[0] == 240:
					total = total + result[1] 
				else:
					total = total + (result[1]/result[0])*240
		
			self.pace_cache[key] = total/count
			return total/count
		finally:
			cursor.close()

	########################################################
	# Calculates the league average for the provided stat.
	########################################################
	def calculate_league_avg(self, stat, position, season, date=date.today()):
		# This calculation is somewhat expensive, so just return
		# the cached value if we've already computed it.
		key = stat + "-" + position
		if key in self.league_averages:
			return self.league_averages[key]
	
		cursor = self.cnx.cursor()
		query = """
			select sum(%s)/(select max(t.game) from team_game_totals t where t.team = b.opponent and season = %d and date <= '%s') as "avg", opponent 
			from game_totals_basic b inner join players p on p.id = b.player_id 
			where season = %d and position = '%s' and date <= '%s'
			group by opponent 
			order by avg desc
		""" % (stat, season, date, season, position, date)
	
		total = 0
		count = 0
		try:
			cursor.execute(query)
			for result in cursor:
				count = count + 1
				total = total + result[0]
		finally:
			cursor.close()
	
		avg = total/count
		self.league_averages[key] = avg
	
		return avg

	def calculate_defense_factor_vs_position(self, position, team, season, league_avg = False):
		cursor = self.cnx.cursor()
		query = ""
		if league_avg:
			query = """
				select sum(b.points)/(select max(game) from team_game_totals where season = %d) 
				from players p inner join game_totals_basic b on p.id = b.player_id 
				where b.season = %d and p.position = '%s' and b.opponent = '%s'
			""" % (team, season, season, position, team)
		else:
			query = """
				select sum(b.points)/(select max(game) from team_game_totals where team = '%s' and season = %d) 
				from players p inner join game_totals_basic b on p.id = b.player_id 
				where b.season = %d and p.position = '%s' and b.opponent = '%s'
			""" % (team, season, season, position, team)
	
	
		factor = -1
		try:
			cursor.execute(query)
			for result in cursor:
				factor = result[0]
		finally:
			cursor.close()
	
		return factor

	###################################################################################
	# Retrieves season averages for a player up to a certain date so we can
	# establish a baseline for the player, prior to adjusting based on matchups, etc.
	###################################################################################
	def get_baseline(self, player_id, season, date=date.today()):
		key = "_".join([player_id, str(season)])
		if key in self.baseline_cache:
			return self.baseline_cache[key]
	
		cursor = self.cnx.cursor()
		query = """
			select avg(points), avg(total_rebounds), avg(assists), avg(steals), avg(blocks), avg(turnovers) from game_totals_basic b where player_id = '%s' and season = %d and date <= '%s'
			""" % (player_id, season, date)
	
		adv_query = """
			select avg(usage_pct), avg(offensive_rating), avg(defensive_rating)
			from game_totals_advanced
			where player_id = '%s' and season = %d and date <= '%s'
		""" % (player_id, season, date)
	
		avg_stat = 0
		avg_usage_pct = 0
		avg_off_rating = 0
		avg_def_rating = 0
	
		try:
			cursor.execute(query)
			for result in cursor:
				avg_points = result[0]
				avg_rebounds = result[1]
				avg_assists = result[2]
				avg_steals = result[3]
				avg_blocks = result[4]
				avg_turnovers = result[5]
		
			cursor.execute(adv_query)
			for result in cursor:
				avg_usage_pct = result[0]
				avg_off_rating = result[1]
				avg_def_rating = result[2]
		finally:
			cursor.close()
	
		baselines = (avg_points, avg_rebounds, avg_assists, avg_steals, avg_blocks, avg_turnovers, avg_usage_pct, avg_off_rating, avg_def_rating)
		self.baseline_cache[key] = baselines
		return baselines
	
	######################################################################################
	# Adjusts the specified stat for each game based on the league average at that point
	# to come up with a real, adjusted value.
	#
	# An example would be if, for the first five games of the season, a player scored
	# 10 points a game.  However, if all of the games were against top-3 defenses, then
	# those 10-point games are more impressive than 10 points vs a bottom-3 defense, 
	# and his scoring average will be adjusted accordingly.
	######################################################################################
	def normalize_player_avg_stat(self, player_id, stat, season, date=date.today()):
		cursor = self.cnx.cursor()
		player_info = self.get_player_info(player_id)
		
		league_avg = 0
		
		query = """
			select avg(b.%s) from players p inner join game_totals_basic b on p.id = b.player_id
			where p.position = '%s' and b.season = %d and b.date <= '%s'
		""" % (stat, player_info["position"], season, date)
		
		try:
			cursor.execute(query)
			
			for result in cursor:
				league_avg = result[0]
			
			# Get all game instances of desired stat for this player.
			query = """
				select %s from game_totals_basic b
				where player_id = '%s' and season = %d and date <= '%s'
			""" % (stat, player_id, season, date)
			
			cursor.execute(query)
			
			adjusted = []
			for result in cursor:
				adjusted.append( (result[0]/league_avg)*result[0] )
			
			return sum(adjusted)/len(adjusted)
		finally:
			cursor.close()
	
	#################################################################################
	# Retrieve the list of games being played for a particular date.  Date defaults
	# to today if none is specified.
	#################################################################################
	def get_game_list(self, d=date.today()):
		games = []
		
		cursor = self.cnx.cursor()
		query = """
			select id, date, season, visitor, home from schedules where date = '%s'
		""" % (d)

		try:
			cursor.execute(query)
			for result in cursor:
				curr = {
					"id": result[0],
					"date": result[1],
					"season": result[2],
					"visitor": result[3],
					"home": result[4]
				}
				
				games.append(curr)
		finally:
			cursor.close()
			
		return games
	
	##################################################################
	# Retrieve a list of players participating in the provided game.
	# The game parameter should take the form of a map containing:
	# - date
	# - home
	# - visitor
	# - season
	##################################################################
	def get_players_in_game(self, game):
		players = []
		cursor = self.cnx.cursor()
		
		query = """
			select player_id, opponent from game_totals_basic 
			where team in ('%s', '%s') and 
				(date = (select max(date) from game_totals_basic where team = '%s') or 
				date = (select max(date) from game_totals_basic where team = '%s'))
			order by date desc
		""" % (game["home"], game["visitor"], game["home"], game["visitor"])
		
		try:
			cursor.execute(query)
			
			for result in cursor:
				players.append({"player_id": result[0], "opponent": result[1]})
		finally:
			cursor.close()
		
		for player in players:
			player["player_info"] = self.get_player_info(player["player_id"])
		
		return players
		
	##############################################################################
	# Makes a projection for a player's stat line based on a variety of factors,
	# starting with their average for the season in each relevant stat.
	##############################################################################
	def calculate_projection(self, player_id, stat, season, opponent, date=date.today()):
		baseline_stat_index = {
			"points": 0,
			"total_rebounds": 1,
			"assists": 2,
			"steals": 3,
			"blocks": 4,
			"turnovers": 5
		}
		
		info = self.get_player_info(player_id)
		team = self.get_team(player_id, season, date)
		baselines = self.get_baseline(player_id,2013, date)
		
		avg_stat = baselines[baseline_stat_index[stat]]		
		adjusted_stat = avg_stat
	
		#######################################
		# Take pace of the game into account.
		#######################################
		team_pace = self.calculate_pace(team, season)
		opp_pace = self.calculate_pace(opponent, season)
		avg_pace = (team_pace + opp_pace)/2
		pace_factor = avg_pace/team_pace
	
		adjusted_stat = float(avg_stat) * float(pace_factor)
	
		######################################################################
		# Effectiveness of opponent defense, compared to the league average
		# for this player's position.
		######################################################################
		league_avg = self.calculate_league_avg(stat, info["position"], season)
		
		def_factor = self.calculate_defense_vs_position(stat, info["position"], opponent, season, date)

		adjusted_stat = adjusted_stat * float(def_factor/league_avg)
	
		return adjusted_stat

	###################################################################################
	# Calculates the percentage of games that a player reaches the floor, consistent, 
	# and ceiling thresholds for fantasy points.
	#
	# Floor 		- 20 fantasy points
	# Consistency 	- 21-40 fantasy points
	# Ceiling 		- 41+ fantasy points
	# Super Ceiling - 50+ fantasy points
	###################################################################################
	def calculate_floor_consistency_ceiling_pct(self, player_id, season, site):
		cursor = self.cnx.cursor()
		stat_list = []
		try:
			query = ("Select * from game_totals_basic t where player_id = '%s' and season = %d") % (player_id, season)
			cursor.execute(query)

			# Collect list of stat lines that don't have fantasy points computed.
			games = 0
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
				games = games + 1
		finally:
			cursor.close()
		
		self.fpc.site = site
		
		floor = 0.0
		consistency = 0.0
		ceiling = 0.0
		s_ceiling = 0.0
		for s in stat_list:
			fantasy_points = self.fpc.calculate(s)
						
			if fantasy_points <= 20:
				floor = floor + 1
			if fantasy_points > 20:
				consistency = consistency + 1
			if fantasy_points > 40:
				ceiling = ceiling + 1
			if fantasy_points > 50:
				s_ceiling = s_ceiling + 1
		
		return (floor/games, consistency/games, ceiling/games, s_ceiling/games)
	
	def get_avg_minutes_past_n_games(self, player_id, season, n):
		cursor = self.cnx.cursor()
		
		query = """
			select avg(minutes_played) from game_totals_basic where player_id = '%s' and season = %d order by date desc limit %d
		""" % (player_id, season, n)
		
		try:
			cursor.execute(query)
			
			for result in cursor:
				return result[0]
		finally:
			cursor.close()

	def regression(self):
		games = []
		cursor = self.cnx.cursor()
		
		print "Grabbing all game logs"
		try:
			# Grab all game logs
			cursor.execute("""
				select player_id, season, game_number, date, team, home, opponent, minutes_played, 
					points, assists, total_rebounds, steals, blocks, turnovers 
				from game_totals_basic 
				where season = 2013 
				order by player_id, date desc""")
			
			for game in cursor:
				games.append(game)	
		finally:
			cursor.close()
		
		print "Writing projections and actuals out to regression.csv"
		f = open("regression.csv", "w")
		f.write("""player_id,game number,date,team,opponent,projected FPs,actual FPs,RMSE,projected points,actual points,RMSE,projected assists,actual assists,RMSE,projected rebounds,actual rebounds,RMSE,projected steals,actual steals,RMSE,projected blocks,actual blocks,RMSE,projected turnovers,actual turnovers,RMSE\n""")
		
		self.fpc.site = DFSConstants.STAR_STREET
		
		count = 0
		for game in games:
			count = count + 1
		
			player_id = game[0]
			season = game[1]
			game_number = game[2]
			date = game[3]
			team = game[4]
			opponent = game[6]
			minutes_played = game[7]
			actual_points = game[8]
			actual_assists = game[9]
			actual_rebounds = game[10]
			actual_steals = game[11]
			actual_blocks = game[12]
			actual_turnovers = game[13]
			
			print "Processing %s/%d/%d/%s/%s/%s (%d/%d)" % (player_id, season, game_number, date, team, opponent, count, len(games))
			
			actual_fps = self.fpc.calculate({
				"points": actual_points,
				"total_rebounds": actual_rebounds,
				"assists": actual_assists,
				"steals": actual_steals,
				"blocks": actual_blocks,
				"turnovers": actual_turnovers
			})
		
			proj_points = 0
			proj_assists = 0
			
			if minutes_played > 0:
				start = time.time()
				proj_points = self.calculate_projection(player_id, "points", season, opponent, date)
				proj_assists = self.calculate_projection(player_id, "assists", season, opponent, date)
				proj_rebounds = self.calculate_projection(player_id, "total_rebounds", season, opponent, date)
				proj_steals = self.calculate_projection(player_id, "steals", season, opponent, date)
				proj_blocks = self.calculate_projection(player_id, "blocks", season, opponent, date)
				proj_turnovers = self.calculate_projection(player_id, "turnovers", season, opponent, date)
				end = time.time()
				#print "calculate_projections - %f" % ((end-start)/1000.0)
				
				proj_fps = self.fpc.calculate({
					"points": proj_points,
					"total_rebounds": proj_rebounds,
					"assists": proj_assists,
					"steals": proj_steals,
					"blocks": proj_blocks,
					"turnovers": proj_turnovers
				})
			
			line = "%s,%d,%s,%s,%s,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f" % (
				player_id,
				game_number,
				date,
				team,
				opponent,
				proj_fps,
				actual_fps,
				(proj_fps - actual_fps)**2,
				proj_points,
				actual_points,
				(proj_points - actual_points)**2,
				proj_assists,
				actual_assists,
				(proj_assists - actual_assists)**2,
				proj_rebounds,
				actual_rebounds,
				(proj_rebounds - actual_rebounds)**2,
				proj_steals,
				actual_steals,
				(proj_steals - actual_steals)**2,
				proj_blocks,
				actual_blocks,
				(proj_blocks - actual_blocks)**2,
				proj_turnovers,
				actual_turnovers,
				(proj_turnovers - actual_turnovers)**2
			)
			f.write(line + "\n")
		
		f.close()
	
	def run(self):
		# Find all games being played today
		games = self.get_game_list()
		
		# List of stats to project for each player.
		stats = ["points", "field_goals", "field_goal_attempts", "three_point_field_goals", "three_point_field_goal_attempts",
							"free_throws", "free_throw_attempts", "total_rebounds", "assists", "steals", "blocks", "turnovers"]
		
		# List of sites to make projections for
		sites = [ self.fpc.DRAFT_DAY, self.fpc.DRAFT_KINGS, DFSConstants.FAN_DUEL, self.fpc.STAR_STREET ]
		
		# CSV files to write to
		files = {}
		for s in sites:
			files[s] = open("projections/%s_%s.csv" % (s, date.today()), "w")
			files[s].write("name,position,projection,salary,floor,consistency,ceiling,avg minutes\n")
		
		print "%d games tonight..." % len(games)
		for game in games:
			print "Evaluating players in %s vs %s" % (game["home"], game["visitor"])
		
			players = self.get_players_in_game(game)
			
			for player in players:
				print "\tEvaluating %s" % player["player_info"]["name"]
			
				projections = {}
					
				for s in stats:
					projections[s] = self.calculate_projection(player["player_id"], s, game["season"], player["opponent"])
				
				for s in sites:
					self.fpc.site = s
					fps = self.fpc.calculate(projections)
					consistency = self.calculate_floor_consistency_ceiling_pct(player["player_id"], game["season"], s)
					salary = self.get_salary(player["player_id"], s)
					salary = -1 if salary == None else salary
					
					avg_minutes = self.get_avg_minutes_past_n_games(player["player_id"], game["season"], 5)
					
					site_position = self.get_position_on_site(player["player_id"], s)
					
					print "\t\t%s (%s) is projected for %f points on %s" % (player["player_info"]["name"], site_position, fps, s)
					files[s].write("%s,%s,%f,%d,%f,%f,%f,%f\n" % (player["player_info"]["name"], site_position, fps, salary, consistency[0], consistency[1], consistency[2], avg_minutes) )
					
		
		# We're done!  Close up the files
		for f in files:
			files[f].close()

if __name__ == '__main__':
	regression = False
	for arg in sys.argv:
		if arg == "projections.py":
			pass
		else:
			pieces = arg.split("=")
			if pieces[0] == "regression":
				regression = pieces[1] == "true"

	projections = Projections()
	
	# Run regression if the flag is set to true.  Otherwise, just generate projections.
	if regression:
		projections.regression()
	else:
		projections.run()