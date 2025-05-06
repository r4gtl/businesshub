from django import forms
from .models import DichiarazioneIntento, FatturaFornitore, Durc
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
            "plafond_singolo",
            "fk_dogana",
        ]
        widgets = {
            "numero_interno": forms.NumberInput(
                attrs={
                    "class": "form-control text-end",
                    "placeholder": "Numero Interno",
                }
            ),
            "numero_dichiarazione": forms.TextInput(
                attrs={
                    "class": "form-control text-end",
                    "placeholder": "Numero Dichiarazione",
                }
            ),
            "data_dichiarazione": forms.DateInput(
                attrs={"class": "form-control  text-end", "type": "date"}
            ),
            "plafond": forms.NumberInput(
                attrs={
                    "class": "form-control text-end",
                    "placeholder": "Plafond fino a concorrenza di Eur.",
                }
            ),
            "anno_riferimento": forms.NumberInput(
                attrs={"class": "form-control text-end", "placeholder": "Anno"}
            ),
            "fornitore": forms.Select(attrs={"class": "form-control"}),
            "tipo_operazione": forms.RadioSelect(),
            "note": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "style": "height: 100px;",
                    "placeholder": "Descrizione",
                }
            ),
            "importosingolo": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "plafond_singolo": forms.NumberInput(
                attrs={
                    "class": "form-control text-end",
                    "placeholder": "Una sola operazione fino ad Eur.",
                }
            ),
            "fk_dogana": forms.Select(attrs={"class": "form-control"}),
        }
        labels = {"note": "Descrizione", "anno_riferimento": "Anno"}

    def __init__(self, *args, **kwargs):
        # Ottieni l'utente loggato (request.user)
        user = kwargs.pop(
            "user", None
        )  # Questo deve essere passato al form dalle views

        super().__init__(*args, **kwargs)

        if user:
            # Filtra il campo "fornitore" in base all'azienda dell'utente loggato
            self.fields["fornitore"].queryset = Fornitore.objects.filter(
                azienda=user.azienda
            )
            # Filtra il campo "fk_dogana" in base all'azienda dell'utente loggato
            self.fields["fk_dogana"].queryset = Dogana.objects.filter(
                azienda=user.azienda
            )

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
        user = kwargs.pop(
            "user", None
        )  # Questo deve essere passato al form dalle views

        super().__init__(*args, **kwargs)

        if user:
            # Filtra il campo "fornitore" in base all'azienda dell'utente loggato
            self.fields["fornitore"].queryset = Fornitore.objects.filter(
                azienda=user.azienda
            )


class DurcForm(forms.ModelForm):
    class Meta:
        model = Durc
        fields = ["fornitore", "numero_durc", "data_durc", "scadenza_durc", "documento"]
        widgets = {
            "data_durc": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
            "scadenza_durc": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
            "fornitore": forms.Select(attrs={"class": "form-select"}),
            "numero_durc": forms.TextInput(attrs={"class": "form-control"}),
            "documento": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }

        def __init__(self, *args, **kwargs):
            # Ottieni l'utente loggato (request.user)
            user = kwargs.pop(
                "user", None
            )  # Questo deve essere passato al form dalle views

            super().__init__(*args, **kwargs)

            if user:
                # Filtra il campo "fornitore" in base all'azienda dell'utente loggato
                self.fields["fornitore"].queryset = Fornitore.objects.filter(
                    azienda=user.azienda
                )
