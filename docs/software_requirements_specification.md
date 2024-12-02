# Overview

The purpose of a Software Requirements Specification (SRS) skeleton document is to provide a structured framework for defining and organizing the key elements of a software project. It helps guide the detailed documentation of the system’s functional and non-functional requirements. Also, it sorts the requirements based on the features they are relevant to. This helps when developing and testing your code. You are able to look at whatever feature you are working on and see the exact requirements relevent to your work that you need to meet. Another added benefit is that it documents all of your requirements and features in one easy access spot. Overall, this document serves as a guide to what features the project has and the requirements related to each of those features. 

# Functional Requirements

1. Search Bar
   1. The interface shall include a search bar that allows users to input the name of a species.
   2. The user shall be able to search by partial or full animal name
   3. The app shall update the dropdown list in real-time as the user types in the search bar.
   4. The app shall clearly label the search bar.
   5. The text in the search bar shall be white text.

2. Favorite Button
   1. Users shall have the ability to mark species as favorites.
   2. The favorites shall be displayed at the top of the dropdown menu.
   3. After a species is marked favorite, it will be added to a favorites list. 
   4. Users shall be able to favorite up to all of the listed species.
   5. The favorite button shall appear to the right of the drop down menu. 

3. Drop Down Menu
   1. There shall be a drop down menu of possible species to choose from. 
   2. When clicked, the drop down menu shall be populated with animals within the database. 
   3. Animals that are marked as favorited, will be at the top of the drop down menu above animals that are not favorited. 
   4. The drop down menu shall only display species that match or partially match search bar entries if something is in the search bar. 
   5. The drop down menu shall appear directly under the search bar. 

# Non-Functional Requirements

1. Search Bar
   1. The drop down menu shall be updated based on the search bar entry within 1.5 seconds. 
   2. If a user searches for something not in the species list, an error message shall occur.
   3. The search bar shall function consistently across different operating systems and computer screen sizes. 
   4. The search bar shall be clearly idenfifiable by 95% of users.
   5. The search bar shall only allow species within the drop down menu to be selected.

2. Favorite Button
   1. When the user favorites an animal, it shall be added to a favorites list within 2 seconds. 
   2. Favorites button shall be large enough that users hit the button on atlesat 95% of attempts.
   3.  The favorite button shall maintain the displayed information without changing any of it. 
   4. The favorite button shall be labeled that 95% of users can identify it.
   5. The system shall prevent duplicate favorite entries for the same item. 

3. Drop Down Menu 
   1. The drop down menu shall consistently have animals that are in the favorited list at the top of the menu. 
   2. The drop down menu shall be able to handle the addition of new species without crashing. 
   3. The drop down menu shall be updated based on the search entries within 1.5 seconds. 
   4. The drop down menu shall follow a color scheme that follows the whole app interfae.
   5. The drop down menu shall have an arrow icon, making it clearly identifiable. 
