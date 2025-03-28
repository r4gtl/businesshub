from accounts.models import Azienda


def azienda_and_user(request):
    # Ottieni l'azienda associata all'utente attivo
    azienda = request.user.azienda if request.user.is_authenticated else None
    return {
        "azienda": azienda,
        "user": request.user,
    }
