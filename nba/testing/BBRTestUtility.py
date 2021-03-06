import sqlite3
import os
import inspect
import sys
from datetime import date

from shared.dfs_constants import DFSConstants
from pymongo import MongoClient


###########################################
# Utility class for helping with testing.
###########################################
class BBRTestUtility():
	def __init__(self):
		self.sql = ""
		self.readSQL()
		
		self.conn = sqlite3.connect(':memory:')

		self.mongo_client = None
		
		cmd_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))
		if cmd_folder not in sys.path:
			sys.path.insert(0, cmd_folder)

		# use this if you want to include modules from a subforder
		cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"subfolder")))
		if cmd_subfolder not in sys.path:
			sys.path.insert(0, cmd_subfolder)

	def get_mongo_db_instance(self):
		"""
		Retrieve an instance of a MongoDB database.  For our testing purposes we'll
		call our test database "test_basketball"
		"""
		self.mongo_client = MongoClient()

		return self.mongo_client[DFSConstants.MONGO_NBA_TEST_DB_NAME]
	
	##########################################################################
	# Reads in the basketball.sql file, where all SQL for the project lives.
	##########################################################################
	def readSQL(self):
		f = open("../basketball.sql","r")
		
		try:
			content = ""
			for line in f:
				content = content + line.replace("\t","").replace("\n","").replace("auto_increment","")
			
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

	def generate_default_player_info(self):
		"""
		Generates a dictionary of default values for the players table.
		"""
		return {
			"id": "",
			"name": "Test",
			"position": "G",
			"height": 0,
			"weight": 0,
			"url": "something"
		}

	def generate_default_team_game_totals_info(self):
		"""
		Generates a dictionary of default values for the team_game_totals table.
		"""
		return {
			"team": "",
			"season": date.today().year,
			"game": 0,
			"date": date.today(),
			"home": True,
			"opponent": "",
			"result": "",
			"minutes_played": 240,
			"field_goals": 0,
			"field_goal_attempts": 0,
			"three_point_field_goals": 0,
			"three_point_field_goal_attempts": 0,
			"free_throws": 0,
			"free_throw_attempts": 0,
			"offensive_rebounds": 0,
			"total_rebounds": 0,
			"assists": 0,
			"steals": 0,
			"blocks": 0,
			"turnovers": 0,
			"personal_fouls": 0,
			"points": 0,
			"opp_field_goals": 0,
			"opp_field_goal_attempts": 0,
			"opp_three_point_field_goals": 0,
			"opp_three_point_field_goal_attempts": 0,
			"opp_free_throws": 0,
			"opp_free_throw_attempts": 0,
			"opp_offensive_rebounds": 0,
			"opp_total_rebounds": 0,
			"opp_assists": 0,
			"opp_steals": 0,
			"opp_blocks": 0,
			"opp_turnovers": 0,
			"opp_personal_fouls": 0,
			"opp_points": 0
		}

	def generate_default_fantasy_points_info(self):
		return {
			"game_totals_basic_id": 0,
			"player_id": "",
			"site": "",
			"season": date.today().year,
			"game_number": 0,
			"points": 0
		}

	def generate_default_game_totals_basic_info(self):
		"""
		Generates a dictionary of default values for the game_totals_basic table.
		"""
		return {
			"player_id": "test",
			"season": date.today().year,
			"game_number": 0,
			"date": date.today(),
			"age": 0,
			"team": "BOS",
			"home": True,
			"opponent": "BOS",
			"result": "",
			"games_started": 0,
			"minutes_played": 0,
			"field_goals": 0,
			"field_goal_attempts": 0,
			"field_goal_pct": 0,
			"three_point_field_goals": 0,
			"three_point_field_goal_attempts": 0,
			"three_point_field_goal_pct": 0,
			"free_throws": 0,
			"free_throw_attempts": 0,
			"free_throw_pct": 0,
			"offensive_rebounds": 0,
			"defensive_rebounds": 0,
			"total_rebounds": 0,
			"assists": 0,
			"steals": 0,
			"blocks": 0,
			"turnovers": 0,
			"personal_fouls": 0,
			"points": 0,
			"game_score": 0,
			"plus_minus": 0
		}

	def generate_default_injury_info(self):
		return {
			"player_id": "",
		    "injury_date": date.today(),
		    "return_date": date.today(),
		    "details": ""
		}
	
	############################################################
	# Convenience method for inserting into the players table.
	############################################################
	def insert_into_players(self, values):
		cursor = self.conn.cursor()
		
		if "rg_position" not in values:
			values["rg_position"] = ""
		
		query = """
			insert into players (
				id, name, position, rg_position, height, weight, url
			)
			values ('%s','%s','%s','%s',%d,%d,'%s')
		""" % (values["id"], values["name"], values["position"], values["rg_position"], values["height"],values["weight"],values["url"])

		try:
			cursor.execute(query)
		except sqlite3.Error, e:
			print "Something went wrong.  %s" % e.args[0]
		finally:
			cursor.close()
	
	def select_from_players(self, player_id):
		cursor = self.conn.cursor()
		
		query = "select * from players where id = '%s'" % (player_id)
		
		try:
			cursor.execute(query)
			
			for result in cursor:
				return {
					"id": result[0],
					"name": result[1],
					"position": result[2],
					"rg_position": result[3],
					"height": result[4],
					"weight": result[5],
					"url": result[6]
				}
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
			return cursor.lastrowid
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
	
	def select_from_dfs_site_positions(self, player_id, site):
		cursor = self.conn.cursor()
		query = """
			select position from dfs_site_positions where player_id = '%s' and site = '%s'
		""" % (player_id, site)
		
		try:
			cursor.execute(query)
			for result in cursor:
				return result[0]
		finally:
			cursor.close()
	
	def insert_into_fantasy_points(self, values):
		cursor = self.conn.cursor()
		query = """
			insert into fantasy_points (game_totals_basic_id, player_id, site, season, game_number, points) 
			values (%d,'%s','%s',%d,%d,%f)
		""" % (values["game_totals_basic_id"], values["player_id"], values["site"], values["season"], values["game_number"], values["points"])
		
		try:
			cursor.execute(query)
			return cursor.lastrowid
		finally:
			cursor.close()
	
	def select_from_fantasy_points(self, player_id, site, season, game_number):
		cursor = self.conn.cursor()
		query = """
			select points from fantasy_points where player_id = '%s' and site = '%s' and season = %d and game_number = %d
		""" % (player_id, site, season, game_number)
		
		try:
			cursor.execute(query)
			for result in cursor:
				return result[0]
		finally:
			cursor.close()
	
	def insert_into_player_name_mapping(self, values):
		cursor = self.conn.cursor()
		query = """
			insert into player_name_mapping (bbr_name, site_name, site) values ('%s','%s','%s')
		""" % (values["bbr_name"], values["site_name"], values["site"])
		
		try:
			cursor.execute(query)
		finally:
			cursor.close()
	
	def select_from_player_name_mapping(self, values):
		cursor = self.conn.cursor()
		query = """
			select site_name from player_name_mapping where bbr_name = '%s' and site = '%s'
		""" % (values["bbr_name"], values["site"])
		
		try:
			cursor.execute(query)
			for result in cursor:
				return result[0]
		finally:
			cursor.close()
	
	def insert_into_vegas(self, values):
		cursor = self.conn.cursor()
		query = """
			insert into vegas (date, road_team, home_team, spread_road, spread_home, over_under, projection_road, projection_home) 
			values ('%s','%s','%s', %f, %f, %f, %f, %f)
		""" % (values["date"], values["road_team"], values["home_team"], values["spread_road"], values["spread_home"], 
				values["over_under"], values["projection_road"], values["projection_home"])
		
		try:
			cursor.execute(query)
		finally:
			cursor.close()
	
	def select_from_vegas(self, values):
		cursor = self.conn.cursor()
		query = """
			select spread_road, spread_home, over_under, projection_road, projection_home from vegas 
			where date = '%s' and road_team = '%s' and home_team = '%s'
		""" % (values["date"], values["road_team"], values["home_team"])
		
		try:
			cursor.execute(query)
			for result in cursor:
				return (result[0], result[1], result[2], result[3], result[4])
		finally:
			cursor.close()
	
	