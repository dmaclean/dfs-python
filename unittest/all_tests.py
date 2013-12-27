import unittest
import test_fantasy_point_calculator
import test_import_salaries
import test_projections

##########################
# FantasyPointCalculator
##########################
suite = unittest.TestLoader().loadTestsFromTestCase(test_fantasy_point_calculator.TestFantasyPointCalculator)
unittest.TextTestRunner(verbosity=2).run(suite)

##################
# SalaryImporter
##################
suite = unittest.TestLoader().loadTestsFromTestCase(test_import_salaries.TestSalaryImporter)
unittest.TextTestRunner(verbosity=2).run(suite)

###############
# Projections
###############
suite = unittest.TestLoader().loadTestsFromTestCase(test_projections.TestProjections)
unittest.TextTestRunner(verbosity=2).run(suite)