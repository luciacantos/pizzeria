from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Carrito, Producto, CarritoItem
import json

@login_required
def carrito_view(request):
    """
    Vista para mostrar el contenido del carrito.
    """
    # Obtener el carrito del usuario
    carrito, _ = Carrito.objects.get_or_create(usuario=request.user)
    items = carrito.carrito_items.all()  # Asegúrate de usar el related_name correcto

    # Calcular totales
    carrito_data = []
    total = 0
    for item in items:
        subtotal = item.cantidad * item.producto.precio
        total += subtotal
        carrito_data.append({
            'producto': item.producto,
            'cantidad': item.cantidad,
            'subtotal': subtotal,
        })

    context = {
        'carrito': carrito_data,
        'total': total,
    }
    return render(request, 'carrito/carrito.html', context)

@login_required
@csrf_exempt
def añadir_al_carrito(request):
    """
    Vista para manejar la adición de productos al carrito.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            producto_id = data.get('producto_id')
            cantidad = data.get('cantidad', 1)

            # Buscar el producto
            producto = get_object_or_404(Producto, id=producto_id)

            # Obtener o crear el carrito del usuario
            carrito, _ = Carrito.objects.get_or_create(usuario=request.user)

            # Añadir el producto al carrito o actualizar la cantidad
            item, creado = CarritoItem.objects.get_or_create(
                carrito=carrito,
                producto=producto,
                defaults={'cantidad': cantidad}
            )
            if not creado:
                item.cantidad += cantidad
                item.save()

            return JsonResponse({'success': True, 'message': 'Producto añadido al carrito'})

        except Producto.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Producto no encontrado'}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=400)

    return JsonResponse({'success': False, 'message': 'Método no permitido'}, status=405)

@login_required
@csrf_exempt
def actualizar_carrito(request):
    """
    Vista para actualizar la cantidad de un producto en el carrito.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            producto_id = data.get('producto_id')
            nueva_cantidad = data.get('cantidad')

            if not producto_id or nueva_cantidad is None:
                return JsonResponse({'success': False, 'message': 'Datos incompletos'})

            carrito = Carrito.objects.get(usuario=request.user)
            item = CarritoItem.objects.get(carrito=carrito, producto_id=producto_id)

            if int(nueva_cantidad) > 0:
                item.cantidad = int(nueva_cantidad)
                item.save()
            else:
                item.delete()

            return JsonResponse({'success': True, 'message': 'Cantidad actualizada'})

        except CarritoItem.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Producto no encontrado en el carrito.'}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=400)

    return JsonResponse({'success': False, 'message': 'Método no permitido'}, status=405)

@login_required
@csrf_exempt
def eliminar_del_carrito(request):
    """
    Vista para eliminar un producto del carrito.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            producto_id = data.get('producto_id')

            carrito = Carrito.objects.get(usuario=request.user)
            item = get_object_or_404(CarritoItem, carrito=carrito, producto_id=producto_id)
            item.delete()

            return JsonResponse({'success': True, 'message': 'Producto eliminado del carrito'})

        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=400)

    return JsonResponse({'success': False, 'message': 'Método no permitido'}, status=405)
