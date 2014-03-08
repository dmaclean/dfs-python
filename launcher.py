import logging
import sys

from models.injury_manager import InjuryManager

logging.basicConfig(level=logging.INFO)

if sys.argv[1] == "fix_injuries":
	try:
		season = int(sys.argv[2])
	except:
		logging.error("A season is required to be specified.")
		logging.error("Usage: python launcher fix_injuries <season>")
		exit()

	injury_manager = InjuryManager()
	injury_manager.fix_injuries(season)