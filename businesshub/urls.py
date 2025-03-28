from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect
from core.views import HomeView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("", HomeView.as_view(), name="home"),
    path("fornitori/", include("anagrafiche.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
    path("documenti/", include("documenti.urls")),
]
