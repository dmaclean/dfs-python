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

	##############
	# Basic info
	##############
	PLAYER_ID = "player_id"
	NAME = "name"
	POSITION = "position"

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