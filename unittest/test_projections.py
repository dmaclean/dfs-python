import sys
sys.path.append('..')

import sqlite3
import unittest
import BBRTestUtility
import projections

class TestProjections(unittest.TestCase):
	def setUp(self):
		self.testUtil = BBRTestUtility.BBRTestUtility()
		self.projections = projections.Projections(self.testUtil.conn)
		self.testUtil.runSQL()
	
	def tearDown(self):
		self.testUtil.conn.close()
	
	####################################################################################
	# Tests retrieval of player information from the players table, given a player_id.
	####################################################################################
	def test_get_player_info(self):
		values = {
			"id": "macleda01",
			"name": "Dan",
			"position": "G",
			"height": 69,
			"weight": 175,
			"url": "something"
		}
		
		self.testUtil.insert_into_players(values)
		info = self.projections.get_player_info("macleda01")
		
		self.assertTrue(len(info) > 0)
		self.assertTrue(info["id"] == values["id"])

if __name__ == '__main__':
	unittest.main()