__author__ = 'ap'

import httplib
import logging
import time
import sys
import mysql.connector
from datetime import date, timedelta

from bs4 import BeautifulSoup
from nba.models.injury import Injury


class InjuryManager():
	def __init__(self, cnx=None):
		# Use dependency injection to determine where the database connection comes from.
		if not cnx:
			self.cnx = mysql.connector.connect(user='fantasy', password='fantasy', host='localhost', database='basketball_reference')
		else:
			self.cnx = cnx

		# Set up caching
		self.injury_cache = {}

		self.one_day = timedelta(days=1)

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
			injury.id = cursor.lastrowid
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

	def delete(self, injury):
		cursor = self.cnx.cursor()

		query = "delete from injuries where id = {}".format(injury.id)

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
		key = str(date)
		if key in self.injury_cache:
			return self.injury_cache[key]

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

		self.injury_cache[key] = injuries
		return self.injury_cache[key]

	def fix_injuries(self, season=None):
		"""
		Take a pass through each injury for each player and compare it to the GTB entries
		to determine if any need to be adjusted.
		"""
		changes = True
		while changes:
			cursor = self.cnx.cursor()

			changes = False
			injury_game_pairs = []
			try:
				injuries = self.get(Injury())
				for i in injuries:
					query = """select date from game_totals_basic b
								where season = {} and player_id = '{}'
								and date between '{}' and '{}'""".format(season, i.player_id, i.injury_date, i.return_date)
					cursor.execute(query)

					for result in cursor:
						injury_game_pairs.append([i, result[0]])

			finally:
				cursor.close()

			for p in injury_game_pairs:
				new_injury = self.fix_injury_entry(p[0], p[1])

				if new_injury:
					changes = True

		self.remove_duplicates()

	def remove_duplicates(self):
		"""
		Find and remove any duplicate injuries.  This can be defined as two injury entries
		where i1.player_id = i2.player_id and i1.injury_date = i2.injury_date and i1.return_date = i2.return_date
		"""
		cursor = self.cnx.cursor()

		query = """select i.id, i2.id from injuries i inner join injuries i2
						on i.player_id = i2.player_id and
						i.injury_date = i2.injury_date and
						i.return_date = i2.return_date
					where i.id != i2.id"""

		try:
			cursor.execute(query)

			# Get all duplicates.  We want to keep the first entry.
			delete_list = []
			for result in cursor:
				id1 = result[0]
				id2 = result[1]

				if str(id1) not in delete_list:
					delete_list.append(str(id2))

			# Delete the injuries that we have found to be duplicates.
			query = "delete from injuries where id in ({})".format(",".join(delete_list))
			cursor.execute(query)

		finally:
			cursor.close()

	def fix_injury_entry(self, injury, game_played_date):
		"""
		Fix an injury entry where during its span the player actually played.

		1- Incorrect one-day injuries can be deleted.
		2- Incorrect multi-day injuries can be shortened if the first or last day is incorrect.
		3- They can also be split if one or more days in the middle are incorrect.

		In the case of the third situation, we return the object representing the second injury.
		"""
		one_day = timedelta(days=1)

		# Unfortunately, this is necessary because MySQL and Sqlite3 handle dates differently.
		# if not isinstance(game_played_date, date):
		# 	pieces = game_played_date.split("-")
		# 	gpd = date(int(pieces[0]), int(pieces[1]), int(pieces[2]))
		# else:
		# 	gpd = game_played_date
		gpd = self.date_conversion(game_played_date)
		injury_date = self.date_conversion(injury.injury_date)
		return_date = self.date_conversion(injury.return_date)

		if gpd == injury_date and injury_date + one_day == return_date:
			# Erroneous one-day injury.  Delete it.
			logging.info("Injury ({} - {}) is a one-day injury where the player played.  Deleting it...".format(
				injury_date, return_date
			))
			self.delete(injury)
			return

		if injury_date == gpd:
			# First day of injury - move it up one day
			logging.info("Injury ({} - {}) is a multi-day injury where the player actually played on the first day."
						"Changing first day to {}".format(
				injury_date, return_date, injury_date + one_day
			))
			injury.injury_date = injury_date + one_day
			self.update(injury)

		elif return_date-one_day == gpd:
			# Last day of injury
			logging.info("Injury ({} - {}) is a multi-day injury where the player actually played on the last day."
						"Changing last day to {}".format(
				injury_date, return_date, return_date - one_day
			))
			injury.return_date = return_date - one_day
			self.update(injury)

		elif injury_date < gpd < return_date:
			# Somewhere in between
			old_injury_date = injury_date
			old_return_date = return_date

			new_injury = Injury(player_id=injury.player_id,
								injury_date=gpd + one_day,
								return_date=return_date,
								details=injury.details)
			injury.return_date = gpd
			logging.info("Injury ({} - {}) is a multi-day injury where the player actually played in the middle."
						"Splitting up the injuries to ({} - {}) and ({} - {})".format(
				old_injury_date, old_return_date, injury_date, return_date, new_injury.injury_date,
				new_injury.return_date
			))

			self.update(injury)
			self.insert(new_injury)

			return new_injury

	def is_player_injured(self, player_id, d=date.today()):
		"""
		Quick lookup on a player injury based on player_id and date.

		This pulls from the injury cache, so after the first call it's quick.
		"""
		if not isinstance(d, date):
			pieces = d.split("-")
			injuries = self.get_currently_injured_players(date(int(pieces[0]), int(pieces[1]), int(pieces[2])))
		else:
			injuries = self.get_currently_injured_players(d)

		return injuries[player_id] if player_id in injuries else None

	def calculate_injuries_from_gamelogs(self, season):
		"""
		Determine which players were injured on which past games based on their presence in the game log.
		"""
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
				logging.info("Looks like %s got traded at some point..." % player)
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
				date_pieces = str(d).split('-')
				injury_date = date(int(date_pieces[0]), int(date_pieces[1]), int(date_pieces[2]))
				return_date = injury_date + self.one_day
				injury = Injury(player_id=player, injury_date=injury_date, return_date=return_date,
									details="from calculate_injuries_from_gamelogs")
				if not self.exists(injury):
					logging.info("{} didn't play, adding ({} to {}) to injuries table".format(player, injury.injury_date, injury.return_date))
					self.insert(injury)

	def scrape_injury_report(self, season, source="site"):
		"""
		Scrape the injury report from Rotoworld.com and update our injuries for the day (or add new ones) accordingly.
		"""
		data = ""
		if source == "site":
			conn = httplib.HTTPConnection("www.rotoworld.com", timeout=5)
			conn.request("GET", "/teams/injuries/nba/all/")
			resp = conn.getresponse()
			data = resp.read()
			conn.close()
		else:
			f = open('../tests/rotoworld_injuries.html', 'r')
			for line in f:
				data += line

		soup = BeautifulSoup(data)

		today = date.today()
		tomorrow = today + self.one_day

		team_divs = soup.find_all("div", class_="pb")
		for team_div in team_divs:
			trs = team_div.table.find_all("tr")

			for tr in trs:
				tds = tr.find_all('td')

				# Skip the first one, it's a header.
				if tds[0].b:
					continue

				# On to the real data
				# Name, position, and status are obvious.
				# Date is the date of the injury.  For this, we're assuming that if the
				#       month of the injury is greater than the current month then the
				#       injury happened in the previous year.  This makes sense since
				#       it's pretty hard to get injured in the future.
				name = tds[0].a.text.replace("'", "")
				position = tds[2].text
				status = tds[3].text
				injury_date = tds[4].text.replace(u'\xa0', u' ')
				date_struct = time.strptime(injury_date + " %d" % (season+1), "%b %d %Y")

				# Looks like the date in the new year ends up being in the future.  Set it to the previous year.
				if date(date_struct.tm_year, date_struct.tm_mon, date_struct.tm_mday) > today:
					date_struct = time.strptime(injury_date + " %d" % season, "%b %d %Y")

				# OK, we have the injury date now.  Does this injury already exist?
				query = "select id from players where name = '%s' and rg_position is not null" % name
				cursor = self.cnx.cursor()
				player_id = None
				try:
					cursor.execute(query)
					for result in cursor:
						player_id = result[0]
				finally:
					cursor.close()

				if not player_id:
					logging.info("\tUnable to locate player_id for %s, please resolve this manually." % name)
					continue

				injury = Injury(player_id=player_id, injury_date=date(date_struct.tm_year, date_struct.tm_mon, date_struct.tm_mday))
				injuries = self.get(injury)

				if len(injuries) == 0:
					# This is a new injury
					injury_date = date(date_struct.tm_year, date_struct.tm_mon, date_struct.tm_mday)
					injury = Injury(player_id=player_id,
									injury_date=injury_date,
									return_date=tomorrow,
									details="Inserted by scrape_injury_report()")
					logging.info("Adding new injury for %s: %s = %s" % (player_id, injury_date, tomorrow))
					self.insert(injury)
				else:
					# This injury already exists.  Update the return date to tomorrow.
					#
					# This code is very sad.  For some reason I can't get actual datetime objects
					# out of the database with sqlite3 with this mysql driver (they come out as strings).
					# So, I need to convert the date to string (which it already will be with sqlite),
					# parse it out into pieces, and reconstruct it explicitly as a date.  When actually run
					# with MySQL this code is completely redundant.
					return_date_pieces = str(injuries[0].return_date).split("-")
					return_date = date(int(return_date_pieces[0]), int(return_date_pieces[1]), int(return_date_pieces[2]))
					if return_date < tomorrow:
						injuries[0].return_date = tomorrow
						logging.info("Updating injury for %s: %s = %s" % (injuries[0].player_id,
																			injuries[0].injury_date,
																			tomorrow))
						self.update(injuries[0])

	def date_conversion(self, d):
		"""
		Simple utility to convert a string to a date, if necessary.
		"""
		if not isinstance(d, date):
			pieces = d.split("-")
			return date(int(pieces[0]), int(pieces[1]), int(pieces[2]))

		return d

if __name__ == '__main__':
	logging.basicConfig(level=logging.INFO)

	manager = InjuryManager()
	manager.scrape_injury_report(2013)