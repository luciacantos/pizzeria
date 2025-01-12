from django.urls import path
from . import views

urlpatterns = [
    path('', views.carrito_view, name='carrito'),
    path('carrito/add/', views.añadir_al_carrito, name='añadir_al_carrito'),
]
