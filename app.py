import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
import urllib.parse

# 1. Konfiguracja strony
st.set_page_config(page_title="KGP TopTracker", page_icon="🏆", layout="centered")

# 2. BEZPIECZNA INICJALIZACJA (Naprawia błąd ze zdjęcia nr 1)
if 'user_id' not in st.session_state:
    st.session_state.user_id = None

# Stylizacja UI
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stTabs [data-baseweb="tab"] { background-color: #1e2130; border-radius: 10px; color: white; }
    .user-card { background: #1e2130; padding: 15px; border-radius: 15px; border-left: 5px solid #00d4ff; margin-bottom: 10px; }
    .map-btn { background: #4caf50; color: white !important; padding: 5px 10px; border-radius: 8px; text-decoration: none; font-size: 12px; }
    </style>
    """, unsafe_allow_html=True)

# 3. LOGOWANIE
if st.session_state.user_id is None:
    st.title("🏔️ Witaj w TopTracker")
    nick = st.text_input("Podaj swój Nick, aby wejść:")
    if st.button("Zaloguj"):
        if nick:
            st.session_state.user_id = nick
            st.rerun()
    st.stop()

# 4. POŁĄCZENIE Z BAZĄ (Wymaga wpisów w Secrets!)
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    all_data = conn.read(ttl="2s")
    # Czyścimy dane z pustych wierszy (naprawa nan)
    if all_data is not None:
        all_data = all_data.dropna(how='all')
    else:
        all_data = pd.DataFrame(columns=['Użytkownik', 'Szczyt'])
except Exception as e:
    st.error("Błąd połączenia. Sprawdź, czy dodałeś link do Arkusza w 'Secrets'!")
    st.stop()

# 5. GŁÓWNE MENU
tab1, tab2 = st.tabs(["⛰️ Moje Szczyty", "🏆 Ranking"])

with tab1:
    st.header(f"Profil: {st.session_state.user_id}")
    
    # Wczytanie szczytów z dane.csv
    try:
        df_peaks = pd.read_csv('dane.csv', sep=None, engine='python').dropna(how='all')
    except:
        st.error("Nie znaleziono pliku dane.csv!")
        st.stop()

    my_done = all_data[all_data['Użytkownik'] == st.session_state.user_id]['Szczyt'].tolist()
    
    st.write(f"Zaliczono: **{len(my_done)} / {len(df_peaks)}**")
    st.progress(len(my_done)/len(df_peaks) if len(df_peaks) > 0 else 0)

    for index, row in df_peaks.iterrows():
        peak_full = str(row.iloc[0]).strip()
        if peak_full == "nan": continue
        
        short = peak_full.split(" w ")[0]
        is_done = peak_full in my_done
        
        c1, c2 = st.columns([4, 1])
        if c1.checkbox(f"📍 {short}", value=is_done, key=f"p_{index}"):
            if not is_done:
                new_row = pd.DataFrame([{"Użytkownik": st.session_state.user_id, "Szczyt": peak_full}])
                updated = pd.concat([all_data, new_row], ignore_index=True)
                conn.update(data=updated)
                st.rerun()
        else:
            if is_done:
                updated = all_data[~((all_data['Użytkownik'] == st.session_state.user_id) & (all_data['Szczyt'] == peak_full))]
                conn.update(data=updated)
                st.rerun()
        
        q = urllib.parse.quote(f"{short} góra Polska")
        c2.markdown(f'<a href="https://mapy.com/search?q={q}" target="_blank" class="map-btn">MAPA</a>', unsafe_allow_html=True)

with tab2:
    st.header("🏆 Ranking")
    if not all_data.empty:
        ranking = all_data.groupby('Użytkownik').size().reset_index(name='Suma').sort_values('Suma', ascending=False)
        for i, row in ranking.iterrows():
            st.markdown(f"""
                <div class="user-card">
                    <b>#{i+1} {row['Użytkownik']}</b> 
                    <span style="float:right; color:#00d4ff;">{row['Suma']} szczytów</span>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.write("Baza jest pusta. Bądź pierwszy!")
