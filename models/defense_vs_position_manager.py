__author__ = 'ap'

import mysql.connector
from dfs_constants import DFSConstants
from datetime import date
from defense_vs_position import DefenseVsPosition


class DefenseVsPositionManager():
	def __init__(self, cnx=None):
		# Use dependency injection to determine where the database connection comes from.
		if not cnx:
			self.cnx = mysql.connector.connect(user='fantasy', password='fantasy', host='localhost', database='basketball_reference')
		else:
			self.cnx = cnx

	def calculate_defense_vs_position(self, metric, position, team, season, site=None, date=date.today()):
		cursor = self.cnx.cursor()

		try:
			if metric == DFSConstants.FANTASY_POINTS:
				query = """
					select sum(fp.points)/(select max(game) from team_game_totals where team = '%s' and
												season = %d and date <= '%s')
					from players p inner join game_totals_basic b on p.id = b.player_id
						inner join fantasy_points fp on fp.player_id = p.id AND fp.season = b.season and fp.game_number = b.game_number
					where b.season = %d and p.rg_position = '%s' and b.opponent = '%s'
						and date <= '%s' and fp.site = '%s'
				""" % (team, season, date, season, position, team, date, site)
			else:
				query = """select sum(b.%s)/(select max(game) from team_game_totals where team = '%s' and season = %d and date <= '%s')
						from players p inner join game_totals_basic b on p.id = b.player_id
						where b.season = %d and p.rg_position = '%s' and b.opponent = '%s'
							and date <= '%s'""" % (metric, team, season, date, season, position, team, date)
			cursor.execute(query)

			for result in cursor:
				if result[0] is not None:
					dvp = DefenseVsPosition(stat=metric, position=position, team=team, season=season, value=result[0],
											date=date, site=site)
					if not self.exists(dvp):
						self.insert(dvp)
					else:
						dvp = self.get(dvp)[0]
					return dvp
				else:
					return None

		finally:
			cursor.close()

	def exists(self, dvp):
		cursor = self.cnx.cursor()

		try:
			query = """
				select id from defense_vs_position
				where stat = '%s' and position = '%s' and team = '%s' and season = %d and date = '%s'
			""" % (dvp.stat, dvp.position, dvp.team, dvp.season, dvp.date)

			if dvp.site:
				query += " and site = '{}'".format(dvp.site)

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
				insert into defense_vs_position (stat, position, team, season, value, date, site)
				values ('%s','%s','%s',%d,%f,'%s',<SITE>)
			"""
			if dvp.site:
				query = query.replace('<SITE>', '\'%s\'') % (dvp.stat, dvp.position, dvp.team, dvp.season, dvp.value, dvp.date, dvp.site)
			else:
				query = query.replace('<SITE>', 'null') % (dvp.stat, dvp.position, dvp.team, dvp.season, dvp.value, dvp.date)

			cursor.execute(query)
			dvp.id = cursor.lastrowid
		finally:
			cursor.close()

	def update(self, dvp):
		cursor = self.cnx.cursor()

		try:
			query = """
				update defense_vs_position set stat = '{}', position = '{}', team = '{}', season = {}, value = {}, date = '{}'
				""".format(dvp.stat, dvp.position, dvp.team, dvp.season, dvp.value, dvp.date)

			if dvp.site:
				query += ", site = '{}'".format(dvp.site)

			if dvp.rank:
				query += ", rank = {}".format(dvp.rank)

			query += " where id = {}".format(dvp.id)

			cursor.execute(query)

		finally:
			cursor.close()

	def get(self, dvp):
		cursor = self.cnx.cursor()

		dvps = []
		try:
			query = "select * from defense_vs_position where 1=1 "

			if dvp.id:
				query += "and id = %d " % dvp.id
			else:
				if dvp.stat:
					query += "and stat = '%s' " % dvp.stat
				if dvp.position:
					query += "and position = '%s' " % dvp.position
				if dvp.team:
					query += "and team = '%s' " % dvp.team
				if dvp.season:
					query += "and season = %d " % dvp.season
				# if dvp.value:
				# 	query += "and value = %f " % dvp.value
				if dvp.date:
					query += "and date = '%s' " % dvp.date
				if dvp.site:
					query += "and site = '{}' ".format(dvp.site)

			cursor.execute(query)
			for result in cursor:
				d = DefenseVsPosition(id=result[0], stat=result[1], position=result[2], team=result[3], season=result[4],
										value=result[5], rank=result[6], date=result[7], site=result[8])
				dvps.append(d)
		finally:
			cursor.close()

		return dvps