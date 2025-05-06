import os
from django.db import models
from django.conf import settings
from anagrafiche.models import Fornitore, Dogana
from accounts.models import Azienda
from django.utils.text import slugify



class DichiarazioneIntento(models.Model):
    TIPO_OPERAZIONE = [
        ("A", "Acquisto"),
        ("I", "Importazione"),
    ]
    numero_interno = models.PositiveIntegerField()
    numero_dichiarazione = models.CharField(max_length=100, blank=True, null=True)
    tipo_operazione = models.CharField(
        "Tipo Operazione", max_length=1, choices=TIPO_OPERAZIONE
    )
    note = models.TextField("Note", blank=True, null=True)
    data_dichiarazione = models.DateField()
    importosingolo = models.BooleanField("Importo Singolo", default=False)
    plafond_singolo = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    plafond = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    anno_riferimento = models.PositiveIntegerField()
    fk_dogana = models.ForeignKey(
        Dogana, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Dogana"
    )
    fornitore = models.ForeignKey(Fornitore, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True
    )

    azienda = models.ForeignKey(Azienda, on_delete=models.CASCADE, null=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.pk and not self.azienda_id and self.created_by:
            self.azienda = self.created_by.azienda
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"{self.fornitore} - {self.numero_dichiarazione}"

    class Meta:        
        ordering = ['data_dichiarazione', '-numero_interno']        
        verbose_name = 'Dichiarazione di Intento'
        verbose_name_plural = 'Dichiarazioni di Intento'

class FatturaFornitore(models.Model):
    fornitore = models.ForeignKey(
        Fornitore, on_delete=models.CASCADE, related_name="fatture"
    )
    numero_fattura = models.CharField(max_length=100)
    data_fattura = models.DateField()
    importo = models.DecimalField(max_digits=12, decimal_places=2)

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True
    )
    azienda = models.ForeignKey(Azienda, on_delete=models.CASCADE, null=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.pk and not self.azienda_id and self.created_by:
            self.azienda = self.created_by.azienda
        super().save(*args, **kwargs)

    class Meta:
        ordering = ["-data_fattura"]
        
    def __str__(self):
        return f"{self.fornitore} - {self.numero_fattura}"



def durc_upload_path(instance, filename):
    ragione_sociale = slugify(instance.fornitore.ragione_sociale)
    return os.path.join("durc", ragione_sociale, filename)


class Durc(models.Model):
    fornitore = models.ForeignKey(
        Fornitore, on_delete=models.CASCADE, related_name="durc"
    )
    numero_durc = models.CharField(max_length=100)
    data_durc = models.DateField()
    scadenza_durc = models.DateField()
    documento = models.FileField(upload_to=durc_upload_path, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True
    )
    azienda = models.ForeignKey(Azienda, on_delete=models.CASCADE, null=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.pk and not self.azienda_id and self.created_by:
            self.azienda = self.created_by.azienda
        super().save(*args, **kwargs)
        
    
    class Meta:
        ordering = ["-scadenza_durc"]
        
    def __str__(self):
        return f"{self.fornitore} - {self.numero_durc}"
    