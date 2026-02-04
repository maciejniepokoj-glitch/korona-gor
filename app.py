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
        df = pd.read_csv('dane.csv', sep
