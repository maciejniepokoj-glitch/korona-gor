import streamlit as st
import pandas as pd

# 1. Konfiguracja strony
st.set_page_config(page_title="Korona Gór Polski", page_icon="🏔️", layout="wide")

# 2. Twój ulubiony styl wizualny (Ciemne tło + niebieskie akcenty)
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stCheckbox { background-color: #1e2130; padding: 20px; border-radius: 12px; border-left: 5px solid #00d4ff; margin-bottom: 20px; }
    .metric-card { background: linear-gradient(135deg, #00b4db, #0083b0); padding: 25px; border-radius: 20px; color: white; text-align: center; margin-bottom: 25px; }
    h1 { color: #00d4ff !important; font-family: 'Arial Black'; }
    img { border-radius: 15px; object-fit: cover; height: 200px !important; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# 3. Baza zdjęć (Uproszczona, by uniknąć błędów)
foto_url = {
    "rysy": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d1/Rysy_od_morskiego_oka.jpg/600px-Rysy_od_morskiego_oka.jpg",
    "babia": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/17/Babia_G%C3%B3ra_widok_z_poudnia.jpg/600px-Babia_G%C3%B3ra_widok_z_poudnia.jpg",
    "śnieżka": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a1/Sniezka_z_oddali.jpg/600px-Sniezka_z_oddali.jpg",
    "tarnica": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/af/Tarnica_Bieszczady.jpg/600px-Tarnica_Bieszczady.jpg",
    "turbacz": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/00/Turbacz_szczyt.jpg/600px-Turbacz_szczyt.jpg",
    "śnieżnik": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e3/%C5%9Anie%C5%BCnik_K%C5%82odzki_S01.jpg/600px-%C5%9Anie%C5%BCnik_K%C5%82odzki_S01.jpg"
}
DOMYSLNE_GORY = "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?q=80&w=800"

# 4. Ładowanie danych
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('dane.csv', sep=None, engine='python', encoding='utf-8-sig')
    except:
        df = pd.read_csv('dane.csv', sep=None, engine='python', encoding='cp1250')
    return df

try:
    df = load_data()
    st.title("🏔️ Moja Korona Gór Polski")
    
    if 'zdobyte' not in st.session_state:
        st.session_state.zdobyte = []

    # --- STATYSTYKI (Te co działały) ---
    zdobyte_n = len(st.session_state.zdobyte)
    razem_n = len(df)
    procent = int((zdobyte_n / razem_n) * 100) if razem_n > 0 else 0

    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"<div class='metric-card'><h3>ZDOBYTE</h3><h2>{zdobyte_n} / {razem_n}</h2></div>", unsafe_allow_html=True)
    with c2:
        st.markdown(f"<div class='metric-card'><h3>PROCENT</h3><h2>{procent}%</h2></div>", unsafe_allow_html=True)

    st.write("---")

    # --- LISTA SZCZYTÓW (2 Kolumny) ---
    col1, col2 = st.columns(2)

    for index, row in df.iterrows():
        # Używamy iloc[0] żeby zawsze brać pierwszą kolumnę niezależnie od nazwy
        nazwa_oryginalna = str(row.iloc[0])
        nazwa_low = nazwa_oryginalna.lower()
        
        with (col1 if index % 2 == 0 else col2):
            # Wybór zdjęcia
            wybrany_url = DOMYSLNE_GORY
            for klucz, link in foto_url.items():
                if klucz in nazwa_low:
                    wybrany_url = link
                    break
            
            # Wyświetlamy zdjęcie i checkbox
            st.image(wybrany_url, use_container_width=True)
            
            checked = st.checkbox(f"{nazwa_oryginalna}", key=f"k_{index}", value=(nazwa_oryginalna in st.session_state.zdobyte))
            
            if checked and nazwa_oryginalna not in st.session_state.zdobyte:
                st.session_state.zdobyte.append(nazwa_oryginalna)
                st.rerun()
            elif not checked and nazwa_oryginalna in st.session_state.zdobyte:
                st.session_state.zdobyte.remove(nazwa_oryginalna)
                st.rerun()

except Exception as e:
    st.error(f"Coś poszło nie tak: {e}")
