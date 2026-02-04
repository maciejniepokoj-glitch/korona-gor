import streamlit as st
import pandas as pd
import json
import os

# 1. Konfiguracja strony pod Mobile App
st.set_page_config(
    page_title="KGP Tracker", 
    page_icon="🏔️", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. Inicjalizacja danych (NAPRAWA BŁĘDU ZE SCREENA)
SAVE_FILE = "postepy.json"

def load_user_data():
    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE, "r") as f:
                return json.load(f)
        except:
            pass
    return {"zdobyte": [], "user_name": "Wędrowcze"}

def save_user_data():
    data = {
        "zdobyte": st.session_state.zdobyte,
        "user_name": st.session_state.user_name
    }
    with open(SAVE_FILE, "w") as f:
        json.dump(data, f)

# Bezpieczne ustawienie zmiennych na samym początku
init_data = load_user_data()
if 'user_name' not in st.session_state:
    st.session_state.user_name = init_data["user_name"]
if 'zdobyte' not in st.session_state:
    st.session_state.zdobyte = init_data["zdobyte"]

# 3. Stylizacja Premium (Glassmorphism)
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    [data-testid="stHeader"] { background: rgba(0,0,0,0); }
    
    .app-card {
        background: rgba(30, 33, 48, 0.7);
        backdrop-filter: blur(10px);
        border-radius: 25px;
        padding: 20px;
        border: 1px solid rgba(255,255,255,0.1);
        margin-bottom: 20px;
    }
    
    .circle-progres {
        border: 5px solid #00d4ff;
        border-radius: 50%;
        width: 120px;
        height: 120px;
        margin: 0 auto;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        box-shadow: 0 0 20px rgba(0,212,255,0.2);
    }
    
    .mountain-item {
        background: #1e2130;
        border-radius: 15px;
        padding: 15px;
        margin-bottom: 10px;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }

    h1 { color: white !important; font-size: 24px !important; margin-bottom: 0px !important; }
    p { color: #888 !important; }
    </style>
    """, unsafe_allow_html=True)

# 4. Interfejs Aplikacji
try:
    df = pd.read_csv('dane.csv', sep=None, engine='python').dropna(how='all')
    
    # Nagłówek użytkownika
    with st.container():
        c1, c2 = st.columns([3, 1])
        c1.markdown(f"<h1>Cześć, {st.session_state.user_name}! 🏔️</h1>", unsafe_allow_html=True)
        if c2.button("⚙️"):
            st.session_state.show_settings = not st.session_state.get('show_settings', False)
        
        if st.session_state.get('show_settings', False):
            new_name = st.text_input("Twoje Imię:", st.session_state.user_name)
            if new_name != st.session_state.user_name:
                st.session_state.user_name = new_name
                save_user_data()
                st.rerun()

    # Dashboard (Okrągły postęp)
    z_n = len(st.session_state.zdobyte)
    r_n = len(df)
    proc = int((z_n/r_n)*100) if r_n > 0 else 0
    
    st.markdown(f"""
        <div class="app-card" style="text-align: center;">
            <div class="circle-progres">
                <span style="font-size: 24px; font-weight: bold; color: white;">{proc}%</span>
                <span style="font-size: 10px; color: #00d4ff;">UKOŃCZONO</span>
            </div>
            <div style="margin-top: 15px; color: white;">Zaliczono {z_n} z {r_n} szczytów</div>
        </div>
    """, unsafe_allow_html=True)

    # Zakładki
    tab1, tab2 = st.tabs(["⛰️ MOJE SZCZYTY", "🏆 RANKING"])

    with tab1:
        for index, row in df.iterrows():
            nazwa = str(row.iloc[0]).strip()
            short = nazwa.split(" w ")[0]
            
            # Customowy wiersz szczytu
            is_checked = nazwa in st.session_state.zdobyte
            
            col_txt, col_chk = st.columns([4, 1])
            col_txt.markdown(f"""
                <div style="padding: 10px 0;">
                    <b style="color: white; font-size: 16px;">{short}</b><br>
                    <span style="color: #666; font-size: 12px;">Korona Gór Polski</span>
                </div>
            """, unsafe_allow_html=True)
            
            if col_chk.checkbox("", key=f"m_{index}", value=is_checked):
                if nazwa not in st.session_state.zdobyte:
                    st.session_state.zdobyte.append(nazwa)
                    save_user_data()
                    st.rerun()
            else:
                if nazwa in st.session_state.zdobyte:
                    st.session_state.zdobyte.remove(nazwa)
                    save_user_data()
                    st.rerun()
            st.markdown("<hr style='margin:0; border-color: rgba(255,255,255,0.05)'>", unsafe_allow_html=True)

    with tab2:
        st.markdown("<div style='text-align:center; padding: 50px;'>Ranking będzie dostępny po połączeniu bazy danych.</div>", unsafe_allow_html=True)

except Exception as e:
    st.error(f"Wystąpił nieoczekiwany błąd. Sprawdź plik dane.csv. Szczegóły: {e}")
