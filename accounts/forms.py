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
            "cf_rappresentante",
            "codice_carica",
            "cognome_rappresentante",
            "nome_rappresentante",
            "data_nascita_rappresentante",
            "comune_nascita",
            "provincia",
            "tel",
            "email",
            "tipo_plafond"
        ]


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "password", "email", "azienda"]
