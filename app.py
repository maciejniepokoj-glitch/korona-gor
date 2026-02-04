import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Konfiguracja strony
st.set_page_config(page_title="KGP Tracker", page_icon="🏔️")
st.title("🏔️ Witaj w TopTracker")

# 1. Połączenie z Google Sheets
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    # Odczyt danych (ttl=0 zapewnia brak opóźnień)
    all_data = conn.read(ttl=0)
except Exception:
    st.error("Błąd połączenia. Sprawdź, czy link do arkusza jest w Secrets!")
    st.stop()

# 2. Czytanie listy gór z Twojego pliku (separator średnik)
@st.cache_data
def load_peaks():
    return pd.read_csv("dane.csv", sep=";")

df_peaks = load_peaks()

# 3. Logowanie
if 'user_id' not in st.session_state:
    nick = st.text_input("Podaj swój Nick, aby wejść:")
    if st.button("Zaloguj"):
        if nick:
            st.session_state.user_id = nick
            st.rerun()
        else:
            st.warning("Musisz podać nick!")
    st.stop()

# 4. Przygotowanie danych użytkownika
# Jeśli arkusz jest pusty, tworzymy nową tabelę z kolumnami
if all_data is None or all_data.empty:
    all_data = pd.DataFrame(columns=['Użytkownik', 'Szczyt'])

# Sprawdzamy co zaliczył obecny użytkownik
user_peaks = all_data[all_data['Użytkownik'] == st.session_state.user_id]['Szczyt'].tolist()

# 5. Interfejs
tab1, tab2 = st.tabs(["⛰️ Twoje Szczyty", "🏆 Ranking"])

with tab1:
    st.write(f"Zalogowany jako: **{st.session_state.user_id}**")
    st.write(f"Zaliczono: **{len(user_peaks)} / {len(df_peaks)}**")
    st.divider()

    # Wyświetlanie listy checkboxów
    for index, row in df_peaks.iterrows():
        peak_name = row['Szczyt']
        is_done = peak_name in user_peaks
        
        # Zmiana stanu (zaznaczenie/odznaczenie)
        if st.checkbox(f"📍 {peak_name}", value=is_done, key=f"peak_{index}"):
            if not is_done:
                # DODAWANIE: Tworzymy nowy wiersz i wysyłamy całość
                new_row = pd.DataFrame([{"Użytkownik": st.session_state.user_id, "Szczyt": peak_name}])
                updated_df = pd.concat([all_data, new_row], ignore_index=True)
                conn.update(data=updated_df)
                st.rerun()
        else:
            if is_done:
                # USUWANIE: Filtrujemy dane bez tego szczytu i wysyłamy
                updated_df = all_data[~((all_data['Użytkownik'] == st.session_state.user_id) & (all_data['Szczyt'] == peak_name))]
                conn.update(data=updated_df)
                st.rerun()

with tab2:
    st.subheader("🏆 Globalny Ranking")
    if not all_data.empty:
        # Liczymy ile szczytów ma każdy użytkownik
        ranking = all_data['Użytkownik'].value_counts().reset_index()
        ranking.columns = ['Wędrowiec', 'Liczba Szczytów']
        st.table(ranking)
    else:
        st.info("Ranking jest pusty. Zaznacz swój pierwszy szczyt!")

# Sidebar z wylogowaniem
if st.sidebar.button("Wyloguj"):
    del st.session_state.user_id
    st.rerun()
