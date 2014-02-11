import httplib
import logging
import random
import sys
import time
import mysql.connector
from datetime import date, timedelta
from HTMLParser import HTMLParser

from models.injury_manager import InjuryManager, Injury
from projections import Projections


class Processor:
	source = ""
	file = ""
	season = -1
	type = "players"
	all_players = False
	yesterday_only = False
	
	listParser = None
	playerMainParser = None
	playerGameLogParser = None
	playerSplitsParser = None
	teamGameLogParser = None
	teamSplitsParser = None
	
	def __init__(self):
		self.source = "file"
		self.file = "player_list.html"
		self.listParser = BasketballReferencePlayerListParser()
		self.playerMainParser = BasketballReferencePlayerMainParser()
		self.playerGameLogParser = BasketballReferenceGameLogParser()
		self.playerSplitsParser = BasketballReferenceSplitsParser()
		self.teamSplitsParser = BasketballReferenceTeamSplitsParser()
		self.teamGameLogParser = BasketballReferenceTeamGameLogParser()

		self.injury_manager = InjuryManager()
	
	def readCLI(self):
		for arg in sys.argv:
			if arg == "basketball.py":
				pass
			else:
				pieces = arg.split("=")
				if pieces[0] == "source":
					self.source = pieces[1]
				elif pieces[0] == "file":
					self.file = pieces[1]
				elif pieces[0] == "season":
					self.season = int(pieces[1])
				elif pieces[0] == "type":
					self.type = pieces[1]
				elif pieces[0] == "all_players":
					self.all_players = pieces[1] == "true"
				elif pieces[0] == "yesterday_only":
					self.yesterday_only = pieces[1] == "true"
					
	
	##############################################################################
	# Make an HTTP GET request to the server and return the data that comes back
	# in the response.
	##############################################################################
	def fetchData(self, url, logToConsole):
		successful = False
		data = ""
		
		while not successful:
			try:
				conn = httplib.HTTPConnection("www.basketball-reference.com", timeout=5)
				conn.request("GET", url)
				resp = conn.getresponse()
				content_type = resp.getheader("content-type")

				encoding = None
				if content_type.find("charset=") > -1:
					encoding = content_type.split("charset=")[1]

				if logToConsole:
					print resp.status,"for",url

				if encoding:
					data = resp.read().decode(encoding, 'ignore')
				else:
					data = resp.read()
				
				conn.close()
				successful = True
			except Exception, err:
				logging.error("Issue connecting to basketball-reference.  Retrying in 10 seconds...", str(err))
				time.sleep( 10 )
		
		return data
	
	def process(self):
		self.readCLI()
		if self.type == "teams":
			self.processTeams()
		elif self.type == "schedule":
			self.processSchedule()
		else:
			self.processPlayers()
	
	def processSchedule(self):
		parser = BasketballReferenceScheduleParser()
		
		if self.source == "site":
			cnx = mysql.connector.connect(user='fantasy', password='fantasy', host='localhost', database='basketball_reference')
			
			if self.season != -1:
				seasons = [self.season]
			else:
				seasons = [2010,2011,2012,2013]
			
			for season in seasons:
				url = "/leagues/NBA_%s_games.html" % str(season+1)
				data = self.fetchData(url, True)
				parser.feed(data)
				print parser.data
				
				for d in parser.data:
					print d
					entry = Schedule(d["date"], d["season"], d["home"], d["visitor"])
					if not entry.game_exists(cnx):
						entry.insert_game(cnx)
								
		else:
			f = open("tests/" + self.source,"r")
			data = f.read().replace("\n","")
			
			parser = BasketballReferenceScheduleParser()
			parser.feed(data)
			
	
	##############################################################
	# Process the individual data, season totals, game logs, and 
	# splits for a particular player.
	##############################################################
	def processPlayers(self):
		parser = None
		
		if self.source == "site":
			cnx = mysql.connector.connect(user='fantasy', password='fantasy', host='localhost', database='basketball_reference')
			alphabet = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]

			# Figure out who played yesterday and collect their URLs.
			projections = Projections()
			one_day = timedelta(days=1)
			yesterday = date.today() - one_day
			games = projections.get_game_list(yesterday)

			eligible_urls = []
			for game in games:
				players = projections.get_players_in_game(game)
				for player in players:
					eligible_urls.append(player["player_info"]["url"])

			for letter in alphabet:
				data = self.fetchData("/players/"+letter+"/", True)
				
				# Parse the HTML for the list of players at this letter and iterate
				# over the players found.
				self.listParser.players = []
				
				# Should we be grabbing all players (not just active)?
				self.listParser.all_players = self.all_players
				
				self.listParser.feed(data)
				for player in self.listParser.players:
					if not player.playerExists(cnx):
						player.writePlayerInfoToDatabase(cnx)
					
					s = "%s,%s,%d,%d,%s\n" % (player.name, player.positions, player.height, player.weight, player.url) 

					if self.yesterday_only and player.url not in eligible_urls:
						print "\t%s didn't play last night.  Moving on..." % player.name
						continue

					time.sleep( 5 + (5*random.random()) )
					data = self.fetchData(player.url, True)
					
					# Reset the stats maps before we parse the HTML
					self.playerMainParser.totals_stats = {}
					self.playerMainParser.advanced_stats = {}
					
					# Parse HTML
					self.playerMainParser.feed(data)
					
					#######################################################################
					# Iterate over the totals stats for each season and write to database
					#######################################################################
					player.season_totals = self.playerMainParser.totals_stats
					for k in self.playerMainParser.totals_stats:
						if self.season != -1 and k != self.season:
							print "Skipping",k,"- only interested in", self.season
							continue
						else:
							print "Processing season", k
					
						if not player.seasonTotalsExist(cnx, player.code, k):
							player.writeSeasonTotalsToDatabase(cnx, player.code, k)
						else:
							player.updateSeasonTotalsInDatabase(cnx, player.code, k)
						
						######################
						# Grab the game logs.
						######################
						time.sleep( 5 + (5*random.random()) )
						gameLogUrl = "/players/" + letter + "/" + player.code + "/gamelog/" + str(k+1)
						data = self.fetchData(gameLogUrl, True)
						
						self.playerGameLogParser.basic_game_stats = {}
						self.playerGameLogParser.advanced_game_stats = {}
						self.playerGameLogParser.feed(data)
						player.game_basic = self.playerGameLogParser.basic_game_stats
						player.game_advanced = self.playerGameLogParser.advanced_game_stats
						
						for game_number in player.game_basic:
							# Determine if the player is listed as injured for the game on this date.
							injury = self.injury_manager.is_player_injured(player.code, player.game_basic[game_number]["date"])
							if injury:
								self.injury_manager.fix_injury_entry(injury, player.game_basic[game_number]["date"])

							# Write the game entry into game_totals_basic if it's not already there.
							if not player.basicGameLogStatsExist(cnx, player.code, k, game_number):
								player.writeBasicGameLogStatsToDatabase(cnx, player.code, k, game_number)
						
						for game_number in player.game_advanced:
							if not player.advancedGameLogStatsExist(cnx, player.code, k, game_number):
								player.writeAdvancedGameLogStatsToDatabase(cnx, player.code, k, game_number)
					
						####################
						# Grab the splits.
						####################
						time.sleep( 5 + (5*random.random()) )
						splitUrl = "/players/" + letter + "/" + player.code + "/splits/" + str(k+1)
						data = self.fetchData(splitUrl, True)
						
						self.playerSplitsParser.stats = {}
						self.playerSplitsParser.feed(data)
						player.splits = self.playerSplitsParser.stats
						
						for type in player.splits:
							for subtype in player.splits[type]:
								if not player.splitsExist(cnx, player.code, k, type, subtype):
									player.writeSplitToDatabase(cnx, player.code, k, type, subtype)
								else:
									player.updateSplitInDatabase(cnx, player.code, k, type, subtype)
					
					#########################################################################
					# Iterate over the advanced stats for each season and write to database
					#########################################################################
					player.season_advanced = self.playerMainParser.advanced_stats
					for k in self.playerMainParser.advanced_stats:
						if not player.seasonAdvancedExist(cnx, player.code, k):
							player.writeSeasonAdvancedStatsToDatabase(cnx, player.code, k)
						else:
							player.updateSeasonAdvancedStatsInDatabase(cnx, player.code, k)
					
				time.sleep( 5 + (5*random.random()) )
		else:
			f = open("tests/" + self.source,"r")
			data = f.read().replace("\n","")
			
			if self.source == "player_list.html":
				parser = BasketballReferencePlayerListParser()
				parser.all_players = self.all_players
			elif self.source == "player_main.html" or self.source == "forest_able.html":
				parser = BasketballReferencePlayerMainParser()
			elif self.source == "player_gamelog.html":
				parser = BasketballReferenceGameLogParser()
			elif self.source == "player_splits.html" or self.source == "player_splits_no_plusminus.html":
				parser = BasketballReferenceSplitsParser()
			elif self.source == "team_splits.html":
				parser = BasketballReferenceTeamSplitsParser()
			elif self.source == "team_gamelog.html" or self.source == "team_gamelog_2012.html":
				parser = BasketballReferenceTeamGameLogParser()
			parser.feed(data)
	
	###################################################################
	# Process the game logs and splits for each team for each season.
	###################################################################
	def processTeams(self):
		parser = None
		
		if self.source == "site":
			cnx = mysql.connector.connect(user='fantasy', password='fantasy', host='localhost', database='basketball_reference')
			
			if self.season != -1:
				seasons = [self.season]
			else:
				seasons = [2010,2011,2012,2013]
			
			for season in seasons:			
				cursor = cnx.cursor()

				teams = []
				if self.yesterday_only:
					projections = Projections()
					one_day = timedelta(days=1)
					yesterday = date.today() - one_day
					games = projections.get_game_list(yesterday)

					for game in games:
						teams.append(game["home"])
						teams.append(game["visitor"])
				else:
					query = "select distinct team from game_totals_basic where season = %d order by team" % season
					cursor.execute(query)

					for (result) in cursor:
						teams.append(result[0])
					cursor.close()

				for team_name in teams:
					#####################################
					# Get game log data for team/season
					#####################################
					time.sleep( 10 + (10*random.random()) )
					data = self.fetchData("/teams/"+team_name+"/"+str(season+1)+"/gamelog/", True)
					self.teamGameLogParser.game_stats = {}
					self.teamGameLogParser.feed(data)
					
					team = Team(team_name, self.teamGameLogParser.game_stats)
					for game in team.game_log_stats:
						if not team.teamGameLogExists(cnx, season, game):
							team.writeTeamGameLogToDatabase(cnx, season, game)
						else:
							team.updateTeamGameLogInDatabase(cnx, season, game)
					
					###################################
					# Get splits data for team/season
					###################################
					time.sleep( 10 + (10*random.random()) )
					data = self.fetchData("/teams/"+team_name+"/"+str(season+1)+"/splits/", True)
					self.teamSplitsParser.stats = {}
					self.teamSplitsParser.feed(data)
					
					team.splits_stats = self.teamSplitsParser.stats
					for type in team.splits_stats:
						for subtype in team.splits_stats[type]:
							if not team.teamSplitExists(cnx, season, type, subtype):
								team.writeTeamSplitToDatabase(cnx, season, type, subtype)
							else:
								team.updateTeamSplitInDatabase(cnx, season, type, subtype)
		else:
			f = open("tests/" + self.source,"r")
			data = f.read().replace("\n","")
			
			if self.source == "player_list.html":
				parser = BasketballReferencePlayerListParser()
			elif self.source == "player_main.html":
				parser = BasketballReferencePlayerMainParser()
			elif self.source == "player_gamelog.html":
				parser = BasketballReferenceGameLogParser()
			elif self.source == "player_splits.html" or self.source == "player_splits_no_plusminus.html":
				parser = BasketballReferenceSplitsParser()
			elif self.source == "team_splits.html":
				parser = BasketballReferenceTeamSplitsParser()
			elif self.source == "team_gamelog.html":
				parser = BasketballReferenceTeamGameLogParser()
			parser.feed(data)


class Team:
	def __init__(self, name=None, game_log_stats=None, splits_stats=None):
		self.name = name
		self.game_log_stats = game_log_stats
		self.splits_stats = splits_stats
	
	#############################################################################
	# Determine if a game log for a particular team/season/game exists already.
	#############################################################################
	def teamGameLogExists(self, conn, season, game_number):
		cursor = conn.cursor()
		query = ("select id from team_game_totals where team = '%s' and season = %d and game = %d") % (self.name, season, game_number)
		
		try:
			cursor.execute(query)
		
			for (id) in cursor:
				cursor.close()
				return True
		
			return False
		finally:
			cursor.close()
	
	#################################################
	# Write a team's game log data to the database.
	#################################################
	def writeTeamGameLogToDatabase(self, conn, season, game_number):
		cursor = conn.cursor()
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
			self.name,
			season,
			game_number,
			self.game_log_stats[game_number]["date"],
			self.game_log_stats[game_number]["home"],
			self.game_log_stats[game_number]["opponent"],
			self.game_log_stats[game_number]["result"],
			self.game_log_stats[game_number]["minutes_played"],
			self.game_log_stats[game_number]["field_goals"],
			self.game_log_stats[game_number]["field_goal_attempts"],
			self.game_log_stats[game_number]["three_point_field_goals"],
			self.game_log_stats[game_number]["three_point_field_goal_attempts"],
			self.game_log_stats[game_number]["free_throws"],
			self.game_log_stats[game_number]["free_throw_attempts"],
			self.game_log_stats[game_number]["offensive_rebounds"],
			self.game_log_stats[game_number]["total_rebounds"],
			self.game_log_stats[game_number]["assists"],
			self.game_log_stats[game_number]["steals"],
			self.game_log_stats[game_number]["blocks"],
			self.game_log_stats[game_number]["turnovers"],
			self.game_log_stats[game_number]["personal_fouls"],
			self.game_log_stats[game_number]["points"],
			self.game_log_stats[game_number]["opp_field_goals"],
			self.game_log_stats[game_number]["opp_field_goal_attempts"],
			self.game_log_stats[game_number]["opp_three_point_field_goals"],
			self.game_log_stats[game_number]["opp_three_point_field_goal_attempts"],
			self.game_log_stats[game_number]["opp_free_throws"],
			self.game_log_stats[game_number]["opp_free_throw_attempts"],
			self.game_log_stats[game_number]["opp_offensive_rebounds"],
			self.game_log_stats[game_number]["opp_total_rebounds"],
			self.game_log_stats[game_number]["opp_assists"],
			self.game_log_stats[game_number]["opp_steals"],
			self.game_log_stats[game_number]["opp_blocks"],
			self.game_log_stats[game_number]["opp_turnovers"],
			self.game_log_stats[game_number]["opp_personal_fouls"],
			self.game_log_stats[game_number]["opp_points"]
		)
		
		try:
			cursor.execute(query)
		finally:
			cursor.close()
			
	def updateTeamGameLogInDatabase(self, conn, season, game_number):
		cursor = conn.cursor()
		query = ("""
			update team_game_totals set
				date = '%s',
				home = %d,
				opponent = '%s',
				result = '%s',
				minutes_played = %d,
				field_goals = %d,
				field_goal_attempts = %d,
				three_point_field_goals = %d,
				three_point_field_goal_attempts = %d,
				free_throws = %d,
				free_throw_attempts = %d,
				offensive_rebounds = %d,
				total_rebounds = %d,
				assists = %d,
				steals = %d,
				blocks = %d,
				turnovers = %d,
				personal_fouls = %d,
				points = %d,
				opp_field_goals = %d,
				opp_field_goal_attempts = %d,
				opp_three_point_field_goals = %d,
				opp_three_point_field_goal_attempts = %d,
				opp_free_throws = %d,
				opp_free_throw_attempts = %d,
				opp_offensive_rebounds = %d,
				opp_total_rebounds = %d,
				opp_assists = %d,
				opp_steals = %d,
				opp_blocks = %d,
				opp_turnovers = %d,
				opp_personal_fouls = %d,
				opp_points = %d
			where team = '%s' and season = %d and game = %d
		""") % (
			self.game_log_stats[game_number]["date"],
			self.game_log_stats[game_number]["home"],
			self.game_log_stats[game_number]["opponent"],
			self.game_log_stats[game_number]["result"],
			self.game_log_stats[game_number]["minutes_played"],
			self.game_log_stats[game_number]["field_goals"],
			self.game_log_stats[game_number]["field_goal_attempts"],
			self.game_log_stats[game_number]["three_point_field_goals"],
			self.game_log_stats[game_number]["three_point_field_goal_attempts"],
			self.game_log_stats[game_number]["free_throws"],
			self.game_log_stats[game_number]["free_throw_attempts"],
			self.game_log_stats[game_number]["offensive_rebounds"],
			self.game_log_stats[game_number]["total_rebounds"],
			self.game_log_stats[game_number]["assists"],
			self.game_log_stats[game_number]["steals"],
			self.game_log_stats[game_number]["blocks"],
			self.game_log_stats[game_number]["turnovers"],
			self.game_log_stats[game_number]["personal_fouls"],
			self.game_log_stats[game_number]["points"],
			self.game_log_stats[game_number]["opp_field_goals"],
			self.game_log_stats[game_number]["opp_field_goal_attempts"],
			self.game_log_stats[game_number]["opp_three_point_field_goals"],
			self.game_log_stats[game_number]["opp_three_point_field_goal_attempts"],
			self.game_log_stats[game_number]["opp_free_throws"],
			self.game_log_stats[game_number]["opp_free_throw_attempts"],
			self.game_log_stats[game_number]["opp_offensive_rebounds"],
			self.game_log_stats[game_number]["opp_total_rebounds"],
			self.game_log_stats[game_number]["opp_assists"],
			self.game_log_stats[game_number]["opp_steals"],
			self.game_log_stats[game_number]["opp_blocks"],
			self.game_log_stats[game_number]["opp_turnovers"],
			self.game_log_stats[game_number]["opp_personal_fouls"],
			self.game_log_stats[game_number]["opp_points"],
			self.name,
			season,
			game_number
		)
		
		try:
			cursor.execute(query)
		finally:
			cursor.close()
	
	
	#####################################################################
	# Determine if a split for a particular team/season exists already.
	#####################################################################
	def teamSplitExists(self, conn, season, type, subtype):
		cursor = conn.cursor()
		query = ("select id from team_splits where team = '%s' and season = %d and type = '%s' and subtype = '%s'") % (self.name, season, type, subtype)
		
		try:
			cursor.execute(query)
		
			for (id) in cursor:
				cursor.close()
				return True
		
			return False
		finally:
			cursor.close()
	
	###################################################
	# Insert a new record into the team_splits table.
	###################################################
	def writeTeamSplitToDatabase(self, conn, season, type, subtype):
		cursor = conn.cursor()
		query = ("""
			insert into team_splits (
				team,
				season,
				type,
				subtype,
				games,
				wins,
				losses,
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
				'%s',%d,'%s','%s',%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,
				%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d				
			)
		""") % (
			self.name,
			season,
			type,
			subtype,
			self.splits_stats[type][subtype]["games"],
			self.splits_stats[type][subtype]["wins"],
			self.splits_stats[type][subtype]["losses"],
			self.splits_stats[type][subtype]["field_goals"],
			self.splits_stats[type][subtype]["field_goal_attempts"],
			self.splits_stats[type][subtype]["three_point_field_goals"],
			self.splits_stats[type][subtype]["three_point_field_goal_attempts"],
			self.splits_stats[type][subtype]["free_throws"],
			self.splits_stats[type][subtype]["free_throw_attempts"],
			self.splits_stats[type][subtype]["offensive_rebounds"],
			self.splits_stats[type][subtype]["total_rebounds"],
			self.splits_stats[type][subtype]["assists"],
			self.splits_stats[type][subtype]["steals"],
			self.splits_stats[type][subtype]["blocks"],
			self.splits_stats[type][subtype]["turnovers"],
			self.splits_stats[type][subtype]["personal_fouls"],
			self.splits_stats[type][subtype]["points"],
			self.splits_stats[type][subtype]["opp_field_goals"],
			self.splits_stats[type][subtype]["opp_field_goal_attempts"],
			self.splits_stats[type][subtype]["opp_three_point_field_goals"],
			self.splits_stats[type][subtype]["opp_three_point_field_goal_attempts"],
			self.splits_stats[type][subtype]["opp_free_throws"],
			self.splits_stats[type][subtype]["opp_free_throw_attempts"],
			self.splits_stats[type][subtype]["opp_offensive_rebounds"],
			self.splits_stats[type][subtype]["opp_total_rebounds"],
			self.splits_stats[type][subtype]["opp_assists"],
			self.splits_stats[type][subtype]["opp_steals"],
			self.splits_stats[type][subtype]["opp_blocks"],
			self.splits_stats[type][subtype]["opp_turnovers"],
			self.splits_stats[type][subtype]["opp_personal_fouls"],
			self.splits_stats[type][subtype]["opp_points"]
		)
		
		try:
			cursor.execute(query)
		finally:
			cursor.close()
	
	def updateTeamSplitInDatabase(self, conn, season, type, subtype):
		cursor = conn.cursor()
		query = ("""
			update team_splits set
				games = %d,
				wins = %d,
				losses = %d,
				field_goals = %d,
				field_goal_attempts = %d,
				three_point_field_goals = %d,
				three_point_field_goal_attempts = %d,
				free_throws = %d,
				free_throw_attempts = %d,
				offensive_rebounds = %d,
				total_rebounds = %d,
				assists = %d,
				steals = %d,
				blocks = %d,
				turnovers = %d,
				personal_fouls = %d,
				points = %d,
				opp_field_goals = %d,
				opp_field_goal_attempts = %d,
				opp_three_point_field_goals = %d,
				opp_three_point_field_goal_attempts = %d,
				opp_free_throws = %d,
				opp_free_throw_attempts = %d,
				opp_offensive_rebounds = %d,
				opp_total_rebounds = %d,
				opp_assists = %d,
				opp_steals = %d,
				opp_blocks = %d,
				opp_turnovers = %d,
				opp_personal_fouls = %d,
				opp_points = %d
			where team = '%s' and season = %d and type = '%s' and subtype = '%s'
			""") % (
			self.splits_stats[type][subtype]["games"],
			self.splits_stats[type][subtype]["wins"],
			self.splits_stats[type][subtype]["losses"],
			self.splits_stats[type][subtype]["field_goals"],
			self.splits_stats[type][subtype]["field_goal_attempts"],
			self.splits_stats[type][subtype]["three_point_field_goals"],
			self.splits_stats[type][subtype]["three_point_field_goal_attempts"],
			self.splits_stats[type][subtype]["free_throws"],
			self.splits_stats[type][subtype]["free_throw_attempts"],
			self.splits_stats[type][subtype]["offensive_rebounds"],
			self.splits_stats[type][subtype]["total_rebounds"],
			self.splits_stats[type][subtype]["assists"],
			self.splits_stats[type][subtype]["steals"],
			self.splits_stats[type][subtype]["blocks"],
			self.splits_stats[type][subtype]["turnovers"],
			self.splits_stats[type][subtype]["personal_fouls"],
			self.splits_stats[type][subtype]["points"],
			self.splits_stats[type][subtype]["opp_field_goals"],
			self.splits_stats[type][subtype]["opp_field_goal_attempts"],
			self.splits_stats[type][subtype]["opp_three_point_field_goals"],
			self.splits_stats[type][subtype]["opp_three_point_field_goal_attempts"],
			self.splits_stats[type][subtype]["opp_free_throws"],
			self.splits_stats[type][subtype]["opp_free_throw_attempts"],
			self.splits_stats[type][subtype]["opp_offensive_rebounds"],
			self.splits_stats[type][subtype]["opp_total_rebounds"],
			self.splits_stats[type][subtype]["opp_assists"],
			self.splits_stats[type][subtype]["opp_steals"],
			self.splits_stats[type][subtype]["opp_blocks"],
			self.splits_stats[type][subtype]["opp_turnovers"],
			self.splits_stats[type][subtype]["opp_personal_fouls"],
			self.splits_stats[type][subtype]["opp_points"],
			self.name,
			season,
			type,
			subtype
		)
		
		try:
			cursor.execute(query)
		finally:
			cursor.close()

class Player:
	def __init__(self):
		self.name = ""
		self.code = ""
		self.positions = []
		self.height = 0
		self.weight = 0
		self.url = ""
		
		self.season_totals = {}
		self.season_advanced = {}
		self.game_basic = {}
		self.game_advanced = {}
		self.splits = {}
	
	def playerExists(self, conn):
		cursor = conn.cursor()
		query = ("select id from players where id = %(id)s")
		data = { 'id': self.code }
		cursor.execute(query, data)
		
		for (id) in cursor:
			return True
		
		return False
	
	def writePlayerInfoToDatabase(self, conn):
		cursor = conn.cursor()
		query = "insert into players (id, name, position, height, weight, url) values ('%s', '%s', '%s', %d, %d, '%s')" % (self.code, self.name, self.positions[0], self.height, self.weight, self.url)
		cursor.execute(query)
		conn.commit()
		cursor.close()
		
	def seasonTotalsExist(self, conn, playerId, season):
		cursor = conn.cursor()
		query = ("select id from season_totals where player_id = '%s' and season = %d") % (playerId, season)
		cursor.execute(query)
		
		for (id) in cursor:
			return True
		
		return False
	
	def writeSeasonTotalsToDatabase(self, conn, playerId, season):
		cursor = conn.cursor()
		query = """
				insert into season_totals (
					player_id,
					season,
					age,
					team,
					league,
					position,
					games,
					games_started,
					minutes_played,
					field_goals,
					field_goal_attempts,
					field_goal_pct,
					three_point_field_goals,
					three_point_field_goal_attempts,
					three_point_field_goal_pct,
					two_point_field_goals,
					two_point_field_goal_attempts,
					two_point_field_goal_pct,
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
					points
				) 
				values (
					'%s',%d,%d,'%s','%s','%s',%d,%d,%d,%d,
					%d,%f,%d,%d,%f,%d,%d,%f,%d,%d,
					%f,%d,%d,%d,%d,%d,%d,%d,%d,%d
				)
		""" % (
		playerId,
		season,
		self.season_totals[season]["age"],
		self.season_totals[season]["team"],
		self.season_totals[season]["league"],
		self.season_totals[season]["position"],
		self.season_totals[season]["games"],
		self.season_totals[season]["games_started"],
		self.season_totals[season]["minutes_played"],
		self.season_totals[season]["field_goals"],
		self.season_totals[season]["field_goal_attempts"],
		self.season_totals[season]["field_goal_pct"],
		self.season_totals[season]["three_point_field_goals"],
		self.season_totals[season]["three_point_field_goal_attempts"],
		self.season_totals[season]["three_point_field_goal_pct"],
		self.season_totals[season]["two_point_field_goals"],
		self.season_totals[season]["two_point_field_goal_attempts"],
		self.season_totals[season]["two_point_field_goal_pct"],
		self.season_totals[season]["free_throws"],
		self.season_totals[season]["free_throw_attempts"],
		self.season_totals[season]["free_throw_pct"],
		self.season_totals[season]["offensive_rebounds"],
		self.season_totals[season]["defensive_rebounds"],
		self.season_totals[season]["total_rebounds"],
		self.season_totals[season]["assists"],
		self.season_totals[season]["steals"],
		self.season_totals[season]["blocks"],
		self.season_totals[season]["turnovers"],
		self.season_totals[season]["personal_fouls"],
		self.season_totals[season]["points"],
		)
		
		cursor.execute(query)
		cursor.close()
	
	def updateSeasonTotalsInDatabase(self, conn, playerId, season):
		cursor = conn.cursor()
		query = """
				update season_totals set
					age = %d,
					team = '%s',
					league = '%s',
					position = '%s',
					games = %d,
					games_started = %d,
					minutes_played = %d,
					field_goals = %d,
					field_goal_attempts = %d,
					field_goal_pct = %f,
					three_point_field_goals = %d,
					three_point_field_goal_attempts = %d,
					three_point_field_goal_pct = %f,
					two_point_field_goals = %d,
					two_point_field_goal_attempts = %d,
					two_point_field_goal_pct = %f,
					free_throws = %d,
					free_throw_attempts = %d,
					free_throw_pct = %f,
					offensive_rebounds = %d,
					defensive_rebounds = %d,
					total_rebounds = %d,
					assists = %d,
					steals = %d,
					blocks = %d,
					turnovers = %d,
					personal_fouls = %d,
					points = %d
				where player_id = '%s' and season = %d
		""" % (
		self.season_totals[season]["age"],
		self.season_totals[season]["team"],
		self.season_totals[season]["league"],
		self.season_totals[season]["position"],
		self.season_totals[season]["games"],
		self.season_totals[season]["games_started"],
		self.season_totals[season]["minutes_played"],
		self.season_totals[season]["field_goals"],
		self.season_totals[season]["field_goal_attempts"],
		self.season_totals[season]["field_goal_pct"],
		self.season_totals[season]["three_point_field_goals"],
		self.season_totals[season]["three_point_field_goal_attempts"],
		self.season_totals[season]["three_point_field_goal_pct"],
		self.season_totals[season]["two_point_field_goals"],
		self.season_totals[season]["two_point_field_goal_attempts"],
		self.season_totals[season]["two_point_field_goal_pct"],
		self.season_totals[season]["free_throws"],
		self.season_totals[season]["free_throw_attempts"],
		self.season_totals[season]["free_throw_pct"],
		self.season_totals[season]["offensive_rebounds"],
		self.season_totals[season]["defensive_rebounds"],
		self.season_totals[season]["total_rebounds"],
		self.season_totals[season]["assists"],
		self.season_totals[season]["steals"],
		self.season_totals[season]["blocks"],
		self.season_totals[season]["turnovers"],
		self.season_totals[season]["personal_fouls"],
		self.season_totals[season]["points"],
		playerId,
		season
		)
		
		cursor.execute(query)
		cursor.close()
	
	def seasonAdvancedExist(self, conn, playerId, season):
		cursor = conn.cursor()
		query = ("select id from season_advanced where player_id = '%s' and season = %d") % (playerId, season)
		cursor.execute(query)
		
		for (id) in cursor:
			return True
		
		return False
	
	def writeSeasonAdvancedStatsToDatabase(self, conn, playerId, season):
		cursor = conn.cursor()
		query = """
				insert into season_advanced (
					player_id,
					season,
					age,
					team,
					league,
					position,
					games,
					minutes_played,
					player_efficiency_rating,
					true_shooting_pct,
					effective_field_goal_pct,
					free_throw_attempt_rate,
					three_point_field_goal_attempt_rate,
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
					offensive_win_shares,
					defensive_win_shares,
					win_shares,
					win_shares_per_48_minutes
				) 
				values (
					'%s',%d,%d,'%s','%s','%s',%d,%d,%f,%f,
					%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%d,
					%f,%f,%f,%f,%f
				)
		""" % (
		playerId,
		season,
		self.season_advanced[season]["age"],
		self.season_advanced[season]["team"],
		self.season_advanced[season]["league"],
		self.season_advanced[season]["position"],
		self.season_advanced[season]["games"],
		self.season_advanced[season]["minutes_played"],
		self.season_advanced[season]["player_efficiency_rating"],
		self.season_advanced[season]["true_shooting_pct"],
		self.season_advanced[season]["effective_field_goal_pct"],
		self.season_advanced[season]["free_throw_attempt_rate"],
		self.season_advanced[season]["three_point_field_goal_attempt_rate"],
		self.season_advanced[season]["offensive_rebound_pct"],
		self.season_advanced[season]["defensive_rebound_pct"],
		self.season_advanced[season]["total_rebound_pct"],
		self.season_advanced[season]["assist_pct"],
		self.season_advanced[season]["steal_pct"],
		self.season_advanced[season]["block_pct"],
		self.season_advanced[season]["turnover_pct"],
		self.season_advanced[season]["usage_pct"],
		self.season_advanced[season]["offensive_rating"],
		self.season_advanced[season]["defensive_rating"],
		self.season_advanced[season]["offensive_win_shares"],
		self.season_advanced[season]["defensive_win_shares"],
		self.season_advanced[season]["win_shares"],
		self.season_advanced[season]["win_shares_per_48_minutes"]
		)
		
		cursor.execute(query)
		cursor.close()
	
	def updateSeasonAdvancedStatsInDatabase(self, conn, playerId, season):
		cursor = conn.cursor()
		query = """
				update season_advanced set
					age = %d,
					team = '%s',
					league = '%s',
					position = '%s',
					games = %d,
					minutes_played = %d,
					player_efficiency_rating = %f,
					true_shooting_pct = %f,
					effective_field_goal_pct = %f,
					free_throw_attempt_rate = %f,
					three_point_field_goal_attempt_rate = %f,
					offensive_rebound_pct = %f,
					defensive_rebound_pct = %f,
					total_rebound_pct = %f,
					assist_pct = %f,
					steal_pct = %f,
					block_pct = %f,
					turnover_pct = %f,
					usage_pct = %f,
					offensive_rating = %d,
					defensive_rating = %d,
					offensive_win_shares = %f,
					defensive_win_shares = %f,
					win_shares = %f,
					win_shares_per_48_minutes = %f
				where player_id = '%s' and season = %d
		""" % (
		self.season_advanced[season]["age"],
		self.season_advanced[season]["team"],
		self.season_advanced[season]["league"],
		self.season_advanced[season]["position"],
		self.season_advanced[season]["games"],
		self.season_advanced[season]["minutes_played"],
		self.season_advanced[season]["player_efficiency_rating"],
		self.season_advanced[season]["true_shooting_pct"],
		self.season_advanced[season]["effective_field_goal_pct"],
		self.season_advanced[season]["free_throw_attempt_rate"],
		self.season_advanced[season]["three_point_field_goal_attempt_rate"],
		self.season_advanced[season]["offensive_rebound_pct"],
		self.season_advanced[season]["defensive_rebound_pct"],
		self.season_advanced[season]["total_rebound_pct"],
		self.season_advanced[season]["assist_pct"],
		self.season_advanced[season]["steal_pct"],
		self.season_advanced[season]["block_pct"],
		self.season_advanced[season]["turnover_pct"],
		self.season_advanced[season]["usage_pct"],
		self.season_advanced[season]["offensive_rating"],
		self.season_advanced[season]["defensive_rating"],
		self.season_advanced[season]["offensive_win_shares"],
		self.season_advanced[season]["defensive_win_shares"],
		self.season_advanced[season]["win_shares"],
		self.season_advanced[season]["win_shares_per_48_minutes"],
		playerId,
		season
		)
		
		cursor.execute(query)
		cursor.close()
	
	################################################################
	# Checks to see if basic game log stats exist for a particular
	# player/season/game combination.
	################################################################
	def basicGameLogStatsExist(self, conn, playerId, season, game_number):
		cursor = conn.cursor()
		query = ("select id from game_totals_basic where player_id = '%s' and season = %d and game_number = %d") % (playerId, season, game_number)
		cursor.execute(query)
		
		for (id) in cursor:
			return True
		
		return False
	
	#######################################################################
	# Writes data for a single game for a player into the database in the 
	# game_totals_basic table.
	#######################################################################
	def writeBasicGameLogStatsToDatabase(self, conn, playerId, season, game_number):
		cursor = conn.cursor()
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
			playerId,
			season,
			game_number,
			self.game_basic[game_number]["date"],
			self.game_basic[game_number]["age"],
			self.game_basic[game_number]["team"],
			self.game_basic[game_number]["home"],
			self.game_basic[game_number]["opponent"],
			self.game_basic[game_number]["result"],
			self.game_basic[game_number]["games_started"],
			self.game_basic[game_number]["minutes_played"],
			self.game_basic[game_number]["field_goals"],
			self.game_basic[game_number]["field_goal_attempts"],
			self.game_basic[game_number]["field_goal_pct"],
			self.game_basic[game_number]["three_point_field_goals"],
			self.game_basic[game_number]["three_point_field_goal_attempts"],
			self.game_basic[game_number]["three_point_field_goal_pct"],
			self.game_basic[game_number]["free_throws"],
			self.game_basic[game_number]["free_throw_attempts"],
			self.game_basic[game_number]["free_throw_pct"],
			self.game_basic[game_number]["offensive_rebounds"],
			self.game_basic[game_number]["defensive_rebounds"],
			self.game_basic[game_number]["total_rebounds"],
			self.game_basic[game_number]["assists"],
			self.game_basic[game_number]["steals"],
			self.game_basic[game_number]["blocks"],
			self.game_basic[game_number]["turnovers"],
			self.game_basic[game_number]["personal_fouls"],
			self.game_basic[game_number]["points"],
			self.game_basic[game_number]["game_score"],
			self.game_basic[game_number]["plus_minus"]
		)
		
		cursor.execute(query)
		cursor.close()
	
	###################################################################
	# Checks to see if advanced game log stats exist for a particular
	# player/season/game combination.
	###################################################################
	def advancedGameLogStatsExist(self, conn, playerId, season, game_number):
		cursor = conn.cursor()
		query = ("select id from game_totals_advanced where player_id = '%s' and season = %d and game_number = %d") % (playerId, season, game_number)
		cursor.execute(query)
		
		for (id) in cursor:
			return True
		
		return False
	
	#######################################################################
	# Writes data for a single game for a player into the database in the 
	# game_totals_basic table.
	#######################################################################
	def writeAdvancedGameLogStatsToDatabase(self, conn, playerId, season, game_number):
		cursor = conn.cursor()
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
			playerId,
			game_number,
			season,
			self.game_advanced[game_number]["date"],
			self.game_advanced[game_number]["age"],
			self.game_advanced[game_number]["team"],
			self.game_advanced[game_number]["home"],
			self.game_advanced[game_number]["opponent"],
			self.game_advanced[game_number]["result"],
			self.game_advanced[game_number]["games_started"],
			self.game_advanced[game_number]["minutes_played"],
			self.game_advanced[game_number]["true_shooting_pct"],
			self.game_advanced[game_number]["effective_field_goal_pct"],
			self.game_advanced[game_number]["offensive_rebound_pct"],
			self.game_advanced[game_number]["defensive_rebound_pct"],
			self.game_advanced[game_number]["total_rebound_pct"],
			self.game_advanced[game_number]["assist_pct"],
			self.game_advanced[game_number]["steal_pct"],
			self.game_advanced[game_number]["block_pct"],
			self.game_advanced[game_number]["turnover_pct"],
			self.game_advanced[game_number]["usage_pct"],
			self.game_advanced[game_number]["offensive_rating"],
			self.game_advanced[game_number]["defensive_rating"],
			self.game_advanced[game_number]["game_score"]
		)
		
		cursor.execute(query)
		cursor.close()
	
	##################################################################################
	# Checks to see if splits exist for a particular player/season/game combination.
	##################################################################################
	def splitsExist(self, conn, playerId, season, splitType, splitSubType):
		cursor = conn.cursor()
		query = "select * from splits where player_id = '%s' and season = %d and type = '%s' and subtype = '%s'" % (playerId, season, splitType, splitSubType)
		cursor.execute(query)
		
		for (id) in cursor:
			cursor.close()
			return True
		
		cursor.close()
		return False
	
	def writeSplitToDatabase(self, conn, playerId, season, splitType, splitSubType):
		cursor = conn.cursor()
		query = ""
		
		if self.splits[splitType][splitSubType]["plus_minus"] != None:
			query = """
				insert into splits (
					player_id,
					season,
					type,
					subtype,
					games,
					games_started,
					minutes_played,
					field_goals,
					field_goal_attempts,
					three_point_field_goals,
					three_point_field_goal_attempts,
					free_throws,
					free_throw_attempts,
					offensive_rebounds,
					defensive_rebounds,
					total_rebounds,
					assists,
					steals,
					blocks,
					turnovers,
					personal_fouls,
					points,
					field_goal_pct,
					three_point_field_goal_pct,
					free_throw_pct,
					true_shooting_pct,
					usage_pct,
					offensive_rating,
					defensive_rating,
					plus_minus,
					minutes_played_per_game,
					points_per_game,
					total_rebounds_per_game,
					assists_per_game
				) values (
					'%s',%d,'%s','%s',%d,%d,%d,%d,%d,%d,%d,
					%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%f,
					%f,%f,%f,%f,%d,%d,%f,%f,%f,%f,%f
				)
			""" % (
				playerId,
				season,
				splitType,
				splitSubType,
				self.splits[splitType][splitSubType]["games"],
				self.splits[splitType][splitSubType]["games_started"],
				self.splits[splitType][splitSubType]["minutes_played"],
				self.splits[splitType][splitSubType]["field_goals"],
				self.splits[splitType][splitSubType]["field_goal_attempts"],
				self.splits[splitType][splitSubType]["three_point_field_goals"],
				self.splits[splitType][splitSubType]["three_point_field_goal_attempts"],
				self.splits[splitType][splitSubType]["free_throws"],
				self.splits[splitType][splitSubType]["free_throw_attempts"],
				self.splits[splitType][splitSubType]["offensive_rebounds"],
				self.splits[splitType][splitSubType]["defensive_rebounds"],
				self.splits[splitType][splitSubType]["total_rebounds"],
				self.splits[splitType][splitSubType]["assists"],
				self.splits[splitType][splitSubType]["steals"],
				self.splits[splitType][splitSubType]["blocks"],
				self.splits[splitType][splitSubType]["turnovers"],
				self.splits[splitType][splitSubType]["personal_fouls"],
				self.splits[splitType][splitSubType]["points"],
				self.splits[splitType][splitSubType]["field_goal_pct"],
				self.splits[splitType][splitSubType]["three_point_field_goal_pct"],
				self.splits[splitType][splitSubType]["free_throw_pct"],
				self.splits[splitType][splitSubType]["true_shooting_pct"],
				self.splits[splitType][splitSubType]["usage_pct"],
				self.splits[splitType][splitSubType]["offensive_rating"],
				self.splits[splitType][splitSubType]["defensive_rating"],
				self.splits[splitType][splitSubType]["plus_minus"],
				self.splits[splitType][splitSubType]["minutes_played_per_game"],
				self.splits[splitType][splitSubType]["points_per_game"],
				self.splits[splitType][splitSubType]["total_rebounds_per_game"],
				self.splits[splitType][splitSubType]["assists_per_game"]
			)
		else:
			query = """
				insert into splits (
					player_id,
					season,
					type,
					subtype,
					games,
					games_started,
					minutes_played,
					field_goals,
					field_goal_attempts,
					three_point_field_goals,
					three_point_field_goal_attempts,
					free_throws,
					free_throw_attempts,
					offensive_rebounds,
					defensive_rebounds,
					total_rebounds,
					assists,
					steals,
					blocks,
					turnovers,
					personal_fouls,
					points,
					field_goal_pct,
					three_point_field_goal_pct,
					free_throw_pct,
					true_shooting_pct,
					usage_pct,
					offensive_rating,
					defensive_rating,
					minutes_played_per_game,
					points_per_game,
					total_rebounds_per_game,
					assists_per_game
				) values (
					'%s',%d,'%s','%s',%d,%d,%d,%d,%d,%d,%d,
					%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%f,
					%f,%f,%f,%f,%d,%d,%f,%f,%f,%f
				)
			""" % (
				playerId,
				season,
				splitType,
				splitSubType,
				self.splits[splitType][splitSubType]["games"],
				self.splits[splitType][splitSubType]["games_started"],
				self.splits[splitType][splitSubType]["minutes_played"],
				self.splits[splitType][splitSubType]["field_goals"],
				self.splits[splitType][splitSubType]["field_goal_attempts"],
				self.splits[splitType][splitSubType]["three_point_field_goals"],
				self.splits[splitType][splitSubType]["three_point_field_goal_attempts"],
				self.splits[splitType][splitSubType]["free_throws"],
				self.splits[splitType][splitSubType]["free_throw_attempts"],
				self.splits[splitType][splitSubType]["offensive_rebounds"],
				self.splits[splitType][splitSubType]["defensive_rebounds"],
				self.splits[splitType][splitSubType]["total_rebounds"],
				self.splits[splitType][splitSubType]["assists"],
				self.splits[splitType][splitSubType]["steals"],
				self.splits[splitType][splitSubType]["blocks"],
				self.splits[splitType][splitSubType]["turnovers"],
				self.splits[splitType][splitSubType]["personal_fouls"],
				self.splits[splitType][splitSubType]["points"],
				self.splits[splitType][splitSubType]["field_goal_pct"],
				self.splits[splitType][splitSubType]["three_point_field_goal_pct"],
				self.splits[splitType][splitSubType]["free_throw_pct"],
				self.splits[splitType][splitSubType]["true_shooting_pct"],
				self.splits[splitType][splitSubType]["usage_pct"],
				self.splits[splitType][splitSubType]["offensive_rating"],
				self.splits[splitType][splitSubType]["defensive_rating"],
				self.splits[splitType][splitSubType]["minutes_played_per_game"],
				self.splits[splitType][splitSubType]["points_per_game"],
				self.splits[splitType][splitSubType]["total_rebounds_per_game"],
				self.splits[splitType][splitSubType]["assists_per_game"]
			)
		
		cursor.execute(query)
		cursor.close()
	
	def updateSplitInDatabase(self, conn, playerId, season, splitType, splitSubType):
		cursor = conn.cursor()
		query = ""
		
		if self.splits[splitType][splitSubType]["plus_minus"] != None:
			query = """
				update splits set
					games = %d,
					games_started = %d,
					minutes_played = %d,
					field_goals = %d,
					field_goal_attempts = %d,
					three_point_field_goals = %d,
					three_point_field_goal_attempts = %d,
					free_throws = %d,
					free_throw_attempts = %d,
					offensive_rebounds = %d,
					defensive_rebounds = %d,
					total_rebounds = %d,
					assists = %d,
					steals = %d,
					blocks = %d,
					turnovers = %d,
					personal_fouls = %d,
					points = %d,
					field_goal_pct = %f,
					three_point_field_goal_pct = %f,
					free_throw_pct = %f,
					true_shooting_pct = %f,
					usage_pct = %f,
					offensive_rating = %d,
					defensive_rating = %d,
					plus_minus = %f,
					minutes_played_per_game = %f,
					points_per_game = %f,
					total_rebounds_per_game = %f,
					assists_per_game = %f
				where player_id = '%s' and season = %d and type = '%s' and subtype = '%s'
			""" % (
				self.splits[splitType][splitSubType]["games"],
				self.splits[splitType][splitSubType]["games_started"],
				self.splits[splitType][splitSubType]["minutes_played"],
				self.splits[splitType][splitSubType]["field_goals"],
				self.splits[splitType][splitSubType]["field_goal_attempts"],
				self.splits[splitType][splitSubType]["three_point_field_goals"],
				self.splits[splitType][splitSubType]["three_point_field_goal_attempts"],
				self.splits[splitType][splitSubType]["free_throws"],
				self.splits[splitType][splitSubType]["free_throw_attempts"],
				self.splits[splitType][splitSubType]["offensive_rebounds"],
				self.splits[splitType][splitSubType]["defensive_rebounds"],
				self.splits[splitType][splitSubType]["total_rebounds"],
				self.splits[splitType][splitSubType]["assists"],
				self.splits[splitType][splitSubType]["steals"],
				self.splits[splitType][splitSubType]["blocks"],
				self.splits[splitType][splitSubType]["turnovers"],
				self.splits[splitType][splitSubType]["personal_fouls"],
				self.splits[splitType][splitSubType]["points"],
				self.splits[splitType][splitSubType]["field_goal_pct"],
				self.splits[splitType][splitSubType]["three_point_field_goal_pct"],
				self.splits[splitType][splitSubType]["free_throw_pct"],
				self.splits[splitType][splitSubType]["true_shooting_pct"],
				self.splits[splitType][splitSubType]["usage_pct"],
				self.splits[splitType][splitSubType]["offensive_rating"],
				self.splits[splitType][splitSubType]["defensive_rating"],
				self.splits[splitType][splitSubType]["plus_minus"],
				self.splits[splitType][splitSubType]["minutes_played_per_game"],
				self.splits[splitType][splitSubType]["points_per_game"],
				self.splits[splitType][splitSubType]["total_rebounds_per_game"],
				self.splits[splitType][splitSubType]["assists_per_game"],
				playerId,
				season,
				splitType,
				splitSubType
			)
		else:
			query = """
				update splits set
					games = %d,
					games_started = %d,
					minutes_played = %d,
					field_goals = %d,
					field_goal_attempts = %d,
					three_point_field_goals = %d,
					three_point_field_goal_attempts = %d,
					free_throws = %d,
					free_throw_attempts = %d,
					offensive_rebounds = %d,
					defensive_rebounds = %d,
					total_rebounds = %d,
					assists = %d,
					steals = %d,
					blocks = %d,
					turnovers = %d,
					personal_fouls = %d,
					points = %d,
					field_goal_pct = %f,
					three_point_field_goal_pct = %f,
					free_throw_pct = %f,
					true_shooting_pct = %f,
					usage_pct = %f,
					offensive_rating = %d,
					defensive_rating = %d,
					minutes_played_per_game = %f,
					points_per_game = %f,
					total_rebounds_per_game = %f,
					assists_per_game = %f
				where player_id = '%s' and season = %d and type = '%s' and subtype = '%s'
			""" % (
				self.splits[splitType][splitSubType]["games"],
				self.splits[splitType][splitSubType]["games_started"],
				self.splits[splitType][splitSubType]["minutes_played"],
				self.splits[splitType][splitSubType]["field_goals"],
				self.splits[splitType][splitSubType]["field_goal_attempts"],
				self.splits[splitType][splitSubType]["three_point_field_goals"],
				self.splits[splitType][splitSubType]["three_point_field_goal_attempts"],
				self.splits[splitType][splitSubType]["free_throws"],
				self.splits[splitType][splitSubType]["free_throw_attempts"],
				self.splits[splitType][splitSubType]["offensive_rebounds"],
				self.splits[splitType][splitSubType]["defensive_rebounds"],
				self.splits[splitType][splitSubType]["total_rebounds"],
				self.splits[splitType][splitSubType]["assists"],
				self.splits[splitType][splitSubType]["steals"],
				self.splits[splitType][splitSubType]["blocks"],
				self.splits[splitType][splitSubType]["turnovers"],
				self.splits[splitType][splitSubType]["personal_fouls"],
				self.splits[splitType][splitSubType]["points"],
				self.splits[splitType][splitSubType]["field_goal_pct"],
				self.splits[splitType][splitSubType]["three_point_field_goal_pct"],
				self.splits[splitType][splitSubType]["free_throw_pct"],
				self.splits[splitType][splitSubType]["true_shooting_pct"],
				self.splits[splitType][splitSubType]["usage_pct"],
				self.splits[splitType][splitSubType]["offensive_rating"],
				self.splits[splitType][splitSubType]["defensive_rating"],
				self.splits[splitType][splitSubType]["minutes_played_per_game"],
				self.splits[splitType][splitSubType]["points_per_game"],
				self.splits[splitType][splitSubType]["total_rebounds_per_game"],
				self.splits[splitType][splitSubType]["assists_per_game"],
				playerId,
				season,
				splitType,
				splitSubType
			)
		
		cursor.execute(query)
		cursor.close()

class SeasonTotals:
	def __init__(self):
		self.id = -1
		self.playerId = ""
		self.season = -1
		self.age = -1
		self.team = ""
		self.league = ""
		self.position = ""
		self.games = -1
		self.gamesStarted = -1
		self.minutesPlayed = -1
		self.fieldGoals = -1
		self.fieldGoalAttempts = -1
		self.fieldGoalPct = -1
		self.threePointFieldGoals = -1
		self.threePointFieldGoalAttempts = -1
		self.threePointFieldGoalPct = -1
		self.twoPointFieldGoals = -1
		self.twoPointFieldGoalAttempts = -1
		self.twoPointFieldGoalPct = -1
		self.freeThrows = -1
		self.freeThrowAttempts = -1
		self.freeThrowPct = -1
		self.offensiveRebounds = -1
		self.defensiveRebounds = -1
		self.totalRebounds = -1
		self.assists = -1
		self.steals = -1
		self.blocks = -1
		self.turnovers = -1
		self.personalFouls = -1
		self.points = -1
	
	def seasonTotalsExist(self, conn):
		cursor = conn.cursor()
		query = ("select id from season_totals where player_id = %(id)s and season = %(season)d")
		data = { 'id': self.playerId, 'season': self.season }
		cursor.execute(query, data)
		
		for (id) in cursor:
			return True
		
		return False
	
	def writeSeasonTotalsToDatabase(self, conn):
		cursor = conn.cursor()
		query = """
				insert into season_totals (
					player_id,
					season,
					age,
					team,
					league,
					position,
					games,
					games_started,
					minutes_played,
					field_goals,
					field_goal_attempts,
					field_goal_pct,
					three_point_field_goals,
					three_point_field_goal_attempts,
					three_point_field_goal_pct,
					two_point_field_goals,
					two_point_field_goal_attempts,
					two_point_field_goal_pct,
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
					points
				) 
				values (
					%s,%d,%d,%s,%s,%s,%d,%d,%d,%d,
					%d,%f,%d,%d,%f,%d,%d,%f,%d,%d,
					%f,%d,%d,%d,%d,%d,%d,%d,%d,%d
				)
		""" % (
		self.playerId,
		self.season,
		self.age,
		self.team,
		self.league,
		self.position,
		self.games,
		self.gamesStarted,
		self.minutesPlayed,
		self.fieldGoals,
		self.fieldGoalAttempts,
		self.fieldGoalPct,
		self.threePointFieldGoals,
		self.threePointFieldGoalAttempts,
		self.threePointFieldGoalPct,
		self.twoPointFieldGoals,
		self.twoPointFieldGoalAttempts,
		self.twoPointFieldGoalPct,
		self.freeThrows,
		self.freeThrowAttempts,
		self.freeThrowPct,
		self.offensiveRebounds,
		self.defensiveRebounds,
		self.totalRebounds,
		self.assists,
		self.steals,
		self.blocks,
		self.turnovers,
		self.personalFouls,
		self.points,
		)
		
		cursor.execute(query)
		cursor.close()

class Schedule:
	def __init__(self, date=date.today(), season=date.today().year, home="", visitor=""):
		self.date = date
		self.season = season
		self.home = home
		self.visitor = visitor
	
	def game_exists(self, conn):
		cursor = conn.cursor()
		
		try:
			query = """
				select id from schedules where date = '%s' and home = '%s' and visitor = '%s'
			""" % (self.date, self.home, self.visitor)

			cursor.execute(query)
			for result in cursor:
				return True
			
			return False
		except:
			print "Something went wrong in Schedule.game_exists"
		finally:
			cursor.close()
	
	def insert_game(self, conn):
		cursor = conn.cursor()
		
		try:
			query = """
				insert into schedules (date, season, visitor, home) values ('%s', %d,'%s','%s')
			""" % (self.date, self.season, self.visitor, self.home)
			
			cursor.execute(query)
		except:
			print "Something went wrong in Schedule.insert_game"
		finally:
			cursor.close()

################################################################
# Parses the main list of players to get basic information and
# the link to their individual page.
################################################################
class BasketballReferencePlayerListParser(HTMLParser):
	rowCount = 0
	tdCount = 0
	current = ""
	isActive = False
	all_players = False
	player = Player()
	
	players = []
	
	def handle_starttag(self, tag, attrs):
		#print "Found start tag", tag
		if tag == "tr":
			self.player = Player()
			self.rowCount = self.rowCount + 1
			self.tdCount = 0
			self.isActive = self.all_players	# Initially set to False if we're only interested in active players.
		elif tag == "td":
			self.tdCount = self.tdCount + 1
		elif tag == "strong":
			self.isActive = True
		elif tag == "a" and self.isActive and self.tdCount == 1:
			for attr in attrs:
				self.player.url = attr[1]
				pieces = self.player.url.split("/")
				self.player.code = pieces[len(pieces)-1].split(".")[0]
		
		self.current = tag
		
	def handle_endtag(self,tag):
		if tag == "tr" and self.isActive and self.player.name != "":
			self.players.append(self.player)
			print "Player",self.player.name,"(",self.player.url,")/",self.player.code,"/",self.player.positions,"/",self.player.height,"inches/",self.player.weight,"lbs"
	
	def handle_data(self, data):
		if data.strip() == "" or data.strip() == "*":
			return
		
		if self.current == "a" and self.isActive and self.tdCount == 1:
			self.player.name = data.replace("'","")
		# Fourth column - position.
		elif self.current == "td" and self.isActive and self.tdCount == 4:
			pieces = data.split("-")
			self.player.positions = pieces
		# Fifth column - height
		elif self.current == "td" and self.isActive and self.tdCount == 5:
			pieces = data.split("-")
			self.player.height = int(pieces[0])*12 + int(pieces[1])
		# Sixth column - weight
		elif self.current == "td" and self.isActive and self.tdCount == 6:
			self.player.weight = int(data)

####################################################################
# Parses the main page for an individual player.  This page mostly 
# consists of career stats, broken down by season.
####################################################################
class BasketballReferencePlayerMainParser(HTMLParser):
	current = ""
	currentSeason = -1
	table_type = ""
	tdCount = 0
	found_footer = False
	totals_stats = {}
	advanced_stats = {}
	
	def handle_starttag(self, tag, attrs):
		if tag == "tr" and len(attrs) > 1 and attrs[1][1].find("totals") == 0:
			self.table_type = "totals"
			self.tdCount = 0
		elif tag == "tr" and len(attrs) > 1 and attrs[1][1].find("advanced.") == 0:
			self.table_type = "advanced"
			self.tdCount = 0
		elif tag == "td":
			self.tdCount = self.tdCount + 1
		elif tag == "tfoot":
			found_footer = True
		
		self.current = tag
		
	def handle_endtag(self, tag):
		if tag == "table":
			self.table_type = ""
	
	def handle_data(self, data):
		if data.strip() == "" or self.found_footer:
			return
		
		if self.table_type == "totals":
			# Season column (<a> tag for linkable season, <td> for non-linkable)
			if (self.current == "a" or self.current == "td") and self.tdCount == 1:
				self.currentSeason = int(data.split("-")[0])
				self.totals_stats[self.currentSeason] = {
					"age": -1,
					"team": "",
					"position": "",
					"games_started": 0,
					"minutes_played": 0.0,
					"field_goal_pct": 0.0,
					"three_point_field_goals": 0,
					"three_point_field_goal_attempts": 0,
					"three_point_field_goal_pct": 0.0,
					"two_point_field_goal_pct": 0.0,
					"free_throw_pct": 0.0,
					"offensive_rebounds": 0,
					"defensive_rebounds": 0,
					"total_rebounds": 0,
					"assists": 0,
					"steals": 0,
					"blocks": 0,
					"turnovers": 0
				}
			# Age column
			elif self.current == "td" and self.tdCount == 2:
				self.totals_stats[self.currentSeason]["age"] = int(data)
			# Team column
			elif self.current == "a" and self.tdCount == 3:
				self.totals_stats[self.currentSeason]["team"] = data
			# League column
			elif self.current == "a" and self.tdCount == 4:
				self.totals_stats[self.currentSeason]["league"] = data
			# Position column
			elif self.current == "td" and self.tdCount == 5:
				self.totals_stats[self.currentSeason]["position"] = data
			# Games column
			elif self.current == "td" and self.tdCount == 6:
				self.totals_stats[self.currentSeason]["games"] = int(data)
			# Games started
			elif self.current == "td" and self.tdCount == 7:
				self.totals_stats[self.currentSeason]["games_started"] = int(data)
			# Minutes played
			elif self.current == "td" and self.tdCount == 8:
				self.totals_stats[self.currentSeason]["minutes_played"] = int(data)
			# Field goals
			elif self.current == "td" and self.tdCount == 9:
				self.totals_stats[self.currentSeason]["field_goals"] = int(data)
			# Field goal attempts
			elif self.current == "td" and self.tdCount == 10:
				self.totals_stats[self.currentSeason]["field_goal_attempts"] = int(data)
			# Field goal pct
			elif self.current == "td" and self.tdCount == 11:
				self.totals_stats[self.currentSeason]["field_goal_pct"] = float(data)
			# 3 pointers
			elif self.current == "td" and self.tdCount == 12:
				self.totals_stats[self.currentSeason]["three_point_field_goals"] = int(data)
			# 3 point attempts
			elif self.current == "td" and self.tdCount == 13:
				self.totals_stats[self.currentSeason]["three_point_field_goal_attempts"] = int(data)
			# 3 pointer pct
			elif self.current == "td" and self.tdCount == 14:
				self.totals_stats[self.currentSeason]["three_point_field_goal_pct"] = float(data)
			# 2 pointers
			elif self.current == "td" and self.tdCount == 15:
				self.totals_stats[self.currentSeason]["two_point_field_goals"] = int(data)
			# 2 point attempts
			elif self.current == "td" and self.tdCount == 16:
				self.totals_stats[self.currentSeason]["two_point_field_goal_attempts"] = int(data)
			# 2 pointer pct
			elif self.current == "td" and self.tdCount == 17:
				self.totals_stats[self.currentSeason]["two_point_field_goal_pct"] = float(data)
			# Free throws
			elif self.current == "td" and self.tdCount == 18:
				self.totals_stats[self.currentSeason]["free_throws"] = int(data)
			# Free throws attempted
			elif self.current == "td" and self.tdCount == 19:
				self.totals_stats[self.currentSeason]["free_throw_attempts"] = int(data)
			# Free throw pct
			elif self.current == "td" and self.tdCount == 20:
				self.totals_stats[self.currentSeason]["free_throw_pct"] = float(data)
			# Offensive rebounds
			elif self.current == "td" and self.tdCount == 21:
				self.totals_stats[self.currentSeason]["offensive_rebounds"] = int(data)
			# Defensive rebounds
			elif self.current == "td" and self.tdCount == 22:
				self.totals_stats[self.currentSeason]["defensive_rebounds"] = int(data)
			# Total rebounds
			elif self.current == "td" and self.tdCount == 23:
				self.totals_stats[self.currentSeason]["total_rebounds"] = int(data)
			# Assists
			elif self.current == "td" and self.tdCount == 24:
				self.totals_stats[self.currentSeason]["assists"] = int(data)
			# Steals
			elif self.current == "td" and self.tdCount == 25:
				self.totals_stats[self.currentSeason]["steals"] = int(data)
			# Blocks
			elif self.current == "td" and self.tdCount == 26:
				self.totals_stats[self.currentSeason]["blocks"] = int(data)
			# Turnovers
			elif self.current == "td" and self.tdCount == 27:
				self.totals_stats[self.currentSeason]["turnovers"] = int(data)
			# Personal fouls
			elif self.current == "td" and self.tdCount == 28:
				self.totals_stats[self.currentSeason]["personal_fouls"] = int(data)
			# Points
			elif self.current == "td" and self.tdCount == 29:
				self.totals_stats[self.currentSeason]["points"] = int(data)
			
			
		elif self.table_type == "advanced":
			# Season column
			if (self.current == "a" or self.current == "td") and self.tdCount == 1:
				self.currentSeason = int(data.split("-")[0])
				self.advanced_stats[self.currentSeason] = {
					"age": -1,
					"team": "",
					"position": "",
					"minutes_played": 0,
					"player_efficiency_rating": 0.0,
					"true_shooting_pct": 0.0,
					"effective_field_goal_pct": 0.0,
					"free_throw_attempt_rate": 0.0,
					"three_point_field_goal_attempt_rate": 0.0,
					"offensive_rebound_pct": 0.0,
					"defensive_rebound_pct": 0.0,
					"total_rebound_pct": 0.0,
					"assist_pct": 0.0,
					"steal_pct": 0.0,
					"block_pct": 0.0,
					"turnover_pct": 0.0,
					"usage_pct": 0.0,
					"offensive_rating": 0,
					"defensive_rating": 0,
					"offensive_win_shares": 0.0,
					"defensive_win_shares": 0.0,
					"win_shares": 0.0,
					"win_shares_per_48_minutes": 0.0
				}
			# Age column
			elif self.current == "td" and self.tdCount == 2:
				self.advanced_stats[self.currentSeason]["age"] = int(data)
			# Team column
			elif self.current == "a" and self.tdCount == 3:
				self.advanced_stats[self.currentSeason]["team"] = data
			# League column
			elif self.current == "a" and self.tdCount == 4:
				self.advanced_stats[self.currentSeason]["league"] = data
			# Position
			elif self.current == "td" and self.tdCount == 5:
				self.advanced_stats[self.currentSeason]["position"] = data
			# Games
			elif self.current == "td" and self.tdCount == 6:
				self.advanced_stats[self.currentSeason]["games"] = int(data)
			# Minutes played
			elif self.current == "td" and self.tdCount == 7:
				self.advanced_stats[self.currentSeason]["minutes_played"] = int(data)
			# Player efficiency rating
			elif self.current == "td" and self.tdCount == 8:
				self.advanced_stats[self.currentSeason]["player_efficiency_rating"] = float(data)
			# True shooting percentage
			elif self.current == "td" and self.tdCount == 9:
				self.advanced_stats[self.currentSeason]["true_shooting_pct"] = float(data)
			# Effective field goal pct
			elif self.current == "td" and self.tdCount == 10:
				self.advanced_stats[self.currentSeason]["effective_field_goal_pct"] = float(data)
			# Free throw attempt rate
			elif self.current == "td" and self.tdCount == 11:
				self.advanced_stats[self.currentSeason]["free_throw_attempt_rate"] = float(data)
			# Three point attempt rate
			elif self.current == "td" and self.tdCount == 12:
				self.advanced_stats[self.currentSeason]["three_point_field_goal_attempt_rate"] = float(data)
			# Offensive rebound pct
			elif self.current == "td" and self.tdCount == 13:
				self.advanced_stats[self.currentSeason]["offensive_rebound_pct"] = float(data)
			# Defensive rebound pct
			elif self.current == "td" and self.tdCount == 14:
				self.advanced_stats[self.currentSeason]["defensive_rebound_pct"] = float(data)
			# Total rebound pct
			elif self.current == "td" and self.tdCount == 15:
				self.advanced_stats[self.currentSeason]["total_rebound_pct"] = float(data)
			# Assist pct
			elif self.current == "td" and self.tdCount == 16:
				self.advanced_stats[self.currentSeason]["assist_pct"] = float(data)
			# Steal pct
			elif self.current == "td" and self.tdCount == 17:
				self.advanced_stats[self.currentSeason]["steal_pct"] = float(data)
			# Block pct
			elif self.current == "td" and self.tdCount == 18:
				self.advanced_stats[self.currentSeason]["block_pct"] = float(data)
			# Turnover pct
			elif self.current == "td" and self.tdCount == 19:
				self.advanced_stats[self.currentSeason]["turnover_pct"] = float(data)
			# Usage pct
			elif self.current == "td" and self.tdCount == 20:
				self.advanced_stats[self.currentSeason]["usage_pct"] = float(data)
			# Offensive rating
			elif self.current == "td" and self.tdCount == 21:
				self.advanced_stats[self.currentSeason]["offensive_rating"] = int(data)
			# Defensive rating
			elif self.current == "td" and self.tdCount == 22:
				self.advanced_stats[self.currentSeason]["defensive_rating"] = int(data)
			# Offensive win shares
			elif self.current == "td" and self.tdCount == 23:
				self.advanced_stats[self.currentSeason]["offensive_win_shares"] = float(data)
			# Defensive win shares
			elif self.current == "td" and self.tdCount == 24:
				self.advanced_stats[self.currentSeason]["defensive_win_shares"] = float(data)
			# Win shares
			elif self.current == "td" and self.tdCount == 25:
				self.advanced_stats[self.currentSeason]["win_shares"] = float(data)
			# Win shares per 48 minutes
			elif self.current == "td" and self.tdCount == 26:
				self.advanced_stats[self.currentSeason]["win_shares_per_48_minutes"] = float(data)
	
###############################
# Parses a player's game log.
###############################
class BasketballReferenceGameLogParser(HTMLParser):
	current = ""
	tableType = ""
	tdCount = 0
	game_number = -1
	basic_game_stats = {}
	advanced_game_stats = {}

	def handle_starttag(self, tag, attrs):
		
		if tag == "tr" and len(attrs) > 1 and attrs[1][1].find("pgl_basic") > -1:
			self.tdCount = 0
			self.game_number = 0
			self.tableType = "pgl_basic"
		elif tag == "td" and (self.tableType == "pgl_basic" or self.tableType == "pgl_advanced"):
			self.tdCount = self.tdCount + 1
		if tag == "tr" and len(attrs) > 1 and attrs[1][1].find("pgl_advanced") > -1:
			self.tdCount = 0
			self.game_number = 0
			self.tableType = "pgl_advanced"
		
		self.current = tag
	
	def handle_endtag(self, tag):
		# We've reached the end of the pgl_basic table.  Tell the app that we're done with it.
		if tag == "table" and self.tableType == "pgl_basic":
			self.tableType = ""
		elif tag == "tr" and self.tableType == "pgl_basic":
			#print self.basic_game_stats[self.game_number]
			pass
		elif tag == "tr" and self.tableType == "pgl_advanced":
			#print self.advanced_game_stats[self.game_number]
			pass
		elif tag == "td" and self.tdCount == 6:
			# Properly set the home/away value.  On the site, this is denoted
			# as an "@" sign, which means if we don't collect anything then it's
			# a home game.  Therefore, we have a catch block to set the value to True.
			try:
				if self.tableType == "pgl_basic":
					self.basic_game_stats[self.game_number]["home"]
				elif self.tableType == "pgl_advanced":
					self.advanced_game_stats[self.game_number]["home"]
			except:
				if self.tableType == "pgl_basic":
					self.basic_game_stats[self.game_number]["home"] = True
				elif self.tableType == "pgl_advanced":
					self.advanced_game_stats[self.game_number]["home"] = True
					
	
	def handle_data(self, data):
		if data.strip() == "":
			return
	
		if self.tableType == "pgl_basic":
			# Game number
			if self.current == "span" and self.tdCount == 2:
				self.game_number = int(data)
				self.basic_game_stats[self.game_number] = {
					"age": -1,
					"team": "",
					"result": "",
					"games_started": 0,
					"minutes_played": 0,
					"field_goals": 0,
					"field_goal_attempts": 0,
					"field_goal_pct": 0.0,
					"three_point_field_goals": 0,
					"three_point_field_goal_attempts": 0,
					"three_point_field_goal_pct": 0.0,
					"free_throws": 0,
					"free_throw_attempts": 0,
					"free_throw_pct": 0.0,
					"offensive_rebounds": 0,
					"defensive_rebounds": 0,
					"total_rebounds": 0,
					"assists": 0,
					"steals": 0,
					"blocks": 0,
					"turnovers": 0,
					"personal_fouls": 0,
					"plus_minus": 0,
					"game_score": 0
				}
			# Date
			elif self.current == "a" and self.tdCount == 3:
				self.basic_game_stats[self.game_number]["date"] = data
			# Age
			elif self.current == "td" and self.tdCount == 4:
				pieces = data.split("-")
				self.basic_game_stats[self.game_number]["age"] = int(pieces[0])
			# Team
			elif self.current == "a" and self.tdCount == 5:
				self.basic_game_stats[self.game_number]["team"] = data
			# Home or Away
			elif self.current == "td" and self.tdCount == 6:
				self.basic_game_stats[self.game_number]["home"] = data != "@"
			# Opponent
			elif self.current == "a" and self.tdCount == 7:
				self.basic_game_stats[self.game_number]["opponent"] = data
			# Win or Loss
			elif self.current == "td" and self.tdCount == 8:
				self.basic_game_stats[self.game_number]["result"] = data
			# Games started
			elif self.current == "td" and self.tdCount == 9:
				self.basic_game_stats[self.game_number]["games_started"] = int(data)
			# Minutes played
			elif self.current == "td" and self.tdCount == 10:
				pieces = data.split(":")
				minutes = int(pieces[0])
				minutes = minutes + int(pieces[1])/60.0
				self.basic_game_stats[self.game_number]["minutes_played"] = minutes
			# Field goals
			elif self.current == "td" and self.tdCount == 11:
				self.basic_game_stats[self.game_number]["field_goals"] = int(data)
			# Field goal attempts
			elif self.current == "td" and self.tdCount == 12:
				self.basic_game_stats[self.game_number]["field_goal_attempts"] = int(data)
			# Field goal pct
			elif self.current == "td" and self.tdCount == 13:
				self.basic_game_stats[self.game_number]["field_goal_pct"] = float(data)
			# 3 pointers
			elif self.current == "td" and self.tdCount == 14:
				self.basic_game_stats[self.game_number]["three_point_field_goals"] = int(data)
			# 3 point attempts
			elif self.current == "td" and self.tdCount == 15:
				self.basic_game_stats[self.game_number]["three_point_field_goal_attempts"] = int(data)
			# 3 pointer pct
			elif self.current == "td" and self.tdCount == 16:
				self.basic_game_stats[self.game_number]["three_point_field_goal_pct"] = float(data)
			# Free throws
			elif self.current == "td" and self.tdCount == 17:
				self.basic_game_stats[self.game_number]["free_throws"] = int(data)
			# Free throws attempted
			elif self.current == "td" and self.tdCount == 18:
				self.basic_game_stats[self.game_number]["free_throw_attempts"] = int(data)
			# Free throw pct
			elif self.current == "td" and self.tdCount == 19:
				self.basic_game_stats[self.game_number]["free_throw_pct"] = float(data)
			# Offensive rebounds
			elif self.current == "td" and self.tdCount == 20:
				self.basic_game_stats[self.game_number]["offensive_rebounds"] = int(data)
			# Defensive rebounds
			elif self.current == "td" and self.tdCount == 21:
				self.basic_game_stats[self.game_number]["defensive_rebounds"] = int(data)
			# Total rebounds
			elif self.current == "td" and self.tdCount == 22:
				self.basic_game_stats[self.game_number]["total_rebounds"] = int(data)
			# Assists
			elif self.current == "td" and self.tdCount == 23:
				self.basic_game_stats[self.game_number]["assists"] = int(data)
			# Steals
			elif self.current == "td" and self.tdCount == 24:
				self.basic_game_stats[self.game_number]["steals"] = int(data)
			# Blocks
			elif self.current == "td" and self.tdCount == 25:
				self.basic_game_stats[self.game_number]["blocks"] = int(data)
			# Turnovers
			elif self.current == "td" and self.tdCount == 26:
				self.basic_game_stats[self.game_number]["turnovers"] = int(data)
			# Personal fouls
			elif self.current == "td" and self.tdCount == 27:
				self.basic_game_stats[self.game_number]["personal_fouls"] = int(data)
			# Points
			elif self.current == "td" and self.tdCount == 28:
				self.basic_game_stats[self.game_number]["points"] = int(data)
			# Game score (no clue what this is)
			elif self.current == "td" and self.tdCount == 29:
				self.basic_game_stats[self.game_number]["game_score"] = float(data)
			# Plus/minus
			elif self.current == "td" and self.tdCount == 30:
				self.basic_game_stats[self.game_number]["plus_minus"] = int(data)
		
		elif self.tableType == "pgl_advanced":
			# Game number
			if self.current == "td" and self.tdCount == 2:
				self.game_number = int(data)
				self.advanced_game_stats[self.game_number] = {
					"age": -1,
					"team": "",
					"result": "",
					"games_started": 0,
					"minutes_played": 0,
					"true_shooting_pct": 0.0,
					"effective_field_goal_pct": 0.0,
					"offensive_rebound_pct": 0.0,
					"defensive_rebound_pct": 0.0,
					"total_rebound_pct": 0.0,
					"assist_pct": 0.0,
					"steal_pct": 0.0,
					"block_pct": 0.0,
					"turnover_pct": 0.0,
					"usage_pct": 0.0,
					"offensive_rating": 0,
					"defensive_rating": 0,
					"game_score": 0
				}
			# Date
			elif self.current == "a" and self.tdCount == 3:
				self.advanced_game_stats[self.game_number]["date"] = data
			# Age
			elif self.current == "td" and self.tdCount == 4:
				pieces = data.split("-")
				self.advanced_game_stats[self.game_number]["age"] = int(pieces[0])
			# Team
			elif self.current == "a" and self.tdCount == 5:
				self.advanced_game_stats[self.game_number]["team"] = data
			# Home or Away
			elif self.current == "td" and self.tdCount == 6:
				self.advanced_game_stats[self.game_number]["home"] = data != "@"
			# Opponent
			elif self.current == "a" and self.tdCount == 7:
				self.advanced_game_stats[self.game_number]["opponent"] = data
			# Win or Loss
			elif self.current == "td" and self.tdCount == 8:
				self.advanced_game_stats[self.game_number]["result"] = data
			# Games started
			elif self.current == "td" and self.tdCount == 9:
				self.advanced_game_stats[self.game_number]["games_started"] = int(data)
			# Minutes played
			elif self.current == "td" and self.tdCount == 10:
				pieces = data.split(":")
				minutes = int(pieces[0])
				minutes = minutes + int(pieces[1])/60.0
				self.advanced_game_stats[self.game_number]["minutes_played"] = minutes
			# True shooting pct
			elif self.current == "td" and self.tdCount == 11:
				self.advanced_game_stats[self.game_number]["true_shooting_pct"] = float(data)
			# Effective field goal pct
			elif self.current == "td" and self.tdCount == 12:
				self.advanced_game_stats[self.game_number]["effective_field_goal_pct"] = float(data)
			# Offensive rebound pct
			elif self.current == "td" and self.tdCount == 13:
				self.advanced_game_stats[self.game_number]["offensive_rebound_pct"] = float(data)
			# Defensive rebound pct
			elif self.current == "td" and self.tdCount == 14:
				self.advanced_game_stats[self.game_number]["defensive_rebound_pct"] = float(data)
			# Total rebound pct
			elif self.current == "td" and self.tdCount == 15:
				self.advanced_game_stats[self.game_number]["total_rebound_pct"] = float(data)
			# Assist pct
			elif self.current == "td" and self.tdCount == 16:
				self.advanced_game_stats[self.game_number]["assist_pct"] = float(data)
			# Steal pct
			elif self.current == "td" and self.tdCount == 17:
				self.advanced_game_stats[self.game_number]["steal_pct"] = float(data)
			# Block pct
			elif self.current == "td" and self.tdCount == 18:
				self.advanced_game_stats[self.game_number]["block_pct"] = float(data)
			# Turnover pct
			elif self.current == "td" and self.tdCount == 19:
				self.advanced_game_stats[self.game_number]["turnover_pct"] = float(data)
			# Usage pct
			elif self.current == "td" and self.tdCount == 20:
				self.advanced_game_stats[self.game_number]["usage_pct"] = float(data)
			# Offensive rating
			elif self.current == "td" and self.tdCount == 21:
				self.advanced_game_stats[self.game_number]["offensive_rating"] = int(data)
			# Defensive rating
			elif self.current == "td" and self.tdCount == 22:
				self.advanced_game_stats[self.game_number]["defensive_rating"] = int(data)
			# Game score
			elif self.current == "td" and self.tdCount == 23:
				self.advanced_game_stats[self.game_number]["game_score"] = float(data)

###############################
# Parses a player's game log.
###############################
class BasketballReferenceTeamGameLogParser(HTMLParser):
	current = ""
	table_type = ""
	td_count = 0
	found_basic_table = False
	game_number = 0
	game_stats = {}

	def handle_starttag(self, tag, attrs):
		if tag == "table" and len(attrs) > 1 and attrs[1][1] == "stats" and not self.found_basic_table:
			self.table_type = "stats"
			self.found_basic_table = True
		if tag == "tr" and self.table_type == "stats":
			self.td_count = 0
			self.game_number = 0
		elif tag == "td":
			self.td_count += 1
		
		self.current = tag
	
	def handle_endtag(self, tag):
		# We've reached the end of the stats table.  Tell the app that we're done with it.
		if tag == "table" and self.table_type == "stats":
			self.table_type = ""
		# End of the row.  Print out the stats we've acquired.
		elif tag == "tr" and self.table_type == "stats" and self.game_number > 0:
			#print self.game_stats[self.game_number]
			pass
		elif tag == "td" and self.td_count == 6:
			# Properly set the home/away value.  On the site, this is denoted
			# as an "@" sign, which means if we don't collect anything then it's
			# a home game.  Therefore, we have a catch block to set the value to True.
			try:
				self.game_stats[self.game_number]["home"]
			except:
				self.game_stats[self.game_number]["home"] = True
		elif tag == "body":
			self.found_basic_table = False
	
	def handle_data(self, data):
		if data.strip() == "":
			return

		# Game number
		if self.current == "span" and self.td_count == 2:
			self.game_number = int(data)
			self.game_stats[self.game_number] = {
				"minutes_played": 240,
				"result": "",
				"opp_free_throws": 0,
				"opp_free_throw_attempts": 0
			}
		# Date
		elif self.current == "a" and self.td_count == 3:
			self.game_stats[self.game_number]["date"] = data
		# Home or Away
		elif self.current == "td" and self.td_count == 4:
			self.game_stats[self.game_number]["home"] = data != "@"
		# Opponent
		elif self.current == "a" and self.td_count == 5:
			self.game_stats[self.game_number]["opponent"] = data
		# Game Result (Win or loss)
		elif self.current == "td" and self.td_count == 6:
			self.game_stats[self.game_number]["result"] = data
		# Team points
		elif self.current == "td" and self.td_count == 7:
			self.game_stats[self.game_number]["points"] = int(data)
		# Opponent points
		elif self.current == "td" and self.td_count == 8:
			self.game_stats[self.game_number]["opp_points"] = int(data)
		# Field goals
		elif self.current == "td" and self.td_count == 9:
			self.game_stats[self.game_number]["field_goals"] = int(data)
		# Field goal attempts
		elif self.current == "td" and self.td_count == 10:
			self.game_stats[self.game_number]["field_goal_attempts"] = int(data)
		# Field goal pct
		elif self.current == "td" and self.td_count == 11:
			self.game_stats[self.game_number]["field_goal_pct"] = float(data)
		# 3 pointers
		elif self.current == "td" and self.td_count == 12:
			self.game_stats[self.game_number]["three_point_field_goals"] = int(data)
		# 3 point attempts
		elif self.current == "td" and self.td_count == 13:
			self.game_stats[self.game_number]["three_point_field_goal_attempts"] = int(data)
		# 3 point field goal pct
		elif self.current == "td" and self.td_count == 14:
			self.game_stats[self.game_number]["three_point_field_goal_pct"] = float(data)
		# Free throws
		elif self.current == "td" and self.td_count == 15:
			self.game_stats[self.game_number]["free_throws"] = int(data)
		# Free throws attempted
		elif self.current == "td" and self.td_count == 16:
			self.game_stats[self.game_number]["free_throw_attempts"] = int(data)
		# 3 point field goal pct
		elif self.current == "td" and self.td_count == 17:
			self.game_stats[self.game_number]["free_throw_pct"] = float(data)
		# Offensive rebounds
		elif self.current == "td" and self.td_count == 18:
			self.game_stats[self.game_number]["offensive_rebounds"] = int(data)
		# Total rebounds
		elif self.current == "td" and self.td_count == 19:
			self.game_stats[self.game_number]["total_rebounds"] = int(data)
		# Assists
		elif self.current == "td" and self.td_count == 20:
			self.game_stats[self.game_number]["assists"] = int(data)
		# Steals
		elif self.current == "td" and self.td_count == 21:
			self.game_stats[self.game_number]["steals"] = int(data)
		# Blocks
		elif self.current == "td" and self.td_count == 22:
			self.game_stats[self.game_number]["blocks"] = int(data)
		# Turnovers
		elif self.current == "td" and self.td_count == 23:
			self.game_stats[self.game_number]["turnovers"] = int(data)
		# Personal fouls
		elif self.current == "td" and self.td_count == 24:
			self.game_stats[self.game_number]["personal_fouls"] = int(data)

		## Skip the spacer TD

		# Opponent Field goals
		elif self.current == "td" and self.td_count == 26:
			self.game_stats[self.game_number]["opp_field_goals"] = int(data)
		# Opponent Field goal attempts
		elif self.current == "td" and self.td_count == 27:
			self.game_stats[self.game_number]["opp_field_goal_attempts"] = int(data)
		# Opponent field goal pct
		elif self.current == "td" and self.td_count == 28:
			self.game_stats[self.game_number]["opp_field_goal_pct"] = float(data)
		# Opponent 3 pointers
		elif self.current == "td" and self.td_count == 29:
			self.game_stats[self.game_number]["opp_three_point_field_goals"] = int(data)
		# Opponent 3 point attempts
		elif self.current == "td" and self.td_count == 30:
			self.game_stats[self.game_number]["opp_three_point_field_goal_attempts"] = int(data)
		# Opponent 3 point field goal pct
		elif self.current == "td" and self.td_count == 31:
			self.game_stats[self.game_number]["opp_three_point_field_goal_pct"] = float(data)
		# Opponent Free throws
		elif self.current == "td" and self.td_count == 32:
			self.game_stats[self.game_number]["opp_free_throws"] = int(data)
		# Opponent Free throws attempted
		elif self.current == "td" and self.td_count == 33:
			self.game_stats[self.game_number]["opp_free_throw_attempts"] = int(data)
		# Opponent free throw pct
		elif self.current == "td" and self.td_count == 34:
			self.game_stats[self.game_number]["opp_free_throw_pct"] = float(data)
		# Opponent Offensive rebounds
		elif self.current == "td" and self.td_count == 35:
			self.game_stats[self.game_number]["opp_offensive_rebounds"] = int(data)
		# Opponent Total rebounds
		elif self.current == "td" and self.td_count == 36:
			self.game_stats[self.game_number]["opp_total_rebounds"] = int(data)
		# Opponent Assists
		elif self.current == "td" and self.td_count == 37:
			self.game_stats[self.game_number]["opp_assists"] = int(data)
		# Opponent Steals
		elif self.current == "td" and self.td_count == 38:
			self.game_stats[self.game_number]["opp_steals"] = int(data)
		# Opponent Blocks
		elif self.current == "td" and self.td_count == 39:
			self.game_stats[self.game_number]["opp_blocks"] = int(data)
		# Opponent Turnovers
		elif self.current == "td" and self.td_count == 40:
			self.game_stats[self.game_number]["opp_turnovers"] = int(data)
		# Opponent Personal fouls
		elif self.current == "td" and self.td_count == 41:
			self.game_stats[self.game_number]["opp_personal_fouls"] = int(data)
		
		
		
###################################################				
# Parse the splits page for an individual player.
###################################################
class BasketballReferenceSplitsParser(HTMLParser):
	found_table = False
	tbodyCount = 0
	tdCount = 0
	current = ""
	type = ""
	subtype = ""
	usingPlusMinus = False
	
	######################################################################################
	# Map of main types of splits (i.e. Conference, Division, Opponent).  The value of
	# each key will be a map the subtypes for each type (i.e. Opponent will have each of
	# the teams that a player played against.).  Inside of those maps will be a map
	# containing the stats for that split.
	######################################################################################
	stats = {}

	def handle_starttag(self, tag, attrs):
		if tag == "table" and len(attrs) > 1 and attrs[1][1] == "stats":
			self.found_table = True
			self.type = ""
			self.subtype = ""
		elif tag == "tbody":
			self.tbodyCount = self.tbodyCount + 1
		elif tag == "tr":
			self.tdCount = 0
		elif tag == "td":
			self.tdCount = self.tdCount + 1
		
		self.current = tag
	
	def handle_endtag(self, tag):
		if tag == "tr" and self.type != "" and self.subtype != "":
			#print self.type+"/"+self.subtype, self.stats[self.type][self.subtype],"\n"
			self.isDataRow = False
	
	def handle_data(self, data):
		if data.strip() == "" or not self.found_table:
			return
	
		#########################################################################################
		# Look at the first td of a row.
		# - If it is blank then we're likely looking at the second or subsequent row of a split.
		# - If it contains any text other than "Split" then it is the first row of a split.
		# - If it contains the text "Split" then it is a header row and can be ignored.
		#########################################################################################
		if self.current == "td" and self.tdCount == 1:
			self.type = data
			self.stats[data] = {}
				
		# Set up the sub-map for each split type (i.e. Win/Loss for the Result map).
		elif (self.current == "td" or self.current == "a") and self.tdCount == 2:
			#print "Found a new split type - ", data
		
			# This is the row for totals, not sure what to do with it yet.
			if data == "Total":
				self.type = data
				self.stats[self.type] = {}
			
			self.subtype = data
			self.stats[self.type][self.subtype] = {
				"games_started": 0,
				"minutes_played": 0,
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
				"defensive_rebounds": 0,
				"field_goal_pct": 0.0,
				"three_point_field_goal_pct": 0.0,
				"free_throw_pct": 0.0,
				"true_shooting_pct": 0.0,
				"usage_pct": 0.0,
				"offensive_rating": 0.0,
				"defensive_rating": 0.0,
				"minutes_played_per_game": 0.0,
				"points_per_game": 0.0,
				"total_rebounds_per_game": 0.0,
				"assists_per_game": 0.0,
				"plus_minus": None
			}
		# Games
		elif self.current == "td" and self.tdCount == 3:
			#print "Data is",data
			self.stats[self.type][self.subtype]["games"] = int(data)
		# Games started
		elif self.current == "td" and self.tdCount == 4:
			self.stats[self.type][self.subtype]["games_started"] = int(data)
		# Minutes played
		elif self.current == "td" and self.tdCount == 5:
			self.stats[self.type][self.subtype]["minutes_played"] = int(data)
		# Field goals
		elif self.current == "td" and self.tdCount == 6:
			self.stats[self.type][self.subtype]["field_goals"] = int(data)
		# Field goal attempts
		elif self.current == "td" and self.tdCount == 7:
			self.stats[self.type][self.subtype]["field_goal_attempts"] = int(data)
		# 3-pointers
		elif self.current == "td" and self.tdCount == 8:
			self.stats[self.type][self.subtype]["three_point_field_goals"] = int(data)
		# 3-pointer attempts
		elif self.current == "td" and self.tdCount == 9:
			self.stats[self.type][self.subtype]["three_point_field_goal_attempts"] = int(data)
		# Free throws
		elif self.current == "td" and self.tdCount == 10:
			self.stats[self.type][self.subtype]["free_throws"] = int(data)
		# Free throw attempts
		elif self.current == "td" and self.tdCount == 11:
			self.stats[self.type][self.subtype]["free_throw_attempts"] = int(data)
		# Offensive rebounds
		elif self.current == "td" and self.tdCount == 12:
			self.stats[self.type][self.subtype]["offensive_rebounds"] = int(data)
		# Total rebounds
		elif self.current == "td" and self.tdCount == 13:
			self.stats[self.type][self.subtype]["total_rebounds"] = int(data)
		# Assists
		elif self.current == "td" and self.tdCount == 14:
			self.stats[self.type][self.subtype]["assists"] = int(data)
		# Steals
		elif self.current == "td" and self.tdCount == 15:
			self.stats[self.type][self.subtype]["steals"] = int(data)
		# Blocks
		elif self.current == "td" and self.tdCount == 16:
			self.stats[self.type][self.subtype]["blocks"] = int(data)
		# Turnovers
		elif self.current == "td" and self.tdCount == 17:
			self.stats[self.type][self.subtype]["turnovers"] = int(data)
		# Personal fouls
		elif self.current == "td" and self.tdCount == 18:
			self.stats[self.type][self.subtype]["personal_fouls"] = int(data)
		# Points (total)
		elif self.current == "td" and self.tdCount == 19:
			self.stats[self.type][self.subtype]["points"] = int(data)
		# Field goal pct
		elif self.current == "td" and self.tdCount == 20:
			self.stats[self.type][self.subtype]["field_goal_pct"] = float(data)
		# 3-Point pct
		elif self.current == "td" and self.tdCount == 21:
			self.stats[self.type][self.subtype]["three_point_field_goal_pct"] = float(data)
		# Free throw pct
		elif self.current == "td" and self.tdCount == 22:
			self.stats[self.type][self.subtype]["free_throw_pct"] = float(data)
		# True shooting pct
		elif self.current == "td" and self.tdCount == 23:
			self.stats[self.type][self.subtype]["true_shooting_pct"] = float(data)
		# Usage pct
		elif self.current == "td" and self.tdCount == 24:
			self.stats[self.type][self.subtype]["usage_pct"] = float(data)
		# Offensive rating
		elif self.current == "td" and self.tdCount == 25:
			self.stats[self.type][self.subtype]["offensive_rating"] = int(data)
		# Defensive rating
		elif self.current == "td" and self.tdCount == 26:
			self.stats[self.type][self.subtype]["defensive_rating"] = int(data)
		###########################################################################################
		# Plus/minus (or minutes played per game)
		# We don't get the plus/minus stat until the player gets 200 possessions (or something
		# like that), so we need to detect when the column isn't there and adjust for all future
		# columns.
		###########################################################################################
		elif self.current == "td" and self.tdCount == 27:
			self.usingPlusMinus = data.find("+") > -1 or data.find("-") > -1
			if self.usingPlusMinus:
				self.stats[self.type][self.subtype]["plus_minus"] = float(data)
			else:
				self.stats[self.type][self.subtype]["minutes_played_per_game"] = float(data)
		# Minutes played per game (or points per game)
		elif self.current == "td" and self.tdCount == 28:
			if self.usingPlusMinus:
				self.stats[self.type][self.subtype]["minutes_played_per_game"] = float(data)
			else:
				self.stats[self.type][self.subtype]["points_per_game"] = float(data)
		# Points per game (or total rebounds per game)
		elif self.current == "td" and self.tdCount == 29:
			if self.usingPlusMinus:
				self.stats[self.type][self.subtype]["points_per_game"] = float(data)
			else:
				self.stats[self.type][self.subtype]["total_rebounds_per_game"] = float(data)
		# Total rebounds per game (or assists per game)
		elif self.current == "td" and self.tdCount == 30:
			if self.usingPlusMinus:
				self.stats[self.type][self.subtype]["total_rebounds_per_game"] = float(data)
			else:
				self.stats[self.type][self.subtype]["assists_per_game"] = float(data)
		# Assists per game (or nothing)
		elif self.current == "td" and self.tdCount == 31:
			if self.usingPlusMinus:
				self.stats[self.type][self.subtype]["assists_per_game"] = float(data)


#####################################
# Parse the splits page for a team.
#####################################
class BasketballReferenceTeamSplitsParser(HTMLParser):
	found_table = False
	tbodyCount = 0
	tdCount = 0
	current = ""
	type = ""
	subtype = ""
	usingPlusMinus = False
	
	######################################################################################
	# Map of main types of splits (i.e. Conference, Division, Opponent).  The value of
	# each key will be a map the subtypes for each type (i.e. Opponent will have each of
	# the teams that a player played against.).  Inside of those maps will be a map
	# containing the stats for that split.
	######################################################################################
	stats = {}

	def handle_starttag(self, tag, attrs):
		if tag == "table" and len(attrs) > 1 and attrs[1][1] == "stats":
			self.found_table = True
			self.type = ""
			self.subtype = ""
		elif tag == "tbody":
			self.tbodyCount = self.tbodyCount + 1
		elif tag == "tr":
			self.tdCount = 0
		elif tag == "td":
			self.tdCount = self.tdCount + 1
		
		self.current = tag
	
	def handle_endtag(self, tag):
		if tag == "tr" and self.type != "" and self.subtype != "":
			#print self.type+"/"+self.subtype, self.stats[self.type][self.subtype],"\n"
			self.isDataRow = False
	
	def handle_data(self, data):
		if data.strip() == "" or not self.found_table:
			return
	
		#########################################################################################
		# Look at the first td of a row.
		# - If it is blank then we're likely looking at the second or subsequent row of a split.
		# - If it contains any text other than "Split" then it is the first row of a split.
		# - If it contains the text "Split" then it is a header row and can be ignored.
		#########################################################################################
		if self.current == "td" and self.tdCount == 1:
			self.type = data
			self.stats[data] = {}
				
		# Set up the sub-map for each split type (i.e. Win/Loss for the Result map).
		elif (self.current == "td" or self.current == "a") and self.tdCount == 2:
			#print "Found a new split type - ", data
		
			# This is the row for totals, not sure what to do with it yet.
			if data == "Total":
				self.type = data
				self.stats[self.type] = {}
			
			self.subtype = data
			self.stats[self.type][self.subtype] = {

			}
		# Games
		elif self.current == "td" and self.tdCount == 3:
			#print "Data is",data
			self.stats[self.type][self.subtype]["games"] = int(data)
		# Wins
		elif self.current == "td" and self.tdCount == 4:
			self.stats[self.type][self.subtype]["wins"] = int(data)
		# Losses
		elif self.current == "td" and self.tdCount == 5:
			self.stats[self.type][self.subtype]["losses"] = int(data)
		# Field goals
		elif self.current == "td" and self.tdCount == 6:
			self.stats[self.type][self.subtype]["field_goals"] = float(data)
		# Field goal attempts
		elif self.current == "td" and self.tdCount == 7:
			self.stats[self.type][self.subtype]["field_goal_attempts"] = float(data)
		# 3-pointers
		elif self.current == "td" and self.tdCount == 8:
			self.stats[self.type][self.subtype]["three_point_field_goals"] = float(data)
		# 3-pointer attempts
		elif self.current == "td" and self.tdCount == 9:
			self.stats[self.type][self.subtype]["three_point_field_goal_attempts"] = float(data)
		# Free throws
		elif self.current == "td" and self.tdCount == 10:
			self.stats[self.type][self.subtype]["free_throws"] = float(data)
		# Free throw attempts
		elif self.current == "td" and self.tdCount == 11:
			self.stats[self.type][self.subtype]["free_throw_attempts"] = float(data)
		# Offensive rebounds
		elif self.current == "td" and self.tdCount == 12:
			self.stats[self.type][self.subtype]["offensive_rebounds"] = float(data)
		# Total rebounds
		elif self.current == "td" and self.tdCount == 13:
			self.stats[self.type][self.subtype]["total_rebounds"] = float(data)
		# Assists
		elif self.current == "td" and self.tdCount == 14:
			self.stats[self.type][self.subtype]["assists"] = float(data)
		# Steals
		elif self.current == "td" and self.tdCount == 15:
			self.stats[self.type][self.subtype]["steals"] = float(data)
		# Blocks
		elif self.current == "td" and self.tdCount == 16:
			self.stats[self.type][self.subtype]["blocks"] = float(data)
		# Turnovers
		elif self.current == "td" and self.tdCount == 17:
			self.stats[self.type][self.subtype]["turnovers"] = float(data)
		# Personal fouls
		elif self.current == "td" and self.tdCount == 18:
			self.stats[self.type][self.subtype]["personal_fouls"] = float(data)
		# Points (total)
		elif self.current == "td" and self.tdCount == 19:
			self.stats[self.type][self.subtype]["points"] = float(data)
		# Opponent Field goals
		elif self.current == "td" and self.tdCount == 20:
			self.stats[self.type][self.subtype]["opp_field_goals"] = float(data)
		# Opponent Field goal attempts
		elif self.current == "td" and self.tdCount == 21:
			self.stats[self.type][self.subtype]["opp_field_goal_attempts"] = float(data)
		# Opponent 3-pointers
		elif self.current == "td" and self.tdCount == 22:
			self.stats[self.type][self.subtype]["opp_three_point_field_goals"] = float(data)
		# Opponent 3-pointer attempts
		elif self.current == "td" and self.tdCount == 23:
			self.stats[self.type][self.subtype]["opp_three_point_field_goal_attempts"] = float(data)
		# Opponent Free throws
		elif self.current == "td" and self.tdCount == 24:
			self.stats[self.type][self.subtype]["opp_free_throws"] = float(data)
		# Opponent Free throw attempts
		elif self.current == "td" and self.tdCount == 25:
			self.stats[self.type][self.subtype]["opp_free_throw_attempts"] = float(data)
		# Opponent Offensive rebounds
		elif self.current == "td" and self.tdCount == 26:
			self.stats[self.type][self.subtype]["opp_offensive_rebounds"] = float(data)
		# OpponentTotal rebounds
		elif self.current == "td" and self.tdCount == 27:
			self.stats[self.type][self.subtype]["opp_total_rebounds"] = float(data)
		# Opponent Assists
		elif self.current == "td" and self.tdCount == 28:
			self.stats[self.type][self.subtype]["opp_assists"] = float(data)
		# Opponent Steals
		elif self.current == "td" and self.tdCount == 29:
			self.stats[self.type][self.subtype]["opp_steals"] = float(data)
		# Opponent Blocks
		elif self.current == "td" and self.tdCount == 30:
			self.stats[self.type][self.subtype]["opp_blocks"] = float(data)
		# Opponent Turnovers
		elif self.current == "td" and self.tdCount == 31:
			self.stats[self.type][self.subtype]["opp_turnovers"] = float(data)
		# Opponent Personal fouls
		elif self.current == "td" and self.tdCount == 32:
			self.stats[self.type][self.subtype]["opp_personal_fouls"] = float(data)
		# Opponent Points (total)
		elif self.current == "td" and self.tdCount == 33:
			self.stats[self.type][self.subtype]["opp_points"] = float(data)


class BasketballReferenceScheduleParser(HTMLParser):
	found_table = False
	tbodyCount = 0
	tdCount = 0
	current = ""
	data = []
	instance = {}
	
	def handle_starttag(self, tag, attrs):
		if tag == "table" and len(attrs) > 1 and attrs[1][1] == "games":
			self.found_table = True
		elif tag == "tbody":
			self.tbodyCount = self.tbodyCount + 1
		elif tag == "tr":
			self.instance = {}
			self.tdCount = 0
		elif tag == "td":
			self.tdCount = self.tdCount + 1
		elif tag == "a" and self.tdCount == 1 and len(attrs) == 1:
			pieces = attrs[0][1].split("?")
			pieces = pieces[1].split("&")
			
			month = int(pieces[0].split("=")[1])
			day = int(pieces[1].split("=")[1])
			year = int(pieces[2].split("=")[1])
			
			if month >= 1 and month <= 8:
				self.instance["season"] = year-1
			else:
				self.instance["season"] = year
			
			self.instance["date"] = date(year, month, day)
		elif tag == "a" and self.tdCount == 3 and len(attrs) == 1:
			self.instance["visitor"] = attrs[0][1].split("/")[2]
		
		elif tag == "a" and self.tdCount == 5 and len(attrs) == 1:
			self.instance["home"] = attrs[0][1].split("/")[2]
		
		self.current = tag
	
	def handle_endtag(self, tag):
		if tag == "tr" and self.tbodyCount == 1:
			self.data.append(self.instance)
			

if __name__ == '__main__':
	logging.basicConfig(level=logging.INFO)

	processor = Processor()
	processor.process()