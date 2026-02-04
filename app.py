import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="TopTracker KGP", page_icon="🏔️")
st.title("🏔️ TopTracker KGP")

# Łączymy się
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    all_data = conn.read(ttl=0)
except Exception as e:
    st.error(f"Problem z połączeniem: {e}")
    st.stop()

# Czytamy listę gór (sep=";" bo tak masz w CSV)
@st.cache_data
def load_peaks():
    return pd.read_csv("dane.csv", sep=";")

df_peaks = load_peaks()

# Logowanie
if 'user_id' not in st.session_state:
    nick = st.text_input("Twój Nick:")
    if st.button("Zaloguj") and nick:
        st.session_state.user_id = nick
        st.rerun()
    st.stop()

# Przygotowanie danych (jeśli arkusz jest pusty lub ma błąd)
if all_data is None or not isinstance(all_data, pd.DataFrame) or all_data.empty:
    all_data = pd.DataFrame(columns=['Użytkownik', 'Szczyt'])

user_peaks = all_data[all_data['Użytkownik'] == st.session_state.user_id]['Szczyt'].tolist()

st.write(f"Witaj **{st.session_state.user_id}**! Zaliczono: {len(user_peaks)}/28")

# Lista szczytów
for idx, row in df_peaks.iterrows():
    peak = row['Szczyt']
    is_done = peak in user_peaks
    
    if st.checkbox(f"📍 {peak}", value=is_done, key=f"p{idx}"):
        if not is_done:
            # Tworzymy nowy wiersz i wysyłamy
            new_row = pd.DataFrame([{"Użytkownik": st.session_state.user_id, "Szczyt": peak}])
            updated = pd.concat([all_data, new_row], ignore_index=True)
            try:
                conn.update(data=updated)
                st.rerun()
            except Exception as e:
                st.error("BŁĄD ZAPISU! Sprawdź czy w Arkuszu Google ustawiłeś rolę EDYTOR!")
                st.stop()
