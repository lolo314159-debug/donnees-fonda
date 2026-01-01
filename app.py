import streamlit as st
import pandas as pd

# 1. Configuration de la page
st.set_page_config(page_title="Stock Picker STOXX 600", layout="wide")

st.title("🇪🇺 Analyse Fondamentale : STOXX 600")

# --- MÉMO ANALYSE ---
with st.expander("ℹ️ MÉMO : Signification des indicateurs"):
    st.markdown("""
    * **PER** (Vert = Moins cher) : Rapport cours/bénéfice.
    * **ROE %** (Vert = Plus rentable) : Capacité à générer du profit avec l'argent des actionnaires.
    * **Yield %** (Bleu = Dividende élevé) : Rendement annuel versé.
    """)

# --- CHARGEMENT DES DONNÉES ---
@st.cache_data
def load_data():
    try:
        # Lecture du fichier CSV sur GitHub
        df = pd.read_csv("stoxx_data.csv")
        # Nettoyage minimal pour éviter les erreurs de texte
        df.columns = df.columns.str.strip()
        return df
    except:
        return pd.DataFrame()

df = load_data()

# Vérification de la présence des données pour éviter les KeyError
if df.empty:
    st.error("⚠️ Le fichier 'stoxx_data.csv' est manquant ou mal formaté sur GitHub.")
    st.info("Créez un fichier stoxx_data.csv avec les colonnes : Société, Ticker, Secteur, Pays, PER, Yield %, ROE %")
else:
    # --- BARRE LATÉRALE ---
    st.sidebar.header("🔍 Filtres")
    
    # Filtre de recherche
    search = st.sidebar.text_input("Rechercher une société", "")
    
    # Filtres par Pays et Secteur (Sécurisés)
    list_pays = sorted(df["Pays"].dropna().unique())
    selected_pays = st.sidebar.multiselect("Pays", list_pays, default=list_pays)
    
    list_secteurs = sorted(df["Secteur"].dropna().unique())
    selected_secteurs = st.sidebar.multiselect("Secteurs", list_secteurs, default=list_secteurs)
    
    # Application des filtres
    mask = (df["Pays"].isin(selected_pays)) & (df["Secteur"].isin(selected_secteurs))
    if search:
        mask = mask & (df["Société"].str.contains(search, case=False))
    
    df_filtered = df[mask].copy()

    # --- AFFICHAGE ET COULEURS ---
    if not df_filtered.empty:
        # Application des dégradés de couleurs
        styled_df = df_filtered.style.format({
            "PER": "{:.2f}",
            "Yield %": "{:.2f}%",
            "ROE %": "{:.2f}%"
        }).background_gradient(cmap='RdYlGn_r', subset=['PER']
        ).background_gradient(cmap='RdYlGn', subset=['ROE %']
        ).background_gradient(cmap='Blues', subset=['Yield %'])

        st.dataframe(styled_df, use_container_width=True, hide_index=True)
    else:
        st.warning("Aucun résultat pour ces filtres.")

st.caption("Données de démonstration STOXX 600 - Mise à jour 2026")
