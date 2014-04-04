import logging
import unittest
from mlb.testing.test_player_bvp import TestPlayerBvPParser
from mlb.testing.test_player_gamelog_parser import TestPlayerGamelogParser
from mlb.testing.test_player_manager import TestPlayerManager

from test_player_list_parser import TestPlayerListParser
from test_player_season_stats_parser import TestPlayerSeasonStatsParser

logging.basicConfig(level=logging.WARNING)

######################
# Player List Parser
######################
suite = unittest.TestLoader().loadTestsFromTestCase(TestPlayerListParser)
unittest.TextTestRunner(verbosity=2).run(suite)

##############################
# Player Season Stats Parser
##############################
suite = unittest.TestLoader().loadTestsFromTestCase(TestPlayerSeasonStatsParser)
unittest.TextTestRunner(verbosity=2).run(suite)

#########################
# Player Gamelog Parser
#########################
suite = unittest.TestLoader().loadTestsFromTestCase(TestPlayerGamelogParser)
unittest.TextTestRunner(verbosity=2).run(suite)

##################
# Player Manager
##################
suite = unittest.TestLoader().loadTestsFromTestCase(TestPlayerManager)
unittest.TextTestRunner(verbosity=2).run(suite)

############################
# Player Batter vs Pitcher
############################
suite = unittest.TestLoader().loadTestsFromTestCase(TestPlayerBvPParser)
unittest.TextTestRunner(verbosity=2).run(suite)