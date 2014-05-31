import unittest
from datetime import date
from pymongo import MongoClient
from mlb.constants.mlb_constants import MLBConstants
from mlb.parsers.rotogrinders_ballpark_factors_parser import RotogrindersBallparkFactorsParser

__author__ = 'dan'


class TestRotogrindersBallparkFactorsParser(unittest.TestCase):
	def setUp(self):
		self.parser = RotogrindersBallparkFactorsParser()

		self.client = MongoClient('localhost', 27017)
		self.db = self.client[MLBConstants.MONGO_MLB_TEST_DB_NAME]
		self.ballparks_collection = self.db[MLBConstants.MONGO_MLB_BALLPARK_FACTORS_COLLECTION]

		self.parser.ballpark_factors_collection = self.ballparks_collection

	def tearDown(self):
		self.parser = None
		self.ballparks_collection.drop()

	def test_parse(self):
		f = open('test_files/rotogrinders_ballpark_factors.html')

		data = f.read()
		self.parser.parse(data)

		bpf = self.ballparks_collection.find_one({"date": str(date.today())})
		self.assertTrue(bpf is not None)

		# All
		self.assertTrue(bpf[MLBConstants.BPF_ALL]["ARI"][MLBConstants.BPF_BALLPARK] == "Chase Field")
		self.assertTrue(bpf[MLBConstants.BPF_ALL]["ARI"][MLBConstants.RUNS] == 0.989)
		self.assertTrue(bpf[MLBConstants.BPF_ALL]["ARI"][MLBConstants.HOME_RUNS] == 0.962)
		self.assertTrue(bpf[MLBConstants.BPF_ALL]["ARI"][MLBConstants.HITS] == 0.965)
		self.assertTrue(bpf[MLBConstants.BPF_ALL]["ARI"][MLBConstants.DOUBLES] == 1.046)
		self.assertTrue(bpf[MLBConstants.BPF_ALL]["ARI"][MLBConstants.TRIPLES] == 1.258)
		self.assertTrue(bpf[MLBConstants.BPF_ALL]["ARI"][MLBConstants.WALKS] == 1.001)

		self.assertTrue(bpf[MLBConstants.BPF_ALL]["WSN"][MLBConstants.BPF_BALLPARK] == "Nationals Park")
		self.assertTrue(bpf[MLBConstants.BPF_ALL]["WSN"][MLBConstants.RUNS] == 0.964)
		self.assertTrue(bpf[MLBConstants.BPF_ALL]["WSN"][MLBConstants.HOME_RUNS] == 0.737)
		self.assertTrue(bpf[MLBConstants.BPF_ALL]["WSN"][MLBConstants.HITS] == 1.062)
		self.assertTrue(bpf[MLBConstants.BPF_ALL]["WSN"][MLBConstants.DOUBLES] == 1.011)
		self.assertTrue(bpf[MLBConstants.BPF_ALL]["WSN"][MLBConstants.TRIPLES] == 0.539)
		self.assertTrue(bpf[MLBConstants.BPF_ALL]["WSN"][MLBConstants.WALKS] == 0.973)

		# Lefties


		# Righties

	def test_parse_already_exists(self):
		f = open('test_files/rotogrinders_ballpark_factors.html')

		data = f.read()
		self.parser.parse(data)

		self.parser.parse(data)

		bpf = self.ballparks_collection.find_one({"date": str(date.today())})
		self.assertTrue(bpf is not None)

		# All
		self.assertTrue(bpf[MLBConstants.BPF_ALL]["ARI"][MLBConstants.BPF_BALLPARK] == "Chase Field")
		self.assertTrue(bpf[MLBConstants.BPF_ALL]["ARI"][MLBConstants.RUNS] == 0.989)
		self.assertTrue(bpf[MLBConstants.BPF_ALL]["ARI"][MLBConstants.HOME_RUNS] == 0.962)
		self.assertTrue(bpf[MLBConstants.BPF_ALL]["ARI"][MLBConstants.HITS] == 0.965)
		self.assertTrue(bpf[MLBConstants.BPF_ALL]["ARI"][MLBConstants.DOUBLES] == 1.046)
		self.assertTrue(bpf[MLBConstants.BPF_ALL]["ARI"][MLBConstants.TRIPLES] == 1.258)
		self.assertTrue(bpf[MLBConstants.BPF_ALL]["ARI"][MLBConstants.WALKS] == 1.001)

		self.assertTrue(bpf[MLBConstants.BPF_ALL]["WSN"][MLBConstants.BPF_BALLPARK] == "Nationals Park")
		self.assertTrue(bpf[MLBConstants.BPF_ALL]["WSN"][MLBConstants.RUNS] == 0.964)
		self.assertTrue(bpf[MLBConstants.BPF_ALL]["WSN"][MLBConstants.HOME_RUNS] == 0.737)
		self.assertTrue(bpf[MLBConstants.BPF_ALL]["WSN"][MLBConstants.HITS] == 1.062)
		self.assertTrue(bpf[MLBConstants.BPF_ALL]["WSN"][MLBConstants.DOUBLES] == 1.011)
		self.assertTrue(bpf[MLBConstants.BPF_ALL]["WSN"][MLBConstants.TRIPLES] == 0.539)
		self.assertTrue(bpf[MLBConstants.BPF_ALL]["WSN"][MLBConstants.WALKS] == 0.973)

		# Lefties
		self.assertTrue(bpf[MLBConstants.BPF_VS_LHP]["ARI"][MLBConstants.BPF_BALLPARK] == "Chase Field")
		self.assertTrue(bpf[MLBConstants.BPF_VS_LHP]["ARI"][MLBConstants.BATTING_AVERAGE] == 0.254)
		self.assertTrue(bpf[MLBConstants.BPF_VS_LHP]["ARI"][MLBConstants.ON_BASE_PERCENTAGE] == 0.314)
		self.assertTrue(bpf[MLBConstants.BPF_VS_LHP]["ARI"][MLBConstants.SLUGGING_PERCENTAGE] == 0.393)
		self.assertTrue(bpf[MLBConstants.BPF_VS_LHP]["ARI"][MLBConstants.OPS] == 0.708)
		self.assertTrue(bpf[MLBConstants.BPF_VS_LHP]["ARI"][MLBConstants.HOME_RUNS_PER_AT_BAT] == 2.52)
		self.assertTrue(bpf[MLBConstants.BPF_VS_LHP]["ARI"][MLBConstants.TOTAL_BASES_PER_HIT] == 1.55)
		self.assertTrue(bpf[MLBConstants.BPF_VS_LHP]["ARI"][MLBConstants.EXTRA_BASE_HITS_PER_AT_BAT] == 8.23)

		self.assertTrue(bpf[MLBConstants.BPF_VS_LHP]["WSN"][MLBConstants.BPF_BALLPARK] == "Nationals Park")
		self.assertTrue(bpf[MLBConstants.BPF_VS_LHP]["WSN"][MLBConstants.BATTING_AVERAGE] == 0.254)
		self.assertTrue(bpf[MLBConstants.BPF_VS_LHP]["WSN"][MLBConstants.ON_BASE_PERCENTAGE] == 0.317)
		self.assertTrue(bpf[MLBConstants.BPF_VS_LHP]["WSN"][MLBConstants.SLUGGING_PERCENTAGE] == 0.376)
		self.assertTrue(bpf[MLBConstants.BPF_VS_LHP]["WSN"][MLBConstants.OPS] == 0.693)
		self.assertTrue(bpf[MLBConstants.BPF_VS_LHP]["WSN"][MLBConstants.HOME_RUNS_PER_AT_BAT] == 2.17)
		self.assertTrue(bpf[MLBConstants.BPF_VS_LHP]["WSN"][MLBConstants.TOTAL_BASES_PER_HIT] == 1.48)
		self.assertTrue(bpf[MLBConstants.BPF_VS_LHP]["WSN"][MLBConstants.EXTRA_BASE_HITS_PER_AT_BAT] == 7.24)

		# Righties
		self.assertTrue(bpf[MLBConstants.BPF_VS_RHP]["ARI"][MLBConstants.BPF_BALLPARK] == "Chase Field")
		self.assertTrue(bpf[MLBConstants.BPF_VS_RHP]["ARI"][MLBConstants.BATTING_AVERAGE] == 0.261)
		self.assertTrue(bpf[MLBConstants.BPF_VS_RHP]["ARI"][MLBConstants.ON_BASE_PERCENTAGE] == 0.325)
		self.assertTrue(bpf[MLBConstants.BPF_VS_RHP]["ARI"][MLBConstants.SLUGGING_PERCENTAGE] == 0.416)
		self.assertTrue(bpf[MLBConstants.BPF_VS_RHP]["ARI"][MLBConstants.OPS] == 0.741)
		self.assertTrue(bpf[MLBConstants.BPF_VS_RHP]["ARI"][MLBConstants.HOME_RUNS_PER_AT_BAT] == 2.87)
		self.assertTrue(bpf[MLBConstants.BPF_VS_RHP]["ARI"][MLBConstants.TOTAL_BASES_PER_HIT] == 1.6)
		self.assertTrue(bpf[MLBConstants.BPF_VS_RHP]["ARI"][MLBConstants.EXTRA_BASE_HITS_PER_AT_BAT] == 9.26)

		self.assertTrue(bpf[MLBConstants.BPF_VS_RHP]["WSN"][MLBConstants.BPF_BALLPARK] == "Nationals Park")
		self.assertTrue(bpf[MLBConstants.BPF_VS_RHP]["WSN"][MLBConstants.BATTING_AVERAGE] == 0.261)
		self.assertTrue(bpf[MLBConstants.BPF_VS_RHP]["WSN"][MLBConstants.ON_BASE_PERCENTAGE] == 0.316)
		self.assertTrue(bpf[MLBConstants.BPF_VS_RHP]["WSN"][MLBConstants.SLUGGING_PERCENTAGE] == 0.386)
		self.assertTrue(bpf[MLBConstants.BPF_VS_RHP]["WSN"][MLBConstants.OPS] == 0.703)
		self.assertTrue(bpf[MLBConstants.BPF_VS_RHP]["WSN"][MLBConstants.HOME_RUNS_PER_AT_BAT] == 2.42)
		self.assertTrue(bpf[MLBConstants.BPF_VS_RHP]["WSN"][MLBConstants.TOTAL_BASES_PER_HIT] == 1.48)
		self.assertTrue(bpf[MLBConstants.BPF_VS_RHP]["WSN"][MLBConstants.EXTRA_BASE_HITS_PER_AT_BAT] == 7.54)

if __name__ == '__main__':
	unittest.main()