import django_filters
from .models import Usuarios

class StaffFilter(django_filters.FilterSet):
    class Meta:
        model = Usuarios
        fields = ['nombre', 'dni', 'rol', 'estado']
