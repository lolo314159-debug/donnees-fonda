import streamlit as st
import pandas as pd
import yfinance as yf

# Configuration
st.set_page_config(page_title="Stoxx 600 Analyzer", layout="wide")

@st.cache_data(ttl=3600) # Garde les données en mémoire 1h pour la rapidité
def fetch_data():
    # Liste de tickers représentatifs du Stoxx 600 (Échantillon)
    tickers = [
        "ASML.AS", "MC.PA", "SAP.DE", "NESN.SW", "NOVN.SW", 
        "ROG.SW", "HSBA.L", "SHEL.L", "TTE.PA", "AIR.PA",
        "OR.PA", "RMS.PA", "SIE.DE", "ALV.DE", "SANOFI.PA",
        "BNP.PA", "IBE.MC", "ITX.MC", "VOLVB.ST", "BMW.DE"
    ]
    
    results = []
    progress_bar = st.progress(0)
    
    for i, t in enumerate(tickers):
        try:
            stock = yf.Ticker(t)
            inf = stock.info
            results.append({
                "Société": inf.get("longName", t),
                "Ticker": t,
                "Secteur": inf.get("sector", "N/A"),
                "PER": inf.get("trailingPE"),
                "P/Book": inf.get("priceToBook"),
                "Yield %": (inf.get("dividendYield", 0) or 0) * 100,
                "ROE %": (inf.get("returnOnEquity", 0) or 0) * 100,
                "Dette/Equity": inf.get("debtToEquity"),
                "Marge %": (inf.get("grossMargins", 0) or 0) * 100
            })
        except:
            pass
        progress_bar.progress((i + 1) / len(tickers))
    
    return pd.DataFrame(results)

st.title("🇪🇺 STOXX 600 Stock Picking Dashboard")
st.write("Analyse comparative des fondamentaux en temps réel.")

# Chargement
df = fetch_data()

# Barre latérale pour le filtrage
st.sidebar.header("Paramètres de filtrage")
selected_sector = st.sidebar.multiselect("Secteurs", df["Secteur"].unique(), default=df["Secteur"].unique())
min_yield = st.sidebar.slider("Rendement Div. Min (%)", 0.0, 10.0, 0.0)

# Application des filtres
filtered_df = df[(df["Secteur"].isin(selected_sector)) & (df["Yield %"] >= min_yield)]

# Affichage avec style
st.subheader("Tableau de bord interactif")
st.dataframe(
    filtered_df.style.highlight_max(axis=0, subset=['ROE %'], color='#2ecc71')
                     .highlight_min(axis=0, subset=['PER'], color='#2ecc71')
                     .format({"PER": "{:.2f}", "P/Book": "{:.2f}", "Yield %": "{:.2f}%", "ROE %": "{:.2f}%"}),
    use_container_width=True
)

st.success("✅ Tri possible : cliquez sur le nom d'une colonne.")
