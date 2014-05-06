import hashlib
import logging
import random
import sys
import time
from httplib import HTTPConnection
from json import JSONDecoder
from mlb.models.player_manager import PlayerManager

__author__ = 'dan'


class StatsCollector:
	def __init__(self, api_key=None, secret=None):
		self.api_key = api_key
		self.secret = secret
		self.player_manager = PlayerManager()

	def build_auth_params(self):
		"""This function takes our API key and shared secret and uses it to create the signature that mashery wants """
		auth_hash = hashlib.sha256()

		#time.time() gets the current time since the epoch (1970) with decimals seconds
		temp = str.encode(self.api_key + self.secret + repr(int(time.time())))
		auth_hash.update(temp)

		return auth_hash.hexdigest()


	def fetch_data(self, url, log_to_console):
		"""
		Makes connection to baseball-reference and downloads data from URL.
		"""
		successful = False
		data = ""

		while not successful:
			try:
				conn = HTTPConnection("api.stats.com", timeout=5)
				conn.request("GET", "{}?api_key={}&sig={}".format(url, self.api_key, self.build_auth_params()))
				resp = conn.getresponse()
				content_type = resp.getheader("content-type")

				encoding = None
				if content_type.find("charset=") > -1:
					encoding = content_type.split("charset=")[1]

				if log_to_console:
					print "{} for {}".format(resp.status, url)

				if encoding:
					data = resp.read().decode(encoding, 'ignore')
				else:
					data = resp.read()

				conn.close()
				successful = True
			except Exception, err:
				logging.error("Issue connecting to STATS INC ({}).  Retrying in 10 seconds...".format(err))
				time.sleep(10)

		time.sleep(5 + (5 * random.random()))
		return data

	def get_mlb_teams(self, data):
		result = {}

		team_data = JSONDecoder().decode(data)
		leagues = team_data["apiResults"][0]["league"]["season"]["conferences"]
		for league in leagues:
			divisions = league["divisions"]
			for division in divisions:
				teams = division["teams"]
				for team in teams:
					result[str(team["teamId"])] = {
						"location": team["location"],
					    "nickname": team["nickname"]
					}

					result[str(team["location"])] = {
						"teamId": team["teamId"],
					    "nickname": team["nickname"]
					}

		return result

	def collect_stats(self):
		# doc = self.player_manager.
		#
		# data = self.fetch_data("/v1/stats/baseball/mlb/teams/", True)
		# result = self.get_mlb_teams(data)
		pass



if __name__ == '__main__':
	api_key = None
	secret = None

	for arg in sys.argv:
		pieces = arg.split('=')
		if arg == 'stats_collector.py':
			pass
		elif pieces[0] == 'api_key':
			api_key = pieces[1]
		elif pieces[0] == 'shared_secret':
			secret = pieces[1]

	sc = StatsCollector(api_key, secret)
	sc.collect_stats()