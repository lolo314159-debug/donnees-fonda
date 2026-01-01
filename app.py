import streamlit as st
import pandas as pd
import yfinance as yf

st.set_page_config(page_title="Stoxx 600 Picker", layout="wide")

st.title("🇪🇺 STOXX 600 Dashboard")

@st.cache_data(ttl=3600)
def fetch_financial_data():
    # Liste de tickers ultra-connus pour tester la connexion
    tickers = ["ASML.AS", "MC.PA", "SAP.DE", "NESN.SW", "SHEL.L", "AIR.PA", "SIE.DE", "OR.PA"]
    
    results = []
    
    # Utilisation d'un conteneur pour afficher l'avancement
    status_text = st.empty()
    
    for t in tickers:
        try:
            status_text.text(f"Récupération de : {t}...")
            stock = yf.Ticker(t)
            # On demande uniquement les données spécifiques pour éviter le blocage
            fast_info = stock.fast_info 
            info = stock.info
            
            results.append({
                "Société": info.get("longName", t),
                "Ticker": t,
                "Secteur": info.get("sector", "Non classé"),
                "Prix": fast_info.get("last_price"),
                "PER": info.get("trailingPE"),
                "ROE %": (info.get("returnOnEquity", 0) or 0) * 100,
                "Yield %": (info.get("dividendYield", 0) or 0) * 100
            })
        except Exception as e:
            continue
            
    status_text.empty()
    return pd.DataFrame(results)

# --- EXECUTION ---
data = fetch_financial_data()

if data.empty:
    st.error("⚠️ Yahoo Finance ne répond pas. Cela arrive parfois avec les serveurs partagés. Cliquez sur 'Rerun' en haut à droite dans quelques instants.")
    if st.button("Réessayer maintenant"):
        st.cache_data.clear()
        st.rerun()
else:
    # Sidebar
    st.sidebar.header("Filtres")
    secteurs = sorted(data["Secteur"].unique())
    selected = st.sidebar.multiselect("Choisir Secteurs", secteurs, default=secteurs)
    
    # Filtrage et Affichage
    df_filtered = data[data["Secteur"].isin(selected)]
    
    st.subheader(f"Analyse de {len(df_filtered)} sociétés")
    st.dataframe(
        df_filtered.style.format({
            "Prix": "{:.2f} €",
            "PER": "{:.2f}",
            "ROE %": "{:.2f}%",
            "Yield %": "{:.2f}%"
        }),
        use_container_width=True
    )
