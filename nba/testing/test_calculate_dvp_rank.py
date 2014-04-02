import unittest
from datetime import date

from shared.dfs_constants import DFSConstants
from calculate_dvp_rank import DvPRankCalculator
from models.defense_vs_position_manager import DefenseVsPositionManager, DefenseVsPosition
import BBRTestUtility


class TestCalculateDvPRank(unittest.TestCase):
	"""
	Test cases for CalculateDvPRank
	"""
	test_util = None
	dvp_rank_calculator = None
	dvp_manager = None

	def setUp(self):
		self.test_util = BBRTestUtility.BBRTestUtility()
		self.dvp_manager = DefenseVsPositionManager(cnx=self.test_util.conn)
		self.dvp_rank_calculator = DvPRankCalculator(cnx=self.test_util.conn)
		self.test_util.runSQL()

	def tearDown(self):
		self.test_util = None
		self.dvp_rank_calculator = None

	def test_calculate_fantasy_points(self):
		# Create the teams that will participate
		team_game_totals = self.test_util.generate_default_team_game_totals_info()
		team_game_totals["team"] = "BOS"
		team_game_totals["season"] = 2013
		team_game_totals["date"] = date(2014, 1, 1)
		team_game_totals["game"] = 1
		self.test_util.insert_into_team_game_totals(team_game_totals)

		team_game_totals["team"] = "BOS"
		team_game_totals["season"] = 2013
		team_game_totals["date"] = date(2014, 1, 2)
		team_game_totals["game"] = 2
		self.test_util.insert_into_team_game_totals(team_game_totals)

		team_game_totals["team"] = "NYK"
		team_game_totals["season"] = 2013
		team_game_totals["date"] = date(2014, 1, 1)
		team_game_totals["game"] = 1
		self.test_util.insert_into_team_game_totals(team_game_totals)

		team_game_totals["team"] = "NYK"
		team_game_totals["season"] = 2013
		team_game_totals["date"] = date(2014, 1, 2)
		team_game_totals["game"] = 2
		self.test_util.insert_into_team_game_totals(team_game_totals)

		for position in ["PG", "SG", "SF", "PF", "C"]:
			p1 = "{}1".format(position)
			p2 = "{}2".format(position)

			# Create players
			player_info = self.test_util.generate_default_player_info()
			player_info["id"] = p1
			player_info["name"] = "{} 1".format(position)
			player_info["position"] = position
			player_info["rg_position"] = position
			self.test_util.insert_into_players(player_info)

			player_info["id"] = p2
			player_info["name"] = "{} 2".format(position)
			player_info["position"] = position
			player_info["rg_position"] = position
			self.test_util.insert_into_players(player_info)

			# Create game_totals_basic info (49 FD fantasy points)
			game_totals_basic_info = self.test_util.generate_default_game_totals_basic_info()
			game_totals_basic_info["player_id"] = p1
			game_totals_basic_info["season"] = 2013
			game_totals_basic_info["game_number"] = 1
			game_totals_basic_info["team"] = "BOS"
			game_totals_basic_info["opponent"] = "NYK"
			game_totals_basic_info["date"] = date(2014, 1, 1)
			game_totals_basic_info["points"] = 20
			game_totals_basic_info["offensive_rebounds"] = 5
			game_totals_basic_info["defensive_rebounds"] = 10
			game_totals_basic_info["assists"] = 4
			game_totals_basic_info["steals"] = 3
			game_totals_basic_info["blocks"] = 2
			game_totals_basic_info["turnovers"] = 5
			gtb1_id = self.test_util.insert_into_game_totals_basic(game_totals_basic_info)

			# 20.4 FD fantasy points
			game_totals_basic_info["player_id"] = p2
			game_totals_basic_info["season"] = 2013
			game_totals_basic_info["game_number"] = 1
			game_totals_basic_info["team"] = "NYK"
			game_totals_basic_info["opponent"] = "BOS"
			game_totals_basic_info["date"] = date(2014, 1, 1)
			game_totals_basic_info["points"] = 10
			game_totals_basic_info["offensive_rebounds"] = 0
			game_totals_basic_info["defensive_rebounds"] = 2
			game_totals_basic_info["assists"] = 4
			game_totals_basic_info["steals"] = 1
			game_totals_basic_info["blocks"] = 0
			game_totals_basic_info["turnovers"] = 0
			gtb2_id = self.test_util.insert_into_game_totals_basic(game_totals_basic_info)

			game_totals_basic_info = self.test_util.generate_default_game_totals_basic_info()
			game_totals_basic_info["player_id"] = p1
			game_totals_basic_info["season"] = 2013
			game_totals_basic_info["game_number"] = 2
			game_totals_basic_info["team"] = "BOS"
			game_totals_basic_info["opponent"] = "NYK"
			game_totals_basic_info["date"] = date(2014, 1, 2)
			game_totals_basic_info["points"] = 20
			game_totals_basic_info["offensive_rebounds"] = 5
			game_totals_basic_info["defensive_rebounds"] = 10
			game_totals_basic_info["assists"] = 4
			game_totals_basic_info["steals"] = 3
			game_totals_basic_info["blocks"] = 2
			game_totals_basic_info["turnovers"] = 5
			gtb3_id = self.test_util.insert_into_game_totals_basic(game_totals_basic_info)

			# 20.4 FD fantasy points
			game_totals_basic_info["player_id"] = p2
			game_totals_basic_info["season"] = 2013
			game_totals_basic_info["game_number"] = 2
			game_totals_basic_info["team"] = "NYK"
			game_totals_basic_info["opponent"] = "BOS"
			game_totals_basic_info["date"] = date(2014, 1, 2)
			game_totals_basic_info["points"] = 10
			game_totals_basic_info["offensive_rebounds"] = 0
			game_totals_basic_info["defensive_rebounds"] = 2
			game_totals_basic_info["assists"] = 4
			game_totals_basic_info["steals"] = 1
			game_totals_basic_info["blocks"] = 0
			game_totals_basic_info["turnovers"] = 0
			gtb4_id = self.test_util.insert_into_game_totals_basic(game_totals_basic_info)

			# Set up Fantasy Points
			fantasy_points_info = self.test_util.generate_default_fantasy_points_info()
			for s in [DFSConstants.DRAFT_DAY, DFSConstants.DRAFT_KINGS, DFSConstants.FAN_DUEL, DFSConstants.STAR_STREET]:
				fantasy_points_info["game_totals_basic_id"] = gtb1_id
				fantasy_points_info["player_id"] = p1
				fantasy_points_info["site"] = s
				fantasy_points_info["season"] = 2013
				fantasy_points_info["game_number"] = 1
				fantasy_points_info["points"] = 49
				self.test_util.insert_into_fantasy_points(fantasy_points_info)

				fantasy_points_info["game_totals_basic_id"] = gtb3_id
				fantasy_points_info["player_id"] = p1
				fantasy_points_info["site"] = s
				fantasy_points_info["season"] = 2013
				fantasy_points_info["game_number"] = 2
				fantasy_points_info["points"] = 49
				self.test_util.insert_into_fantasy_points(fantasy_points_info)

				fantasy_points_info["game_totals_basic_id"] = gtb4_id
				fantasy_points_info["player_id"] = p2
				fantasy_points_info["site"] = s
				fantasy_points_info["season"] = 2013
				fantasy_points_info["game_number"] = 2
				fantasy_points_info["points"] = 20.4
				self.test_util.insert_into_fantasy_points(fantasy_points_info)

				fantasy_points_info["game_totals_basic_id"] = gtb2_id
				fantasy_points_info["player_id"] = p2
				fantasy_points_info["site"] = s
				fantasy_points_info["season"] = 2013
				fantasy_points_info["game_number"] = 1
				fantasy_points_info["points"] = 20.4
				self.test_util.insert_into_fantasy_points(fantasy_points_info)

		self.dvp_rank_calculator.calculate(2013)

		for stat in [DFSConstants.FANTASY_POINTS, DFSConstants.POINTS]:
			for position in ["PG", "SG", "SF", "PF", "C"]:
				for s in [DFSConstants.DRAFT_DAY, DFSConstants.DRAFT_KINGS, DFSConstants.FAN_DUEL, DFSConstants.STAR_STREET]:
					if stat == DFSConstants.FANTASY_POINTS:
						dvps = self.dvp_manager.get(DefenseVsPosition(stat=stat, position=position, site=s))
					else:
						dvps = self.dvp_manager.get(DefenseVsPosition(stat=stat, position=position))
						s = None

					# Should get two entries for each team (BOS and NYK) for each of the two dates, so since we
					# have two players we'll get 4 for this position/site combination.
					self.assertTrue(len(dvps) == 4)

					# First game for BOS
					self.assertTrue(dvps[0].date == '2014-01-01')
					self.assertTrue(dvps[0].position == position)
					self.assertTrue(dvps[0].site == s)
					self.assertTrue(dvps[0].stat == stat)
					if stat == DFSConstants.FANTASY_POINTS:
						self.assertTrue(dvps[0].value == 20.4)
					elif stat == DFSConstants.POINTS:
						self.assertTrue(dvps[0].value == 10)
					self.assertTrue(dvps[0].rank == 1)
					self.assertTrue(dvps[0].team == "BOS")

					# First game for NYK
					self.assertTrue(dvps[1].date == '2014-01-01')
					self.assertTrue(dvps[1].position == position)
					self.assertTrue(dvps[1].site == s)
					self.assertTrue(dvps[1].stat == stat)
					if stat == DFSConstants.FANTASY_POINTS:
						self.assertTrue(dvps[1].value == 49)
					elif stat == DFSConstants.POINTS:
						self.assertTrue(dvps[1].value == 20)
					self.assertTrue(dvps[1].rank == 2)
					self.assertTrue(dvps[1].team == "NYK")

					# Second game for BOS
					self.assertTrue(dvps[2].date == '2014-01-02')
					self.assertTrue(dvps[2].position == position)
					self.assertTrue(dvps[2].site == s)
					self.assertTrue(dvps[2].stat == stat)
					if stat == DFSConstants.FANTASY_POINTS:
						self.assertTrue(dvps[2].value == 20.4)
					elif stat == DFSConstants.POINTS:
						self.assertTrue(dvps[2].value == 10)
					self.assertTrue(dvps[2].rank == 1)
					self.assertTrue(dvps[2].team == "BOS")

					# Second game for NYK
					self.assertTrue(dvps[3].date == '2014-01-02')
					self.assertTrue(dvps[3].position == position)
					self.assertTrue(dvps[3].site == s)
					self.assertTrue(dvps[3].stat == stat)
					if stat == DFSConstants.FANTASY_POINTS:
						self.assertTrue(dvps[3].value == 49)
					elif stat == DFSConstants.POINTS:
						self.assertTrue(dvps[3].value == 20)
					self.assertTrue(dvps[3].rank == 2)
					self.assertTrue(dvps[3].team == "NYK")

	def test_calculate_fantasy_points_one_existing(self):
		# Create the teams that will participate
		team_game_totals = self.test_util.generate_default_team_game_totals_info()
		team_game_totals["team"] = "BOS"
		team_game_totals["season"] = 2013
		team_game_totals["date"] = date(2014, 1, 1)
		team_game_totals["game"] = 1
		self.test_util.insert_into_team_game_totals(team_game_totals)

		team_game_totals["team"] = "BOS"
		team_game_totals["season"] = 2013
		team_game_totals["date"] = date(2014, 1, 2)
		team_game_totals["game"] = 2
		self.test_util.insert_into_team_game_totals(team_game_totals)

		team_game_totals["team"] = "NYK"
		team_game_totals["season"] = 2013
		team_game_totals["date"] = date(2014, 1, 1)
		team_game_totals["game"] = 1
		self.test_util.insert_into_team_game_totals(team_game_totals)

		team_game_totals["team"] = "NYK"
		team_game_totals["season"] = 2013
		team_game_totals["date"] = date(2014, 1, 2)
		team_game_totals["game"] = 2
		self.test_util.insert_into_team_game_totals(team_game_totals)

		for position in ["PG", "SG", "SF", "PF", "C"]:
			p1 = "{}1".format(position)
			p2 = "{}2".format(position)

			# Create players
			player_info = self.test_util.generate_default_player_info()
			player_info["id"] = p1
			player_info["name"] = "{} 1".format(position)
			player_info["position"] = position
			player_info["rg_position"] = position
			self.test_util.insert_into_players(player_info)

			player_info["id"] = p2
			player_info["name"] = "{} 2".format(position)
			player_info["position"] = position
			player_info["rg_position"] = position
			self.test_util.insert_into_players(player_info)

			# Create game_totals_basic info (49 FD fantasy points)
			game_totals_basic_info = self.test_util.generate_default_game_totals_basic_info()
			game_totals_basic_info["player_id"] = p1
			game_totals_basic_info["season"] = 2013
			game_totals_basic_info["game_number"] = 1
			game_totals_basic_info["team"] = "BOS"
			game_totals_basic_info["opponent"] = "NYK"
			game_totals_basic_info["date"] = date(2014, 1, 1)
			game_totals_basic_info["points"] = 20
			game_totals_basic_info["offensive_rebounds"] = 5
			game_totals_basic_info["defensive_rebounds"] = 10
			game_totals_basic_info["total_rebounds"] = 15
			game_totals_basic_info["assists"] = 4
			game_totals_basic_info["steals"] = 3
			game_totals_basic_info["blocks"] = 2
			game_totals_basic_info["turnovers"] = 5
			game_totals_basic_info["field_goals"] = 1
			game_totals_basic_info["field_goal_attempts"] = 1
			game_totals_basic_info["three_point_field_goals"] = 1
			game_totals_basic_info["three_point_field_goal_attempts"] = 1
			game_totals_basic_info["free_throws"] = 1
			game_totals_basic_info["free_throw_attempts"] = 1
			gtb1_id = self.test_util.insert_into_game_totals_basic(game_totals_basic_info)

			# 20.4 FD fantasy points
			game_totals_basic_info["player_id"] = p2
			game_totals_basic_info["season"] = 2013
			game_totals_basic_info["game_number"] = 1
			game_totals_basic_info["team"] = "NYK"
			game_totals_basic_info["opponent"] = "BOS"
			game_totals_basic_info["date"] = date(2014, 1, 1)
			game_totals_basic_info["points"] = 10
			game_totals_basic_info["offensive_rebounds"] = 0
			game_totals_basic_info["defensive_rebounds"] = 2
			game_totals_basic_info["total_rebounds"] = 2
			game_totals_basic_info["assists"] = 4
			game_totals_basic_info["steals"] = 1
			game_totals_basic_info["blocks"] = 0
			game_totals_basic_info["turnovers"] = 0
			game_totals_basic_info["field_goals"] = 1
			game_totals_basic_info["field_goal_attempts"] = 1
			game_totals_basic_info["three_point_field_goals"] = 1
			game_totals_basic_info["three_point_field_goal_attempts"] = 1
			game_totals_basic_info["free_throws"] = 1
			game_totals_basic_info["free_throw_attempts"] = 1
			gtb2_id = self.test_util.insert_into_game_totals_basic(game_totals_basic_info)

			game_totals_basic_info = self.test_util.generate_default_game_totals_basic_info()
			game_totals_basic_info["player_id"] = p1
			game_totals_basic_info["season"] = 2013
			game_totals_basic_info["game_number"] = 2
			game_totals_basic_info["team"] = "BOS"
			game_totals_basic_info["opponent"] = "NYK"
			game_totals_basic_info["date"] = date(2014, 1, 2)
			game_totals_basic_info["points"] = 20
			game_totals_basic_info["offensive_rebounds"] = 5
			game_totals_basic_info["defensive_rebounds"] = 10
			game_totals_basic_info["total_rebounds"] = 15
			game_totals_basic_info["assists"] = 4
			game_totals_basic_info["steals"] = 3
			game_totals_basic_info["blocks"] = 2
			game_totals_basic_info["turnovers"] = 5
			game_totals_basic_info["field_goals"] = 1
			game_totals_basic_info["field_goal_attempts"] = 1
			game_totals_basic_info["three_point_field_goals"] = 1
			game_totals_basic_info["three_point_field_goal_attempts"] = 1
			game_totals_basic_info["free_throws"] = 1
			game_totals_basic_info["free_throw_attempts"] = 1
			gtb3_id = self.test_util.insert_into_game_totals_basic(game_totals_basic_info)

			# 20.4 FD fantasy points
			game_totals_basic_info["player_id"] = p2
			game_totals_basic_info["season"] = 2013
			game_totals_basic_info["game_number"] = 2
			game_totals_basic_info["team"] = "NYK"
			game_totals_basic_info["opponent"] = "BOS"
			game_totals_basic_info["date"] = date(2014, 1, 2)
			game_totals_basic_info["points"] = 10
			game_totals_basic_info["offensive_rebounds"] = 0
			game_totals_basic_info["defensive_rebounds"] = 2
			game_totals_basic_info["total_rebounds"] = 2
			game_totals_basic_info["assists"] = 4
			game_totals_basic_info["steals"] = 1
			game_totals_basic_info["blocks"] = 0
			game_totals_basic_info["turnovers"] = 0
			game_totals_basic_info["field_goals"] = 1
			game_totals_basic_info["field_goal_attempts"] = 1
			game_totals_basic_info["three_point_field_goals"] = 1
			game_totals_basic_info["three_point_field_goal_attempts"] = 1
			game_totals_basic_info["free_throws"] = 1
			game_totals_basic_info["free_throw_attempts"] = 1
			gtb4_id = self.test_util.insert_into_game_totals_basic(game_totals_basic_info)

			# Set up Fantasy Points
			fantasy_points_info = self.test_util.generate_default_fantasy_points_info()
			for s in [DFSConstants.DRAFT_DAY, DFSConstants.DRAFT_KINGS, DFSConstants.FAN_DUEL, DFSConstants.STAR_STREET]:
				fantasy_points_info["game_totals_basic_id"] = gtb1_id
				fantasy_points_info["player_id"] = p1
				fantasy_points_info["site"] = s
				fantasy_points_info["season"] = 2013
				fantasy_points_info["game_number"] = 1
				fantasy_points_info["points"] = 49
				self.test_util.insert_into_fantasy_points(fantasy_points_info)

				fantasy_points_info["game_totals_basic_id"] = gtb3_id
				fantasy_points_info["player_id"] = p1
				fantasy_points_info["site"] = s
				fantasy_points_info["season"] = 2013
				fantasy_points_info["game_number"] = 2
				fantasy_points_info["points"] = 49
				self.test_util.insert_into_fantasy_points(fantasy_points_info)

				fantasy_points_info["game_totals_basic_id"] = gtb4_id
				fantasy_points_info["player_id"] = p2
				fantasy_points_info["site"] = s
				fantasy_points_info["season"] = 2013
				fantasy_points_info["game_number"] = 2
				fantasy_points_info["points"] = 20.4
				self.test_util.insert_into_fantasy_points(fantasy_points_info)

				fantasy_points_info["game_totals_basic_id"] = gtb2_id
				fantasy_points_info["player_id"] = p2
				fantasy_points_info["site"] = s
				fantasy_points_info["season"] = 2013
				fantasy_points_info["game_number"] = 1
				fantasy_points_info["points"] = 20.4
				self.test_util.insert_into_fantasy_points(fantasy_points_info)

		# No filter, should get all of them, and it should be empty
		dvps = self.dvp_manager.get(DefenseVsPosition())
		self.assertTrue(len(dvps) == 0)

		# Add one manually.  Now our count should be 1
		self.dvp_manager.insert(DefenseVsPosition(stat=DFSConstants.FANTASY_POINTS, position="PG", team="BOS", season=2013, value=15, date="2014-01-01", site=DFSConstants.FAN_DUEL))
		dvps = self.dvp_manager.get(DefenseVsPosition())
		self.assertTrue(len(dvps) == 1)

		self.dvp_rank_calculator.calculate(2013, yesterday_only=False)

		# After running the calculator, there should be
		#   12 stats * 5 positions * 1 sites * 4 team/dates = 240 +
		#   1 stat (FPs) * 5 positions * 4 sites * 4 team/dates = 80 + 240 = 320
		# That calculation includes the one that represents the inserted entity above.  A result of 321 would
		# mean that the calculator isn't properly picking up the one already there.
		dvps = self.dvp_manager.get(DefenseVsPosition())
		self.assertTrue(len(dvps) == 320)

	def test_calculate_fantasy_points_yesterday_only(self):
		# Create the teams that will participate
		team_game_totals = self.test_util.generate_default_team_game_totals_info()
		team_game_totals["team"] = "BOS"
		team_game_totals["season"] = 2013
		team_game_totals["date"] = date(2014, 1, 1)
		team_game_totals["game"] = 1
		self.test_util.insert_into_team_game_totals(team_game_totals)

		team_game_totals["team"] = "BOS"
		team_game_totals["season"] = 2013
		team_game_totals["date"] = date.today()
		team_game_totals["game"] = 2
		self.test_util.insert_into_team_game_totals(team_game_totals)

		team_game_totals["team"] = "NYK"
		team_game_totals["season"] = 2013
		team_game_totals["date"] = date(2014, 1, 1)
		team_game_totals["game"] = 1
		self.test_util.insert_into_team_game_totals(team_game_totals)

		team_game_totals["team"] = "NYK"
		team_game_totals["season"] = 2013
		team_game_totals["date"] = date.today()
		team_game_totals["game"] = 2
		self.test_util.insert_into_team_game_totals(team_game_totals)

		for position in ["PG", "SG", "SF", "PF", "C"]:
			p1 = "{}1".format(position)
			p2 = "{}2".format(position)

			# Create players
			player_info = self.test_util.generate_default_player_info()
			player_info["id"] = p1
			player_info["name"] = "{} 1".format(position)
			player_info["position"] = position
			player_info["rg_position"] = position
			self.test_util.insert_into_players(player_info)

			player_info["id"] = p2
			player_info["name"] = "{} 2".format(position)
			player_info["position"] = position
			player_info["rg_position"] = position
			self.test_util.insert_into_players(player_info)

			# Create game_totals_basic info (49 FD fantasy points)
			game_totals_basic_info = self.test_util.generate_default_game_totals_basic_info()
			game_totals_basic_info["player_id"] = p1
			game_totals_basic_info["season"] = 2013
			game_totals_basic_info["game_number"] = 1
			game_totals_basic_info["team"] = "BOS"
			game_totals_basic_info["opponent"] = "NYK"
			game_totals_basic_info["date"] = date(2014, 1, 1)
			game_totals_basic_info["points"] = 20
			game_totals_basic_info["offensive_rebounds"] = 5
			game_totals_basic_info["defensive_rebounds"] = 10
			game_totals_basic_info["total_rebounds"] = 15
			game_totals_basic_info["assists"] = 4
			game_totals_basic_info["steals"] = 3
			game_totals_basic_info["blocks"] = 2
			game_totals_basic_info["turnovers"] = 5
			game_totals_basic_info["field_goals"] = 1
			game_totals_basic_info["field_goal_attempts"] = 1
			game_totals_basic_info["three_point_field_goals"] = 1
			game_totals_basic_info["three_point_field_goal_attempts"] = 1
			game_totals_basic_info["free_throws"] = 1
			game_totals_basic_info["free_throw_attempts"] = 1
			gtb1_id = self.test_util.insert_into_game_totals_basic(game_totals_basic_info)

			# 20.4 FD fantasy points
			game_totals_basic_info["player_id"] = p2
			game_totals_basic_info["season"] = 2013
			game_totals_basic_info["game_number"] = 1
			game_totals_basic_info["team"] = "NYK"
			game_totals_basic_info["opponent"] = "BOS"
			game_totals_basic_info["date"] = date(2014, 1, 1)
			game_totals_basic_info["points"] = 10
			game_totals_basic_info["offensive_rebounds"] = 0
			game_totals_basic_info["defensive_rebounds"] = 2
			game_totals_basic_info["total_rebounds"] = 2
			game_totals_basic_info["assists"] = 4
			game_totals_basic_info["steals"] = 1
			game_totals_basic_info["blocks"] = 0
			game_totals_basic_info["turnovers"] = 0
			game_totals_basic_info["field_goals"] = 1
			game_totals_basic_info["field_goal_attempts"] = 1
			game_totals_basic_info["three_point_field_goals"] = 1
			game_totals_basic_info["three_point_field_goal_attempts"] = 1
			game_totals_basic_info["free_throws"] = 1
			game_totals_basic_info["free_throw_attempts"] = 1
			gtb2_id = self.test_util.insert_into_game_totals_basic(game_totals_basic_info)

			game_totals_basic_info = self.test_util.generate_default_game_totals_basic_info()
			game_totals_basic_info["player_id"] = p1
			game_totals_basic_info["season"] = 2013
			game_totals_basic_info["game_number"] = 2
			game_totals_basic_info["team"] = "BOS"
			game_totals_basic_info["opponent"] = "NYK"
			game_totals_basic_info["date"] = date.today()
			game_totals_basic_info["points"] = 20
			game_totals_basic_info["offensive_rebounds"] = 5
			game_totals_basic_info["defensive_rebounds"] = 10
			game_totals_basic_info["total_rebounds"] = 15
			game_totals_basic_info["assists"] = 4
			game_totals_basic_info["steals"] = 3
			game_totals_basic_info["blocks"] = 2
			game_totals_basic_info["turnovers"] = 5
			game_totals_basic_info["field_goals"] = 1
			game_totals_basic_info["field_goal_attempts"] = 1
			game_totals_basic_info["three_point_field_goals"] = 1
			game_totals_basic_info["three_point_field_goal_attempts"] = 1
			game_totals_basic_info["free_throws"] = 1
			game_totals_basic_info["free_throw_attempts"] = 1
			gtb3_id = self.test_util.insert_into_game_totals_basic(game_totals_basic_info)

			# 20.4 FD fantasy points
			game_totals_basic_info["player_id"] = p2
			game_totals_basic_info["season"] = 2013
			game_totals_basic_info["game_number"] = 2
			game_totals_basic_info["team"] = "NYK"
			game_totals_basic_info["opponent"] = "BOS"
			game_totals_basic_info["date"] = date.today()
			game_totals_basic_info["points"] = 10
			game_totals_basic_info["offensive_rebounds"] = 0
			game_totals_basic_info["defensive_rebounds"] = 2
			game_totals_basic_info["total_rebounds"] = 2
			game_totals_basic_info["assists"] = 4
			game_totals_basic_info["steals"] = 1
			game_totals_basic_info["blocks"] = 0
			game_totals_basic_info["turnovers"] = 0
			game_totals_basic_info["field_goals"] = 1
			game_totals_basic_info["field_goal_attempts"] = 1
			game_totals_basic_info["three_point_field_goals"] = 1
			game_totals_basic_info["three_point_field_goal_attempts"] = 1
			game_totals_basic_info["free_throws"] = 1
			game_totals_basic_info["free_throw_attempts"] = 1
			gtb4_id = self.test_util.insert_into_game_totals_basic(game_totals_basic_info)

			# Set up Fantasy Points
			fantasy_points_info = self.test_util.generate_default_fantasy_points_info()
			for s in [DFSConstants.DRAFT_DAY, DFSConstants.DRAFT_KINGS, DFSConstants.FAN_DUEL, DFSConstants.STAR_STREET]:
				fantasy_points_info["game_totals_basic_id"] = gtb1_id
				fantasy_points_info["player_id"] = p1
				fantasy_points_info["site"] = s
				fantasy_points_info["season"] = 2013
				fantasy_points_info["game_number"] = 1
				fantasy_points_info["points"] = 49
				self.test_util.insert_into_fantasy_points(fantasy_points_info)

				fantasy_points_info["game_totals_basic_id"] = gtb3_id
				fantasy_points_info["player_id"] = p1
				fantasy_points_info["site"] = s
				fantasy_points_info["season"] = 2013
				fantasy_points_info["game_number"] = 2
				fantasy_points_info["points"] = 49
				self.test_util.insert_into_fantasy_points(fantasy_points_info)

				fantasy_points_info["game_totals_basic_id"] = gtb4_id
				fantasy_points_info["player_id"] = p2
				fantasy_points_info["site"] = s
				fantasy_points_info["season"] = 2013
				fantasy_points_info["game_number"] = 2
				fantasy_points_info["points"] = 20.4
				self.test_util.insert_into_fantasy_points(fantasy_points_info)

				fantasy_points_info["game_totals_basic_id"] = gtb2_id
				fantasy_points_info["player_id"] = p2
				fantasy_points_info["site"] = s
				fantasy_points_info["season"] = 2013
				fantasy_points_info["game_number"] = 1
				fantasy_points_info["points"] = 20.4
				self.test_util.insert_into_fantasy_points(fantasy_points_info)

		# No filter, should get all of them, and it should be empty
		dvps = self.dvp_manager.get(DefenseVsPosition())
		self.assertTrue(len(dvps) == 0)

		self.dvp_rank_calculator.calculate(2013, yesterday_only=True)

		# After running the calculator, there should be
		#   12 stats * 5 positions * 1 sites * 2 team/dates = 120 +
		#   1 stat (FPs) * 5 positions * 4 sites * 2 team/dates = 40 + 120 = 160
		# That calculation includes the one that represents the inserted entity above.  A result of 209 would
		# mean that the calculator isn't properly picking up the one already there.
		dvps = self.dvp_manager.get(DefenseVsPosition())
		self.assertTrue(len(dvps) == 160)


if __name__ == '__main__':
	unittest.main()