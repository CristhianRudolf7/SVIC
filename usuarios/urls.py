from django.urls import path
from usuarios import views as usuarios_views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', usuarios_views.landing, name='home'),
    path('login/', usuarios_views.LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
]