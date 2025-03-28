from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView
from .forms import AziendaForm, UserForm
from .models import Azienda, User


class AziendaCreateView(CreateView):
    model = Azienda
    form_class = AziendaForm
    template_name = "accounts/azienda_form.html"
    success_url = "/"


class UserCreateView(CreateView):
    model = User
    form_class = UserForm
    template_name = "accounts/user_form.html"

    def form_valid(self, form):
        # Associa l'utente all'azienda
        form.instance.azienda = (
            Azienda.objects.first()
        )  # Modifica questo per associare l'azienda corretta
        user = form.save()
        login(self.request, user)
        return redirect("/")
