import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from opcua import Client

# 🌟 Configuration de la page Streamlit
st.set_page_config(page_title="Dashboard OPC UA", page_icon="📡", layout="wide")

# Adresse du serveur OPC UA
OPC_SERVER_URL = "opc.tcp://135.236.107.162:4840"

# Fonction pour récupérer les données OPC UA
def get_opcua_data():
    with Client(OPC_SERVER_URL) as client:
        fio_msg = client.get_node("ns=1;s=FIO-msg").get_value()
        fio_humidity = client.get_node("ns=1;s=FIO-humidity").get_value()
        fio_pressure = client.get_node("ns=1;s=FIO-pressure").get_value()
        fio_temperature = client.get_node("ns=1;s=FIO-temperature").get_value()
        fio_status = client.get_node("ns=1;s=FIO-status").get_value()

    return {
        "FIO-msg": fio_msg,
        "FIO-humidity": fio_humidity,
        "FIO-pressure": fio_pressure,
        "FIO-temperature": fio_temperature,
        "FIO-status": fio_status,
    }

# 📈 Stockage des données pour les graphiques
if "data_history" not in st.session_state:
    st.session_state.data_history = pd.DataFrame(columns=["Timestamp", "FIO-humidity", "FIO-pressure", "FIO-temperature"])

# 📊 Interface utilisateur
st.title("📡 Dashboard OPC UA")

if st.button("🔄 Actualiser les données OPC UA"):
    data = get_opcua_data()

    # Ajout aux données historiques
    new_data = pd.DataFrame({
        "Timestamp": [pd.Timestamp.now()],
        "FIO-humidity": [data["FIO-humidity"]],
        "FIO-pressure": [data["FIO-pressure"]],
        "FIO-temperature": [data["FIO-temperature"]],
    })
    st.session_state.data_history = pd.concat([st.session_state.data_history, new_data], ignore_index=True)

    # 🎯 Affichage des métriques
    st.markdown("### 📊 Données en temps réel")
    col1, col2 = st.columns(2)
    col1.metric("💧 Humidité (%)", f"{data['FIO-humidity']:.2f}%")
    col1.metric("📏 Pression (hPa)", f"{data['FIO-pressure']:.2f}")
    col2.metric("🌡️ Température (°C)", f"{data['FIO-temperature']:.2f}")
    col2.metric("🔘 Statut", "🟢 ON" if data["FIO-status"] else "🔴 OFF")

    # 📢 Affichage du message
    st.write(f"**📜 Message :** {data['FIO-msg']}")

# 📈 Affichage des graphiques
if not st.session_state.data_history.empty:
    st.markdown("### 📊 Visualisation des données")

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(st.session_state.data_history["Timestamp"], st.session_state.data_history["FIO-temperature"], marker='o', linestyle='-', linewidth=2, label="Température (°C)")
    ax.plot(st.session_state.data_history["Timestamp"], st.session_state.data_history["FIO-humidity"], marker='x', linestyle='--', linewidth=2, label="Humidité (%)")
    ax.set_title("Évolution Température et Humidité", fontsize=16, fontweight='bold')
    ax.set_xlabel("Temps", fontsize=14)
    ax.set_ylabel("Valeur", fontsize=14)
    ax.legend()
    ax.grid(True, linestyle='--', alpha=0.7)
    st.pyplot(fig)

    fig2, ax2 = plt.subplots(figsize=(10, 5))
    ax2.plot(st.session_state.data_history["Timestamp"], st.session_state.data_history["FIO-pressure"], marker='s', linestyle='-', color='purple', linewidth=2, label="Pression (hPa)")
    ax2.set_title("Évolution Pression", fontsize=16, fontweight='bold')
    ax2.set_xlabel("Temps", fontsize=14)
    ax2.set_ylabel("Pression (hPa)", fontsize=14)
    ax2.legend()
    ax2.grid(True, linestyle='--', alpha=0.7)
    st.pyplot(fig2)
