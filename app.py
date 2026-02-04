import streamlit as st
import pandas as pd

# 1. Konfiguracja strony
st.set_page_config(page_title="TopTracker KGP", page_icon="🏔️", layout="centered")

# 2. Stylizacja CSS - Efekt szklanych kafelków i okrągłych zdjęć
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    
    /* Okrągły licznik na górze */
    .circle-stat {
        border: 6px solid #00d4ff;
        border-radius: 50%;
        width: 140px;
        height: 140px;
        margin: 0 auto;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        background: radial-gradient(circle, #1e2130 0%, #0e1117 100%);
        box-shadow: 0 0 25px rgba(0,212,255,0.2);
    }

    /* Stylizacja pojedynczego wiersza (kafelka) */
    .mountain-row {
        background-color: #1e2130;
        border-radius: 20px;
        padding: 10px 15px;
        margin-bottom: 10px;
        border: 1px solid #2d3142;
    }
    
    /* Okrągłe zdjęcie */
    .stImage > img {
        border-radius: 50% !important;
        width: 60px !important;
        height: 60px !important;
        object-fit: cover;
        border: 2px solid #00d4ff;
    }

    .m-title { color: white; font-weight: bold; font-size: 16px; margin-bottom: 0px; }
    .m-desc { color: #888; font-size: 12px; }
    
    /* Ukrycie labeli checkboxa dla czystego wyglądu */
    .stCheckbox label { display: none; }
    
    hr { border-color: #2d3142; margin: 15px 0; }
    h3 { color: #00d4ff !important; letter-spacing: 1px; }
    </style>
    """, unsafe_allow_html=True)

# 3. Rozszerzona baza realnych zdjęć (Klucze dopasowane do Twojego pliku)
foto_url = {
    "rysy": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d1/Rysy_od_morskiego_oka.jpg/200px-Rysy_od_morskiego_oka.jpg",
    "babia": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/17/Babia_G%C3%B3ra_widok_z_poudnia.jpg/200px-Babia_G%C3%B3ra_widok_z_poudnia.jpg",
    "śnieżka": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a1/Sniezka_z_oddali.jpg/200px-Sniezka_z_oddali.jpg",
    "śnieżnik": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e3/%C5%9Anie%C5%BCnik_K%C5%82odzki_S01.jpg/200px-%C5%9Anie%C5%BCnik_K%C5%82odzki_S01.jpg",
    "tarnica": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/af/Tarnica_Bieszczady.jpg/200px-Tarnica_Bieszczady.jpg",
    "turbacz": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/00/Turbacz_szczyt.jpg/200px-Turbacz_szczyt.jpg",
    "radziejowa": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a2/Radziejowa_szczyt.jpg/200px-Radziejowa_szczyt.jpg",
    "skrzyczne": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/23/Skrzyczne_widok_z_poudnia.jpg/200px-Skrzyczne_widok_z_poudnia.jpg",
    "mogielica": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b3/Mogielica_widok_z_Jasienia.jpg/200px-Mogielica_widok_z_Jasienia.jpg",
    "wysoka kopa": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/df/Wysoka_Kopa_S01.jpg/200px-Wysoka_Kopa_S01.jpg",
    "rudawiec": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b8/Rudawiec_szczyt.jpg/200px-Rudawiec_szczyt.jpg",
    "orlica": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/77/Orlica_szczyt.jpg/200px-Orlica_szczyt.jpg",
    "wysoka": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a7/Wysokie_Ska%C5%82ki_Pieniny.jpg/200px-Wysokie_Ska%C5%82ki_Pieniny.jpg",
    "wielka sowa": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f6/Wielka_Sowa_wie%C5%BCa.jpg/200px-Wielka_Sowa_wie%C5%BCa.jpg",
    "lackowa": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/45/Lackowa_z_Ciechania.jpg/200px-Lackowa_z_Ciechania.jpg",
    "kowadło": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Kowad%C5%82o_szczyt.jpg/200px-Kowad%C5%82o_szczyt.jpg",
    "jagodna": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/be/Jagodna_szczyt.jpg/200px-Jagodna_szczyt.jpg",
    "skalnik": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Skalnik_szczyt.jpg/200px-Skalnik_szczyt.jpg",
    "waligóra": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3b/Walig%C3%B3ra_szczyt.jpg/200px-Walig%C3%B3ra_szczyt.jpg",
    "czupel": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/25/Czupel_widok_z_Magurki.jpg/200px-Czupel_widok_z_Magurki.jpg",
    "szczeliniec": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/aa/Szczeliniec_Wielki_S01.jpg/200px-Szczeliniec_Wielki_S01.jpg",
    "lubomir": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a6/Lubomir_szczyt.jpg/200px-Lubomir_szczyt.jpg",
    "biskupia": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f5/Biskupia_Kopa_wie%C5%BCa.jpg/200px-Biskupia_Kopa_wie%C5%BCa.jpg",
    "chełmiec": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/70/Che%C5%82miec_widok.jpg/200px-Che%C5%82miec_widok.jpg",
    "kłodzka góra": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0e/K%C5%82odzka_G%C3%B3ra_szczyt.jpg/200px-K%C5%82odzka_G%C3%B3ra_szczyt.jpg",
    "ślęża": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/22/%C5%9Al%C4%99%C5%BCa_widok.jpg/200px-%C5%9Al%C4%99%C5%BCa_widok.jpg",
    "łysica": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/07/%C5%81ysica_go%C5%82oborze.jpg/200px-%C5%81ysica_go%C5%82oborze.jpg"
}
DEF_IMG = "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?q=80&w=200"

@st.cache_data
def load_data():
    try:
        df = pd.read_csv('dane.csv', sep=None, engine='python', encoding='utf-8-sig')
    except:
        df = pd.read_csv('dane.csv', sep=None, engine='python', encoding='cp1250')
    return df.dropna(how='all')

try:
    df = load_data()
    st.markdown("<h3>🏔️ TopTracker KGP</h3>", unsafe_allow_html=True)
    
    if 'zdobyte' not in st.session_state:
        st.session_state.zdobyte = []

    # 4. OKRĄGŁY WYKRES POSTĘPU
    zdobyte_n = len(st.session_state.zdobyte)
    razem_n = len(df)
    procent = int((zdobyte_n / razem_n) * 100) if razem_n > 0 else 0
    
    st.markdown(f"""
        <div class="circle-stat">
            <div style="font-size: 28px; font-weight: bold; color: white;">{procent}%</div>
            <div style="font-size: 10px; color: #00d4ff; text-transform: uppercase;">Zrobione</div>
        </div>
    """, unsafe_allow_html=True)

    st.write("##")
    
    # 5. LISTA SZCZYTÓW
    st.markdown("<p style='text-align: center; color: #888;'>Twoja lista wyzwań</p>", unsafe_allow_html=True)

    for index, row in df.iterrows():
        nazwa_full = str(row.iloc[0]).strip()
        nazwa_low = nazwa_full.lower()
        
        # Kontener kafelka
        with st.container():
            col_img, col_txt, col_chk = st.columns([1, 4, 1])
            
            # Kolumna 1: Okrągłe zdjęcie
            url = DEF_IMG
            for k, v in foto_url.items():
                if k in nazwa_low:
                    url = v
                    break
            col_img.image(url)
            
            # Kolumna 2: Tekst
            clean_name = nazwa_full.split(" w ")[0]
            col_txt.markdown(f"""
                <div style="padding-top: 10px;">
                    <div class="m-title">{clean_name}</div>
                    <div class="m-desc">Polska • Korona Gór Polski</div>
                </div>
            """, unsafe_allow_html=True)
            
            # Kolumna 3: Checkbox
            with col_chk:
                st.write("##") # Obniżenie checkboxa
                checked = st.checkbox("", key=f"f_{index}", value=(nazwa_full in st.session_state.zdobyte))
                
                if checked and nazwa_full not in st.session_state.zdobyte:
                    st.session_state.zdobyte.append(nazwa_full)
                    st.rerun()
                elif not checked and nazwa_full in st.session_state.zdobyte:
                    st.session_state.zdobyte.remove(nazwa_full)
                    st.rerun()
            
            st.markdown("<div style='height: 5px;'></div>", unsafe_allow_html=True)

except Exception as e:
    st.error(f"Wystąpił błąd: {e}")
