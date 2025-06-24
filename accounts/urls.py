from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from .api import RegisterView, MyTokenObtainPairView, UserDetailView
from . import views

urlpatterns = [
    # API endpoints
    path("register/", RegisterView.as_view(), name="register"),
    path("token/", MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("user/", UserDetailView.as_view(), name="user_detail"),
    # Views classiche
    path("azienda/nuovo/", views.AziendaCreateView.as_view(), name="azienda_create"),
    path("user/nuovo/", views.UserCreateView.as_view(), name="user_create"),
]
