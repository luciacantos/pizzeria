from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Carrito, Producto

# Create your views here.

@login_required
def carrito_view(request):
    # Aquí va la lógica para obtener los productos del carrito
    carrito = []  # Simula el contenido del carrito
    return render(request, 'carrito/carrito.html', {'carrito': carrito})


@login_required
@csrf_exempt  # Solo si usas fetch desde el frontend. Reemplaza con un formulario si lo haces con HTML puro.
def añadir_al_carrito(request):
    if request.method == 'POST':
        try:
            # Parsear datos de la solicitud
            data = json.loads(request.body)
            producto_id = data.get('producto_id')
            cantidad = data.get('cantidad', 1)

            # Buscar el producto
            producto = Producto.objects.get(id=producto_id)

            # Obtener o crear el carrito del usuario
            carrito, _ = Carrito.objects.get_or_create(usuario=request.user)

            # Añadir el producto al carrito
            item, creado = carrito.items.get_or_create(producto=producto, defaults={'cantidad': cantidad})
            if not creado:
                item.cantidad += cantidad
                item.save()

            return JsonResponse({'success': True, 'message': 'Producto añadido al carrito'})

        except Producto.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Producto no encontrado'}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=400)

    return JsonResponse({'success': False, 'message': 'Método no permitido'}, status=405)