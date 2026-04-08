import streamlit as st
import pandas as pd
from pycaret.regression import load_model, predict_model

# Wczytanie zapisanego modelu
model = load_model('model_maratonu')

# Tytuł aplikacji
st.title("🏃 Kalkulator czasu maratonu")
st.write("Podaj swoje dane, a przewidzimy Twój czas na mecie!")

# Formularz dla użytkownika
plec = st.selectbox("Płeć", ["Mężczyzna", "Kobieta"])
wiek = st.number_input("Wiek", min_value=15, max_value=90, value=30)
minuty_5km = st.number_input("Twój czas na 5 km (minuty)", min_value=10, max_value=60, value=25)
sekundy_5km = st.number_input("Twój czas na 5 km (sekundy)", min_value=0, max_value=59, value=0)

# Przycisk
if st.button("Oblicz mój czas!"):
    # Przeliczamy dane
    czas_5km_s = minuty_5km * 60 + sekundy_5km
    tempo = (czas_5km_s / 5) / 60
    plec_numer = 0 if plec == "Mężczyzna" else 1

    # Tworzymy DataFrame dla modelu
    dane = pd.DataFrame({
        'plec': [plec_numer],
        'wiek': [float(wiek)],
        'tempo_5km': [tempo]
    })

    # Przewidywanie
    wynik = predict_model(model, data=dane)
    czas_s = wynik['prediction_label'][0]

    # Formatujemy wynik
    godziny = int(czas_s // 3600)
    minuty = int((czas_s % 3600) // 60)
    sekundy = int(czas_s % 60)

    st.success(f"⏱️ Przewidywany czas na mecie: **{godziny}h {minuty}min {sekundy}s**")