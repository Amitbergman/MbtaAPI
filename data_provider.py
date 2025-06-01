import constants
import requests
from models import Route, Stop

# retrieves all the subway routes from the MBTA API (hitting the "routes" endpoint and filtering for "subway routes")
def get_all_subway_routes() -> list[Route]:
    # Ideally, I would retrieve this API key from a key vault, but in this specific case, this API key is not a valuable secret, it only controls the rate limiting, and cannot be used to access my personal data or any resourece
    query_params = {
        "api_key" : constants.MBTA_API_KEY,
        "filter[type]": constants.SUBWAY_ROUTES_TYPES_FILTER}

    # I considered the 2 options of querying for all the routes and then filtering here locally as opposed to filtering in the request parameters
    # I ended up deciding to filter in the request parameters, since:
    # The backend is probably filtering it in their SQL query, so the calculation in the backend will be faster
    # The payload that I will be getting back in the http response will be substantially smaller (178 items compared to 8) which will make the http request return faster as less bandwidth is used
    all_routes_api_response = requests.get(
        url=constants.ROUTES_URI,
        params=query_params)
    status_code = all_routes_api_response.status_code

    assert status_code == 200, f"Error fetching subway routes. Status code: {status_code}"

    routes_raw_data = all_routes_api_response.json()["data"]
    # Converting the route raw objects to the abstract model of Route
    routes = []
    for raw_route in routes_raw_data:
        route = Route(
            id=raw_route["id"],
            full_name=raw_route["attributes"]["long_name"]
        )
        routes.append(route)
        
    return routes

# Get list of stops by subway route id
def get_list_of_stops_by_route_id(route_id: str) -> list[Stop]:
    stops_params = {
        "api_key" : constants.MBTA_API_KEY,
        "filter[route]": route_id
        }
    all_stops_by_id = requests.get(
        url=constants.STOPS_URI,
        params=stops_params
    )
    assert all_stops_by_id.status_code == 200, f"Error fetching stops for route: {route_id}. status code: {all_stops_by_id.status_code}"

    stops_raw_data = all_stops_by_id.json()["data"]
    # Converting the stop raw objects to the abstract model of Stop
    stops = []
    for raw_stop in stops_raw_data:
        stop = Stop(
            id=raw_stop["id"],
            name=raw_stop["attributes"]["name"]
        )
        stops.append(stop)

    return stops

# Retrieves the information of the routes and the relevant stops, and returns:
# 1. Dictionary that has mapping from every subway_route_name to the list of stops that it goes through
# 2. Dictionary that has mapping from every stop_name to the list of route names that go through it
def get_route_to_stops_map_and_stop_to_routes_map(subway_routes : list[Route]) -> tuple[dict[str, list[Stop]], dict[str, list[str]]]:
    route_to_stops_map = dict()
    stop_to_routes_map = dict()
    # Go over all the routes, gets the stops relevant to this line
    for subway_route in subway_routes:
        route_id = subway_route.id
        route_name = subway_route.full_name
        stops = get_list_of_stops_by_route_id(route_id=route_id)
        route_to_stops_map[route_name] = stops

        for stop in stops:
            # For each stop we encounter, we add the current route to the list of routes that this stop is part of
            # It is useful since we want to eventually extract the stops that have more than one route going through them
            stop_name = stop.name
            if (stop_name in stop_to_routes_map):
                stop_to_routes_map[stop_name].append(route_name)
            else:
                stop_to_routes_map[stop_name] = [route_name]
    
    return (route_to_stops_map, stop_to_routes_map)