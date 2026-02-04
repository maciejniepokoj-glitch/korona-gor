import streamlit as st
import pandas as pd

# 1. Konfiguracja "Fancy" - szeroki układ i ciemny motyw
st.set_page_config(
    page_title="TopTracker | KGP",
    page_icon="🏔️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Stylizacja CSS dla lepszego wyglądu
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMetric { background-color: #161b22; padding: 15px; border-radius: 10px; border: 1px solid #30363d; }
    .stCheckbox { background-color: #161b22; padding: 10px; border-radius: 5px; margin-bottom: 5px; border: 1px solid #21262d; }
    .stProgress > div > div > div > div { background-image: linear-gradient(to right, #4facfe 0%, #00f2fe 100%); }
    </style>
    """, unsafe_allow_html=True)

# 2. Wczytywanie danych z Twojego CSV
@st.cache_data
def load_peaks():
    df = pd.read_csv("dane.csv", sep=";")
    return df.dropna(subset=['Szczyt'])

df_peaks = load_peaks()
total_peaks = len(df_peaks)

# 3. Zarządzanie postępem (Session State)
if 'zaliczone' not in st.session_state:
    st.session_state.zaliczone = []

# Nagłówek
st.title("🏔️ Korona Gór Polski - Twój Progress")
st.markdown("---")

# 4. Sekcja Statystyk (Dashboard)
progress_count = len(st.session_state.zaliczone)
progress_percent = int((progress_count / total_peaks) * 100) if total_peaks > 0 else 0

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Zdobyte Szczyty", f"{progress_count} / {total_peaks}")
with col2:
    st.metric("
