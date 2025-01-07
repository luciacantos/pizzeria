from django.shortcuts import render

import requests
from django.conf import settings


# Create your views here.

def get_nutritional_info(ingredients):
    url = f"https://api.edamam.com/api/nutrition-details"
    headers = {
        "Content-Type": "application/json"
    }
    params = {
        "app_id": settings.EDAMAM_APP_ID,
        "app_key": settings.EDAMAM_APP_KEY
    }
    data = {
        "title": "Custom Pizza",
        "ingr": ingredients  # Lista de ingredientes
    }
    
    response = requests.post(url, json=data, headers=headers, params=params)
    
    if response.status_code == 200:
        return response.json()  # Devuelve los datos nutricionales
    else:
        return {"error": response.status_code, "message": response.text}

def menu(request):
    return render(request, "menu/menu.html")