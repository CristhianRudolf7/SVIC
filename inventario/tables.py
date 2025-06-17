import django_tables2 as tables
from .models import Productos, Categorias, UnidadMedida

class ProductosTable(tables.Table):
    class Meta:
        model = Productos
        template_name = "django_tables2/semantic.html"
        fields = (
            'foto','nombre', 'categoria', 'precio',
            'stock', 'unidad'
        )
        order_by_field = 'sort'

class CategoriasTable(tables.Table):
    class Meta:
        model = Categorias
        template_name = "django_tables2/semantic.html"
        fields = (
            'nombre',
            'descripcion',
            'fecha_creacion'
        )
        order_by_field = 'sort'

class UnidadesTable(tables.Table):
    class Meta:
        model = UnidadMedida
        template_name = "django_tables2/semantic.html"
        fields = (
            'nombre',
            'simbolo',
            'fecha_creacion'
        )
        order_by_field = 'sort'
