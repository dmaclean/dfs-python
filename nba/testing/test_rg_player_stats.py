import sys
sys.path.append('..')

import unittest
import BBRTestUtility
from nba.rg_player_stats import RGPlayerStats


class TestRGPlayerStats(unittest.TestCase):
	def setUp(self):
		self.testUtil = BBRTestUtility.BBRTestUtility()
		self.ps = RGPlayerStats(self.testUtil.conn)
		
		self.testUtil.runSQL()
		
		# Initialize the player info map.
		self.player_info = {
			"id": "",
			"name": "",
			"position": "G",
			"rg_position": "",
			"height": 0,
			"weight": 0,
			"url": "something"
		}
	
	def tearDown(self):
		self.ps = None
	
	def test_process(self):
		self.player_info["id"] = "curryst01"
		self.player_info["name"] = "Stephen Curry"
		self.testUtil.insert_into_players(self.player_info)
		
		self.player_info["id"] = "lillada01"
		self.player_info["name"] = "Damian Lillard"
		self.testUtil.insert_into_players(self.player_info)
		
		self.player_info["id"] = "cunninja01"
		self.player_info["name"] = "Jared Cunningham"
		self.testUtil.insert_into_players(self.player_info)
	
		self.ps.process(source="file")
		
		data = self.testUtil.select_from_players("curryst01")
		self.assertTrue(data["rg_position"] == "PG")
		
		data = self.testUtil.select_from_players("lillada01")
		self.assertTrue(data["rg_position"] == "PG")
		
		data = self.testUtil.select_from_players("cunninja01")
		self.assertTrue(data["rg_position"] == "SG")