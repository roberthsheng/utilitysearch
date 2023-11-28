import heapq
import csv
import random

# Uniformly returns location preference between a and b
def location_preference_assignments(a, b):
    return random.uniform(a, b)

# Uniformly returns edge preference between a and b
def edge_preference_assignments(a, b):
    return random.uniform(a, b)

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
def load_data(LocFile, EdgeFile):
    locations, edges = {}, {}
    with open(LocFile, 'r') as locs:
        next(csv.reader(locs))
        for label, lat, lon, _, _ in csv.reader(locs):
            pref = location_preference_assignments(0, 1)
            locations[label] = {'lat': float(lat), 'lon': float(lon), 'preference': pref}

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

    for i, (locationA, edge_label, locationB) in enumerate(path):
        edge = edges[edge_label]
        edge_distance = edge['distance']
        edge_preference = edge['preference']
        total_distance += edge_distance
        edge_time = edge_distance / x_mph  # Assuming x_mph is accessible here
        loc_preference = locations[locationB]['preference']
        loc_time = time_at_location(locations[locationB]['preference'])
        
        line = f"{i + 1}. {locationA} {locationB} {edge_label} {edge_preference} {edge_time} {loc_preference} {loc_time}"
        output_lines.append(line)
    
    output_lines.append(f"{startLoc} {total_preference} {total_distance} {total_time}")
    return output_lines

# Uses heap to find all possible roadtrips that start and end at the same location within a given time at a given speed
def RoundTripRoadTrip(startLoc, LocFile, EdgeFile, maxTime, x_mph, resultFile):
    locations, edges = load_data(LocFile, EdgeFile)
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
        print(f"solutionLabel  {startLoc}  {maxTime}  {x_mph}")
        for line in formatted_output:
            print(line)
        with open(resultFile, 'a') as f:
            f.write(f"solutionLabel  {startLoc}  {maxTime}  {x_mph}")
            f.write('\n')
            f.write('\n'.join(formatted_output))
            f.write('\n')
            f.write('\n')
        print()


# Test
if __name__ == "__main__":
    startLoc = input("Enter starting location: ")
    locationfile = input("Enter location file: ")
    edgefile = input("Enter edge file: ")
    maxTime = float(input("Enter maximum time: "))
    x_mph = float(input("Enter speed: "))
    resultsfile = input("Enter results file: ")
    RoundTripRoadTrip(startLoc, locationfile, edgefile, maxTime, x_mph, resultsfile)