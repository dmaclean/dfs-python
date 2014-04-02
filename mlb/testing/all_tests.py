import logging
import unittest
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

##################
# Player Manager
##################
suite = unittest.TestLoader().loadTestsFromTestCase(TestPlayerManager)
unittest.TextTestRunner(verbosity=2).run(suite)