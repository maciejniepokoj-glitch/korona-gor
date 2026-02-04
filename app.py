import streamlit as st
import pandas as pd

# 1. Konfiguracja strony
st.set_page_config(page_title="KGP Tracker Pro", page_icon="🏔️", layout="wide")

# 2. Stylizacja - mniejsze karty i lepszy wygląd
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    div[data-testid="stColumn"] { padding: 5px; }
    .stCheckbox { background-color: #1e2130; padding: 10px; border-radius: 8px; font-size: 14px; }
    .metric-card { background: linear-gradient(135deg, #00b4db, #0083b0); padding: 15px; border-radius: 15px; color: white; text-align: center; }
    img { border-radius: 10px; object-fit: cover; }
    </style>
    """, unsafe_allow_html=True)

# 3. Pełna baza linków do zdjęć KGP
foto_url = {
    "Rysy": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d1/Rysy_od_morskiego_oka.jpg/400px-Rysy_od_morskiego_oka.jpg",
    "Babia Góra": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/17/Babia_G%C3%B3ra_widok_z_poudnia.jpg/400px-Babia_G%C3%B3ra_widok_z_poudnia.jpg",
    "Śnieżka": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a1/Sniezka_z_oddali.jpg/400px-Sniezka_z_oddali.jpg",
    "Śnieżnik": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e3/%C5%9Anie%C5%BCnik_K%C5%82odzki_S01.jpg/400px-%C5%9Anie%C5%BCnik_K%C5%82odzki_S01.jpg",
    "Tarnica": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/af/Tarnica_Bieszczady.jpg/400px-Tarnica_Bieszczady.jpg",
    "Turbacz": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/00/Turbacz_szczyt.jpg/400px-Turbacz_szczyt.jpg",
    "Radziejowa": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a2/Radziejowa_szczyt.jpg/400px-Radziejowa_szczyt.jpg",
    "Skrzyczne": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/23/Skrzyczne_widok_z_poudnia.jpg/400px-Skrzyczne_widok_z_poudnia.jpg",
    "Mogielica": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b3/Mogielica_widok_z_Jasienia.jpg/400px-Mogielica_widok_z_Jasienia.jpg",
    "Wysoka Kopa": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/df/Wysoka_Kopa_S01.jpg/400px-Wysoka_Kopa_S01.jpg",
    "Rudawiec": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b8/Rudawiec_szczyt.jpg/400px-Rudawiec_szczyt.jpg",
    "Orlica": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/77/Orlica_szczyt.jpg/400px-Orlica_szczyt.jpg",
    "Wysoka": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a7/Wysokie_Ska%C5%82ki_Pieniny.jpg/400px-Wysokie_Ska%C5%82ki_Pieniny.jpg",
    "Wielka Sowa": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f6/Wielka_Sowa_wie%C5%BCa.jpg/400px-Wielka_Sowa_wie%C5%BCa.jpg",
    "Lackowa": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/45/Lackowa_z_Ciechania.jpg/400px-Lackowa_z_Ciechania.jpg",
    "Kowadło": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Kowad%C5%82o_szczyt.jpg/400px-Kowad%C5%82o_szczyt.jpg",
    "Jagodna": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/be/Jagodna_szczyt.jpg/400px-Jagodna_szczyt.jpg",
    "Skalnik": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Skalnik_szczyt.jpg/400px-Skalnik_szczyt.jpg",
    "Waligóra": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3b/Walig%C3%B3ra_szczyt.jpg/400px-Walig%C3%B3ra_szczyt.jpg",
    "Czyniec": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/25/Czupel_widok_z_Magurki.jpg/400px-Czupel_widok_z_Magurki.jpg", # Czupel
    "Czupel": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/25/Czupel_widok_z_Magurki.jpg/400px-Czupel_widok_z_Magurki.jpg",
    "Szczeliniec Wielki": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/aa/Szczeliniec_Wielki_S01.jpg/400px-Szczeliniec_Wielki_S01.jpg",
    "Lubomir": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a6/Lubomir_szczyt.jpg/400px-Lubomir_szczyt.jpg",
    "Biskupia Kopa": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f5/Biskupia_Kopa_wie%C5%BCa.jpg/400px-Biskupia_Kopa_wie%C5%BCa.jpg",
    "Chełmiec": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/70/Che%C5%82miec_widok.jpg/400px-Che%C5%82miec_widok.jpg",
    "Kłodzka Góra": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0e/K%C5%82odzka_G%C3%B3ra_szczyt.jpg/400px-K%C5%82odzka_G%C3%B3ra_szczyt.jpg",
    "Skołczanka": "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?q=80&w=400", # Zastępcze
    "Wysoka Kopa": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/df/Wysoka_Kopa_S01.jpg/400px-Wysoka_Kopa_S01.jpg",
    "Ślęża": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/22/%C5%9Al%C4%99%C5%BCa_widok.jpg/400px-%C5%9Al%C4%99%C5%BCa_widok.jpg",
    "Łysica": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/07/%C5%81ysica_go%C5%82oborze.jpg/400px-%C5%81ysica_go%C5%82oborze.jpg"
}

# 4. Ładowanie danych
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('dane.csv', sep=None, engine='python', encoding='utf-8-sig')
    except:
        df = pd.read_csv('dane.csv', sep=None, engine='python', encoding='cp1250')
    df.columns = df.columns.str.replace('^\\ufeff', '', regex=True).str.strip()
    return df

try:
    df = load_data()
    st.title("🏔️ Korona Gór Polski")
    
    if 'zdobyte' not in st.session_state:
        st.session_state.zdobyte = []

    # Statystyki
    zdobyte_n = len(st.session_state.zdobyte)
    razem_n = len(df)
    procent = int((zdobyte_n / razem_n) * 100) if razem_n > 0 else 0

    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"<div class='metric-card'><h3>ZDOBYTE</h3><h2>{zdobyte_n} / {razem_n}</h2></div>", unsafe_allow_html=True)
    with c2:
        st.markdown(f"<div class='metric-card'><h3>POSTĘP</h3><h2>{procent}%</h2></div>", unsafe_allow_html=True)

    st.write("---")

    # 5. Generowanie kafelków - 3 w rzędzie (mniejsze zdjęcia)
    cols = st.columns(3)

    for index, row in df.iterrows():
        nazwa = row['Szczyt']
        wys = row['Wysokość mnp'] if 'Wysokość mnp' in df.columns else ""
        
        with cols[index % 3]:
            # Zdjęcie
            url = foto_url.get(nazwa, "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?q=80&w=400")
            st.image(url, use_container_width=True)
            
            # Checkbox
            checked = st.checkbox(f"{nazwa} ({wys}m)", key=f"btn_{index}", value=(nazwa in st.session_state.zdobyte))
            
            if checked and nazwa not in st.session_state.zdobyte:
                st.session_state.zdobyte.append(nazwa)
                st.rerun()
            elif not checked and nazwa in st.session_state.zdobyte:
                st.session_state.zdobyte.remove(nazwa)
                st.rerun()

except Exception as e:
    st.error(f"Błąd: {e}")
