# Usa un'immagine base che include Java
FROM openjdk:11-jdk-slim

# Variabili d'ambiente
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Impostazione della directory di lavoro
WORKDIR /code

# Installa Python e le dipendenze necessarie
RUN apt-get update && \
    apt-get install -y python3 python3-pip python3-dev netcat-openbsd wget build-essential \
    libffi-dev libpango1.0-0 libpangocairo-1.0-0 libcairo2 libjpeg-dev \
    zlib1g-dev libxml2 libxslt1.1 libgdk-pixbuf2.0-0 unzip

# Aggiorna pip e installa le dipendenze Python
RUN pip3 install --upgrade pip
COPY requirements.txt .
RUN pip3 install -r requirements.txt

# Copia il codice del progetto nel container
COPY . .

# Copia la cartella jreports contenente i file .jasper e .jrxml
COPY jreports /code/jreports

# Crea la cartella per i JAR di JasperReports
RUN mkdir -p /opt/jasperreports/lib

# Scarica JasperReports 6.20.0 e le sue dipendenze
RUN wget https://repo1.maven.org/maven2/net/sf/jasperreports/jasperreports/6.20.0/jasperreports-6.20.0.jar -P /opt/jasperreports/lib/ && \
    wget https://repo1.maven.org/maven2/commons-digester/commons-digester/2.1/commons-digester-2.1.jar -P /opt/jasperreports/lib/ && \
    wget https://repo1.maven.org/maven2/org/apache/commons/commons-collections4/4.4/commons-collections4-4.4.jar -P /opt/jasperreports/lib/ && \
    wget https://repo1.maven.org/maven2/commons-beanutils/commons-beanutils/1.9.4/commons-beanutils-1.9.4.jar -P /opt/jasperreports/lib/ && \
    wget https://repo1.maven.org/maven2/commons-logging/commons-logging/1.2/commons-logging-1.2.jar -P /opt/jasperreports/lib/ && \
    wget https://repo1.maven.org/maven2/com/lowagie/itext/2.1.7/itext-2.1.7.jar -P /opt/jasperreports/lib/ && \
    wget https://repo1.maven.org/maven2/org/jfree/jcommon/1.0.23/jcommon-1.0.23.jar -P /opt/jasperreports/lib/ && \
    wget https://repo1.maven.org/maven2/org/jfree/jfreechart/1.0.19/jfreechart-1.0.19.jar -P /opt/jasperreports/lib/ && \
    wget https://repo1.maven.org/maven2/org/eclipse/jdt/ecj/3.21.0/ecj-3.21.0.jar -P /opt/jasperreports/lib/ && \
    wget https://repo1.maven.org/maven2/org/apache/commons/commons-lang3/3.9/commons-lang3-3.9.jar -P /opt/jasperreports/lib/

# Copia il file ReportGenerator.java semplificato
COPY ReportGenerator.java /opt/jasperreports/

# Compila il file ReportGenerator.java
RUN cd /opt/jasperreports && \
    javac -cp "lib/*" ReportGenerator.java && \
    mkdir -p classes && \
    mv ReportGenerator.class classes/

RUN wget https://jdbc.postgresql.org/download/postgresql-42.5.0.jar -O /opt/jasperreports/lib/postgresql-42.5.0.jar

# Imposta i permessi di esecuzione per entrypoint.sh
RUN chmod +x /code/entrypoint.sh

# Comando di avvio del container
ENTRYPOINT ["/bin/sh", "/code/entrypoint.sh"]