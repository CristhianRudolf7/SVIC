from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.contrib.auth import views as auth_views
from accounts import views as user_views
from .views import (
    ProfileListView,
    ProfileCreateView,
    ProfileUpdateView,
    ProfileDeleteView,
    CustomerListView,
    CustomerCreateView,
    CustomerUpdateView,
    CustomerDeleteView,
    get_customers,
    VendorListView,
    VendorCreateView,
    VendorUpdateView,
    VendorDeleteView
)

urlpatterns = [
    # User authentication URLs
    path('', user_views.landing, name='user-home'),
    path('crear-empresa/', user_views.crearEmpresa, name='crearEmpresa'),
    path('iniciar-sesion/', auth_views.LoginView.as_view(
        template_name='accounts/login.html'), name='user-login'),
    path('perfil/', user_views.profile, name='user-profile'),
    path('perfil/editar/', user_views.profile_update,
         name='user-profile-update'),
    path('logout/', auth_views.LogoutView.as_view(
        template_name='accounts/logout.html'), name='user-logout'),

    # Profile URLs
    path('trabajadores/', ProfileListView.as_view(), name='profile_list'),
    path('crear-trabajador/', ProfileCreateView.as_view(), name='profile-create'),
    path('trabajador/<int:pk>/editar/', ProfileUpdateView.as_view(),
         name='profile-update'),
    path('trabajador/<int:pk>/eliminar/', ProfileDeleteView.as_view(),
         name='profile-delete'),

    # Customer URLs
    path('clientes/', CustomerListView.as_view(), name='customer_list'),
    path('clientes/crear/', CustomerCreateView.as_view(),
         name='customer_create'),
    path('clientes/<int:pk>/editar/', CustomerUpdateView.as_view(),
         name='customer_update'),
    path('clientes/<int:pk>/eliminar/', CustomerDeleteView.as_view(),
         name='customer_delete'),
    path('get_customers/', get_customers, name='get_customers'),

    # Vendor URLs
    path('proveedores/', VendorListView.as_view(), name='vendor-list'),
    path('proveedores/crear/', VendorCreateView.as_view(), name='vendor-create'),
    path('proveedores/<int:pk>/editar/', VendorUpdateView.as_view(),
         name='vendor-update'),
    path('proveedores/<int:pk>/eliminar/', VendorDeleteView.as_view(),
         name='vendor-delete'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
