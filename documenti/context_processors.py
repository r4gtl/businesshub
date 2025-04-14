from .models import Durc
from django.utils.timezone import now
from django.db.models import OuterRef, Subquery


def durc_scaduti_notifica(request):
    if not request.user.is_authenticated:
        return {}

    today = now().date()

    # Prendi solo l'ultimo DURC per ogni fornitore
    ultimi_durc_ids = (
        Durc.objects.filter(fornitore=OuterRef("fornitore"))
        .order_by("-scadenza_durc")
        .values("id")[:1]
    )

    durc_scaduti = Durc.objects.filter(
        id__in=Subquery(ultimi_durc_ids), scadenza_durc__lt=today
    ).count()

    return {"durc_scaduti_count": durc_scaduti}
