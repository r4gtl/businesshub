import subprocess
from django.http import HttpResponse
from django.conf import settings
from django.shortcuts import get_object_or_404
from .models import DichiarazioneIntento

def genera_report(request, pk):
    # Ottieni l'istanza della dichiarazione dal database
    dichiarazione = get_object_or_404(DichiarazioneIntento, pk=pk)
    
    # Definisci il percorso del file .jasper (aggiungendo la cartella jreports)
    jasper_file = f"{settings.BASE_DIR}/jreports/DichIntento.jasper"
    
    # Definisci il file di output del report
    output_file = f"{settings.BASE_DIR}/jreports/output_report.pdf"
    
    # Definisci i parametri da passare al report
    params = {
        'PK': dichiarazione.pk,
        'numero_interno': dichiarazione.numero_interno,
        'numero_dichiarazione': dichiarazione.numero_dichiarazione,
        # Aggiungi altri parametri se necessario
    }

    # Comando per eseguire JasperReports usando il subprocess
    # Usa JasperReports in modalità batch tramite Java
    command = [
        'java', '-jar', '/opt/jasperreports/jasperreports-7.0.2/jasperreports-server.jar',
        jasper_file,  # percorso al file .jasper
        output_file,  # file di output, es. pdf
        str(params['PK'])  # Parametro da passare (in questo caso il pk)
    ]
    
    try:
        # Esegui il comando con i parametri
        subprocess.run(command, check=True)
        # Se il comando va a buon fine, restituisci il PDF come risposta HTTP
        with open(output_file, 'rb') as f:
            pdf = f.read()
        
        # Restituisci il PDF come risposta
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename=report_{params["PK"]}.pdf'
        return response
    except subprocess.CalledProcessError as e:
        # Gestisci l'errore nel caso in cui il comando fallisca
        return HttpResponse(f"Si è verificato un errore nel generare il report: {e}")


