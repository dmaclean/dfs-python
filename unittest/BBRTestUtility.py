import sqlite3
import os
import inspect
import sys

###########################################
# Utility class for helping with testing.
###########################################
class BBRTestUtility():
	def __init__(self):
		self.sql = ""
		self.readSQL()
		
		self.conn = sqlite3.connect(':memory:')
		
		cmd_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))
		if cmd_folder not in sys.path:
			sys.path.insert(0, cmd_folder)

		# use this if you want to include modules from a subforder
		cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"subfolder")))
		if cmd_subfolder not in sys.path:
			sys.path.insert(0, cmd_subfolder)
	
	##########################################################################
	# Reads in the basketball.sql file, where all SQL for the project lives.
	##########################################################################
	def readSQL(self):
		f = open("../basketball.sql","r")
		
		try:
			content = ""
			for line in f:
				content = content + line.replace("\t","").replace("\n","")
			
			self.sql = content.split(";")
		finally:
			f.close()
	
	#########################
	# Runs the read-in SQL.
	#########################
	def runSQL(self):
		cursor = self.conn.cursor()
		
		try:
			for statement in self.sql:
				cursor.execute(statement)
				self.conn.commit()
		except sqlite3.Error, e:
			print "Something went wrong with SQL. %s" % e.args[0]
		finally:
			cursor.close()
	
	############################################################
	# Convenience method for inserting into the players table.
	############################################################
	def insert_into_players(self, values):
		cursor = self.conn.cursor()
		query = """
			insert into players (
				id, name, position, height, weight, url
			)
			values ('%s','%s','%s',%d,%d,'%s')
		""" % (values["id"], values["name"], values["position"], values["height"],values["weight"],values["url"])

		try:
			cursor.execute(query)
		except sqlite3.Error, e:
			print "Something went wrong.  %s" % e.args[0]
		finally:
			cursor.close()
	
	######################################################################
	# Convenience method for inserting into the game_totals_basic table.
	######################################################################
	def insert_into_game_totals_basic(self, values):
		cursor = self.conn.cursor()
		query = """
			insert into game_totals_basic (
				player_id,
				season,
				game_number,
				date,
				age,
				team,
				home,
				opponent,
				result,
				games_started,
				minutes_played,
				field_goals,
				field_goal_attempts,
				field_goal_pct,
				three_point_field_goals,
				three_point_field_goal_attempts,
				three_point_field_goal_pct,
				free_throws,
				free_throw_attempts,
				free_throw_pct,
				offensive_rebounds,
				defensive_rebounds,
				total_rebounds,
				assists,
				steals,
				blocks,
				turnovers,
				personal_fouls,
				points,
				game_score,
				plus_minus
			) values (
				'%s',%d,%d,'%s',%d,'%s',%d,'%s','%s',%d,
				%f,%d,%d,%f,%d,%d,%f,%d,%d,%f,%d,%d,%d,
				%d,%d,%d,%d,%d,%d,%f,%d
			)
		""" % (
			values["player_id"],
			values["season"],
			values["game_number"],
			values["date"],
			values["age"],
			values["team"],
			values["home"],
			values["opponent"],
			values["result"],
			values["games_started"],
			values["minutes_played"],
			values["field_goals"],
			values["field_goal_attempts"],
			values["field_goal_pct"],
			values["three_point_field_goals"],
			values["three_point_field_goal_attempts"],
			values["three_point_field_goal_pct"],
			values["free_throws"],
			values["free_throw_attempts"],
			values["free_throw_pct"],
			values["offensive_rebounds"],
			values["defensive_rebounds"],
			values["total_rebounds"],
			values["assists"],
			values["steals"],
			values["blocks"],
			values["turnovers"],
			values["personal_fouls"],
			values["points"],
			values["game_score"],
			values["plus_minus"]
		)
		
		try:
			cursor.execute(query)
		except sqlite3.Error, e:
			print "Something went wrong.  %s" % e.args[0]
		finally:
			cursor.close()
	
	def insert_into_game_totals_advanced(self, values):
		cursor = self.conn.cursor()
		query = """
			insert into game_totals_advanced (
				player_id,
				game_number,
				season,
				date,
				age,
				team,
				home,
				opponent,
				result,
				games_started,
				minutes_played,
				true_shooting_pct,
				effective_field_goal_pct,
				offensive_rebound_pct,
				defensive_rebound_pct,
				total_rebound_pct,
				assist_pct,
				steal_pct,
				block_pct,
				turnover_pct,
				usage_pct,
				offensive_rating,
				defensive_rating,
				game_score
			) values (
				'%s',%d,%d,'%s',%d,'%s',%d,'%s','%s',%d,
				%d,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%d,%d,%f
			)
		""" % (
			values["player_id"],
			values["game_number"],
			values["season"],
			values["date"],
			values["age"],
			values["team"],
			values["home"],
			values["opponent"],
			values["result"],
			values["games_started"],
			values["minutes_played"],
			values["true_shooting_pct"],
			values["effective_field_goal_pct"],
			values["offensive_rebound_pct"],
			values["defensive_rebound_pct"],
			values["total_rebound_pct"],
			values["assist_pct"],
			values["steal_pct"],
			values["block_pct"],
			values["turnover_pct"],
			values["usage_pct"],
			values["offensive_rating"],
			values["defensive_rating"],
			values["game_score"]
		)
		
		try:
			cursor.execute(query)
		except:
			print "Something went wrong with insert_info_game_totals_advanced."
		finally:
			cursor.close()
	
	def insert_into_team_game_totals(self, values):
		cursor = self.conn.cursor()
		query = ("""
			insert into team_game_totals (
				team,
				season,
				game,
				date,
				home,
				opponent,
				result,
				minutes_played,
				field_goals,
				field_goal_attempts,
				three_point_field_goals,
				three_point_field_goal_attempts,
				free_throws,
				free_throw_attempts,
				offensive_rebounds,
				total_rebounds,
				assists,
				steals,
				blocks,
				turnovers,
				personal_fouls,
				points,
				opp_field_goals,
				opp_field_goal_attempts,
				opp_three_point_field_goals,
				opp_three_point_field_goal_attempts,
				opp_free_throws,
				opp_free_throw_attempts,
				opp_offensive_rebounds,
				opp_total_rebounds,
				opp_assists,
				opp_steals,
				opp_blocks,
				opp_turnovers,
				opp_personal_fouls,
				opp_points
			) values (
				'%s',%d,%d,'%s',%d,'%s','%s',%d,%d,%d,%d,%d,
				%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,
				%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d
			)
		""") % (
			values["team"],
			values["season"],
			values["game"],
			values["date"],
			values["home"],
			values["opponent"],
			values["result"],
			values["minutes_played"],
			values["field_goals"],
			values["field_goal_attempts"],
			values["three_point_field_goals"],
			values["three_point_field_goal_attempts"],
			values["free_throws"],
			values["free_throw_attempts"],
			values["offensive_rebounds"],
			values["total_rebounds"],
			values["assists"],
			values["steals"],
			values["blocks"],
			values["turnovers"],
			values["personal_fouls"],
			values["points"],
			values["opp_field_goals"],
			values["opp_field_goal_attempts"],
			values["opp_three_point_field_goals"],
			values["opp_three_point_field_goal_attempts"],
			values["opp_free_throws"],
			values["opp_free_throw_attempts"],
			values["opp_offensive_rebounds"],
			values["opp_total_rebounds"],
			values["opp_assists"],
			values["opp_steals"],
			values["opp_blocks"],
			values["opp_turnovers"],
			values["opp_personal_fouls"],
			values["opp_points"]
		)
		
		try:
			cursor.execute(query)
		finally:
			cursor.close()
	
	def insert_into_schedules(self, values):
		cursor = self.conn.cursor()
		query = """
			insert into schedules (date, season, visitor, home)
			values ('%s',%d,'%s','%s')
		""" % (values["date"], values["season"], values["visitor"], values["home"])
		
		try:
			cursor.execute(query)
		finally:
			cursor.close()
	
	def insert_into_salaries(self, values):
		cursor = self.conn.cursor()
		query = """
			insert into salaries (player_id, site, salary, date)
			values ('%s','%s',%d,'%s')
		""" % (values["player_id"], values["site"], values["salary"], values["date"])
		
		try:
			cursor.execute(query)
		finally:
			cursor.close()
	
	def insert_into_dfs_site_positions(self, values):
		cursor = self.conn.cursor()
		query = """
			insert into dfs_site_positions (player_id, site, position)
			values ('%s','%s','%s')
		""" % (values["player_id"], values["site"], values["position"])
		
		try:
			cursor.execute(query)
		finally:
			cursor.close()