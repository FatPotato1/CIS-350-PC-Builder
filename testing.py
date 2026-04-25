"""
The testing file will give tests using unittests for auto_generate.py, compatability.py,
data_loading.py, and save_load.py

Anything else that can be logically tested will be tested with a a manual test that will be marked
with a test ID
"""

import unittest as unittest
import os
import json
import auto_generate
from data_loading import load_games, load_gpu_rankings, load_cpu_rankings
import data_loading
import components
import save_load
import compatibility

class Data_loading_tests(unittest.TestCase):
    """
    Unit tests for functions in the data_loading module.
    """


    def test_load_games_returns_list(self):

        games = data_loading.load_games()
        self.assertIsInstance(games, list)
        self.assertGreater(len(games), 0)


    def test_gpu_rankings_returns_dict(self):

        rankings = data_loading.load_gpu_rankings()
        self.assertIsInstance(rankings, dict)


    def test_cpu_rankings_returns_dict(self):

        rankings = data_loading.load_cpu_rankings()
        self.assertIsInstance(rankings, dict)


    def test_extract_gpu_model(self):

        result = data_loading.extract_gpu_model("RTX 5090")
        self.assertTrue(result is None or isinstance(result, str))


    def test_extract_cpu_model(self):
        result = data_loading.extract_cpu_model("Core i9-14900KS")
        self.assertTrue(result is None or isinstance(result, str))


GAMES = load_games()
GPU_RANKINGS = load_gpu_rankings()
CPU_RANKINGS = load_cpu_rankings()


class TestAutoGenerate(unittest.TestCase):

    def test_generate_pc_returns_three_tuple(self):
        result = auto_generate.generate_pc(
            "Fortnite", "rec", GAMES, CPU_RANKINGS, GPU_RANKINGS,
            "Intel", "NVIDIA", None
        )
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 3)

    def test_generate_cpu_intel(self):
        cpu = auto_generate.generate_cpu(
            "Fortnite", "rec", GAMES, CPU_RANKINGS, "Intel", None
        )
        self.assertIsInstance(cpu, str)

    def test_generate_cpu_amd(self):
        cpu = auto_generate.generate_cpu(
            "Fortnite", "rec", GAMES, CPU_RANKINGS, "AMD", None
        )
        self.assertIsInstance(cpu, str)

    def test_generate_cpu_empty_rankings_returns_none(self):
        cpu = auto_generate.generate_cpu(
            "Fortnite", "rec", GAMES, {}, "Intel", None
        )
        self.assertIsNone(cpu)

    def test_generate_gpu_nvidia(self):
        gpu = auto_generate.generate_gpu(
            "Fortnite", "rec", GAMES, GPU_RANKINGS, "NVIDIA", None
        )
        self.assertIsInstance(gpu, str)

    def test_generate_gpu_empty_rankings_returns_none(self):
        gpu = auto_generate.generate_gpu(
            "Fortnite", "rec", GAMES, {}, "NVIDIA", None
        )
        self.assertIsNone(gpu)

    def test_generate_ram_rec(self):
        ram = auto_generate.generate_ram("Fortnite", "rec", GAMES, None)
        self.assertIsInstance(ram, str)

    def test_generate_ram_min(self):
        ram = auto_generate.generate_ram("Fortnite", "min", GAMES, None)
        self.assertIsInstance(ram, str)

    def test_get_price_known(self):
        price = auto_generate._get_price("NVIDIA GPUs", "RTX 5090")
        self.assertEqual(price, 2000)

    def test_get_price_unknown_returns_none(self):
        price = auto_generate._get_price("NVIDIA GPUs", "RTX 9999")
        self.assertIsNone(price)

    def test_get_build_price_known_value(self):
        build = {
            "GPU": "RTX 5090", "GPU_Brand": "NVIDIA",
            "CPU": "Core i9-14900K", "CPU_Brand": "Intel",
            "Motherboard": "ASUS Prime Z790-A",
            "Case": "DIYPC Wood Black Case",
            "Storage": "Samsung 870 EVO 1TB SSD",
            "PSU": "Corsair RM1000x 1000W 80+ Gold",
            "RAM": "CORSAIR VENGEANCE RGB 16GB DDR5",
        }
        self.assertEqual(auto_generate.get_build_price(build), 3392)

    def test_get_build_price_empty_build(self):
        self.assertEqual(auto_generate.get_build_price({}), 0)

    def test_fixed_component_cost_positive(self):
        cost = auto_generate._fixed_component_cost("Intel")
        self.assertGreater(cost, 0)

    def test_generate_pc_budget_too_low(self):
        result = auto_generate.generate_pc_budget(
            "Fortnite", GAMES, CPU_RANKINGS, GPU_RANKINGS,
            "Intel", "NVIDIA", 10
        )
        self.assertEqual(result, (None, None, None))

    def test_generate_pc_budget_reasonable(self):
        gpu, cpu, ram = auto_generate.generate_pc_budget(
            "Fortnite", GAMES, CPU_RANKINGS, GPU_RANKINGS,
            "Intel", "NVIDIA", 1500
        )
        self.assertIsInstance(gpu, str)
        self.assertIsInstance(cpu, str)
        self.assertIsInstance(ram, str)

    def test_ram_price_known(self):
        price = auto_generate._ram_price("CORSAIR VENGEANCE RGB 32GB DDR5")
        self.assertGreater(price, 0)

    def test_ram_price_none_returns_zero(self):
        self.assertEqual(auto_generate._ram_price(None), 0)

    def test_pick_budget_ram_adequate_budget(self):
        gpu_prices = [("RTX 5050", 249)]
        cpu_prices = [("Core i3-14100", 149)]
        ram = auto_generate._pick_budget_ram(1000, gpu_prices, cpu_prices)
        self.assertIsInstance(ram, str)

    def test_pick_budget_ram_too_low_returns_none(self):
        gpu_prices = [("RTX 5050", 249)]
        cpu_prices = [("Core i3-14100", 149)]
        ram = auto_generate._pick_budget_ram(1, gpu_prices, cpu_prices)
        self.assertIsNone(ram)


class Save_load_tests(unittest.TestCase): # Testing for the save_load.py file
    """
    Unit tests for functions in the save_load module.
    """


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

    class TestIntegration(unittest.TestCase):

        def test_full_pc_generation_pipeline(self):

            games = data_loading.load_games()
            cpu_rankings = data_loading.load_cpu_rankings()
            gpu_rankings = data_loading.load_gpu_rankings()

            gpu, cpu, ram = auto_generate.generate_pc(
                "Fortnite",
                "rec",
                games,
                cpu_rankings,
                gpu_rankings,
                "Intel",
                "NVIDIA",
                None
            )

            self.assertIsNotNone(cpu)
            self.assertIsNotNone(gpu)
            self.assertIsNotNone(ram)

        def test_build_price_integration(self):

            build = {
                "GPU": "RTX 5090",
                "GPU_Brand": "NVIDIA",
                "CPU": "Core i9-14900KS",
                "CPU_Brand": "Intel",
                "Motherboard": "ASUS Prime Z790-A",
                "Case": "DIYPC Wood Black Case",
                "Storage": "Samsung 870 EVO 1TB SSD",
                "PSU": "Corsair RM1000x 1000W 80+ Gold",
                "RAM": "CORSAIR VENGEANCE RGB 16GB DDR5"
            }

            price = auto_generate.get_build_price(build)

            self.assertIsInstance(price, int)
            self.assertGreater(price, 0)

        def test_save_and_load_build_integration(self):

            build = {
                "CPU": "i5",
                "GPU": "RTX 3060",
                "RAM": "16GB"
            }

            save_load.save_build("integration_test_build", build)
            loaded = save_load.load_build("integration_test_build")

            self.assertEqual(loaded, build)

        def test_delete_build_integration(self):

            build = {"CPU": "i5"}

            save_load.save_build("delete_test", build)
            save_load.delete_build("delete_test")

            result = save_load.load_build("delete_test")
            self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()

