import streamlit as st
import pandas as pd

# 1. Konfiguracja "Fancy" - Szeroki układ i ikona góry
st.set_page_config(
    page_title="KGP | Personal Tracker",
    page_icon="🏔️",
    layout="wide"
)

# Stylizacja CSS dla efektu premium
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    div[data-testid="stMetricValue"] { color: #00f2fe; font-size: 36px; }
    .stProgress > div > div > div > div { background-image: linear-gradient(to right, #4facfe 0%, #00f2fe 100%); }
    div[data-testid="stMetric"] { background-color: #1c2128; padding: 20px; border-radius: 15px; border: 1px solid #30363d; }
    </style>
    """, unsafe_allow_html=True)

# 2. Wczytywanie danych z Twojego pliku
@st.cache_data
def load_peaks():
    try:
        # Używamy separatora średnik (;) zgodnie z Twoim plikiem
        df = pd.read_csv("dane.csv", sep=";")
        return df.dropna(subset=['Szczyt'])
    except Exception:
        return pd.DataFrame(columns=['Szczyt', 'Wysokość mnp'])

df_peaks = load_peaks()
total_peaks = len(df_peaks)

# 3. Zarządzanie postępem (Session State)
if 'zaliczone' not in st.session_state:
    st.session_state.zaliczone = []

# Nagłówek aplikacji
st.title("🏔️ Twoja Korona Gór Polski")
st.write("Zaznaczaj zdobyte szczyty i obserwuj swój postęp.")

# 4. Sekcja Statystyk (Dashboard z Procentami)
progress_count = len(st.session_state.zaliczone)
progress_percent = int((progress_count / total_peaks) * 100) if total_peaks > 0 else 0

# Wyświetlanie metryk w rzędzie
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Zdobyte Szczyty", f"{progress_count} / {total_peaks}")
with col2:
    st.metric("Postęp", f"{progress_percent}%")
with col3:
    st.metric("Pozostało", f"{total_peaks - progress_count}")

# Pasek Postępu
st.write(f"### Całkowite ukończenie: {progress_percent}%")
st.progress(progress_count / total_peaks if total_peaks > 0 else 0)

st.divider()

# 5. Lista Szczytów w dwóch kolumnach
st.subheader("📍 Twoja lista kontrolna")
left_col, right_col = st.columns(2)

# Dzielimy listę na pół
mid_point = (total_peaks + 1) // 2

for index, row in df_peaks.iterrows():
    peak_name = row['Szczyt']
    h = row['Wysokość mnp']
    
    # Wybór kolumny (lewa lub prawa)
    target_col = left_col if index < mid_point else right_col
    
    with target_col:
        is_checked = peak_name in st.session_state.zaliczone
        
        # Checkbox ze stanem
        if st.checkbox(f"**{peak_name}** — {h} m n.p.m.", value=is_checked, key=f"peak_{index}"):
            if peak_name not in st.session_state.zaliczone:
                st.session_state.zaliczone.append(peak_name)
                st.rerun()
        else:
            if peak_name in st.session_state.zaliczone:
                st.session_state.zaliczone.remove(peak_name)
                st.rerun()

# Sidebar z opcjami
with st.sidebar:
    st.header("Opcje")
    if st.button("Resetuj wszystkie postępy"):
        st.session_state.zaliczone = []
        st.rerun()
    st.divider()
    # Naprawiona linia 94:
    st.info("Dane są przechowywane w pamięci sesji Twojej przeglądarki.")
