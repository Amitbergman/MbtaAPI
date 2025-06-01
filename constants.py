MBTA_API_URI = "https://api-v3.mbta.com"
ROUTES_ENDPOINT = "routes"
STOPS_ENDPOINT = "stops"
# Ideally, I would retrieve this API key from a key vault, but in this specific case, this API key is not a valuable secret, it only controls the rate limiting, and cannot be used to access my personal data or any resourece
MBTA_API_KEY = "ed8da688c57344cdafa859a2b5b2eb1a"
SUBWAY_ROUTES_TYPES_FILTER = "0,1"
CANCELLATION_KEYWORD = "cancel"