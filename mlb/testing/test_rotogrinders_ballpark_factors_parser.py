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

	def tearDown(self):
		self.parser = None

	def test_parse(self):
		f = open('test_files/rotogrinders_ballpark_factors.html')

		self.parser.parse(f.readlines())

		bpf = self.ballparks_collection.find_one({"date": str(date.today())})
		self.assertTrue(bpf is not None)

		self.assertTrue(bpf[MLBConstants.BPF_ALL]["ARI"][MLBConstants.BPF_BALLPARK] == "Chase Field")
		self.assertTrue(bpf[MLBConstants.BPF_ALL]["ARI"][MLBConstants.RUNS] == 0.989)
		self.assertTrue(bpf[MLBConstants.BPF_ALL]["ARI"][MLBConstants.HOME_RUNS] == 0.962)
		self.assertTrue(bpf[MLBConstants.BPF_ALL]["ARI"][MLBConstants.HITS] == 0.965)
		self.assertTrue(bpf[MLBConstants.BPF_ALL]["ARI"][MLBConstants.DOUBLES] == 1.046)
		self.assertTrue(bpf[MLBConstants.BPF_ALL]["ARI"][MLBConstants.TRIPLES] == 1.258)
		self.assertTrue(bpf[MLBConstants.BPF_ALL]["ARI"][MLBConstants.WALKS] == 1.001)

if __name__ == '__main__':
	unittest.main()