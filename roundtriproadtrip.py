import heapq
import time
import math
import csv
import random

def location_preference_assignments(a, b):
    return random.uniform(a, b)

def edge_preference_assignments(a, b):
    return random.uniform(a, b)

def total_preference(roadtrip, locations, edges):
    loc_pref = sum(locations[loc]['preference'] for loc in roadtrip['locations'])
    edge_pref = sum(edges[edge]['preference'] for edge in roadtrip['edges'])
    return loc_pref + edge_pref

def time_at_location(vloc):
    return vloc * 10  # Example function, can be modified

def add_time_on_edge(vedge):
    return time_at_location(vedge)

def time_estimate(roadtrip, x, edges):
    edge_time = sum((edges[edge]['distance'] / x) + add_time_on_edge(edges[edge]['preference']) for edge in roadtrip['edges'])
    loc_time = sum(time_at_location(edges[edge]['preference']) for edge in roadtrip['edges'])
    return edge_time + loc_time

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

def write_to_file(output, filename):
    with open(filename, 'w') as f:
        for line in output:
            f.write(line + "\n")

def RoundTripRoadTrip(startLoc, LocFile, EdgeFile, maxTime, x_mph, resultFile):
    locations, edges = load_data(LocFile, EdgeFile)
    Frontier = [(0, startLoc, 0, [], 0)]
    visited = set()
    output = []

    while Frontier:
        total_preference, current_loc, total_time, path, edge_time = heapq.heappop(Frontier)
        total_preference = -total_preference  # Since we are maximizing preference, but heapq is a min-heap

        if current_loc == startLoc and path:
            # Save this to the output list
            output.append(f"Path: {path}\nTotal Preference: {total_preference}\nTotal Time: {total_time}\n")

            cont = input("Continue? (yes/no): ")
            if cont.lower() == 'no':
                break
            continue

        visited.add(current_loc)

        for edge_label, edge_info in edges.items():
            if current_loc in {edge_info['locationA'], edge_info['locationB']}:
                next_loc = edge_info['locationB'] if current_loc == edge_info['locationA'] else edge_info['locationA']

                if next_loc in visited:
                    continue

                new_total_time = total_time + (edge_info['distance'] / x_mph) + add_time_on_edge(edge_info['preference'])
                new_edge_time = edge_time + (edge_info['distance'] / x_mph) + add_time_on_edge(edge_info['preference'])

                if new_total_time > maxTime:
                    continue

                new_total_preference = total_preference + edge_info['preference'] + locations[next_loc]['preference']
                new_path = path + [edge_label]
                heapq.heappush(Frontier, (-new_total_preference, next_loc, new_total_time, new_path, new_edge_time))

        visited.remove(current_loc)  # Remove from visited set to allow revisiting locations

    write_to_file(output, resultFile)

# Test
if __name__ == "__main__":
    startLoc = input("Enter starting location: ")
    maxTime = float(input("Enter maximum time: "))
    x_mph = float(input("Enter speed: "))
    RoundTripRoadTrip(startLoc, 'locations.csv', 'edges.csv', maxTime, x_mph, 'results/{startLoc}_{maxTime}_{x_mph}.txt'.format(startLoc=startLoc, maxTime=maxTime, x_mph=x_mph))