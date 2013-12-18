import sys
from datetime import date
import mysql.connector

def insert_or_update_positions(player_id, site, positions, conn):
	cursor = conn.cursor()
	
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

cnx = mysql.connector.connect(user='fantasy', password='fantasy', host='localhost', database='basketball_reference')

site = "DRAFT_DAY"
file = ""

for arg in sys.argv:
	if arg == "import_salaries.py":
		pass
	else:
		pieces = arg.split("=")
		if pieces[0] == "site":
			site = pieces[1]
		elif pieces[0] == "file":
			file = pieces[1]

f = open(file, "r")
read_header = False
salaries = {}
positions = {}

print "Importing salaries for %s" % site

for line in f:
	if not read_header:
		read_header = True
		continue
	pieces = line.split(",")
	if site == "DRAFT_DAY":
		position = pieces[0].replace("\"", "")
		name = pieces[1]
		salary = int(pieces[4])
	elif site == "DRAFT_KINGS":
		position = pieces[0].replace("\"", "")
		name = pieces[1]
		salary = int(pieces[2])
	elif site == "STAR_STREET":
		position = pieces[0].replace("\"", "").replace("-","/")
		name = pieces[1]
		salary = int(pieces[6])
	
	salaries[name] = salary
	positions[name] = position

for k in salaries:
	cursor = cnx.cursor()
	query = ("select id from players where name = '%s'") % (k.replace("'","").replace("\"",""))
	cursor.execute(query)
	
	player_id = ""
	for (id) in cursor:
		player_id = id[0]
		query = ("insert into salaries (player_id, site, salary, date) values ('%s','%s',%d, '%s')") % (player_id,site,salaries[k],date.today())
		cursor.execute(query)
	
	cursor.close()
	
	insert_or_update_positions(player_id, site, positions[k], cnx)

