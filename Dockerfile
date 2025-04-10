FROM openjdk:11-jdk-slim

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
    

# Pip deps
COPY requirements.txt .
RUN pip3 install --upgrade pip && pip3 install -r requirements.txt

# Copy project
COPY . .

# Copy jreports
COPY jreports /code/jreports

# Create Jasper folder
RUN mkdir -p /opt/jasperreports/lib

# Scarica JAR necessari
RUN wget https://repo1.maven.org/maven2/net/sf/jasperreports/jasperreports/7.0.2/jasperreports-7.0.2.jar -P /opt/jasperreports/lib/ && \
    wget https://repo1.maven.org/maven2/org/apache/commons/commons-lang3/3.12.0/commons-lang3-3.12.0.jar -P /opt/jasperreports/lib/ && \
    wget https://repo1.maven.org/maven2/org/apache/commons/commons-collections4/4.4/commons-collections4-4.4.jar -P /opt/jasperreports/lib/ && \
    wget https://repo1.maven.org/maven2/org/jfree/jfreechart/1.5.3/jfreechart-1.5.3.jar -P /opt/jasperreports/lib/ && \
    wget https://repo1.maven.org/maven2/org/jfree/jcommon/1.0.23/jcommon-1.0.23.jar -P /opt/jasperreports/lib/ && \
    wget https://repo1.maven.org/maven2/com/itextpdf/kernel/7.1.16/kernel-7.1.16.jar -P /opt/jasperreports/lib/ && \
    wget https://repo1.maven.org/maven2/com/itextpdf/io/7.1.16/io-7.1.16.jar -P /opt/jasperreports/lib/ && \
    wget https://repo1.maven.org/maven2/com/itextpdf/layout/7.1.16/layout-7.1.16.jar -P /opt/jasperreports/lib/ && \
    wget https://repo1.maven.org/maven2/com/itextpdf/forms/7.1.16/forms-7.1.16.jar -P /opt/jasperreports/lib/ && \
    wget https://repo1.maven.org/maven2/com/itextpdf/pdfa/7.1.16/pdfa-7.1.16.jar -P /opt/jasperreports/lib/ && \
    wget https://repo1.maven.org/maven2/com/itextpdf/sign/7.1.16/sign-7.1.16.jar -P /opt/jasperreports/lib/ && \
    wget https://repo1.maven.org/maven2/com/itextpdf/barcodes/7.1.16/barcodes-7.1.16.jar -P /opt/jasperreports/lib/ && \
    wget https://repo1.maven.org/maven2/org/eclipse/jdt/ecj/3.21.0/ecj-3.21.0.jar -P /opt/jasperreports/lib/ && \
    wget https://repo1.maven.org/maven2/commons-digester/commons-digester/2.1/commons-digester-2.1.jar -P /opt/jasperreports/lib/ && \
    wget https://repo1.maven.org/maven2/commons-beanutils/commons-beanutils/1.9.4/commons-beanutils-1.9.4.jar -P /opt/jasperreports/lib/ && \
    wget https://repo1.maven.org/maven2/commons-logging/commons-logging/1.2/commons-logging-1.2.jar -P /opt/jasperreports/lib/ && \
    wget https://repo1.maven.org/maven2/commons-collections/commons-collections/3.2.2/commons-collections-3.2.2.jar -P /opt/jasperreports/lib/ && \
    wget https://repo1.maven.org/maven2/org/slf4j/slf4j-api/1.7.30/slf4j-api-1.7.30.jar -P /opt/jasperreports/lib/ && \
    wget https://repo1.maven.org/maven2/org/slf4j/slf4j-simple/1.7.30/slf4j-simple-1.7.30.jar -P /opt/jasperreports/lib/ && \
    wget https://repo1.maven.org/maven2/net/sf/jasperreports/jasperreports-pdf/7.0.2/jasperreports-pdf-7.0.2.jar -P /opt/jasperreports/lib/ && \
    wget https://repo1.maven.org/maven2/com/itextpdf/commons/7.2.0/commons-7.2.0.jar -P /opt/jasperreports/lib/ && \
    wget https://repo1.maven.org/maven2/com/github/librepdf/openpdf/1.3.30/openpdf-1.3.30.jar -P /opt/jasperreports/lib/

# PostgreSQL JDBC driver
RUN wget https://jdbc.postgresql.org/download/postgresql-42.5.0.jar -O /opt/jasperreports/lib/postgresql-42.5.0.jar

# ReportGenerator.java
COPY ReportGenerator.java /opt/jasperreports/

# Compila il ReportGenerator
RUN cd /opt/jasperreports && \
    javac -cp "lib/*" ReportGenerator.java && \
    mkdir -p classes && \
    mv ReportGenerator.class classes/

# Entrypoint
RUN chmod +x /code/entrypoint.sh
ENTRYPOINT ["/bin/sh", "/code/entrypoint.sh"]
