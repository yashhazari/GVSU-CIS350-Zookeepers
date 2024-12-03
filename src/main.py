import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import requests
import wikipediaapi
import io
import re
from bs4 import BeautifulSoup


class AnimalApp:
    """
    Class for the application.  This class was developed by Yash Hazari (the lead SW developer) with
    aid from Lucian Whitaker.  The class and system were tested by Lucian Whitaker (the lead test engineer)
    with aid from Yash Hazari.  The purpose of this class is to create the variables needed to allow for
    all features of the app including species image/info display, drop down menu, favorite button, and 
    search bar.  This class also defines all methods related to making those features fully functional 
    and usable in a real setting.
    """
    def __init__(self, root):
        self.root = root
        self.root.title("Zookeepers - CIS350 - Project")
        self.root.geometry("1000x675")
        self.root.configure(bg='#FFFFE0')

        # List of animals to be featured
        self.all_animals = [
            "Lion", "Tiger", "Elephant", "Chicken", "Sea Star", "Giraffe", "Monkey", "Penguin", "Bear", "Zebra",
            "Koala", "Kangaroo", "Cheetah", "Leopard", "Wolf", "Fox", "Panda", "Rhino",
            "Hippo", "Crocodile", "Alligator", "Dolphin", "Whale", "Shark", "Eagle",
            "Falcon", "Hawk", "Parrot", "Toucan", "Sloth", "Ostrich", "Flamingo",
            "Peacock", "Camel", "Meerkat", "Otter", "Seal", "Walrus", "Armadillo",
            "Porcupine", "Platypus", "Turtle", "Tortoise", "Snake", "Iguana",
            "Lemur", "Chameleon", "Orangutan", "Baboon", "Coyote", "Moose", "Elk",
            "Reindeer", "Bison", "Buffalo", "Antelope", "Wombat", "Tasmanian Devil",
            "Puffin", "Polar Bear", "Grizzly Bear", "Black Bear", "Raccoon", "Skunk",
            "Opossum", "Hedgehog", "Badger", "Ferret", "Weasel", "Mongoose",
            "Hyena", "Jackal", "Caracal", "Serval", "Ocelot", "Snow Leopard",
            "Sea Lion", "Manatee", "Dugong", "Narwhal", "Beluga", "Octopus",
            "Squid", "Jellyfish", "Starfish", "Clownfish", "Sea Turtle", "Lobster",
            "Crab", "Shrimp", "Coral", "Manta Ray", "Stingray"
        ]
        self.animal_data = {}  # Allows for cache of recently accessed species
        self.favorite_animals = set()  # Set for favorite species

        # Search bar label
        self.search_label = tk.Label(root, text="Search:", bg='#FFFFE0', fg='black', anchor="w")
        self.search_label.grid(row=0, column=0, padx=10, pady=(10, 0), sticky='w')

        # Search bar creation
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(root, textvariable=self.search_var)
        self.search_entry.grid(row=1, column=0, padx=10, pady=(0, 10), sticky='ew')
        self.search_entry.bind('<KeyRelease>', self.search_animal)

        # Drop-down menu creation
        self.selected_animal = tk.StringVar()
        self.dropdown = ttk.Combobox(root, textvariable=self.selected_animal, state="readonly")
        self.dropdown.grid(row=2, column=0, padx=10, pady=10, sticky='ew')
        self.dropdown.bind("<<ComboboxSelected>>", self.display_animal_info)
        self.update_dropdown()

        # Favorite button creation
        self.favorite_button = ttk.Button(root, text="Favorite", command=self.add_to_favorites)
        self.favorite_button.grid(row=2, column=1, padx=10, pady=10, sticky='ew')

        # Labels for displaying species info
        self.info_label = tk.Label(
            root,
            text="",
            bg='#FFFFE0',  # Sky blue background
            fg='black',  # Black text
            justify="left",
            wraplength=500,  # Updated wrap length to 500
            anchor="w",  # Align text to the left
            font=('Arial', 18)
        )
        self.info_label.grid(row=3, column=0, padx=10, pady=10, sticky='w')

        # Image display creation
        self.image_label = tk.Label(root, bg='#FFFFE0')
        self.image_label.grid(row=3, column=1, rowspan=4, padx=10, pady=10)

        # Make columns resizable to allow for formatting
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

        # List of countries for possible locations
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
        # Searches for search entry through list to update dropdown accordingly
        search_text = self.search_var.get().lower()
        filtered_animals = [animal for animal in self.all_animals if search_text in animal.lower()]
        self.dropdown['values'] = filtered_animals

    def add_to_favorites(self):
        # Adds species to favorites set
        animal = self.selected_animal.get()
        if animal and animal not in self.favorite_animals:
            self.favorite_animals.add(animal)
            self.update_dropdown()

    def display_animal_info(self, event):
        # Gets the animal data if not in cache and displays it
        animal = self.selected_animal.get()
        if animal:
            if animal not in self.animal_data:
                # Fetch data if not already cached
                self.fetch_animal_data(animal)
            # Display data
            self.show_animal_data(animal)

    def fetch_animal_data(self, animal):
        # Uses wikpedia data library to find species info and put it in animal_data
        wiki = wikipediaapi.Wikipedia(
            language='en',
            user_agent="AnimalApp/1.0 (mailto:hazariy@mail.gvsu.edu)"
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
        # Calls various functions to gather all the relevant species data
        details = {}

        details['Average Life Expectancy'] = self.extract_life_expectancy(text)
        details['Habitat'] = self.extract_habitat(text)
        details['Diet'] = self.extract_diet(text)
        details['Locations Found'] = self.extract_locations(text)
        details['Class'] = self.extract_class(text)
        details['Reproduction'] = self.extract_reproduction(text)
        
        # Remove empty sections
        return {k: v for k, v in details.items() if v and v != "Not available"}

    def extract_life_expectancy(self, text):
        # Reg ex to capture life expectancy
        match = re.search(r"(\d{2,3})\s*(?:years?|lifespan)", text, re.IGNORECASE)
        if match:
            life_expectancy = match.group(1)
            # Bug fix for 10 year life span
            if life_expectancy == "000":
                return "10 years"
            return life_expectancy + " years"
        return "Life expectancy not available"

    def extract_habitat(self, text):
        # Searches for keywords in species data page to find habitat
        habitat_keywords = ["forest", "rainforest", "grasslands", "desert", "polar", "aquatic", "mountain", "coastal"]
        for habitat in habitat_keywords:
            if habitat in text.lower():
                return habitat.capitalize()
        return "Habitat not clearly defined"

    def extract_diet(self, text):
        # Searches for keywords in species data page to find diet
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
        # Compares species data page to list of all countries to see where species are found
        countries_found = []
        for country in self.country_list:
            if country.lower() in text.lower():
                countries_found.append(country)
        return ", ".join(countries_found) if countries_found else "Location information not available"

    def extract_class(self, text):
        # Searches for keywords in species data page to find animal class
        classes = [
            "Mammalia", "Aves", "Reptile", "Reptilia", "Amphibia", "Pisces", "Insecta",
            "Arachnida", "Crustacea", "Cephalopoda", "Bird", "Fish", "Chondrichthyes"
        ]
        for animal_class in classes:
            if animal_class.lower() in text.lower():
                return animal_class
        return "Class not defined"

    def extract_reproduction(self, text):
        # Searches for keywords in species data page to find reproduction/birth type
        reproduction_keywords = {
            "Live Birth (Viviparous)": [
                "birth", "live birth", "viviparous", "viviparity", "placenta", "placental",
                "gestation", "mammalian birth", "parturition", "giving birth", "offspring born alive"
            ],
            "Asexual": [
                "asexual reproduction", "budding", "cloning", "asexual", "fragmentation",
                "binary fission", "parthenogenesis", "regeneration", "self-replication",
                "vegetative reproduction", "mitotic division", "spore formation", "gemmulation",
                "fission", "cytoplasmic division", "somatic cell division", "clonal propagation",
                "clonal growth", "multiplying", "asexual reproduction by mitosis", "fission"
            ],
            "Egg Laying (Oviparous)": [
                "oviparous", "laying eggs", "egg-laying", "eggs", "oviparity",
                "nesting eggs", "egg deposition", "hatching", "egg incubation"
            ]
        }
        
        for reproduction_type, keywords in reproduction_keywords.items():
            for keyword in keywords:
                # Match exact phrases
                if re.search(r'\b' + re.escape(keyword) + r'\b', text.lower()):
                    return reproduction_type
        return "Reproduction type not specified"

    def fetch_image(self, animal, url):
        # Go to image url found in species data page and extract the image
        try:
            # Construct Wikipedia URL
            wiki_url = f"https://en.wikipedia.org/wiki/{animal.replace(' ', '_')}"
            response = requests.get(wiki_url)
            if response.status_code != 200:
                print(f"Failed to fetch page for {animal}. Status code: {response.status_code}")
                self.animal_data[animal]["image"] = None
                return
            # Parse HTML for image
            soup = BeautifulSoup(response.content, 'html.parser')
            # Find the first image
            infobox = soup.find('table', {'class': 'infobox'})
            if infobox:
                img_tag = infobox.find('img')
                if img_tag:
                    img_url = "https:" + img_tag['src']
                    # Extract the image
                    img_response = requests.get(img_url, stream=True)
                    if img_response.status_code == 200:
                        image = Image.open(io.BytesIO(img_response.content))
                        # Resize image
                        image = image.resize((300, 300), Image.Resampling.LANCZOS)
                        self.animal_data[animal]["image"] = ImageTk.PhotoImage(image)
                        return
                    
            print(f"No image found for {animal} in the infobox.")
            self.animal_data[animal]["image"] = None
        except Exception as e:
            print(f"Error fetching image for {animal}: {e}")
            self.animal_data[animal]["image"] = None

    def show_animal_data(self, animal):
        # Displays species info in formatted way
        data = self.animal_data[animal]
        info = data.get("info", {"Error": "No information available."})

        formatted_info = "\n\n".join([f"{key}: {value}" for key, value in info.items()])
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

