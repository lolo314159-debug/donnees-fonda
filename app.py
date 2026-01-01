import streamlit as st
import pandas as pd

st.set_page_config(page_title="Stoxx 600 Picker", layout="wide")

st.title("🇪🇺 STOXX 600 Dashboard (Mode Fichier)")

# Fonction pour charger les données sans risque de blocage
@st.cache_data
def load_data():
    try:
        # On lit le fichier CSV que vous avez mis sur GitHub
        df = pd.read_csv("stoxx_data.csv")
        return df
    except:
        return pd.DataFrame()

df = load_data()

if df.empty:
    st.error("⚠️ Le fichier 'stoxx_data.csv' est introuvable sur votre GitHub.")
    st.info("Créez un fichier nommé stoxx_data.csv à côté de votre app.py pour afficher les données.")
else:
    # Sidebar pour les filtres
    st.sidebar.header("Filtres")
    secteurs = sorted(df["Secteur"].unique())
    selected_sector = st.sidebar.multiselect("Secteurs", secteurs, default=secteurs)
    
    # Filtrage
    filtered_df = df[df["Secteur"].isin(selected_sector)]
    
    # Affichage du tableau
    st.subheader(f"Analyse de {len(filtered_df)} sociétés")
    st.dataframe(
        filtered_df.style.format({
            "PER": "{:.2f}",
            "Yield %": "{:.2f}%",
            "ROE %": "{:.2f}%"
        }),
        use_container_width=True
    )
    
    st.success("Données chargées depuis le fichier local (Pas de risque de blocage Yahoo).")
