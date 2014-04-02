import sys
sys.path.append('..')

from datetime import date
import unittest
import BBRTestUtility
from nba.import_salaries import SalaryImporter
from shared.dfs_constants import DFSConstants

class TestSalaryImporter(unittest.TestCase):
	def setUp(self):
		self.testUtil = BBRTestUtility.BBRTestUtility()
		self.salary_importer = SalaryImporter(self.testUtil.conn)
		self.testUtil.runSQL()
		
		# Initialize the player info map.
		self.player_info = {
			"id": "",
			"name": "Test",
			"position": "G",
			"height": 0,
			"weight": 0,
			"url": "something"
		}
		
		# Initialize the player game totals map.
		self.game_totals_basic_info = {
			"player_id": "test",
			"season": date.today().year,
			"game_number": 0,
			"date": date.today(),
			"age": 0,
			"team": "BOS",
			"home": True,
			"opponent": "BOS",
			"result": "",
			"games_started": 0,
			"minutes_played": 0,
			"field_goals": 0,
			"field_goal_attempts": 0,
			"field_goal_pct": 0,
			"three_point_field_goals": 0,
			"three_point_field_goal_attempts": 0,
			"three_point_field_goal_pct": 0,
			"free_throws": 0,
			"free_throw_attempts": 0,
			"free_throw_pct": 0,
			"offensive_rebounds": 0,
			"defensive_rebounds": 0,
			"total_rebounds": 0,
			"assists": 0,
			"steals": 0,
			"blocks": 0,
			"turnovers": 0,
			"personal_fouls": 0,
			"points": 0,
			"game_score": 0,
			"plus_minus": 0
		}
		
		self.game_totals_advanced_info = {
			"player_id": "",
			"game_number": 0,
			"season": date.today().year,
			"date": date.today(),
			"age": 0,
			"team": "BOS",
			"home": True,
			"opponent": "NYK",
			"result": "",
			"games_started": 0,
			"minutes_played": 0,
			"true_shooting_pct": 0,
			"effective_field_goal_pct": 0,
			"offensive_rebound_pct": 0,
			"defensive_rebound_pct": 0,
			"total_rebound_pct": 0,
			"assist_pct": 0,
			"steal_pct": 0,
			"block_pct": 0,
			"turnover_pct": 0,
			"usage_pct": 0,
			"offensive_rating": 0,
			"defensive_rating": 0,
			"game_score": 0
		}
		
		# Initialize the team game totals map.
		self.team_game_totals_info = {
			"team": "",
			"season": date.today().year,
			"game": 0,
			"date": date.today(),
			"home": True,
			"opponent": "",
			"result": "",
			"minutes_played": 240,
			"field_goals": 0,
			"field_goal_attempts": 0,
			"three_point_field_goals": 0,
			"three_point_field_goal_attempts": 0,
			"free_throws": 0,
			"free_throw_attempts": 0,
			"offensive_rebounds": 0,
			"total_rebounds": 0,
			"assists": 0,
			"steals": 0,
			"blocks": 0,
			"turnovers": 0,
			"personal_fouls": 0,
			"points": 0,
			"opp_field_goals": 0,
			"opp_field_goal_attempts": 0,
			"opp_three_point_field_goals": 0,
			"opp_three_point_field_goal_attempts": 0,
			"opp_free_throws": 0,
			"opp_free_throw_attempts": 0,
			"opp_offensive_rebounds": 0,
			"opp_total_rebounds": 0,
			"opp_assists": 0,
			"opp_steals": 0,
			"opp_blocks": 0,
			"opp_turnovers": 0,
			"opp_personal_fouls": 0,
			"opp_points": 0
		}
		
		self.schedule_info = {
			"date": date.today(),
			"season": date.today().year,
			"visitor": "",
			"home": ""
		}
		
		self.dfs_site_positions_info = {
			"player_id": "",
			"site": "",
			"position": ""
		}
		
		self.player_name_mapping_info = {
			"bbr_name": "",
			"site_name": "",
			"site": ""
		}
	
	def tearDown(self):
		self.testUtil.conn.close()
		
		self.player_info = {}
	
	def test_insert_or_update_positions(self):
		self.salary_importer.insert_or_update_positions("macleda01", "DRAFT_KINGS", "PG")
		self.assertTrue(self.testUtil.select_from_dfs_site_positions("macleda01", "DRAFT_KINGS") == "PG")
		
		self.salary_importer.insert_or_update_positions("macleda01", "DRAFT_KINGS", "SF")
		self.assertTrue(self.testUtil.select_from_dfs_site_positions("macleda01", "DRAFT_KINGS") == "SF")
		
	def test_process_line_draft_day(self):
		self.salary_importer.site = "DRAFT_DAY"
		self.salary_importer.process_line("C,Elton Brand,Hawks,Kings,5000,9.2")
		self.salary_importer.process_line("PF,Elton Brand,Hawks,Kings,5000,9.2")
		
		self.assertTrue(self.salary_importer.salaries["Elton Brand"] == 5000)
		self.assertTrue(self.salary_importer.positions["Elton Brand"] == "C/PF")
	
	def test_process_line_draft_kings(self):
		self.salary_importer.site = "DRAFT_KINGS"
		self.salary_importer.process_line("\"PF/C\",\"Kevin Love\",10800,\"Por@Min 08:00PM ET\",51.802")
		
		self.assertTrue(self.salary_importer.salaries["Kevin Love"] == 10800)
		self.assertTrue(self.salary_importer.positions["Kevin Love"] == "PF/C")
	
	def test_process_line_star_street(self):
		self.salary_importer.site = "STAR_STREET"
		self.salary_importer.process_line("PF-C,Kevin Love,MIN,MIN vs POR, 8:00 PM,47.9,18000,\"\",")
		
		self.assertTrue(self.salary_importer.salaries["Kevin Love"] == 18000)
		self.assertTrue(self.salary_importer.positions["Kevin Love"] == "PF/C")

	def test_process_line_fanduel(self):
		self.salary_importer.site = "FAN_DUEL"
		self.salary_importer.process_line("Kevin Love,PF,11700")
		
		self.assertTrue(self.salary_importer.salaries["Kevin Love"] == 11700)
		self.assertTrue(self.salary_importer.positions["Kevin Love"] == "PF")
	
	def test_process_line_fanduel_changed_name(self):
		self.player_name_mapping_info["bbr_name"] = "Tim Hardaway"
		self.player_name_mapping_info["site_name"] = "Tim Hardaway Jr."
		self.player_name_mapping_info["site"] = DFSConstants.FAN_DUEL
		self.testUtil.insert_into_player_name_mapping(self.player_name_mapping_info)
		
		self.salary_importer.site = DFSConstants.FAN_DUEL
		self.salary_importer.process_line("Tim Hardaway Jr.,PF,11700")
		
		self.assertTrue(self.salary_importer.salaries["Tim Hardaway"] == 11700)
		self.assertTrue(self.salary_importer.positions["Tim Hardaway"] == "PF")
	
	def test_get_name_for_site(self):
		self.player_name_mapping_info["bbr_name"] = "Tim Hardaway"
		self.player_name_mapping_info["site_name"] = "Tim Hardaway Jr."
		self.player_name_mapping_info["site"] = DFSConstants.DRAFT_KINGS
		self.testUtil.insert_into_player_name_mapping(self.player_name_mapping_info)
	
		self.player_name_mapping_info["bbr_name"] = "Tim Hardaway"
		self.player_name_mapping_info["site_name"] = "Tim Hardaway Jr"
		self.player_name_mapping_info["site"] = DFSConstants.STAR_STREET
		self.testUtil.insert_into_player_name_mapping(self.player_name_mapping_info)
		
		name = self.salary_importer.get_name_for_site("Tim Hardaway Jr.", DFSConstants.DRAFT_KINGS)
		self.assertTrue(name == "Tim Hardaway")
		
		name = self.salary_importer.get_name_for_site("Tim Hardaway Jr", DFSConstants.STAR_STREET)
		self.assertTrue(name == "Tim Hardaway")
	
	def test_get_name_for_site_no_hit(self):
		self.player_name_mapping_info["bbr_name"] = "Tim Hardaway"
		self.player_name_mapping_info["site_name"] = "Tim Hardaway Jr."
		self.player_name_mapping_info["site"] = DFSConstants.DRAFT_KINGS
		self.testUtil.insert_into_player_name_mapping(self.player_name_mapping_info)
	
		self.player_name_mapping_info["bbr_name"] = "Tim Hardaway"
		self.player_name_mapping_info["site_name"] = "Tim Hardaway Jr"
		self.player_name_mapping_info["site"] = DFSConstants.STAR_STREET
		self.testUtil.insert_into_player_name_mapping(self.player_name_mapping_info)
		
		name = self.salary_importer.get_name_for_site("Kevin Love", DFSConstants.DRAFT_KINGS)
		self.assertTrue(name == "Kevin Love")
	
if __name__ == '__main__':
	unittest.main()