import logging
import sys
import time
import mysql.connector

from fantasy_point_calculator import FantasyPointCalculator
from dfs_constants import DFSConstants
from models.defense_vs_position_manager import DefenseVsPositionManager
from models.defense_vs_position import DefenseVsPosition
from models.injury_manager import InjuryManager,Injury

from datetime import date, timedelta


class Projections:
	def __init__(self, cnx = None):
		self.league_averages = {}
		self.dvp_cache = {}
		self.dvp_ranking_cache = {}
		self.pace_cache = {}
		self.player_info_cache = {}
		self.team_cache = {}
		self.baseline_cache = {}
		self.scoring_stddev_cache = {}
		self.expected_points_cache = {}
		self.depth_chart_cache = {}

		# The current DFS site we're projecting for.
		self.site = ""

		self.stats = ["points", "field_goals", "field_goal_attempts", "three_point_field_goals", "three_point_field_goal_attempts",
							"free_throws", "free_throw_attempts", "total_rebounds", "assists", "steals", "blocks", "turnovers",
							"minutes_played"]

		# In regression mode?
		self.regression_mode = False

		# The calculator of Fantasy Points for each site.
		self.fpc = FantasyPointCalculator()

		# Use dependency injection to determine where the database connection comes from.
		if(not cnx):
			self.cnx = mysql.connector.connect(user='fantasy', password='fantasy', host='localhost', database='basketball_reference')
		else:
			self.cnx = cnx

		self.dvpManager = DefenseVsPositionManager(cnx=self.cnx)
		self.injury_manager = InjuryManager(cnx=self.cnx)

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
				info["rg_position"] = result[3]
				info["height"] = result[4]
				info["weight"] = result[5]
				info["url"] = result[6]

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
	def calculate_defense_vs_position(self, metric, position, team, season, date=date.today(), n=None):
		# Initialize the cache, if necessary
		if len(self.dvp_cache) == 0:
			logging.info("Populating the DvP cache...")
			dvps = self.dvpManager.get(DefenseVsPosition(season=season))
			for dvp in dvps:
				key = "_".join([dvp.stat, dvp.position, dvp.team, str(dvp.season), str(dvp.date)])
				self.dvp_cache[key] = dvp.value

		key = "_".join([metric, position, team, str(season), str(date).replace(" 00:00:00","")])
		if key in self.dvp_cache:
			return self.dvp_cache[key]

		self.dvp_cache[key] = self.dvpManager.calculate_defense_vs_position(metric, position, team, season, self.site, date)

		return self.dvp_cache[key]

	def calculate_defense_vs_position_ranking(self, metric, position, team, season, site, d=date.today()):
		"""
		To calculate defensive vs a position we want to get all of the players who
		played against a team, sum their fantasy points, and divide by the number of games
		the team has played.
		"""
		key = "_".join([metric, position, team, str(season), str(d)])
		if key in self.dvp_ranking_cache:
			return self.dvp_ranking_cache[key]

		cursor = self.cnx.cursor()

		try:
			# Get all teams for season
			teams = []
			query = "select distinct team from team_game_totals where season = %d" % season

			cursor.execute(query)
			for result in cursor:
				teams.append(result[0])

			ranks = []
			for t in teams:
				dvp = self.dvpManager.calculate_defense_vs_position(metric, position, t, season, site, d)
				ranks.append((dvp, t))

			# Sort the results in ascending order (lowest value at element 0).
			ranks.sort()

			# Put the results in the cache.  We only want the ranking, so we're going to 
			# put the index i in the cache instead of the actual value.
			i = 1
			for r in ranks:
				temp_key = "_".join([metric, position, r[1], str(season), str(d)])
				self.dvp_ranking_cache[temp_key] = i
				i += 1

		finally:
			cursor.close()

		return self.dvp_ranking_cache[key]

	def calculate_pace(self, team, season, d=date.today(), n=None):
		key = "_".join([team, str(season)])
		if key in self.pace_cache:
			return self.pace_cache[key]

		cursor = self.cnx.cursor()
		query = """
			select minutes_played, 0.5 * ((field_goal_attempts + 0.4 * free_throw_attempts - 1.07 * (offensive_rebounds / (offensive_rebounds + (opp_total_rebounds - opp_offensive_rebounds))) * (field_goal_attempts - field_goals) + turnovers) + (opp_field_goal_attempts + 0.4 * opp_free_throw_attempts - 1.07 * ((opp_offensive_rebounds) / (opp_offensive_rebounds + (total_rebounds - offensive_rebounds))) * (opp_field_goal_attempts - opp_field_goals) + opp_turnovers)) as "pace"
			from team_game_totals t 
			where season = %d and team = '%s' and date <= '%s'
		""" % (season, team, d)

		if n:
			query += " order by date desc limit %d" % n

		total = 0.0
		count = 0
		try:
			cursor.execute(query)
			for result in cursor:
				count += 1
				if result[0] == 240:
					total += result[1]
				else:
					total += (result[1]/result[0])*240

			self.pace_cache[key] = total/count
			return total/count
		finally:
			cursor.close()

	def calculate_expected_team_points(self, team, opponent, season, d=date.today()):
		"""
		Calculate the number of points we expect a team to score based on the opponent they are playing.

		expected = ((team_off_efficiency + opp_def_efficiency)/2 * (team_pace + opp_pace)/2) * 100
		"""

		# Check the cache first
		if team in self.expected_points_cache:
			return self.expected_points_cache[team]

		team_pace = self.calculate_pace(team, season, d)
		opp_pace = self.calculate_pace(opponent, season, d)

		# Get the average points per game
		cursor = self.cnx.cursor()

		query = """
			select avg(points), avg(opp_points), team from team_game_totals
			where season = %d and date <= '%s' and team in ('%s','%s') group by team
		""" % (season, d, team, opponent)

		try:
			cursor.execute(query)
			for result in cursor:
				if result[2] == team:
					team_avg_points = result[0]
					team_avg_opp_points = result[1]
				else:
					opp_avg_points = result[0]
					opp_avg_opp_points = result[1]
		finally:
			cursor.close()

		# Calculate the offensive and defensive efficiency for our team and their opponent.
		team_off_efficiency = (team_avg_points/team_pace) * 100
		team_def_efficiency = (team_avg_opp_points/team_pace) * 100
		opp_off_efficiency = (opp_avg_points/opp_pace) * 100
		opp_def_efficiency = (opp_avg_opp_points/opp_pace) * 100

		# Calculate expected points for this game.
		team_expected_points = ((team_off_efficiency + opp_def_efficiency)/2 * (team_pace + opp_pace)/2) / 100
		opp_expected_points = ((opp_off_efficiency + team_def_efficiency)/2 * (team_pace + opp_pace)/2) / 100

		# Store our results in the cache before returning.
		self.expected_points_cache[team] = team_expected_points
		self.expected_points_cache[opponent] = opp_expected_points

		return team_expected_points

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
			select sum(%s)/(select max(t.game) from team_game_totals t 
			where t.team = b.opponent and season = %d and date <= '%s') as "avg", opponent 
			from game_totals_basic b inner join players p on p.id = b.player_id 
			where season = %d and rg_position = '%s' and date <= '%s'
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

		# Construct game_totals_basic query
		query = "select "
		count = 1
		for s in self.stats:
			query = query + "avg(%s)" % (s)
			if count < len(self.stats):
				query = query + ","
			count = count + 1

		query = query + """
			from game_totals_basic b where player_id = '%s' and season = %d and date <= '%s'
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
			baselines = []

			for result in cursor:
				for r in result:
					baselines.append(r)
				#avg_points = result[0]
				#avg_rebounds = result[1]
				#avg_assists = result[2]
				#avg_steals = result[3]
				#avg_blocks = result[4]
				#avg_turnovers = result[5]

			cursor.execute(adv_query)
			for result in cursor:
				for r in result:
					baselines.append(r)
				#avg_usage_pct = result[0]
				#avg_off_rating = result[1]
				#avg_def_rating = result[2]
		finally:
			cursor.close()

		#baselines = (avg_points, avg_rebounds, avg_assists, avg_steals, avg_blocks, avg_turnovers, avg_usage_pct, avg_off_rating, avg_def_rating)
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
			select player_id, team, date
			from game_totals_basic b
			where season = %d
			order by player_id, date desc
		""" % (game["season"])

		try:
			cursor.execute(query)

			ids = {}
			for result in cursor:
				if result[0] not in ids:
					if result[1] == game["home"] or result[1] == game["visitor"]:
						ids[result[0]] = True
					else:
						ids[result[0]] = False

			for id in ids:
				if ids[id]:
					players.append({"player_id": id})
		finally:
			cursor.close()

		delete_list = []
		for player in players:
			player["player_info"] = self.get_player_info(player["player_id"])

			# Players with no rg_position will cause errors.  Usually they're so obscure
			# that we won't miss them, so get rid of them.
			if not player["player_info"]["rg_position"]:
				delete_list.append(player)

		for player in delete_list:
			players.remove(player)

		return players

	##############################################################################
	# Makes a projection for a player's stat line based on a variety of factors,
	# starting with their average for the season in each relevant stat.
	##############################################################################
	def calculate_projection(self, player_id, stat, season, opponent, d=date.today()):
		baseline_stat_index = {
			"points": 0,
			"field_goals": 1,
			"field_goal_attempts": 2,
			"three_point_field_goals": 3,
			"three_point_field_goal_attempts": 4,
			"free_throws": 5,
			"free_throw_attempts": 6,
			"total_rebounds": 7,
			"assists": 8,
			"steals": 9,
			"blocks": 10,
			"turnovers": 11,
			"minutes_played": 12
		}

		info = self.get_player_info(player_id)
		team = self.get_team(player_id, season, d)
		baselines = self.get_baseline(player_id,season, d)

		avg_stat = baselines[baseline_stat_index[stat]]

		adjusted_stat = avg_stat
	
		#######################################
		# Take pace of the game into account.
		#######################################
		team_pace = self.calculate_pace(team, season)
		opp_pace = self.calculate_pace(opponent, season)
		avg_pace = (team_pace + opp_pace)/2
		pace_factor = avg_pace/team_pace
	
		adjusted_stat = float(adjusted_stat) * float(pace_factor)
	
		######################################################################
		# Effectiveness of opponent defense, compared to the league average
		# for this player's position.
		######################################################################
		league_avg = self.calculate_league_avg(stat, info["rg_position"], season)

		def_factor = self.calculate_defense_vs_position(stat, info["rg_position"], opponent, season, d)

		adjusted_stat = float(adjusted_stat) * (float(def_factor)/float(league_avg))
	
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
	
	############################################################
	# Gets the standard deviation of a player's fantasy points
	############################################################
	def calculate_scoring_stddev(self, player_id, season, site, d=date.today()):
		key = "_".join([player_id, site])
		
		# Lazy initialization.  Populate the cache on the first request for it.
		if len(self.scoring_stddev_cache) == 0:	
			logging.info("Populating stddev cache...")
			cursor = self.cnx.cursor()

			query = """
				select f.player_id, f.site, avg(f.points), stddev(f.points)
				from fantasy_points f inner join game_totals_basic b on f.game_totals_basic_id = b.id
				where f.season = %d and b.date <= '%s' group by f.player_id, f.site
			""" % (season, d)
				
			try:
				cursor.execute(query)
			
				for result in cursor:
					curr_key = "_".join([result[0], result[1]])
					self.scoring_stddev_cache[curr_key] = (result[2], result[3])
			finally:
				cursor.close()
		
		return self.scoring_stddev_cache[key]
	
	###########################################################################################
	# Retrieves the average minutes that a player has been on the floor for the past n games.
	###########################################################################################
	def get_avg_stat_past_n_games(self, player_id, stat, season, n, d=date.today()):
		cursor = self.cnx.cursor()
		
		query = """
			select %s from game_totals_basic where player_id = '%s' and season = %d and date <= '%s' order by date desc limit %d
		""" % (stat, player_id, season, d, n)
		
		try:
			cursor.execute(query)

			total = 0
			for result in cursor:
				total = total + result[0]

			return total/n
		finally:
			cursor.close()
	
	###############################################################################
	# Retrieves the odds calculated by Vegas for this player's game.  The
	# data includes the spread (relative to his team), over/under, and projection
	# (again, for his team).
	###############################################################################		
	def get_vegas_odds(self, team, date=date.today()):
		cursor = self.cnx.cursor()
		
		query = """
			select date, road_team, home_team, spread_road, spread_home, over_under, projection_road, projection_home
			from vegas where (road_team = '%s' or home_team = '%s') and date = '%s'
		""" % (team, team, date)
		
		try:
			cursor.execute(query)

			data = {}			
			for result in cursor:
				# road team
				if team == result[1]:
					data["spread"] = result[3]
					data["over_under"] = result[5]
					data["projection"] = result[6]
				else:
					data["spread"] = result[4]
					data["over_under"] = result[5]
					data["projection"] = result[7]
			return data
				
		finally:
			cursor.close()

	def determine_depth_chart(self, season, d=date.today()):
		"""
		Creates two depth charts for teams.

		One is from the perspective of a team/position breakdown.  It gives a global perspective of all players.
		Team
		--> Position
		------> Player1 = (<avg minutes>, <player_id>, <player name>)
		------> Player2 = (<avg minutes>, <player_id>, <player name>)
		------> PlayerN = (<avg minutes>, <player_id>, <player name>)


		Another is a quick lookup of the player
		Player_id = (<player name>, <avg_minutes>, <rank>, <pct of minutes for position>)
		"""

		# Return an existing one if we've already created this.
		key = "_".join([str(season), str(d)])
		if key in self.depth_chart_cache:
			return self.depth_chart_cache[key]

		cursor = self.cnx.cursor()

		injury_manager = InjuryManager(self.cnx)
		injuries = injury_manager.get_currently_injured_players(d)

		two_weeks = timedelta(days=14)

		query = """
				select name, p.id, team, rg_position, avg(minutes_played) as "avg mp"
				from players p inner join game_totals_basic b on p.id = b.player_id
				where b.season = %d and b.date between '%s' and '%s'
				group by player_id
				order by team, rg_position, avg(minutes_played) desc
			""" % (season, d-two_weeks, d)

		depth_chart = {}
		depth_chart_by_player_id = {}

		try:
			cursor.execute(query)
			for result in cursor:
				name = result[0]
				player_id = result[1]
				team = result[2]
				position = result[3]
				minutes = result[4]

				# Create the map for a team if it doesn't exist yet.
				if team not in depth_chart:
					depth_chart[team] = {}

				# Create the map for a position if it doesn't exist yet.
				if position not in depth_chart[team]:
					depth_chart[team][position] = []

				depth_chart[team][position].append((minutes, player_id, name))
				depth_chart[team][position].sort(reverse=True)

			for t in depth_chart:
				for p in depth_chart[t]:

					# Determine the total avg minutes at the position
					total = 0
					for player in depth_chart[t][p]:
						total = total + player[0]

					# Generate the entry for each player, now that we know the total avg minutes at the position.
					i = 1
					for player in depth_chart[t][p]:
						depth_chart_by_player_id[player[1]] = [player[2], player[0], i, player[0]/total]
						i += 1

					# Now we need to factor in injuries.  In this loop, go through all the players
					# for this team at this position and if they're injured, add their expected minutes
					# to a pool of available minutes.  In a subsequent loop we'll redistribute them to
					# players that will be playing.
					avail_minutes = 0
					percentage_injured = 0
					for player in depth_chart[t][p]:
						pid = player[1]

						# is player injured (and have we yet to factor it in [0 minutes])?
						if pid in injuries:
							# Player is injured.  Add their expected minutes to avail_minutes and
							# set avg minutes and pct of total to 0.
							avail_minutes += depth_chart_by_player_id[pid][1]
							percentage_injured += depth_chart_by_player_id[pid][3]
							depth_chart_by_player_id[pid][1] = 0
							depth_chart_by_player_id[pid][2] = -1
							depth_chart_by_player_id[pid][3] = 0

					# In this loop we're going to redistribute the available minutes.  This will be done
					# proportionally, so assume the following scenario:
					# P1 = 50% of minutes (20 minutes)
					# P2 = 25% of minutes (10 minutes)
					# P3 = 25% of minutes (10 minutes)
					# P1 gets injured, so 50% of total minutes are up for grabs (percentage_injured = 0.5).
					# P2 and P3 each get a new_pct_of_total = .25/(1-0.5) = 0.5
					# So, their new expected minutes each become 10 + (20 * 0.5) = 20 minutes.
					rank = 1
					for player in depth_chart[t][p]:
						pid = player[1]

						if pid not in injuries:
							new_pct_of_total = depth_chart_by_player_id[pid][3]/(1-percentage_injured)
							depth_chart_by_player_id[pid][2] = rank
							depth_chart_by_player_id[pid][3] = new_pct_of_total
							depth_chart_by_player_id[pid][1] += avail_minutes * new_pct_of_total

							if depth_chart_by_player_id[pid][1] > 35:
								depth_chart_by_player_id[pid][1] = 35

							rank += 1

		finally:
			cursor.close()

		self.depth_chart_cache[key] = (depth_chart, depth_chart_by_player_id)
		return self.depth_chart_cache[key]

	def print_depth_chart(self, season, site, d=date.today()):
		"""
		Prints out the depth chart to file (depth_chart_<timestamp>.txt).  This is meant to
		help with finding good value plays each day.  We'll be able to quickly see each player
		based on their average minutes and their expected minutes (0 if they are injured).
		There is also additional data to help decide if a player is worth taking, like average
		FPs, standard deviation, DvP, etc.
		"""

		f = open("projections/depth_chart_%s_%s.txt" % (site, str(d)), "w")

		try:
			depth_chart, depth_chart_by_player_id = self.determine_depth_chart(season, d)
			games = self.get_game_list(d)

			for game in games:
				dcs = {game["home"]: depth_chart[game["home"]], game["visitor"]: depth_chart[game["visitor"]]}

				for team in dcs:
					f.write("%s\n" % team)

					opponent = game["home"] if team != game["home"] else game["visitor"]

					dc = dcs[team]
					for position in dc:
						#f.write("\t%s\n" % position)
						f.write("{:>10}\n".format(position))

						f.write("{:>40}{:>20}{:>20}{:>20}{:>20}{:>20}{:>20}\n".format('Name', 'Average minutes', 'Expected minutes', 'Average FPs',
																		'FP stddev', 'Opponent DvP', 'Salary'))
						for player in dc[position]:
							if not position:
								print player
							player_id = player[1]
							name = player[2]
							avg_minutes = player[0]
							expected_minutes = depth_chart_by_player_id[player_id][1]
							fp_data = self.calculate_scoring_stddev(player_id, season, site, d)
							salary = self.get_salary(player_id, site, d)
							fp_rank = self.calculate_defense_vs_position_ranking(DFSConstants.FANTASY_POINTS, position, opponent, game["season"], site)

							f.write("{:>40}{:>20}{:>20}{:>20}{:>20}{:>20}{:>20}\n".format(name,
							                                      avg_minutes,
							                                      expected_minutes,
							                                      fp_data[0],
							                                      float(fp_data[1]),
							                                      fp_rank,
							                                      salary))
						f.write("\n")
					f.write("\n\n")
		finally:
			f.close()


	def regression(self):
		games = []
		cursor = self.cnx.cursor()

		season = 2013

		print "Grabbing all game logs"
		try:
			# Grab all game logs
			cursor.execute("""
				select player_id, season, game_number, date, team, home, opponent, minutes_played, 
					points, assists, total_rebounds, steals, blocks, turnovers 
				from game_totals_basic b inner join players p on p.id = b.player_id
				where b.season = %d and p.rg_position is not null
				order by player_id, date desc""" % season)
			
			for game in cursor:
				games.append(game)	
		finally:
			cursor.close()
		
		print "Writing projections and actuals out to regression.csv"
		f = open("regression.csv", "w")
		f.write("player_id,\
					game number,\
					date,team,\
					opponent,\
					floor FPs,ceiling FPs,projected FPs,actual FPs,MSE,\
					projected points,actual points,MSE,\
					projected assists,actual assists,MSE,\
					projected rebounds,actual rebounds,MSE,\
					projected steals,actual steals,MSE,\
					projected blocks,actual blocks,MSE,\
					projected turnovers,actual turnovers,MSE,\
					projected minutes,actual minutes,MSE\n")
		
		self.fpc.site = DFSConstants.STAR_STREET
		
		# Squared errors
		ssq_fps = 0
		ssq_points = 0
		ssq_rebounds = 0
		ssq_assists = 0
		ssq_steals = 0
		ssq_blocks = 0
		ssq_turnovers = 0
		ssq_minutes = 0
		
		count = 0
		processed = 0
		for game in games:
			count += 1
		
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

			depth_chart, depth_chart_by_player_id = self.determine_depth_chart(season, date)
			
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
				processed = processed + 1

				start = time.time()
				proj_points = self.calculate_projection(player_id, "points", season, opponent, date)
				proj_assists = self.calculate_projection(player_id, "assists", season, opponent, date)
				proj_rebounds = self.calculate_projection(player_id, "total_rebounds", season, opponent, date)
				proj_steals = self.calculate_projection(player_id, "steals", season, opponent, date)
				proj_blocks = self.calculate_projection(player_id, "blocks", season, opponent, date)
				proj_turnovers = self.calculate_projection(player_id, "turnovers", season, opponent, date)
				proj_minutes = depth_chart_by_player_id[player_id][1]

				end = time.time()
				#print "calculate_projections - %f" % (end-start)
				
				proj_fps = self.fpc.calculate({
					"points": proj_points,
					"total_rebounds": proj_rebounds,
					"assists": proj_assists,
					"steals": proj_steals,
					"blocks": proj_blocks,
					"turnovers": proj_turnovers
				})
				
				# Calculate squared error
				error_fps = (proj_fps - actual_fps)**2
				error_points = (proj_points - actual_points)**2
				error_assists = (proj_assists - actual_assists)**2
				error_rebounds = (proj_rebounds - actual_rebounds)**2
				error_steals = (proj_steals - actual_steals)**2
				error_blocks = (proj_blocks - actual_blocks)**2
				error_turnovers = (proj_turnovers - actual_turnovers)**2
				error_minutes = (proj_minutes - minutes_played)**2

				ssq_fps += error_fps
				ssq_points += error_points
				ssq_rebounds += error_rebounds
				ssq_assists += error_assists
				ssq_steals += error_steals
				ssq_blocks += error_blocks
				ssq_turnovers += error_turnovers
				ssq_minutes += error_minutes
				
				stddev = self.calculate_scoring_stddev(player_id, season, DFSConstants.STAR_STREET, date)[1]
			
				line = "%s,%d,%s,%s,%s,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f" % (
					player_id,
					game_number,
					date,
					team,
					opponent,
					proj_fps - stddev,
					proj_fps + stddev,
					proj_fps,
					actual_fps,
					error_fps,
					proj_points,
					actual_points,
					error_points,
					proj_assists,
					actual_assists,
					error_assists,
					proj_rebounds,
					actual_rebounds,
					error_rebounds,
					proj_steals,
					actual_steals,
					error_steals,
					proj_blocks,
					actual_blocks,
					error_blocks,
					proj_turnovers,
					actual_turnovers,
					error_turnovers,
				    proj_minutes,
				    minutes_played,
				    error_minutes
				)
				f.write(line + "\n")

		mse_fps = ssq_fps/processed
		mse_points = ssq_points/processed
		mse_assists = ssq_assists/processed
		mse_rebounds = ssq_rebounds/processed
		mse_steals = ssq_steals/processed
		mse_blocks = ssq_blocks/processed
		mse_turnovers = ssq_turnovers/processed
		mse_minutes = ssq_minutes/processed
		
		f.write("\n\n\n")

		f.write("MSE FPS,MSE Points,MSE Assists,MSE Rebounds,MSE Steals,MSE Blocks,MSE Turnovers,MSE Minutes\n")
		f.write("%f,%f,%f,%f,%f,%f,%f,%f" % (mse_fps,mse_points,mse_assists,mse_rebounds,mse_steals,mse_blocks,mse_turnovers,mse_minutes))
		f.close()
	
	def run(self):
		# Find all games being played today
		games = self.get_game_list()
		if len(games) == 0:
			logging.error("No games today. Exiting...")
			quit()

		# Determine the season we're working with
		season = games[0]["season"]

		injuries = self.injury_manager.get_currently_injured_players()

		# List of sites to make projections for
		sites = [ self.fpc.DRAFT_DAY, self.fpc.DRAFT_KINGS, DFSConstants.FAN_DUEL, self.fpc.STAR_STREET ]
		
		# CSV files to write to
		files = {}
		for s in sites:
			files[s] = open("projections/%s_%s.csv" % (s, date.today()), "w")
			files[s].write("name,position,projection,salary,floor,consistency,ceiling,"
							"avg minutes,spread,O/U,vegas projection,DvP,DPP,4x+5\n")

			# Generate the depth chart for teams playing today and print it to file.
			self.determine_depth_chart(season)
			for s in sites:
				self.print_depth_chart(season, s)
		
		print "%d games tonight..." % len(games)
		for game in games:
			print "Evaluating players in %s vs %s" % (game["home"], game["visitor"])
		
			players = self.get_players_in_game(game)
			
			for player in players:
				print "\tEvaluating %s" % player["player_info"]["name"]

				# Skip this player if they're injured.
				if player["player_id"] in injuries:
					print "\t%s is injured (%s - %s), moving on..." % (player["player_id"],
																		injuries[player["player_id"]].injury_date,
																		injuries[player["player_id"]].return_date)
					continue
			
				projections = {}

				team = self.get_team(player["player_id"], game["season"])
				opponent = game["home"] if team != game["home"] else game["visitor"]

				# Determine the vegas odds for this game based on the player's team.
				vegas_odds = self.get_vegas_odds(team)
					
				for s in self.stats:
					projections[s] = self.calculate_projection(player["player_id"], s, game["season"], opponent)
				
				for s in sites:
					self.fpc.site = s
					self.site = s
					fps = self.fpc.calculate(projections)
					consistency = self.calculate_floor_consistency_ceiling_pct(player["player_id"], game["season"], s)
					salary = self.get_salary(player["player_id"], s)
					salary = -1 if not salary else salary
					
					# FPs standard deviation
					stddev = self.calculate_scoring_stddev(player["player_id"], game["season"], s)[1]
					
					avg_minutes = self.get_avg_stat_past_n_games(player["player_id"], "minutes_played", game["season"], 5)
					
					site_position = self.get_position_on_site(player["player_id"], s)
					
					fp_rank = self.calculate_defense_vs_position_ranking(DFSConstants.FANTASY_POINTS, player["player_info"]["rg_position"], opponent, game["season"], s)
					
					# Floor and ceiling projections
					floor = fps - stddev
					ceiling = fps + stddev
					
					print "\t\t%s (%s) is projected for %f points on %s" % (player["player_info"]["name"], site_position, fps, s)
					#files[s].write("%s,%s,%f,%d,%f,%f,%f,%f\n" % (player["player_info"]["name"], site_position, fps, salary, consistency[0], consistency[1], consistency[2], avg_minutes) )
					files[s].write("%s,%s,%f,%d,%f,%f,%f,%f,%f,%f,%f,%d,%f,%f\n" % (player["player_info"]["name"],
																				site_position,
																				fps,
																				salary,
																				floor,
																				consistency[1],
																				ceiling,
																				avg_minutes,
																				vegas_odds["spread"],
																				vegas_odds["over_under"],
																				vegas_odds["projection"],
																				fp_rank,
																				salary/fps if fps > 0 else -1,
																				4*(salary/1000)+5) )
					
		
		# We're done!  Close up the files
		for f in files:
			files[f].close()

if __name__ == '__main__':
	logging.basicConfig(level=logging.INFO)

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
		projections.regression_mode = True
		projections.regression()
	else:
		projections.run()