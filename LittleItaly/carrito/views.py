from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def carrito_view(request):
    # Aquí va la lógica para obtener los productos del carrito
    carrito = []  # Simula el contenido del carrito
    return render(request, 'carrito/carrito.html', {'carrito': carrito})