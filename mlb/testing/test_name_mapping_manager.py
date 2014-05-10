import unittest
from mlb.constants.mlb_constants import MLBConstants
from mlb.models.name_mapping_manager import NameMappingManager

__author__ = 'dan'

class TestNameMappingManager(unittest.TestCase):
	def setUp(self):
		self.name_mapping_manager = NameMappingManager(testing=True)

	def tearDown(self):
		self.name_mapping_manager.name_mapping_collection.drop()
		self.name_mapping_manager = None

	def test_get_player_name_has_match(self):
		self.name_mapping_manager.name_mapping_collection.save({
			MLBConstants.MONGO_MLB_NAME_MAPPING_BBR: "Daniel MacLean",
		    MLBConstants.MONGO_MLB_NAME_MAPPING_ROTOWIRE: "Dan MacLean"
		})

		name = self.name_mapping_manager.get_player_name(MLBConstants.MONGO_MLB_NAME_MAPPING_ROTOWIRE, MLBConstants.MONGO_MLB_NAME_MAPPING_BBR, "Dan MacLean")
		self.assertTrue(name == "Daniel MacLean")

	def test_get_player_name_no_match(self):
		name = self.name_mapping_manager.get_player_name(MLBConstants.MONGO_MLB_NAME_MAPPING_ROTOWIRE, MLBConstants.MONGO_MLB_NAME_MAPPING_BBR, "Dan MacLean")
		self.assertTrue(name is None)

if __name__ == "__main__":
	unittest.main()