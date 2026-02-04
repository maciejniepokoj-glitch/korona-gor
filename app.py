import streamlit as st
import pandas as pd

# Konfiguracja strony
st.set_page_config(page_title="Korona Gór Polski - Tracker", page_icon="🏔️", layout="wide")

# Stylizacja CSS dla lepszego wyglądu
st.markdown("""
    <style>
    .stProgress > div > div > div > div { background-color: #00d4ff; }
    .main { background-color: #0e1117; color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏔️ Korona Gór Polski - Twój Profil")

# Ładowanie danych
@st.cache_data
def load_data():
    df = pd.read_csv('dane.csv')
    return df

try:
    df = load_data()
    
    # --- PROFIL UŻYTKOWNIKA ---
    with st.sidebar:
        st.header("👤 Twój Profil")
        user_name = st.text_input("Twoje Imię/Nick", "Wędrowiec")
        st.write(f"Witaj, **{user_name}**!")
        st.divider()
        st.info("Twoje postępy są zapisywane w sesji przeglądarki.")

    # --- LOGIKA POSTĘPU ---
    st.subheader(f"Statystyki: {user_name}")
    
    # Tworzymy listę zdobytych szczytów (w wersji demo oparte o session_state)
    if 'acquired' not in st.session_state:
        st.session_state.acquired = []

    progress = len(st.session_state.acquired) / len(df)
    st.progress(progress)
    st.write(f"Zdobyłeś już **{len(st.session_state.acquired)}** z **{len(df)}** szczytów!")

    # --- LISTA SZCZYTÓW ---
    col1, col2 = st.columns(2)

    for index, row in df.iterrows():
        # Decydujemy w której kolumnie wyświetlić kartę
        target_col = col1 if index % 2 == 0 else col2
        
        with target_col:
            with st.expander(f"⛰️ {row['Szczyt']} ({row['Wysokość']} m n.p.m.)"):
                st.write(f"**Pasmo:** {row['Pasmo górskie']}")
                
                is_checked = row['Szczyt'] in st.session_state.acquired
                if st.checkbox("Zdobyty!", key=row['Szczyt'], value=is_checked):
                    if row['Szczyt'] not in st.session_state.acquired:
                        st.session_state.acquired.append(row['Szczyt'])
                        st.rerun()
                elif row['Szczyt'] in st.session_state.acquired:
                    st.session_state.acquired.remove(row['Szczyt'])
                    st.rerun()

    # --- PORÓWNYWANIE (DLA ZNAJOMYCH) ---
    st.divider()
    if st.button("🔗 Wygeneruj link do udostępnienia (Sim)"):
        st.success("Skopiowano link do Twojego profilu! (W pełnej wersji link zawierałby ID Twojej bazy danych)")

except Exception as e:
    st.error(f"Upewnij się, że plik CSV znajduje się w tym samym folderze co skrypt! Błąd: {e}")