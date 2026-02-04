import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Konfiguracja strony
st.set_page_config(page_title="TopTracker - Korona Gór Polski", page_icon="🏔️")

# Nagłówek aplikacji
st.title("🏔️ Witaj w TopTracker")

# Połączenie z Google Sheets
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    # ttl=0 pozwala widzieć zmiany natychmiast po kliknięciu
    all_data = conn.read(ttl=0)
except Exception as e:
    st.error("Błąd połączenia. Sprawdź, czy dodałeś link do Arkusza w 'Secrets'!")
    st.stop()

# Pobieranie listy szczytów z Twojego pliku CSV (z uwzględnieniem średników)
@st.cache_data
def load_peaks():
    # Dodano sep=";", aby poprawnie czytać Twój plik
    return pd.read_csv("dane.csv", sep=";")

try:
    df_peaks = load_peaks()
except Exception as e:
    st.error("Błąd ładowania pliku dane.csv. Sprawdź, czy używasz średników jako separatorów.")
    st.stop()

# Logowanie użytkownika
if 'user_id' not in st.session_state:
    st.subheader("Podaj swój Nick, aby wejść:")
    nick = st.text_input("Nick")
    if st.button("Zaloguj"):
        if nick:
            st.session_state.user_id = nick
            st.rerun()
        else:
            st.warning("Musisz podać nick!")
    st.stop()

# Interfejs po zalogowaniu
tab1, tab2 = st.tabs(["⛰️ Twoje Szczyty", "🏆 Ranking"])

with tab1:
    st.write(f"Zalogowany jako: **{st.session_state.user_id}**")
    
    # Sprawdzanie, co użytkownik już zdobył
    if not all_data.empty and 'Użytkownik' in all_data.columns:
        user_peaks = all_data[all_data['Użytkownik'] == st.session_state.user_id]['Szczyt'].tolist()
    else:
        user_peaks = []
    
    progress = len(user_peaks)
    st.write(f"Zaliczone: **{progress} / {len(df_peaks)}**")
    st.progress(progress / len(df_peaks) if len(df_peaks) > 0 else 0)
    
    st.divider()

    # Wyświetlanie listy szczytów z Twojego CSV
    for index, row in df_peaks.iterrows():
        peak_full = row['Szczyt']
        # Wyświetlamy tylko nazwę przed nawiasem dla czytelności
        short_name = str(peak_full).split(' w ')[0] if ' w ' in str(peak_full) else str(peak_full)
        is_done = peak_full in user_peaks
        
        # Obsługa zaznaczania szczytów
        if st.checkbox(f"📍 {short_name}", value=is_done, key=f"peak_{index}"):
            if not is_done:
                new_row = pd.DataFrame([{"Użytkownik": st.session_state.user_id, "Szczyt": peak_full}])
                updated_df = pd.concat([all_data, new_row], ignore_index=True)
                conn.update(data=updated_df)
                st.rerun()
        else:
            if is_done:
                # Jeśli użytkownik odznaczy szczyt
                updated_df = all_data[~((all_data['Użytkownik'] == st.session_state.user_id) & (all_data['Szczyt'] == peak_full))]
                conn.update(data=updated_df)
                st.rerun()

with tab2:
    st.subheader("🏆 Globalny Ranking")
    if not all_data.empty and 'Użytkownik' in all_data.columns:
        ranking = all_data['Użytkownik'].value_counts().reset_index()
        ranking.columns = ['Wędrowiec', 'Liczba Szczytów']
        st.table(ranking)
    else:
        st.info("Ranking jest jeszcze pusty. Bądź pierwszy!")

# Wylogowanie
if st.sidebar.button("Wyloguj"):
    del st.session_state.user_id
    st.rerun()
