import httplib
import mysql.connector
from bs4 import BeautifulSoup
from datetime import date

class RGPlayerStats:
	def __init__(self, cnx=None):
		if not cnx:
			self.cnx = mysql.connector.connect(user='fantasy', password='fantasy', host='localhost', database='basketball_reference')
		else:
			self.cnx = cnx
		
		self.players = []
	
	###################################################################################
	# As the name suggests, this function does an insert for a new record, or updates
	# it if it already exists.
	###################################################################################
	def update_rg_position(self, values):
		cursor = self.cnx.cursor()
	
		try:
			cursor.execute("select rg_position from players where id = '%s'"  % (values["player_id"]))
			
			for result in cursor:
				cursor.execute("update players set rg_position = '%s' where id = '%s'" % (values["rg_position"], 
					values["player_id"]))
		finally:
			cursor.close()
	
	def get_id_for_player(self, name):
		cursor = self.cnx.cursor()
		
		query = "select id from players where name = '%s'" % (name)
		
		try:
			cursor.execute(query)
			
			for result in cursor:
				return result[0]
		finally:
			cursor.close()
	
	def process(self, source="site", page=None):
		data = ""
		if source == "site":
			conn = httplib.HTTPConnection("rotogrinders.com", timeout=5)
			conn.request("GET", page)
			resp = conn.getresponse()
			data = resp.read()
			conn.close()
		else:
			f = open('../tests/NBA_Player_Stats_Guards.html', 'r')
			for line in f:
				data = data + line

		soup = BeautifulSoup(data)

		# Table containing the odds
		table = soup.find_all('table')[1]

		# Iterate through each row, ignoring the first (which is just a header).
		found_header = False
		for tr in table.find_all('tr'):
			if not found_header:
				found_header = True
				continue
	
			try:
				tds = tr.find_all('td')
				
				# Try to grab the player name from the anchor tag.
				try:
					name = tds[0].a.text
				# Looks like there's no anchor tag.  Try just the td.
				except AttributeError:
					name = tds[0].text.strip()
				position = tds[2].text.strip()
				
				player_id = self.get_id_for_player(name)
			except ValueError:
				print "Error parsing one of the values."
				quit()
			
			self.players.append( { "player_id": player_id, "name": name, "rg_position": position } )

		# Store in database.
		for p in self.players:
			self.update_rg_position(p)

if __name__ == '__main__':
	ps = RGPlayerStats()
	
	season_pages = ['/pages/NBA_Player_Stats_Guards-181856',
					'/pages/NBA_Player_Stats_Forwards-181857',
					'/pages/NBA_Player_Stats_Centers-181858']
	
	for p in season_pages:
		ps.process(page=p)