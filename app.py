import streamlit as st
import pandas as pd

# Configuration de la page
st.set_page_config(page_title="Stock Picker Européen", layout="wide")

st.title("🇪🇺 Analyse Fondamentale : STOXX 600 (Heatmap Edition)")

# --- MÉMO ANALYSE ---
with st.expander("ℹ️ MÉMO : Signification des couleurs"):
    st.markdown("""
    * **PER** : Plus c'est **Vert**, moins l'action est chère par rapport à ses bénéfices.
    * **ROE %** : Plus c'est **Vert**, plus l'entreprise est rentable sur ses fonds propres.
    * **Yield %** : Plus c'est **Bleu**, plus le rendement du dividende est élevé.
    """)

# --- CHARGEMENT DES DONNÉES ---
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("stoxx_data.csv")
        return df
    except:
        return pd.DataFrame()

df = load_data()

if df.empty:
    st.error("⚠️ Erreur : Le fichier 'stoxx_data.csv' est introuvable sur GitHub.")
else:
    # --- BARRE LATÉRALE (FILTRES) ---
    st.sidebar.header("🔍 Recherche & Filtres")
    search = st.sidebar.text_input("Nom de la société", "")
    
    list_pays = sorted(df["Pays"].unique())
    selected_pays = st.sidebar.multiselect("Filtrer par Pays", list_pays, default=list_pays)
    
    list_secteurs = sorted(df["Secteur"].unique())
    selected_secteurs = st.sidebar.multiselect("Filtrer par Secteur", list_secteurs, default=list_secteurs)
    
    # Filtrage
    mask = (df["Pays"].isin(selected_pays)) & (df["Secteur"].isin(selected_secteurs))
    if search:
        mask = mask & (df["Société"].str.contains(search, case=False))
    
    df_filtered = df[mask].copy()

    # --- STYLE AVEC COULEURS GRADUÉES ---
    # On définit des dégradés (Colormaps)
    # 'RdYlGn_r' : Red to Yellow to Green inversé (pour le PER : petit est vert)
    # 'RdYlGn' : Red to Yellow to Green (pour le ROE : grand est vert)
    # 'Blues' : Dégradé de bleu pour le rendement
    
    styled_df = df_filtered.style.format({
        "PER": "{:.2f}",
        "Yield %": "{:.2f}%",
        "ROE %": "{:.2f}%"
    }).background_gradient(cmap='RdYlGn_r', subset=['PER']
    ).background_gradient(cmap='RdYlGn', subset=['ROE %']
    ).background_gradient(cmap='Blues', subset=['Yield %'])

    # --- AFFICHAGE ---
    st.subheader(f"Résultats de l'analyse ({len(df_filtered)} sociétés)")
    st.dataframe(styled_df, use_container_width=True, hide_index=True)

st.divider()
st.caption("Astuce : Cliquez sur le nom d'une colonne pour trier et voir les dégradés se regrouper.")
