from django import forms
from .models import DichiarazioneIntento


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
            "tipo_operazione": forms.Select(attrs={"class": "form-control"}),
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
