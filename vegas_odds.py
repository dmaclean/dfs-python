import httplib
import mysql.connector
from bs4 import BeautifulSoup
from datetime import date

def insert_or_update(cnx, odds):
	cursor = cnx.cursor()
	
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
	
	

conn = httplib.HTTPConnection("rotogrinders.com", timeout=5)
conn.request("GET", "/pages/NBA_Vegas_Odds_Page-81324")
resp = conn.getresponse()

soup = BeautifulSoup(resp)

# Translation map for full name --> abbreviations
team_names = {
	"Bobcats": "CHA",
	"Chicago": "CHI",
	"Dallas": "DAL",
	"Denver": "DEN",
	"Detroit": "DET",
	"LAClippers": "LAC",
	"Memphis": "MEM",
	"Miami": "MIA",
	"Minnesota": "MIN",
	"NewOrleans": "NOP",
	"Phoenix": "PHO",
	"Portland": "POR",
	"Utah": "UTA",
	"Washington": "WAS"
}

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
	road_team = team_names[road_team] if road_team in team_names else road_team
	
	# Home team
	img_src = tr.find_all('td')[1].img['src']
	img_pieces = img_src.split('/')
	home_team = img_pieces[len(img_pieces)-1].split('_')[0].replace("NBA", "")
	home_team = team_names[home_team] if home_team in team_names else home_team
	
	road_spread = float(tr.find_all('td')[2].text)
	home_spread = float(tr.find_all('td')[3].text)
	over_under = float(tr.find_all('td')[4].text)
	road_score = float(tr.find_all('td')[5].text)
	home_score = float(tr.find_all('td')[6].text)
	
	odds.append( { "date": date.today(), 
		"road_team": road_team, 
		"home_team": home_team, 
		"spread_road": road_spread, 
		"spread_home": home_spread, 
		"over_under": over_under, 
		"projection_road": road_score, 
		"projection_home": home_score
		} )
	
	print "%s\t%s\t%f\t%f\t%f\t%f\t%f" % (road_team, home_team, road_spread, home_spread, over_under, road_score, home_score)

# Store in database.
cnx = mysql.connector.connect(user='fantasy', password='fantasy', host='localhost', database='basketball_reference')

for o in odds:
	insert_or_update(cnx, o)

cnx.close()
conn.close()