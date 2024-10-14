import tkinter as tk
from tkinter import ttk

# Animal data: favorite food, location of origin, and population size
animal_info = {
    'Lion': {'food': 'Meat', 'origin': 'Africa', 'population': '20,000'},
    'Tiger': {'food': 'Meat', 'origin': 'Asia', 'population': '3,900'},
    'Elephant': {'food': 'Grass', 'origin': 'Africa/Asia', 'population': '415,000'},
    'Giraffe': {'food': 'Leaves', 'origin': 'Africa', 'population': '68,000'},
    'Monkey': {'food': 'Fruits', 'origin': 'Tropical Regions', 'population': 'Varies by species'},
    'Penguin': {'food': 'Fish', 'origin': 'Antarctica', 'population': '12 million'},
    'Bear': {'food': 'Fish', 'origin': 'North America, Europe, Asia', 'population': '200,000 (brown bears)'},
    'Zebra': {'food': 'Grass', 'origin': 'Africa', 'population': '500,000'},
    'Koala': {'food': 'Eucalyptus Leaves', 'origin': 'Australia', 'population': '80,000'},
    'Kangaroo': {'food': 'Grass', 'origin': 'Australia', 'population': '50 million'},
}

class AnimalApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Zookeeper App")
        self.root.geometry("900x600")  # Larger window size
        self.root.configure(bg='#d9ead3')

        # Colors for a colorful UI
        self.label_color = '#6fa8dc'
        self.button_color = '#f4cccc'

        # List of animals
        self.all_animals = list(animal_info.keys())
        self.favorites = []

        # Search bar
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(root, textvariable=self.search_var)
        self.search_entry.grid(row=0, column=0, padx=10, pady=10, sticky='ew')
        self.search_entry.bind('<KeyRelease>', self.search_animal)

        # Drop-down menu
        self.selected_animal = tk.StringVar()
        self.dropdown = ttk.Combobox(root, textvariable=self.selected_animal, state="readonly")
        self.dropdown.grid(row=1, column=0, padx=10, pady=10, sticky='ew')
        self.dropdown.bind("<<ComboboxSelected>>", self.display_animal_info)
        self.update_dropdown()

        # Favorite button
        self.favorite_button = ttk.Button(root, text="Favorite", command=self.add_to_favorites)
        self.favorite_button.grid(row=2, column=0, padx=10, pady=10, sticky='ew')

        # Labels for displaying animal details
        self.food_label = tk.Label(root, text="", bg=self.root['bg'], fg=self.label_color)
        self.food_label.grid(row=3, column=0, padx=10, pady=5, sticky='ew')

        self.origin_label = tk.Label(root, text="", bg=self.root['bg'], fg=self.label_color)
        self.origin_label.grid(row=4, column=0, padx=10, pady=5, sticky='ew')

        self.population_label = tk.Label(root, text="", bg=self.root['bg'], fg=self.label_color)
        self.population_label.grid(row=5, column=0, padx=10, pady=5, sticky='ew')

        # Make columns resizable for responsiveness
        self.root.grid_columnconfigure(0, weight=1)

    def update_dropdown(self, filtered_animals=None):
        if filtered_animals is None:
            filtered_animals = self.all_animals

        # Combine favorites and non-favorites
        all_animals_sorted = self.favorites + [animal for animal in filtered_animals if animal not in self.favorites]
        self.dropdown['values'] = all_animals_sorted
        self.dropdown.set('')

    def add_to_favorites(self):
        current_selection = self.selected_animal.get()
        if current_selection and current_selection not in self.favorites:
            self.favorites.append(current_selection)
            self.update_dropdown()

    def search_animal(self, event):
        search_text = self.search_var.get().lower()
        filtered_animals = [animal for animal in self.all_animals if search_text in animal.lower()]
        self.update_dropdown(filtered_animals)

    def display_animal_info(self, event):
        # Get the selected animal
        animal = self.selected_animal.get()
        if animal in animal_info:
            # Fetch and display the animal's details
            info = animal_info[animal]
            self.food_label.config(text=f"Favorite Food: {info['food']}")
            self.origin_label.config(text=f"Location of Origin: {info['origin']}")
            self.population_label.config(text=f"Population Size: {info['population']}")
        else:
            self.food_label.config(text="")
            self.origin_label.config(text="")
            self.population_label.config(text="")

if __name__ == "__main__":
    root = tk.Tk()
    app = AnimalApp(root)
    root.mainloop()
