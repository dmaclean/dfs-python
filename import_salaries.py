import sys
from datetime import date
import mysql.connector

class SalaryImporter:
	
	def __init__(self, conn=None):
		if conn:
			self.cnx = conn
		else:
			self.cnx = mysql.connector.connect(user='fantasy', password='fantasy', host='localhost', database='basketball_reference')
		
		self.site = "DRAFT_DAY"
		self.salaries = {}
		self.positions = {}
	
	#########################################################################################
	# Maintains player positions for each site.  We want to keep track of which players are
	# allowed at which positions for a given site.  This will allow for more accuracy when
	# automating roster generation.
	#########################################################################################
	def insert_or_update_positions(self, player_id, site, positions):
		cursor = self.cnx.cursor()
	
		query = "select id from dfs_site_positions where player_id = '%s' and site = '%s' limit 1" % (player_id, site)
	
		try:
			cursor.execute(query)
		
			# We found a result, so do an update
			for result in cursor:
				query = "update dfs_site_positions set position = '%s' where player_id = '%s' and site = '%s'" % (positions, player_id, site)
				cursor.execute(query)
				return
		
			# No result, do an insert
			query = "insert into dfs_site_positions (player_id, site, position) values ('%s','%s','%s')" % (player_id, site, positions)
			cursor.execute(query)
		finally:
			cursor.close()

	#######################################################################################
	# Parses the provided line to properly extract the player name, position, and salary.
	# The position and salary are both stored in dictionaries which are keyed off the
	# player name.
	#######################################################################################
	def process_line(self, line):
		pieces = line.split(",")
		if self.site == "DRAFT_DAY":
			position = pieces[0].replace("\"", "")
			name = pieces[1].replace("\"", "").replace("'","")
			salary = int(pieces[4])
		elif self.site == "DRAFT_KINGS":
			position = pieces[0].replace("\"", "")
			name = pieces[1].replace("\"", "").replace("'","")
			salary = int(pieces[2])
		elif self.site == "STAR_STREET":
			position = pieces[0].replace("\"", "").replace("-","/")
			name = pieces[1].replace("\"", "").replace("'","")
			salary = int(pieces[6])

		self.salaries[name] = salary
		if name in self.positions:
			self.positions[name] = self.positions[name] + "/" + position
		else:
			self.positions[name] = position

	def run(self):
		file = ""

		for arg in sys.argv:
			if arg == "import_salaries.py":
				pass
			else:
				pieces = arg.split("=")
				if pieces[0] == "site":
					self.site = pieces[1]
				elif pieces[0] == "file":
					file = pieces[1]

		f = open(file, "r")
		read_header = False
		

		print "Importing salaries for %s" % self.site

		for line in f:
			if not read_header:
				read_header = True
				continue
			self.process_line(line)

		for k in self.salaries:
			cursor = self.cnx.cursor()
			query = ("select id from players where name = '%s'") % (k.replace("'","").replace("\"",""))
			cursor.execute(query)
	
			player_id = ""
			for (id) in cursor:
				player_id = id[0]
				query = ("insert into salaries (player_id, site, salary, date) values ('%s','%s',%d, '%s')") % (player_id,self.site,self.salaries[k],date.today())
				cursor.execute(query)
	
			cursor.close()
	
			self.insert_or_update_positions(player_id, self.site, self.positions[k])

if __name__ == '__main__':
	sa = SalaryImporter()
	sa.run()