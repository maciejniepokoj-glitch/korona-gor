import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Konfiguracja strony
st.set_page_config(page_title="TopTracker - KGP", page_icon="🏔️")

st.title("🏔️ Witaj w TopTracker")

# Połączenie z Google Sheets
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    # ttl=0 zapewnia odświeżanie danych na bieżąco
    all_data = conn.read(ttl=0)
except Exception:
    st.error("Błąd połączenia z bazą. Sprawdź 'Secrets'!")
    st.stop()

# Pobieranie listy szczytów (uwzględniamy Twoje średniki)
@st.cache_data
def load_peaks():
    return pd.read_csv("dane.csv", sep=";")

df_peaks = load_peaks()

# Logowanie
if 'user_id' not in st.session_state:
    nick = st.text_input("Podaj swój Nick, aby wejść:")
    if st.button("Zaloguj"):
        if nick:
            st.session_state.user_id = nick
            st.rerun()
        else:
            st.warning("Wpisz nick!")
    st.stop()

tab1, tab2 = st.tabs(["⛰️ Twoje Szczyty", "🏆 Ranking"])

with tab1:
    st.write(f"Wędrowiec: **{st.session_state.user_id}**")
    
    # Bezpieczne sprawdzanie zdobytych szczytów
    if not all_data.empty and 'Użytkownik' in all_data.columns:
        user_peaks = all_data[all_data['Użytkownik'] == st.session_state.user_id]['Szczyt'].tolist()
    else:
        user_peaks = []
        # Jeśli arkusz jest całkiem pusty, tworzymy ramkę danych z kolumnami
        all_data = pd.DataFrame(columns=['Użytkownik', 'Szczyt'])
    
    st.write(f"Zaliczono: **{len(user_peaks)} / {len(df_peaks)}**")
    st.progress(len(user_peaks) / len(df_peaks) if len(df_peaks) > 0 else 0)
    st.divider()

    # Wyświetlanie listy z checkboxami
    for index, row in df_peaks.iterrows():
        peak_full = row['Szczyt']
        is_done = peak_full in user_peaks
        
        if st.checkbox(f"📍 {peak_full}", value=is_done, key=f"p_{index}"):
            if not is_done:
                # Dodawanie szczytu do arkusza
                new_row = pd.DataFrame([{"Użytkownik": st.session_state.user_id, "Szczyt": peak_full}])
                updated_df = pd.concat([all_data, new_row], ignore_index=True)
                conn.update(data=updated_df)
                st.rerun()
        else:
            if is_done:
                # Usuwanie szczytu z arkusza
                updated_df = all_data[~((all_data['Użytkownik'] == st.session_state.user_id) & (all_data['Szczyt'] == peak_full))]
                conn.update(data=updated_df)
                st.rerun()

with tab2:
    st.subheader("🏆 Ranking")
    if not all_data.empty and 'Użytkownik' in all_data.columns:
        ranking = all_data['Użytkownik'].value_counts().reset_index()
        ranking.columns = ['Wędrowiec', 'Szczyty']
        st.table(ranking)
    else:
        st.info("Ranking jest pusty.")
