import streamlit as st
import pandas as pd

# 1. Konfiguracja strony
st.set_page_config(page_title="TopTracker KGP", page_icon="🏔️", layout="centered")

# 2. Stylizacja CSS - imitacja Twojego zdjęcia (Dashboard + Kafelki)
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    
    /* Okrągły Dashboard (imitacja) */
    .circle-stat {
        border: 8px solid #00d4ff;
        border-radius: 50%;
        width: 150px;
        height: 150px;
        margin: 0 auto;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        color: white;
        box-shadow: 0 0 20px rgba(0,212,255,0.3);
    }

    /* Karty szczytów - Poziome (obrazek lewo, tekst prawo) */
    .mountain-card {
        background-color: #1e2130;
        border-radius: 15px;
        padding: 10px;
        display: flex;
        align-items: center;
        margin-bottom: 10px;
    }
    
    /* Napisy wewnątrz kafelka */
    .mountain-info { color: #cfd0d6; font-size: 12px; margin-left: 15px; flex-grow: 1; }
    .mountain-title { color: white; font-weight: bold; font-size: 16px; margin-bottom: 2px; }

    /* Checkboxy stylizowane na ikony zaliczenia */
    .stCheckbox { margin-top: 0px; }
    
    h1, h2, h3 { color: white !important; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# 3. Baza zdjęć (Miniaturki)
foto_url = {
    "rysy": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d1/Rysy_od_morskiego_oka.jpg/200px-Rysy_od_morskiego_oka.jpg",
    "babia": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/17/Babia_G%C3%B3ra_widok_z_poudnia.jpg/200px-Babia_G%C3%B3ra_widok_z_poudnia.jpg",
    "śnieżka": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a1/Sniezka_z_oddali.jpg/200px-Sniezka_z_oddali.jpg",
    "śnieżnik": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e3/%C5%9Anie%C5%BCnik_K%C5%82odzki_S01.jpg/200px-%C5%9Anie%C5%BCnik_K%C5%82odzki_S01.jpg",
    "tarnica": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/af/Tarnica_Bieszczady.jpg/200px-Tarnica_Bieszczady.jpg",
    "turbacz": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/00/Turbacz_szczyt.jpg/200px-Turbacz_szczyt.jpg"
}
DEF_IMG = "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?q=80&w=200"

@st.cache_data
def load_data():
    try:
        df = pd.read_csv('dane.csv', sep=None, engine='python', encoding='utf-8-sig')
    except:
        df = pd.read_csv('dane.csv', sep=None, engine='python', encoding='cp1250')
    df = df.dropna(how='all')
    df = df[df.iloc[:, 0].notna()]
    return df

try:
    df = load_data()
    st.markdown("<h3>🏔️ TopTracker KGP</h3>", unsafe_allow_html=True)
    
    if 'zdobyte' not in st.session_state:
        st.session_state.zdobyte = []

    # --- OKRĄGŁY DASHBOARD ---
    zdobyte_n = len(st.session_state.zdobyte)
    razem_n = len(df)
    
    st.markdown(f"""
        <div class="circle-stat">
            <div style="font-size: 10px;">ZDOBYTE:</div>
            <div style="font-size: 28px; font-weight: bold;">{zdobyte_n}</div>
            <div style="font-size: 12px; color: #00d4ff;">z {razem_n}</div>
        </div>
    """, unsafe_allow_html=True)

    st.write("##")

    # --- ZAKŁADKI (Jak na obrazku) ---
    tab1, tab2 = st.tabs(["Twoje Szczyty", "Ranking Ogólny"])

    with tab1:
        for index, row in df.iterrows():
            nazwa_full = str(row.iloc[0]).strip()
            nazwa_low = nazwa_full.lower()
            
            # Kontener na kafelek (zdjęcie + tekst + checkbox)
            with st.container():
                col_img, col_txt, col_check = st.columns([1, 2, 0.5])
                
                # 1. Zdjęcie (Miniaturka)
                url = DEF_IMG
                for k, v in foto_url.items():
                    if k in nazwa_low: url = v; break
                col_img.image(url, use_container_width=True)
                
                # 2. Informacje
                label_name = nazwa_full.split(" w ")[0]
                col_txt.markdown(f"""
                    <div style="margin-top: 5px;">
                        <div class="mountain-title">{label_name}</div>
                        <div style="color: #888; font-size: 12px;">Polska • KGP</div>
                    </div>
                """, unsafe_allow_html=True)
                
                # 3. Checkbox (Odznaczone!)
                if col_check.checkbox("", key=f"kgp_{index}", value=(nazwa_full in st.session_state.zdobyte)):
                    if nazwa_full not in st.session_state.zdobyte:
                        st.session_state.zdobyte.append(nazwa_full)
                        st.rerun()
                else:
                    if nazwa_full in st.session_state.zdobyte:
                        st.session_state.zdobyte.remove(nazwa_full)
                        st.rerun()
                st.markdown("<hr style='margin: 10px 0; border-color: #333;'>", unsafe_allow_html=True)

except Exception as e:
    st.error(f"Błąd: {e}")
