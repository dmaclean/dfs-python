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
		print "Running SQL on SQLite database"
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
	
	def insert_into_game_totals_basic(self, values):
		pass