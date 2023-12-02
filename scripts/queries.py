import requests

def search_query(search_type, search_query, API_BASE_URL, API_KEY):
    endpoint_path = f"/search/tv" if search_type == "tv" else f"/search/movie"
    endpoint = f"{API_BASE_URL}{endpoint_path}?api_key={API_KEY}&query={search_query}"
    response = requests.get(endpoint)
    return response

def get_details(details_type, id, API_BASE_URL, API_KEY):
    endpoint_path = f"/tv/{id}" if details_type == "tv" else f"/movie/{id}"
    endpoint = f"{API_BASE_URL}{endpoint_path}?api_key={API_KEY}"
    response = requests.get(endpoint)
    return response

def get_trendings(page, time, API_BASE_URL, API_KEY):
    day = "month" if time == "month" else "year" if time == "year" else "day"
    endpoint_path = f"/trending/tv/{day}"
    pages = f"{page}"
    endpoint = f"{API_BASE_URL}{endpoint_path}?api_key={API_KEY}&page={pages}"
    result = requests.get(endpoint)
    return result

def get_top_rated(type, page, API_BASE_URL, API_KEY):
    endpoint_path = f"/{type}/top_rated"
    pages = f"{page}"
    endpoint = f"{API_BASE_URL}{endpoint_path}?api_key={API_KEY}&page={pages}"
    results = requests.get(endpoint)
    return results