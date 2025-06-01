from models import Route, Stop
import paths_calculator
import data_provider
import user_interaction

# Go over the list of subway lines and print them (Question 1)
def print_all_routes(routes: list[Route]):
    for subway_route in routes:
        print(subway_route.full_name)

# Print routes with minimal and maximal number of stops (Questions 2.a, 2.b)
def print_minimal_and_maximal_stops(route_to_stop_map : dict[str, list[Stop]]):
    
    maximal_stops = max(route_to_stop_map, key=lambda a:len(route_to_stop_map[a]))
    minimal_stops = min(route_to_stop_map, key=lambda a:len(route_to_stop_map[a]))

    print(f"Route with most stops: {maximal_stops}. This route has: {len(route_to_stop_map[maximal_stops])} stops.")
    print(f"Route with least stops: {minimal_stops}. This route has: {len(route_to_stop_map[minimal_stops])} stops.")

# Print stops that have more than 1 route go through them (question 2.c)
def print_stops_with_more_than_one_route(stop_to_routes_map: dict[str, list[str]]):
    print("Stops with more than 1 route:")
    # Now we go over all the stops and list the ones that have more than one route
    for stop_name, routes in stop_to_routes_map.items():
        if (len(routes) > 1):
            print(f"Stop name: {stop_name}. route names: {routes}")

if __name__ == "__main__":
    # Retrieving the raw data once, and then using it for all questions
    routes = data_provider.get_all_subway_routes()
    print("------- Question 1 - printing all subway routes full names-------\n\n")
    print_all_routes(routes)

    print("\n\n\n------- Question 2 - printing minimal subway route, maximal subway route, and stops with more than 2 routes-------\n\n")
    (route_to_stops_map, stop_to_routes_map) = data_provider.get_route_to_stops_map_and_stop_to_routes_map(subway_routes=routes)
    print_minimal_and_maximal_stops(route_to_stops_map)
    print_stops_with_more_than_one_route(stop_to_routes_map)

    print("\n\n\n------- Question 3 - providing a path from stop a to stop b ----------- \n\n")
    all_paths = paths_calculator.calculate_all_paths(stop_to_routes_dict=stop_to_routes_map)
    user_interaction.provide_path_for_user(all_paths=all_paths)
    print("Exiting ...")