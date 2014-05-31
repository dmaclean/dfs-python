from bs4 import BeautifulSoup
from datetime import date
from pymongo import MongoClient
from mlb.constants.mlb_constants import MLBConstants

__author__ = 'dan'


class RotogrindersBallparkFactorsParser:
	"""
	Parser for the Rotogrinders park factors page.
	"""
	def __init__(self):
		self.client = MongoClient('localhost', 27017)
		self.db = self.client[MLBConstants.MONGO_MLB_DB_NAME]
		self.ballpark_factors_collection = self.db[MLBConstants.MONGO_MLB_BALLPARK_FACTORS_COLLECTION]

	def process_general_batters(self, factors, tds):
		"""
		Processes the first table encountered, which is general stats for both lefty and righty batters.
		"""
		bp = ""
		i = 0
		for td in tds:
			if i == 0:
				# Ballpark name
				bp = td.text
			elif i == 1:
				team = td.span.text
				if team not in factors:
					factors[team] = {}

				factors[team][MLBConstants.BPF_BALLPARK] = bp.replace("\t", "")
			elif i == 2:
				factors[team][MLBConstants.RUNS] = float(td.text)
			elif i == 3:
				factors[team][MLBConstants.HOME_RUNS] = float(td.text)
			elif i == 4:
				factors[team][MLBConstants.HITS] = float(td.text)
			elif i == 5:
				factors[team][MLBConstants.DOUBLES] = float(td.text)
			elif i == 6:
				factors[team][MLBConstants.TRIPLES] = float(td.text)
			elif i == 7:
				factors[team][MLBConstants.WALKS] = float(td.text)

			i += 1

	def process_lefty_righty_batters(self, factors, tds):
		"""
		Processes the second table encountered, which is stats for lefty batters.
		"""
		bp = ""
		i = 0
		for td in tds:
			if i == 0:
				# Ballpark name
				bp = td.text
			elif i == 1:
				team = td.span.text
				if team not in factors:
					factors[team] = {}

				factors[team][MLBConstants.BPF_BALLPARK] = bp.replace("\t", "")
			elif i == 2:
				# Just specifies we're dealing with lefties or righties; we already know this.
				pass
			elif i == 3:
				factors[team][MLBConstants.BATTING_AVERAGE] = float(td.text)
			elif i == 4:
				factors[team][MLBConstants.ON_BASE_PERCENTAGE] = float(td.text)
			elif i == 5:
				factors[team][MLBConstants.SLUGGING_PERCENTAGE] = float(td.text)
			elif i == 6:
				factors[team][MLBConstants.OPS] = float(td.text)
			elif i == 7:
				factors[team][MLBConstants.HOME_RUNS_PER_AT_BAT] = float(td.text.replace("%", ""))
			elif i == 8:
				factors[team][MLBConstants.TOTAL_BASES_PER_HIT] = float(td.text)
			elif i == 9:
				factors[team][MLBConstants.EXTRA_BASE_HITS_PER_AT_BAT] = float(td.text.replace("%", ""))

			i += 1

	def parse(self, data, d=date.today()):
		soup = BeautifulSoup(data)

		tables = soup.find_all("table", attrs={"class": "sortable"})

		table_num = 0
		factors = {
			MLBConstants.BPF_ALL: {},
		    MLBConstants.BPF_VS_LHP: {},
		    MLBConstants.BPF_VS_RHP: {}
		}

		factors_all = factors[MLBConstants.BPF_ALL]
		factors_lhb = factors[MLBConstants.BPF_VS_LHP]
		factors_rhb = factors[MLBConstants.BPF_VS_RHP]

		for table in tables:
			trs = table.find_all("tr")

			for tr in trs:
				tds = tr.find_all("td")

				if table_num == 0:
					self.process_general_batters(factors_all, tds)
				elif table_num == 1:
					self.process_lefty_righty_batters(factors_lhb, tds)
				elif table_num == 2:
					self.process_lefty_righty_batters(factors_rhb, tds)

			table_num += 1

		# Did we already scrape this?
		existing_factors = self.ballpark_factors_collection.find_one({"date": str(d)})
		if existing_factors is not None:
			existing_factors[MLBConstants.BPF_ALL] = factors_all
			existing_factors[MLBConstants.BPF_VS_LHP] = factors_lhb
			existing_factors[MLBConstants.BPF_VS_RHP] = factors_rhb
			self.ballpark_factors_collection.save(existing_factors)
		else:
			self.ballpark_factors_collection.save({"date": str(d), MLBConstants.BPF_ALL: factors_all, MLBConstants.BPF_VS_LHP: factors_lhb, MLBConstants.BPF_VS_RHP: factors_rhb})