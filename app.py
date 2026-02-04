import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="TopTracker KGP", page_icon="🏔️")
st.title("🏔️ Witaj w TopTracker")

# Połączenie z bazą
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    all_data = conn.read(ttl=0)
except Exception:
    st.error("Błąd połączenia. Sprawdź 'Secrets'!")
    st.stop()

# Czytanie listy gór (średniki!)
@st.cache_data
def load_peaks():
    return pd.read_csv("dane.csv", sep=";")

df_peaks = load_peaks()

# Logowanie
if 'user_id' not in st.session_state:
    nick = st.text_input("Podaj swój Nick:")
    if st.button("Zaloguj") and nick:
        st.session_state.user_id = nick
        st.rerun()
    st.stop()

tab1, tab2 = st.tabs(["⛰️ Moje Szczyty", "🏆 Ranking"])

with tab1:
    # Jeśli arkusz jest pusty, stwórz tabelę w locie
    if all_data is None or all_data.empty:
        all_data = pd.DataFrame(columns=['Użytkownik', 'Szczyt'])
    
    user_peaks = all_data[all_data['Użytkownik'] == st.session_state.user_id]['Szczyt'].tolist()
    
    st.write(f"Zaliczono: **{len(user_peaks)} / {len(df_peaks)}**")
    st.divider()

    for idx, row in df_peaks.iterrows():
        peak = row['Szczyt']
        # Naprawa błędu zapisu
        if st.checkbox(f"📍 {peak}", value=(peak in user_peaks), key=f"p{idx}"):
            if peak not in user_peaks:
                new_row = pd.DataFrame([{"Użytkownik": st.session_state.user_id, "Szczyt": peak}])
                updated = pd.concat([all_data, new_row], ignore_index=True)
                conn.update(data=updated)
                st.rerun()
        elif peak in user_peaks:
            # Usuwanie, jeśli ktoś odznaczy
            updated = all_data[~((all_data['Użytkownik']==st.session_state.user_id) & (all_data['Szczyt']==peak))]
            conn.update(data=updated)
            st.rerun()

with tab2:
    if not all_data.empty:
        st.table(all_data['Użytkownik'].value_counts().reset_index(name='Suma'))
