import logging
import re
import time

from bs4 import BeautifulSoup
from mlb.constants.mlb_constants import MLBConstants
from mlb.models.lineup_manager import LineupManager
from mlb.models.name_mapping_manager import NameMappingManager
from mlb.models.player_manager import PlayerManager
from mlb.scrapers.bbr_scraper import BaseballReferenceScraper


__author__ = 'dan'


class RotoworldLineupScraper:
	def __init__(self, sleep_time=2, testing=False):
		self.source = "site"
		self.player_regex = re.compile("/baseball/player.htm\?id=\d+")
		self.player_manager = PlayerManager(testing=testing)
		self.lineup_manager = LineupManager(testing=testing)
		self.name_mapping_manager = NameMappingManager(testing=testing)
		self.bbr_scraper = BaseballReferenceScraper()
		self.bbr_scraper.sleep_time = sleep_time

	def parse_teams_only(self, data):
		"""
		Parse the rotowire page to determine which teams are playing today.
		"""
		data = data.replace("\r", "").replace("\n", "").replace("\t", "")
		soup = BeautifulSoup(data, "lxml")

		teams = []
		team_details = {}

		matchups = soup.find_all(attrs={"class": "offset1 span15"})
		for matchup in matchups:
			# Is this an ad tile?
			promo_div = matchup.find(attrs={"class": "dlineups-toolpromo-head"})
			if promo_div is not None:
				continue

			# Is this game postponed?
			postponed_div = matchup.find(attrs={"class": "dlineups-postponed"})
			if postponed_div is not None:
				continue

			away_team = matchup.find(attrs={"class": "dlineups-topboxleft"}).text
			home_team = matchup.find(attrs={"class": "span5 dlineups-topboxright"}).text

			teams.append(away_team)
			teams.append(home_team)

			pitchers_divs = matchup.find(attrs={"class": "span11 dlineups-pitchers"}).find_all("div")
			away_pitcher = pitchers_divs[0].a.text
			home_pitcher = pitchers_divs[1].a.text

			# Grab the odds
			odds_div = matchup.find(attrs={"class": "span4 dlineups-odds-bottom"})
			odds = odds_div.text.replace("Line:", "").split("O/U:")
			odds[0] = odds[0].strip().replace(u"\xa0"," ")
			odds[1] = odds[1].strip().replace(u"\xa0"," ")

			team_details[home_team] = {
				"batting_order_position": -1,
				MLBConstants.POSITION: "",
				"opposing_pitcher": away_pitcher,
				"team": home_team,
				"opponent": away_team,
				"home": True,
				MLBConstants.VEGAS_LINE: odds[0],
				MLBConstants.OVER_UNDER: odds[1],
				MLBConstants.VERIFIED: False
			}

			team_details[away_team] = {
				"batting_order_position": -1,
				MLBConstants.POSITION: "",
				"opposing_pitcher": home_pitcher,
				"team": away_team,
				"opponent": home_team,
				"home": False,
				MLBConstants.VEGAS_LINE: odds[0],
				MLBConstants.OVER_UNDER: odds[1],
				MLBConstants.VERIFIED: False
			}

		return teams, team_details

	def parse(self, data):
		data = data.replace("\r", "").replace("\n", "").replace("\t", "")
		soup = BeautifulSoup(data, "lxml")

		teams = []
		team_details = {}

		matchups = soup.find_all(attrs={"class": "offset1 span15"})
		for matchup in matchups:
			# Is this an ad tile?
			promo_div = matchup.find(attrs={"class": "dlineups-toolpromo-head"})
			if promo_div is not None:
				continue

			# Is this game postponed?
			postponed_div = matchup.find(attrs={"class": "dlineups-postponed"})
			if postponed_div is not None:
				continue

			away_team = matchup.find(attrs={"class": "dlineups-topboxleft"}).text
			home_team = matchup.find(attrs={"class": "span5 dlineups-topboxright"}).text

			teams.append(away_team)
			teams.append(home_team)

			lineup_divs = matchup.find_all(attrs={"class": "dlineups-half"})
			away_lineup = lineup_divs[0]
			home_lineup = lineup_divs[1]

			pitchers_divs = matchup.find(attrs={"class": "span11 dlineups-pitchers"}).find_all("div")
			away_pitcher = pitchers_divs[0].a.text
			home_pitcher = pitchers_divs[1].a.text

			# Grab the odds
			odds_div = matchup.find(attrs={"class": "span4 dlineups-odds-bottom"})
			odds = odds_div.text.replace("Line:", "").split("O/U:")
			odds[0] = odds[0].strip().replace(u"\xa0"," ")
			odds[1] = odds[1].strip().replace(u"\xa0"," ")

			for lineup in [away_lineup, home_lineup]:
				players = lineup.find_all(href=self.player_regex)
				batting_order_position = 1
				position = ""
				for player in players:
					player_name = None

					# Pitcher
					if "title" not in player.attrs:
						print "{} (Starting pitcher)".format(player.text)
						player_name = player.text
						position = "P"
					# Position player
					else:
						print "{}".format(player.text)
						player_name = player.attrs["title"]
						position = player.parent.parent.find_all("div", attrs={"class": "dlineups-pos"})[0].text

					team = home_team if lineup == home_lineup else away_team
					opponent = home_team if lineup == away_lineup else away_team
					self.process_player(player_name, {
						"batting_order_position": batting_order_position,
						MLBConstants.POSITION: position,
						"opposing_pitcher": home_pitcher if lineup == away_lineup else away_pitcher,
						"team": team,
						"opponent": opponent,
						"home": True if lineup == home_lineup else False,
						MLBConstants.VEGAS_LINE: odds[0],
						MLBConstants.OVER_UNDER: odds[1],
					    MLBConstants.VERIFIED: True
					})

					batting_order_position += 1

			# Process the pitchers
			self.process_player(away_pitcher, {
				"batting_order_position": -1,
				MLBConstants.POSITION: "P",
				"opposing_pitcher": home_pitcher,
				"team": away_team,
				"opponent": home_team,
				"home": False,
				MLBConstants.VEGAS_LINE: odds[0],
				MLBConstants.OVER_UNDER: odds[1],
				MLBConstants.VERIFIED: True
			})

			self.process_player(home_pitcher, {
				"batting_order_position": -1,
				MLBConstants.POSITION: "P",
				"opposing_pitcher": away_pitcher,
				"team": home_team,
				"opponent": away_team,
				"home": True,
				MLBConstants.VEGAS_LINE: odds[0],
				MLBConstants.OVER_UNDER: odds[1],
				MLBConstants.VERIFIED: True
			})

	def process_player(self, player_name, additional_data):
		"""
		Perform data scraping and creation of lineup data for each player.  We also save
		the player's entry into the day's lineup from here.
		"""
		start = time.time()

		player_data = self.player_manager.players_collection.find_one({'name': player_name}, {"player_id": 1})
		if player_data is None:
			original_name = player_name
			player_name = self.name_mapping_manager.get_player_name(MLBConstants.MONGO_MLB_NAME_MAPPING_ROTOWIRE, MLBConstants.MONGO_MLB_NAME_MAPPING_BBR, player_name)
			player_data = self.player_manager.players_collection.find_one({'name': player_name}, {"player_id": 1})
			if player_data is None:
				logging.critical("Could not find record for {}".format(original_name))
				return

		player_id = player_data["player_id"]
		escaped_player_id = self.lineup_manager.get_id_for_player_name(player_name)
		if self.lineup_manager.is_processed(escaped_player_id):
			print "{} already processed.  No scraping necessary.".format(player_name.encode('ascii','ignore'))
		else:
			# Found a player.  Let's update their stuff.
			url = "/players/{}/".format(player_id[0:1])
			self.bbr_scraper.process_player(player_id, url, active=True)

		# Mark the player as processed (write to the lineup) once their stats have been updated.
		player_lineup_data = {
			"batting_order_position": additional_data["batting_order_position"],
			"opposing_pitcher": additional_data["opposing_pitcher"],
			"team": additional_data["team"],
			"opponent": additional_data["opponent"],
			"home": additional_data["home"],
			MLBConstants.POSITION: additional_data[MLBConstants.POSITION],
			MLBConstants.VEGAS_LINE: additional_data[MLBConstants.VEGAS_LINE],
			MLBConstants.OVER_UNDER: additional_data[MLBConstants.OVER_UNDER],
		    MLBConstants.VERIFIED: additional_data[MLBConstants.VERIFIED]
		}
		self.lineup_manager.add_player_to_lineup(escaped_player_id, player_lineup_data)

		end = time.time()
		print "Processed {} in {} seconds".format(player_id, end-start)