import requests
from django.conf import settings

APP_ID = settings.EDAMAM_APP_ID
APP_KEY = settings.EDAMAM_APP_KEY
BASE_URL = "https://api.edamam.com/api/recipes/v2"

def fetch_recipes(query):
    """
    Fetches recipes from the Edamam Recipe API.
    """
    params = {
        "type": "public",
        "q": query,
        "app_id": APP_ID,
        "app_key": APP_KEY
    }
    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()
