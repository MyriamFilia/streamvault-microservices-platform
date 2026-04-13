import requests
from app.config.settings import TVMAZE_BASE_URL

def search_series(query: str):
    url = f"{TVMAZE_BASE_URL}/search/shows"

    response = requests.get(
        url,
        params={"q": query},
        timeout=10
    )

    response.raise_for_status()

    return response.json()

def get_popular_series():
    url = f"{TVMAZE_BASE_URL}/shows"

    response = requests.get(url, timeout=10)
    response.raise_for_status()

    return response.json()


def get_series_details(series_id: int):
    url = f"{TVMAZE_BASE_URL}/shows/{series_id}"
    response = requests.get(
        url,
        params={"embed[]": ["cast", "seasons"]},
        timeout=10
    )
    response.raise_for_status()
    return response.json()