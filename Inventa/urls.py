from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dashborad/', include('store.urls')),
    path('chat/', include('chat.urls')),
    path('transactions/', include('transactions.urls')),
    path('', include('accounts.urls')),
]
