__author__ = 'ap'

import mysql.connector
from datetime import date
from defense_vs_position import DefenseVsPosition

class DefenseVsPositionManager():
	def __init__(self, cnx=None):
		# Use dependency injection to determine where the database connection comes from.
		if(not cnx):
			self.cnx = mysql.connector.connect(user='fantasy', password='fantasy', host='localhost', database='basketball_reference')
		else:
			self.cnx = cnx

	def calculateDefenseVsPosition(self, metric, position, team, season, date=date.today()):
		cursor = self.cnx.cursor()

		try:
			query = """select sum(b.%s)/(select max(game) from team_game_totals where team = '%s' and season = %d and date <= '%s')
					from players p inner join game_totals_basic b on p.id = b.player_id
					where b.season = %d and p.rg_position = '%s' and b.opponent = '%s'
						and date <= '%s'""" % (metric, team, season, date, season, position, team, date)
			cursor.execute(query)

			for result in cursor:
				dvp = DefenseVsPosition(stat=metric, position=position, team=team, season=season, value=result[0], date=date)
				if not self.exists(dvp):
					self.insert(dvp)
				return result[0]

		finally:
			cursor.close()


	def exists(self, dvp):
		cursor = self.cnx.cursor()

		try:
			query = """
				select id from defense_vs_position
				where stat = '%s' and position = '%s' and team = '%s' and season = %d and date = '%s'
			""" % (dvp.stat, dvp.position, dvp.team, dvp.season, dvp.date)

			cursor.execute(query)
			for result in cursor:
				return True

		finally:
			cursor.close()

		return False

	def insert(self, dvp):
		cursor = self.cnx.cursor()

		try:
			query = """
				insert into defense_vs_position (stat, position, team, season, value, date)
				values ('%s','%s','%s',%d,%f,'%s')
			""" % (dvp.stat, dvp.position, dvp.team, dvp.season, dvp.value, dvp.date)

			cursor.execute(query)
		finally:
			cursor.close()

	def update(self, dvp):
		cursor = self.cnx.cursor()

		try:
			query = """
				update defense_vs_position set stat = '%s', position = '%s', team = '%s', season = %d, value = %f, date = '%s'
				where id = %d
			""" % (dvp.stat, dvp.position, dvp.team, dvp.season, dvp.value, dvp.date, dvp.id)

			cursor.execute(query)

		finally:
			cursor.close()

	def get(self, dvp):
		cursor = self.cnx.cursor()

		dvps = []
		try:
			query = "select * from defense_vs_position where 1=1 "

			if dvp.id:
				query = query + "and id = %d " % dvp.id
			else:
				if dvp.stat:
					query = query + "and stat = '%s' " % dvp.stat
				if dvp.position:
					query = query + "and position = '%s' " % dvp.position
				if dvp.team:
					query = query + "and team = '%s' " % dvp.team
				if dvp.season:
					query = query + "and season = %d " % dvp.season
				if dvp.value:
					query = query + "and value = %f " % dvp.value
				if dvp.date:
					query = query + "and date = '%s' " % dvp.date

			cursor.execute(query)
			for result in cursor:
				d = DefenseVsPosition(id=result[0], stat=result[1], position=result[2], team=result[3], season=result[4],
										value=result[5], date=result[6])
				dvps.append(d)
		finally:
			cursor.close()

		return dvps