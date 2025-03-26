from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect
from core.views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('fornitori/', include('anagrafiche.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('documenti/', include('documenti.urls')),
]