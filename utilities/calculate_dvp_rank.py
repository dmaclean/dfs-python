import mysql
from dfs_constants import DFSConstants
from models.defense_vs_position_manager import DefenseVsPositionManager


class DvPRankCalculator:
	def __init__(self, cnx=None):
		if not cnx:
			self.cnx = mysql.connector.connect(user='fantasy', password='fantasy', host='localhost', database='basketball_reference')
		else:
			self.cnx = cnx

		self.dvp_manager = DefenseVsPositionManager(cnx=self.cnx)

	def calculate(self, season=None):
		cursor = self.cnx.cursor()

		try:
			metrics = [DFSConstants.FANTASY_POINTS, DFSConstants.POINTS, DFSConstants.FIELD_GOALS,
						DFSConstants.FIELD_GOAL_ATTEMPTS, DFSConstants.THREE_POINT_FIELD_GOALS,
						DFSConstants.THREE_POINT_FIELD_GOAL_ATTEMPTS, DFSConstants.FREE_THROWS, DFSConstants.FREE_THROW_ATTEMPTS,
						DFSConstants.TOTAL_REBOUNDS, DFSConstants.ASSISTS, DFSConstants.STEALS,
						DFSConstants.BLOCKS, DFSConstants.TURNOVERS]
			positions = ["PG", "SG", "SF", "PF", "C"]
			team_dates = {}

			# Get all teams for season
			teams = []
			query = "select distinct team from team_game_totals where season = {}".format(season)

			cursor.execute(query)
			for result in cursor:
				teams.append(result[0])

			# Get all teams that played on each date
			query = "select date, team from team_game_totals where season = {}".format(season)
			cursor.execute(query)
			for result in cursor:
				if result[0] not in team_dates:
					team_dates[result[0]] = [result[1]]
				else:
					team_dates[result[0]].append(result[1])

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
								dvp = self.dvp_manager.calculate_defense_vs_position(metric, position, t, season, site, d)
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

if __name__ == '__main__':
	calculator = DvPRankCalculator()
	calculator.calculate(2013)