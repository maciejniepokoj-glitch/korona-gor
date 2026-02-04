import streamlit as st
import pandas as pd
import json
import os
import urllib.parse

# 1. Konfiguracja pod Mobile
st.set_page_config(page_title="KGP Tracker Pro", page_icon="🏔️", layout="centered")

# --- SYSTEM ZAPISU ---
SAVE_FILE = "postepy.json"

def load_user_data():
    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE, "r") as f: return json.load(f)
        except: pass
    return {"zdobyte": [], "user_name": "Wędrowcze"}

def save_user_data():
    data = {"zdobyte": st.session_state.zdobyte, "user_name": st.session_state.user_name}
    with open(SAVE_FILE, "w") as f: json.dump(data, f)

# Inicjalizacja stanu
init_data = load_user_data()
if 'user_name' not in st.session_state: st.session_state.user_name = init_data["user_name"]
if 'zdobyte' not in st.session_state: st.session_state.zdobyte = init_data["zdobyte"]

# 2. Stylizacja CSS (Efekt Wow + Mapy)
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .app-card {
        background: rgba(30, 33, 48, 0.7); backdrop-filter: blur(10px);
        border-radius: 20px; padding: 20px; border: 1px solid rgba(255,255,255,0.1); margin-bottom: 20px;
    }
    .mountain-row {
        display: flex; align-items: center; justify-content: space-between;
        padding: 12px; border-bottom: 1px solid rgba(255,255,255,0.05);
    }
    .map-link {
        text-decoration: none; font-size: 20px; padding: 5px 10px;
        background: rgba(0, 212, 255, 0.1); border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Logika i Dane
try:
    # NAPRAWA 'nan': skip_blank_lines=True i dropna usuwają puste rekordy
    df = pd.read_csv('dane.csv', sep=None, engine='python', skip_blank_lines=True).dropna(how='all')
    
    st.markdown(f"<h1>Witaj, {st.session_state.user_name}! 🏔️</h1>", unsafe_allow_html=True)

    # Dashboard
    z_n, r_n = len(st.session_state.zdobyte), len(df)
    proc = int((z_n/r_n)*100) if r_n > 0 else 0
    st.markdown(f"""
        <div class="app-card" style="text-align: center;">
            <div style="font-size: 40px; font-weight: bold; color: #00d4ff;">{proc}%</div>
            <div style="color: white;">Zaliczono {z_n} z {r_n} szczytów</div>
        </div>
    """, unsafe_allow_html=True)

    # Lista szczytów
    st.write("### Twoje wyzwania")
    for index, row in df.iterrows():
        # Bezpieczne wczytanie nazwy (naprawa nan w tekście)
        nazwa_full = str(row.iloc[0]).strip()
        if nazwa_full == "nan" or not nazwa_full: continue
        
        short_name = nazwa_full.split(" w ")[0]
        
        # Generowanie linku do Google Maps
        search_query = urllib.parse.quote(f"{short_name} góra Polska")
        map_url = f"https://www.google.com/maps/search/?api=1&query={search_query}"

        # Layout wiersza
        col_chk, col_txt, col_map = st.columns([1, 4, 1])
        
        is_checked = col_chk.checkbox("", key=f"c_{index}", value=(nazwa_full in st.session_state.zdobyte))
        
        col_txt.markdown(f"**{short_name}**")
        col_map.markdown(f' <a href="{map_url}" target="_blank" class="map-link">📍</a>', unsafe_allow_html=True)

        # Obsługa zaznaczania
        if is_checked and nazwa_full not in st.session_state.zdobyte:
            st.session_state.zdobyte.append(nazwa_full)
            save_user_data()
            st.rerun()
        elif not is_checked and nazwa_full in st.session_state.zdobyte:
            st.session_state.zdobyte.remove(nazwa_full)
            save_user_data()
            st.rerun()

except Exception as e:
    st.error(f"Problem z danymi: {e}")
