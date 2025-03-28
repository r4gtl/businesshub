from django.contrib.auth.models import AbstractUser
from django.db import models


class Azienda(models.Model):
    ragionesociale = models.CharField(max_length=255, unique=True)
    partita_iva = models.CharField(max_length=20, unique=True)
    codice_fiscale = models.CharField(max_length=16, unique=True)
    indirizzo = models.CharField(max_length=255)
    cap = models.CharField(max_length=5)
    citta = models.CharField(max_length=100)
    provincia = models.CharField(max_length=100)
    paese = models.CharField(max_length=100)

    def __str__(self):
        return self.ragionesociale


class User(AbstractUser):
    azienda = models.ForeignKey(
        Azienda,
        on_delete=models.CASCADE,
        related_name="utenti",
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.username
