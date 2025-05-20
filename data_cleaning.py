import pandas as pd
import re
import unicodedata

def nettoyage_csv(fichier):
    df = pd.read_csv(fichier)  # charger le fichier CSV
    df = df.fillna("NULL").astype(str)  # convertir toutes les colonnes en chaîne de caractères

    def nettoyer_texte(texte):
        texte = unicodedata.normalize('NFKD', texte).encode('ascii', 'ignore').decode('ascii')  # mettre en ASCII
        texte = texte.strip()  # retirer les espaces début/fin
        texte = re.sub(r'\s+', ' ', texte)  # remplacer les espaces multiples par un seul
        return texte

    for col in df.columns:
        df[col] = df[col].apply(nettoyer_texte)

    def nettoyer_numeros_telephone(texte):
        texte = texte.split(',')[0].strip()
        pattern = r'\b(0[1-9](?:[ .-]?\d{2}){4}|0[1-9]\d{8})\b'
        match = re.search(pattern, texte)
        if match:
            numero = match.group(0)
            numero = re.sub(r'\D', '', numero)
            numero = ' '.join(numero[i:i+2] for i in range(0, len(numero), 2))
            return numero.strip()
        return "NULL"

    if "téléphone" in df.columns:
        df["téléphone"] = df["téléphone"].apply(nettoyer_numeros_telephone)
    else:
        print("Colonne 'téléphone' non trouvée dans le fichier.")

    df.to_csv("fichier_nettoye.csv", index=False)
    print("Fichier nettoyé et sauvegardé dans 'fichier_nettoye.csv'")

# Utilisation avec votre fichier
nettoyage_csv("coworking_data_pandas.csv")