import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection # Biblioteka do obsługi bazy

# 1. Konfiguracja i Stylizacja Premium
st.set_page_config(page_title="TopTracker Ranking", page_icon="🏆", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] {
        background-color: #1e2130; border-radius: 10px; padding: 10px 20px; color: white;
    }
    .user-card {
        background: #1e2130; padding: 15px; border-radius: 15px;
        border-left: 5px solid #00d4ff; margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Połączenie z Bazą Danych (Google Sheets)
conn = st.connection("gsheets", type=GSheetsConnection)

def get_data():
    return conn.read(ttl="1s") # Odczyt danych w czasie rzeczywistym

# 3. Logowanie / Profil (Bezpieczeństwo)
if 'user_id' not in st.session_state:
    st.markdown("### 🏔️ Witaj w TopTracker!")
    u_name = st.text_input("Podaj swój unikalny Nick, aby zacząć:", placeholder="Np. GorskiWilk92")
    if st.button("Wejdź do gry"):
        if u_name:
            st.session_state.user_id = u_name
            st.rerun()
        else:
            st.warning("Musisz podać nick!")
    st.stop()

# 4. Główne Menu
tab1, tab2 = st.tabs(["⛰️ Moje Szczyty", "🏆 Ranking Ogólny"])

with tab1:
    st.title(f"Profil: {st.session_state.user_id}")
    
    # Ładowanie listy szczytów z Twojego pliku dane.csv
    df_peaks = pd.read_csv('dane.csv', sep=None, engine='python').dropna(how='all')
    
    # Pobieranie aktualnych postępów z bazy online
    all_progress = get_data()
    my_peaks = all_progress[all_progress['Użytkownik'] == st.session_state.user_id]['Szczyt'].tolist()

    st.write(f"Zaliczono: **{len(my_peaks)} / {len(df_peaks)}**")
    st.progress(len(my_peaks)/len(df_peaks))

    for index, row in df_peaks.iterrows():
        peak_name = str(row.iloc[0]).strip()
        is_done = peak_name in my_peaks
        
        # Checkbox wysyłający dane do bazy
        check = st.checkbox(f"📍 {peak_name}", value=is_done, key=f"p_{index}")
        
        if check and not is_done:
            # DODAJ DO BAZY (Tylko dla Twojego nicku)
            new_row = pd.DataFrame([{"Użytkownik": st.session_state.user_id, "Szczyt": peak_name}])
            updated_df = pd.concat([all_progress, new_row], ignore_index=True)
            conn.update(data=updated_df)
            st.rerun()
        elif not check and is_done:
            # USUŃ Z BAZY
            updated_df = all_progress[~((all_progress['Użytkownik'] == st.session_state.user_id) & (all_progress['Szczyt'] == peak_name))]
            conn.update(data=updated_df)
            st.rerun()

with tab2:
    st.title("Ranking Wędrowców")
    
    # Grupowanie wyników wszystkich użytkowników
    ranking = all_progress.groupby('Użytkownik').size().reset_index(name='Zdobyte')
    ranking = ranking.sort_values(by='Zdobyte', ascending=False)
    
    for i, row in ranking.iterrows():
        color = "#FFD700" if i == 0 else "#C0C0C0" if i == 1 else "#CD7F32" if i == 2 else "#ffffff"
        st.markdown(f"""
            <div class="user-card">
                <span style="color:{color}; font-weight:bold;">#{i+1}</span> 
                <b style="color:white; margin-left:15px;">{row['Użytkownik']}</b>
                <span style="float:right; color:#00d4ff;">{row['Zdobyte']} szczytów</span>
            </div>
        """, unsafe_allow_html=True)
