import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="KGP Tracker", page_icon="🏔️")

# Nagłówek
st.title("🏔️ TopTracker KGP")

# Połączenie
conn = st.connection("gsheets", type=GSheetsConnection)

# Pobieranie listy gór (średniki!)
@st.cache_data
def load_peaks():
    return pd.read_csv("dane.csv", sep=";")

df_peaks = load_peaks()

# Pobieranie danych z Google Sheets
try:
    # ttl=0 wyłącza buforowanie, żeby widzieć zmiany od razu
    all_data = conn.read(ttl=0)
except:
    all_data = pd.DataFrame(columns=['Użytkownik', 'Szczyt'])

# Logowanie
if 'user_id' not in st.session_state:
    nick = st.text_input("Twój Nick:")
    if st.button("Zaloguj") and nick:
        st.session_state.user_id = nick
        st.rerun()
    st.stop()

# Interfejs
user_peaks = []
if not all_data.empty and 'Użytkownik' in all_data.columns:
    user_peaks = all_data[all_data['Użytkownik'] == st.session_state.user_id]['Szczyt'].tolist()

st.write(f"Witaj **{st.session_state.user_id}**! Zaliczono: {len(user_peaks)}/{len(df_peaks)}")

# Wyświetlanie listy
for idx, row in df_peaks.iterrows():
    peak = row['Szczyt']
    is_done = peak in user_peaks
    
    if st.checkbox(f"📍 {peak}", value=is_done, key=f"p{idx}"):
        if not is_done:
            new_row = pd.DataFrame([{"Użytkownik": st.session_state.user_id, "Szczyt": peak}])
            # Łączymy stare dane z nowymi
            updated = pd.concat([all_data, new_row], ignore_index=True)
            # Wymuszamy zapis do "Sheet1"
            conn.update(worksheet="Sheet1", data=updated)
            st.rerun()
    elif is_done:
        # Usuwanie jeśli ktoś odznaczy
        updated = all_data[~((all_data['Użytkownik'] == st.session_state.user_id) & (all_data['Szczyt'] == peak))]
        conn.update(worksheet="Sheet1", data=updated)
        st.rerun()
