import sys
import mysql.connector

from datetime import date

cnx = mysql.connector.connect(user='fantasy', password='fantasy', host='localhost', database='basketball_reference')

league_averages = {}

def get_player_info(player_id):
	cursor = cnx.cursor()
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
	finally:
		cursor.close()
		
	return info

def get_team(player_id, season, date=date.today()):
	cursor = cnx.cursor()
	
	query = """
		select team from game_totals_basic where player_id = '%s' and season = %d and
			game_number = (select max(game_number) from game_totals_basic 
				where player_id = '%s' and season = %d and date <= '%s')
	""" % (player_id, season, player_id, season, date)
	
	try:
		cursor.execute(query)
		for result in cursor:
			return result[0]
	finally:
		cursor.close()

##############################################################################
# To calculate defensive vs a position we want to get all of the players who
# played against a team, sum their points, and divide by the number of games
# the team has played.
##############################################################################
def calculate_defense_vs_position(metric, position, team, season):
	cursor = cnx.cursor()
	
	query = ""
	try:
		if metric == "points":
			query = """select sum(b.points)/(select max(game) from team_game_totals where team = '%s' and season = %d) 
					from players p inner join game_totals_basic b on p.id = b.player_id 
					where b.season = %d and p.position = '%s' and b.opponent = '%s'""" % (team, season, season, position, team)
		elif metric == "offensive_rebounds":
			query = """select sum(b.offensive_rebounds)/(select max(game) from team_game_totals where team = '%s' and season = %d) 
					from players p inner join game_totals_basic b on p.id = b.player_id 
					where b.season = %d and p.position = '%s' and b.opponent = '%s'""" % (team, season, season, position, team)
		elif metric == "defensive_rebounds":
			query = """select sum(b.defensive_rebounds)/(select max(game) from team_game_totals where team = '%s' and season = %d) 
					from players p inner join game_totals_basic b on p.id = b.player_id 
					where b.season = %d and p.position = '%s' and b.opponent = '%s'""" % (team, season, season, position, team)
		elif metric == "assists":
			query = """select sum(b.assists)/(select max(game) from team_game_totals where team = '%s' and season = %d) 
					from players p inner join game_totals_basic b on p.id = b.player_id 
					where b.season = %d and p.position = '%s' and b.opponent = '%s'""" % (team, season, season, position, team)
		elif metric == "steals":
			query = """select sum(b.steals)/(select max(game) from team_game_totals where team = '%s' and season = %d) 
					from players p inner join game_totals_basic b on p.id = b.player_id 
					where b.season = %d and p.position = '%s' and b.opponent = '%s'""" % (team, season, season, position, team)
		elif metric == "blocks":
			query = """select sum(b.blocks)/(select max(game) from team_game_totals where team = '%s' and season = %d) 
					from players p inner join game_totals_basic b on p.id = b.player_id 
					where b.season = %d and p.position = '%s' and b.opponent = '%s'""" % (team, season, season, position, team)
		elif metric == "turnovers":
			query = """select sum(b.turnovers)/(select max(game) from team_game_totals where team = '%s' and season = %d) 
					from players p inner join game_totals_basic b on p.id = b.player_id 
					where b.season = %d and p.position = '%s' and b.opponent = '%s'""" % (team, season, season, position, team)
		cursor.execute(query)
		
		for result in cursor:
			return result[0]
			
	finally:
		cursor.close()

def calculate_pace(team, season):
	cursor = cnx.cursor()
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
		
		return total/count
	finally:
		cursor.close()

########################################################
# Calculates the league average for the provided stat.
########################################################
def calculate_league_avg(stat, position, season):
	##########################################################
	# This calculation is somewhat expensive, so just return
	# the cached value if we've already computed it.
	##########################################################
	key = stat + "-" + position
	if key in league_averages:
		return league_averages[key]
	
	cursor = cnx.cursor()
	query = """
		select sum(%s)/(select max(t.game) from team_game_totals t where t.team = b.opponent and season = %d) as "avg", opponent 
		from game_totals_basic b inner join players p on p.id = b.player_id 
		where season = %d and position = '%s'
		group by opponent 
		order by avg desc
	""" % (stat, season, season, position)
	
	total = -1
	count = 0
	try:
		cursor.execute(query)
		for result in cursor:
			count = count + 1
			total = total + result[0]
	finally:
		cursor.close()
	
	avg = total/count
	league_averages[key] = avg
	
	return avg

def calculate_defense_factor_vs_position(position, team, season, league_avg = False):
	cursor = cnx.cursor()
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

def get_baseline(player_id, season, stat):
	cursor = cnx.cursor()
	query = """
		select avg(%s) from game_totals_basic b where player_id = '%s' and season = %d
		""" % (stat, player_id, season)
	
	adv_query = """
		select avg(usage_pct), avg(offensive_rating), avg(defensive_rating)
		from game_totals_advanced
		where player_id = '%s' and season = %d
	""" % (player_id, season)
	
	avg_stat = 0
	avg_usage_pct = 0
	avg_off_rating = 0
	avg_def_rating = 0
	
	try:
		cursor.execute(query)
		for result in cursor:
			avg_stat = result[0]
		
		cursor.execute(adv_query)
		for result in cursor:
			avg_usage_pct = result[0]
			avg_off_rating = result[1]
			avg_def_rating = result[2]
	finally:
		cursor.close()
	
	return (avg_stat, avg_usage_pct, avg_off_rating, avg_def_rating)

def calculate_projection(player_id, season, opponent, date=date.today()):
	print "%s" % date

	info = get_player_info(player_id)
	team = get_team(player_id, season)
	baselines = get_baseline(id,2013,'points')
	
	avg_points = baselines[0]
	adjusted_points = avg_points
	
	#######################################
	# Take pace of the game into account.
	#######################################
	team_pace = calculate_pace(team, season)
	opp_pace = calculate_pace(opponent, season)
	avg_pace = (team_pace + opp_pace)/2
	pace_factor = avg_pace/team_pace
	
	adjusted_points = float(avg_points) * float(pace_factor)
	
	######################################################################
	# Effectiveness of opponent defense, compared to the league average
	# for this player's position.
	######################################################################
	league_avg = calculate_league_avg("points", info["position"], season)
	def_factor = calculate_defense_vs_position("points", info["position"], opponent, season)
	
	adjusted_points = adjusted_points * float(def_factor/league_avg)
	
	return adjusted_points

positions = ["G","F","C"]
teams = ["ATL","BOS","BRK","LAL"]

id = 'anthoca01'
game_date = date(2013,11,25)
print calculate_projection(id, 2013, 'BOS', game_date)
