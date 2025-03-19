import mysql.connector
import csv
from datetime import datetime

# Connexion à la base de données MySQL
conn = mysql.connector.connect(
    host="mysql",  # Nom du service MySQL défini dans docker-compose
    user="user",
    password="password",
    database="mydb"
)
cursor = conn.cursor()

# Chemin du fichier CSV
csv_file = "/data/inverter.csv"

# Définition de la requête d'insertion
insert_query = """
INSERT INTO inverter_data (
    TIMESTAMP, DATE, ANNEE, MOIS, JOUR, HEURE, PV1, PV2, PV3, PV4, PV5, PV6, PV7, PV8, PV9, PV10,
    MPPT1A, MPPT2A, MPPT3A, MPPT4A, MPPT5A, MPPT1V, MPPT2V, MPPT3V, MPPT4V, MPPT5V,
    PHASE_A_CURRENT, PHASE_B_CURRENT, PHASE_C_CURRENT, PHASE_A_VOLTAGE, PHASE_B_VOLTAGE, PHASE_C_VOLTAGE,
    TOTAL_DC_POWER, TOTAL_ACTIVE_POWER, DAILY_YIELD, TOTAL_YIELD
) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

# Fonction de conversion du format de date

def is_valid_datetime(value, format):
    try:
        datetime.strptime(value, format)
        return True
    except ValueError:
        return False

def convert_datetime(value):
    if is_valid_datetime(value, "%d/%m/%Y %H:%M"):
        return datetime.strptime(value, "%d/%m/%Y %H:%M").strftime("%Y-%m-%d %H:%M:%S")
    print(f"⚠️ Ignoré : TIMESTAMP invalide -> {value}")
    return None

def convert_date(value):
    if is_valid_datetime(value, "%d/%m/%Y"):
        return datetime.strptime(value, "%d/%m/%Y").strftime("%Y-%m-%d")
    print(f"⚠️ Ignoré : DATE invalide -> {value}")
    return None

def convert_time(value):
    if is_valid_datetime(value, "%H:%M"):
        return datetime.strptime(value, "%H:%M").strftime("%H:%M:%S")
    print(f"⚠️ Ignoré : HEURE invalide -> {value}")
    return None

# Lecture et insertion des données du fichier CSV
with open(csv_file, newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')  # Délimiteur virgule
    next(reader)  # Ignorer l'en-tête
    for row in reader:
        row[0] = convert_datetime(row[0]) if row[0] else None  # TIMESTAMP
        row[1] = convert_date(row[1]) if row[1] else None  # DATE
        row[5] = convert_time(row[5]) if row[5] else None  # HEURE
        
        # Vérification des valeurs converties
        if None in (row[0], row[1], row[5]):
            print(f"⚠️ Enregistrement ignoré en raison de dates invalides: {row}")
            continue
        
        try:
            row = [float(x) if x.replace('.', '', 1).isdigit() else None for x in row]  # Convertir les nombres
            cursor.execute(insert_query, row)
        except Exception as e:
            print(f"❌ Erreur lors de l'insertion de la ligne {row}: {e}")

# Valider les insertions et fermer la connexion
conn.commit()
cursor.close()
conn.close()

print("✅ Données du fichier CSV insérées avec succès dans MySQL !")

