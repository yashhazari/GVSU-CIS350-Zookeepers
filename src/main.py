import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import requests
import wikipediaapi
import io
import re

class AnimalApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Zookeeper App")
        self.root.geometry("900x600")
        self.root.configure(bg='#87CEEB')  # Sky blue background

        # List of animals
        self.all_animals = ["Lion", "Tiger", "Elephant", "Giraffe", "Monkey", "Penguin", "Bear", "Zebra", "Koala", "Kangaroo"]
        self.animal_data = {}  # Cache for fetched animal data
        self.favorite_animals = set()  # Set to store favorite animals

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
        self.favorite_button.grid(row=1, column=1, padx=10, pady=10, sticky='ew')

        # Labels for displaying animal details
        self.info_label = tk.Label(
            root,
            text="",
            bg='#87CEEB',  # Sky blue background
            fg='black',  # Black text
            justify="left",
            wraplength=500,  # Updated wrap length to 500
            anchor="w"  # Align text to the left
        )
        self.info_label.grid(row=2, column=0, padx=10, pady=10, sticky='w')

        # Image display
        self.image_label = tk.Label(root, bg='#87CEEB')
        self.image_label.grid(row=2, column=1, rowspan=4, padx=10, pady=10)

        # Make columns resizable
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

        # List of countries (to be used for location extraction)
        self.country_list = [
            "Afghanistan", "Albania", "Algeria", "Andorra", "Angola", "Antigua and Barbuda", "Argentina", "Armenia",
            "Australia", "Austria", "Azerbaijan", "Bahamas", "Bahrain", "Bangladesh", "Barbados", "Belarus", "Belgium",
            "Belize", "Benin", "Bhutan", "Bolivia", "Bosnia and Herzegovina", "Botswana", "Brazil", "Brunei", "Bulgaria",
            "Burkina Faso", "Burundi", "Cabo Verde", "Cambodia", "Cameroon", "Canada", "Central African Republic", "Chad",
            "Chile", "China", "Colombia", "Comoros", "Congo", "Costa Rica", "Croatia", "Cuba", "Cyprus", "Czech Republic",
            "Denmark", "Djibouti", "Dominica", "Dominican Republic", "Ecuador", "Egypt", "El Salvador", "Equatorial Guinea",
            "Eritrea", "Estonia", "Eswatini", "Ethiopia", "Fiji", "Finland", "France", "Gabon", "Gambia", "Georgia", "Germany",
            "Ghana", "Greece", "Grenada", "Guatemala", "Guinea", "Guinea-Bissau", "Guyana", "Haiti", "Honduras", "Hungary",
            "Iceland", "India", "Indonesia", "Iran", "Iraq", "Ireland", "Israel", "Italy", "Jamaica", "Japan", "Jordan",
            "Kazakhstan", "Kenya", "Kiribati", "Korea, North", "Korea, South", "Kuwait", "Kyrgyzstan", "Laos", "Latvia", "Lebanon",
            "Lesotho", "Liberia", "Libya", "Liechtenstein", "Lithuania", "Luxembourg", "Madagascar", "Malawi", "Malaysia",
            "Maldives", "Mali", "Malta", "Marshall Islands", "Mauritania", "Mauritius", "Mexico", "Micronesia", "Moldova",
            "Monaco", "Mongolia", "Montenegro", "Morocco", "Mozambique", "Myanmar", "Namibia", "Nauru", "Nepal", "Netherlands",
            "New Zealand", "Nicaragua", "Niger", "Nigeria", "North Macedonia", "Norway", "Oman", "Pakistan", "Palau", "Panama",
            "Papua New Guinea", "Paraguay", "Peru", "Philippines", "Poland", "Portugal", "Qatar", "Romania", "Russia", "Rwanda",
            "Saint Kitts and Nevis", "Saint Lucia", "Saint Vincent and the Grenadines", "Samoa", "San Marino", "Sao Tome and Principe",
            "Saudi Arabia", "Senegal", "Serbia", "Seychelles", "Sierra Leone", "Singapore", "Slovakia", "Slovenia", "Solomon Islands",
            "Somalia", "South Africa", "South Sudan", "Spain", "Sri Lanka", "Sudan", "Suriname", "Sweden", "Switzerland", "Syria",
            "Taiwan", "Tajikistan", "Tanzania", "Thailand", "Timor-Leste", "Togo", "Tonga", "Trinidad and Tobago", "Tunisia", "Turkey",
            "Turkmenistan", "Tuvalu", "Uganda", "Ukraine", "United Arab Emirates", "United Kingdom", "United States", "Uruguay",
            "Uzbekistan", "Vanuatu", "Vatican City", "Venezuela", "Vietnam", "Yemen", "Zambia", "Zimbabwe"
        ]

    def update_dropdown(self):
        # Combine favorites at the top and all other animals
        animals_sorted = list(self.favorite_animals) + [animal for animal in self.all_animals if animal not in self.favorite_animals]
        self.dropdown['values'] = animals_sorted
        self.dropdown.set('')

    def search_animal(self, event):
        search_text = self.search_var.get().lower()
        filtered_animals = [animal for animal in self.all_animals if search_text in animal.lower()]
        self.dropdown['values'] = filtered_animals

    def add_to_favorites(self):
        animal = self.selected_animal.get()
        if animal and animal not in self.favorite_animals:
            self.favorite_animals.add(animal)
            self.update_dropdown()

    def display_animal_info(self, event):
        animal = self.selected_animal.get()
        if animal:
            if animal not in self.animal_data:
                # Fetch data if not already cached
                self.fetch_animal_data(animal)
            # Display data
            self.show_animal_data(animal)

    def fetch_animal_data(self, animal):
        wiki = wikipediaapi.Wikipedia(
            language='en',
            user_agent="AnimalApp/1.0 (mailto:your-email@example.com)"
        )
        page = wiki.page(animal)
        if page.exists():
            full_text = page.text
            self.animal_data[animal] = {
                "info": self.extract_details(full_text)
            }
            self.fetch_image(animal, page.fullurl)
        else:
            self.animal_data[animal] = {"info": {"Error": "Information not found."}}

    def extract_details(self, text):
        details = {}

        # Extract average life expectancy
        details['Average Life Expectancy'] = self.extract_life_expectancy(text)

        # Extract habitat
        details['Habitat'] = self.extract_habitat(text)

        # Extract diet (carnivore, herbivore, omnivore)
        details['Diet'] = self.extract_diet(text)

        # Extract countries where found
        details['Locations Found'] = self.extract_locations(text)

        # Remove empty or unavailable sections
        return {k: v for k, v in details.items() if v and v != "Not available"}

    def extract_life_expectancy(self, text):
        # Extract life expectancy (using regular expression for a number pattern)
        match = re.search(r'(\d{1,2}[-\d]{1,2})\s*years?|\d+(\.\d+)?\s*(years?)\s*life expectancy', text, re.IGNORECASE)
        if match:
            return match.group(1) + " years"
        return "Life expectancy not available"

    def extract_habitat(self, text):
        habitat_keywords = ["forest", "rainforest", "grasslands", "desert", "polar", "aquatic", "mountain", "coastal"]
        for habitat in habitat_keywords:
            if habitat in text.lower():
                return habitat.capitalize()
        return "Habitat not clearly defined"

    def extract_diet(self, text):
        diet_keywords = {
            "herbivore": ["grass", "leaves", "plant"],
            "carnivore": ["meat", "fish", "carnivorous"],
            "omnivore": ["fruits", "insects", "omnivorous"]
        }
        for diet, keywords in diet_keywords.items():
            for keyword in keywords:
                if keyword in text.lower():
                    return diet.capitalize()
        return "Diet not defined"

    def extract_locations(self, text):
        countries_found = []
        for country in self.country_list:
            if country.lower() in text.lower():
                countries_found.append(country)
        return ", ".join(countries_found) if countries_found else "Location information not available"

    def fetch_image(self, animal, url):
        try:
            response = requests.get(f"https://en.wikipedia.org/wiki/Special:FilePath/{animal.lower()}.jpg", stream=True)
            if response.status_code == 200:
                image = Image.open(io.BytesIO(response.content))
                image = image.resize((300, 300), Image.ANTIALIAS)
                self.animal_data[animal]["image"] = ImageTk.PhotoImage(image)
            else:
                self.animal_data[animal]["image"] = None
        except Exception as e:
            print(f"Image fetch error for {animal}: {e}")
            self.animal_data[animal]["image"] = None

    def show_animal_data(self, animal):
        data = self.animal_data[animal]
        info = data.get("info", {"Error": "No information available."})

        formatted_info = "\n".join([f"{key}: {value}" for key, value in info.items()])
        self.info_label.config(text=formatted_info)

        image = data.get("image")
        if image:
            self.image_label.config(image=image)
            self.image_label.image = image
        else:
            self.image_label.config(image="", text="Image not available")


if __name__ == "__main__":
    root = tk.Tk()
    app = AnimalApp(root)
    root.mainloop()

