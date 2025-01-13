from django.shortcuts import render
import requests
from django.conf import settings
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from carrito.models import Producto




def menu(request):
    """
    Vista para mostrar el menú de pizzas y sincronizarlas con el modelo Producto.
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
            for index, hit in enumerate(data["hits"]):
                # Datos de la pizza obtenidos desde la API
                name = hit["recipe"]["label"]
                image = hit["recipe"]["image"]
                price = 12.50  # Precio fijo para todas las pizzas

                # Sincronizar con el modelo Producto
                producto, created = Producto.objects.get_or_create(
                    nombre=name,
                    defaults={'precio': price, 'imagen': image}
                )

                print(f"Producto: {producto.nombre}, Creado: {created}")

                # Agregar al contexto de la vista
                pizzas.append({
                    "id": producto.id,
                    "name": producto.nombre,
                    "image": producto.imagen,
                    "price": producto.precio,
                })

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


@login_required
def add_to_cart(request):
    """
    Vista para manejar la adición de pizzas al carrito.
    """
    if request.method == 'POST':
        import json
        data = json.loads(request.body)
        pizza_id = data.get('producto_id')

        # Lógica para añadir al carrito
        # Esto es un ejemplo básico, necesitarás tener un modelo de Carrito para almacenar los datos
        try:
            # Aquí podrías usar tu modelo de carrito para almacenar la información
            # cart = Cart.objects.get(user=request.user)
            # cart.add(product_id=pizza_id)
            return JsonResponse({'success': True, 'message': 'Pizza añadida al carrito.'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    
    return JsonResponse({'success': False, 'message': 'Método no permitido'}, status=405)
