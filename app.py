import streamlit as st
import pandas as pd

# 1. Konfiguracja i Styl PRO (Twój ulubiony)
st.set_page_config(page_title="Korona Gór Polski", page_icon="🏔️", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stCheckbox { background-color: #1e2130; padding: 15px; border-radius: 12px; border-left: 5px solid #00d4ff; margin-bottom: 20px; }
    .metric-card { background: linear-gradient(135deg, #00b4db, #0083b0); padding: 25px; border-radius: 20px; color: white; text-align: center; margin-bottom: 25px; }
    h1 { color: #00d4ff !important; font-family: 'Arial Black'; text-align: center; }
    img { border-radius: 15px; object-fit: cover; height: 180px !important; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# 2. Baza zdjęć - zoptymalizowane linki
foto_url = {
    "rysy": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d1/Rysy_od_morskiego_oka.jpg/600px-Rysy_od_morskiego_oka.jpg",
    "babia": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/17/Babia_G%C3%B3ra_widok_z_poudnia.jpg/600px-Babia_G%C3%B3ra_widok_z_poudnia.jpg",
    "śnieżka": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a1/Sniezka_z_oddali.jpg/600px-Sniezka_z_oddali.jpg",
    "śnieżnik": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e3/%C5%9Anie%C5%BCnik_K%C5%82odzki_S01.jpg/600px-%C5%9Anie%C5%BCnik_K%C5%82odzki_S01.jpg",
    "tarnica": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/af/Tarnica_Bieszczady.jpg/600px-Tarnica_Bieszczady.jpg",
    "turbacz": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/00/Turbacz_szczyt.jpg/600px-Turbacz_szczyt.jpg",
    "radziejowa": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a2/Radziejowa_szczyt.jpg/600px-Radziejowa_szczyt.jpg",
    "skrzyczne": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/23/Skrzyczne_widok_z_poudnia.jpg/600px-Skrzyczne_widok_z_poudnia.jpg",
    "mogielica": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b3/Mogielica_widok_z_Jasienia.jpg/600px-Mogielica_widok_z_Jasienia.jpg",
    "kopa": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/df/Wysoka_Kopa_S01.jpg/600px-Wysoka_Kopa_S01.jpg",
    "sowa": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f6/Wielka_Sowa_wie%C5%BCa.jpg/600px-Wielka_Sowa_wie%C5%BCa.jpg",
    "szczeliniec": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/aa/Szczeliniec_Wielki_S01.jpg/600px-Szczeliniec_Wielki_S01.jpg",
    "ślęża": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/22/%C5%9Al%C4%99%C5%BCa_widok.jpg/600px-%C5%9Al%C4%99%C5%BCa_widok.jpg",
    "łysica": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/07/%C5%81ysica_go%C5%82oborze.jpg/600px-%C5%81ysica_go%C5%82oborze.jpg"
}
DOMYSLNE_FOTO = "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?q=80&w=800"

# 3. Bezpieczne ładowanie danych
@st.cache_data
def load_data():
    try:
        # Próba odczytu z automatycznym wykrywaniem separatora i obsługą BOM
        df = pd.read_csv('dane.csv', sep=None, engine='python', encoding='utf-8-sig')
    except:
        df = pd.read_csv('dane.csv', sep=None, engine='python', encoding='cp1250')
    
    # Czyszczenie nazw kolumn ze spacji i dziwnych znaków
    df.columns = df.columns.str.replace(r'[^\w\s]', '', regex=True).str.strip()
    return df

try:
    df = load_data()
    st.title("🏔️ Moja Korona Gór Polski")
    
    if 'zdobyte' not in st.session_state:
        st.session_state.zdobyte = []

    # --- DASHBOARD STATYSTYK ---
    zdobyte_n = len(st.session_state.zdobyte)
    razem_n = len(df)
    procent = int((zdobyte_n / razem_n) * 100) if razem_n > 0 else 0

    col_s1, col_s2 = st.columns(2)
    with col_s1:
        st.markdown(f"<div class='metric-card'><h3>ZDOBYTE</h3><h2>{zdobyte_n} / {razem_n}</h2></div>", unsafe_allow_html=True)
    with col_s2:
        st.markdown(f"<div class='metric-card'><h3>POSTĘP</h3><h2>{procent}%</h2></div>", unsafe_allow_html=True)

    st.write("---")

    # --- KARTY SZCZYTÓW (2 Kolumny) ---
    col1, col2 = st.columns(2)

    for index, row in df.iterrows():
        # Pobieramy nazwę z pierwszej dostępnej kolumny (odporność na błąd 'Szczyt')
        nazwa_full = str(row.iloc[0]).strip()
        nazwa_low = nazwa_full.lower()
        
        with (col1 if index % 2 == 0 else col2):
            # Dopasowanie zdjęcia
            url = DOMYSLNE_FOTO
            for klucz, link in foto_url.items():
                if klucz in nazwa_low:
                    url = link
                    break
            
            st.image(url, use_container_width=True)
            
            # Checkbox z nazwą
            if st.checkbox(nazwa_full, key=f"chk_{index}", value=(nazwa_full in st.session_state.zdobyte)):
                if nazwa_full not in st.session_state.zdobyte:
                    st.session_state.zdobyte.append(nazwa_full)
                    st.rerun()
            else:
                if nazwa_full in st.session_state.zdobyte:
                    st.session_state.zdobyte.remove(nazwa_full)
                    st.rerun()

except Exception as e:
    st.error(f"⚠️ Wystąpił błąd podczas ładowania aplikacji: {e}")
