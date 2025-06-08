from django.urls import path
from django.http import HttpResponse

def prueba(request):
    return HttpResponse("Ruta de prueba funcionando.")

urlpatterns = [
    path('', prueba),
]