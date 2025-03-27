from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
    TemplateView,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.db.models.functions import ExtractMonth
from .models import DichiarazioneIntento, FatturaFornitore
from .forms import DichiarazioneIntentoForm

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.http import HttpResponse


class DichiarazioneListView(LoginRequiredMixin, ListView):
    model = DichiarazioneIntento
    template_name = "documenti/dichiarazione_list.html"
    context_object_name = "dichiarazioni"


class DichiarazioneIntentoCreateView(LoginRequiredMixin, CreateView):
    model = DichiarazioneIntento
    form_class = DichiarazioneIntentoForm
    template_name = "documenti/dichiarazione_form.html"
    success_url = reverse_lazy("documenti:dichiarazione_list")

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class DichiarazioneIntentoUpdateView(LoginRequiredMixin, UpdateView):
    model = DichiarazioneIntento
    form_class = DichiarazioneIntentoForm
    template_name = "documenti/dichiarazione_form.html"
    success_url = reverse_lazy("documenti:dichiarazione_list")


class DichiarazioneDeleteView(LoginRequiredMixin, DeleteView):
    model = DichiarazioneIntento
    template_name = "documenti/dichiarazione_confirm_delete.html"
    success_url = reverse_lazy("documenti:dichiarazione_list")


class FatturaListView(LoginRequiredMixin, ListView):
    model = FatturaFornitore
    template_name = "documenti/fattura_list.html"
    context_object_name = "fatture"


class FatturaCreateView(LoginRequiredMixin, CreateView):
    model = FatturaFornitore
    fields = ["fornitore", "numero_fattura", "data_fattura", "importo"]
    template_name = "documenti/fattura_form.html"
    success_url = reverse_lazy("documenti:fattura_list")

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class FatturaUpdateView(LoginRequiredMixin, UpdateView):
    model = FatturaFornitore
    fields = ["fornitore", "numero_fattura", "data_fattura", "importo"]
    template_name = "documenti/fattura_form.html"
    success_url = reverse_lazy("documenti:fattura_list")


class FatturaDeleteView(LoginRequiredMixin, DeleteView):
    model = FatturaFornitore
    template_name = "documenti/fattura_confirm_delete.html"
    success_url = reverse_lazy("documenti:fattura_list")


class ReportPlafondView(TemplateView):
    template_name = "documenti/report_plafond.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        selected_anno = self.request.GET.get("anno")
        dichiarazioni_qs = DichiarazioneIntento.objects.select_related("fornitore")

        if selected_anno:
            dichiarazioni_qs = dichiarazioni_qs.filter(anno_riferimento=selected_anno)

        # calcolo anni disponibili per select
        anni_disponibili = (
            DichiarazioneIntento.objects.values_list("anno_riferimento", flat=True)
            .distinct()
            .order_by("-anno_riferimento")
        )
        report_data = []

        for dichiarazione in dichiarazioni_qs:
            # Fatture di quell'anno per quel fornitore
            fatture = FatturaFornitore.objects.filter(
                fornitore=dichiarazione.fornitore,
                data_fattura__year=dichiarazione.anno_riferimento,
            )

            mesi = {i: 0 for i in range(1, 13)}  # da gennaio a dicembre

            tot = 0
            for f in fatture:
                mese = f.data_fattura.month
                mesi[mese] += float(f.importo)
                tot += f.importo

            report_data.append(
                {
                    "fornitore": dichiarazione.fornitore.ragione_sociale,
                    "numero_interno": dichiarazione.numero_interno,
                    "numero_dichiarazione": dichiarazione.numero_dichiarazione,
                    "data_dichiarazione": dichiarazione.data_dichiarazione,
                    "plafond": dichiarazione.plafond,
                    "mesi": [mesi[i] for i in range(1, 13)],
                    "totale": tot,
                    "rimanenza": dichiarazione.plafond - tot,
                }
            )
        context["mesi_nomi"] = [
            "Gen",
            "Feb",
            "Mar",
            "Apr",
            "Mag",
            "Giu",
            "Lug",
            "Ago",
            "Set",
            "Ott",
            "Nov",
            "Dic",
        ]
        context["mesi_num"] = range(1, 13)
        context["report"] = report_data
        context["anni"] = anni_disponibili
        context["anno_selezionato"] = selected_anno

        return context


def dichiarazione_pdf(request, pk):
    dichiarazione = DichiarazioneIntento.objects.get(pk=pk)

    # Crea una risposta HTTP con tipo MIME PDF
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'inline; filename="dichiarazione_{pk}.pdf"'

    # Creazione PDF
    p = canvas.Canvas(response, pagesize=letter)

    # Impostazioni font e dimensioni
    p.setFont("Helvetica", 10)

    # Titolo
    p.setFont("Helvetica-Bold", 14)
    p.drawString(200, 750, "Dichiarazione di Intento")

    # Linea separatrice
    p.line(50, 740, 550, 740)

    # Sezione Emittente
    p.setFont("Helvetica", 10)
    p.drawString(50, 720, "Emittente:")
    p.drawString(50, 705, f"Ragione Sociale: ")
    p.drawString(50, 690, f"P. IVA: ")
    p.drawString(50, 675, f"Codice Fiscale: ")
    p.drawString(50, 660, f"Indirizzo: ")
    p.drawString(50, 645, f"CAP:  Comune: ")
    p.drawString(50, 630, f"Provincia:  Paese: ")

    # Linea separatrice
    p.line(50, 625, 550, 625)

    # Sezione Dichiarante
    p.drawString(50, 610, "Dichiarante:")
    p.drawString(50, 595, f"Ragione Sociale: {dichiarazione.fornitore.ragione_sociale}")
    p.drawString(50, 580, f"P. IVA: {dichiarazione.fornitore.partita_iva}")
    p.drawString(50, 565, f"Codice Fiscale: {dichiarazione.fornitore.codice_fiscale}")
    p.drawString(50, 550, f"Indirizzo: {dichiarazione.fornitore.indirizzo}")
    p.drawString(
        50,
        535,
        f"CAP: {dichiarazione.fornitore.cap} Comune: {dichiarazione.fornitore.citta}",
    )
    p.drawString(
        50,
        520,
        f"Provincia: {dichiarazione.fornitore.provincia} Paese: {dichiarazione.fornitore.paese}",
    )

    # Linea separatrice
    p.line(50, 505, 550, 505)

    # Sezione Dichiarazione
    p.drawString(50, 490, f"Numero Dichiarazione: {dichiarazione.numero_dichiarazione}")
    p.drawString(
        50, 475, f"Data: {dichiarazione.data_dichiarazione.strftime('%d/%m/%Y')}"
    )
    p.drawString(50, 460, f"Anno di riferimento: {dichiarazione.anno_riferimento}")
    p.drawString(50, 445, f"Plafond: € {dichiarazione.plafond:.2f}")
    p.drawString(50, 430, f"Tipo Operazione: {dichiarazione.tipo_operazione}")
    p.drawString(
        50,
        415,
        f"Importo Singola Operazione: {'Sì' if dichiarazione.importosingolo else 'No'}",
    )
    p.drawString(50, 400, f"Dogana: {dichiarazione.fk_dogana}")

    # Linea separatrice
    p.line(50, 385, 550, 385)

    # Sezione Note
    p.drawString(
        50, 370, f"Note: {dichiarazione.note if dichiarazione.note else 'Nessuna'}"
    )

    # Linea separatrice finale
    p.line(50, 355, 550, 355)

    # Firma e Luogo
    p.drawString(50, 340, "Luogo e Data: ______________________________")
    p.drawString(50, 325, "Firma del Dichiarante: ________________________")

    # Salva il PDF
    p.showPage()
    p.save()

    return response
