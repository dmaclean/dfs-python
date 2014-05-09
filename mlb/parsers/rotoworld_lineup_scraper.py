import logging
import re
from bs4 import BeautifulSoup
from mlb.models.lineup_manager import LineupManager
from mlb.models.player_manager import PlayerManager
from mlb.utilities.bbr_scraper import BaseballReferenceScraper

__author__ = 'dan'


class RotoworldLineupScraper:
	def __init__(self, sleep_time=2, testing=False):
		self.source = "site"
		self.player_regex = re.compile("/baseball/player.htm\?id=\d+")
		self.player_manager = PlayerManager(testing=testing)
		self.lineup_manager = LineupManager(testing=testing)
		self.bbr_scraper = BaseballReferenceScraper()
		self.bbr_scraper.sleep_time = sleep_time

	def parse(self, data):
		data = data.replace("\r", "").replace("\n", "").replace("\t", "")
		soup = BeautifulSoup(data)

		matchups = soup.find_all(attrs={"class": "offset1 span15"})
		for matchup in matchups:
			away_team = matchup.find(attrs={"class": "dlineups-topboxleft"}).text
			home_team = matchup.find(attrs={"class": "span5 dlineups-topboxright"}).text

			lineup_divs = matchup.find_all(attrs={"class": "dlineups-half"})
			away_lineup = lineup_divs[0]
			home_lineup = lineup_divs[1]

			pitchers_divs = matchup.find(attrs={"class": "span11 dlineups-pitchers"}).find_all("div")
			away_pitcher = pitchers_divs[0].a.text
			home_pitcher = pitchers_divs[1].a.text

			for lineup in [away_lineup, home_lineup]:
				players = lineup.find_all(href=self.player_regex)
				batting_order_position = 1
				for player in players:
					player_name = None

					# Pitcher
					if "title" not in player.attrs:
						print "{} (Starting pitcher)".format(player.text)
						player_name = player.text
					# Position player
					else:
						print "{}".format(player.text)
						player_name = player.attrs["title"]

					# player_data = self.player_manager.players_collection.find_one({'name': player_name}, {"player_id": 1})
					# if player_data is None:
					# 	logging.critical("Could not find record for {}".format(player_name))
					# 	continue
					#
					# player_id = player_data["player_id"]
					# escaped_player_id = self.lineup_manager.get_id_for_player_name(player_name)
					# if self.lineup_manager.is_processed(escaped_player_id):
					# 	print "{} already processed.  No scraping necessary.".format(player_name)
					# else:
					# 	# Found a player.  Let's update their stuff.
					# 	url = "/players/{}/".format(player_id[0:1])
					# 	self.bbr_scraper.process_player(player_id, url, active=True)
					#
					# # Mark the player as processed (write to the lineup) once their stats have been updated.
					# player_lineup_data = {
					# 	"batting_order_position": batting_order_position,
					#     "opposing_pitcher": home_pitcher if lineup == away_lineup else away_pitcher,
					#     "team": home_team if lineup == home_lineup else away_team,
					#     "opponent": home_team if lineup == away_lineup else home_team
					# }
					# self.lineup_manager.add_player_to_lineup(escaped_player_id, player_lineup_data)
					self.process_player(player_name, {
						"batting_order_position": batting_order_position,
					    "opposing_pitcher": home_pitcher if lineup == away_lineup else away_pitcher,
					    "team": home_team if lineup == home_lineup else away_team,
					    "opponent": home_team if lineup == away_lineup else home_team
					})

					batting_order_position += 1

			# Process the pitchers
			self.process_player(away_pitcher, {
				"batting_order_position": -1,
			    "opposing_pitcher": home_pitcher,
			    "team": away_team,
			    "opponent": home_team
			})

			self.process_player(home_pitcher, {
				"batting_order_position": -1,
			    "opposing_pitcher": away_pitcher,
			    "team": home_team,
			    "opponent": away_team
			})

	def process_player(self, player_name, additional_data):
		"""
		Perform data scraping and creation of lineup data for each player.  We also save
		the player's entry into the day's lineup from here.
		"""
		player_data = self.player_manager.players_collection.find_one({'name': player_name}, {"player_id": 1})
		if player_data is None:
			logging.critical("Could not find record for {}".format(player_name))
			return

		player_id = player_data["player_id"]
		escaped_player_id = self.lineup_manager.get_id_for_player_name(player_name)
		if self.lineup_manager.is_processed(escaped_player_id):
			print "{} already processed.  No scraping necessary.".format(player_name)
		else:
			# Found a player.  Let's update their stuff.
			url = "/players/{}/".format(player_id[0:1])
			self.bbr_scraper.process_player(player_id, url, active=True)

		# Mark the player as processed (write to the lineup) once their stats have been updated.
		player_lineup_data = {
			"batting_order_position": additional_data["batting_order_position"],
		    "opposing_pitcher": additional_data["opposing_pitcher"],
		    "team": additional_data["team"],
		    "opponent": additional_data["opponent"]
		}
		self.lineup_manager.add_player_to_lineup(escaped_player_id, player_lineup_data)