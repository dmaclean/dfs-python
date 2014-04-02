__author__ = 'ap'

import mysql.connector

from shared.dfs_constants import DFSConstants
from projections import Projections
from models.defense_vs_position_manager import DefenseVsPositionManager


cnx = mysql.connector.connect(user='fantasy', password='fantasy', host='localhost', database='basketball_reference')
dvp_manager = DefenseVsPositionManager(cnx=cnx)
projections = Projections(cnx=cnx)

teams = []

cursor = cnx.cursor()
try:
	cursor.execute("select distinct team from game_totals_basic where season = 2013")
	for result in cursor:
		teams.append(result[0])

	for position in ["PG", "SG", "SF", "PF", "C"]:
		ranks = []
		for team in teams:
			dvp = dvp_manager.calculate_defense_vs_position(DFSConstants.FANTASY_POINTS, position, team, 2013, DFSConstants.FAN_DUEL)
			ranks.append((dvp, team))
			# rank = projections.calculate_defense_vs_position_ranking(DFSConstants.FANTASY_POINTS, position, team, 2013, DFSConstants.FAN_DUEL)

		# Sort the results in ascending order (lowest value at element 0).
		ranks.sort()

		print position
		i=1
		for r in ranks:
			print "{} - {} {}".format(i, r[1], r[0])
			i +=1
finally:
	cursor.close()