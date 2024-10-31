import unittest
from unittest.mock import Mock
import tkinter as tk
from tkinter import ttk

class TestAnimalApp(unittest.TestCase):
    
    def setUp(self):
        self.root = tk.Tk()
        self.app = AnimalApp(self.root)
    
    def tearDown(self):
        self.root.destroy()

    def test_initial_dropdown_population(self):
        expected_animals = list(animal_info.keys())
        self.assertEqual(list(self.app.dropdown['values']), expected_animals)

    def test_add_to_favorites(self):
        self.app.selected_animal.set('Lion')
        self.app.add_to_favorites()
        
        self.assertIn('Lion', self.app.favorites)

        dropdown_values = list(self.app.dropdown['values'])
        self.assertEqual(dropdown_values[0], 'Lion')

    def test_search_animal_partial_match(self):
        self.app.search_var.set("Ti")
        self.app.search_animal(None)
        
        filtered_dropdown_values = list(self.app.dropdown['values'])
        self.assertIn('Tiger', filtered_dropdown_values)
        self.assertNotIn('Lion', filtered_dropdown_values)

    def test_search_animal_full_match(self):
        self.app.search_var.set("Elephant") 
        self.app.search_animal(None)

        filtered_dropdown_values = list(self.app.dropdown['values'])
        self.assertEqual(filtered_dropdown_values, ['Elephant'])

    def test_display_animal_info(self):
        self.app.selected_animal.set('Giraffe')
        self.app.display_animal_info(None)
        self.assertEqual(self.app.food_label.cget('text'), "Favorite Food: Leaves")
        self.assertEqual(self.app.origin_label.cget('text'), "Location of Origin: Africa")
        self.assertEqual(self.app.population_label.cget('text'), "Population Size: 68,000")

    def test_favorite_button_disabled_for_no_selection(self):
        self.app.selected_animal.set('')
        self.app.add_to_favorites()
        self.assertEqual(self.app.favorites, [])

    def test_update_dropdown_with_favorites(self):
        self.app.favorites.append('Penguin')
        self.app.update_dropdown()
        dropdown_values = list(self.app.dropdown['values'])
        self.assertEqual(dropdown_values[0], 'Penguin')

if __name__ == "__main__":
    unittest.main()

