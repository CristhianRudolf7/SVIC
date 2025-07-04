from django.urls import path
from usuarios import views as usuarios_views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', usuarios_views.landing, name='home'),
    path('login/', usuarios_views.LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('crear-empresa/', usuarios_views.crearEmpresa, name='crearEmpresa'),
    path('pagar/', usuarios_views.pagar, name='pagar'),
    path('listaTrabajadores/', usuarios_views.listaTrabajadoresView.as_view(), name='listaTrabajadores'),
    path('crearTrabajador/', usuarios_views.crearTrabajadorView.as_view(), name='crearTrabajador'),
    path('editarTrabajador/<uuid:usuario_id>/', usuarios_views.editarTrabajadorView.as_view(), name='editarTrabajador'),
    path('eliminarTrabajador/<uuid:usuario_id>/', usuarios_views.eliminarTrabajadorView.as_view(), name='eliminarTrabajador'),
]