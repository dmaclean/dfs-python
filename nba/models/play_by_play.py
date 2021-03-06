import json

class PlayByPlay:
	"""
	Class representing a play-by-play instance.

	Various types:
	Jump ball: <name vs. <name> (<name> gains possession)

	<name> makes [2|3]-pt shot from <n> ft ((assist by <name>))?

	<name> misses [2|3]-pt shot from <n> ft

	<name makes free throw [1|2] of [1|2]

	(Defensive|Offensive) rebound by [<name>|Team]

	Shooting foul by <name> (drawn by <name>)
	Loose ball foul by <name>
	Personal foul by <name>
	Offensive charge foul by <name>

	Turnover by <name> (lost ball; steal by <name>)
	Turnover by <name> (bad pass; steal by <name>)
	Turnover by <name> (bad pass)
	Turnover by <name> (offensive foul)

	<name> enters game for <name>

	<team> full timeout
	Official timeout
	"""
	# Play types
	FOUL = "FOUL"
	FREE_THROW = "FREE_THROW"
	JUMP_BALL = "JUMP_BALL"
	REBOUND = "REBOUND"
	SHOT = "SHOT"
	SUBSTITUTION = "SUBSTITUTION"
	TIMEOUT = "TIMEOUT"
	TURNOVER = "TURNOVER"

	FOUL_SHOOTING = "Shooting"
	FOUL_LOOSE_BALL = "Loose ball"
	FOUL_PERSONAL = "Personal"
	FOUL_OFFENSIVE_CHARGE = "Offensive charge"

	REBOUND_DEFENSIVE = "defensive"
	REBOUND_OFFENSIVE = "offensive"

	TURNOVER_BAD_PASS = "bad pass"
	TURNOVER_LOST_BALL = "lost ball"
	TURNOVER_OFFENSIVE_FOUL = "offensive foul"

	def __init__(self, quarter=None, minutes=None, seconds=None, play_type=None,
					detail=None, secondary_play_type=None, players=None, home_players=None, away_players=None):
		# The quarter that is currently being played.
		self.quarter = quarter

		# The minute that the play occurred.
		self.minutes = minutes

		# The second that the play occurred
		self.seconds = seconds

		# The type of play.
		# - Jump ball
		# - made shot
		# - missed shot
		# - rebound
		# - foul
		# - substitution
		# - timeout
		self.play_type = play_type

		self.detail = detail

		# The secondary play type.
		#
		# For a shot, this will be either block or assist.
		self.secondary_play_type = secondary_play_type

		# The ids of players involved in this play.
		self.players = []

		# Flag to determine whether a shot was made or missed.  This is only relevant
		# when the play_type is "SHOT".
		self.shot_made = False

		# The distance (in feet) that the shot was taken from.
		self.shot_distance = 0

		# The point value (2 or 3) of the shot (if made).
		self.point_value = 0

		# The number of points the home team has
		self.home_score = 0

		# The number of points the visitor team has
		self.visitor_score = 0

		# An array of player ids representing players on the court for the home team
		self.home_players = home_players

		# An array of player ids representing players on the court for the away team
		self.away_players = away_players

	def to_json(self):
		"""
		Convert the PBP object to its JSON representation.  For PyMongo, the JSON rep will just
		be a dictionary.
		"""
		json_rep = {}
		for k in self.__dict__.keys():
			if self.__dict__[k] is not None:
				json_rep[k] = self.__dict__[k]

		return json_rep
