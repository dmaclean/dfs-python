from datetime import date
import sys
from pymongo.mongo_client import MongoClient
from mlb.constants.mlb_constants import MLBConstants
from mlb.models.lineup_manager import LineupManager
from mlb.models.player_manager import PlayerManager
from mlb.utilities.mlb_utilities import MLBUtilities

__author__ = 'dan'

class ProjectionGenerator:
	def __init__(self):
		self.lineup_manager = LineupManager()
		self.player_manager = PlayerManager()
		self.ballpark_collection = MongoClient('localhost', 27017)[MLBConstants.MONGO_MLB_DB_NAME][MLBConstants.MONGO_MLB_BALLPARK_FACTORS_COLLECTION]
		self.game_date = date.today()
		self.season = str(self.game_date.year)

	def read_cli(self):
		for arg in sys.argv:
			pieces = arg.split("=")
			if pieces[0] == "date":
				self.game_date = pieces[1]
				self.season = str(self.game_date.split("-")[0])

	def process(self):
		players = self.lineup_manager.lineups_collection.find_one({"date": str(self.game_date)}, {"players": 1})

		batter_csv_contents = [["Name", "Team", "Opponent", "Verified", "Position", "Batting Order Position", "wOBA", "wOBA vs Pitcher Type (LH/RH)",
								"OPS vs Pitcher Type (LH/RH)", "OPS", "Plate Appearances vs Pitcher", "Avg vs Pitcher",
								"Hits vs Pitcher", "HRs vs Pitcher", "Park Runs", "Park HRs", "Vegas Line", "O/U"]]
		pitcher_csv_contents = [["Name", "Team", "Opponent", "Verified", "LH/RH", "FIP", "wOBA", "wOBA vs RHB", "wOBA vs LHB",
								 "BABIP vs RHB", "BABIP vs LHB", "K/9", "BB/9", "Park Runs", "Park HRs", "Vegas Line", "O/U"]]

		ballpark_data = self.ballpark_collection.find_one({"date": str(self.game_date)})

		for player in players["players"]:
			player_lineup_data = players["players"][player]
			if len(player_lineup_data) < 8:
				continue

			player_csv_data = []

			escaped_player_id = player.replace("_", ".")

			player_data = self.player_manager.players_collection.find_one({MLBConstants.PLAYER_ID: escaped_player_id}, {MLBConstants.POSITION: 1, MLBConstants.NAME: 1})
			player_csv_data.append(player_data[MLBConstants.NAME].encode('ascii', errors='ignore'))
			player_csv_data.append(player_lineup_data[MLBConstants.TEAM])
			player_csv_data.append(player_lineup_data[MLBConstants.OPPONENT])
			player_csv_data.append(str(player_lineup_data[MLBConstants.VERIFIED]))

			is_batter = player_data[MLBConstants.POSITION] != "Pitcher"

			######################
			# Player is a batter
			######################
			if is_batter:
				# Retrieve opposing pitcher data
				opposing_pitcher_data = self.player_manager.players_collection.find_one({MLBConstants.NAME: player_lineup_data["opposing_pitcher"]}, {MLBConstants.PLAYER_ID: 1, MLBConstants.HANDEDNESS_THROWING: 1})
				batter_data = self.player_manager.players_collection.find_one({MLBConstants.PLAYER_ID: escaped_player_id},
																			  {MLBConstants.POSITION: 1,
																			   MLBConstants.HANDEDNESS_BATTING: 1,
																			   "{}.{}.{}".format(MLBConstants.STANDARD_BATTING, self.season, MLBConstants.WOBA): 1,
																			   "{}.{}.{}.{}".format(MLBConstants.BATTER_SPLITS, self.season, MLBConstants.SPLITS_VS_RHP, MLBConstants.WOBA): 1,
																			   "{}.{}.{}.{}".format(MLBConstants.BATTER_SPLITS, self.season, MLBConstants.SPLITS_VS_LHP, MLBConstants.WOBA): 1,
																			   "{}.{}.{}".format(MLBConstants.STANDARD_BATTING, self.season, MLBConstants.OPS): 1,
																			   "{}.{}.{}.{}".format(MLBConstants.BATTER_SPLITS, self.season, MLBConstants.SPLITS_VS_RHP, MLBConstants.OPS): 1,
																			   "{}.{}.{}.{}".format(MLBConstants.BATTER_SPLITS, self.season, MLBConstants.SPLITS_VS_LHP, MLBConstants.OPS): 1,
																			   MLBConstants.BATTER_VS_PITCHER: 1})

				if player_lineup_data["home"]:
					ballpark_hits = ballpark_data[MLBConstants.BPF_ALL][MLBUtilities.map_rg_team_to_rotowire(player_lineup_data[MLBConstants.TEAM])][MLBConstants.HITS]
					ballpark_home_runs = ballpark_data[MLBConstants.BPF_ALL][MLBUtilities.map_rg_team_to_rotowire(player_lineup_data[MLBConstants.TEAM])][MLBConstants.HOME_RUNS]
				else:
					ballpark_hits = ballpark_data[MLBConstants.BPF_ALL][MLBUtilities.map_rg_team_to_rotowire(player_lineup_data[MLBConstants.OPPONENT])][MLBConstants.HITS]
					ballpark_home_runs = ballpark_data[MLBConstants.BPF_ALL][MLBUtilities.map_rg_team_to_rotowire(player_lineup_data[MLBConstants.OPPONENT])][MLBConstants.HOME_RUNS]

				player_csv_data.append(player_lineup_data[MLBConstants.POSITION].replace(",", "/"))
				player_csv_data.append(str(player_lineup_data[MLBConstants.BATTING_ORDER_POSITION]))

				if self.season in batter_data[MLBConstants.STANDARD_BATTING]:
					player_csv_data.append(str(batter_data[MLBConstants.STANDARD_BATTING][self.season][MLBConstants.WOBA]))
				else:
					player_csv_data.append("N/A")

				if self.season in batter_data[MLBConstants.BATTER_SPLITS]:
					if opposing_pitcher_data is None or MLBConstants.HANDEDNESS_THROWING not in opposing_pitcher_data\
							or (MLBConstants.SPLITS_VS_LHP not in batter_data[MLBConstants.BATTER_SPLITS][self.season] and opposing_pitcher_data[MLBConstants.HANDEDNESS_THROWING] == "Left")\
							or (MLBConstants.SPLITS_VS_RHP not in batter_data[MLBConstants.BATTER_SPLITS][self.season] and opposing_pitcher_data[MLBConstants.HANDEDNESS_THROWING] == "Right"):
						player_csv_data.append("N/A")
						player_csv_data.append("N/A")
					elif opposing_pitcher_data[MLBConstants.HANDEDNESS_THROWING] == "Right":
						player_csv_data.append(str(batter_data[MLBConstants.BATTER_SPLITS][self.season][MLBConstants.SPLITS_VS_RHP][MLBConstants.WOBA]))
						player_csv_data.append(str(batter_data[MLBConstants.BATTER_SPLITS][self.season][MLBConstants.SPLITS_VS_RHP][MLBConstants.OPS]))
					else:
						player_csv_data.append(str(batter_data[MLBConstants.BATTER_SPLITS][self.season][MLBConstants.SPLITS_VS_LHP][MLBConstants.WOBA]))
						player_csv_data.append(str(batter_data[MLBConstants.BATTER_SPLITS][self.season][MLBConstants.SPLITS_VS_LHP][MLBConstants.OPS]))
				else:
					player_csv_data.append("N/A")
					player_csv_data.append("N/A")

				if self.season in batter_data[MLBConstants.STANDARD_BATTING]:
					player_csv_data.append(str(batter_data[MLBConstants.STANDARD_BATTING][self.season][MLBConstants.OPS]))
				else:
					player_csv_data.append("N/A")

				# BvP
				if opposing_pitcher_data is not None and opposing_pitcher_data[MLBConstants.PLAYER_ID] in batter_data[MLBConstants.BATTER_VS_PITCHER]:
					player_csv_data.append(str(batter_data[MLBConstants.BATTER_VS_PITCHER][opposing_pitcher_data[MLBConstants.PLAYER_ID]][MLBConstants.PLATE_APPEARANCES]))
					player_csv_data.append(str(batter_data[MLBConstants.BATTER_VS_PITCHER][opposing_pitcher_data[MLBConstants.PLAYER_ID]][MLBConstants.BATTING_AVERAGE]))
					player_csv_data.append(str(batter_data[MLBConstants.BATTER_VS_PITCHER][opposing_pitcher_data[MLBConstants.PLAYER_ID]][MLBConstants.HITS]))
					player_csv_data.append(str(batter_data[MLBConstants.BATTER_VS_PITCHER][opposing_pitcher_data[MLBConstants.PLAYER_ID]][MLBConstants.HOME_RUNS]))
				else:
					player_csv_data.append("N/A")
					player_csv_data.append("N/A")
					player_csv_data.append("N/A")
					player_csv_data.append("N/A")

				# Park factors
				player_csv_data.append(str(ballpark_hits))
				player_csv_data.append(str(ballpark_home_runs))

				######################
				# Vegas line and O/U
				######################
				if MLBConstants.VEGAS_LINE in player_lineup_data:
					player_csv_data.append(player_lineup_data[MLBConstants.VEGAS_LINE])
				else:
					player_csv_data.append("N/A")

				if MLBConstants.OVER_UNDER in player_lineup_data:
					player_csv_data.append(player_lineup_data[MLBConstants.OVER_UNDER])
				else:
					player_csv_data.append("N/A")

				batter_csv_contents.append(player_csv_data)

			#######################
			# Player is a pitcher
			#######################
			else:
				pitcher_data = self.player_manager.players_collection.find_one({MLBConstants.PLAYER_ID: escaped_player_id},
																			  {MLBConstants.POSITION: 1,
																			   MLBConstants.HANDEDNESS_THROWING: 1,
																			   "{}.{}.{}".format(MLBConstants.STANDARD_PITCHING, self.season, MLBConstants.FIP): 1,
																			   "{}.{}.vs RHB.{}".format(MLBConstants.PITCHER_SPLITS, self.season, MLBConstants.FIP): 1,
																			   "{}.{}.vs LHB.{}".format(MLBConstants.PITCHER_SPLITS, self.season, MLBConstants.FIP): 1,
																			   "{}.{}.{} Totals.{}".format(MLBConstants.PITCHER_SPLITS, self.season, self.season, MLBConstants.WOBA): 1,
																			   "{}.{}.vs RHB.{}".format(MLBConstants.PITCHER_SPLITS, self.season, MLBConstants.WOBA): 1,
																			   "{}.{}.vs LHB.{}".format(MLBConstants.PITCHER_SPLITS, self.season, MLBConstants.WOBA): 1,
																			   "{}.{}.vs RHB.{}".format(MLBConstants.PITCHER_SPLITS, self.season, MLBConstants.BABIP): 1,
																			   "{}.{}.vs LHB.{}".format(MLBConstants.PITCHER_SPLITS, self.season, MLBConstants.BABIP): 1,
																			   "{}.{}.{}".format(MLBConstants.STANDARD_PITCHING, self.season, MLBConstants.STRIKE_OUTS_PER_9_INNINGS): 1,
																			   "{}.{}.{}".format(MLBConstants.STANDARD_PITCHING, self.season, MLBConstants.WALKS_PER_9_INNINGS): 1,
																			   MLBConstants.BATTER_VS_PITCHER: 1})

				# Do a quick check to make sure the pitcher has stats for the current season.
				# If the current season isn't available then bail on this pitcher.
				if self.season not in pitcher_data[MLBConstants.STANDARD_PITCHING] or self.season not in pitcher_data[MLBConstants.PITCHER_SPLITS]:
					print "Could not find season {} for either Standard Pitching or Splits for {}.  Not sure how that would happen".format(self.season, escaped_player_id)
					continue

				if player_lineup_data["home"]:
					ballpark_hits = ballpark_data[MLBConstants.BPF_ALL][MLBUtilities.map_rg_team_to_rotowire(player_lineup_data[MLBConstants.TEAM])][MLBConstants.HITS]
					ballpark_home_runs = ballpark_data[MLBConstants.BPF_ALL][MLBUtilities.map_rg_team_to_rotowire(player_lineup_data[MLBConstants.TEAM])][MLBConstants.HOME_RUNS]
				else:
					ballpark_hits = ballpark_data[MLBConstants.BPF_ALL][MLBUtilities.map_rg_team_to_rotowire(player_lineup_data[MLBConstants.OPPONENT])][MLBConstants.HITS]
					ballpark_home_runs = ballpark_data[MLBConstants.BPF_ALL][MLBUtilities.map_rg_team_to_rotowire(player_lineup_data[MLBConstants.OPPONENT])][MLBConstants.HOME_RUNS]

				player_csv_data.append(pitcher_data[MLBConstants.HANDEDNESS_THROWING])

				if self.season in pitcher_data[MLBConstants.STANDARD_PITCHING]:
					player_csv_data.append(str(pitcher_data[MLBConstants.STANDARD_PITCHING][self.season][MLBConstants.FIP]))
				else:
					player_csv_data.append("N/A")

				if self.season in pitcher_data[MLBConstants.PITCHER_SPLITS] and MLBConstants.WOBA in pitcher_data[MLBConstants.PITCHER_SPLITS][self.season]["{} Totals".format(self.season)]:
					player_csv_data.append(str(pitcher_data[MLBConstants.PITCHER_SPLITS][self.season]["{} Totals".format(self.season)][MLBConstants.WOBA]))
				else:
					player_csv_data.append("N/A")

				if MLBConstants.PITCHER_SPLITS in pitcher_data:
					if MLBConstants.SPLITS_VS_RHB in pitcher_data[MLBConstants.PITCHER_SPLITS][self.season]:
						player_csv_data.append(str(pitcher_data[MLBConstants.PITCHER_SPLITS][self.season][MLBConstants.SPLITS_VS_RHB][MLBConstants.WOBA]))
					else:
						player_csv_data.append("N/A")
					if MLBConstants.SPLITS_VS_LHB in pitcher_data[MLBConstants.PITCHER_SPLITS][self.season]:
						player_csv_data.append(str(pitcher_data[MLBConstants.PITCHER_SPLITS][self.season][MLBConstants.SPLITS_VS_LHB][MLBConstants.WOBA]))
					else:
						player_csv_data.append("N/A")
					if MLBConstants.SPLITS_VS_RHB in pitcher_data[MLBConstants.PITCHER_SPLITS][self.season]:
						player_csv_data.append(str(pitcher_data[MLBConstants.PITCHER_SPLITS][self.season][MLBConstants.SPLITS_VS_RHB][MLBConstants.BABIP]))
					else:
						player_csv_data.append("N/A")
					if MLBConstants.SPLITS_VS_LHB in pitcher_data[MLBConstants.PITCHER_SPLITS][self.season]:
						player_csv_data.append(str(pitcher_data[MLBConstants.PITCHER_SPLITS][self.season][MLBConstants.SPLITS_VS_LHB][MLBConstants.BABIP]))
					else:
						player_csv_data.append("N/A")

				if self.season in pitcher_data[MLBConstants.STANDARD_PITCHING]:
					player_csv_data.append(str(pitcher_data[MLBConstants.STANDARD_PITCHING][self.season][MLBConstants.STRIKE_OUTS_PER_9_INNINGS]))
					player_csv_data.append(str(pitcher_data[MLBConstants.STANDARD_PITCHING][self.season][MLBConstants.WALKS_PER_9_INNINGS]))
				else:
					player_csv_data.append("N/A")
					player_csv_data.append("N/A")

				player_csv_data.append(str(ballpark_hits))
				player_csv_data.append(str(ballpark_home_runs))

				######################
				# Vegas line and O/U
				######################
				if MLBConstants.VEGAS_LINE in player_lineup_data:
					player_csv_data.append(player_lineup_data[MLBConstants.VEGAS_LINE])
				else:
					player_csv_data.append("N/A")

				if MLBConstants.OVER_UNDER in player_lineup_data:
					player_csv_data.append(player_lineup_data[MLBConstants.OVER_UNDER])
				else:
					player_csv_data.append("N/A")

				# Look for opponents
				opponents = []

				# for p in players["players"]:
				# 	pld = players["players"][p]
				# 	if len(pld) == 0 or pld["opposing_pitcher"] != player_data[MLBConstants.NAME]:
				# 		continue
				#
				# 	opponent = self.player_manager.players_collection.find_one({MLBConstants.PLAYER_ID: p},
				#                                                               {MLBConstants.POSITION: 1,
				#                                                                "{}.{}.{}".format(MLBConstants.STANDARD_BATTING, self.season, MLBConstants.WOBA): 1,
				#                                                                "{}.{}.vs RH Starter.{}".format(MLBConstants.BATTER_SPLITS, self.season, MLBConstants.WOBA): 1,
				#                                                                "{}.{}.vs LH Starter.{}".format(MLBConstants.BATTER_SPLITS, self.season, MLBConstants.WOBA): 1,
				#                                                                MLBConstants.BATTER_VS_PITCHER: 1})
				# 	opponents.append(opponent)
				#
				# for o in opponents:
				# 	pass

				pitcher_csv_contents.append(player_csv_data)

			print player_csv_data

		# Write results out to file
		pitcher_output = open("../projections/pitchers_{}.csv".format(str(date.today())), "w")
		batter_output = open("../projections/batters_{}.csv".format(str(date.today())), "w")

		for line in pitcher_csv_contents:
			pitcher_output.write(",".join(line) + "\n")
		for line in batter_csv_contents:
			batter_output.write(",".join(line) + "\n")


if __name__ == '__main__':
	projection_generator = ProjectionGenerator()
	projection_generator.read_cli()
	projection_generator.process()