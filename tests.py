from paths_calculator import calculate_all_paths
from data_provider import get_all_subway_routes, get_route_to_stops_map_and_stop_to_routes_map

# Run a test that validates the path calculator is working properly on mock data
def run_path_calculator_tests():
    print("Start running path calculator tests")
    stop_to_route_dict = dict()

    stop_to_route_dict[1] = ["yellow"]
    stop_to_route_dict[2] = ["red"]
    stop_to_route_dict[3] = ["red", "green"]
    stop_to_route_dict[4] = ["yellow", "green"]
    stop_to_route_dict[5] = ["green"]

    paths = calculate_all_paths(stop_to_routes_dict=stop_to_route_dict)
    expected_1_1 = "Stay in 1..."
    assert paths[1][1] == expected_1_1, f"Expceted: '{expected_1_1}', got: `{paths[1][1]}`"

    expected_1_2 = "yellow -> green -> red"
    assert paths[1][2] == expected_1_2, f"Expceted: `{expected_1_2}`, got: `{paths[1][2]}`"

    expected_1_4 = "yellow"
    assert paths[1][4] == expected_1_4, f"Expceted: `{expected_1_4}`, got: `{paths[1][4]}`"

    number_of_stops = 5
    for stop in paths.keys():
        routes = paths[stop]
        number_of_routes_from_this_stop = len(routes)
        assert number_of_routes_from_this_stop == number_of_stops, "TEST FAILURE in `calculate_all_paths`: From any stop there should be paths to any other stop."

    print("Success!")

# Run tests that validate that the data provider functions are properly retrieving the data from MBTA API 
def run_data_provider_tests():
    print("Start running data provider tests")
    routes = get_all_subway_routes()
    red_line_item = [r for r in routes if r.full_name == "Red Line"]

    assert len(red_line_item) == 1, "TEST FAILURE in `get_all_subway_routes`: Could not find red line item in the output"


    (route_to_stop, stop_to_routes) = get_route_to_stops_map_and_stop_to_routes_map(routes)
    assert "Broadway" in stop_to_routes.keys(), "TEST FAILURE in `get_route_to_stops_map_and_stop_to_routes_map`: Could not find Broadway stop in stop to route map"
    assert "Orange Line" in route_to_stop.keys(), "TEST FAILURE in `get_route_to_stops_map_and_stop_to_routes_map`:Could not find Orange line in route to stop map"

    print("Success!")

if __name__ == "__main__":
    run_path_calculator_tests()
    run_data_provider_tests()