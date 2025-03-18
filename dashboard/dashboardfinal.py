import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


# 🔧 **Konfigurasi Halaman** (Harus di paling atas)
st.set_page_config(page_title="Product Quality Assurance Dashboard", layout="wide")

# Tambahkan logo di bagian atas
st.markdown("<br>", unsafe_allow_html=True)  # Beri jarak ke bawah jika terpotong
st.image("https://raw.githubusercontent.com/fitrifatmadewi/KP_dashboard/main/dashboard/SIG_Logo.png", width=100)

# 🎨 Tambahkan Warna Latar Belakang Dashboard
# 🎨 CSS agar kompatibel dengan mode terang & gelap
st.markdown(
    """
    <style>
    :root {
        --primary-color: #d71920; /* Merah */
        --text-color: white; /* Warna teks di mode gelap */
        --bg-light: white; /* Latar belakang di mode terang */
        --bg-dark: #1e1e1e; /* Latar belakang di mode gelap */
        --shadow: rgba(0, 0, 0, 0.2);
    }
    @media (prefers-color-scheme: light) {
        body, .block-container {
            background-color: var(--bg-light);
            color: black;
        }
    }
    @media (prefers-color-scheme: dark) {
        body, .block-container {
            background-color: var(--bg-dark);
            color: var(--text-color);
        }
    }
    .block-container {
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0px 6px 15px var(--shadow);
        border-left: 8px solid var(--primary-color);
    }
    .stButton>button {
        background-color: var(--primary-color);
        color: white;
        font-size: 16px;
        border-radius: 8px;
        padding: 8px 16px;
        border: 2px solid black;
    }
    .stButton>button:hover {
        background-color: #a31518;
    }
    .stSelectbox, .stTextInput, .stNumberInput {
        border-radius: 8px;
        border: 2px solid black;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# 🎯 Header Utama
st.title("📊 Product Quality Assurance Dashboard")
st.caption("**Author:** Fitri Fatma Dewi (5003221031) | Devi Sagita Rachman (5003221172)")  
st.caption("Proyek Kerja Praktek – PT Semen Indonesia (Persero) Tbk | Institut Teknologi Sepuluh Nopember")  
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

# Hitung regresi manual (dari hasil PCR)
kuat_tekan_1d = 203.873 + (1.288 * SiO2) + (0.902 * Al2O3) + (- 5.521 * Fe2O3) + (4.162 * CaO) + (-2.728 * MgO) + (5.611 * SO3) + (0.842 * C3S) + (-0.014 * C2S) + (3.924 * C3A) + (5.720 * C4AF) + (0.936 * FL) + (-0.304 * LOI) + (-6.203 * Residu) + (7.664 * Blaine) + (-0.193 * Insoluble) + (0.657 * Na2O) + (1.533 * K2O)
kuat_tekan_3d = 355.191 + (-0.275 * SiO2) + (4.510 * Al2O3) + (-3.382 * Fe2O3) + (5.175 * CaO) + (-1.699 * MgO) + (-1.236 * SO3) + (2.581 * C3S) + (-1.634 * C2S) + (5.33 * C3A) + (-3.265 * C4AF) + (0.508 * FL) + (-1.759 * LOI) + (-3.025 * Residu) + (13.976* Blaine) + (-0.550 * Insoluble) + (0.119 * Na2O) + (2.178 * K2O)
kuat_tekan_7d = 430.582 + (1.176 * SiO2) + (1.138 * Al2O3) + (-3.165 * Fe2O3) + (4.831 * CaO) + (2.453 * MgO) + (-0.912 * SO3) + (2.422 * C3S) + (-0.648 * C2S) + (3.126 * C3A) + (-2.715 * C4AF) + (3.031 * FL) + (-3.831 * LOI) + (-0.306 * Residu) + (10.915* Blaine) + (-3.064 * Insoluble) + (2.155 * Na2O) + (-0.962 * K2O)
kuat_tekan_28d = 538.751 + (52.966 * SiO2) + (162.395 * Al2O3) + (-226.411 * Fe2O3) + (-24.526 * CaO) + (4.539 * MgO) + (3.757 * SO3) + (32.333 * C3S) + (-16.180 * C2S) + (-210.471 * C3A) + (97.881 * C4AF) + (0.613 * FL) + (-6.829 * LOI) + (0.995 * Residu) + (10.584* Blaine) + (-0.047 * Insoluble) + (0.659 * Na2O) + (-3.647 * K2O)
setting_time_awal = 97.442 + (0.997 * SiO2) + (-1.093 * Al2O3) + (0.478 * Fe2O3) + (0.760 * CaO) + (1.905 * MgO) + (-0.514 * SO3) + (-0.203 * C3S) + (0.548 * C2S) + (-1.010 * C3A) + (0.517 * C4AF) + (-2.730 * FL) + (-0.23 * LOI) + (-1.534 * Residu) + (-6.875 * Blaine) + (-0.271 * Insoluble) + (0.596 * Na2O) + (2.64 * K2O)
setting_time_akhir = 205.375 + (0.405 * SiO2) + (-0.628 * Al2O3) + (-0.643 * Fe2O3) + (-1.166 * CaO) + (1.265 * MgO) + (1.19 * SO3) + (-1.068 * C3S) + (0.818 * C2S) + (-0.114 * C3A) + (-0.778 * C4AF) + (-1.292 * FL) + (0.559 * LOI) + (-1.034 * Residu) + (-5.868 * Blaine) + (0.278 * Insoluble) + (-1.995 * Na2O) + (0.109 * K2O)

# Inisialisasi session state jika belum ada
if "data_list" not in st.session_state:
    st.session_state.data_list = []

# Simpan Data
if st.sidebar.button("Simpan Data"):
    st.session_state.data_list.append([Tanggal, Silo, Peneliti, SiO2, Al2O3, Fe2O3, CaO, MgO, SO3, C3S, C2S, C3A, C4AF, FL, LOI, Residu, Blaine, Insoluble, Na2O, K2O, kuat_tekan_1d, kuat_tekan_3d, kuat_tekan_7d, kuat_tekan_28d, setting_time_awal, setting_time_akhir])

# Tabs
tabs = st.tabs(["🔎 Prediksi", "📋 Data Tersimpan", "📈 Analisis Deskriptif", "📊 Visualisasi Data", "👥Tentang Kami"])

with tabs[0]:
    st.subheader("🔎 Hasil Prediksi")
    cols_pred = st.columns(2)
    cols_pred[0].metric(label="🧪 Kuat Tekan 1 Hari", value=f"{kuat_tekan_1d:.2f} kg/cm²")
    cols_pred[1].metric(label="🧪 Kuat Tekan 3 Hari", value=f"{kuat_tekan_3d:.2f} kg/cm²")
    cols_pred[0].metric(label="🧪 Kuat Tekan 7 Hari", value=f"{kuat_tekan_7d:.2f} kg/cm²")
    cols_pred[1].metric(label="🧪 Kuat Tekan 28 Hari", value=f"{kuat_tekan_28d:.2f} kg/cm²")
    cols_pred[0].metric(label="⏳ Setting Time Awal", value=f"{setting_time_awal:.2f} Menit")
    cols_pred[1].metric(label="⏳ Setting Time Akhir", value=f"{setting_time_akhir:.2f} Menit")

with tabs[1]:
    st.subheader("📋 Data yang Telah Disimpan")
    df = pd.DataFrame(st.session_state.data_list, columns=["Tanggal", "Silo", "Peneliti", "SiO2", "Al2O3", "Fe2O3", "CaO", "MgO", "SO3", "C3S", "C2S", "C3A", "C4AF", "FL", "LOI", "Residu", "Blaine", "Insoluble", "Na2O", "K2O", "Kuat Tekan 1 Hari", "Kuat Tekan 3 Hari", "Kuat Tekan 7 Hari", "Kuat Tekan 28 Hari", "Setting Time Awal", "Setting Time Akhir"])
    st.dataframe(df)

    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(label="Download CSV", data=csv, file_name="data_prediksi.csv", mime="text/csv")

with tabs[2]:
    st.subheader("📈 Analisis Deskriptif")
    st.write(df.describe())

with tabs[3]:
    # 📊 **Visualisasi Data**
    st.subheader("📊 Visualisasi Data")

    # 🎨 **Gaya Warna Seragam**
    main_colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728"]  # Biru, Oranye, Hijau, Merah

    # 🟢 **Boxplot Distribusi Variabel**
    df["Tanggal"] = pd.to_datetime(df["Tanggal"], errors="coerce")
    df["Bulan"] = df["Tanggal"].dt.strftime("%Y-%m")

    if not df.empty:
        var_x = st.selectbox("Pilih Variabel Penelitian untuk Boxplot", df.columns[3:19])
        fig1 = px.box(df, x="Bulan", y=var_x, title=f"Distribusi {var_x} per Bulan",
                    color_discrete_sequence=[main_colors[0]])  # Biru
        fig1.update_layout(template="plotly_white")  # Tema Modern
        st.plotly_chart(fig1)

    # 🔵 **Bar Chart Setting Time + Line Chart Variabel X**
    var_x_plot = st.selectbox("Pilih Variabel Penelitian untuk Line Chart", df.columns[3:19])

    if var_x_plot:
        df_melted = df.melt(id_vars=["Tanggal"], value_vars=["Setting Time Awal", "Setting Time Akhir"], 
                            var_name="Tipe Setting Time", value_name="Waktu")

        fig2 = px.bar(df_melted, x="Tanggal", y="Waktu", color="Tipe Setting Time",
                    barmode="group", title="Setting Time dengan Line Chart Variabel Penelitian",
                    color_discrete_sequence=[main_colors[1], main_colors[2]])  # Oranye & Hijau

        # Tambahkan Line Chart di atas Bar Chart
        fig2.add_scatter(x=df["Tanggal"], y=df[var_x_plot], mode="lines+markers", 
                        name=var_x_plot, line=dict(color=main_colors[3], width=2))  # Merah

        fig2.update_layout(template="plotly_white")
        st.plotly_chart(fig2)

    # 🔴 **Tracking Kuat Tekan**
    tekan_vars = ["Kuat Tekan 1 Hari", "Kuat Tekan 3 Hari", "Kuat Tekan 7 Hari", "Kuat Tekan 28 Hari"]

    fig3 = go.Figure()

    for i, tekan in enumerate(tekan_vars):
        fig3.add_trace(go.Scatter(
            x=df["Tanggal"], y=df[tekan], mode="lines+markers",
            name=tekan, line=dict(color=main_colors[i], width=2))
        )

    fig3.update_layout(
        title="Tracking Kuat Tekan 1, 3, 7, 28 Hari",
        xaxis_title="Tanggal",
        yaxis_title="Kuat Tekan",
        template="plotly_white"
    )

    st.plotly_chart(fig3)
    
with tabs[4]:
    st.subheader("👥 Tentang Kami")
    st.write("""
    **Dashboard Product Quality Assurance** ini dikembangkan sebagai bagian dari proyek kerja praktik di **PT Semen Indonesia (Persero) Tbk** oleh:

    👩‍💼 **Fitri Fatma Dewi**  
    📧 fitrifatmadewi10@gmail.com  
    📞 +62 857-3183-3302  

    👩‍💼 **Devi Sagita Rachman**  
    📧 devisrachmn@gmail.com  
    📞 +62 838-4432-2614  

    🏫 **Departemen Statistika | Fakultas Sains dan Analitika Data (FSAD) | Institut Teknologi Sepuluh Nopember | 2025**
    """)
