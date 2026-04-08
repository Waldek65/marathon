import os
import streamlit as st
import pandas as pd
from pycaret.regression import load_model, predict_model

# Ustawienie folderu roboczego
#os.chdir(r'C:\Users\w\Desktop\od_zera_do_ai\projekty\moduł 9 marathon')

# Wczytanie modelu
model = load_model('model_maratonu_10')

# ── Interfejs użytkownika ─────────────────────────────────────────
st.title("🏃 Kalkulator czasu maratonu (wersja dokładna)")
st.write("Podaj swoje dane z biegu – im więcej danych, tym dokładniejszy wynik!")

# Dane podstawowe
plec      = st.selectbox("Płeć", ["Mężczyzna", "Kobieta"])
wiek      = st.number_input("Wiek", min_value=15, max_value=90, value=30)

# Czas na 5 km
st.subheader("⏱️ Twój czas na 5 km")
min_5km = st.number_input("Minuty (5 km)", min_value=10, max_value=60, value=25)
sek_5km = st.number_input("Sekundy (5 km)", min_value=0, max_value=59, value=0)

# Czas na 10 km
st.subheader("⏱️ Twój czas na 10 km")
min_10km = st.number_input("Minuty (10 km)", min_value=20, max_value=120, value=52)
sek_10km = st.number_input("Sekundy (10 km)", min_value=0, max_value=59, value=0)

# ── Przycisk i obliczenie ─────────────────────────────────────────
if st.button("Oblicz mój czas!"):

    # Przeliczamy czasy na tempo (min/km)
    czas_5km_s  = min_5km * 60 + sek_5km
    czas_10km_s = min_10km * 60 + sek_10km
    tempo_5km   = (czas_5km_s / 5) / 60
    tempo_10km  = (czas_10km_s / 10) / 60
    spadek      = tempo_10km - tempo_5km
    plec_numer  = 0 if plec == "Mężczyzna" else 1

    # Walidacja: czas na 10 km musi być dłuższy niż na 5 km
    if czas_10km_s <= czas_5km_s:
        st.error("❌ Czas na 10 km musi być dłuższy niż czas na 5 km!")
    else:
        # Tworzymy DataFrame dla modelu
        dane = pd.DataFrame({
            'plec':         [float(plec_numer)],
            'wiek':         [float(wiek)],
            'tempo_5km':    [tempo_5km],
            'tempo_10km':   [tempo_10km],
            'spadek_tempa': [spadek]
        })

        # Przewidywanie
        wynik  = predict_model(model, data=dane)
        czas_s = wynik['prediction_label'][0]

        # Formatowanie wyniku
        godziny = int(czas_s // 3600)
        minuty  = int((czas_s % 3600) // 60)
        sekundy = int(czas_s % 60)

        st.success(f"⏱️ Przewidywany czas na mecie: **{godziny}h {minuty}min {sekundy}s**")

        # Dodatkowa informacja o tempie
        if spadek > 0.3:
            st.warning("⚠️ Twoje tempo wyraźnie spada – uwaga na drugą połowę trasy!")
        elif spadek < 0:
            st.info("💪 Świetnie! Przyspieszasz – to dobry znak!")
        else:
            st.info("👌 Twoje tempo jest bardzo równomierne – idealnie!")