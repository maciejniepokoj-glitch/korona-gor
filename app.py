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

# 2. Stylizacja CSS (Efekt Appki)
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .app-card {
        background: rgba(30, 33, 48, 0.7); backdrop-filter: blur(10px);
        border-radius: 20px; padding: 20px; border: 1px solid rgba(255,255,255,0.1); margin-bottom: 20px;
    }
    .map-link {
        text-decoration: none; font-size: 20px; padding: 8px 12px;
        background: #4caf50; color: white !important; border-radius: 12px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.3);
    }
    .mountain-row { border-bottom: 1px solid rgba(255,255,255,0.05); padding: 15px 0; }
    </style>
    """, unsafe_allow_html=True)

# 3. Logika i Dane
try:
    # Agresywne usuwanie 'nan' (puste wiersze i kolumny)
    df = pd.read_csv('dane.csv', sep=None, engine='python', skip_blank_lines=True).dropna(how='all')
    
    st.markdown(f"<h1>Witaj, {st.session_state.user_name}! 🏔️</h1>", unsafe_allow_html=True)

    # Dashboard
    z_n, r_n = len(st.session_state.zdobyte), len(df)
    proc = int((z_n/r_n)*100) if r_n > 0 else 0
    st.markdown(f"""
        <div class="app-card" style="text-align: center;">
            <div style="font-size: 42px; font-weight: bold; color: #00d4ff;">{proc}%</div>
            <div style="color: white; font-size: 14px; letter-spacing: 1px;">TWOJA KORONA GÓR POLSKI</div>
        </div>
    """, unsafe_allow_html=True)

    # Lista szczytów
    st.write("### Szlaki i Szczyty")
    for index, row in df.iterrows():
        # Pobranie czystej nazwy
        nazwa_full = str(row.iloc[0]).strip()
        if nazwa_full.lower() == "nan" or not nazwa_full: continue
        
        short_name = nazwa_full.split(" w ")[0]
        
        # Link do Mapy.com (wyszukiwanie konkretnej góry)
        search_query = urllib.parse.quote(f"{short_name} góra Polska")
        map_url = f"https://mapy.com/search?q={search_query}"

        # Layout wiersza (Checkbox | Nazwa | Mapa)
        with st.container():
            c1, c2, c3 = st.columns([1, 4, 1])
            
            is_checked = c1.checkbox("", key=f"c_{index}", value=(nazwa_full in st.session_state.zdobyte))
            c2.markdown(f"**{short_name}**<br><small style='color:#777'>Polska</small>", unsafe_allow_html=True)
            c3.markdown(f' <a href="{map_url}" target="_blank" class="map-link">📍</a>', unsafe_allow_html=True)
            
            st.markdown("<div class='mountain-row'></div>", unsafe_allow_html=True)

        # Obsługa zaznaczania i zapisu
        if is_checked and nazwa_full not in st.session_state.zdobyte:
            st.session_state.zdobyte.append(nazwa_full)
            save_user_data()
            st.rerun()
        elif not is_checked and nazwa_full in st.session_state.zdobyte:
            st.session_state.zdobyte.remove(nazwa_full)
            save_user_data()
            st.rerun()

except Exception as e:
    st.error(f"Coś nie tak z danymi: {e}")
