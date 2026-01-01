import streamlit as st
import pandas as pd
import yfinance as yf

st.set_page_config(page_title="Stoxx 600 Analyzer", layout="wide")

@st.cache_data(ttl=3600)
def fetch_data():
    # Liste de test réduite pour assurer le fonctionnement
    tickers = ["ASML.AS", "MC.PA", "SAP.DE", "NESN.SW", "SHEL.L", "AIR.PA", "SIE.DE"]
    
    results = []
    progress_bar = st.progress(0)
    
    for i, t in enumerate(tickers):
        try:
            stock = yf.Ticker(t)
            inf = stock.info
            # On vérifie que les données essentielles existent avant d'ajouter
            if 'longName' in inf:
                results.append({
                    "Société": inf.get("longName"),
                    "Ticker": t,
                    "Secteur": inf.get("sector", "Inconnu"),
                    "PER": inf.get("trailingPE"),
                    "Yield %": (inf.get("dividendYield", 0) or 0) * 100,
                    "ROE %": (inf.get("returnOnEquity", 0) or 0) * 100
                })
        except Exception:
            continue
        progress_bar.progress((i + 1) / len(tickers))
    
    # Création du DataFrame avec des colonnes par défaut si vide
    if not results:
        return pd.DataFrame(columns=["Société", "Ticker", "Secteur", "PER", "Yield %", "ROE %"])
    
    return pd.DataFrame(results)

st.title("🇪🇺 STOXX 600 Dashboard")

with st.spinner('Chargement des données...'):
    df = fetch_data()

if df.empty:
    st.error("⚠️ Impossible de récupérer les données de Yahoo Finance pour le moment. Réessayez dans quelques minutes.")
else:
    # FILTRES SÉCURISÉS
    st.sidebar.header("Paramètres")
    
    # On s'assure que la colonne existe avant de créer le filtre
    secteurs_dispo = df["Secteur"].unique().tolist()
    selected_sector = st.sidebar.multiselect("Secteurs", secteurs_dispo, default=secteurs_dispo)

    # Filtrage
    filtered_df = df[df["Secteur"].isin(selected_sector)]

    # Affichage
    st.dataframe(
        filtered_df.style.format({"PER": "{:.2f}", "Yield %": "{:.2f}%", "ROE %": "{:.2f}%"}),
        use_container_width=True
    )
