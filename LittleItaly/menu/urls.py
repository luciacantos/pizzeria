from django.urls import path
from .views import menu, recipe_details, add_to_cart

urlpatterns = [
    path('', menu, name='menu'),
    path('recipe/<int:recipe_id>/', recipe_details, name='recipe_details'),
    path('carrito/añadir/', add_to_cart, name='add_to_cart'),
]

