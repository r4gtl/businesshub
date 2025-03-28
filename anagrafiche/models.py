from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


class Fornitore(models.Model):
    ragione_sociale = models.CharField(max_length=255)
    partita_iva = models.CharField(max_length=20, unique=True)
    codice_fiscale = models.CharField(max_length=20, blank=True, null=True)
    indirizzo = models.CharField(max_length=255, blank=True, null=True)
    cap = models.CharField(max_length=10, blank=True, null=True)
    citta = models.CharField("Città", max_length=100, blank=True, null=True)
    provincia = models.CharField(max_length=2, blank=True, null=True)
    paese = models.CharField(max_length=100, blank=True, null=True)
    telefono = models.CharField(max_length=30, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    attivo = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )

    class Meta:
        ordering = ["ragione_sociale"]

    def __str__(self):
        return self.ragione_sociale


class Dogana(models.Model):
    descrizione = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )

    def __str__(self):
        return self.descrizione

    class Meta:
        ordering = ["descrizione"]
