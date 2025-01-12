from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

# Create your models here.
User = get_user_model()
class EmailAuthBackend(ModelBackend):
    """
    Autentica usando el correo electrónico en lugar del nombre de usuario.
    """
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            user = User.objects.get(email=email)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None