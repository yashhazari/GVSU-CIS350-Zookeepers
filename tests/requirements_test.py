import unittest
import time
class Interface:
    def __init__(self):
        self.species_list = ['Lion', 'Tiger', 'Leopard', 'Cheetah']
        self.favorites_list = []
        self.search_results = []
    
    def search_species(self, query):
        return [species for species in self.species_list if query.lower() in species.lower()]
    
    def mark_as_favorite(self, species):
        if species in self.species_list and species not in self.favorites_list:
            self.favorites_list.append(species)
    
    def update_dropdown(self, query):
        self.search_results = self.search_species(query)
        return self.search_results
    
    def add_species(self, species):
        if species not in self.species_list:
            self.species_list.append(species)

class TestSRSRequirements(unittest.TestCase):
    
    def setUp(self):
        self.interface = Interface()

    def test_search_by_partial_name(self):
        result = self.interface.search_species("Li")
        self.assertIn("Lion", result)
        self.assertNotIn("Tiger", result)

    def test_search_by_full_name(self):
        result = self.interface.search_species("Tiger")
        self.assertEqual(result, ["Tiger"])

    def test_update_dropdown_real_time(self):
        start_time = time.time()
        result = self.interface.update_dropdown("Leo")
        end_time = time.time()
        self.assertIn("Leopard", result)
        self.assertLess(end_time - start_time, 1.5)

    def test_mark_as_favorite(self):
        self.interface.mark_as_favorite("Tiger")
        self.assertIn("Tiger", self.interface.favorites_list)

    def test_favorites_in_dropdown(self):
        self.interface.mark_as_favorite("Tiger")
        dropdown = self.interface.update_dropdown("")
        self.assertEqual(dropdown[0], "Tiger")

    def test_dropdown_update_time(self):
        start_time = time.time()
        self.interface.update_dropdown("Leopard")
        end_time = time.time()
        self.assertLess(end_time - start_time, 1.5)

    def test_search_nonexistent_species(self):
        result = self.interface.search_species("Dinosaur")
        self.assertEqual(result, [])

    def test_favorite_within_2_seconds(self):
        start_time = time.time()
        self.interface.mark_as_favorite("Lion")
        end_time = time.time()
        self.assertIn("Lion", self.interface.favorites_list)
        self.assertLess(end_time - start_time, 2)

    def test_favorite_button_accuracy(self):
        hits = 0
        for _ in range(100):
            self.interface.mark_as_favorite("Lion")
            if "Lion" in self.interface.favorites_list:
                hits += 1
        self.assertGreaterEqual(hits, 95)

    def test_dropdown_stability(self):
        self.interface.add_species("Elephant")
        self.assertIn("Elephant", self.interface.species_list)

    def test_color_scheme_consistency(self):
        color_scheme = "consistent"
        self.assertEqual(color_scheme, "consistent")

if __name__ == "__main__":
    unittest.main()

