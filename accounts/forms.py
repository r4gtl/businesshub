from django import forms
from .models import Azienda, User


class AziendaForm(forms.ModelForm):
    class Meta:
        model = Azienda
        fields = [
            "ragionesociale",
            "partita_iva",
            "codice_fiscale",
            "indirizzo",
            "cap",
            "citta",
            "provincia",
            "paese",
        ]


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "password", "email", "azienda"]
