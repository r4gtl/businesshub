from django.db import models
from django.contrib.auth.models import User

class Fornitore(models.Model):
    ragione_sociale = models.CharField(max_length=255)
    partita_iva = models.CharField(max_length=20, unique=True)
    codice_fiscale = models.CharField(max_length=20, blank=True, null=True)
    indirizzo = models.CharField(max_length=255, blank=True, null=True)
    telefono = models.CharField(max_length=30, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    attivo = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.ragione_sociale
