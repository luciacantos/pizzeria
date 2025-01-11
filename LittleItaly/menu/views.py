from django.shortcuts import render
import requests
from django.conf import settings

def menu(request):
    """
    Vista para mostrar el menú de pizzas.
    """
    url = "https://api.edamam.com/api/recipes/v2"
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
            # Generamos una lista de pizzas con un ID único
            pizzas = [
                {
                    "id": index,  # Usamos el índice del bucle como ID
                    "name": hit["recipe"]["label"],
                    "image": hit["recipe"]["image"]
                }
                for index, hit in enumerate(data["hits"])
            ]
    
    return render(request, "menu/menu.html", {"pizzas": pizzas})


def recipe_details(request, recipe_id):
    """
    Vista para mostrar los detalles de una receta seleccionada.
    """
    url = "https://api.edamam.com/api/recipes/v2"
    params = {
        "type": "public",
        "q": "pizza",
        "app_id": settings.EDAMAM_APP_ID,
        "app_key": settings.EDAMAM_APP_KEY
    }
    
    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        # Verificamos que el ID sea válido
        if "hits" in data and 0 <= recipe_id < len(data["hits"]):
            recipe = data["hits"][recipe_id]["recipe"]
            
            # Preparación de los datos para el template
            ingredients_list = recipe.get("ingredientLines", [])  # Lista de ingredientes
            health_labels_list = recipe.get("healthLabels", [])   # Lista de etiquetas de salud
            nutrients = recipe.get("totalNutrients", {})          # Nutrientes totales
            
            # Pasamos los datos necesarios a la plantilla
            context = {
                "recipe": {
                    "name": recipe.get("label", "Receta sin nombre"),
                    "image": recipe.get("image", ""),
                    "ingredients": ingredients_list,
                    "healthLabels": health_labels_list,
                    "cuisineType": recipe.get("cuisineType", ["Desconocido"])[0],  # Primer tipo de cocina
                    "calories": recipe.get("calories", 0),
                    "totalNutrients": nutrients,
                }
            }
            return render(request, 'menu/recipe_details.html', context)
    
    # Manejo de error si la receta no existe o la API falla
    return render(request, 'menu/recipe_details.html', {'error': 'Receta no encontrada'})


