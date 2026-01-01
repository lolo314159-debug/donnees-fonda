import streamlit as st
import pandas as pd

# Configuration de la page
st.set_page_config(page_title="Stock Picker Européen", layout="wide")

st.title("🇪🇺 Analyse Fondamentale : STOXX 600 (Échantillon Pro)")

# --- MÉMO ANALYSE ---
with st.expander("ℹ️ MÉMO : Comment utiliser ces colonnes pour le Stock Picking ?"):
    c1, c2, c3 = st.columns(3)
    with c1:
        st.info("**PER (Price Earnings Ratio)**\n\nC'est le prix à payer pour 1€ de bénéfice. < 15 = souvent bon marché. > 25 = cher (souvent de la forte croissance).")
    with c2:
        st.info("**ROE % (Return on Equity)**\n\nRentabilité de l'argent des actionnaires. Cherchez des valeurs > 15% pour de la qualité.")
    with c3:
        st.info("**Yield % (Rendement)**\n\nLe dividende annuel. Utile pour le revenu passif. Attention si > 8% (risque de coupure).")

# --- CHARGEMENT DES DONNÉES ---
@st.cache_data
def load_data():
    try:
        # Charge le fichier CSV depuis le dépôt GitHub
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
    
    # Recherche textuelle
    search = st.sidebar.text_input("Nom de la société", "")
    
    # Filtre Pays
    list_pays = sorted(df["Pays"].unique())
    selected_pays = st.sidebar.multiselect("Filtrer par Pays", list_pays, default=list_pays)
    
    # Filtre Secteur
    list_secteurs = sorted(df["Secteur"].unique())
    selected_secteurs = st.sidebar.multiselect("Filtrer par Secteur", list_secteurs, default=list_secteurs)
    
    # Filtrage du DataFrame
    mask = (df["Pays"].isin(selected_pays)) & (df["Secteur"].isin(selected_secteurs))
    if search:
        mask = mask & (df["Société"].str.contains(search, case=False))
    
    df_filtered = df[mask]

    # --- AFFICHAGE DU TABLEAU ---
    st.subheader(f"Tableau Comparatif ({len(df_filtered)} sociétés)")
    
    # Style pour mettre en évidence les bonnes affaires
    st.dataframe(
        df_filtered.style.format({
            "PER": "{:.2f}",
            "Yield %": "{:.2f}%",
            "ROE %": "{:.2f}%"
        }).highlight_max(subset=["ROE %"], color="#2ecc71") # Vert pour meilleur ROE
          .highlight_min(subset=["PER"], color="#2ecc71"),   # Vert pour PER le plus bas
        use_container_width=True,
        hide_index=True
    )

st.divider()
st.caption("Données simulées pour 2026 basées sur les tendances historiques du CAC40, DAX40 et IBEX35.")
