from django.urls import path
from . import views

urlpatterns = [
    path("azienda/nuovo/", views.AziendaCreateView.as_view(), name="azienda_create"),
    path("user/nuovo/", views.UserCreateView.as_view(), name="user_create"),
]
