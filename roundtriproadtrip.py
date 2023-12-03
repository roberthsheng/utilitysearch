import heapq
import csv
import random

# Returns location preference based on user preferred themes
def location_preference_assignments(location_themes, user_preferred_themes):
    base_pref = 0.2
    multiplier = 5
    for theme in user_preferred_themes:
        if theme in location_themes:
            return (base_pref * multiplier, theme.strip(' '))  # Return matching theme
        else:
            multiplier -= 0.5
    return (base_pref, "None")  # Return default theme if no match

# Uniformly returns edge preference between a and b
def edge_preference_assignments(a, b):
    # return random.uniform(a, b)
    return 0

# Returns total preference of a roadtrip
def total_preference(roadtrip, locations, edges):
    loc_pref = sum(locations[loc]['preference'] for loc in roadtrip['locations'])
    edge_pref = sum(edges[edge]['preference'] for edge in roadtrip['edges'])
    return loc_pref + edge_pref

# Returns total time at a location
def time_at_location(vloc):
    return vloc * 10

# Adds time on an edge
def add_time_on_edge(vedge):
    return time_at_location(vedge)

# Returns total time of a roadtrip
def time_estimate(roadtrip, x, edges):
    edge_time = sum((edges[edge]['distance'] / x) + add_time_on_edge(edges[edge]['preference']) for edge in roadtrip['edges'])
    loc_time = sum(time_at_location(edges[edge]['preference']) for edge in roadtrip['edges'])
    return edge_time + loc_time

# Loads data from location and edge files
def load_data(LocFile, EdgeFile, user_preferred_themes):
    locations, edges = {}, {}
    with open(LocFile, 'r') as locs:
        next(csv.reader(locs))
        for label, lat, lon, _, _, themes in csv.reader(locs):
            themes = themes.strip('"').split(',')  # Split themes into a list
            pref, theme = location_preference_assignments(themes, user_preferred_themes)
            locations[label] = {'lat': float(lat), 'lon': float(lon), 'preference': pref, 'themes': themes, 'determining_theme': theme}

    with open(EdgeFile, 'r') as edgs:
        next(csv.reader(edgs))
        for edgeLabel, label_A, label_B, actual_distance, _, _ in csv.reader(edgs):
            if 50 <= float(actual_distance) <= 200:
                pref = edge_preference_assignments(0, 0.1)
                edges[edgeLabel] = {'locationA': label_A, 'locationB': label_B, 'distance': float(actual_distance), 'preference': pref}
    return locations, edges

# Formats output
def format_output(path, locations, edges, total_preference, total_time):
    output_lines = []
    # output_lines.append(f"solutionLabel  {startLoc}  {}  {total_time}")
    total_distance = 0
    global visited_themes

    for i, (locationA, edge_label, locationB) in enumerate(path):
        visited_themes = {}
        edge = edges[edge_label]
        edge_distance = edge['distance']
        edge_preference = edge['preference']
        total_distance += edge_distance
        edge_time = edge_distance / x_mph  # Assuming x_mph is accessible here
        loc_theme = locations[locationB]['determining_theme']  # Get the theme
        if loc_theme in visited_themes:
            visited_themes[loc_theme] += 1
        else:
            visited_themes[loc_theme] = 1
        loc_preference = locations[locationB]['preference'] * (0.5 ** (visited_themes[loc_theme] - 1))
        loc_time = time_at_location(locations[locationB]['preference'])
        
        line = f"{i + 1}. {locationA} {locationB} {edge_label} {edge_preference} {edge_time} (Preference:{loc_preference}) (Theme: {loc_theme}) {loc_time}"
        output_lines.append(line)
    
    output_lines.append(f"{startLoc} {total_preference} {total_distance} {total_time}")
    return output_lines

# Uses heap to find all possible roadtrips that start and end at the same location within a given time at a given speed
def RoundTripRoadTrip(startLoc, LocFile, EdgeFile, maxTime, x_mph, resultFile):
    global visited_themes
    user_preferred_themes = input("Enter preferred themes, comma-separated, with higher preference themes first. \nChoose Themes: Weather, Sightseeing, Party, Sports, Fun, Family, Food, Nature, Relax, Celebration: ").split(',')
    locations, edges = load_data(LocFile, EdgeFile, user_preferred_themes)
    Frontier = [(-0, startLoc, 0, [], 0)]  # Negative sign for max heap
    visited = set()
    all_solutions = []

    while Frontier:
        total_preference, current_loc, total_time, path, edge_time = heapq.heappop(Frontier)
        total_preference = -total_preference

        if current_loc == startLoc and path:
            # Save this to the output list
            all_solutions.append({
                'path': path,
                'total_preference': total_preference,
                'total_time': total_time
            })
            cont = input("Continue? (yes/no): ")
            if cont.lower() == 'no':
                break
            visited = set()
            # clear visited themes dict
            visited_themes = {}
            continue
        
        visited.add(current_loc)

        for edge_label, edge_info in edges.items():
            if current_loc in {edge_info['locationA'], edge_info['locationB']}:
                next_loc = edge_info['locationB'] if current_loc == edge_info['locationA'] else edge_info['locationA']

                if next_loc in visited and next_loc != startLoc:
                    continue

                new_total_time = total_time + (edge_info['distance'] / x_mph) + add_time_on_edge(edge_info['preference'])
                new_edge_time = edge_time + (edge_info['distance'] / x_mph) + add_time_on_edge(edge_info['preference'])

                if new_total_time > maxTime:
                    continue

                current_to_next = True if current_loc == edge_info['locationA'] else False
                next_loc_preference = locations[next_loc]['preference'] if current_to_next else locations[current_loc]['preference']
                new_total_preference = total_preference + edge_info['preference'] + next_loc_preference

                new_path = path + [(current_loc, edge_label, next_loc)]
                heapq.heappush(Frontier, (-new_total_preference, next_loc, new_total_time, new_path, new_edge_time))

    for solution in all_solutions:
        formatted_output = format_output(solution['path'], locations, edges, solution['total_preference'], solution['total_time'])
        print(f"solutionLabel Start:{startLoc}  Hours:{maxTime}  MPH:{x_mph}")
        for line in formatted_output:
            print(line)
        with open(resultFile, 'a') as f:
            f.write(f"solutionLabel  Start:{startLoc}  Hours:{maxTime}  MPH:{x_mph}")
            f.write('\n')
            f.write("Format: Start End EdgeLabel EdgePreference EdgeTime LocationPreference (LocationTheme) LocationTime")
            f.write('\n')
            f.write('\n'.join(formatted_output))
            f.write('\n')
            f.write('\n')
        print()


# Test
if __name__ == "__main__":
    startLoc = input("Enter starting location (Example: NashvilleTN): ")
    locationfile = input("Enter location file (locations.csv): ")
    edgefile = input("Enter edge file (edges.csv): ")
    maxTime = float(input("Enter maximum time (in hours, ex. 50): "))
    x_mph = float(input("Enter speed (in mph, ex. 50): "))
    resultsfile = input("Enter results file (results.txt): ")
    # global visited themes dict keeping track of visited themes and number of times visited
    visited_themes = {}
    RoundTripRoadTrip(startLoc, locationfile, edgefile, maxTime, x_mph, resultsfile)