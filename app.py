import streamlit as st
import pandas as pd

# 1. Konfiguracja strony
st.set_page_config(page_title="KGP Tracker Pro", page_icon="🏔️", layout="wide")

# 2. Stylizacja CSS dla eleganckich kafelków
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    
    /* Styl Dashboardu */
    .metric-card { 
        background: linear-gradient(135deg, #00b4db, #0083b0); 
        padding: 20px; 
        border-radius: 15px; 
        color: white; 
        text-align: center; 
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }

    /* Styl Kafelków Szczytów */
    .stCheckbox { 
        background-color: #1e2130; 
        padding: 15px 20px; 
        border-radius: 12px; 
        border-left: 6px solid #00d4ff; 
        margin-bottom: 12px; 
        transition: 0.3s;
        box-shadow: 0 2px 8px rgba(0,0,0,0.2);
    }
    
    .stCheckbox:hover {
        background-color: #262a3d;
        border-left: 6px solid #ffffff;
        transform: translateX(5px);
    }

    /* Ukrycie domyślnych obramowań Streamlit */
    div[data-testid="stMetric"] {
        background-color: #1e2130;
        padding: 15px;
        border-radius: 10px;
    }

    h1, h3 { color: #00d4ff !important; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    </style>
    """, unsafe_allow_html=True)

# 3. Funkcja ładowania danych
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('dane.csv', sep=None, engine='python', encoding='utf-8-sig')
    except:
        df = pd.read_csv('dane.csv', sep=None, engine='python', encoding='cp1250')
    df.columns = df.columns.str.strip()
    return df

try:
    df = load_data()
    st.markdown("<h1>🏔️ KORONA GÓR POLSKI</h1>", unsafe_allow_html=True)
    
    if 'zdobyte' not in st.session_state:
        st.session_state.zdobyte = []

    # --- SEKCJA STATYSTYK ---
    zdobyte_n = len(st.session_state.zdobyte)
    razem_n = len(df)
    procent = int((zdobyte_n / razem_n) * 100) if razem_n > 0 else 0

    col_s1, col_s2, col_s3 = st.columns([1, 1, 1])
    
    with col_s1:
        st.markdown(f"<div class='metric-card'>ZALICZONE<br><span style='font-size:32px; font-weight:bold;'>{zdobyte_n} / {razem_n}</span></div>", unsafe_allow_html=True)
    with col_s2:
        st.markdown(f"<div class='metric-card'>POSTĘP<br><span style='font-size:32px; font-weight:bold;'>{procent}%</span></div>", unsafe_allow_html=True)
    with col_s3:
        st.markdown(f"<div class='metric-card'>DO ZDOBYCIA<br><span style='font-size:32px; font-weight:bold;'>{razem_n - zdobyte_n}</span></div>", unsafe_allow_html=True)

    st.write("##")
    st.progress(zdobyte_n / razem_n if razem_n > 0 else 0)
    st.write("##")

    # --- LISTA KAFELKÓW (3 kolumny dla przejrzystości) ---
    st.subheader("Lista Twoich szczytów")
    cols = st.columns(3)

    for index, row in df.iterrows():
        # Pobieramy nazwę (bezpiecznie z pierwszej kolumny)
        nazwa_full = str(row.iloc[0]).strip()
        
        # Wybieramy kolumnę (1, 2 lub 3)
        with cols[index % 3]:
            # Kafelek jako checkbox
            is_checked = st.checkbox(f"⛰️ {nazwa_full}", key=f"kgp_{index}", value=(nazwa_full in st.session_state.zdobyte))
            
            if is_checked:
                if nazwa_full not in st.session_state.zdobyte:
                    st.session_state.zdobyte.append(nazwa_full)
                    st.rerun()
            else:
                if nazwa_full in st.session_state.zdobyte:
                    st.session_state.zdobyte.remove(nazwa_full)
                    st.rerun()

except Exception as e:
    st.error(f"⚠️ Problem z plikiem danych: {e}")
