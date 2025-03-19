import mysql.connector
import vertica_python

# Connexion à la base de données MySQL
mysql_conn = mysql.connector.connect(
    host="mysql",  # Nom du service MySQL défini dans docker-compose
    user="user",
    password="password",
    database="mydb"
)
mysql_cursor = mysql_conn.cursor()

# Connexion à la base de données Vertica
vertica_conn_info = {
    'host': "vertica",
    'port': 5433,
    'user': "dbadmin",
    'password': "password",
    'database': "VMart",
    'autocommit': True
}
vertica_conn = vertica_python.connect(**vertica_conn_info)
vertica_cursor = vertica_conn.cursor()

# Sélection des données de MySQL
mysql_cursor.execute("SELECT * FROM inverter_data")
rows = mysql_cursor.fetchall()
columns = [desc[0] for desc in mysql_cursor.description]

# Création de la table dans Vertica si elle n'existe pas
create_table_query = f"""
CREATE TABLE IF NOT EXISTS inverter_data (
    {', '.join(f'{col} VARCHAR(255)' for col in columns)}
);
"""
vertica_cursor.execute(create_table_query)

# Insertion des données dans Vertica
insert_query = f"""
INSERT INTO inverter_data ({', '.join(columns)})
VALUES ({', '.join(['%s'] * len(columns))})
"""

for row in rows:
    try:
        vertica_cursor.execute(insert_query, row)
    except Exception as e:
        print(f"❌ Erreur lors de l'insertion de la ligne {row}: {e}")

# Fermeture des connexions
mysql_cursor.close()
mysql_conn.close()
vertica_cursor.close()
vertica_conn.close()

print("✅ Données transférées de MySQL vers Vertica avec succès !")
