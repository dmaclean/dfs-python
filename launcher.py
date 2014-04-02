import logging
import sys
from nba.import_salaries import SalaryImporter

from nba.models.injury_manager import InjuryManager
from nba.basketball import Processor
from nba.calculate_dvp_rank import DvPRankCalculator
from nba.fantasy_point_calculator import FantasyPointCalculator

logging.basicConfig(level=logging.INFO)

if sys.argv[1] == "fix_injuries":
	try:
		season = int(sys.argv[2])
	except ValueError, e:
		logging.error("A season is required to be specified.")
		logging.error("Usage: python launcher fix_injuries <season>")
		exit()

	injury_manager = InjuryManager()
	injury_manager.fix_injuries(season)

elif sys.argv[1] == "scrape_basketball_reference":
	processor = Processor()
	processor.readCLI()
	processor.process()

elif sys.argv[1] == "fantasy_point_calculator":
	fpc = FantasyPointCalculator()
	fpc.read_cli()
	fpc.run()

elif sys.argv[1] == "determine_injuries":
	for arg in sys.argv:
		if arg == "determine_injuries.py":
			pass
		else:
			pieces = arg.split("=")
			if pieces[0] == "season":
				season = int(pieces[1])
			elif pieces[0] == "type":
				type = pieces[1]

	injury_manager = InjuryManager()

	if type == "current":
		injury_manager.scrape_injury_report(season=season)
	elif type == "previous":
		injury_manager.calculate_injuries_from_gamelogs(season=season)

elif sys.argv[1] == "calculate_dvp_rank":
	calculator = DvPRankCalculator()
	calculator.read_cli()
	calculator.calculate(calculator.season, calculator.yesterday_only)

elif sys.argv[1] == "import_salaries":
	salary_importer = SalaryImporter()
	salary_importer.run()