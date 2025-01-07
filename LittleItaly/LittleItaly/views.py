import requests
from django.shortcuts import render

def home(request):
    # Llamada a la API de pizzas
    api_url = "https://api.pizzas.com/v1/pizzas"
    response = requests.get(api_url)
    
    if response.status_code == 200:
        api_data = response.json()  # Datos obtenidos de la API
    else:
        api_data = {"error": "No se pudo conectar con la API"}

    return render(request, "LittleItaly/home.html", {"api_data": api_data})