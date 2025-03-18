import mysql.connector

# Connexion à la base de données MySQL
conn = mysql.connector.connect(
    host="mysql",  # Nom du service MySQL défini dans docker-compose
    user="user",
    password="password",
    database="mydb"
)
cursor = conn.cursor()

# Création de la table pour stocker les données du fichier CSV
create_table_query = """
CREATE TABLE IF NOT EXISTS inverter_data (
    TIMESTAMP DATETIME,
    DATE DATE,
    ANNEE INT,
    MOIS INT,
    JOUR INT,
    HEURE TIME,
    PV1 FLOAT,
    PV2 FLOAT,
    PV3 FLOAT,
    PV4 FLOAT,
    PV5 FLOAT,
    PV6 FLOAT,
    PV7 FLOAT,
    PV8 FLOAT,
    PV9 FLOAT,
    PV10 FLOAT,
    MPPT1A FLOAT,
    MPPT2A FLOAT,
    MPPT3A FLOAT,
    MPPT4A FLOAT,
    MPPT5A FLOAT,
    MPPT1V FLOAT,
    MPPT2V FLOAT,
    MPPT3V FLOAT,
    MPPT4V FLOAT,
    MPPT5V FLOAT,
    PHASE_A_CURRENT FLOAT,
    PHASE_B_CURRENT FLOAT,
    PHASE_C_CURRENT FLOAT,
    PHASE_A_VOLTAGE FLOAT,
    PHASE_B_VOLTAGE FLOAT,
    PHASE_C_VOLTAGE FLOAT,
    TOTAL_DC_POWER FLOAT,
    TOTAL_ACTIVE_POWER FLOAT,
    DAILY_YIELD FLOAT,
    TOTAL_YIELD FLOAT
);
"""

cursor.execute(create_table_query)
conn.commit()

print("✅ Table `inverter_data` créée avec succès !")

# Fermeture de la connexion
cursor.close()
conn.close()
