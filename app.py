import streamlit as st
import pandas as pd

# 1. Konfiguracja strony
st.set_page_config(page_title="KGP Tracker Pro", page_icon="🏔️", layout="wide")

# 2. Stylizacja CSS
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .metric-card { 
        background: linear-gradient(135deg, #00b4db, #0083b0); 
        padding: 20px; border-radius: 15px; color: white; text-align: center; 
    }
    .stCheckbox { 
        background-color: #1e2130; padding: 15px 20px; border-radius: 12px; 
        border-left: 6px solid #00d4ff; margin-bottom: 12px;
    }
    h1 { color: #00d4ff !important; text-align: center; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 3. Funkcja ładowania danych z filtrem "nan"
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('dane.csv', sep=None, engine='python', encoding='utf-8-sig')
    except:
        df = pd.read_csv('dane.csv', sep=None, engine='python', encoding='cp1250')
    
    # USUWANIE PUSTYCH WIERSZY (To naprawia błąd "nan")
    df = df.dropna(how='all') 
    df = df[df.iloc[:, 0].notna()] 
    
    df.columns = df.columns.str.strip()
    return df

try:
    df = load_data()
    st.markdown("<h1>🏔️ KORONA GÓR POLSKI</h1>", unsafe_allow_html=True)
    
    if 'zdobyte' not in st.session_state:
        st.session_state.zdobyte = []

    # Statystyki
    zdobyte_n = len(st.session_state.zdobyte)
    razem_n = len(df)
    procent = int((zdobyte_n / razem_n) * 100) if razem_n > 0 else 0

    c1, c2, c3 = st.columns(3)
    with c1: st.markdown(f"<div class='metric-card'>ZALICZONE<br><b>{zdobyte_n} / {razem_n}</b></div>", unsafe_allow_html=True)
    with c2: st.markdown(f"<div class='metric-card'>POSTĘP<br><b>{procent}%</b></div>", unsafe_allow_html=True)
    with c3: st.markdown(f"<div class='metric-card'>DO ZDOBYCIA<br><b>{razem_n - zdobyte_n}</b></div>", unsafe_allow_html=True)

    st.write("##")
    st.progress(zdobyte_n / razem_n if razem_n > 0 else 0)

    # Lista szczytów
    cols = st.columns(3)
    for index, row in df.iterrows():
        nazwa_full = str(row.iloc[0]).strip()
        
        with cols[index % 3]:
            if st.checkbox(f"⛰️ {nazwa_full}", key=f"kgp_{index}", value=(nazwa_full in st.session_state.zdobyte)):
                if nazwa_full not in st.session_state.zdobyte:
                    st.session_state.zdobyte.append(nazwa_full)
                    st.rerun()
            else:
                if nazwa_full in st.session_state.zdobyte:
                    st.session_state.zdobyte.remove(nazwa_full)
                    st.rerun()

except Exception as e:
    st.error(f"Błąd: {e}")
