import streamlit as st
import random
import pandas as pd
import numpy as np
import time

# Titre de l'application
st.title("TFE AGNABER CHAHID : OPCUA")

# Création de variables aléatoires pour démo
var_numeric_1 = random.randint(0, 100)
var_numeric_2 = random.uniform(0, 50)
var_numeric_3 = random.randint(200, 400)
var_text = random.choice(["Normal", "Attention", "Erreur", "Maintenance"])
var_bool = random.choice([True, False])

# Affichage des variables dans des cases
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Variable 1", var_numeric_1)
col2.metric("Variable 2", f"{var_numeric_2:.2f}")
col3.metric("Variable 3", var_numeric_3)
col4.metric("État", var_text)

# Affichage personnalisé du booléen
status_color = "green" if var_bool else "red"
status_label = "ON" if var_bool else "OFF"
col5.markdown(f"<h2 style='color:{status_color};text-align:center;'>{status_label}</h2>", unsafe_allow_html=True)

# Génération de données pour graphiques
chart_data1 = pd.DataFrame(
    np.random.randn(20, 1),
    columns=["Variable Numérique"]
)

chart_data2 = pd.DataFrame({
    'État': np.random.choice(["Normal", "Attention", "Erreur", "Maintenance"], 100),
    'Valeurs': np.random.randint(0, 100, 100)
})

# Affichage des graphiques
st.subheader("Graphique Variable Numérique")
st.line_chart(chart_data1)

st.subheader("Graphique État")
st.bar_chart(chart_data2.groupby('État').mean())
