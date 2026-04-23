"""
The testing file will give tests using unittests for auto_generate.py, compatability.py,
data_loading.py, and save_load.py

Anything else that can be logically tested will be tested with a a manual test that will be marked
with a test ID
"""

import unittest as unittest
import auto_generate
import data_loading
import components
import save_load
import compatibility
import os
import json

class Data_loading_tests(unittest.TestCase): # Testing of the data_loading.py file

    # Needs to return a list of games
    def test_load_games_returns_list(self):
        games = data_loading.load_games()
        self.assertIsInstance(games, list)
        self.assertGreater(len(games), 0)

    # GPU rankings should be loaded as a dictionary
    def test_gpu_rankings_returns_dict(self):
        rankings = data_loading.load_gpu_rankings()
        self.assertIsInstance(rankings, dict)

    # CPU rankings should be loaded as a dictionary
    def test_cpu_rankings_returns_dict(self):
        rankings = data_loading.load_cpu_rankings()
        self.assertIsInstance(rankings, dict)

    # Make sure the code is extracting the gpu correctly
    # Use the first gpu in the csv to make it easier to track
    def test_extract_gpu_model(self):
        result = data_loading.extract_gpu_model("RTX 5090")
        self.assertTrue(result is None or isinstance(result, str))

    # Make sure the code is extracting the cpu correctly
    # Use the first cpu in the csv to make it easier to track
    def test_extract_cpu_model(self):
        result = data_loading.extract_cpu_model("Core i9-14900KS")
        self.assertTrue(result is None or isinstance(result, str))

class Auto_generate_tests(unittest.TestCase): # Testing of the auto_generate.py file

    # generate_cpu should return a cpu if there is one
    # If there is no cpu, return None
    def test_generate_cpu_returns_value(self):
        result = auto_generate.generate_cpu(
            "Fortnite",
            "min",
            auto_generate.components.hardware,
            auto_generate.components.prices,
            "Intel",
            None
        )
        self.assertTrue(result is None or isinstance(result, str))

    # generate_gpu should return a gpu if there is one
    # If there is no gpu, return None
    def test_generate_gpu_returns_value(self):
        result = auto_generate.generate_gpu(
            "Fortnite",
            "min",
            auto_generate.components.hardware,
            auto_generate.components.prices,
            "NVIDIA",
            None
        )
        self.assertTrue(result is None or isinstance(result, str))

    # generate_ram should return the minimum ram needed for a game
    def test_generate_ram_min(self):
        games = auto_generate.load_games() if hasattr(auto_generate, "load_games") else None
        result = auto_generate.generate_ram(
            "Fortnite",
            "min",
            games,
            None
        )
        self.assertIsInstance(result, str)

    # There cannot be a cost of zero
    def test_fixed_component_cost_non_negative(self):
        cost = auto_generate._fixed_component_cost("Intel")
        self.assertGreaterEqual(cost, 0)

    # Build price is unconventionally an integer
    def test_build_price_returns_int(self):
        build = {
            "GPU": "RTX 5090",
            "GPU_Brand": "NVIDIA",
            "CPU": "Core i9-14900K",
            "CPU_Brand": "Intel",
            "Motherboard": "ASUS Prime Z790-A",
            "Case": "DIYPC Wood Black Case",
            "Storage": "Samsung 870 EVO 1TB SSD",
            "PSU": "Corsair RM1000x 1000W 80+ Gold",
            "RAM": "CORSAIR VENGEANCE RGB 16GB DDR5"
        }

        result = auto_generate.get_build_price(build)
        self.assertIsInstance(result, int)
        self.assertEquals(result,3392)

class Compatibility_tests(unittest.TestCase): # Testing of the compatability.py file

    # Test to make sure that Intel CPUs are compatible with the Z790-A
    # All Intel CPU are set to be paired with the ASUS Prime motherboard
    def test_intel_valid(self):
        build = {
            "CPU_Brand": "Intel",
            "Motherboard": "ASUS Prime Z790-A"
        }
        self.assertTrue(compatibility.is_compatible(build))

    # Any AMD CPU should be compatible with a MSI B650 Tomahawk
    # All AMD CPUs are set to pair with the MSI B650 Tomahawk
    def test_amd_valid(self):
        build = {
            "CPU_Brand": "AMD",
            "Motherboard": "MSI B650 Tomahawk"
        }
        self.assertTrue(compatibility.is_compatible(build))

    # Test should fail as AMD is paired with MSI and Intel is paired with ASUS
    def test_wrong_motherboard_compatibility(self):
        build = {
            "CPU_Brand": "Intel",
            "Motherboard": "MSI B650 Tomahawk"
        }
        self.assertFalse(compatibility.is_compatible(build))

    # Entering no motherboard should be considered true in compatibility
    def test_missing_motherboard_passes(self):
        build = {"CPU_Brand": "Intel"}
        self.assertTrue(compatibility.is_compatible(build))

class Save_load_tests(unittest.TestCase): # Testing for the save_load.py file

    # Reset state for testing
    def setUp(self):
        self.name = "test_build_unit"

        if os.path.exists(save_load.SAVE_FILE):
            os.remove(save_load.SAVE_FILE)

    # Can retrieve a saved build later
    def test_save_load_creates_file(self):
        build = {"CPU": "i5", "GPU": "RTX 3060"}

        save_load.save_build(self.name, build)
        loaded = save_load.load_build(self.name)

        self.assertEqual(loaded["CPU"], "i5")

    # Missing build should return None
    def test_load_missing_build_returns_none(self):
        self.assertIsNone(save_load.load_build("fake_name"))

    # If the user deletes a build it should be deleted from storage
    def test_delete_build_removes_entry(self):
        build = {"CPU": "i5"}

        save_load.save_build(self.name, build)
        save_load.delete_build(self.name)

        self.assertIsNone(save_load.load_build(self.name))

    # All builds need to be returned as a dictionary
    def test_load_all_builds_returns_dict(self):
        result = save_load.load_all_builds()
        self.assertIsInstance(result, dict)
if __name__ == '__main__':
    unittest.main()
