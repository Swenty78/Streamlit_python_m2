import pandas as pd
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import time

# Charger le fichier avec encodage correct
df = pd.read_csv("fichier_nettoye.csv", encoding="utf-8")

# Nettoyer les lignes où l'adresse est vide ou invalide
df = df.dropna(subset=["adresse"])
df["adresse"] = df["adresse"].astype(str).str.strip()

# Initialiser Nominatim avec un user-agent personnalisé
geolocator = Nominatim(user_agent="my_cowork_geocoder")

# Fonction robuste de récupération des coordonnées
def get_coordinates(adresse, retries=3):
    try:
        location = geolocator.geocode(adresse)
        if location:
            return location.latitude, location.longitude
        else:
            return None, None
    except GeocoderTimedOut:
        if retries > 0:
            time.sleep(1)
            return get_coordinates(adresse, retries - 1)
        return None, None
    except Exception:
        return None, None

# Appliquer le géocodage ligne par ligne avec respect du quota
latitudes = []
longitudes = []

print("Début du géocodage...")

for adresse in df["adresse"]:
    lat, lon = get_coordinates(adresse)
    latitudes.append(lat)
    longitudes.append(lon)
    time.sleep(1)  # Respect de la limite de Nominatim

# Ajouter les colonnes de coordonnées
df["latitude"] = latitudes
df["longitude"] = longitudes

# Sauvegarder dans un nouveau fichier
df.to_csv("fichier_geocode.csv", index=False, encoding="utf-8")

print("✅ Géocodage terminé. Résultats enregistrés dans 'fichier_geocode.csv'.")