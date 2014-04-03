__author__ = 'dan'


class MLBUtilities:
	def __init__(self):
		pass

	@staticmethod
	def resolve_value(value, type):
		"""
		Convenience method for gracefully casting values to int or float.
		"""

		new_val = 0
		try:
			if type == "int":
				new_val = int(value)
			elif type == "float":
				new_val = float(value)
			else:
				new_val = value
		except ValueError:
			pass

		return new_val