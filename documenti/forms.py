from django import forms
from .models import DichiarazioneIntento, FatturaFornitore
from anagrafiche.models import Fornitore, Dogana


class DichiarazioneIntentoForm(forms.ModelForm):
    class Meta:
        model = DichiarazioneIntento
        fields = [
            "numero_interno",
            "numero_dichiarazione",
            "data_dichiarazione",
            "plafond",
            "anno_riferimento",
            "fornitore",
            "tipo_operazione",
            "note",
            "importosingolo",
            "fk_dogana",
        ]
        widgets = {
            "numero_interno": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "Numero Interno"}
            ),
            "numero_dichiarazione": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Numero Dichiarazione"}
            ),
            "data_dichiarazione": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "plafond": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "Plafond"}
            ),
            "anno_riferimento": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "Anno"}
            ),
            "fornitore": forms.Select(attrs={"class": "form-control"}),
            "tipo_operazione": forms.RadioSelect(),
            "note": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "style": "height: 100px;",
                    "placeholder": "Note",
                }
            ),
            "importosingolo": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "fk_dogana": forms.Select(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        # Ottieni l'utente loggato (request.user)
        user = kwargs.pop('user', None)  # Questo deve essere passato al form dalle views

        super().__init__(*args, **kwargs)

        if user:
            # Filtra il campo "fornitore" in base all'azienda dell'utente loggato
            self.fields["fornitore"].queryset = Fornitore.objects.filter(azienda=user.azienda)
            # Filtra il campo "fk_dogana" in base all'azienda dell'utente loggato
            self.fields["fk_dogana"].queryset = Dogana.objects.filter(azienda=user.azienda)

        # Forza il campo tipo_operazione come richiesto
        self.fields["tipo_operazione"].required = True
        self.fields["tipo_operazione"].choices = DichiarazioneIntento.TIPO_OPERAZIONE

class FatturaFornitoreForm(forms.ModelForm):
    class Meta:
        model = FatturaFornitore
        fields = [
            "fornitore",
            "numero_fattura",
            "data_fattura",
            "importo",
            
        ]
        widgets = {
            "fornitore": forms.Select(attrs={"class": "form-control"}),
            "numero_fattura": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Numero Fattura"}
            ),
            
            "data_fattura": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "importo": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "Importo"}
            ),
            
        }
        
    def __init__(self, *args, **kwargs):
        # Ottieni l'utente loggato (request.user)
        user = kwargs.pop('user', None)  # Questo deve essere passato al form dalle views

        super().__init__(*args, **kwargs)

        if user:
            # Filtra il campo "fornitore" in base all'azienda dell'utente loggato
            self.fields["fornitore"].queryset = Fornitore.objects.filter(azienda=user.azienda)
        
