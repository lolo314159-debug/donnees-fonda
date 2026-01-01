import streamlit as st
import pandas as pd

# Configuration large
st.set_page_config(page_title="Stock Picker Pro", layout="wide")

st.title("🇪🇺 Analyse Fondamentale : STOXX 600")

# --- MÉMO ---
with st.expander("ℹ️ MÉMO : Aide à l'analyse"):
    st.markdown("""
    * **PER** : Vert = Action bon marché.
    * **ROE %** : Vert = Entreprise très rentable.
    * **Yield %** : Bleu = Dividende élevé.
    """)

# --- CHARGEMENT SÉCURISÉ ---
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("stoxx_data.csv")
        return df
    except:
        return pd.DataFrame(columns=["Société", "Ticker", "Secteur", "Pays", "PER", "Yield %", "ROE %"])

df = load_data()

if df.empty:
    st.error("⚠️ Fichier 'stoxx_data.csv' introuvable sur GitHub. Créez-le pour afficher les données.")
else:
    # Sidebar
    st.sidebar.header("🔍 Filtres")
    search = st.sidebar.text_input("Rechercher une société", "")
    
    # Filtres Pays et Secteurs
    p_list = sorted(df["Pays"].unique())
    s_list = sorted(df["Secteur"].unique())
    
    sel_p = st.sidebar.multiselect("Pays", p_list, default=p_list)
    sel_s = st.sidebar.multiselect("Secteurs", s_list, default=s_list)
    
    # Application filtres
    mask = (df["Pays"].isin(sel_p)) & (df["Secteur"].isin(sel_s))
    if search:
        mask = mask & (df["Société"].str.contains(search, case=False))
    
    df_filtered = df[mask].copy()

    # --- STYLE GRADUÉ ---
    if not df_filtered.empty:
        styled = df_filtered.style.format({
            "PER": "{:.2f}", "Yield %": "{:.2f}%", "ROE %": "{:.2f}%"
        }).background_gradient(cmap='RdYlGn_r', subset=['PER']
        ).background_gradient(cmap='RdYlGn', subset=['ROE %']
        ).background_gradient(cmap='Blues', subset=['Yield %'])
        
        st.dataframe(styled, use_container_width=True, hide_index=True)
    else:
        st.info("Aucun résultat pour ces filtres.")
