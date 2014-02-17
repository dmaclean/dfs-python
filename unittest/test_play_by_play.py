import unittest
import BBRTestUtility

from models.play_by_play_manager import PlayByPlayManager
from models.play_by_play import PlayByPlay


class TestPlayByPlay(unittest.TestCase):
	def setUp(self):
		self.test_util = BBRTestUtility.BBRTestUtility()
		self.pbp_manager = PlayByPlayManager(cnx=self.test_util.conn)
		self.test_util.runSQL()

	def tearDown(self):
		self.test_util.conn.close()

	def test_create_pbp_instance_jump_ball(self):
		pbp = self.pbp_manager.create_pbp_instance(['12:00.0', 'Jump ball: <a href="/players/d/drumman01.html">A. Drummond</a> vs. <a href="/players/d/duncati01.html">T. Duncan</a> (<a href="/players/p/parketo01.html">T. Parker</a> gains possession)'])

		self.assertTrue(pbp.minutes == 12)
		self.assertTrue(pbp.seconds == 0.0)
		self.assertTrue(pbp.play_type == PlayByPlay.JUMP_BALL)
		self.assertTrue(pbp.players[0] == 'drumman01')
		self.assertTrue(pbp.players[1] == 'duncati01')
		self.assertTrue(pbp.players[2] == 'parketo01')

	def test_create_pbp_instance_visitor_missed_2pt_shot_with_block(self):
		pbp = self.pbp_manager.create_pbp_instance(['11:44.0', '<a href="/players/b/baynear01.html">A. Baynes</a> misses 2-pt shot from 3 ft (block by <a href="/players/d/drumman01.html">A. Drummond</a>)', '', '0-0', '', ''])

		self.assertTrue(pbp.minutes == 11)
		self.assertTrue(pbp.seconds == 44.0)
		self.assertTrue(pbp.play_type == PlayByPlay.SHOT)
		self.assertTrue(pbp.secondary_play_type == "block")
		self.assertTrue(not pbp.shot_made)
		self.assertTrue(pbp.point_value == 2)
		self.assertTrue(pbp.shot_distance == 3)
		self.assertTrue(pbp.home_score == 0)
		self.assertTrue(pbp.visitor_score == 0)
		self.assertTrue(len(pbp.players) == 2)
		self.assertTrue(pbp.players[0] == 'baynear01')
		self.assertTrue(pbp.players[1] == 'drumman01')

	def test_create_pbp_instance_visitor_made_2pt_shot_with_assist(self):
		pbp = self.pbp_manager.create_pbp_instance(['11:16.0', '<a href="/players/d/decolna01.html">N. De Colo</a> makes 2-pt shot from 1 ft (assist by <a href="/players/d/duncati01.html">T. Duncan</a>)', '+2', '2-0', '', ''])

		self.assertTrue(pbp.minutes == 11)
		self.assertTrue(pbp.seconds == 16.0)
		self.assertTrue(pbp.play_type == PlayByPlay.SHOT)
		self.assertTrue(pbp.secondary_play_type == "assist")
		self.assertTrue(pbp.shot_made)
		self.assertTrue(pbp.point_value == 2)
		self.assertTrue(pbp.shot_distance == 1)
		self.assertTrue(pbp.home_score == 0)
		self.assertTrue(pbp.visitor_score == 2)
		self.assertTrue(len(pbp.players) == 2)
		self.assertTrue(pbp.players[0] == 'decolna01')
		self.assertTrue(pbp.players[1] == 'duncati01')

	def test_create_pbp_instance_home_missed_2pt_shot(self):
		pbp = self.pbp_manager.create_pbp_instance(['11:30.0', '', '', '0-0', '', '<td class="background_white"><a href="/players/j/jennibr01.html">B. Jennings</a> misses 3-pt shot from 25 ft</td>'])

		self.assertTrue(pbp.minutes == 11)
		self.assertTrue(pbp.seconds == 30.0)
		self.assertTrue(pbp.play_type == PlayByPlay.SHOT)
		self.assertTrue(pbp.secondary_play_type is None)
		self.assertTrue(pbp.point_value == 3)
		self.assertTrue(not pbp.shot_made)
		self.assertTrue(pbp.home_score == 0)
		self.assertTrue(pbp.visitor_score == 0)
		self.assertTrue(pbp.shot_distance == 25)
		self.assertTrue(len(pbp.players) == 1)
		self.assertTrue(pbp.players[0] == 'jennibr01')

	def test_create_pbp_instance_home_made_2pt_shot(self):
		pbp = self.pbp_manager.create_pbp_instance(['9:35.0', '', '', '4-7', '+2', '<a href="/players/j/jennibr01.html">B. Jennings</a> makes 2-pt shot from 1 ft'])

		self.assertTrue(pbp.minutes == 9)
		self.assertTrue(pbp.seconds == 35.0)
		self.assertTrue(pbp.play_type == PlayByPlay.SHOT)
		self.assertTrue(pbp.secondary_play_type is None)
		self.assertTrue(pbp.point_value == 2)
		self.assertTrue(pbp.shot_made)
		self.assertTrue(pbp.home_score == 7)
		self.assertTrue(pbp.visitor_score == 4)
		self.assertTrue(pbp.shot_distance == 1)
		self.assertTrue(len(pbp.players) == 1)
		self.assertTrue(pbp.players[0] == 'jennibr01')

	def test_create_pbp_instance_visitor_missed_2pt_shot(self):
		pbp = self.pbp_manager.create_pbp_instance(['9:14.0', '<a href="/players/d/duncati01.html">T. Duncan</a> misses 2-pt shot from 18 ft', '', '4-7', '', ''])

		self.assertTrue(pbp.minutes == 9)
		self.assertTrue(pbp.seconds == 14.0)
		self.assertTrue(pbp.play_type == PlayByPlay.SHOT)
		self.assertTrue(pbp.secondary_play_type is None)
		self.assertTrue(pbp.point_value == 2)
		self.assertTrue(not pbp.shot_made)
		self.assertTrue(pbp.home_score == 7)
		self.assertTrue(pbp.visitor_score == 4)
		self.assertTrue(pbp.shot_distance == 18)
		self.assertTrue(len(pbp.players) == 1)
		self.assertTrue(pbp.players[0] == 'duncati01')

	def test_create_pbp_instance_visitor_made_2pt_shot(self):
		pbp = self.pbp_manager.create_pbp_instance(['7:28.0', '<a href="/players/p/parketo01.html">T. Parker</a> makes 2-pt shot from 19 ft', '+2', '6-7', '', ''])

		self.assertTrue(pbp.minutes == 7)
		self.assertTrue(pbp.seconds == 28.0)
		self.assertTrue(pbp.play_type == PlayByPlay.SHOT)
		self.assertTrue(pbp.secondary_play_type is None)
		self.assertTrue(pbp.point_value == 2)
		self.assertTrue(pbp.shot_made)
		self.assertTrue(pbp.home_score == 7)
		self.assertTrue(pbp.visitor_score == 6)
		self.assertTrue(pbp.shot_distance == 19)
		self.assertTrue(len(pbp.players) == 1)
		self.assertTrue(pbp.players[0] == 'parketo01')

	def test_create_pbp_instance_home_made_free_throw_1_2(self):
		pbp = self.pbp_manager.create_pbp_instance(['10:01.0', '', '', '4-4', '+1', '<a href="/players/s/smithjo03.html">J. Smith</a> makes free throw 1 of 2'])

		self.assertTrue(pbp.minutes == 10)
		self.assertTrue(pbp.seconds == 01.0)
		self.assertTrue(pbp.play_type == PlayByPlay.FREE_THROW)
		self.assertTrue(pbp.secondary_play_type is None)
		self.assertTrue(pbp.point_value == 1)
		self.assertTrue(pbp.shot_made)
		self.assertTrue(pbp.home_score == 4)
		self.assertTrue(pbp.visitor_score == 4)
		self.assertTrue(pbp.shot_distance == 15)
		self.assertTrue(len(pbp.players) == 1)
		self.assertTrue(pbp.players[0] == 'smithjo03')

	def test_create_pbp_instance_home_made_free_throw_2_2(self):
		pbp = self.pbp_manager.create_pbp_instance(['10:01.0', '', '', '4-5', '+1', '<a href="/players/s/smithjo03.html">J. Smith</a> makes free throw 2 of 2'])

		self.assertTrue(pbp.minutes == 10)
		self.assertTrue(pbp.seconds == 01.0)
		self.assertTrue(pbp.play_type == PlayByPlay.FREE_THROW)
		self.assertTrue(pbp.secondary_play_type is None)
		self.assertTrue(pbp.point_value == 1)
		self.assertTrue(pbp.shot_made)
		self.assertTrue(pbp.home_score == 5)
		self.assertTrue(pbp.visitor_score == 4)
		self.assertTrue(pbp.shot_distance == 15)
		self.assertTrue(len(pbp.players) == 1)
		self.assertTrue(pbp.players[0] == 'smithjo03')

	def test_create_pbp_instance_home_missed_free_throw_1_2(self):
		pbp = self.pbp_manager.create_pbp_instance(['11:07.0', '', '', '24-26', '', '<a href="/players/s/stuckro01.html">R. Stuckey</a> misses free throw 1 of 2'])

		self.assertTrue(pbp.minutes == 11)
		self.assertTrue(pbp.seconds == 07.0)
		self.assertTrue(pbp.play_type == PlayByPlay.FREE_THROW)
		self.assertTrue(pbp.secondary_play_type is None)
		self.assertTrue(pbp.point_value == 1)
		self.assertTrue(not pbp.shot_made)
		self.assertTrue(pbp.home_score == 26)
		self.assertTrue(pbp.visitor_score == 24)
		self.assertTrue(pbp.shot_distance == 15)
		self.assertTrue(len(pbp.players) == 1)
		self.assertTrue(pbp.players[0] == 'stuckro01')

	def test_create_pbp_instance_home_missed_free_throw_2_2(self):
		pbp = self.pbp_manager.create_pbp_instance(['5:40.0', '', '', '8-12', '', '<a href="/players/m/monrogr01.html">G. Monroe</a> misses free throw 2 of 2'])

		self.assertTrue(pbp.minutes == 5)
		self.assertTrue(pbp.seconds == 40.0)
		self.assertTrue(pbp.play_type == PlayByPlay.FREE_THROW)
		self.assertTrue(pbp.secondary_play_type is None)
		self.assertTrue(pbp.point_value == 1)
		self.assertTrue(not pbp.shot_made)
		self.assertTrue(pbp.home_score == 12)
		self.assertTrue(pbp.visitor_score == 8)
		self.assertTrue(pbp.shot_distance == 15)
		self.assertTrue(len(pbp.players) == 1)
		self.assertTrue(pbp.players[0] == 'monrogr01')

	def test_create_pbp_instance_home_made_free_throw_1_1(self):
		pbp = self.pbp_manager.create_pbp_instance(['10:01.0', '', '', '4-5', '+1', '<a href="/players/s/smithjo03.html">J. Smith</a> makes free throw 1 of 1'])

		self.assertTrue(pbp.minutes == 10)
		self.assertTrue(pbp.seconds == 01.0)
		self.assertTrue(pbp.play_type == PlayByPlay.FREE_THROW)
		self.assertTrue(pbp.secondary_play_type is None)
		self.assertTrue(pbp.point_value == 1)
		self.assertTrue(pbp.shot_made)
		self.assertTrue(pbp.home_score == 5)
		self.assertTrue(pbp.visitor_score == 4)
		self.assertTrue(pbp.shot_distance == 15)
		self.assertTrue(len(pbp.players) == 1)
		self.assertTrue(pbp.players[0] == 'smithjo03')

	def test_create_pbp_instance_home_missed_free_throw_1_1(self):
		pbp = self.pbp_manager.create_pbp_instance(['11:07.0', '', '', '24-26', '', '<a href="/players/s/stuckro01.html">R. Stuckey</a> misses free throw 1 of 1'])

		self.assertTrue(pbp.minutes == 11)
		self.assertTrue(pbp.seconds == 07.0)
		self.assertTrue(pbp.play_type == PlayByPlay.FREE_THROW)
		self.assertTrue(pbp.secondary_play_type is None)
		self.assertTrue(pbp.point_value == 1)
		self.assertTrue(not pbp.shot_made)
		self.assertTrue(pbp.home_score == 26)
		self.assertTrue(pbp.visitor_score == 24)
		self.assertTrue(pbp.shot_distance == 15)
		self.assertTrue(len(pbp.players) == 1)
		self.assertTrue(pbp.players[0] == 'stuckro01')

	def test_create_pbp_instance_visitor_made_free_throw_1_2(self):
		pbp = self.pbp_manager.create_pbp_instance(['2:33.0', '<a href="/players/j/josepco01.html">C. Joseph</a> makes free throw 1 of 2', '+1', '63-84', '', ''])

		self.assertTrue(pbp.minutes == 2)
		self.assertTrue(pbp.seconds == 33.0)
		self.assertTrue(pbp.play_type == PlayByPlay.FREE_THROW)
		self.assertTrue(pbp.secondary_play_type is None)
		self.assertTrue(pbp.point_value == 1)
		self.assertTrue(pbp.shot_made)
		self.assertTrue(pbp.home_score == 84)
		self.assertTrue(pbp.visitor_score == 63)
		self.assertTrue(pbp.shot_distance == 15)
		self.assertTrue(len(pbp.players) == 1)
		self.assertTrue(pbp.players[0] == 'josepco01')

	def test_create_pbp_instance_visitor_made_free_throw_2_2(self):
		pbp = self.pbp_manager.create_pbp_instance(['5:25.0', '<a href="/players/d/duncati01.html">T. Duncan</a> makes free throw 2 of 2', '+1', '36-39', '', ''])

		self.assertTrue(pbp.minutes == 5)
		self.assertTrue(pbp.seconds == 25.0)
		self.assertTrue(pbp.play_type == PlayByPlay.FREE_THROW)
		self.assertTrue(pbp.secondary_play_type is None)
		self.assertTrue(pbp.point_value == 1)
		self.assertTrue(pbp.shot_made)
		self.assertTrue(pbp.home_score == 39)
		self.assertTrue(pbp.visitor_score == 36)
		self.assertTrue(pbp.shot_distance == 15)
		self.assertTrue(len(pbp.players) == 1)
		self.assertTrue(pbp.players[0] == 'duncati01')

	def test_create_pbp_instance_visitor_missed_free_throw_1_2(self):
		pbp = self.pbp_manager.create_pbp_instance(['5:25.0', '<a href="/players/d/duncati01.html">T. Duncan</a> misses free throw 1 of 2<', '', '35-39', '', ''])

		self.assertTrue(pbp.minutes == 5)
		self.assertTrue(pbp.seconds == 25.0)
		self.assertTrue(pbp.play_type == PlayByPlay.FREE_THROW)
		self.assertTrue(pbp.secondary_play_type is None)
		self.assertTrue(pbp.point_value == 1)
		self.assertTrue(not pbp.shot_made)
		self.assertTrue(pbp.home_score == 39)
		self.assertTrue(pbp.visitor_score == 35)
		self.assertTrue(pbp.shot_distance == 15)
		self.assertTrue(len(pbp.players) == 1)
		self.assertTrue(pbp.players[0] == 'duncati01')

	def test_create_pbp_instance_visitor_missed_free_throw_2_2(self):
		pbp = self.pbp_manager.create_pbp_instance(['2:33.0', '<a href="/players/j/josepco01.html">C. Joseph</a> misses free throw 2 of 2', '', '63-84', '', ''])

		self.assertTrue(pbp.minutes == 2)
		self.assertTrue(pbp.seconds == 33.0)
		self.assertTrue(pbp.play_type == PlayByPlay.FREE_THROW)
		self.assertTrue(pbp.secondary_play_type is None)
		self.assertTrue(pbp.point_value == 1)
		self.assertTrue(not pbp.shot_made)
		self.assertTrue(pbp.home_score == 84)
		self.assertTrue(pbp.visitor_score == 63)
		self.assertTrue(pbp.shot_distance == 15)
		self.assertTrue(len(pbp.players) == 1)
		self.assertTrue(pbp.players[0] == 'josepco01')

	def test_create_pbp_instance_visitor_made_free_throw_1_1(self):
		pbp = self.pbp_manager.create_pbp_instance(['5:25.0', '<a href="/players/s/smithjo03.html">J. Smith</a> makes free throw 1 of 1', '+1', '41-42', '', ''])

		self.assertTrue(pbp.minutes == 5)
		self.assertTrue(pbp.seconds == 25.0)
		self.assertTrue(pbp.play_type == PlayByPlay.FREE_THROW)
		self.assertTrue(pbp.secondary_play_type is None)
		self.assertTrue(pbp.point_value == 1)
		self.assertTrue(pbp.shot_made)
		self.assertTrue(pbp.home_score == 42)
		self.assertTrue(pbp.visitor_score == 41)
		self.assertTrue(pbp.shot_distance == 15)
		self.assertTrue(len(pbp.players) == 1)
		self.assertTrue(pbp.players[0] == 'smithjo03')

	def test_create_pbp_instance_visitor_missed_free_throw_1_1(self):
		pbp = self.pbp_manager.create_pbp_instance(['4:00.0', '<a href="/players/s/smithjo03.html">J. Smith</a> misses free throw 1 of 1', '', '41-42', '', ''])

		self.assertTrue(pbp.minutes == 4)
		self.assertTrue(pbp.seconds == 00.0)
		self.assertTrue(pbp.play_type == PlayByPlay.FREE_THROW)
		self.assertTrue(pbp.secondary_play_type is None)
		self.assertTrue(pbp.point_value == 1)
		self.assertTrue(not pbp.shot_made)
		self.assertTrue(pbp.home_score == 42)
		self.assertTrue(pbp.visitor_score == 41)
		self.assertTrue(pbp.shot_distance == 15)
		self.assertTrue(len(pbp.players) == 1)
		self.assertTrue(pbp.players[0] == 'smithjo03')

	def test_create_pbp_instance_home_offensive_rebound_player(self):
		pbp = self.pbp_manager.create_pbp_instance(['7:06.0', '', '', '6-7', '', 'Offensive rebound by <a href="/players/d/drumman01.html">A. Drummond</a>'])

		self.assertTrue(pbp.minutes == 7)
		self.assertTrue(pbp.seconds == 06.0)
		self.assertTrue(pbp.play_type == PlayByPlay.REBOUND)
		self.assertTrue(pbp.detail == PlayByPlay.REBOUND_OFFENSIVE)
		self.assertTrue(pbp.secondary_play_type is None)
		self.assertTrue(pbp.point_value == 0)
		self.assertTrue(pbp.shot_made is None)
		self.assertTrue(pbp.home_score == 7)
		self.assertTrue(pbp.visitor_score == 6)
		self.assertTrue(pbp.shot_distance is None)
		self.assertTrue(len(pbp.players) == 1)
		self.assertTrue(pbp.players[0] == 'drumman01')

	def test_create_pbp_instance_home_offensive_rebound_team(self):
		pbp = self.pbp_manager.create_pbp_instance(['4:05.0', '', '', '12-14', '', 'Offensive rebound by Team'])

		self.assertTrue(pbp.minutes == 4)
		self.assertTrue(pbp.seconds == 05.0)
		self.assertTrue(pbp.play_type == PlayByPlay.REBOUND)
		self.assertTrue(pbp.detail == PlayByPlay.REBOUND_OFFENSIVE)
		self.assertTrue(pbp.secondary_play_type is None)
		self.assertTrue(pbp.point_value == 0)
		self.assertTrue(pbp.shot_made is None)
		self.assertTrue(pbp.home_score == 14)
		self.assertTrue(pbp.visitor_score == 12)
		self.assertTrue(pbp.shot_distance is None)
		self.assertTrue(len(pbp.players) == 0)

	def test_create_pbp_instance_home_defensive_rebound_player(self):
		pbp = self.pbp_manager.create_pbp_instance(['10:39.0', '', '', '2-0', '', 'Defensive rebound by <a href="/players/d/drumman01.html">A. Drummond</a>'])

		self.assertTrue(pbp.minutes == 10)
		self.assertTrue(pbp.seconds == 39.0)
		self.assertTrue(pbp.play_type == PlayByPlay.REBOUND)
		self.assertTrue(pbp.detail == PlayByPlay.REBOUND_DEFENSIVE)
		self.assertTrue(pbp.secondary_play_type is None)
		self.assertTrue(pbp.point_value == 0)
		self.assertTrue(pbp.shot_made is None)
		self.assertTrue(pbp.home_score == 0)
		self.assertTrue(pbp.visitor_score == 2)
		self.assertTrue(pbp.shot_distance is None)
		self.assertTrue(len(pbp.players) == 1)
		self.assertTrue(pbp.players[0] == 'drumman01')

	def test_create_pbp_instance_home_defensive_rebound_team(self):
		pbp = self.pbp_manager.create_pbp_instance(['11:44.0', '', '', '0-0', '', 'Defensive rebound by Team'])

		self.assertTrue(pbp.minutes == 11)
		self.assertTrue(pbp.seconds == 44.0)
		self.assertTrue(pbp.play_type == PlayByPlay.REBOUND)
		self.assertTrue(pbp.detail == PlayByPlay.REBOUND_DEFENSIVE)
		self.assertTrue(pbp.secondary_play_type is None)
		self.assertTrue(pbp.point_value == 0)
		self.assertTrue(pbp.shot_made is None)
		self.assertTrue(pbp.home_score == 0)
		self.assertTrue(pbp.visitor_score == 0)
		self.assertTrue(pbp.shot_distance is None)
		self.assertTrue(len(pbp.players) == 0)

	def test_create_pbp_instance_visitor_offensive_rebound_player(self):
		pbp = self.pbp_manager.create_pbp_instance(['8:28.0', 'Offensive rebound by <a href="/players/g/greenda02.html">D. Green</a>', '', '4-7', '', ''])

		self.assertTrue(pbp.minutes == 8)
		self.assertTrue(pbp.seconds == 28.0)
		self.assertTrue(pbp.play_type == PlayByPlay.REBOUND)
		self.assertTrue(pbp.detail == PlayByPlay.REBOUND_OFFENSIVE)
		self.assertTrue(pbp.secondary_play_type is None)
		self.assertTrue(pbp.point_value == 0)
		self.assertTrue(pbp.shot_made is None)
		self.assertTrue(pbp.home_score == 7)
		self.assertTrue(pbp.visitor_score == 4)
		self.assertTrue(pbp.shot_distance is None)
		self.assertTrue(len(pbp.players) == 1)
		self.assertTrue(pbp.players[0] == 'greenda02')

	def test_create_pbp_instance_visitor_offensive_rebound_team(self):
		pbp = self.pbp_manager.create_pbp_instance(['0:00.0', 'Offensive rebound by Team', '', '24-25', '', ''])

		self.assertTrue(pbp.minutes == 0)
		self.assertTrue(pbp.seconds == 00.0)
		self.assertTrue(pbp.play_type == PlayByPlay.REBOUND)
		self.assertTrue(pbp.detail == PlayByPlay.REBOUND_OFFENSIVE)
		self.assertTrue(pbp.secondary_play_type is None)
		self.assertTrue(pbp.point_value == 0)
		self.assertTrue(pbp.shot_made is None)
		self.assertTrue(pbp.home_score == 25)
		self.assertTrue(pbp.visitor_score == 24)
		self.assertTrue(pbp.shot_distance is None)
		self.assertTrue(len(pbp.players) == 0)

	def test_create_pbp_instance_visitor_defensive_rebound_player(self):
		pbp = self.pbp_manager.create_pbp_instance(['11:29.0', 'Defensive rebound by <a href="/players/d/duncati01.html">T. Duncan</a>', '', '0-0', '', ''])

		self.assertTrue(pbp.minutes == 11)
		self.assertTrue(pbp.seconds == 29.0)
		self.assertTrue(pbp.play_type == PlayByPlay.REBOUND)
		self.assertTrue(pbp.detail == PlayByPlay.REBOUND_DEFENSIVE)
		self.assertTrue(pbp.secondary_play_type is None)
		self.assertTrue(pbp.point_value == 0)
		self.assertTrue(pbp.shot_made is None)
		self.assertTrue(pbp.home_score == 0)
		self.assertTrue(pbp.visitor_score == 0)
		self.assertTrue(pbp.shot_distance is None)
		self.assertTrue(len(pbp.players) == 1)
		self.assertTrue(pbp.players[0] == 'duncati01')

	def test_create_pbp_instance_visitor_defensive_rebound_team(self):
		pbp = self.pbp_manager.create_pbp_instance(['4:12.0', 'Defensive rebound by Team', '', '38-42', '', ''])

		self.assertTrue(pbp.minutes == 4)
		self.assertTrue(pbp.seconds == 12.0)
		self.assertTrue(pbp.play_type == PlayByPlay.REBOUND)
		self.assertTrue(pbp.detail == PlayByPlay.REBOUND_DEFENSIVE)
		self.assertTrue(pbp.secondary_play_type is None)
		self.assertTrue(pbp.point_value == 0)
		self.assertTrue(pbp.shot_made is None)
		self.assertTrue(pbp.home_score == 42)
		self.assertTrue(pbp.visitor_score == 38)
		self.assertTrue(pbp.shot_distance is None)
		self.assertTrue(len(pbp.players) == 0)


if __name__ == '__main__':
	unittest.main()