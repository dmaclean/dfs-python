import sys
from datetime import date
import mysql.connector

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

print "Importing salaries for %s" % site

for line in f:
	if not read_header:
		read_header = True
		continue
	pieces = line.split(",")
	if site == "DRAFT_DAY":
		name = pieces[1]
		salary = int(pieces[4])
	elif site == "DRAFT_KINGS":
		name = pieces[1]
		salary = int(pieces[2])
	
	salaries[name] = salary

for k in salaries:
	cursor = cnx.cursor()
	query = ("select id from players where name = '%s'") % (k.replace("'","").replace("\"",""))
	cursor.execute(query)
	
	player_id = ""
	for (id) in cursor:
		query = ("insert into salaries (player_id, site, salary, date) values ('%s','%s',%d, '%s')") % (id[0],site,salaries[k],date.today())
		cursor.execute(query)
	
	cursor.close()

	