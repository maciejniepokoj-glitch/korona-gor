import streamlit as st
import pandas as pd

# 1. Konfiguracja strony
st.set_page_config(page_title="Korona Gór Polski v2.0", page_icon="🏔️", layout="wide")

# 2. Profesjonalna stylizacja CSS
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stCheckbox { background-color: #1e2130; padding: 20px; border-radius: 15px; border-left: 5px solid #00d4ff; margin-bottom: 10px; transition: 0.3s; }
    .stCheckbox:hover { background-color: #262a3d; transform: translateY(-2px); }
    .metric-card { background: linear-gradient(135deg, #00b4db, #0083b0); padding: 20px; border-radius: 20px; color: white; text-align: center; }
    h1 { color: #00d4ff; font-family: 'Helvetica Neue', sans-serif; font-weight: 800; }
    </style>
    """, unsafe_allow_html=True)

# 3. Ładowanie danych (z poprawką na Twoje kolumny)
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('dane.csv', sep=None, engine='python', encoding='utf-8-sig')
    except:
        df = pd.read_csv('dane.csv', sep=None, engine='python', encoding='cp1250')
    df.columns = df.columns.str.replace('^\\ufeff', '', regex=True).str.strip()
    return df

try:
    df = load_data()
    
    # Nagłówek i Statystyki
    st.title("🏔️ Korona Gór Polski")
    
    if 'zdobyte' not in st.session_state:
        st.session_state.zdobyte = []

    # --- DASHBOARD STATYSTYK ---
    col_stat1, col_stat2, col_stat3 = st.columns([1, 1, 1])
    
    zdobyte_n = len(st.session_state.zdobyte)
    razem_n = len(df)
    procent = int((zdobyte_n / razem_n) * 100)

    with col_stat1:
        st.markdown(f"<div class='metric-card'><h3>ZDOBYTE</h3><h2>{zdobyte_n} / {razem_n}</h2></div>", unsafe_allow_html=True)
    with col_stat2:
        st.markdown(f"<div class='metric-card'><h3>POSTĘP</h3><h2>{procent}%</h2></div>", unsafe_allow_html=True)
    with col_stat3:
        # Przeliczamy wysokość (zakładając że masz kolumnę 'Wysokość mnp')
        suma_m = zdobyte_n * 1000 # To tylko przykład, dopóki nie przeliczymy realnej sumy
        st.markdown(f"<div class='metric-card'><h3>WYNIK GÓRSKI</h3><h2>🏆</h2></div>", unsafe_allow_html=True)

    st.write("##") # Odstęp

    # --- LISTA KART SZCZYTÓW ---
    st.subheader("Twoje wyzwania")
    
    # Tworzymy 2 kolumny dla kart
    col1, col2 = st.columns(2)

    for index, row in df.iterrows():
        nazwa = row['Szczyt']
        wys = row['Wysokość mnp'] if 'Wysokość mnp' in df.columns else "---"
        
        # Wybieramy kolumnę (lewa/prawa)
        with (col1 if index % 2 == 0 else col2):
            # Tworzymy kontener, który imituje profesjonalną kartę
            is_checked = st.checkbox(f"⛰️ {nazwa} | {wys} m n.p.m.", key=f"card_{index}")
            
            if is_checked:
                if nazwa not in st.session_state.zdobyte:
                    st.session_state.zdobyte.append(nazwa)
                    st.rerun()
            else:
                if nazwa in st.session_state.zdobyte:
                    st.session_state.zdobyte.remove(nazwa)
                    st.rerun()

except Exception as e:
    st.error(f"Coś poszło nie tak: {e}")
