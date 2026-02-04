import streamlit as st
import pandas as pd

# 1. Konfiguracja strony
st.set_page_config(page_title="KGP Tracker Pro", page_icon="🏔️", layout="wide")

# 2. Stylizacja: Bardzo małe kafelki i zgrabne zdjęcia
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    [data-testid="stMetricValue"] { font-size: 20px !important; color: #00d4ff; }
    .stCheckbox { background-color: #1e2130; padding: 3px 8px; border-radius: 4px; margin-top: -10px; }
    .stCheckbox label p { font-size: 11px !important; color: #cfd0d6; }
    .stImage > img { border-radius: 6px; height: 90px !important; object-fit: cover; }
    div[data-testid="stColumn"] { padding: 1px !important; }
    hr { margin: 10px 0px; }
    </style>
    """, unsafe_allow_html=True)

# 3. Baza zdjęć (skrócone klucze dla lepszego dopasowania)
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
    "rudawiec": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b8/Rudawiec_szczyt.jpg/400px-Rudawiec_szczyt.jpg",
    "orlica": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/77/Orlica_szczyt.jpg/400px-Orlica_szczyt.jpg",
    "wysoka": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a7/Wysokie_Ska%C5%82ki_Pieniny.jpg/400px-Wysokie_Ska%C5%82ki_Pieniny.jpg",
    "sowa": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f6/Wielka_Sowa_wie%C5%BCa.jpg/400px-Wielka_Sowa_wie%C5%BCa.jpg",
    "lackowa": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/45/Lackowa_z_Ciechania.jpg/400px-Lackowa_z_Ciechania.jpg",
    "kowadło": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Kowad%C5%82o_szczyt.jpg/400px-Kowad%C5%82o_szczyt.jpg",
    "jagodna": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/be/Jagodna_szczyt.jpg/400px-Jagodna_szczyt.jpg",
    "skalnik": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Skalnik_szczyt.jpg/400px-Skalnik_szczyt.jpg",
    "waligóra": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3b/Walig%C3%B3ra_szczyt.jpg/400px-Walig%C3%B3ra_szczyt.jpg",
    "czupel": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/25/Czupel_widok_z_Magurki.jpg/400px-Czupel_widok_z_Magurki.jpg",
    "szczeliniec": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/aa/Szczeliniec_Wielki_S01.jpg/400px-Szczeliniec_Wielki_S01.jpg",
    "lubomir": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a6/Lubomir_szczyt.jpg/400px-Lubomir_szczyt.jpg",
    "biskupia": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f5/Biskupia_Kopa_wie%C5%BCa.jpg/400px-Biskupia_Kopa_wie%C5%BCa.jpg",
    "chełmiec": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/70/Che%C5%82miec_widok.jpg/400px-Che%C5%82miec_widok.jpg",
    "kłodzka": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0e/K%C5%82odzka_G%C3%B3ra_szczyt.jpg/400px-K%C5%82odzka_G%C3%B3ra_szczyt.jpg",
    "ślęża": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/22/%C5%9Al%C4%99%C5%BCa_widok.jpg/400px-%C5%9Al%C4%99%C5%BCa_widok.jpg",
    "łysica": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/07/%C5%81ysica_go%C5%82oborze.jpg/400px-%C5%81ysica_go%C5%82oborze.jpg"
}

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
    st.markdown("<h3 style='text-align: center; color: white;'>🏔️ MÓJ TRACKER KGP</h3>", unsafe_allow_html=True)
    
    if 'zdobyte' not in st.session_state:
        st.session_state.zdobyte = []

    # Mini statystyki w jednej linii
    zdobyte_n = len(st.session_state.zdobyte)
    razem_n = len(df)
    
    s1, s2 = st.columns([1, 3])
    s1.metric("Wynik", f"{zdobyte_n}/{razem_n}")
    s2.progress(zdobyte_n / razem_n if razem_n > 0 else 0)

    st.write("---")

    # 5 KOLUMN (Bardzo małe kafelki)
    cols = st.columns(5)

    for index, row in df.iterrows():
        nazwa_z_pliku = str(row['Szczyt'])
        nazwa_do_szukania = nazwa_z_pliku.lower()
        
        with cols[index % 5]:
            # Inteligentne dopasowanie zdjęcia
            url = "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?q=80&w=400" # domyślne
            for klucz, link in foto_url.items():
                if klucz in nazwa_do_szukania:
                    url = link
                    break
            
            st.image(url, use_container_width=True)
            
            # Skracamy nazwę do wyświetlenia na kafelku (tylko pierwsze 2 wyrazy)
            krotka_nazwa = " ".join(nazwa_z_pliku.split()[:2])
            
            checked = st.checkbox(f"{krotka_nazwa}", key=f"c_{index}", value=(nazwa_z_pliku in st.session_state.zdobyte))
            
            if checked and nazwa_z_pliku not in st.session_state.zdobyte:
                st.session_state.zdobyte.append(nazwa_z_pliku)
                st.rerun()
            elif not checked and nazwa_z_pliku in st.session_state.zdobyte:
                st.session_state.zdobyte.remove(nazwa_z_pliku)
                st.rerun()

except Exception as e:
    st.error(f"Błąd danych: {e}")
