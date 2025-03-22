# Conception et implémentation d'un Pipeline Data sur Vultr
Ceci est un exemple de Pipeline Data qui tourne sur un Serveur Ubuntu 24.04 LTS x64 dans le cloud Vultr

## **1️⃣ Architecture du Pipeline**

### **🔹 Description des composants**
- **GitHub** : Contient le code source et gère l’intégration et le déploiement continu (CI/CD) avec GitHub Actions.
- **Vultr (Ubuntu)** : Héberge les services Docker pour exécuter l’ensemble du pipeline.
- **Docker Compose** : Gère le déploiement des services (MySQL, DBT, Vertica, Metabase, Airflow).
- **Airflow** : Orchestration des tâches ETL (extraction, transformation, chargement des données).
- **CSV** : Fichier source contenant les données brutes.
- **MySQL** : Stockage temporaire des données avant transformation.
- **DBT (Data Build Tool)** : Transformation et modélisation des données.
- **Vertica** : Stockage analytique des données transformées.
- **Metabase** : Visualisation des données stockées dans Vertica.


Le pipeline de données suit l’architecture suivante :


```

GitHub (Code & CI/CD) → Vultr (Ubuntu) → Docker Compose (Services) → Airflow (Orchestration)

CSV (Source) → MySQL (Stockage temporaire) → DBT (Transformation) → Vertica (Stockage Analytique) → Metabase (Visualisation)

```

### Schéma du Pipeline

```
                ┌────────────────────┐
                │      GitHub        │
                │  (CI/CD & Code)    │
                └────────────────────┘
                         │
                         ▼
                ┌────────────────────┐
                │      Vultr         │
                │  (Ubuntu Server)   │
                └────────────────────┘
                         │
                         ▼
                ┌────────────────────┐
                │   Docker Compose   │
                │  (Services Multi)  │
                └────────────────────┘
                         │
                         ▼
        ┌────────────────────────────────────┐
        │            Airflow                 │
        │       (Orchestration)              │
        └────────────────────────────────────┘
                         │
                         ▼
                ┌────────────────────┐
                │      MySQL         │
                │  (Stockage Source) │
                └────────────────────┘
                         │
                         ▼
                ┌─────────────────────┐
                │        DBT          │
                │  (Modélisation SQL) │
                └─────────────────────┘
                         │
                         ▼
                ┌───────────────────────┐
                │      Vertica          │
                │ (Stockage Analytique) │
                └───────────────────────┘
                         │
                         ▼
                ┌────────────────────┐
                │      Metabase      │
                │  (Visualisation)   │
                └────────────────────┘

```


---

## **2️⃣ Stack Technologique**
| Technologie | Rôle |
|------------|------|
| **GitHub Actions** | CI/CD pour déploiement automatique |
| **Docker & Docker Compose** | Conteneurisation et orchestration des services |
| **CSV** | Source des données brutes |
| **MySQL** | Stockage intermédiaire des données |
| **DBT** | Transformation et modélisation des données |
| **Vertica** | Stockage analytique (Data Warehouse) |
| **Metabase** | Visualisation et exploration des données |
| **Apache Airflow** | Orchestration des tâches ETL |

---

## **3️⃣ Arborescence du Projet**

```
pipeline-data-vultr/
│── dags/                               # DAGs pour Airflow (orchestration)
│   ├── csv_to_mysql.py                 # DAG orchestrant l'ingestion CSV → MySQL
│   ├── mysql_to_vertica.py             # DAG orchestrant l'ETL MySQL → Vertica
│── dbt_project/                        # Projet DBT (modélisation SQL)
│   ├── profiles.yml                    # Configuration DBT pour Vertica
│   ├── dbt_project.yml                 # Paramètres du projet DBT
│   ├── logs/                           # Logs d'exécution de DBT
│   │   ├── dbt.log                     # Fichier de log DBT
│   ├── models/                         # Modèles SQL pour la transformation
│   │   ├── marts/                      # Contient les tables de faits
│   │   │   ├── fact_inverter_data.sql  # Table de faits principale
│   │   ├── staging/                    # Contient les tables de staging
│   │   │   ├── stg_inverter_data.sql   # Table staging des données 
│── scripts/                            # Scripts Python pour ingestion et transfert
│   ├── create_mysql_table.py           # Script de création de table dans MySQL
│   ├── load_csv_to_mysql.py            # Script de chargement CSV → MySQL
│   ├── transfer_data.py                # Script de transfert MySQL → Vertica
│── data/                               # Dossier contenant les fichiers CSV
│   ├── inverter.csv                    # Fichier CSV contenant les données des onduleurs
│── db_driver/                          # Drivers de Base de données pour Metabase
│   ├── vertica-jdbc-24.1.0-0.jar       # Vertica JDBC Driver
│── .github/workflows/                  # CI/CD GitHub Actions (déploiement auto)
│   ├── deploy.yml                      # Pipeline CI/CD pour Vultr
│── docker-compose.yml                  # Déploiement multi-services avec Docker
│── README.md                           # Documentation du projet
```

---

## **4️⃣ Description des Composants du Projet**

### 1. `docker-compose.yml`
Définit et orchestre les services du pipeline :
- **CSV** : Source des données.
- **MySQL** : Stocke temporairement les données brutes.
- **Vertica** : Stocke les données transformées.
- **DBT** : Transforme les données avant stockage.
- **Metabase** : Visualisation des données.
- **Airflow** : Orchestration ETL.
- **Transfer** : Extrait, transforme et charge les données.

Services Déployés

|Service	    | Image	                            |Rôle                               |
|---------------|-----------------------------------|-----------------------------------|
|MySQL	        |mysql:latest	                    |Base de données source             |
|Vertica	    |vertica/vertica-ce	                |Stockage analytique                |
|Metabase	    |metabase/metabase	                |Visualisation des données          |
|DBT	        |ghcr.io/dbt-labs/dbt-core:1.5.0	|Modélisation et transformation SQL |
|Airflow	    |puckel/docker-airflow	            |Orchestration des pipelines        |
|Python (ETL)	|python:3.9	                        |Scripts pour ingestion et transfert|

### 2. `scripts/load_csv_to_mysql.py`
- **Charge** les données depuis le fichier `inverter.csv` vers MySQL.

### 3. `scripts/transfer_data.py`
- **Extrait** les données de MySQL.
- **Transforme** les données avec DBT.
- **Charge** les données transformées dans Vertica.

### 4. `dags/csv_to_mysql.py`
- Automatisation avec **Apache Airflow**.
- Charge les fichiers CSV vers MySQL automatiquement.

### 5. `dags/mysql_to_vertica.py`
- Orchestration de la transformation et du chargement des données avec DBT et Vertica.

### 6. `.github/workflows/deploy.yml`
- Déploiement **automatique** du pipeline sur **Vultr** après chaque `git push`.
- Connexion SSH sécurisée avec un **secret GitHub** (`VULTR_SSH_KEY`).

---

## **5️⃣ Déploiement du Projet**
### **🔹 0. Assurez-vous d'avoir Docker et Docker Compose installés sur votre serveur Vultr :**
```bash
sudo apt update && sudo apt install -y docker docker-compose
```

### **🔹 1. Cloner le Projet sur Vultr**
```bash
git clone https://github.com/ton_username/pipeline-data-vultr.git
cd pipeline-data-vultr
```

### **🔹 2. Lancer Docker Compose**
```bash
docker-compose up -d
```

### **🔹 3. Vérifier les Conteneurs**
```bash
docker ps
```

### **🔹 4. Effectuer les tests et vérification**
- Tester le Fonctionnement
Vérifier MySQL

```bash
docker exec -it mysql mysql -u user -p -D mydb -e "SHOW TABLES;"
```

Vérifier Vertica
```bash
docker exec -it vertica /opt/vertica/bin/vsql -U dbadmin -d VMart -c "SELECT COUNT(*) FROM inverter_data;"
```

Vérifier DBT
```bash
docker exec -it dbt dbt debug
docker exec -it dbt dbt run
```

Vérifier Metabase
Accédez à Metabase via le navigateur
http://<VULTR_SERVER_IP>:3000/

Aller dans "Bases de données"
Ajouter une connexion Vertica
Tester avec cette requête :
```sql
SELECT * FROM inverter_data LIMIT 10;
```

- Automatisation avec GitHub Actions
Le pipeline CI/CD déploie automatiquement les services sur Vultr après chaque mise à jour.

Fichier CI/CD : .github/workflows/deploy.yml
Secrets GitHub à ajouter :
VULTR_SERVER_IP = xxx.xxx.xxx.xxx
VULTR_SSH_KEY = Clé SSH privée


### **🔹 5. Accéder aux Services**
| Service | URL / Commande |
|------------|--------------------|
| **Metabase** | `http://your_server_ip:3000` |
| **Airflow** | `http://your_server_ip:8080` |
| **MySQL** | `mysql -u user -p -h your_server_ip -D mydb` |
| **Vertica** | `/opt/vertica/bin/vsql -U dbadmin -d mywarehouse` |


---

## **6️⃣ Automatisation avec GitHub Actions**
Chaque **push sur `main`** déclenche **GitHub Actions** qui :
1. **Se connecte à Vultr via SSH**.
2. **Met à jour le code** avec `git pull`.
3. **Redémarre Docker Compose** pour appliquer les modifications.


## **Auteur : Roland ASSILEVI**
## **Mars 2025**

