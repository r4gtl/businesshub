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
from .forms import DichiarazioneIntentoForm, FatturaFornitoreForm


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
    form_class = FatturaFornitoreForm    
    template_name = "documenti/fattura_form.html"
    success_url = reverse_lazy("documenti:fattura_list")

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class FatturaUpdateView(LoginRequiredMixin, UpdateView):
    model = FatturaFornitore
    form_class = FatturaFornitoreForm     
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
