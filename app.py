import streamlit as st
import pandas as pd

# Konfiguracja strony
st.set_page_config(page_title="Mój TopTracker", page_icon="⛰️")

st.title("🏔️ Moja Korona Gór Polski")

# 1. Wczytywanie Twoich danych (z uwzględnieniem średników)
@st.cache_data
def load_peaks():
    # Czytamy plik i usuwamy ewentualne puste wiersze na końcu
    df = pd.read_csv("dane.csv", sep=";")
    return df.dropna(subset=['Szczyt'])

try:
    df_peaks = load_peaks()
except Exception:
    st.error("Problem z plikiem dane.csv. Sprawdź, czy są w nim średniki!")
    st.stop()

# 2. Zarządzanie stanem (Twoje postępy w sesji)
if 'zaliczone' not in st.session_state:
    # Tutaj możesz wpisać na sztywno nazwy szczytów, które już masz zdobyte
    # np. st.session_state.zaliczone = ["Rysy w Tatrach", "Turbacz w Gorcach"]
    st.session_state.zaliczone = []

# 3. Interfejs i statystyki
progress = len(st.session_state.zaliczone)
total = len(df_peaks)

col1, col2 = st.columns(2)
col1.metric("Zdobyte", f"{progress} / {total}")
col2.metric("Do końca", f"{total - progress}")

st.progress(progress / total if total > 0 else 0)
st.divider()

# 4. Lista szczytów do klikania
st.subheader("Lista Twoich szczytów:")

for index, row in df_peaks.iterrows():
    peak_name = row['Szczyt']
    wysokosc = row['Wysokość mnp']
    
    # Sprawdzamy czy szczyt jest już na liście zaliczonych
    is_checked = peak_name in st.session_state.zaliczone
    
    # Checkbox dla każdego szczytu
    if st.checkbox(f"📍 {peak_name} ({wysokosc} m n.p.m.)", value=is_checked, key=f"peak_{index}"):
        if peak_name not in st.session_state.zaliczone:
            st.session_state.zaliczone.append(peak_name)
            st.rerun()
    else:
        if peak_name in st.session_state.zaliczone:
            st.session_state.zaliczone.remove(peak_name)
            st.rerun()

# Przycisk resetu
if st.sidebar.button("Resetuj wszystkie postępy"):
    st.session_state.zaliczone = []
    st.rerun()
