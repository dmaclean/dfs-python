from mlb.constants.mlb_constants import MLBConstants

__author__ = 'dan'


class StatCalculator:
	"""
	Computes stats not provided by BBR.
	"""
	def __init__(self):
		pass

	def calculate_woba(self, data):
		"""
		wOBA = (0.691*BB + 0.722*HBP + 0.884*1B + 1.257*2B + 1.593*3B + 2.058*HR) / (AB + BB - IBB + SF + HBP)
		"""
		singles = data[MLBConstants.HITS] - (data[MLBConstants.DOUBLES] + data[MLBConstants.TRIPLES] + data[MLBConstants.HOME_RUNS])

		try:
			return (0.691*data[MLBConstants.WALKS] + 0.722*data[MLBConstants.HIT_BY_PITCH] + 0.884*singles +
			        1.257*data[MLBConstants.DOUBLES] + 1.593*data[MLBConstants.TRIPLES] + 2.058*data[MLBConstants.HOME_RUNS]) / (data[MLBConstants.AT_BATS] + data[MLBConstants.WALKS] - data[MLBConstants.INTENTIONAL_WALKS] + data[MLBConstants.SACRIFICE_FLIES] + data[MLBConstants.HIT_BY_PITCH])
		except ZeroDivisionError as err:
			print "calculate_woba - division by zero, returning zero."
			return 0


	def calculate_fip(self, data):
		"""
		FIP = ((13*HR)+(3*(BB+HBP))-(2*K))/IP + constant
		"""
		return ((13*data[MLBConstants.HOME_RUNS])+(3*(data[MLBConstants.WALKS] + data[MLBConstants.HIT_BY_PITCH])-(2*data[MLBConstants.STRIKE_OUTS]))/data[MLBConstants.INNINGS_PITCHED]) + 3.08