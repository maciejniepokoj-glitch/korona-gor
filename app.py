import streamlit as st
import pandas as pd

# 1. Konfiguracja i styl
st.set_page_config(page_title="Korona Gór Polski v2.0", page_icon="🏔️", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stCheckbox { background-color: #1e2130; padding: 15px; border-radius: 10px; margin-bottom: 20px; }
    .metric-card { background: linear-gradient(135deg, #00b4db, #0083b0); padding: 20px; border-radius: 20px; color: white; text-align: center; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# 2. Ładowanie danych
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

    # 3. Statystyki na górze
    zdobyte_n = len(st.session_state.zdobyte)
    razem_n = len(df)
    procent = int((zdobyte_n / razem_n) * 100) if razem_n > 0 else 0

    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"<div class='metric-card'><h3>ZDOBYTE</h3><h2>{zdobyte_n} / {razem_n}</h2></div>", unsafe_allow_html=True)
    with c2:
        st.markdown(f"<div class='metric-card'><h3>POSTĘP</h3><h2>{procent}%</h2></div>", unsafe_allow_html=True)

    st.write("---")

    # 4. BAZA ZDJĘĆ (Tutaj dopisujesz linki do zdjęć)
    foto_url = {
        "Rysy": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d1/Rysy_od_morskiego_oka.jpg/800px-Rysy_od_morskiego_oka.jpg",
        "Śnieżka": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a1/Sniezka_z_oddali.jpg/800px-Sniezka_z_oddali.jpg",
        "Babia Góra": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/17/Babia_G%C3%B3ra_widok_z_poudnia.jpg/800px-Babia_G%C3%B3ra_widok_z_poudnia.jpg",
        "Tarnica": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/af/Tarnica_Bieszczady.jpg/800px-Tarnica_Bieszczady.jpg"
    }

    # 5. GENEROWANIE KART (To jest to miejsce!)
    col1, col2 = st.columns(2)

    for index, row in df.iterrows():
        nazwa = row['Szczyt']
        wys = row['Wysokość mnp'] if 'Wysokość mnp' in df.columns else ""
        
        with (col1 if index % 2 == 0 else col2):
            # Wyświetlamy zdjęcie (jeśli nie ma w bazie, dajemy domyślne góry)
            url = foto_url.get(nazwa, "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?q=80&w=800")
            st.image(url, use_container_width=True)
            
            # Checkbox pod zdjęciem
            checked = st.checkbox(f"Zaliczono: {nazwa} ({wys}m)", key=f"btn_{index}", value=(nazwa in st.session_state.zdobyte))
            
            if checked and nazwa not in st.session_state.zdobyte:
                st.session_state.zdobyte.append(nazwa)
                st.rerun()
            elif not checked and nazwa in st.session_state.zdobyte:
                st.session_state.zdobyte.remove(nazwa)
                st.rerun()

except Exception as e:
    st.error(f"Wystąpił błąd: {e}")
