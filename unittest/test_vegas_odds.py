import sys
sys.path.append('..')

from datetime import date
import sqlite3
import unittest
import BBRTestUtility
import vegas_odds
from dfs_constants import DFSConstants

class TestVegasOdds(unittest.TestCase):
	def setUp(self):
		self.testUtil = BBRTestUtility.BBRTestUtility()
		self.odds = vegas_odds.VegasOdds(self.testUtil.conn)
		
		self.testUtil.runSQL()
	
	def tearDown(self):
		self.odds = None
	
	def test_process(self):
		self.odds.process(source="file")
		
		# Dallas at Washington
		result = self.testUtil.select_from_vegas({ "date": date.today(), "road_team": "DAL", "home_team": "WAS" })
		self.assertTrue(result[0] == 2.0 and result[1] == -2.0 and result[2] == 204.0 and result[3] == 101.0 and result[4] == 103.0)
		
		# Indiana at Toronto
		result = self.testUtil.select_from_vegas({ "date": date.today(), "road_team": "IND", "home_team": "TOR" })
		self.assertTrue(result[0] == -5.0 and result[1] == 5.0 and result[2] == 191.5 and result[3] == 98.25 and result[4] == 93.25)
		
		# New Orleans at Minnesota
		result = self.testUtil.select_from_vegas({ "date": date.today(), "road_team": "NOP", "home_team": "MIN" })
		self.assertTrue(result[0] == 5.5 and result[1] == -5.5 and result[2] == 211.5 and result[3] == 103 and result[4] == 108.5)
		
		# Philly at Denver
		result = self.testUtil.select_from_vegas({ "date": date.today(), "road_team": "PHI", "home_team": "DEN" })
		self.assertTrue(result[0] == 9.5 and result[1] == -9.5 and result[2] == 212.5 and result[3] == 101.5 and result[4] == 111)
		
		# Charlotte at LA Clippers
		result = self.testUtil.select_from_vegas({ "date": date.today(), "road_team": "CHA", "home_team": "LAC" })
		self.assertTrue(result[0] == 10.5 and result[1] == -10.5 and result[2] == 194 and result[3] == 91.75 and result[4] == 102.25)