import psycopg2

conn = psycopg2.connect(
    host="localhost",
    port="5432",
    database="businesshub_db",
    user="postgres",
    password="stefanopostgresql"
)
cursor = conn.cursor()
cursor.execute("SELECT 1")
print("Connessione riuscita!")
conn.close()