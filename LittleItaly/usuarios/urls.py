from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Página de inicio de sesión
    path('login/', auth_views.LoginView.as_view(template_name='usuarios/login.html'), name='login'),
    
    # Página de cierre de sesión
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # Página de registro
    path('register/', views.register, name='register'),
]
