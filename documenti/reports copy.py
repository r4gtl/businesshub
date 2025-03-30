from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
import io
from django.http import HttpResponse
from documenti.models import DichiarazioneIntento


# Definizione degli stili per titolo e sottotitoli (allineati al centro) ed etichette
style_title = ParagraphStyle(
    "Title", fontName="Helvetica", fontSize=0.5 * cm, alignment=TA_CENTER
)  # 0.5 cm ≈ 14 pt
style_subtitle = ParagraphStyle(
    "Subtitle", fontName="Helvetica", fontSize=0.2 * cm, alignment=TA_CENTER
)  # 0.2 cm ≈ 5.7 pt
style_label = ParagraphStyle(
    "Label", fontName="Helvetica", fontSize=8, alignment=TA_CENTER
)  # Etichette campo (circa 8 pt)
style_left_label = ParagraphStyle(
    "LeftLabel", fontName="Helvetica", fontSize=8, alignment=TA_LEFT
)  # Label colonna sinistra

style_value = ParagraphStyle(
    name="ValueStyle", fontName="Helvetica", fontSize=9, leading=12
)

def dichiarazione_intento(request, pk)
    dichiarazione= DichiarazioneIntento.objects.get(pk=pk)
    
    
    
def dichiarazione_intento_pdf(request, pk):
    dichiarazione = DichiarazioneIntento.objects.get(pk=pk)

    # Impostazione della risposta HTTP come PDF
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'inline; filename="dichiarazione_{pk}.pdf"'

    # Creazione di un buffer in memoria per il PDF
    buffer = io.BytesIO()

    # Configurazione del documento PDF
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=0.5 * cm,
        rightMargin=0.5 * cm,
        topMargin=3.5 * cm,
        bottomMargin=1 * cm,
    )

    # Creazione delle tabelle per le due sezioni
    dati1 = dati_dichiarante(dichiarazione)
    dati2 = dati_rappresentante(dichiarazione)

    # Definizione dello stile comune per entrambe le tabelle
    table_style = TableStyle(
        [
            # SPAN per titolo principale nella prima riga
            ("SPAN", (0, 0), (3, 0)),
            # SPAN per la prima colonna (celle (0,1) a (0,5))
            ("SPAN", (0, 1), (0, 5)),
            # Allineamento verticale della prima colonna
            ("VALIGN", (0, 1), (0, 5), "MIDDLE"),
            # Bordi esterni della tabella
            ("BOX", (0, 0), (3, 5), 1, colors.black),
            # Bordi per tutti i campi
            ("GRID", (1, 1), (3, 5), 0.5, colors.black),
            # Linee orizzontali principali
            ("LINEABOVE", (0, 1), (3, 1), 1, colors.black),
            ("LINEBELOW", (0, 5), (3, 5), 1, colors.black),
            # Sfondo grigio per la prima colonna
            ("BACKGROUND", (0, 1), (0, 5), colors.whitesmoke),
            # Sfondo grigio per la seconda colonna
            ("BACKGROUND", (1, 1), (1, 5), colors.whitesmoke),
        ]
    )

    # Creazione e stilizzazione delle tabelle
    table1 = Table(dati1, colWidths=[2.6 * cm, 8 * cm, 6 * cm, 3.4 * cm])
    table1.setStyle(table_style)

    table2 = Table(dati2, colWidths=[2.6 * cm, 8 * cm, 6 * cm, 3.4 * cm])
    table2.setStyle(table_style)

    # Aggiunta delle tabelle alla storia del documento con uno spazio tra di esse
    story = [table1, Spacer(1, 0.5 * cm), table2]

    # Costruzione del PDF
    doc.build(story)

    # Scrittura del PDF nel buffer e ritorno della risposta
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response


def dichiarazione_intento_pdf_old(request, pk):
    dichiarazione = DichiarazioneIntento.objects.get(pk=pk)

    # Impostazione della risposta HTTP come PDF
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'inline; filename="dichiarazione_{pk}.pdf"'

    # Creazione di un buffer in memoria per il PDF
    buffer = io.BytesIO()

    # Configurazione del documento PDF
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=0.5 * cm,
        rightMargin=0.5 * cm,
        topMargin=3.5 * cm,
        bottomMargin=1 * cm,
    )

    # Creazione delle tabelle per le due sezioni
    dati1 = dati_dichiarante(dichiarazione)
    dati2 = dati_rappresentante(dichiarazione)

    # Creazione delle tabelle senza ridefinire TableStyle (questo è già definito nelle funzioni minori)
    table1 = Table(dati1, colWidths=[2.6 * cm, 8 * cm, 6 * cm, 3.4 * cm])
    table2 = Table(dati2, colWidths=[2.6 * cm, 8 * cm, 6 * cm, 3.4 * cm])
    # table2 = dati_rappresentante(dichiarazione)

    # Aggiunta delle tabelle alla storia del documento
    story = [table1, table2]

    # Costruzione del PDF
    doc.build(story)

    # Scrittura del PDF nel buffer e ritorno della risposta
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response


def dati_dichiarante(dichiarazione):
    # Etichette e valori per la prima sezione (DATI DEL DICHIARANTE)
    left_col_text = Paragraph("DATI DEL<br/>DICHIARANTE", style_left_label)

    # Etichette per i campi
    label_cf = Paragraph("Codice Fiscale", style_label)
    label_piva = Paragraph("Partita IVA", style_label)
    label_ragione = Paragraph("Ragione Sociale", style_label)
    label_nome = Paragraph("Nome", style_label)
    label_sesso = Paragraph("Sesso (M/F)", style_label)
    label_data = Paragraph("Data di Nascita", style_label)
    label_comune = Paragraph("Comune/Stato estero di nascita", style_label)
    label_prov = Paragraph("Provincia (sigla)", style_label)

    # Aggiunta dei valori ai campi
    cf_value = dichiarazione.fornitore.codice_fiscale
    piva_value = dichiarazione.fornitore.partita_iva
    ragione_value = dichiarazione.fornitore.ragione_sociale
    nome_value = " "  # Nome vuoto
    sesso_value = ""  # Campo sesso vuoto (checkbox)
    data_value = " "  # Data di nascita vuota
    comune_value = ""  # Comune vuoto
    prov_value = ""  # Provincia vuota

    # Costruzione della tabella per i dati del dichiarante
    data = [
        [left_col_text, label_cf, label_piva, None],
        [None, cf_value, piva_value, None],
        [None, label_ragione, label_nome, label_sesso],
        [None, ragione_value, nome_value, sesso_value],
        [None, label_data, label_comune, label_prov],
        [None, data_value, comune_value, prov_value],
    ]

    # Modifica la larghezza delle colonne
    col_widths = [2.6 * cm, 8 * cm, 6 * cm, 3.4 * cm]

    return data


def dati_rappresentante(dichiarazione):
    # Etichette per la sezione "Dati relativi al rappresentante firmatario"
    left_col_text_2 = Paragraph(
        "DATI RELATIVI AL RAPPRESENTANTE FIRMATARIO DELLA DICHIARAZIONE",
        style_left_label,
    )

    # Etichette per i campi
    label_cf2 = Paragraph("Codice Fiscale", style_label)
    label_carica = Paragraph("Codice Carica", style_label)
    label_cf_societa = Paragraph("Codice Fiscale Società", style_label)
    label_cognome = Paragraph("Cognome", style_label)
    label_nome2 = Paragraph("Nome", style_label)
    label_sesso2 = Paragraph("Sesso (M/F)", style_label)
    label_data2 = Paragraph("Data di Nascita", style_label)
    label_comune2 = Paragraph("Comune/Stato estero di nascita", style_label)
    label_prov2 = Paragraph("Provincia (sigla)", style_label)

    # Aggiunta dei valori ai campi (tutti i valori sono impostati a una stringa vuota " ")
    cf2_value = " "
    carica_value = " "
    cf_societa_value = " "
    cognome_value = " "
    nome2_value = " "
    sesso2_value = " "
    data2_value = " "
    comune2_value = " "
    prov2_value = " "

    # Costruzione della tabella per i dati del rappresentante firmatario
    data2 = [
        [left_col_text_2, label_cf2, label_carica, label_cf_societa],
        [None, cf2_value, carica_value, cf_societa_value],
        [None, label_cognome, label_nome2, label_sesso2],
        [None, cognome_value, nome2_value, sesso2_value],
        [None, label_data2, label_comune2, label_prov2],
        [None, data2_value, comune2_value, prov2_value],
    ]

    # Modifica la larghezza delle colonne - uguale alla prima funzione
    col_widths = [2.6 * cm, 8 * cm, 6 * cm, 3.4 * cm]

    return data2


def dati_dichiarante_old(dichiarazione):
    # Etichette e valori per la prima sezione (DATI DEL DICHIARANTE)
    left_col_text = Paragraph("DATI DEL<br/>DICHIARANTE", style_left_label)

    # Etichette per i campi
    label_cf = Paragraph("Codice Fiscale", style_label)
    label_piva = Paragraph("Partita IVA", style_label)
    label_ragione = Paragraph("Ragione Sociale", style_label)
    label_nome = Paragraph("Nome", style_label)
    label_sesso = Paragraph("Sesso (M/F)", style_label)
    label_data = Paragraph("Data di Nascita", style_label)
    label_comune = Paragraph("Comune/Stato estero di nascita", style_label)
    label_prov = Paragraph("Provincia (sigla)", style_label)

    # Aggiunta dei valori ai campi
    cf_value = dichiarazione.fornitore.codice_fiscale
    piva_value = dichiarazione.fornitore.partita_iva
    ragione_value = dichiarazione.fornitore.ragione_sociale
    nome_value = " "  # Nome vuoto
    sesso_value = ""  # Campo sesso vuoto (checkbox)
    data_value = " "  # Data di nascita vuota
    comune_value = ""  # Comune vuoto
    prov_value = ""  # Provincia vuota

    # Costruzione della tabella per i dati del dichiarante
    data = [
        [left_col_text, label_cf, label_piva, None],
        [None, cf_value, piva_value, None],
        [None, label_ragione, label_nome, label_sesso],
        [None, ragione_value, nome_value, sesso_value],
        [None, label_data, label_comune, label_prov],
        [None, data_value, comune_value, prov_value],
    ]

    # Modifica la larghezza delle colonne e controlla il numero di righe
    col_widths = [2.6 * cm, 8 * cm, 6 * cm, 3.4 * cm]

    # Creazione della tabella con modifiche
    table = Table(data, colWidths=col_widths)

    # Definizione del TableStyle
    table_style = TableStyle(
        [
            ("SPAN", (0, 0), (3, 0)),  # Titolo
            ("SPAN", (0, 1), (3, 1)),  # Sottotitolo 1
            ("SPAN", (0, 2), (3, 2)),  # Sottotitolo 2
            ("SPAN", (0, 3), (0, 5)),  # Unione solo per 3 righe in questa sezione
            ("VALIGN", (0, 3), (0, 5), "MIDDLE"),
            ("LINEABOVE", (0, 3), (3, 3), 1, colors.black),
            ("LINEBELOW", (0, 5), (3, 5), 1, colors.black),
            ("BACKGROUND", (0, 3), (0, 5), colors.white),
            ("BACKGROUND", (1, 3), (3, 5), colors.whitesmoke),
        ]
    )

    table.setStyle(table_style)

    return data


def dati_rappresentante_old1(dichiarazione):
    # Etichette per la sezione "Dati relativi al rappresentante firmatario"
    left_col_text_2 = Paragraph(
        "DATI RELATIVI AL RAPPRESENTANTE FIRMATARIO DELLA DICHIARAZIONE",
        style_left_label,
    )

    # Etichette per i campi
    label_cf2 = Paragraph("Codice Fiscale", style_label)
    label_carica = Paragraph("Codice Carica", style_label)
    label_cf_societa = Paragraph("Codice Fiscale Società", style_label)
    label_cognome = Paragraph("Cognome", style_label)
    label_nome2 = Paragraph("Nome", style_label)
    label_sesso2 = Paragraph("Sesso (M/F)", style_label)
    label_data2 = Paragraph("Data di Nascita", style_label)
    label_comune2 = Paragraph("Comune/Stato estero di nascita", style_label)
    label_prov2 = Paragraph("Provincia (sigla)", style_label)

    # Aggiunta dei valori ai campi (tutti i valori sono impostati a una stringa vuota " ")
    cf2_value = " "
    carica_value = " "
    cf_societa_value = " "
    cognome_value = " "
    nome2_value = " "
    sesso2_value = " "
    data2_value = " "
    comune2_value = " "
    prov2_value = " "

    # Costruzione della tabella per i dati del rappresentante firmatario
    data2 = [
        [left_col_text_2, label_cf2, label_carica, label_cf_societa],
        [None, cf2_value, carica_value, cf_societa_value],
        [None, label_cognome, label_nome2, label_sesso2],
        [None, cognome_value, nome2_value, sesso2_value],
        [None, label_data2, label_comune2, label_prov2],
        [None, data2_value, comune2_value, prov2_value],
    ]

    # Modifica la larghezza delle colonne - ora uguale alla prima funzione
    col_widths = [2.6 * cm, 8 * cm, 6 * cm, 3.4 * cm]

    # Non creiamo e restituiamo la tabella qui, ma solo i dati
    return data2


def dati_rappresentante_old(dichiarazione):
    # Etichette per la sezione "Dati relativi al rappresentante firmatario"
    left_col_text_2 = Paragraph(
        "DATI RELATIVI AL RAPPRESENTANTE FIRMATARIO DELLA DICHIARAZIONE",
        style_left_label,
    )

    # Etichette per i campi
    label_cf2 = Paragraph("Codice Fiscale", style_label)
    label_carica = Paragraph("Codice Carica", style_label)
    label_cf_societa = Paragraph("Codice Fiscale Società", style_label)
    label_cognome = Paragraph("Cognome", style_label)
    label_nome2 = Paragraph("Nome", style_label)
    label_sesso2 = Paragraph("Sesso (M/F)", style_label)
    label_data2 = Paragraph("Data di Nascita", style_label)
    label_comune2 = Paragraph("Comune/Stato estero di nascita", style_label)
    label_prov2 = Paragraph("Provincia (sigla)", style_label)

    # Aggiunta dei valori ai campi (valori vuoti se non esistono dati)
    cf2_value = " "

    carica_value = " "

    cf_societa_value = " "

    cognome_value = " "

    nome2_value = " "

    sesso2_value = " "

    data2_value = " "

    comune2_value = " "

    prov2_value = " "

    # Costruzione della tabella per i dati del rappresentante firmatario
    data2 = [
        [left_col_text_2, label_cf2, label_carica, label_cf_societa],
        [None, cf2_value, carica_value, cf_societa_value],
        [None, label_cognome, label_nome2, label_sesso2],
        [None, cognome_value, nome2_value, sesso2_value],
        [None, label_data2, label_comune2, label_prov2],
        [None, data2_value, comune2_value, prov2_value],
    ]

    # Definizione delle larghezze delle colonne
    col_widths = [2.6 * cm, 8 * cm, 6 * cm, 3.4 * cm]

    # Creazione della tabella
    table2 = Table(data2, colWidths=col_widths)

    # Definizione del TableStyle
    table_style = TableStyle(
        [
            ("SPAN", (0, 0), (3, 0)),  # Unione della prima riga (titolo)
            ("SPAN", (0, 1), (3, 1)),  # Unione della seconda riga (dati)
            ("SPAN", (0, 2), (3, 2)),  # Unione della terza riga (etichette)
            ("SPAN", (0, 3), (3, 3)),  # Unione della quarta riga (etichette)
            ("SPAN", (0, 4), (3, 4)),  # Unione della quinta riga (etichette)
            ("SPAN", (0, 5), (3, 5)),  # Unione della sesta riga (etichette)
            (
                "VALIGN",
                (0, 1),
                (0, 5),
                "MIDDLE",
            ),  # Allineamento verticale della colonna 0
            (
                "LINEABOVE",
                (0, 3),
                (3, 3),
                1,
                colors.black,
            ),  # Linea sopra la quarta riga
            ("LINEBELOW", (0, 5), (3, 5), 1, colors.black),  # Linea sotto la sesta riga
            (
                "BACKGROUND",
                (0, 3),
                (0, 5),
                colors.white,
            ),  # Colore di sfondo per la colonna 0 nelle righe 3-5
            (
                "BACKGROUND",
                (1, 3),
                (3, 5),
                colors.whitesmoke,
            ),  # Colore di sfondo per le colonne 1-3 nelle righe 3-5
        ]
    )

    # Applica il style alla tabella
    table2.setStyle(table_style)

    return table2


"""import io
from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT

from .models import DichiarazioneIntento  # Assicurati di importare il modello


def dichiarazione_intento_pdf(request, pk):
    # Recupera la DichiarazioneIntento specifica con il pk
    dichiarazione = DichiarazioneIntento.objects.get(pk=pk)

    # Impostazione della risposta HTTP come PDF
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'inline; filename="dichiarazione_intento.pdf"'

    # Creazione di un buffer in memoria per il PDF
    buffer = io.BytesIO()

    # Configurazione del documento PDF con margini (3.5 cm dall'alto, 0.5 cm laterali)
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=0.5 * cm,
        rightMargin=0.5 * cm,
        topMargin=3.5 * cm,
        bottomMargin=1 * cm,
    )

    # Registrazione del font Arial (assicurarsi che 'Arial.ttf' sia disponibile nel sistema)
    # pdfmetrics.registerFont(TTFont("Helvetica", "Helvetica.ttf"))

    # Definizione degli stili per titolo e sottotitoli (allineati al centro) ed etichette
    style_title = ParagraphStyle(
        "Title", fontName="Helvetica", fontSize=0.5 * cm, alignment=TA_CENTER
    )  # 0.5 cm ≈ 14 pt
    style_subtitle = ParagraphStyle(
        "Subtitle", fontName="Helvetica", fontSize=0.2 * cm, alignment=TA_CENTER
    )  # 0.2 cm ≈ 5.7 pt
    style_label = ParagraphStyle(
        "Label", fontName="Helvetica", fontSize=8, alignment=TA_CENTER
    )  # Etichette campo (circa 8 pt)
    style_left_label = ParagraphStyle(
        "LeftLabel", fontName="Helvetica", fontSize=8, alignment=TA_LEFT
    )  # Label colonna sinistra

    # Testi per titolo e sottotitoli
    title = Paragraph("DICHIARAZIONE D'INTENTO", style_title)
    subtitle1 = Paragraph(
        "DI ACQUISTARE O IMPORTARE BENI E SERVIZI SENZA", style_subtitle
    )
    subtitle2 = Paragraph(
        "APPLICAZIONE DELL'IMPOSTA SUL VALORE AGGIUNTO", style_subtitle
    )

    # Testo colonna sinistra (con eventuale a capo per lunghe stringhe)
    left_col_text = Paragraph("DATI DEL<br/>DICHIARANTE", style_left_label)

    # Etichette per i campi (colonna destra)
    label_cf = Paragraph("Codice Fiscale", style_label)
    label_piva = Paragraph("Partita IVA", style_label)
    label_ragione = Paragraph("Ragione Sociale", style_label)
    label_nome = Paragraph("Nome", style_label)
    label_sesso = Paragraph("Sesso (M/F)", style_label)
    label_data = Paragraph("Data di Nascita", style_label)
    label_comune = Paragraph("Comune/Stato estero di nascita", style_label)
    label_prov = Paragraph("Provincia (sigla)", style_label)

    # Recupera i dati dalla dichiarazione
    cf_value = dichiarazione.fornitore.codice_fiscale
    piva_value = dichiarazione.fornitore.partita_iva
    ragione_value = dichiarazione.fornitore.ragione_sociale
    nome_value = "N/A"  # Aggiungi un campo fittizio se necessario
    sesso_value = "M"  # Aggiungi un campo fittizio se necessario
    data_value = "01/01/1980"  # Aggiungi un campo fittizio se necessario
    comune_value = dichiarazione.fornitore.citta
    prov_value = dichiarazione.fornitore.provincia

    # Costruzione della tabella con 4 colonne:
    # [Colonna sinistra, Colonna destra 1, Colonna destra 2, Colonna destra 3]
    data = [
        [title, None, None, None],  # Riga 0: Titolo (span su 4 colonne)
        [subtitle1, None, None, None],  # Riga 1: Sottotitolo 1 (span)
        [subtitle2, None, None, None],  # Riga 2: Sottotitolo 2 (span)
        [
            left_col_text,
            label_cf,
            label_piva,
            None,
        ],  # Riga 3: Etichette campi riga 1 (col3 vuota)
        [None, cf_value, piva_value, None],  # Riga 4: Valori campi riga 1 (col3 vuota)
        [
            None,
            label_ragione,
            label_nome,
            label_sesso,
        ],  # Riga 5: Etichette campi riga 2
        [None, ragione_value, nome_value, sesso_value],  # Riga 6: Valori campi riga 2
        [None, label_data, label_comune, label_prov],  # Riga 7: Etichette campi riga 3
        [None, data_value, comune_value, prov_value],  # Riga 8: Valori campi riga 3
    ]

    # Definizione della larghezza delle colonne:
    #  - Colonna sinistra: 2.6 cm
    #  - Colonne destra 1,2,3: larghezze ripartite per i campi
    col_widths = [2.6 * cm, 8 * cm, 6 * cm, 3.4 * cm]

    # Creazione tabella
    table = Table(data, colWidths=col_widths)

    # Stile tabella
    table_style = TableStyle(
        [
            # Unione celle (SPAN) per titolo e sottotitoli su 4 colonne
            ("SPAN", (0, 0), (3, 0)),  # Titolo
            ("SPAN", (0, 1), (3, 1)),  # Sottotitolo 1
            ("SPAN", (0, 2), (3, 2)),  # Sottotitolo 2
            # Unione celle colonna sinistra dalla riga 3 alla riga 8 (sezione DATI DEL DICHIARANTE)
            ("SPAN", (0, 3), (0, 8)),
            # Allineamento verticale al centro per il testo nella colonna sinistra unita
            ("VALIGN", (0, 3), (0, 8), "MIDDLE"),
            # Bordi superiore e inferiore dell'intera sezione (da margine a margine)
            (
                "LINEABOVE",
                (0, 3),
                (3, 3),
                1,
                colors.black,
            ),  # linea superiore (sopra la riga 3)
            (
                "LINEBELOW",
                (0, 8),
                (3, 8),
                1,
                colors.black,
            ),  # linea inferiore (sotto la riga 8)
            # Impostazione sfondi: bianco per colonna sinistra, grigio chiaro per colonna destra
            ("BACKGROUND", (0, 3), (0, 8), colors.white),
            ("BACKGROUND", (1, 3), (3, 8), colors.whitesmoke),
            # Nessun bordo verticale interno (implicitamente, non definendo linee verticali tra col0 e col1)
            # Disegno dei rettangoli vuoti per i campi (bordo di 0.5 pt intorno alle celle vuote corrispondenti ai campi)
        ]
    )
    # Aggiunta bordi (rettangoli) attorno a ciascun campo:
    # Riga 4 (Codice Fiscale, Partita IVA)
    table_style.add(
        "BOX", (1, 4), (1, 4), 0.5, colors.black
    )  # rettangolo Codice Fiscale
    table_style.add("BOX", (2, 4), (2, 4), 0.5, colors.black)  # rettangolo Partita IVA
    # Riga 6 (Ragione Sociale, Nome, Sesso)
    table_style.add(
        "BOX", (1, 6), (1, 6), 0.5, colors.black
    )  # rettangolo Ragione Sociale
    table_style.add("BOX", (2, 6), (2, 6), 0.5, colors.black)  # rettangolo Nome
    table_style.add("BOX", (3, 6), (3, 6), 0.5, colors.black)  # rettangolo Sesso (M/F)
    # Riga 8 (Data di Nascita, Comune/Stato, Provincia)
    table_style.add(
        "BOX", (1, 8), (1, 8), 0.5, colors.black
    )  # rettangolo Data di Nascita
    table_style.add(
        "BOX", (2, 8), (2, 8), 0.5, colors.black
    )  # rettangolo Comune/Stato estero
    table_style.add(
        "BOX", (3, 8), (3, 8), 0.5, colors.black
    )  # rettangolo Provincia (sigla)

    table.setStyle(table_style)

    # Costruzione del PDF
    story = [table]
    doc.build(story)

    # Scrittura del PDF nel buffer e ritorno della risposta
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response"""
