import streamlit as st
import pandas as pd
import json
import os

# 1. Konfiguracja strony
st.set_page_config(page_title="KGP Tracker Pro", page_icon="🏔️", layout="centered")

# --- FUNKCJE ZAPISU I ODCZYTU (Efekt Wow: Dane nie znikają!) ---
SAVE_FILE = "postepy.json"

def load_progress():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as f:
            return json.load(f)
    return []

def save_progress(zdobyte):
    with open(SAVE_FILE, "w") as f:
        json.dump(zdobyte, f)

# 2. Stylizacja CSS (Design Premium)
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    
    /* Nagłówek */
    .main-title {
        text-align: center;
        color: #00d4ff;
        font-family: 'Arial Black';
        font-size: 40px;
        margin-bottom: 30px;
        text-shadow: 0 0 15px rgba(0,212,255,0.4);
    }

    /* Kafelki statystyk */
    .stat-container {
        display: flex;
        justify-content: space-between;
        gap: 15px;
        margin-bottom: 30px;
    }
    .stat-card {
        background: linear-gradient(135deg, #1e2130 0%, #141722 100%);
        border: 1px solid #2d3142;
        padding: 20px;
        border-radius: 20px;
        text-align: center;
        flex: 1;
        box-shadow: 0 10px 20px rgba(0,0,0,0.3);
    }
    .stat-val { font-size: 24px; font-weight: bold; color: #00d4ff; }
    .stat-label { font-size: 10px; color: #888; text-transform: uppercase; letter-spacing: 1px; }

    /* Kafelki Szczytów */
    .stCheckbox {
        background: #1e2130;
        border: 1px solid #2d3142;
        padding: 20px 25px !important;
        border-radius: 20px !important;
        margin-bottom: 12px !important;
        transition: all 0.3s ease;
    }
    .stCheckbox:hover {
        border-color: #00d4ff;
        transform: translateY(-3px);
        box-shadow: 0 5px 15px rgba(0,212,255,0.1);
    }
    
    /* Tekst checkboxa */
    .stCheckbox label p {
        color: white !important;
        font-weight: 600 !important;
        font-size: 16px !important;
    }

    /* Ukrycie domyślnego menu Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# 3. Ładowanie danych
@st.cache_data
def load_mountain_data():
    try:
        df = pd.read_csv('dane.csv', sep=None, engine='python', encoding='utf-8-sig')
    except:
        df = pd.read_csv('dane.csv', sep=None, engine='python', encoding='cp1250')
    return df.dropna(how='all')

try:
    df = load_mountain_data()
    
    # Inicjalizacja stanu z zapisanego pliku
    if 'zdobyte' not in st.session_state:
        st.session_state.zdobyte = load_progress()

    st.markdown("<div class='main-title'>KGP TRACKER PRO</div>", unsafe_allow_html=True)

    # 4. DASHBOARD STATYSTYK
    zdobyte_n = len(st.session_state.zdobyte)
    razem_n = len(df)
    procent = int((zdobyte_n / razem_n) * 100) if razem_n > 0 else 0

    st.markdown(f"""
        <div class="stat-container">
            <div class="stat-card"><div class="stat-label">Zaliczone</div><div class="stat-val">🏔️ {zdobyte_n}</div></div>
            <div class="stat-card"><div class="stat-label">Progres</div><div class="stat-val">📈 {procent}%</div></div>
            <div class="stat-card"><div class="stat-label">Pozostało</div><div class="stat-val">🎯 {razem_n - zdobyte_n}</div></div>
        </div>
    """, unsafe_allow_html=True)

    st.progress(zdobyte_n / razem_n if razem_n > 0 else 0)
    st.write("##")

    # 5. LISTA SZCZYTÓW (Elegancka lista)
    st.markdown("<h3 style='color: white; font-size: 18px;'>Lista Wyzwań</h3>", unsafe_allow_html=True)

    for index, row in df.iterrows():
        nazwa_full = str(row.iloc[0]).strip()
        
        # Wyświetlamy tylko główną nazwę góry
        short_name = nazwa_full.split(" w ")[0].split("(")[0]
        
        # Checkbox jako kafelek
        if st.checkbox(f"⛰️  {short_name}", key=f"mtn_{index}", value=(nazwa_full in st.session_state.zdobyte)):
            if nazwa_full not in st.session_state.zdobyte:
                st.session_state.zdobyte.append(nazwa_full)
                save_progress(st.session_state.zdobyte) # Zapis do pliku
                st.rerun()
        else:
            if nazwa_full in st.session_state.zdobyte:
                st.session_state.zdobyte.remove(nazwa_full)
                save_progress(st.session_state.zdobyte) # Zapis do pliku
                st.rerun()

    # Stopka
    st.markdown("<div style='text-align: center; color: #444; margin-top: 50px; font-size: 12px;'>TopTracker v3.0 • Premium Edition</div>", unsafe_allow_html=True)

except Exception as e:
    st.error(f"⚠️ Błąd aplikacji: {e}")
