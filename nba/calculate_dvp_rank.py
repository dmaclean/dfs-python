import logging
import sys
from datetime import date, timedelta

import mysql

from shared.dfs_constants import DFSConstants
from models.defense_vs_position_manager import DefenseVsPositionManager
from models.defense_vs_position import DefenseVsPosition


class DvPRankCalculator:
	def __init__(self, cnx=None):
		if not cnx:
			self.cnx = mysql.connector.connect(user='fantasy', password='fantasy', host='localhost', database='basketball_reference')
		else:
			self.cnx = cnx

		self.dvp_manager = DefenseVsPositionManager(cnx=self.cnx)

		self.ranked_dvps = {}
		self.one_day = timedelta(days=1)

	def calculate(self, season=None, yesterday_only=False):
		# self.get_existing_ranks(season)

		cursor = self.cnx.cursor()

		try:
			metrics = [DFSConstants.FANTASY_POINTS, DFSConstants.POINTS, DFSConstants.FIELD_GOALS,
						DFSConstants.FIELD_GOAL_ATTEMPTS, DFSConstants.THREE_POINT_FIELD_GOALS,
						DFSConstants.THREE_POINT_FIELD_GOAL_ATTEMPTS, DFSConstants.FREE_THROWS, DFSConstants.FREE_THROW_ATTEMPTS,
						DFSConstants.TOTAL_REBOUNDS, DFSConstants.ASSISTS, DFSConstants.STEALS,
						DFSConstants.BLOCKS, DFSConstants.TURNOVERS]
			positions = ["PG", "SG", "SF", "PF", "C"]
			team_dates = []

			# Get all teams for season
			teams = []
			query = "select distinct team from team_game_totals where season = {}".format(season)

			cursor.execute(query)
			for result in cursor:
				teams.append(result[0])

			# Get all teams that played on each date
			if yesterday_only:
				team_dates.append(date.today() - self.one_day)
			else:
				query = "select distinct date from team_game_totals where season = {} order by date".format(season)
				cursor.execute(query)
				for result in cursor:
					team_dates.append(result[0])

			for metric in metrics:
				for position in positions:
					sites = [None]
					if metric == DFSConstants.FANTASY_POINTS:
						sites = [DFSConstants.DRAFT_DAY, DFSConstants.DRAFT_KINGS, DFSConstants.FAN_DUEL, DFSConstants.STAR_STREET]
					for site in sites:
						for d in team_dates:
							ranks = []
							dvp_val_map = {}    # Associates the DvP value with the actual DefenseVsPosition object.
							for t in teams:
								logging.info("Processing {}/{}/{}/{}/{}".format(metric, position, site, d, t))
								dvp = self.dvp_manager.calculate_defense_vs_position(metric, position, t, season, site, d)
								if dvp:
									ranks.append((dvp.value, t))
									dvp_val_map["{}_{}".format(dvp.value, t)] = dvp

							# Sort the results in ascending order (lowest value at element 0).
							ranks.sort()

							# Put the results in the cache.  We only want the ranking, so we're going to
							# put the index i in the cache instead of the actual value.
							i = 1
							for r in ranks:
								dvp = dvp_val_map["{}_{}".format(r[0], r[1])]
								dvp.rank = i
								self.dvp_manager.update(dvp)
								i += 1
		finally:
			cursor.close()

	def get_existing_ranks(self, season):
		"""
		Figure out which DvP entries don't have ranks.  It'll take forever to process
		all of them, even for a single season.
		"""
		all_dvps = self.dvp_manager.get(DefenseVsPosition(season=season))

		for dvp in all_dvps:
			if dvp.rank:
				self.ranked_dvps["{}_{}_{}_{}_{}_{}".format(dvp.stat, dvp.position, dvp.site, dvp.team, dvp.season, dvp.date)]

if __name__ == '__main__':
	logging.basicConfig(level=logging.INFO)

	season = date.today().year
	yesterday_only = False
	for arg in sys.argv:
		if arg == "calculate_dvp_rank.py":
			pass
		else:
			pieces = arg.split("=")
			if pieces[0] == "season":
				season = int(pieces[1])
			elif pieces[0] == "yesterday_only":
				yesterday_only = pieces[1] == "true"

	calculator = DvPRankCalculator()
	calculator.calculate(season, yesterday_only)