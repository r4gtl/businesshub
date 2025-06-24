#!/bin/bash
set -e

DEST_DIR="/opt/jasperreports/lib"
mkdir -p "$DEST_DIR"

download_if_missing() {
  local url="$1"
  local filename=$(basename "$url")
  local filepath="$DEST_DIR/$filename"

  if [ -f "$filepath" ]; then
    echo "[✔] $filename già presente, salto download."
  else
    echo "[↓] Scarico $filename..."
    wget -q "$url" -O "$filepath"
  fi
}

echo "🔍 Controllo JAR JasperReports..."

JAR_URLS=(
    "https://repo1.maven.org/maven2/net/sf/jasperreports/jasperreports/7.0.2/jasperreports-7.0.2.jar"
    "https://repo1.maven.org/maven2/org/apache/commons/commons-lang3/3.12.0/commons-lang3-3.12.0.jar"
    "https://repo1.maven.org/maven2/org/apache/commons/commons-collections4/4.4/commons-collections4-4.4.jar"
    "https://repo1.maven.org/maven2/org/jfree/jfreechart/1.5.3/jfreechart-1.5.3.jar"
    "https://repo1.maven.org/maven2/org/jfree/jcommon/1.0.23/jcommon-1.0.23.jar"
    "https://repo1.maven.org/maven2/com/itextpdf/kernel/7.1.16/kernel-7.1.16.jar"
    "https://repo1.maven.org/maven2/com/itextpdf/io/7.1.16/io-7.1.16.jar"
    "https://repo1.maven.org/maven2/com/itextpdf/layout/7.1.16/layout-7.1.16.jar"
    "https://repo1.maven.org/maven2/com/itextpdf/forms/7.1.16/forms-7.1.16.jar"
    "https://repo1.maven.org/maven2/com/itextpdf/pdfa/7.1.16/pdfa-7.1.16.jar"
    "https://repo1.maven.org/maven2/com/itextpdf/sign/7.1.16/sign-7.1.16.jar"
    "https://repo1.maven.org/maven2/com/itextpdf/barcodes/7.1.16/barcodes-7.1.16.jar"
    "https://repo1.maven.org/maven2/org/eclipse/jdt/ecj/3.21.0/ecj-3.21.0.jar"
    "https://repo1.maven.org/maven2/commons-digester/commons-digester/2.1/commons-digester-2.1.jar"
    "https://repo1.maven.org/maven2/commons-beanutils/commons-beanutils/1.9.4/commons-beanutils-1.9.4.jar"
    "https://repo1.maven.org/maven2/commons-logging/commons-logging/1.2/commons-logging-1.2.jar"
    "https://repo1.maven.org/maven2/commons-collections/commons-collections/3.2.2/commons-collections-3.2.2.jar"
    "https://repo1.maven.org/maven2/org/slf4j/slf4j-api/1.7.30/slf4j-api-1.7.30.jar"
    "https://repo1.maven.org/maven2/org/slf4j/slf4j-simple/1.7.30/slf4j-simple-1.7.30.jar"
    "https://repo1.maven.org/maven2/net/sf/jasperreports/jasperreports-pdf/7.0.2/jasperreports-pdf-7.0.2.jar"
    "https://repo1.maven.org/maven2/com/itextpdf/commons/7.2.0/commons-7.2.0.jar"
    "https://repo1.maven.org/maven2/com/github/librepdf/openpdf/1.3.30/openpdf-1.3.30.jar"
    "https://jdbc.postgresql.org/download/postgresql-42.5.0.jar"
)

for url in "${JAR_URLS[@]}"; do
  download_if_missing "$url"
done

echo "✅ Tutti i JAR necessari sono pronti."
