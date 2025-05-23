from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
    TemplateView,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum, OuterRef, Subquery, Max, Count
from django.db.models.functions import ExtractMonth
from django.utils.timezone import now
from .models import DichiarazioneIntento, FatturaFornitore, Durc
from .forms import DichiarazioneIntentoForm, FatturaFornitoreForm, DurcForm
from anagrafiche.models import Fornitore, Dogana
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
import json


class DichiarazioneListView(LoginRequiredMixin, ListView):
    model = DichiarazioneIntento
    template_name = "documenti/dichiarazione_list.html"
    context_object_name = "dichiarazioni"

    def get_queryset(self):
        # Ottieni l'azienda dell'utente loggato
        azienda = self.request.user.azienda

        # Filtra le dichiarazioni in base all'azienda dell'utente loggato
        return DichiarazioneIntento.objects.filter(azienda=azienda)


class DichiarazioneIntentoCreateView(LoginRequiredMixin, CreateView):
    model = DichiarazioneIntento
    form_class = DichiarazioneIntentoForm
    template_name = "documenti/dichiarazione_form.html"
    success_url = reverse_lazy("documenti:dichiarazione_list")

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # Passa l'utente loggato al form
        kwargs["user"] = self.request.user
        return kwargs


class DichiarazioneIntentoUpdateView(LoginRequiredMixin, UpdateView):
    model = DichiarazioneIntento
    form_class = DichiarazioneIntentoForm
    template_name = "documenti/dichiarazione_form.html"
    success_url = reverse_lazy("documenti:dichiarazione_list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # Passa l'utente loggato al form
        kwargs["user"] = self.request.user
        return kwargs


class DichiarazioneDeleteView(LoginRequiredMixin, DeleteView):
    model = DichiarazioneIntento
    template_name = "documenti/dichiarazione_confirm_delete.html"
    success_url = reverse_lazy("documenti:dichiarazione_list")


class FatturaListView(ListView):
    model = FatturaFornitore
    template_name = "documenti/fattura_list.html"
    context_object_name = "fatture"

    def get_queryset(self):
        # Ottieni la queryset iniziale
        queryset = super().get_queryset()

        # Filtro per i parametri passati nella query string
        numero_fattura = self.request.GET.get("numero_fattura", "")
        fornitore = self.request.GET.get("fornitore", "")
        data_fattura = self.request.GET.get("data_fattura", "")
        importo = self.request.GET.get("importo", "")

        # Filtra per numero_fattura
        if numero_fattura:
            queryset = queryset.filter(numero_fattura__icontains=numero_fattura)

        # Filtra per fornitore
        if fornitore:
            queryset = queryset.filter(fornitore__ragione_sociale__icontains=fornitore)

        # Filtra per data_fattura
        if data_fattura:
            queryset = queryset.filter(data_fattura=data_fattura)

        # Filtra per importo
        if importo:
            try:
                # Converti importo da stringa a decimal
                importo_val = Decimal(importo.replace(",", "."))
                queryset = queryset.filter(importo=importo_val)
            except (ValueError, decimal.InvalidOperation):
                # Ignora se il valore non è un numero valido
                pass

        return queryset

    def render_to_response(self, context, **kwargs):
        # Verifica se la richiesta è AJAX o ha il parametro ajax=true
        is_ajax = (
            self.request.headers.get("x-requested-with") == "XMLHttpRequest"
            or self.request.GET.get("ajax") == "true"
        )

        if is_ajax:
            # Restituisce solo il contenuto della tabella
            return HttpResponse(
                render(
                    self.request, "documenti/partials/_table_fatture.html", context
                ).content
            )

        # Altrimenti restituisce il template completo
        return super().render_to_response(context, **kwargs)


class FatturaCreateView(LoginRequiredMixin, CreateView):
    model = FatturaFornitore
    form_class = FatturaFornitoreForm
    template_name = "documenti/fattura_form.html"
    success_url = reverse_lazy("documenti:fattura_list")

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # Passa l'utente loggato al form
        kwargs["user"] = self.request.user
        return kwargs


@require_POST
@login_required
def fattura_check(request):
    data = json.loads(request.body)
    qs = FatturaFornitore.objects.filter(
        fornitore_id=data["fornitore"],
        data_fattura=data["data_fattura"],
        importo=data["importo"],
    )
    # Escludi la riga corrente in caso di edit
    if data.get("instance_id"):
        qs = qs.exclude(pk=data["instance_id"])
    duplicates = list(qs.values("id", "numero_fattura", "data_fattura", "importo"))
    return JsonResponse({"duplicates": duplicates})


class FatturaUpdateView(LoginRequiredMixin, UpdateView):
    model = FatturaFornitore
    form_class = FatturaFornitoreForm

    template_name = "documenti/fattura_form.html"
    success_url = reverse_lazy("documenti:fattura_list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # Aggiungi l'oggetto (istanza) al form per garantire che i dati siano inclusi
        instance = self.get_object()
        print(
            instance.data_fattura
        )  # Stampa la data_fattura per vedere se è correttamente impostata
        kwargs["instance"] = instance
        # Passa l'utente loggato al form
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class FatturaDeleteView(LoginRequiredMixin, DeleteView):
    model = FatturaFornitore
    template_name = "documenti/fattura_confirm_delete.html"
    success_url = reverse_lazy("documenti:fattura_list")


class ReportPlafondView(TemplateView):
    template_name = "documenti/report_plafond.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        selected_anno = self.request.GET.get("anno")
        user_azienda = self.request.user.azienda

        dichiarazioni_qs = (
            DichiarazioneIntento.objects.select_related("fornitore")
            .filter(azienda=user_azienda)
            .order_by("numero_interno")
        )

        if selected_anno:
            dichiarazioni_qs = dichiarazioni_qs.filter(anno_riferimento=selected_anno)

        # Calcolo anni disponibili per select
        anni_disponibili = (
            DichiarazioneIntento.objects.values_list("anno_riferimento", flat=True)
            .distinct()
            .order_by("-anno_riferimento")
        )
        report_data = []
        totali_mensili = [0] * 12  # Totali mensili da mostrare nella tabella

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

            # Calcolo il totale per mese
            for mese in range(1, 13):
                totali_mensili[mese - 1] += mesi[mese]

            # Aggiungi la riga di report per questo fornitore
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
                    "percentuale": (
                        (dichiarazione.plafond - tot) / dichiarazione.plafond * 100
                        if dichiarazione.plafond
                        else 0
                    ),
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
        context["totali_mensili"] = (
            totali_mensili  # Aggiungi i totali mensili al contesto
        )
        context["mesi_num"] = range(1, 13)
        context["report"] = report_data
        context["anni"] = anni_disponibili
        context["anno_selezionato"] = selected_anno

        return context


class DurcListView(LoginRequiredMixin, ListView):
    model = Durc
    template_name = "durc/durc_list.html"
    context_object_name = "durc_list"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["today"] = now().date()
        return context

    def get_queryset(self):
        # Sottoselezione: prendi il DURC più recente per ogni fornitore
        latest_durc_ids = (
            Durc.objects.filter(fornitore=OuterRef("fornitore"))
            .order_by("-scadenza_durc")
            .values("id")[:1]
        )

        queryset = (
            Durc.objects.filter(
                id__in=Subquery(
                    Durc.objects.filter(
                        id__in=Durc.objects.filter(fornitore=OuterRef("fornitore"))
                        .order_by("-scadenza_durc")
                        .values("id")[:1]
                    ).values("id")
                )
            )
            .select_related("fornitore")
            .order_by("fornitore__ragione_sociale")
        )

        return queryset


class DurcCreateView(LoginRequiredMixin, CreateView):
    model = Durc
    form_class = DurcForm
    template_name = "documenti/durc_form.html"
    success_url = reverse_lazy("documenti:durc_list")

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class DurcUpdateView(LoginRequiredMixin, UpdateView):
    model = Durc
    form_class = DurcForm
    template_name = "documenti/durc_form.html"
    success_url = reverse_lazy("documenti:durc_list")


class DurcDeleteView(LoginRequiredMixin, DeleteView):
    model = Durc
    template_name = "documenti/durc_confirm_delete.html"
    success_url = reverse_lazy("documenti:durc_list")


class ReportPlafondView_old(TemplateView):
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
