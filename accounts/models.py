from django.contrib.auth.models import AbstractUser
from django.db import models


class Azienda(models.Model):
    CODICE_CARICA = [
        ("1", "Rappresentante legale, negoziale o di fatto, socio amministratore"),
        ("2", "Rappresentante di minore, inabilitato o interdetto, amministratore di sostegno, ovvero curatore dell’eredità giacente, amministratore di eredità devoluta sotto condizione sospensiva o in favore di nascituro non ancora concepito"),
        ("3", "Curatore fallimentare"),
        ("4", "Commissario liquidatore (liquidazione coatta amministrativa ovvero amministrazione straordinaria)"),
        
        ("5", "Custode giudiziario (custodia giudiziaria), ovvero amministratore giudiziario in qualità di rappresentante dei beni sequestrati ovvero commissario giudiziale (amministrazione controllata)"),
        ("6", "Rappresentante fiscale di soggetto non residente"),
        ("7", "Erede"),
        ("8", "Liquidatore (liquidazione volontaria)"),
        ("9", "Soggetto tenuto a presentare la comunicazione ai fini IVA per conto del soggetto estinto a seguito di operazioni straordinarie o altre trasformazioni sostanziali soggettive (cessionario d’azienda, società beneficiaria, incorporante, conferitaria, ecc.)la comunicazione."),
        ("10", "Rappresentante fiscale di soggetto non residente con le limitazioni di cui all'art. 44, comma 3, del D.L. n. 331/1993"),
        ("11", "Soggetto esercente l'attività tutoria del minore o interdetto in relazione alla funzione istituzionale rivestita"),
        ("12", "Liquidatore (liquidazione volontaria di ditta individuale - periodo ante messa in liquidazione)"),
        ("13", "Amministratore di condominio"),
        ("14", "Soggetto che sottoscrive la dichiarazione per conto di una pubblica amministrazione"),
        ("15", "Commissario liquidatore di una pubblica amministrazione")
    ]
    TIPO_PLAFOND = [
        ("1", "Fisso"),
        ("2", "Mobile")
    ]
    ragionesociale = models.CharField(max_length=255, unique=True)
    partita_iva = models.CharField(max_length=20, unique=True)
    codice_fiscale = models.CharField(max_length=16, unique=True)
    indirizzo = models.CharField(max_length=255)
    cap = models.CharField(max_length=5)
    citta = models.CharField(max_length=100)
    provincia = models.CharField(max_length=100)
    paese = models.CharField(max_length=100)
    cf_rappresentante = models.CharField(max_length=16, unique=True, blank=True, null=True)
    codice_carica = models.CharField(
        "Codice Carica", choices=CODICE_CARICA, blank=True
    )
    cognome_rappresentante = models.CharField(max_length=255, blank=True, null=True) 
    nome_rappresentante = models.CharField(max_length=255, blank=True, null=True) 
    data_nascita_rappresentante = models.DateField(blank=True, null=True)
    comune_nascita = models.CharField(max_length=100, blank=True, null=True)
    provincia = models.CharField(max_length=2, blank=True, null=True)
    tel = models.CharField(blank=True, null=True)
    email = models.CharField(blank=True, null=True)
    tipo_plafond = models.CharField(
        "Tipo Plafond", max_length=1, choices=TIPO_PLAFOND, blank=True
    )
    
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
