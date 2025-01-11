from django.urls import path
from . import views

urlpatterns = [
    path('', views.menu, name='menu'),
    path('recipe/<int:recipe_id>/', views.recipe_details, name='recipe_details'),
]
