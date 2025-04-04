FROM python:3.11-slim

# Variabili d'ambiente
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Impostazione della directory di lavoro
WORKDIR /code

# Installa Python e le dipendenze necessarie
RUN apt-get update && \
    apt-get install -y python3 python3-pip python3-dev netcat-openbsd wget build-essential \
    libffi-dev libpango1.0-0 libpangocairo-1.0-0 libcairo2 libjpeg-dev \
    zlib1g-dev libxml2 libxslt1.1 libgdk-pixbuf2.0-0

# Aggiorna pip e installa le dipendenze Python
RUN pip3 install --upgrade pip
COPY requirements.txt .
RUN pip3 install -r requirements.txt

# Copia il codice del progetto nel container
COPY . .

# Copia la cartella jreports contenente i file .jasper e .jrxml
COPY jreports /code/jreports

# Crea la cartella per i JAR di JasperReports e scarica il file JAR principale
RUN mkdir -p /opt/jasperreports/lib && \
    wget https://repo1.maven.org/maven2/net/sf/jasperreports/jasperreports/7.0.2/jasperreports-7.0.2.jar -P /opt/jasperreports/lib/

# Copia anche il tuo report .jasper o .jrxml se necessario
#COPY /path/to/your/report_template.jasper /opt/jasperreports/

# Imposta i permessi di esecuzione per entrypoint.sh
RUN chmod +x /code/entrypoint.sh

# Comando di avvio del container
ENTRYPOINT ["/bin/sh", "/code/entrypoint.sh"]
