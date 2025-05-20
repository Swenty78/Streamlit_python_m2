import streamlit as st
import folium
from streamlit_folium import folium_static
import pandas as pd
import re
from folium.plugins import MarkerCluster

# --- CONFIGURATION GÉNÉRALE ---
st.set_page_config(
    page_title="Coworking Map - Île-de-France",
    layout="wide",
    page_icon="📍"
)

# --- CHARGEMENT DU FICHIER CSV ---
@st.cache_data
def load_data():
    return pd.read_csv("fichier_nettoye_geo.csv", sep=None, engine="python", encoding="utf-8")

data = load_data()


# --- BARRE DE RECHERCHE ---
st.subheader("🔎 Recherche")
search_query = st.text_input("Rechercher par nom ou adresse :", "")

# Appliquer le filtre si une recherche est faite
if search_query:
    search_query_lower = search_query.lower()
    data = data[
        data["nom"].str.lower().str.contains(search_query_lower) |
        data["adresse"].str.lower().str.contains(search_query_lower)
    ]
    st.success(f"{len(data)} résultats trouvés pour : '{search_query}'")

# --- FONCTIONS UTILITAIRES ---
def extraire_arrondissement(adresse):
    match = re.search(r'75(\d{3})', adresse)
    return match.group(0) if match else "Autre"

def google_maps_link(row):
    return f"https://www.google.com/maps/search/?api=1&query={row['latitude']},{row['longitude']}"

# --- ENRICHISSEMENT DES DONNÉES ---
data["arrondissement"] = data["adresse"].apply(extraire_arrondissement)
data["Google Maps"] = data.apply(google_maps_link, axis=1)

# --- EN-TÊTE ---
st.title("📍 Carte interactive des espaces de coworking en Île-de-France")
st.markdown("Explorez visuellement les espaces de coworking disponibles avec carte, stats et infos clés.")



# --- CARTE FOLIUM ---
st.subheader("🗺️ Localisation des coworkings")

m = folium.Map(location=[48.8566, 2.3522], zoom_start=12)
cluster = MarkerCluster().add_to(m)

for _, row in data.dropna(subset=["latitude", "longitude"]).iterrows():
    popup_html = f"""
    <strong>{row['nom']}</strong><br>
    {row['adresse']}<br>
    <a href="{row['Site']}" target="_blank">Site Web</a>
    """
    folium.Marker(
        location=[row["latitude"], row["longitude"]],
        popup=popup_html,
        tooltip=row["nom"]
    ).add_to(cluster)

folium_static(m, width=1000, height=600)

st.markdown("---")

# --- INSIGHTS / STATS ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("🏙️ Répartition par arrondissement")
    arr_counts = data["arrondissement"].value_counts()
    st.bar_chart(arr_counts)

with col2:
    st.subheader("🌐 Présence numérique")
    instagram_pct = (data["Instagram"].notna() & (data["Instagram"] != "NULL")).mean() * 100
    site_pct = (data["Site"].notna() & (data["Site"] != "NULL")).mean() * 100
    st.metric("📸 Instagram", f"{instagram_pct:.1f} %")
    st.metric("🌍 Site Web", f"{site_pct:.1f} %")

st.markdown("---")

# --- LISTE DES COWORKINGS ---
st.subheader("📋 Liste des espaces de coworking")

with st.expander("Afficher la liste complète avec liens"):
    for _, row in data.iterrows():
        if pd.notnull(row["latitude"]) and pd.notnull(row["longitude"]):
            st.markdown(
                f"➡️ **[{row['nom']}]({row['Site']})** - {row['adresse']} "
                f"[🗺️ Carte]({row['Google Maps']})"
            )
