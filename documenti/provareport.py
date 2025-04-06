import subprocess
from django.http import HttpResponse
from django.conf import settings
import os
from documenti.models import DichiarazioneIntento


def genera_report(request, pk):
    # Paths
    report_path = "/code/jreports/DichIntento.jasper"
    output_path = "/code/jreports/output_report.pdf"

    # Get database credentials from environment variables
    db_host = os.environ.get("DB_HOST", "localhost")
    db_port = os.environ.get("DB_PORT", "5432")
    db_user = os.environ.get("POSTGRES_USER", "postgres")
    db_password = os.environ.get("POSTGRES_PASSWORD", "")
    db_name = os.environ.get("POSTGRES_DB", "postgres")

    # Create JDBC URL
    db_url = f"jdbc:postgresql://{db_host}:{db_port}/{db_name}"

    # Get the object to verify it exists
    dichiarazione = DichiarazioneIntento.objects.get(pk=pk)
    print(f"dichiarazione: {dichiarazione.data_dichiarazione}")
    print(f"Generating report with PK: {pk}")

    # Build Java command
    command = [
        "java",
        "-cp",
        "/opt/jasperreports/classes:/opt/jasperreports/lib/*",
        "ReportGenerator",
        report_path,
        output_path,
        db_url,
        db_user,
        db_password,
        f"PK={pk}",  # Pass PK parameter
    ]

    print(f"Executing command: {' '.join(command)}")

    # Execute Java command
    try:
        result = subprocess.run(
            command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        print(f"Output: {result.stdout.decode()}")
    except subprocess.CalledProcessError as e:
        error_message = e.stderr.decode() if e.stderr else str(e)
        print(f"Error: {error_message}")
        return HttpResponse(f"Error generating report: {error_message}", status=500)

    # Verify file exists
    if not os.path.exists(output_path):
        return HttpResponse("Generated PDF file not found", status=500)

    # Return PDF file
    with open(output_path, "rb") as pdf_file:
        pdf_data = pdf_file.read()
    return HttpResponse(pdf_data, content_type="application/pdf")


def genera_report_old(request, pk):
    # Percorso del template e del report
    report_path = "/code/jreports/DichIntento.jasper"
    output_path = "/code/jreports/output_report.pdf"
    dichiarazione = DichiarazioneIntento.objects.get(pk=pk)
    print(f"dichiarazione: {dichiarazione.data_dichiarazione}")
    print(f"Generating report with PK: {pk}")

    # Costruisci il comando Java usando il nostro programma ReportGenerator
    command = [
        "java",
        "-cp",
        "/opt/jasperreports/classes:/opt/jasperreports/lib/*",  # classpath con il nostro programma e le librerie
        "ReportGenerator",
        report_path,
        output_path,
        f"PK={pk}",  # Passa il parametro pk al report
    ]

    print(f"Executing command: {' '.join(command)}")

    # Esegui il comando Java per generare il report
    try:
        result = subprocess.run(
            command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        print(f"Output: {result.stdout.decode()}")
    except subprocess.CalledProcessError as e:
        error_message = e.stderr.decode() if e.stderr else str(e)
        print(f"Error: {error_message}")
        return HttpResponse(f"Error generating report: {error_message}", status=500)

    # Verifica che il file esista
    if not os.path.exists(output_path):
        return HttpResponse("Generated PDF file not found", status=500)

    # Leggi il file PDF generato e restituiscilo come risposta HTTP
    with open(output_path, "rb") as pdf_file:
        pdf_data = pdf_file.read()

    return HttpResponse(pdf_data, content_type="application/pdf")
