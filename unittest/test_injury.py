from datetime import date
from unittest import TestCase
from BBRTestUtility import BBRTestUtility
from models.injury import Injury
from models.injury_manager import InjuryManager

class TestInjury(TestCase):
	def setUp(self):
		self.testUtil = BBRTestUtility()
		self.injury_manager = InjuryManager(cnx=self.testUtil.conn)
		self.testUtil.runSQL()

		self.injury_info = {
			"player_id": "",
		    "injury_date": date.today(),
		    "return_date": date.today(),
		    "details": ""
		}

	def test_db_operations(self):
		injury = Injury(player_id="dan", injury_date=date(2014,1,1), return_date=date(2014,1,10), details="broken leg")

		self.assertTrue(not self.injury_manager.exists(injury))

		self.injury_manager.insert(injury)

		self.assertTrue(self.injury_manager.exists(injury))

		injuries = self.injury_manager.get(injury)
		self.assertTrue(len(injuries) == 1)
		self.assertTrue(injuries[0].player_id == "dan" and injuries[0].injury_date == "2014-01-01" and
		                injuries[0].return_date == "2014-01-10" and injuries[0].details == "broken leg")

		injury2 = injuries[0]
		injury2.return_date = date(2014,1,2)

		self.injury_manager.update(injury2)
		injuries = self.injury_manager.get(injury2)

		self.assertTrue(len(injuries) == 1 and injuries[0].return_date == "2014-01-02")

		# Test get with no id
		injury_no_id = Injury(player_id="dan", injury_date=date(2014,1,1), return_date=date(2014,1,2), details="broken leg")
		injuries = self.injury_manager.get(injury_no_id)

		self.assertTrue(len(injuries) == 1 and injuries[0].return_date == "2014-01-02")

		# Test for currently-injured
		new_injury = Injury(player_id="later injury", injury_date=date(2014,1,10), return_date=date(2014,1,14), details="sick")
		self.injury_manager.insert(new_injury)
		injuries = self.injury_manager.get_currently_injured_players(date=date(2014,1,12))

		self.assertTrue(len(injuries) == 1)
		self.assertTrue(injuries[new_injury.player_id].player_id == "later injury" and
		                injuries[new_injury.player_id].injury_date == "2014-01-10" and
		                injuries[new_injury.player_id].return_date == "2014-01-14" and
		                injuries[new_injury.player_id].details == "sick")