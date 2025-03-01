from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from usuarios.models import EmailAuthBackend
from django.core.mail import send_mail
from django.conf import settings

def contacto(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        # Validar que los campos no estén vacíos
        if not name or not email or not message:
            return render(request, 'usuarios/contacto.html', {'error': 'Todos los campos son obligatorios.'})

        # Configurar y enviar el correo
        try:
            send_mail(
                subject=f"Mensaje de {name}",
                message=f"Correo: {email}\n\nMensaje:\n{message}",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=['ee275252945229@mailtrap.io'],
                fail_silently=False,
            )
            return render(request, 'usuarios/contacto.html', {'success': 'Mensaje enviado correctamente.'})
        except Exception as e:
            return render(request, 'usuarios/contacto.html', {'error': f'Error al enviar el mensaje: {str(e)}'})

    return render(request, 'usuarios/contacto.html')


def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
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


User = get_user_model()

def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        # Validaciones
        if password1 != password2:
            return render(request, 'usuarios/register.html', {'error': 'Las contraseñas no coinciden.'})

        if User.objects.filter(email=email).exists():
            return render(request, 'usuarios/register.html', {'error': 'El correo electrónico ya está registrado.'})

        if User.objects.filter(username=username).exists():
            return render(request, 'usuarios/register.html', {'error': 'El nombre de usuario ya está en uso.'})

        # Crear el usuario
        user = User.objects.create_user(username=username, email=email, password=password1)
        user.save()

        # Inicia sesión automáticamente
        backend_path = 'usuarios.models.EmailAuthBackend'
        user.backend = backend_path
        login(request, user, backend=backend_path)

        return redirect('home')

    return render(request, 'usuarios/register.html')
