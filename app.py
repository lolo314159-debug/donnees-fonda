import streamlit as st
import pandas as pd
import yfinance as yf

# 1. Configuration de la page
st.set_page_config(page_title="Stock Picker Européen", layout="wide")

st.title("🇪🇺 Analyseur Dynamique : STOXX 600")

# --- FONCTION DE MISE À JOUR VIA YAHOO FINANCE ---
def update_stock_data(dataframe):
    progress_bar = st.progress(0)
    status_text = st.empty()
    updated_rows = []
    total = len(dataframe)
    
    for i, row in dataframe.iterrows():
        ticker_symbol = row['Ticker']
        status_text.text(f"Actualisation : {row['Société']}...")
        
        try:
            stock = yf.Ticker(ticker_symbol)
            info = stock.info
            
            # Récupération des données réelles (ou garde l'ancienne si erreur)
            new_per = info.get('trailingPE', row['PER'])
            # Le yield est souvent en décimal (ex: 0.05 pour 5%)
            raw_yield = info.get('dividendYield', 0)
            new_yield = raw_yield * 100 if raw_yield else row['Yield %']
            
            raw_roe = info.get('returnOnEquity', 0)
            new_roe = raw_roe * 100 if raw_roe else row['ROE %']
            
            updated_rows.append({
                "Société": row['Société'],
                "Ticker": ticker_symbol,
                "Secteur": row['Secteur'],
                "Pays": row['Pays'],
                "PER": round(float(new_per), 2) if new_per else 0,
                "Yield %": round(float(new_yield), 2),
                "ROE %": round(float(new_roe), 2)
            })
        except:
            updated_rows.append(row.to_dict())
            
        progress_bar.progress((i + 1) / total)
    
    status_text.text("✅ Mise à jour terminée !")
    return pd.DataFrame(updated_rows)

# --- CHARGEMENT DES DONNÉES ---
@st.cache_data
def load_initial_data():
    try:
        return pd.read_csv("stoxx_data.csv")
    except:
        return pd.DataFrame(columns=["Société", "Ticker", "Secteur", "Pays", "PER", "Yield %", "ROE %"])

# Initialisation des données dans la session Streamlit
if 'df' not in st.session_state:
    st.session_state['df'] = load_initial_data()

df_active = st.session_state['df']

# --- BARRE LATÉRALE (GESTION & FILTRES) ---
st.sidebar.header("⚙️ Administration")

# Bouton de mise à jour
if st.sidebar.button("🔄 Actualiser via Yahoo Finance"):
    updated_df = update_stock_data(df_active)
    st.session_state['df'] = updated_df
    st.rerun()

# Bouton de téléchargement
csv = df_active.to_csv(index=False).encode('utf-8')
st.sidebar.download_button(
    label="📥 Télécharger le CSV à jour",
    data=csv,
    file_name='stoxx_data_final.csv',
    mime='text/csv',
)

st.sidebar.divider()
st.sidebar.header("🔍 Filtres de Recherche")

# Recherche par nom
search = st.sidebar.text_input("Rechercher une société", "")

# Filtres par Pays et Secteurs
if not df_active.empty:
    list_pays = sorted(df_active["Pays"].unique())
    selected_pays = st.sidebar.multiselect("Pays", list_pays, default=list_pays)
    
    list_secteurs = sorted(df_active["Secteur"].unique())
    selected_secteurs = st.sidebar.multiselect("Secteurs", list_secteurs, default=list_secteurs)

    # --- APPLICATION DES FILTRES ---
    mask = (df_active["Pays"].isin(selected_pays)) & (df_active["Secteur"].isin(selected_secteurs))
    if search:
        mask = mask & (df_active["Société"].str.contains(search, case=False))
    
    df_filtered = df_active[mask]

    # --- AFFICHAGE ---
    st.subheader(f"Tableau de bord ({len(df_filtered)} sociétés)")
    
    st.dataframe(
        df_filtered,
        use_container_width=True,
        hide_index=True
    )
else:
    st.warning("Veuillez vérifier que le fichier stoxx_data.csv est présent sur GitHub.")

st.divider()
st.caption("Données récupérées dynamiquement via yfinance. Cliquez sur les colonnes pour trier.")
