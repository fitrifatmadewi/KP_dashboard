import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard Prediksi Kuat Tekan & Setting Time", layout="wide")

# Header Utama
st.title("📊 Dashboard Prediksi Kuat Tekan & Setting Time")
st.markdown("---")

# Sidebar untuk input variabel
st.sidebar.header("🔢 Masukkan Nilai Variabel")
Tanggal = st.sidebar.date_input("📅 Tanggal")
Silo = st.sidebar.text_input("🏗️ Silo")
Peneliti = st.sidebar.text_input("👨‍🔬 Nama Peneliti")

st.sidebar.markdown("---")

# Input Variabel Kimia
cols = st.sidebar.columns(2)
SiO2 = cols[0].number_input("SiO2", value=0.0)
Al2O3 = cols[1].number_input("Al2O3", value=0.0)
Fe2O3 = cols[0].number_input("Fe2O3", value=0.0)
CaO = cols[1].number_input("CaO", value=0.0)
MgO = cols[0].number_input("MgO", value=0.0)
SO3 = cols[1].number_input("SO3", value=0.0)
C3S = cols[0].number_input("C3S", value=0.0)
C2S = cols[1].number_input("C2S", value=0.0)
C3A = cols[0].number_input("C3A", value=0.0)
C4AF = cols[1].number_input("C4AF", value=0.0)
FL = cols[0].number_input("FL", value=0.0)
LOI = cols[1].number_input("LOI", value=0.0)
Residu = cols[0].number_input("Residu", value=0.0)
Blaine = cols[1].number_input("Blaine", value=0.0)
Insoluble = cols[0].number_input("Insoluble", value=0.0)
Na2O = cols[1].number_input("Na2O", value=0.0)
K2O = cols[0].number_input("K2O", value=0.0)

# Hitung regresi manual
kuat_tekan_1d = 10 + (1.5 * SiO2) - (2.3 * Al2O3) + (0.8 * Fe2O3)
kuat_tekan_3d = 12 + (1.8 * SiO2) - (1.5 * Al2O3) + (1.2 * Fe2O3)
kuat_tekan_7d = 15 + (2.0 * SiO2) - (1.2 * Al2O3) + (1.5 * Fe2O3)
kuat_tekan_28d = 20 + (2.5 * SiO2) - (1.0 * Al2O3) + (2.0 * Fe2O3)
setting_time_awal = 20 + (2.5 * SiO2) - (1.0 * Al2O3) + (2.0 * Fe2O3)
setting_time_akhir = 20 + (2.5 * SiO2) - (1.0 * Al2O3) + (2.0 * Fe2O3)

# Inisialisasi session state jika belum ada
if "data_list" not in st.session_state:
    st.session_state.data_list = []

# Simpan Data
if st.sidebar.button("Simpan Data"):
    st.session_state.data_list.append([Tanggal, Silo, Peneliti, kuat_tekan_1d, kuat_tekan_3d, kuat_tekan_7d, kuat_tekan_28d, setting_time_awal, setting_time_akhir])

# Tabs
tabs = st.tabs(["📊 Prediksi", "📋 Data Tersimpan", "📈 Analisis Deskriptif", "📊 Visualisasi Data"])

with tabs[0]:
    st.subheader("📌 Hasil Prediksi")
    cols_pred = st.columns(2)
    cols_pred[0].metric(label="🧪 Kuat Tekan 1 Hari", value=f"{kuat_tekan_1d:.2f} MPa")
    cols_pred[1].metric(label="🧪 Kuat Tekan 3 Hari", value=f"{kuat_tekan_3d:.2f} MPa")
    cols_pred[0].metric(label="🧪 Kuat Tekan 7 Hari", value=f"{kuat_tekan_7d:.2f} MPa")
    cols_pred[1].metric(label="🧪 Kuat Tekan 28 Hari", value=f"{kuat_tekan_28d:.2f} MPa")
    cols_pred[0].metric(label="🧪 Setting Time Awal", value=f"{setting_time_awal:.2f} Menit")
    cols_pred[1].metric(label="🧪 Setting Time Akhir", value=f"{setting_time_akhir:.2f} Menit")

with tabs[1]:
    st.subheader("📋 Data yang Telah Disimpan")
    df = pd.DataFrame(st.session_state.data_list, columns=["Tanggal", "Silo", "Peneliti", "Kuat Tekan 1D", "Kuat Tekan 3D", "Kuat Tekan 7D", "Kuat Tekan 28D", "Setting Time Awal", "Setting Time Akhir"])
    st.dataframe(df)

with tabs[2]:
    st.subheader("📈 Analisis Deskriptif")
    st.write(df.describe())

with tabs[3]:
    st.subheader("📊 Visualisasi Data")
    if not df.empty:
        fig1 = px.bar(df, x="Tanggal", y=["Setting Time Awal", "Setting Time Akhir"], barmode='group', title="Setting Time Awal dan Akhir")
        st.plotly_chart(fig1)
        
        fig2 = px.line(df, x="Tanggal", y=["Kuat Tekan 1D", "Kuat Tekan 3D", "Kuat Tekan 7D", "Kuat Tekan 28D"], markers=True, title="Tren Kuat Tekan")
        st.plotly_chart(fig2)
