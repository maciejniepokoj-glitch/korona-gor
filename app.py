import streamlit as st
import pandas as pd

# 1. Konfiguracja i Twój ulubiony styl PRO
st.set_page_config(page_title="Korona Gór Polski", page_icon="🏔️", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stCheckbox { background-color: #1e2130; padding: 15px; border-radius: 10px; border-left: 5px solid #00d4ff; margin-bottom: 20px; }
    .metric-card { background: linear-gradient(135deg, #00b4db, #0083b0); padding: 20px; border-radius: 20px; color: white; text-align: center; margin-bottom: 20px; }
    h1 { color: #00d4ff !important; }
    img { border-radius: 10px; object-fit: cover; height: 150px !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. Baza zdjęć - słowa klucze (małymi literami)
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

@st.cache_data
def load_data():
    try:
        df = pd.read_csv('dane.csv', sep=None, engine='python', encoding='utf-8-sig')
    except:
        df = pd.read_csv('dane.csv', sep=None, engine='python', encoding='cp1250')
    df.columns = df.columns.str.strip()
    return df

try:
    df = load_data()
    st.title("🏔️ Moja Korona Gór Polski")
    
    if 'zdobyte' not in st.session_state:
        st.session_state.zdobyte = []

    # Statystyki (Układ, który Ci się podobał)
    zdobyte_n = len(st.session_state.zdobyte)
    razem_n = len(df)
    procent = int((zdobyte_n / razem_n) * 100) if razem_n > 0 else 0

    col_stat1, col_stat2 = st.columns(2)
    with col_stat1:
        st.markdown(f"<div class='metric-card'><h3>ZDOBYTE</h3><h2>{zdobyte_n} / {razem_n}</h2></div>", unsafe_allow_html=True)
    with col_stat2:
        st.markdown(f"<div class='metric-card'><h3>POSTĘP</h3><h2>{procent}%</h2></div>", unsafe_allow_html=True)

    st.write("---")

    # Karty szczytów (2 w rzędzie - stabilne i czytelne)
    col1, col2 = st.columns(2)

    for index, row in df.iterrows():
        nazwa_full = str(row.iloc[0]) # Bierze nazwę z pierwszej kolumny
        nazwa_lower = nazwa_full.lower()
        
        with (col1 if index % 2 == 0 else col2):
            # DOPASOWANIE ZDJĘCIA
            img_url = "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?q=80&w=400"
            for klucz in foto_url:
                if klucz in nazwa_lower:
                    img_url = foto_url[klucz]
                    break
            
            st.image(img_url, use_container_width=True)
            
            checked = st.checkbox(f"{nazwa_full}", key=f"kgp_{index}", value=(nazwa_full in st.session_state.zdobyte))
            
            if checked and nazwa_full not in st.session_state.zdobyte:
                st.session_state.zdobyte.append(nazwa_full)
                st.rerun()
            elif not checked and nazwa_full in st.session_state.zdobyte:
                st.session_state.zdobyte.remove(nazwa_full)
                st.rerun()

except Exception as e:
    st.error(f"Problem z plikiem: {e}")
