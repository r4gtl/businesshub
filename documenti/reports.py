from django.shortcuts import render, get_object_or_404
from .models import (
    DichiarazioneIntento,
)  # Assumendo che tu abbia un modello Dichiarazione
from django.template.loader import render_to_string
from weasyprint import HTML
from django.http import HttpResponse


def dichiarazione_intento(request, pk):
    # Ottieni la dichiarazione dal database usando il pk
    dichiarazione = get_object_or_404(DichiarazioneIntento, pk=pk)

    # Prepara i dati da passare al template
    data = {
        "cf_value": (
            dichiarazione.fornitore.codice_fiscale
            if dichiarazione.fornitore.codice_fiscale
            else " "
        ),
        "piva_value": (
            dichiarazione.fornitore.partita_iva
            if dichiarazione.fornitore.partita_iva
            else " "
        ),
        "ragione_value": (
            dichiarazione.fornitore.ragione_sociale
            if dichiarazione.fornitore.ragione_sociale
            else " "
        ),
        "nome_value": " ",
        "sesso_value": " ",
        "data_value": " ",
        "comune_value": " ",
        "prov_value": " ",
        # Dati del rappresentante (da personalizzare)
        "cf2_value": " ",
        "carica_value": " ",
        "cf_societa_value": " ",
        "cognome_value": " ",
        "nome2_value": " ",
        "sesso2_value": " ",
        "data2_value": " ",
        "comune2_value": " ",
        "prov2_value": " ",
    }

    # Renderizza il template HTML con i dati
    html_string = render_to_string("documenti/reports/dichiarazione_intento.html", data)

    # Usa WeasyPrint per generare il PDF dal template HTML
    html = HTML(string=html_string)
    pdf = html.write_pdf()

    # Restituisce il PDF come risposta HTTP
    response = HttpResponse(pdf, content_type="application/pdf")
    response["Content-Disposition"] = (
        'inline; filename="dichiarazione_intento_{}.pdf"'.format(pk)
    )
    return response
