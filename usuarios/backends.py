# usuarios/backends.py
from django.contrib.auth.backends import BaseBackend
from django.db import connection

class DniBackend(BaseBackend):
    def authenticate(self, request, dni=None, password=None):
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT dni, password, rol FROM usuarios WHERE dni = %s", 
                [dni]
            )
            row = cursor.fetchone()
            
            if row and row[1] == password:  # Comparación directa de contraseña
                from django.contrib.auth.models import User
                user = User()
                user.dni = row[0]
                user.rol = row[2]
                return user
        return None

    def get_user(self, user_id):
        # Implementar según necesidad
        pass