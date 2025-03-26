from django.db import models
from django.conf import settings
from anagrafiche.models import Fornitore

class DichiarazioneIntento(models.Model):
    numero_interno = models.PositiveIntegerField()
    numero_dichiarazione = models.CharField(max_length=100)
    data_dichiarazione = models.DateField()
    plafond = models.DecimalField(max_digits=12, decimal_places=2)
    anno_riferimento = models.PositiveIntegerField()
    fornitore = models.ForeignKey(Fornitore, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.fornitore} - {self.numero_dichiarazione}"

class FatturaFornitore(models.Model):
    fornitore = models.ForeignKey(Fornitore, on_delete=models.CASCADE)
    numero_fattura = models.CharField(max_length=100)
    data_fattura = models.DateField()
    importo = models.DecimalField(max_digits=12, decimal_places=2)

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.fornitore} - {self.numero_fattura}"
