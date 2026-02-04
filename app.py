import streamlit as st
import pandas as pd
import json
import os
import urllib.parse

# 1. Konfiguracja strony
st.set_page_config(page_title="TopTracker KGP", page_icon="🏔️", layout="centered")

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

# 2. Stylizacja "Wypas" (CSS)
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    
    /* Nagłówek profilu */
    .profile-header {
        display: flex; align-items: center; gap: 20px;
        padding: 20px; background: rgba(255,255,255,0.03);
        border-radius: 25px; border: 1px solid rgba(255,255,255,0.1);
        margin-bottom: 25px;
    }

    /* Okrągły postęp w stylu Apple Watch / Garmin */
    .progress-circle {
        border: 6px solid #00d4ff; border-radius: 50%;
        width: 100px; height: 100px;
        display: flex; flex-direction: column;
        justify-content: center; align-items: center;
        box-shadow: 0 0 20px rgba(0,212,255,0.2);
    }

    /* Kafelki szczytów */
    .mountain-card {
        background: #1e2130; border-radius: 20px;
        padding: 15px 20px; margin-bottom: 12px;
        border: 1px solid #2d3142;
        transition: 0.3s;
    }
    
    .stCheckbox { 
        background: transparent !important; padding: 0 !important; 
    }
    
    /* Ukrycie labela Streamlit i stylizacja tekstu */
    .stCheckbox label p {
        color: white !important; font-size: 17px !important; font-weight: 600 !important;
    }

    .map-btn {
        background: #4caf50; color: white !important;
        padding: 8px 15px; border-radius: 12px;
        text-decoration: none; font-size: 14px; font-weight: bold;
    }
    
    h1, h2 { color: white !important; }
    </style>
    """, unsafe_allow_html=True)

# 3. Logika Danych
try:
    df = pd.read_csv('dane.csv', sep=None, engine='python', skip_blank_lines=True).dropna(how='all')
    
    # --- NAGŁÓWEK ---
    z_n, r_n = len(st.session_state.zdobyte), len(df)
    proc = int((z_n/r_n)*100) if r_n > 0 else 0

    st.markdown(f"""
        <div class="profile-header">
            <div class="progress-circle">
                <span style="font-size: 22px; font-weight: bold; color: white;">{proc}%</span>
            </div>
            <div>
                <p style="color: #888; margin:0; font-size: 14px;">Witaj z powrotem,</p>
                <h1 style="margin:0; font-size: 24px;">{st.session_state.user_name}!</h1>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # --- ZAKŁADKI ---
    tab1, tab2 = st.tabs(["⛰️ Twoje Szczyty", "🏆 Ranking"])

    with tab1:
        st.write("##")
        for index, row in df.iterrows():
            nazwa_full = str(row.iloc[0]).strip()
            if nazwa_full.lower() == "nan" or not nazwa_full: continue
            
            short_name = nazwa_full.split(" w ")[0]
            
            # Link do Mapy.com
            search_query = urllib.parse.quote(f"{short_name} góra Polska")
            map_url = f"https://mapy.com/search?q={search_query}"

            # Kafelek "Wypas"
            with st.container():
                # Układ: Checkbox z nazwą | Przycisk mapy
                col_left, col_right = st.columns([4, 1.2])
                
                with col_left:
                    # Checkbox z nazwą góry
                    is_checked = st.checkbox(f"{short_name}", key=f"mt_{index}", value=(nazwa_full in st.session_state.zdobyte))
                
                with col_right:
                    # Przycisk mapy
                    st.markdown(f'<a href="{map_url}" target="_blank" class="map-btn">📍 MAPA</a>', unsafe_allow_html=True)
                
                # Obsługa logiki
                if is_checked and nazwa_full not in st.session_state.zdobyte:
                    st.session_state.zdobyte.append(nazwa_full)
                    save_user_data()
                    st.rerun()
                elif not is_checked and nazwa_full in st.session_state.zdobyte:
                    st.session_state.zdobyte.remove(nazwa_full)
                    save_user_data()
                    st.rerun()
                
                st.markdown("<div style='height:15px; border-bottom: 1px solid rgba(255,255,255,0.05); margin-bottom: 15px;'></div>", unsafe_allow_html=True)

    with tab2:
        st.info("Ranking będzie dostępny wkrótce! Połączymy go z profilami Twoich znajomych.")

except Exception as e:
    st.error(f"Upewnij się, że plik dane.csv jest poprawny. Błąd: {e}")
