from django import forms
from .models import Fornitore

class FornitoreForm(forms.ModelForm):
    class Meta:
        model = Fornitore
        fields = ['ragione_sociale', 'partita_iva', 'codice_fiscale', 'indirizzo', 'telefono', 'email', 'attivo']
        widgets = {
            'ragione_sociale': forms.TextInput(attrs={'class': 'form-control'}),
            'partita_iva': forms.TextInput(attrs={'class': 'form-control'}),
            'codice_fiscale': forms.TextInput(attrs={'class': 'form-control'}),
            'indirizzo': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'attivo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }