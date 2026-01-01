import streamlit as st
import pandas as pd

# Configuration de base
st.set_page_config(page_title="Stock Picker Européen", layout="wide")

st.title("🇪🇺 Analyse Fondamentale : STOXX 600")

# --- MÉMO SIMPLE ---
with st.expander("ℹ️ MÉMO : Rappel des indicateurs"):
    st.write("**PER** : Prix / Bénéfice (chercher < 15)")
    st.write("**ROE %** : Rentabilité des fonds propres (chercher > 15%)")
    st.write("**Yield %** : Rendement du dividende")

# --- CHARGEMENT ---
@st.cache_data
def load_data():
    try:
        # Lecture brute sans fioritures
        df = pd.read_csv("stoxx_data.csv")
        return df
    except:
        # Retourne un tableau vide avec colonnes si le fichier est illisible
        return pd.DataFrame(columns=["Société", "Ticker", "Secteur", "Pays", "PER", "Yield %", "ROE %"])

df = load_data()

if df.empty:
    st.error("⚠️ Erreur : Le fichier 'stoxx_data.csv' est manquant ou vide sur GitHub.")
else:
    # --- FILTRES ---
    st.sidebar.header("🔍 Recherche")
    search = st.sidebar.text_input("Nom de la société", "")
    
    p_list = sorted(df["Pays"].unique())
    s_list = sorted(df["Secteur"].unique())
    
    sel_p = st.sidebar.multiselect("Filtrer par Pays", p_list, default=p_list)
    sel_s = st.sidebar.multiselect("Filtrer par Secteur", s_list, default=s_list)
    
    # Application des filtres
    mask = (df["Pays"].isin(sel_p)) & (df["Secteur"].isin(sel_s))
    if search:
        mask = mask & (df["Société"].str.contains(search, case=False))
    
    df_filtered = df[mask].copy()

    # --- AFFICHAGE SIMPLE ---
    st.subheader(f"Résultats ({len(df_filtered)} sociétés)")
    
    # Affichage sans aucun style complexe (Heatmap supprimée)
    st.dataframe(
        df_filtered, 
        use_container_width=True, 
        hide_index=True
    )

st.divider()
st.caption("Application en mode haute compatibilité.")
