from django.urls import path
from . import views

urlpatterns = [
    path('', views.carrito_view, name='carrito'),
    path('actualizar/', views.actualizar_carrito, name='carrito_actualizar'),
    path('eliminar/', views.eliminar_del_carrito, name='carrito_eliminar'),
]
