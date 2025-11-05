# FROM openjdk:11-jdk-slim
FROM eclipse-temurin:11-jdk


ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /code

# Install system deps
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    python3 python3-pip python3-dev netcat-openbsd wget build-essential \
    libffi-dev libpango1.0-0 libpangocairo-1.0-0 libcairo2 libjpeg-dev \
    zlib1g-dev libxml2 libxslt1.1 libgdk-pixbuf2.0-0 unzip postgresql-client && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Install pip deps
COPY requirements.txt .
RUN pip3 install --upgrade pip && pip3 install -r requirements.txt

# Copia codice sorgente Django
COPY . .

# Jasper: crea dir e copia script
RUN mkdir -p /opt/jasperreports/lib
COPY scripts/scarica_jars.sh /opt/jasperreports/scarica_jars.sh

# Scarica JAR se mancanti
RUN chmod +x /opt/jasperreports/scarica_jars.sh && \
    /opt/jasperreports/scarica_jars.sh

# PostgreSQL JDBC driver è incluso nel download

# Copia ReportGenerator e compila
COPY ReportGenerator.java /opt/jasperreports/
RUN cd /opt/jasperreports && \
    javac -cp "lib/*" ReportGenerator.java && \
    mkdir -p classes && mv ReportGenerator.class classes/

# Entrypoint
RUN chmod +x /code/entrypoint.sh
ENTRYPOINT ["/bin/sh", "/code/entrypoint.sh"]
