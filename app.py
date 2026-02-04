import streamlit as st
import pandas as pd
import json
import os

# 1. Konfiguracja strony
st.set_page_config(page_title="KGP Tracker Pro", page_icon="🏔️", layout="centered")

# --- SYSTEM ZAPISU (Persistence) ---
SAVE_FILE = "postepy.json"

def load_data_json():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as f: return json.load(f)
    return {"zdobyte": [], "user_name": "Wędrowcze"}

def save_data_json(data):
    with open(SAVE_FILE, "w") as f: json.dump(data, f)

# 2. Stylizacja CSS (Nowoczesny Interfejs)
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .user-header {
        background: linear-gradient(90deg, #1e2130 0%, #0e1117 100%);
        padding: 20px; border-radius: 20px; border: 1px solid #2d3142; margin-bottom: 25px;
    }
    .main-title { color: #00d4ff; font-family: 'Arial Black'; font-size: 32px; margin: 0; }
    .stat-card {
        background: #1e2130; border: 1px solid #2d3142; padding: 15px;
        border-radius: 18px; text-align: center; flex: 1;
    }
    .stat-val { font-size: 22px; font-weight: bold; color: #00d4ff; }
    .stCheckbox {
        background: #1e2130; border: 1px solid #2d3142; padding: 15px !important;
        border-radius: 15px !important; margin-bottom: 10px !important;
    }
    .stCheckbox:hover { border-color: #00d4ff; transform: scale(1.02); }
    </style>
    """, unsafe_allow_html=True)

# 3. Logika aplikacji
try:
    # Ładowanie danych szczytów i postępów
    df = pd.read_csv('dane.csv', sep=None, engine='python').dropna(how='all')
    user_data = load_data_json()
    
    if 'zdobyte' not in st.session_state:
        st.session_state.zdobyte = user_data["zdobyte"]
        st.session_state.user_name = user_data["user_name"]

    # NAGŁÓWEK Z NICKIEM
    with st.expander(f"👤 Profil: {st.session_state.user_name}"):
        new_name = st.text_input("Zmień swoje imię:", st.session_state.user_name)
        if new_name != st.session_state.user_name:
            st.session_state.user_name = new_name
            save_data_json({"zdobyte": st.session_state.zdobyte, "user_name": new_name})
            st.rerun()

    st.markdown(f"""
        <div class='user-header'>
            <p style='color: #888; margin:0;'>Witaj z powrotem,</p>
            <h1 class='main-title'>{st.session_state.user_name}! 🏔️</h1>
        </div>
    """, unsafe_allow_html=True)

    # STATYSTYKI
    z_n = len(st.session_state.zdobyte)
    r_n = len(df)
    proc = int((z_n/r_n)*100) if r_n > 0 else 0

    c1, c2, c3 = st.columns(3)
    c1.markdown(f"<div class='stat-card'><div style='font-size:10px; color:#888;'>SZCZYTY</div><div class='stat-val'>{z_n}/{r_n}</div></div>", unsafe_allow_html=True)
    c2.markdown(f"<div class='stat-card'><div style='font-size:10px; color:#888;'>PROGRES</div><div class='stat-val'>{proc}%</div></div>", unsafe_allow_html=True)
    c3.markdown(f"<div class='stat-card'><div style='font-size:10px; color:#888;'>CEL</div><div class='stat-val'>{r_n-z_n}</div></div>", unsafe_allow_html=True)
    
    st.write("##")
    st.progress(z_n/r_n if r_n > 0 else 0)

    # LISTA
    for index, row in df.iterrows():
        nazwa = str(row.iloc[0]).strip()
        short = nazwa.split(" w ")[0]
        
        if st.checkbox(f"📍 {short}", key=f"m_{index}", value=(nazwa in st.session_state.zdobyte)):
            if nazwa not in st.session_state.zdobyte:
                st.session_state.zdobyte.append(nazwa)
                save_data_json({"zdobyte": st.session_state.zdobyte, "user_name": st.session_state.user_name})
                st.rerun()
        else:
            if nazwa in st.session_state.zdobyte:
                st.session_state.zdobyte.remove(nazwa)
                save_data_json({"zdobyte": st.session_state.zdobyte, "user_name": st.session_state.user_name})
                st.rerun()

except Exception as e:
    st.error(f"Coś poszło nie tak: {e}")
