import mysql.connector
import vertica_python
import os

# Connexion à MySQL
mysql_conn = mysql.connector.connect(
    host="mysql", user="user", password="password", database="mydb"
)
mysql_cursor = mysql_conn.cursor()
mysql_cursor.execute("SELECT * FROM ventes")

# Stockage temporaire des données extraites
extracted_data = mysql_cursor.fetchall()

# Stockage local pour DBT
with open('/usr/app/dbt_project/raw_data.csv', 'w') as f:
    f.write("id,produit,prix,quantite,date_vente\n")
    for row in extracted_data:
        f.write(",".join(map(str, row)) + "\n")

print("✅ Extraction de MySQL terminée. Lancement de DBT...")

# Exécuter DBT pour transformer les données
os.system("docker exec -it dbt dbt run --project-dir /usr/app")

# Connexion à Vertica
vertica_conn = vertica_python.connect({
    'host': 'vertica', 'user': 'dbadmin', 'password': 'password',
    'database': 'mywarehouse', 'port': 5433
})
vertica_cursor = vertica_conn.cursor()

# Charger les données transformées dans Vertica
with open('/usr/app/dbt_project/transformed_data.csv', 'r') as f:
    next(f)  # Ignorer l'en-tête
    for line in f:
        values = line.strip().split(',')
        vertica_cursor.execute(
            "INSERT INTO ventes_analytiques VALUES (%s, %s, %s, %s, %s)", values
        )

print("✅ Chargement dans Vertica terminé.")

# Fermeture des connexions
mysql_conn.close()
vertica_conn.close()
