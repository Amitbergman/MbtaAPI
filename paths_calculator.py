# This method is getting a dictionary of stops -> List[route] as an input
# And returns a dictionary d, so that d[i][j] is a string representing a path from stop i to stop j
# For example, if d[i][j] = "red -> green" it means that you can take the red line from station i and then switch to the green line and then get to station j 
# The calculation is based on the fact that path of length t from i to j is actually the problem of finding k such that there is a path of length 1 from i to k and path of length t-1 from k to j
# Hence, we given all paths of length <t we can calculate all paths of length t
def calculate_all_paths(stop_to_routes_dict: dict[any, list[str]]) -> dict[any, dict[any, str]]:
    stops = stop_to_routes_dict.keys()

    # Generate a reverse dictionary (routes -> stops)
    route_to_stops_dict = dict()
    for stop in stop_to_routes_dict.keys():
        routes = stop_to_routes_dict[stop]
        for route in routes:
            if (route in route_to_stops_dict):
                route_to_stops_dict[route].append(stop)
            else:
                route_to_stops_dict[route] = [stop]

    # Final routes will be the matrix that we will eventually return from this method
    final_routes = dict()
    for i in stops:
        final_routes[i] = dict()
        final_routes[i][i] = f"Stay in {i}..."

    # First, are building a dictionary D so that D[i][j] is a path you can take from station i to station j directly (path of length 1)
    # If there is no such path, D[i] will not include the key j
    # For example d["harvard"]["porter"] = "Red Line"
    distance_1_matrix = dict()
    for source_station in stops:
        distance_1_matrix[source_station] = dict()
        for route in stop_to_routes_dict[source_station]:
            # We go over all routes that go through this top 
            # and add all the stops in this route to the possible stops to get from current one (also remember the route)
            possible_stops = route_to_stops_dict[route]
            stops_to_add = [s for s in possible_stops if s != source_station]
            for destination in stops_to_add:
                distance_1_matrix[source_station][destination] = route
                # Remembering the path from current stop -> destination
                final_routes[source_station][destination] = route

    # Now we will use the matrix for distance i in order to build a matrix of distance i+1
    # This loop will run at most #Routes times, since you cannot switch a train more than #Routes times -> so there will be no path of length (#Routes + 1)
    prev_distance = 1
    routes_by_distance = dict()
    routes_by_distance[1] = distance_1_matrix
    while True:
        # In iteration i of this loop, we are finding paths of length i between all the stops to all the destinations
        current_distance = prev_distance + 1
        current_routes = dict()
        anything_changed = False

        for source_station in stops:
            current_routes[source_station] = dict()
            distance_1_from_source = distance_1_matrix[source_station]
            # This is the way to assemble a path of length t: Find a path of length 1 from current station to destination `dest``, and attach it to a path of length t-1 from `dest`
            for first_hop, route_to_first_hop in distance_1_from_source.items():
                distance_t_minus_one_from_first_hop = routes_by_distance[prev_distance][first_hop] # Stations that are accessible by path of length t-1 from the `dest`
                for final_destination, route_to_final in distance_t_minus_one_from_first_hop.items():
                    if final_destination not in final_routes[source_station]: # This means we currently do not have a path from source -> dest (and we are now finding one: source -> dest_1 -> dest_next)
                        full_route = f"{route_to_first_hop} -> {route_to_final}"
                        current_routes[source_station][final_destination] = full_route
                        final_routes[source_station][final_destination] = full_route
                        anything_changed = True
        routes_by_distance[current_distance] = current_routes
        
        if (not anything_changed):
            # This means that we did not find any change in the last iteration, there is no reason to keep searching
            # Cause if there are no new paths found in length t, length t+1 will also not find any new paths (cause any path of length t+1 is a path of length 1 attached to a path of length t)
            break

        prev_distance +=1
    
    return final_routes