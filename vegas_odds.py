import httplib
import logging
import mysql.connector
from bs4 import BeautifulSoup
from datetime import date

class VegasOdds:
	def __init__(self, cnx=None):
		if not cnx:
			self.cnx = mysql.connector.connect(user='fantasy', password='fantasy', host='localhost', database='basketball_reference')
		else:
			self.cnx = cnx
		
		# Translation map for full name --> abbreviations
		self.team_names = {
			"Atlanta": "ATL",
			"Bobcats": "CHA",
			"Boston": "BOS",
			"Brooklyn": "BRK",
			"Chicago": "CHI",
			"Cleveland": "CLE",
			"Dallas": "DAL",
			"Denver": "DEN",
			"Detroit": "DET",
			"GoldenState": "GSW",
			"Houston": "HOU",
			"Indiana": "IND",
			"LAClippers": "LAC",
			"LALakers": "LAL",
			"Memphis": "MEM",
			"Miami": "MIA",
			"Milwaukee": "MIL",
			"Minnesota": "MIN",
			"NewOrleans": "NOP",
			"NewYork": "NYK",
			"OklahomaCity": "OKC",
			"Orlando": "ORL",
			"Philadelphia": "PHI",
			"Phoenix": "PHO",
			"Portland": "POR",
			"Sacramento": "SAC",
			"SanAntonio": "SAS",
			"Toronto": "TOR",
			"Utah": "UTA",
			"Washington": "WAS"
		}
		
	
	###################################################################################
	# As the name suggests, this function does an insert for a new record, or updates
	# it if it already exists.
	###################################################################################
	def insert_or_update(self, cnx, odds):
		cursor = self.cnx.cursor()
	
		try:
			got_hit = False
			cursor.execute("""
				select id from vegas where date = '%s' and road_team = '%s' and home_team = '%s'
				"""  % (odds["date"], odds["road_team"], odds["home_team"]))
		
			for result in cursor:
				got_hit = True
				cursor.execute(""""
					update vegas set spread_road = %f, spread_home = %f, over_under = %f, projection_road = %f, projection_home = %f
					where date = '%s' and road_team = '%s' and home_team = '%s'
				""" % (odds["spread_road"], odds["spread_home"], odds["over_under"], odds["projection_road"], odds["projection_home"],
						odds["date"], odds["road_team"], odds["home_team"] ))
		
			if not got_hit:
				query = """
					insert into vegas (date, road_team, home_team, spread_road, spread_home, over_under, projection_road, projection_home)
					values ('%s','%s','%s',%f,%f,%f,%f,%f)
				""" % (odds["date"], odds["road_team"], odds["home_team"], odds["spread_road"], odds["spread_home"], odds["over_under"], odds["projection_road"], odds["projection_home"])
			
				cursor.execute(query)
		finally:
			cursor.close()
	
	def process(self, source="site"):
		data = ""
		if source == "site":
			conn = httplib.HTTPConnection("rotogrinders.com", timeout=5)
			conn.request("GET", "/pages/NBA_Vegas_Odds_Page-81324")
			resp = conn.getresponse()
			data = resp.read()
			conn.close()
		else:
			f = open('../tests/odds.html', 'r')
			for line in f:
				data = data + line

		soup = BeautifulSoup(data)

		# Table containing the odds
		table = soup.find_all('table')[1]

		odds = []

		# Iterate through each row, ignoring the first (which is just a header).
		found_header = False
		for tr in table.find_all('tr'):
			if not found_header:
				found_header = True
				continue
	
			# Images for team
			# http://i1055.photobucket.com/albums/s520/haskele/NBADetroit_zps3479438e.png
			# Road team
			img_src = tr.find_all('td')[0].img['src']
			img_pieces = img_src.split('/')
			road_team = img_pieces[len(img_pieces)-1].split('_')[0].replace("NBA", "")
			road_team = self.team_names[road_team] if road_team in self.team_names else road_team
	
			# Home team
			img_src = tr.find_all('td')[1].img['src']
			img_pieces = img_src.split('/')
			home_team = img_pieces[len(img_pieces)-1].split('_')[0].replace("NBA", "")
			home_team = self.team_names[home_team] if home_team in self.team_names else home_team
	
			try:
				road_spread = float(tr.find_all('td')[2].text)
				home_spread = float(tr.find_all('td')[3].text)
				over_under = float(tr.find_all('td')[4].text)
				road_score = float(tr.find_all('td')[5].text)
				home_score = float(tr.find_all('td')[6].text)
			except ValueError:
				logging.error("Error parsing one of the values.  The odds are probably not fully updated.")
				quit()
	
			odds.append( { "date": date.today(), 
				"road_team": road_team, 
				"home_team": home_team, 
				"spread_road": road_spread, 
				"spread_home": home_spread, 
				"over_under": over_under, 
				"projection_road": road_score, 
				"projection_home": home_score
				} )
	
			logging.info("%s\t%s\t%f\t%f\t%f\t%f\t%f" % (road_team, home_team, road_spread, home_spread, over_under, road_score, home_score))

		# Store in database.
		for o in odds:
			logging.info("Storing %s/%s to database." % (o["road_team"], o["home_team"]))
			self.insert_or_update(self.cnx, o)

if __name__ == '__main__':
	odds = VegasOdds()
	odds.process()