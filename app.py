import streamlit as st
import pandas as pd
import yfinance as yf

st.set_page_config(page_title="Stock Picker Dynamique", layout="wide")

st.title("🇪🇺 Analyseur STOXX 600 - Mise à jour Directe")

# --- FONCTION DE MISE À JOUR ---
def update_stock_data(dataframe):
    progress_bar = st.progress(0)
    status_text = st.empty()
    updated_rows = []
    
    total = len(dataframe)
    
    for i, row in dataframe.iterrows():
        ticker_symbol = row['Ticker']
        status_text.text(f"Récupération de {row['Société']} ({ticker_symbol})...")
        
        try:
            stock = yf.Ticker(ticker_symbol)
            info = stock.info
            
            # Extraction des données en direct
            new_per = info.get('trailingPE', row['PER'])
            new_yield = info.get('dividendYield', 0) * 100 if info.get('dividendYield') else row['Yield %']
            new_roe = info.get('returnOnEquity', 0) * 100 if info.get('returnOnEquity') else row['ROE %']
            
            updated_rows.append({
                "Société": row['Société'],
                "Ticker": ticker_symbol,
                "Secteur": row['Secteur'],
                "Pays": row['Pays'],
                "PER": round(new_per, 2),
                "Yield %": round(new_yield, 2),
                "ROE %": round(new_roe, 2)
            })
        except:
            updated_rows.append(row.to_dict())
            
        progress_bar.progress((i + 1) / total)
    
    status_text.text("Mise à jour terminée !")
    return pd.DataFrame(updated_rows)

# --- CHARGEMENT INITIAL ---
@st.cache_data
def load_data():
    return pd.read_csv("stoxx_data.csv")

df = load_data()

# --- INTERFACE ---
st.sidebar.header("⚙️ Gestion des données")

if st.sidebar.button("🔄 Actualiser les données via Yahoo Finance"):
    df = update_stock_data(df)
    st.session_state['df'] = df
    st.success("Les données ont été actualisées avec les cours du jour !")

# Utilisation des données de session si elles existent
if 'df' in st.session_state:
    df = st.session_state['df']

# Bouton de téléchargement du nouveau CSV
csv = df.to_csv(index=False).encode('utf-8')
st.sidebar.download_button(
    label="📥 Télécharger le CSV mis à jour",
    data=csv,
    file_name='stoxx_data_updated.csv',
    mime='text/csv',
)

# --- FILTRES ET AFFICHAGE ---
# (Reprenez ici votre code de filtrage habituel)
search = st.text_input("Rechercher une action", "")
df_filtered = df[df['Société'].str.contains(search, case=False)] if search else df
st.dataframe(df_filtered, use_container_width=True, hide_index=True)
