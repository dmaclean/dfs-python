__author__ = 'ap'

import mysql.connector
import sys

from models.injury_manager import InjuryManager


class DetermineInjuries():
	"""
	This goes through the game logs and determines which players were injured or otherwise
	missed a game on the schedule.
	"""

	def __init__(self, cnx=None):
		if not cnx:
			self.cnx = mysql.connector.connect(user='fantasy', password='fantasy', host='localhost', database='basketball_reference')
		else:
			self.cnx = cnx
		self.injury_manager = InjuryManager()

	def determine_injuries(self, season):
		"""
		This just runs the calculate_injuries_from_gamelogs function.
		"""
		self.injury_manager.calculate_injuries_from_gamelogs(season=season)

if __name__ == '__main__':
	season = None

	for arg in sys.argv:
		if arg == "determine_injuries.py":
			pass
		else:
			pieces = arg.split("=")
			if pieces[0] == "season":
				season = int(pieces[1])

	if not season:
		print "Usage: python determine_injuries.py season=XXXX"
		exit()

	di = DetermineInjuries()
	di.determine_injuries(season=season)