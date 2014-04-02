import re

import mysql.connector
from bs4 import BeautifulSoup

from pymongo import MongoClient
from shared.dfs_constants import DFSConstants
from nba.models.play_by_play import PlayByPlay
from nba.models.play_by_play_game import PlayByPlayGame


class PlayByPlayManager:
	def __init__(self, cnx=None, mongo_db=None):
		# Use dependency injection to determine where the database connection comes from.
		if not cnx:
			self.cnx = mysql.connector.connect(user='fantasy', password='fantasy', host='localhost', database='basketball_reference')
		else:
			self.cnx = cnx

		if not mongo_db:
			mongo_client = MongoClient()
			self.mongo_db = mongo_client[DFSConstants.MONGO_NBA_DB_NAME]
		else:
			self.mongo_db = mongo_db

	def scrape(self, source, source_type="site", additional_data=None):
		"""
		Scrapes the provided source for play-by-play data.  If the type is
		"site" then the source is expected to be a URL.  Otherwise, the function
		expects a file name.
		"""
		if source_type == "site":
			pass
		else:
			f = open(source, "r")
			data = f.read().decode("utf-8", "ignore")
			data = data.replace('<th colspan="6">1st Quarter (<a href="#pbp">Back to Top</a>)</td>',
								'<td colspan="6">1st Quarter (<a href="#pbp">Back to Top</a>)</td>')
			data = data.replace('<th colspan="6">2nd Quarter (<a href="#pbp">Back to Top</a>)</td>',
								'<td colspan="6">2nd Quarter (<a href="#pbp">Back to Top</a>)</td>')
			data = data.replace('<th colspan="6">3rd Quarter (<a href="#pbp">Back to Top</a>)</td>',
								'<td colspan="6">3rd Quarter (<a href="#pbp">Back to Top</a>)</td>')
			data = data.replace('<th colspan="6">4th Quarter (<a href="#pbp">Back to Top</a>)</td>',
								'<td colspan="6">4th Quarter (<a href="#pbp">Back to Top</a>)</td>')

		soup = BeautifulSoup(data)

		pbps = []

		table = soup.find("table", {"class": "no_highlight stats_table"})
		trs = table.find_all('tr')
		quarter = 0
		for tr in trs:
			ths = tr.find_all('th')
			tds = tr.find_all('td')

			# Detect a quarter announcement
			if "id" in tr.attrs:
				if tr.attrs["id"] == "q1":
					quarter = 1
					print "Found 1st quarter announcement"
				elif tr.attrs["id"] == "q2":
					quarter = 2
					print "Found 2nd quarter announcement"
				elif tr.attrs["id"] == "q3":
					quarter = 3
					print "Found 3rd quarter announcement"
				elif tr.attrs["id"] == "q4":
					quarter = 4
					print "Found 4th quarter announcement"
			# Detect a header
			elif len(ths) > 0:
				print "Found a header - {}/{}/{}/{}".format(ths[0].text, ths[1].text, ths[2].text, ths[3].text)
			# Detect something team-neutral, like the start/end of a quarter or a jump ball.
			elif len(tds) == 2:
				time = tds[0].text
				action = tds[1].text

				print "{} - {}".format(time, action)
			# Detect an action within the game
			elif len(tds) == 6:
				time = tds[0].text
				t1_action = tds[1].text.replace(u'\xa0', u'')
				t1_scoring = tds[2].text.replace(u'\xa0', u'')
				game_score = tds[3].text
				t2_scoring = tds[4].text.replace(u'\xa0', u'')
				t2_action = tds[5].text.replace(u'\xa0', u'')

				print "{:<20}{:<60}{:<10}{:<20}{:<10}{:<20}".format(time, t1_action, t1_scoring, game_score, t2_scoring, t2_action)

				pbp = self.create_pbp_instance([time, t1_action, t1_scoring, game_score, t2_scoring, t2_action, quarter])
				pbps.append(pbp)

		if additional_data and PlayByPlayGame.GAME_DATE in additional_data:
			game_date = additional_data[PlayByPlayGame.GAME_DATE]
		if additional_data and PlayByPlayGame.HOME in additional_data:
			home = additional_data[PlayByPlayGame.HOME]
		if additional_data and PlayByPlayGame.AWAY in additional_data:
			away = additional_data[PlayByPlayGame.AWAY]

		pbp_game = PlayByPlayGame(pbp_data=pbps, game_date=game_date, home=home, away=away)
		self.mongo_db[DFSConstants.MONGO_NBA_PBP_COLLECTION].save(pbp_game)

	def create_pbp_instance(self, play_data):
		"""
		Creates an instance of PlayByPlay based on the data passed in.  A play can be one
		of the following:
		- Jump ball
		- Shot (made/missed 2 or 3 point shot)
		- Free throw (made/missed)
		- Rebound
		- Foul
		- Turnover
		- Substitution
		- Timeout
		"""
		player_link_regex = "<a href=\"/players/[a-z]/([a-z]+[0-9]{2})\.html\">[A-Z]\. [A-Za-z \-\']+</a>"
		jump_ball_regex = "Jump ball: {} vs\. {} \({} gains possession\)".format(player_link_regex, player_link_regex, player_link_regex)
		shot_regex = "{} (makes|misses) (2|3)-pt shot from (\d+) ft( \((block|assist) by {}\))?".format(player_link_regex, player_link_regex)
		free_throw_regex = "{} (makes|misses) free throw [1|2] of [1|2]".format(player_link_regex)
		rebound_regex = "(Defensive|Offensive) rebound by ({}|Team)".format(player_link_regex)
		foul_regex = "(Shooting|Loose ball|Personal|Offensive charge) foul by {}( \(drawn by {}\))?".format(player_link_regex, player_link_regex)
		turnover_regex = "Turnover by {} \((lost ball|bad pass|offensive foul)(; steal by {})?\)".format(player_link_regex, player_link_regex)
		substitution_regex = "{} enters the game for {}".format(player_link_regex, player_link_regex)
		timeout_regex = "([\w ]+) timeout"

		jump_ball = re.compile(jump_ball_regex)
		shot = re.compile(shot_regex)
		free_throw = re.compile(free_throw_regex)
		rebound = re.compile(rebound_regex)
		foul = re.compile(foul_regex)
		turnover = re.compile(turnover_regex)
		substitution = re.compile(substitution_regex)
		timeout = re.compile(timeout_regex)

		pbp = PlayByPlay()

		# Add players on court
		pbp.home_players = play_data[len(play_data)-3]
		pbp.away_players = play_data[len(play_data)-2]

		# Split up the time
		time_pieces = play_data[0].split(":")
		pbp.minutes = int(time_pieces[0])
		pbp.seconds = float(time_pieces[1])

		# Record the quarter
		pbp.quarter = play_data[len(play_data)-1]

		#############
		# Jump ball
		#############
		m = jump_ball.search(play_data[1])
		if m:
			pbp.play_type = PlayByPlay.JUMP_BALL
			pbp.players.append(m.group(1))
			pbp.players.append(m.group(2))
			pbp.players.append(m.group(3))

			return pbp

		score_pieces = play_data[3].split("-")
		pbp.visitor_score = int(score_pieces[0])
		pbp.home_score = int(score_pieces[1])

		if play_data[1] != '':
			data = play_data[1]
		else:
			data = play_data[5]

		#######################
		# Shot made or missed
		#######################
		m = shot.search(data)
		if m:
			pbp.play_type = PlayByPlay.SHOT
			pbp.players.append(m.group(1))
			pbp.shot_made = m.group(2) == "makes"
			pbp.point_value = int(m.group(3))
			pbp.shot_distance = int(m.group(4))
			if m.group(5):
				pbp.secondary_play_type = m.group(6)
				pbp.players.append(m.group(7))

			return pbp

		#############################
		# Free throw made or missed
		#############################
		m = free_throw.search(data)
		if m:
			pbp.play_type = PlayByPlay.FREE_THROW
			pbp.players.append(m.group(1))
			pbp.shot_made = m.group(2) == "makes"
			pbp.point_value = 1
			pbp.shot_distance = 15

			return pbp

		###########
		# Rebound
		###########
		m = rebound.search(data)
		if m:
			pbp.play_type = PlayByPlay.REBOUND
			pbp.shot_made = None
			pbp.point_value = 0
			pbp.secondary_play_type = None
			pbp.shot_distance = None
			if m.group(1) == "Defensive":
				pbp.detail = PlayByPlay.REBOUND_DEFENSIVE
			else:
				pbp.detail = PlayByPlay.REBOUND_OFFENSIVE

			if m.group(2) != "Team":
				pbp.players.append(m.group(3))

			return pbp

		########
		# Foul
		########
		m = foul.search(data)
		if m:
			pbp.play_type = PlayByPlay.FOUL
			pbp.detail = m.group(1)

			pbp.point_value = 0
			pbp.shot_made = None
			pbp.shot_distance = None
			pbp.secondary_play_type = None
			pbp.players.append(m.group(2))

			if pbp.detail == PlayByPlay.FOUL_SHOOTING:
				pbp.players.append(m.group(4))

			return pbp

		############
		# Turnover
		############
		m = turnover.search(data)
		if m:
			pbp.play_type = PlayByPlay.TURNOVER
			pbp.players.append(m.group(1))
			pbp.point_value = 0
			pbp.shot_made = None
			pbp.shot_distance = None
			pbp.secondary_play_type = None
			pbp.detail = m.group(2)

			if m.group(3):
				pbp.players.append(m.group(4))

			return pbp

		################
		# Substitution
		################
		m = substitution.search(data)
		if m:
			pbp.play_type = PlayByPlay.SUBSTITUTION
			pbp.detail = None
			pbp.point_value = 0
			pbp.shot_made = None
			pbp.shot_distance = None
			pbp.secondary_play_type = None
			pbp.players.append(m.group(1))
			pbp.players.append(m.group(2))

			return pbp

		###########
		# Timeout
		###########
		m = timeout.search(data)
		if m:
			pbp.play_type = PlayByPlay.TIMEOUT
			pbp.detail = m.group(1).replace(' full', '')
			pbp.point_value = 0
			pbp.shot_made = None
			pbp.shot_distance = None
			pbp.secondary_play_type = None

			return pbp

	def save(self, pbp_game):
		pass

	def get(self, play_by_play):
		pass

if __name__ == '__main__':
	pbp_manager = PlayByPlayManager()
	pbp_manager.scrape(source="../tests/pbp_lakers_cavs.html", source_type="file")