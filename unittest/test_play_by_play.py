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


if __name__ == '__main__':
	unittest.main()