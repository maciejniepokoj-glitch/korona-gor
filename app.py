import streamlit as st
import pandas as pd

st.set_page_config(page_title="Korona Gór Polski", page_icon="🏔️")

st.title("🏔️ Moja Korona Gór Polski")

@st.cache_data
def load_data():
    # Próbujemy odczytać plik z automatycznym wykrywaniem separatora (przecinek lub średnik)
    try:
        df = pd.read_csv('dane.csv', sep=None, engine='python', encoding='utf-8')
    except:
        df = pd.read_csv('dane.csv', sep=None, engine='python', encoding='cp1250')
    return df

try:
    df = load_data()
    
    # Sprawdzamy czy kolumna 'Szczyt' istnieje (usuwamy spacje z nazw kolumn dla pewności)
    df.columns = df.columns.str.strip()
    
    if 'Szczyt' not in df.columns:
        st.error(f"Nie znaleziono kolumny 'Szczyt'. Dostępne kolumny to: {list(df.columns)}")
        st.info("Otwórz plik CSV w notatniku i upewnij się, że pierwszy wiersz zawiera nazwę Szczyt")
    else:
        # Logika zdobywania szczytów
        if 'zdobyte' not in st.session_state:
            st.session_state.zdobyte = []

        # Pasek postępu
        procent = len(st.session_state.zdobyte) / len(df)
        st.metric("Twój wynik", f"{len(st.session_state.zdobyte)} / {len(df)}")
        st.progress(procent)

        # Lista szczytów
        for index, row in df.iterrows():
            nazwa_szczytu = row['Szczyt']
            wysokosc = row['Wysokość'] if 'Wysokość' in df.columns else ""
            
            label = f"{nazwa_szczytu} ({wysokosc} m n.p.m.)"
            
            # Checkbox
            checked = st.checkbox(label, key=f"check_{index}")
            if checked:
                if nazwa_szczytu not in st.session_state.zdobyte:
                    st.session_state.zdobyte.append(nazwa_szczytu)

except Exception as e:
    st.error(f"Problem z plikiem: {e}")
