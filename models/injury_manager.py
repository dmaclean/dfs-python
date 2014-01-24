__author__ = 'ap'

import mysql.connector
from datetime import date, timedelta

from models.injury import Injury

class InjuryManager():
	def __init__(self, cnx=None):
		# Use dependency injection to determine where the database connection comes from.
		if not cnx:
			self.cnx = mysql.connector.connect(user='fantasy', password='fantasy', host='localhost', database='basketball_reference')
		else:
			self.cnx = cnx

	def exists(self, injury):
		"""
		Determines whether the provided injury already exists in the database.  The function
		returns true when the player_id matches, the injury date is on or after the injury date,
		and the return date is on or before the return date of a row in the database.
		"""
		cursor = self.cnx.cursor()

		query = """
			select id from injuries
			where player_id = '%s' and injury_date <= '%s' and return_date >= '%s' limit 1
		""" % (injury.player_id, injury.injury_date, injury.return_date)

		try:
			cursor.execute(query)

			for result in cursor:
				return True
		finally:
			cursor.close()

		return False

	def insert(self, injury):
		cursor = self.cnx.cursor()

		query = """
			insert into injuries (player_id, injury_date, return_date, details)
			values ('%s','%s','%s','%s')
		""" % (injury.player_id, injury.injury_date, injury.return_date, injury.details)

		try:
			cursor.execute(query)
		finally:
			cursor.close()

	def update(self, injury):
		cursor = self.cnx.cursor()

		query = """
			update injuries set player_id='%s', injury_date='%s', return_date='%s', details='%s'
			where id=%d
		""" % (injury.player_id, injury.injury_date, injury.return_date, injury.details, injury.id)

		try:
			cursor.execute(query)
		finally:
			cursor.close()

	def get(self, injury):
		cursor = self.cnx.cursor()

		injuries = []
		query = "select * from injuries where 1=1 "

		if injury.id:
			query += "and id = %d " % injury.id
		else:
			if injury.player_id:
				query += "and player_id = '%s' " % injury.player_id
			if injury.injury_date:
				query += "and injury_date = '%s' " % injury.injury_date
			if injury.return_date:
				query += "and return_date = '%s' " % injury.return_date
			if injury.details:
				query += "and details = '%s' " % injury.details

		try:
			cursor.execute(query)
			for result in cursor:
				i = Injury(id=result[0], player_id=result[1], injury_date=result[2], return_date=result[3], details=result[4])
				injuries.append(i)
		finally:
			cursor.close()

		return injuries

	def get_currently_injured_players(self, date=date.today()):
		"""
		Returns a map of the currently injured players, keyed by player_id.  A player is considered
		injured if they have an entry in the injuries table where the provided date is between the
		injury_date (inclusive) and the return_date (exclusive).
		"""
		cursor = self.cnx.cursor()

		query = "select * from injuries where injury_date <= '%s' and return_date > '%s'" % (date, date)
		injuries = {}
		try:
			cursor.execute(query)
			for result in cursor:
				injury = Injury(id=result[0], player_id=result[1], injury_date=result[2], return_date=result[3], details=result[4])
				injuries[injury.player_id] = injury
		finally:
			cursor.close()

		return injuries

	def calculate_injuries_from_gamelogs(self, season):
		"""
		Determine which players were injured on which past games based on their presence in the game log.
		"""
		one_day = timedelta(days=1)

		cursor = self.cnx.cursor()

		#######################################################
		# Determine which players participated in the season.
		#######################################################
		query = "select distinct player_id from game_totals_basic where season = %d order by player_id" % season
		try:
			cursor.execute(query)

			players = []
			for result in cursor:
				players.append(result[0])
		finally:
			cursor.close()

		###############################################################################################
		# for each player, determine which team(s) they're on and any games they seem to have missed.
		###############################################################################################
		for player in players:
			# Get gamelogs
			cursor = self.cnx.cursor()
			query = "select team, date from game_totals_basic where season = {0:d} and player_id = '{1:s}' order by date".format(season, player)

			games = []
			teams = []
			try:
				cursor.execute(query)

				last_team = None
				for result in cursor:
					if not last_team or last_team != result[0]:
						last_team = result[0]
					if last_team not in teams:
						teams.append(last_team)
					games.append((result[0], result[1]))
			finally:
				cursor.close()

			if len(games) == 0:
				print "{0:s} apparently didn't play any games in {1:d}.  Moving on...".format(player, season)
				continue

			injury_dates = []

			if len(teams) > 1:
				######################################################################
				# Looks like this player was traded at least once during the season.
				######################################################################
				print "Looks like this player got traded at some point..."
				cursor = self.cnx.cursor()

				try:
					start_date = None
					end_date = None
					current_team = None
					for game in games:
						# We're at the beginning
						if not current_team:
							current_team = game[0]
							start_date = game[1]
						# Player has switched teams
						elif current_team != game[0]:
							# Get game dates for previous team
							query = """select distinct date from team_game_totals
										where season = %d and team = '%s' and date between '%s' and '%s'
										order by date""" % (season, current_team, start_date, end_date)
							cursor.execute(query)

							# For each game played by the team, determine if there is a corresponding game in the player's games.
							# If not, then they were out for some reason (the reason itself doesn't matter).
							for result in cursor:
								d = result[0]

								played = False
								for g in games:
									if d == g[1]:
										played = True
										break
								if not played:
									print "Didn't play, adding {0:s} to injury list".format(d)
									injury_dates.append(d)

							# We're not sure exactly when the player was traded, so we need to count all games between the LAST
							# game of the previous team and the FIRST game of the new team for BOTH teams as injury dates.
							query = """select distinct date from team_game_totals
										where season = {0:d} and team in ('{1:s}','{2:s}') and date between '{3:s}' and '{4:s}'
										order by date""".format(season, current_team, game[0], end_date, game[1])
							cursor.execute(query)

							for result in cursor:
								d = result[0]
								if d == end_date or d == game[1]:
									continue

								injury_dates.append(d)

							# Record the new team and start date
							current_team = game[0]
							start_date = game[1]

						end_date = game[1]
				finally:
					cursor.close()


			else:
				###############################################################
				# Player wasn't traded.  Get the dates of their team's games.
				###############################################################
				cursor = self.cnx.cursor()
				query = "select distinct date from team_game_totals where season = {0:d} and team = '{1:s}'".format(
					season, games[0][0])

				try:
					cursor.execute(query)

					# For each game played by the team, determine if there is a corresponding game in the player's games.
					# If not, then they were out for some reason (the reason itself doesn't matter).
					for result in cursor:
						d = result[0]

						played = False
						for game in games:
							if d == game[1]:
								played = True
								break
						if not played:
							injury_dates.append(d)
				finally:
					cursor.close()

			###########################################################
			# Go through each injury date and add it to the database.
			###########################################################
			for d in injury_dates:
				# Looks like he didn't play.  Log it in the database.
				print "%s did not play on %s" % (player, d)
				date_pieces = str(d).split('-')
				injury_date = date(int(date_pieces[0]), int(date_pieces[1]), int(date_pieces[2]))
				return_date = injury_date + one_day
				injury = Injury(player_id=player, injury_date=injury_date, return_date=return_date,
									details="from calculate_injuries_from_gamelogs")
				if not self.exists(injury):
					self.insert(injury)
				else:
					print "\tWe've already accounted for this injury."