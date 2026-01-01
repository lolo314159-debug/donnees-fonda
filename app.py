import streamlit as st
import pandas as pd

st.set_page_config(page_title="Stoxx 600 Picker", layout="wide")

st.title("🇪🇺 STOXX 600 Dashboard")

# --- MÉMO DES COLONNES ---
with st.expander("ℹ️ Mémo : Signification des indicateurs (Stock Picking)"):
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        **1. PER (Price Earnings Ratio)**
        * *Définition :* Rapport entre le cours de bourse et le bénéfice par action.
        * *Interprétation :* Indique combien de fois l'investisseur paie le bénéfice. 
        * *Seuils :* Un PER < 15 est souvent jugé bon marché (Value), > 25 est jugé cher ou "Croissance".
        
        **2. ROE % (Return on Equity)**
        * *Définition :* Rentabilité des capitaux propres.
        * *Interprétation :* Capacité de l'entreprise à générer du profit avec l'argent des actionnaires.
        * *Cible :* On cherche idéalement un ROE > 15%.
        """)
    with col2:
        st.markdown("""
        **3. Yield % (Rendement du Dividende)**
        * *Définition :* Pourcentage du prix de l'action reversé en dividende.
        * *Interprétation :* Revenu passif généré par l'action.
        * *Attention :* Un rendement trop élevé (> 8%) peut parfois signaler un risque de coupure du dividende.
        
        **4. Secteur**
        * Permet de comparer les entreprises à leurs pairs (on ne compare pas le PER d'une banque avec celui d'une boîte de tech).
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
    st.error("⚠️ Fichier 'stoxx_data.csv' manquant.")
else:
    # Sidebar
    st.sidebar.header("Filtres")
    secteurs = sorted(df["Secteur"].unique())
    selected_sector = st.sidebar.multiselect("Filtrer par Secteur", secteurs, default=secteurs)
    
    # Filtrage
    filtered_df = df[df["Secteur"].isin(selected_sector)]
    
    # Affichage
    st.subheader(f"Résultats ({len(filtered_df)} sociétés)")
    st.dataframe(
        filtered_df.style.format({
            "PER": "{:.2f}",
            "Yield %": "{:.2f}%",
            "ROE %": "{:.2f}%"
        }),
        use_container_width=True
    )

st.info("💡 Conseil : Pour un bon Stock Picking, cherchez des entreprises avec un ROE élevé et un PER modéré.")
