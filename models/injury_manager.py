__author__ = 'ap'

import mysql.connector
from datetime import date

from models.injury import Injury

class InjuryManager():
	def __init__(self, cnx=None):
		# Use dependency injection to determine where the database connection comes from.
		if(not cnx):
			self.cnx = mysql.connector.connect(user='fantasy', password='fantasy', host='localhost', database='basketball_reference')
		else:
			self.cnx = cnx

	def exists(self, injury):
		cursor = self.cnx.cursor()

		query = """
			select id from injuries
			where player_id = '%s' and injury_date = '%s' and return_date = '%s'
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
			query = query + "and id = %d " % injury.id
		else:
			if injury.player_id:
				query = query + "and player_id = '%s' " % injury.player_id
			if injury.injury_date:
				query = query + "and injury_date = '%s' " % injury.injury_date
			if injury.return_date:
				query = query + "and return_date = '%s' " % injury.return_date
			if injury.details:
				query = query + "and details = '%s' " % injury.details

		try:
			cursor.execute(query)
			for result in cursor:
				i = Injury(id=result[0], player_id=result[1], injury_date=result[2], return_date=result[3], details=result[4])
				injuries.append(i)
		finally:
			cursor.close()

		return injuries

	def get_currently_injured_players(self, date=date.today()):
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