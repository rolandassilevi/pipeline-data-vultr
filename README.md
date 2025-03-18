# Pipeline Data Vultr

## **1️⃣ Architecture du Pipeline**
Le pipeline de données suit l’architecture suivante :

```
MySQL (Source) → DBT (Transformation) → Vertica (Stockage Analytique) → Metabase (Visualisation)
```

```
GitHub (Code & CI/CD) → Vultr (Ubuntu) → Docker Compose (Services) → Airflow (Orchestration)
```


### **🔹 Description des composants**
- **GitHub** : Contient le code source et gère l’intégration et le déploiement continu (CI/CD) avec GitHub Actions.
- **Vultr (Ubuntu)** : Héberge les services Docker pour exécuter l’ensemble du pipeline.
- **Docker Compose** : Gère le déploiement des services (MySQL, DBT, Vertica, Metabase, Airflow).
- **Airflow** : Orchestration des tâches ETL (extraction, transformation, chargement des données).
- **MySQL** : Source des données brutes.
- **DBT (Data Build Tool)** : Transformation et modélisation des données.
- **Vertica** : Stockage analytique des données transformées.
- **Metabase** : Visualisation des données stockées dans Vertica.

---

## **2️⃣ Stack Technologique**
| Technologie | Rôle |
|------------|------|
| **GitHub Actions** | CI/CD pour déploiement automatique |
| **Docker & Docker Compose** | Conteneurisation et orchestration des services |
| **MySQL** | Base de données transactionnelle (source) |
| **DBT** | Transformation et modélisation des données |
| **Vertica** | Stockage analytique (Data Warehouse) |
| **Metabase** | Visualisation et exploration des données |
| **Apache Airflow** | Orchestration des tâches ETL |

---

## **3️⃣ Arborescence du Projet**

```
pipeline-data-vultr/
│── dags/                          # DAGs pour Airflow (orchestration)
│   ├── mysql_to_vertica.py        # DAG orchestrant l'ETL
│── dbt_project/                   # Projet DBT (modélisation SQL)
│   ├── profiles.yml               # Configuration DBT pour Vertica
│   ├── models/                    # Modèles SQL pour la transformation
│── scripts/                       # Scripts Python pour ingestion
│   ├── transfer_data.py           # Script de transfert MySQL → Vertica
│── .github/workflows/             # CI/CD GitHub Actions (déploiement auto)
│   ├── deploy.yml                 # Pipeline CI/CD pour Vultr
│── docker-compose.yml             # Déploiement multi-services avec Docker
│── README.md                      # Documentation du projet
```

---

## **4️⃣ Description des Composants du Projet**

### **📌 1. `docker-compose.yml`**
Définit et orchestre les services du pipeline :
- **MySQL** : Stocke les données brutes.
- **Vertica** : Stocke les données transformées.
- **DBT** : Transforme les données avant stockage.
- **Metabase** : Visualisation des données.
- **Airflow** : Orchestration ETL.
- **Transfer** : Extrait, transforme et charge les données.

### **📌 2. `scripts/transfer_data.py`**
- **Extrait** les données de MySQL.
- **Transforme** les données avec DBT.
- **Charge** les données transformées dans Vertica.

### **📌 3. `dags/mysql_to_vertica.py`**
- Automatisation avec **Apache Airflow**.
- Exécute le script de transformation et chargement **chaque jour**.

### **📌 4. `.github/workflows/deploy.yml`**
- Déploiement **automatique** du pipeline sur **Vultr** après chaque `git push`.
- Connexion SSH sécurisée avec un **secret GitHub** (`VULTR_SSH_KEY`).

---

## **5️⃣ Déploiement du Projet**
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

### **🔹 4. Accéder aux Services**
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



