To run code, use the following command:
```
python roundtriproadtrip.py
```
The program will then prompt you for the starting location, location file, edge file, maximum time, speed, and output file. 

For our test runs, we tested some cases where we should definitely be returning no solution (e.g. having speed = 1, max time = 98 should return no solution because nothing is within 100 miles round trip from any other point). Our solutions did not monitonically decrease strictly between each solution, but generally it seemed to decrease, and it would always lead to solutions that met the hard time constraint. We utilized a heap to be able to quickly find the next best solution.



Program Specification: Idea 6: Dynamic Preferences. In constructing a road trip, it may be that after adding a location with an attraction related to a theme (e.g., museum), a user’s preference for that theme with respect to subsequently selected locations may decrease (i.e., a user may not want too much of a good thing). Thus, theme preferences might change along a search path, and change differently along different search paths as search for complete road trips progresses.

Additionally, we wanted to add to this idea. In addition to having diminishing marginal returns for a certain theme, we are planning to create the functionality that when we prompt the user to "Continue" and keep searching for paths, we will also provide the option of changing the theme they prioritize when searching for feasible road trips.




Objective: To provide users with a program that could accept an input of their start location, available hours, and the speed they will drive alongside which location themes they most prefer (ex. Party, Nature, Food) and find a suitable round-trip road trip that would satisfy their specified criteria.

In this program, a locations.csv file (available cities and their themes) and edges.csv file (distance from location A to location B) were provided, but these could also be manipulated to fit a user’s idea of where they are willing to travel, and more specific themes they are looking for/interested in based on the cities they would like to travel to.

Outputted information includes which cities they travel between, the travel time, their preference level, the theme of each location, and in relation, the time spent at each location.




Functional Overview: Location Preference Assignment: This function assigns a preference score to each location based on how well it matches the user's preferred themes (requested in input).
Total Preference Calculation: This function calculates the total preference score of a road trip by summing the preference scores of individual locations and edges (routes) included in the trip.
Time Estimation Functions: These functions estimate the time spent at a location and the total time of a road trip, considering travel and activity durations.
Data Loading: The script reads location and edge data from CSV files and assigns preference scores based on user themes.
Route Planning and Optimization: The script uses a heap data structure to efficiently explore possible road trip routes, considering constraints like maximum time and distance. It optimizes for the highest preference score within these constraints, which is based on the themes present for a location.
Main Function (RoundTripRoadTrip): This is the main function that drives the road trip planning process, taking user inputs for themes, starting location, maximum time, speed, and file names. 






Usage of AI: Within project 4, we first utilized AI (specifically GPT4 from OpenAI’s ChatGPT software) to help understand the project 4 specification guidelines, to truly understand everything we were being asked to do within Idea 6 (Dynamic Preferences). We first used it to increase our understanding of how a diminishing utility might be implemented in a general sense, and then how it might interact with our previous project 3 and the idea of locations having themes. When considering how a user’s preference for that theme with respect to subsequently selected locations may decrease (i.e., a user may not want too much of a good thing), we inquired as to how we could utilize a base preference score that would progressively decrease every time a theme was revisited, as we kept track of which themes were visited and how often. In relation, we also understood that the time spent at that location should decrease, as they like it less.

After understanding the basic design idea of our program, we began to implement our dynamic preferences and modify the customizability/readability of the program such that it would function as an actual road trip guide. Although most of the code and scalar values (ex. Utility dropoff, time spent multipliers) were manually written, we did use ChatGPT in an incremental manner whenever we ran into unexpected errors, such as type consistency and so on. A good example of this is when we were updating the preferences for a visited_theme (present within a dictionary, where a key is a theme and the value being the number of times it was being visited) and making sure those changes were preserved across multiple edges, and also allowing the program to properly handle continuations (ex. Find new road trips with the same user inputted information). Overall, we used ChatGPT more for idea generation and design inquiries, as to how everything should function and work together to output proper road trips according to their dynamic preferences.




continue

