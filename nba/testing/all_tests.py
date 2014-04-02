import logging
import unittest
import test_fantasy_point_calculator
import test_import_salaries
import test_projections
import test_basketballreference_team_gamelog_parser
import test_vegas_odds
import test_rg_player_stats
import test_defense_vs_position
import test_injury
import test_calculate_dvp_rank
import test_play_by_play

logging.basicConfig(level=logging.WARNING)

################
# Play by Play
################
suite = unittest.TestLoader().loadTestsFromTestCase(test_play_by_play.TestPlayByPlay)
unittest.TextTestRunner(verbosity=2).run(suite)

######################
# Calculate DvP Rank
######################
suite = unittest.TestLoader().loadTestsFromTestCase(test_calculate_dvp_rank.TestCalculateDvPRank)
unittest.TextTestRunner(verbosity=2).run(suite)

##########################
# FantasyPointCalculator
##########################
suite = unittest.TestLoader().loadTestsFromTestCase(test_fantasy_point_calculator.TestFantasyPointCalculator)
unittest.TextTestRunner(verbosity=2).run(suite)

##################
# SalaryImporter
##################
suite = unittest.TestLoader().loadTestsFromTestCase(test_import_salaries.TestSalaryImporter)
unittest.TextTestRunner(verbosity=2).run(suite)

###############
# Projections
###############
suite = unittest.TestLoader().loadTestsFromTestCase(test_projections.TestProjections)
unittest.TextTestRunner(verbosity=2).run(suite)

########################
# Defense vs. Position
########################
suite = unittest.TestLoader().loadTestsFromTestCase(test_defense_vs_position.TestDefenseVsPosition)
unittest.TextTestRunner(verbosity=2).run(suite)

##########
# Injury
##########
suite = unittest.TestLoader().loadTestsFromTestCase(test_injury.TestInjury)
unittest.TextTestRunner(verbosity=2).run(suite)

#######################
# Team Gamelog Parser
#######################
suite = unittest.TestLoader().loadTestsFromTestCase(test_basketballreference_team_gamelog_parser.TestBasketballReferenceTeamGameLogParser)
unittest.TextTestRunner(verbosity=2).run(suite)

##############
# Vegas Odds
##############
suite = unittest.TestLoader().loadTestsFromTestCase(test_vegas_odds.TestVegasOdds)
unittest.TextTestRunner(verbosity=2).run(suite)

###################
# RG Player Stats
###################
suite = unittest.TestLoader().loadTestsFromTestCase(test_rg_player_stats.TestRGPlayerStats)
unittest.TextTestRunner(verbosity=2).run(suite)