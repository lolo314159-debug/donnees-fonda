import streamlit as st
import pandas as pd

# Configuration de la page
st.set_page_config(page_title="Stock Picker Européen", layout="wide")

st.title("🇪🇺 Analyse Fondamentale : STOXX 600")

# --- MÉMO ANALYSE ---
with st.expander("ℹ️ MÉMO : Signification des couleurs et colonnes"):
    st.markdown("""
    * **PER** (Vert = Moins cher) : Rapport cours/bénéfice. 
    * **ROE %** (Vert = Plus rentable) : Rendement des capitaux propres.
    * **Yield %** (Bleu = Gros dividende) : Rendement du dividende.
    """)

# --- CHARGEMENT SÉCURISÉ DES DONNÉES ---
@st.cache_data
def load_data():
    try:
        # Tente de lire le fichier CSV sur ton GitHub
        df = pd.read_csv("stoxx_data.csv")
        return df
    except Exception as e:
        # Renvoie un tableau vide avec les colonnes pour éviter le KeyError
        return pd.DataFrame(columns=["Société", "Ticker", "Secteur", "Pays", "PER", "Yield %", "ROE %"])

df = load_data()

# Vérification si le fichier est vide ou manquant
if df.empty:
    st.warning("⚠️ Le fichier 'stoxx_data.csv' est vide ou introuvable sur GitHub. Vérifie tes fichiers.")
else:
    # --- BARRE LATÉRALE (FILTRES) ---
    st.sidebar.header("🔍 Recherche & Filtres")
    search = st.sidebar.text_input("Nom de la société", "")
    
    # Filtres sécurisés (ne s'affichent que si les colonnes existent)
    selected_pays = st.sidebar.multiselect("Pays", sorted(df["Pays"].unique()), default=df["Pays"].unique())
    selected_secteurs = st.sidebar.multiselect("Secteurs", sorted(df["Secteur"].unique()), default=df["Secteur"].unique())
    
    # Application des filtres
    mask = (df["Pays"].isin(selected_pays)) & (df["Secteur"].isin(selected_secteurs))
    if search:
        mask = mask & (df["Société"].str.contains(search, case=False))
    
    df_filtered = df[mask].copy()

    # --- STYLE AVEC GRADIENTS ---
    # On vérifie qu'on a des données avant d'appliquer le style
    if not df_filtered.empty:
        styled_df = df_filtered.style.format({
            "PER": "{:.2f}",
            "Yield %": "{:.2f}%",
            "ROE %": "{:.2f}%"
        }).background_gradient(cmap='RdYlGn_r', subset=['PER']      # Vert = Petit PER
        ).background_gradient(cmap='RdYlGn', subset=['ROE %']       # Vert = Gros ROE
        ).background_gradient(cmap='Blues', subset=['Yield %'])     # Bleu = Gros Dividende

        st.subheader(f"Résultats ({len(df_filtered)} sociétés)")
        st.dataframe(styled_df, use_container_width=True, hide_index=True)
    else:
        st.info("Aucun résultat ne correspond à vos filtres.")

st.divider()
st.caption("Données basées sur le fichier stoxx_data.csv mis à jour.")
