from django.shortcuts import render
import requests
from django.conf import settings


print("EDAMAM_APP_ID:", settings.EDAMAM_APP_ID)
print("EDAMAM_APP_KEY:", settings.EDAMAM_APP_KEY)

def menu(request):
    url = f"https://api.edamam.com/api/recipes/v2"
    params = {
        "type": "public",
        "q": "pizza",
        "app_id": settings.EDAMAM_APP_ID,
        "app_key": settings.EDAMAM_APP_KEY
    }
    
    response = requests.get(url, params=params)
    pizzas = []

    if response.status_code == 200:
        data = response.json()
        if "hits" in data:
            pizzas = [
                {
                    "name": hit["recipe"]["label"],
                    "image": hit["recipe"]["image"],
                    "ingredients": hit["recipe"]["ingredientLines"]
                }
                for hit in data["hits"]
            ]
    
    return render(request, "menu/menu.html", {"pizzas": pizzas})
