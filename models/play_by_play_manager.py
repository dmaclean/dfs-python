import mysql.connector
import re
from bs4 import BeautifulSoup
from models.play_by_play import PlayByPlay


class PlayByPlayManager:
	def __init__(self, cnx=None):
		# Use dependency injection to determine where the database connection comes from.
		if not cnx:
			self.cnx = mysql.connector.connect(user='fantasy', password='fantasy', host='localhost', database='basketball_reference')
		else:
			self.cnx = cnx

	def scrape(self, source, source_type="site"):
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

		table = soup.find("table", {"class": "no_highlight stats_table"})
		trs = table.find_all('tr')
		for tr in trs:
			ths = tr.find_all('th')
			tds = tr.find_all('td')

			# Detect a quarter announcement
			if "id" in tr.attrs:
				if tr.attrs["id"] == "q1":
					print "Found 1st quarter announcement"
				elif tr.attrs["id"] == "q2":
					print "Found 2nd quarter announcement"
				elif tr.attrs["id"] == "q3":
					print "Found 3rd quarter announcement"
				elif tr.attrs["id"] == "q4":
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

	def create_pbp_instance(self, play_data):
		"""

		"""
		player_link_regex = "<a href=\"/players/[a-z]/([a-z]+[0-9]{2})\.html\">[A-Z]\. [A-Za-z \-\']+</a>"
		jump_ball_regex = "Jump ball: {} vs\. {} \({} gains possession\)".format(player_link_regex, player_link_regex, player_link_regex)
		shot_regex = "{} (makes|misses) (2|3)-pt shot from (\d+) ft( \((block|assist) by {}\))?".format(player_link_regex, player_link_regex)

		jump_ball = re.compile(jump_ball_regex)
		shot = re.compile(shot_regex)

		pbp = PlayByPlay()

		# Split up the time
		time_pieces = play_data[0].split(":")
		pbp.minutes = int(time_pieces[0])
		pbp.seconds = float(time_pieces[1])

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

		#######################
		# Shot made or missed
		#######################
		if play_data[1] != '':
			m = shot.search(play_data[1])
		else:
			m = shot.search(play_data[5])
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

if __name__ == '__main__':
	pbp_manager = PlayByPlayManager()
	pbp_manager.scrape(source="../tests/pbp_lakers_cavs.html", source_type="file")