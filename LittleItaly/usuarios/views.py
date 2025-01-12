from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

# Create your views here.

from django.contrib.auth.models import User

def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)  # Usa "email"
        if user is not None:
            login(request, user)
            return redirect('home')  # Cambia 'home' por tu vista principal
        else:
            return render(request, 'usuarios/login.html', {'error': 'Credenciales incorrectas'})
    return render(request, 'usuarios/login.html')



def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')
    return render(request, 'usuarios/logout.html')



def register_view(request):
    if request.method == 'POST':
        # Captura los datos del formulario
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        # Validaciones básicas
        if password1 != password2:
            messages.error(request, 'Las contraseñas no coinciden.')
            return render(request, 'usuarios/register.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'El nombre de usuario ya está en uso.')
            return render(request, 'usuarios/register.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'El correo electrónico ya está registrado.')
            return render(request, 'usuarios/register.html')

        # Crea al usuario
        user = User.objects.create_user(username=username, email=email, password=password1)
        user.save()

        # Inicia sesión automáticamente después de registrarse
        login(request, user)
        messages.success(request, 'Te has registrado exitosamente.')
        return redirect('home')  # Cambia 'home' por la vista principal de tu aplicación

    # Si es una solicitud GET
    return render(request, 'usuarios/register.html')

