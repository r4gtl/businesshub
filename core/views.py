from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from documenti.models import FatturaFornitore, DichiarazioneIntento


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "core/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["ultime_fatture"] = FatturaFornitore.objects.select_related(
            "fornitore"
        ).order_by("-data_fattura")[:5]

        # Aggiungiamo questo nel get_context_data
        context["plafond_alert"] = []

        dichiarazioni = DichiarazioneIntento.objects.select_related("fornitore")

        for dichiarazione in dichiarazioni:
            totale_fatture = (
                dichiarazione.fornitore.fatturefornitore_set.filter(
                    data_fattura__year=dichiarazione.anno_riferimento
                ).aggregate(Sum("importo"))["importo__sum"]
                or 0
            )

            if (
                totale_fatture > 0
                and (dichiarazione.plafond - totale_fatture) / dichiarazione.plafond
                < 0.1
            ):
                context["plafond_alert"].append(
                    {
                        "fornitore": dichiarazione.fornitore.ragione_sociale,
                        "plafond": dichiarazione.plafond,
                        "usato": totale_fatture,
                        "rimanente": dichiarazione.plafond - totale_fatture,
                    }
                )
        return context
