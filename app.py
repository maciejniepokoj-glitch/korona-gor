import streamlit as st
import pandas as pd
import re

# 1. Ustawienia strony
st.set_page_config(page_title="KGP Tracker Pro", page_icon="🏔️", layout="wide")

# 2. Stylizacja (Dashboard + Małe karty)
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .metric-box { background: linear-gradient(135deg, #00b4db, #0083b0); padding: 15px; border-radius: 15px; color: white; text-align: center; }
    .stCheckbox { background-color: #1e2130; padding: 8px; border-radius: 8px; border-left: 3px solid #00d4ff; margin-bottom: 15px; }
    .stCheckbox label p { font-size: 13px !important; color: white !important; }
    .stImage > img { border-radius: 10px; height: 110px !important; object-fit: cover; }
    h1 { color: #00d4ff !important; font-size: 28px !important; }
    </style>
    """, unsafe_allow_html=True)

# 3. Rozszerzona baza zdjęć (Klucze muszą być krótkie)
foto_url = {
    "rysy": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d1/Rysy_od_morskiego_oka.jpg/400px-Rysy_od_morskiego_oka.jpg",
    "babia": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/17/Babia_G%C3%B3ra_widok_z_poudnia.jpg/400px-Babia_G%C3%B3ra_widok_z_poudnia.jpg",
    "śnieżka": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a1/Sniezka_z_oddali.jpg/400px-Sniezka_z_oddali.jpg",
    "śnieżnik": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e3/%C5%9Anie%C5%BCnik_K%C5%82odzki_S01.jpg/400px-%C5%9Anie%C5%BCnik_K%C5%82odzki_S01.jpg",
    "tarnica": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/af/Tarnica_Bieszczady.jpg/400px-Tarnica_Bieszczady.jpg",
    "turbacz": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/00/Turbacz_szczyt.jpg/400px-Turbacz_szczyt.jpg",
    "radziejowa": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a2/Radziejowa_szczyt.jpg/400px-Radziejowa_szczyt.jpg",
    "skrzyczne": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/23/Skrzyczne_widok_z_poudnia.jpg/400px-Skrzyczne_widok_z_poudnia.jpg",
    "mogielica": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b3/Mogielica_widok_z_Jasienia.jpg/400px-Mogielica_widok_z_Jasienia.jpg",
    "kopa": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/df/Wysoka_Kopa_S01.jpg/400px-Wysoka_Kopa_S01.jpg",
    "sowa": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f6/Wielka_Sowa_wie%C5%BCa.jpg/400px-Wielka_Sowa_wie%C5%BCa.jpg",
    "szczeliniec": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/aa/Szczeliniec_Wielki_S01.jpg/400px-Szczeliniec_Wielki_S01.jpg",
    "ślęża": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/22/%C5%9Al%C4%99%C5%BCa_widok.jpg/400px-%C5%9Al%C4%99%C5%BCa_widok.jpg",
    "łysica": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/07/%C5%81ysica_go%C5%82oborze.jpg/400px-%C5%81ysica_go%C5%82oborze.jpg"
}
DOMYSLNE_FOTO = "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?q=80&w=400"

@st.cache_data
def load_data():
    try:
        df = pd.read_csv('dane.csv', sep=None, engine='python', encoding='utf-8-sig')
    except:
        df = pd.read_csv('dane.csv', sep=None, engine='python', encoding='cp1250')
    # Automatyczne czyszczenie nazw kolumn i wierszy
    df.columns = [col.strip() for col in df.columns]
    return df.dropna(subset=[df.columns[0]]) # Usuwa puste wiersze

try:
    df = load_data()
    st.markdown("<h1>🏔️ KGP TRACKER PRO</h1>", unsafe_allow_html=True)
    
    if 'zdobyte' not in st.session_state:
        st.session_state.zdobyte = []

    # Dashboard
    zdobyte_n = len(st.session_state.zdobyte)
    razem_n = len(df)
    
    c1, c2 = st.columns([1, 2])
    with c1:
        st.markdown(f"<div class='metric-box'>ZALICZONE<br><span style='font-size:28px; font-weight:bold;'>{zdobyte_n} / {razem_n}</span></div>", unsafe_allow_html=True)
    with c2:
        st.write("##")
        st.progress(zdobyte_n / razem_n if razem_n > 0 else 0)

    st.write("---")

    # Układ 4 kolumn
    cols = st.columns(4)

    for index, row in df.iterrows():
        # Pobieramy nazwę szczytu (zawsze z pierwszej kolumny)
        nazwa_full = str(row.iloc[0]).strip()
        nazwa_clean = nazwa_full.lower()
        
        with cols[index % 4]:
            # Szukanie zdjęcia w słowniku
            url = DOMYSLNE_FOTO
            for klucz, link in foto_url.items():
                if klucz in nazwa_clean:
                    url = link
                    break
            
            # WYŚWIETLANIE ZDJĘCIA (Zabezpieczone)
            st.image(url, use_container_width=True)
            
            # Wyświetlanie Checkboxa
            display_name = nazwa_full.split(" w ")[0] # Skracamy nazwę do pierwszego członka
            
            if st.checkbox(display_name, key=f"ch_{index}", value=(nazwa_full in st.session_state.zdobyte)):
                if nazwa_full not in st.session_state.zdobyte:
                    st.session_state.zdobyte.append(nazwa_full)
                    st.rerun()
            else:
                if nazwa_full in st.session_state.zdobyte:
                    st.session_state.zdobyte.remove(nazwa_full)
                    st.rerun()

except Exception as e:
    st.error(f"Wystąpił błąd: {e}")
