
# 🗂️ Coworking Data Pipeline - Île-de-France

Ce projet permet de **scraper, nettoyer, géolocaliser et visualiser** les espaces de coworking en Île-de-France à partir du site source jusqu’à un fichier CSV final exploitable dans une application Streamlit.

---

## 📦 Prérequis

Avant d’exécuter ce pipeline, installe les dépendances nécessaires :

```bash
pip install -r requirements.txt
```

### 📁 Structure recommandée

```
.
├── extract.py                # Scraping initial du site source
├── data_cleaning.py         # Nettoyage du fichier brut
├── geo_location.py          # Ajout des coordonnées géographiques
├── data_cleaning_geo.py     # Nettoyage final et formatage
├── fichier_nettoye_geo.csv  # 🔥 Fichier final exploitable
├── app.py                   # Application Streamlit
└── README.md
```

---

## 🛠️ Étapes du traitement

### 1. 🔍 `extract.py`

> **But :** Scraper les données d'espaces de coworking (nom, adresse, etc.)

- Récupère les informations depuis un site web ou une API
- Génère un fichier brut `raw_data.csv` ou équivalent
- ⚠️ Peut nécessiter un `User-Agent` et un `time.sleep()` pour éviter les blocages

```bash
python extract.py
```

---

### 2. 🧼 `data_cleaning.py`

> **But :** Nettoyer les chaînes de caractères, les accents, les doublons, les espaces, etc.

- Normalise les textes (accents, majuscules/minuscules)
- Supprime ou remplace les valeurs manquantes
- Écrit un fichier propre `clean_data.csv`

```bash
python data_cleaning.py
```

---

### 3. 🌍 `geo_location.py`

> **But :** Ajouter les colonnes `latitude` et `longitude` via l'API `Nominatim` de `geopy`.

- Boucle sur chaque adresse
- Appelle l’API de géocodage pour remplir les coordonnées
- Ajoute deux nouvelles colonnes au CSV

```bash
python geo_location.py
```

**Remarques :**
- Nominatim impose une limite de **1 requête par seconde**
- En cas de timeouts, le script inclut une logique de retry

---

### 4. 🧽 `data_cleaning_geo.py`

> **But :** Nettoyage final, suppression des lignes incomplètes, réorganisation des colonnes

- Supprime les entrées sans géolocalisation
- Formate proprement les champs pour l'affichage
- Produit le fichier final : `fichier_nettoye_geo.csv`

```bash
python data_cleaning_geo.py
```

---

## ✅ Fichier final

> **📄 `fichier_nettoye_geo.csv`**

Ce fichier contient toutes les données prêtes à l'emploi, notamment :

- `nom`, `adresse`, `téléphone`, `Accès`, `Site`, `Instagram`
- `latitude`, `longitude` → obtenues par géocodage
- Utilisable directement dans l'application Streamlit `app.py`

---

## 🖥️ Utilisation dans Streamlit

```bash
streamlit run app.py
```

Cette application affiche :
- Une carte interactive Folium
- Des statistiques par arrondissement
- Une présence web (Instagram, site)
- Une liste des espaces de coworking

---

## 🔐 Bonnes pratiques

- Ne pas abuser de l'API de géocodage (limite de Nominatim)
- Conserver les CSV intermédiaires pour audit/debug
- Documenter les champs créés ou transformés dans chaque étape
- Ajouter des logs si les scripts doivent tourner en prod

---

## 📌 TODO possibles

- Ajouter un export GeoJSON pour intégration SIG
- Créer une base de données SQLite ou PostgreSQL pour requêtes complexes
- Rendre le scraping plus robuste avec `requests + BeautifulSoup` ou `Selenium`


---
## 🎯 Objectif

Ce projet a pour but de fournir un **exemple complet et concret de pipeline de traitement de données** intégrant :

- Le **scraping** d'informations depuis un site web,
- Le **nettoyage et la structuration** de la donnée avec `pandas`,
- L’**enrichissement par géocodage** des adresses via l’API `Nominatim` de `geopy`,
- Et la création d’une **mini-application web interactive** avec `Streamlit`.

Le tout est conçu pour démontrer comment transformer une **donnée brute non exploitable** en un **produit interactif visualisable** : carte interactive, statistiques dynamiques, filtres, liens Google Maps, etc.

Ce projet est idéal comme **cas d’usage pédagogique ou démonstratif** pour :

- L’analyse de données géographiques,
- L’automatisation de workflows de données,
- La création rapide de dashboard léger sans backend.

---

## 👨‍💻 Auteur

Projet réalisé par Capgras Noé, dans le cadre de cours de pyton de M2.
