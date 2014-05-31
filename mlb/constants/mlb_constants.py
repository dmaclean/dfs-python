__author__ = 'dan'

class MLBConstants:

	def __init__(self):
		pass

	#################
	# MongoDB stuff
	#################
	MONGO_MLB_DB_NAME = "baseball"
	MONGO_MLB_TEST_DB_NAME = "test_baseball"
	MONGO_MLB_PLAYERS_COLLECTION = "players"
	MONGO_MLB_LINEUPS_COLLECTION = "lineups"
	MONGO_MLB_NAME_MAPPING_COLLECTION = "name_mapping"

	MONGO_STATS_MLB_DB_NAME = "mlb_stats"
	MONGO_MLB_GAMES_COLLECTION = "games"
	MONGO_MLB_BVP_COLLECTION = "bvp"
	MONGO_MLB_GAMELOGS_COLLECTION = "gamelogs"
	MONGO_MLB_YTD_COLLECTION = "ytd"
	MONGO_MLB_BALLPARK_FACTORS_COLLECTION = "ballpark_factors"

	MONGO_MLB_NAME_MAPPING_BBR = "bbr"
	MONGO_MLB_NAME_MAPPING_ROTOWIRE = "rotowire"

	##############
	# Basic info
	##############
	PLAYER_ID = "player_id"
	NAME = "name"
	POSITION = "position"
	HANDEDNESS_BATTING = "handedness_batting"
	HANDEDNESS_THROWING = "handedness_throwing"

	##############################
	# Stats in Standard Pitching
	##############################
	STANDARD_PITCHING = "standard_pitching"
	AGE = "age"
	TEAM = "team"
	LEAGUE = "league"
	WINS = "wins"
	LOSSES = "losses"
	WIN_LOSS_PCT = "win_loss_pct"
	ERA = "era"
	GAMES = "games"
	GAMES_STARTED = "games_started"
	GAMES_FINISHED = "games_finished"
	COMPLETE_GAMES = "complete_games"
	SHUT_OUTS = "shut_outs"
	SAVES = "saves"
	INNINGS_PITCHED = "innings_pitched"
	HITS = "hits"
	RUNS = "runs"
	EARNED_RUNS = "earned_runs"
	HOME_RUNS = "home_runs"
	WALKS = "walks"
	INTENTIONAL_WALKS = "intentional_walks"
	STRIKE_OUTS = "strike_outs"
	HIT_BY_PITCH = "hit_by_pitch"
	BALKS = "balks"
	WILD_PITCHES = "wild_pitches"
	BATTERS_FACED = "batters_faced"
	ERA_PLUS = "era_plus"
	WHIP = "whip"
	HITS_PER_9_INNINGS = "hits_per_9_innings"
	HOME_RUNS_PER_9_INNINGS = "home_runs_per_9_innings"
	WALKS_PER_9_INNINGS = "walks_per_9_innings"
	STRIKE_OUTS_PER_9_INNINGS = "strike_outs_per_9_innings"
	STRIKE_OUT_TO_WALK_RATIO = "strike_out_to_walk_ratio"
	FIP = "fip"

	###########################
	# Player Value - Pitching
	###########################
	PLAYER_VALUE_PITCHING = "player_value_pitching"
	RUNS_ALLOWED_PER_9_INNINGS = "runs_allowed_per_9_innings"
	RUNS_ALLOWED_PER_9_INNINGS_OPP = "runs_allowed_per_9_innings_by_opponent"
	RUNS_PER_9_INNINGS_IN_SUPPORT_FROM_DEFENSE = "runs_allowed_per_9_innings_in_support_from_defense"
	RUNS_PER_9_INNINGS_BY_ROLE = "runs_per_9_innings_by_role"
	PARK_FACTORS = "park_factors"
	RUNS_PER_9_INNINGS_FOR_AVG_PITCHER = "runs_per_9_innings_for_avg_pitcher"
	RUNS_BETTER_THAN_AVG = "runs_better_than_avg"
	WINS_ABOVE_AVG = "wins_above_avg"
	GAME_ENTERING_LEVERAGE_INDEX = "game_entering_leverage_index"
	WINS_ABOVE_AVG_ADJUSTMENT = "wins_above_average_adjustment"
	WINS_ABOVE_REPLACEMENT = "wins_above_replacement"
	RUNS_BETTER_THAN_REPLACEMENT = "runs_better_than_replacement"
	WIN_LOSS_PCT_WITH_AVG_TEAM = "win_loss_pct_with_avg_team"
	WIN_LOSS_PCT_WITH_AVG_TEAM_SEASON = "win_loss_pct_with_avg_team_season"
	SALARY = "salary"

	####################
	# Pitching Gamelog
	####################
	PLAYER_GAMELOG_PITCHING = "player_gamelog_pitching"
	GAME_NUMBER = "game_number"
	DATE = "date"
	HOME_GAME = "home_game"
	OPPONENT = "opponent"
	RESULT = "result"
	TEAM_SCORE = "team_score"
	OPPONENT_SCORE = "opponent_score"
	INNINGS = "innings"
	DECISION = "decision"
	DAYS_REST = "days_rest"
	NUM_PITCHES = "num_pitches"
	STRIKES = "strikes"
	STRIKES_LOOKING = "strikes_looking"
	STRIKES_SWINGING = "strikes_swinging"
	GROUND_BALLS = "ground_balls"
	FLY_BALLS = "fly_balls"
	LINE_DRIVES = "line_drives"
	POP_UPS = "pop_ups"
	UNKNOWN_BATTED_BALLS = "unknown_batted_balls"
	PLAYER_GAME_SCORE = "player_game_score"
	INHERITED_RUNNERS = "inherited_runners"
	INHERITED_SCORE = "inherited_score"
	STOLEN_BASES = "stolen_bases"
	CAUGHT_STEALING = "caught_stealing"
	PICK_OFFS = "pick_offs"
	AT_BATS = "at_bats"
	DOUBLES = "doubles"
	TRIPLES = "triples"
	DOUBLE_PLAYS_GROUNDED_INTO = "double_plays_grounded_into"
	SACRIFICE_FLIES = "sacrifice_flies"
	REACHED_ON_ERROR = "reached_on_error"
	AVERAGE_LEVERAGE_INDEX = "average_leverage_index"
	WIN_PROBABILITY_ADDED_BY_PITCHER = "win_probability_added_by_pitcher"
	BASE_OUT_RUNS_SAVED = "base_out_runs_saved"
	ENTRY_SITUATION = "entry_situation"
	EXIT_SITUATION = "exit_situation"

	#####################
	# Batter vs Pitcher
	#####################
	BATTER_VS_PITCHER = "batter_vs_pitcher"
	BATTER_TYPE = "batter"
	PITCHER_TYPE = "pitcher"

	###########
	# Batters
	###########
	STANDARD_BATTING = "standard_batting"
	PLAYER_GAMELOG_BATTING = "player_gamelog_batting"
	PLATE_APPEARANCES = "plate_appearances"
	RBI = "rbi"
	BATTING_AVERAGE = "batting_average"
	ON_BASE_PERCENTAGE = "on_base_percentage"
	SLUGGING_PERCENTAGE = "slugging_percentage"
	OPS = "ops"
	OPS_PLUS = "ops_plus"
	SACRIFICE_HITS = "sacrifice_hits"
	BATTING_ORDER_POSITION = "batting_order_position"
	WIN_PROBABILITY_ADDED = "win_probability_added"
	BASE_OUT_RUNS_ADDED = "base_out_runs_added"
	GAMES_PLAYED = "games_played"
	TOTAL_BASES = "total_bases"
	HOME_RUNS_PER_AT_BAT = "home_runs_per_at_bat"
	TOTAL_BASES_PER_HIT = "total_bases_per_hit"
	EXTRA_BASE_HITS_PER_AT_BAT = "extra_base_hits_per_at_bat"

	PLAYER_VALUE_BATTING = "player_value_batting"
	RUNS_BATTING = "runs_batting"
	RUNS_FROM_BASERUNNING = "runs_from_baserunning"
	RUNS_GROUNDED_INTO_DOUBLE_PLAY = "runs_grounded_into_double_play"
	RUNS_FROM_FIELDING = "runs_from_fielding"
	RUNS_FROM_POSITION_SCARCITY = "runs_from_position_scarcity"
	RAA = "runs_above_average"
	WAA = "wins_above_average"
	RUNS_FROM_REPLACEMENT_LEVEL = "runs_from_replacement_level"
	RAR = "runs_above_replacement"
	WAR = "wins_above_replacement"
	OFF_WAR = "offensive_wins_above_replacement"
	DEF_WAR = "defensive_wins_above_replacement"
	OFF_RAR = "offensive_runs_above_replacement"
	BABIP = "babip"
	T_OPS_PLUS = "tOPS+"
	S_OPS_PLUS = "sOPS+"
	WOBA = "woba"

	BATTER_SPLITS = "batter_splits"
	PITCHER_SPLITS = "pitcher_splits"

	#################
	# Batter Splits
	#################
	SPLITS_TYPE = "type"
	SPLITS_SEASON_TOTALS = ""
	SPLITS_SEASON_TOTALS_HEADER = "Season Totals"
	SPLITS_LAST_7 = "Last 7 days"
	SPLITS_LAST_14 = "Last 14 days"
	SPLITS_LAST_28 = "Last 28 days"
	SPLITS_LAST_365 = "Last 365days"

	SPLITS_VS_RHP = "vs RHP"
	SPLITS_VS_LHP = "vs LHP"

	SPLITS_VS_LH_STARTER = "vs LH Starter"
	SPLITS_VS_RH_STARTER = "vs RH Starter"

	####################
	# Ballpark Factors
	####################
	BPF_ALL = "all"
	BPF_VS_RHP = "vs_rhp"
	BPF_VS_LHP = "vs_lhp"
	BPF_BALLPARK = "ballpark"

	##############
	# Vegas Odds
	##############
	OVER_UNDER = "over_under"
	VEGAS_LINE = "vegas_line"

	#########
	# Stats
	#########
	STATS_LLC = "stats_llc"