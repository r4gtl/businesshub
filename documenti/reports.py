from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch, cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors

from documenti.models import DichiarazioneIntento
from django.http import HttpResponse


def dichiarazione_pdf(request, pk):
    dichiarazione = DichiarazioneIntento.objects.get(pk=pk)

    # Crea una risposta HTTP con tipo MIME PDF
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'inline; filename="dichiarazione_{pk}.pdf"'

    # Creazione del PDF
    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter

    # Impostazioni font e dimensioni
    p.setFont("Helvetica-Bold", 14)

    # Titolo "DICHIARAZIONE D'INTENTO"
    p.drawCentredString(width / 2, height - 3.5 * cm, "DICHIARAZIONE D'INTENTO")

    # Sottotitoli
    p.setFont("Helvetica", 8)
    p.drawCentredString(
        width / 2, height - 4.5 * cm, "DI ACQUISTARE O IMPORTARE BENI E SERVIZI SENZA"
    )
    p.drawCentredString(
        width / 2, height - 5.5 * cm, "APPLICAZIONE DELL'IMPOSTA SUL VALORE AGGIUNTO"
    )

    # Linea separatrice
    p.setLineWidth(0.5)
    p.line(10, height - 6.5 * cm, width - 10, height - 6.5 * cm)

    # Sezione Dati del Dichiarante
    p.setFont("Helvetica-Bold", 10)
    p.drawString(10, height - 7.5 * cm, "DATI DEL DICHIARANTE")

    # Linea separatrice
    p.setLineWidth(0.5)
    p.line(10, height - 8 * cm, width - 10, height - 8 * cm)

    # Creazione tabella con i dati del dichiarante
    data = [
        ["Codice Fiscale", "Partita IVA"],
        ["Ragione Sociale", "Nome", "Sesso (M/F)"],
        ["Data di Nascita", "Comune di Nascita", "Provincia"],
    ]

    # Prima colonna bianca, seconda colonna grigia
    table = Table(data, colWidths=[2.6 * cm, 5 * cm, 5 * cm])

    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (0, -1), colors.white),
                ("BACKGROUND", (1, 0), (1, -1), colors.lightgrey),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
                ("FONTSIZE", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
            ]
        )
    )

    # Aggiungi la tabella al documento
    table.wrapOn(p, width, height)
    table.drawOn(p, 10, height - 12 * cm)

    # Linea separatrice finale
    p.setLineWidth(0.5)
    p.line(10, height - 15 * cm, width - 10, height - 15 * cm)

    # Firma e Luogo
    p.setFont("Helvetica", 8)
    p.drawString(10, height - 16 * cm, "Luogo e Data: ______________________________")
    p.drawString(
        10, height - 17 * cm, "Firma del Dichiarante: ________________________"
    )

    # Salva il PDF
    p.showPage()
    p.save()

    return response
