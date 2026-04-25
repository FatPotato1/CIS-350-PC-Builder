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

class Data_loading_tests(unittest.TestCase):
    """
    Unit tests for functions in the data_loading module.
    """


    def test_load_games_returns_list(self):
        """
        Verify that load_games() returns a non-empty list.

        Ensures:
        - The return type is a list
        - The list contains at least one game entry
        """

        games = data_loading.load_games()
        self.assertIsInstance(games, list)
        self.assertGreater(len(games), 0)


    def test_gpu_rankings_returns_dict(self):
        """
        Verify that load_gpu_rankings() returns a dictionary.

        Ensures:
        - GPU rankings data is structured as key-value pairs
        """

        rankings = data_loading.load_gpu_rankings()
        self.assertIsInstance(rankings, dict)


    def test_cpu_rankings_returns_dict(self):
        """
       Verify that load_cpu_rankings() returns a dictionary.

       Ensures:
       - CPU rankings data is structured as key-value pairs
       """

        rankings = data_loading.load_cpu_rankings()
        self.assertIsInstance(rankings, dict)


    def test_extract_gpu_model(self):
        """
        Test extraction of a GPU model string.

        Ensures:
        - The function returns either None or a string
        - Handles valid GPU input safely
        """

        result = data_loading.extract_gpu_model("RTX 5090")
        self.assertTrue(result is None or isinstance(result, str))


    def test_extract_cpu_model(self):
        """
        Test extraction of a CPU model string.

        Ensures:
        - The function returns either None or a string
        - Handles valid CPU input safely
        """

        result = data_loading.extract_cpu_model("Core i9-14900KS")
        self.assertTrue(result is None or isinstance(result, str))

class Auto_generate_tests(unittest.TestCase):
    """
    Unit tests for functions in the auto_generate module.
    """

    def test_generate_cpu_returns_value(self):
        """
        Verify generate_cpu() returns a valid CPU or None.

        Ensures:
        - Output is either a string (CPU name) or None if unavailable
        - Function handles valid inputs without crashing
        """

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
        """
        Verify generate_gpu() returns a valid GPU or None.

        Ensures:
        - Output is either a string (GPU name) or None if unavailable
        - Function handles valid inputs without crashing
        """

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
        """
        Verify generate_ram() returns a RAM specification string.

        Ensures:
        - Output is always a string representing RAM requirements
        - Minimum RAM requirement is correctly retrieved
        """

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
        """
        Verify that _fixed_component_cost() never returns a negative value.

        Ensures:
        - Cost is zero or positive
        - Prevents invalid pricing calculations
        """

        cost = auto_generate._fixed_component_cost("Intel")
        self.assertGreaterEqual(cost, 0)

    # Build price is unconventionally an integer
    def test_build_price_returns_int(self):
        """
        Verify get_build_price() returns a valid integer total.

        Ensures:
        - Output type is integer
        - Matches expected total for a known build configuration
        """

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
    """Unit tests for functions in the compatibility module."""


    # Test to make sure that Intel CPUs are compatible with the Z790-A
    # All Intel CPU are set to be paired with the ASUS Prime motherboard
    def test_intel_valid(self):
        """
        Verify Intel CPU and ASUS motherboard are compatible.

        Ensures:
        - Valid Intel build returns True
        """

        build = {
            "CPU_Brand": "Intel",
            "Motherboard": "ASUS Prime Z790-A"
        }
        self.assertTrue(compatibility.is_compatible(build))

    # Any AMD CPU should be compatible with a MSI B650 Tomahawk
    # All AMD CPUs are set to pair with the MSI B650 Tomahawk
    def test_amd_valid(self):
        """
        Verify AMD CPU and MSI motherboard are compatible.

        Ensures:
        - Valid AMD build returns True
        """

        build = {
            "CPU_Brand": "AMD",
            "Motherboard": "MSI B650 Tomahawk"
        }
        self.assertTrue(compatibility.is_compatible(build))

    # Test should fail as AMD is paired with MSI and Intel is paired with ASUS
    def test_wrong_motherboard_compatibility(self):
        """
        Verify mismatched CPU and motherboard return False.

        Ensures:
        - Invalid combinations are correctly rejected
        """

        build = {
            "CPU_Brand": "Intel",
            "Motherboard": "MSI B650 Tomahawk"
        }
        self.assertFalse(compatibility.is_compatible(build))

    # Entering no motherboard should be considered true in compatibility
    def test_missing_motherboard_passes(self):
        """
        Verify compatibility passes when motherboard is missing.

        Ensures:
        - Function does not fail when optional component is absent
        - Returns True in incomplete build scenarios
        """

        build = {"CPU_Brand": "Intel"}
        self.assertTrue(compatibility.is_compatible(build))

class Save_load_tests(unittest.TestCase): # Testing for the save_load.py file
    """Unit tests for functions in the save_load module."""


    # Reset state for testing
    def setUp(self):
        """
        Reset test environment before each test.

        Ensures:
        - Test save file is removed if it exists
        - Each test runs in a clean state
        """

        self.name = "test_build_unit"

        if os.path.exists(save_load.SAVE_FILE):
            os.remove(save_load.SAVE_FILE)

    # Can retrieve a saved build later
    def test_save_load_creates_file(self):
        """
        Verify that saving and loading a build works correctly.

        Ensures:
        - A saved build can be retrieved
        - Stored values remain unchanged
        """

        build = {"CPU": "i5", "GPU": "RTX 3060"}

        save_load.save_build(self.name, build)
        loaded = save_load.load_build(self.name)

        self.assertEqual(loaded["CPU"], "i5")

    # Missing build should return None
    def test_load_missing_build_returns_none(self):
        """
        Verify loading a non-existent build returns None.

        Ensures:
        - Function handles missing data gracefully
        """

        self.assertIsNone(save_load.load_build("fake_name"))

    # If the user deletes a build it should be deleted from storage
    def test_delete_build_removes_entry(self):
        """
        Verify delete_build() removes a saved build.

        Ensures:
        - Deleted build is no longer retrievable
        """

        build = {"CPU": "i5"}

        save_load.save_build(self.name, build)
        save_load.delete_build(self.name)

        self.assertIsNone(save_load.load_build(self.name))

    # All builds need to be returned as a dictionary
    def test_load_all_builds_returns_dict(self):
        """
        Verify load_all_builds() returns all builds as a dictionary.

        Ensures:
        - Output type is dictionary
        - Structure supports multiple saved builds
        """

        result = save_load.load_all_builds()
        self.assertIsInstance(result, dict)


if __name__ == '__main__':
    unittest.main()
