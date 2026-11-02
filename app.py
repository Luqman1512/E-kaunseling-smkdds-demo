import streamlit as st
import sqlite3
import datetime
from datetime import date

st.set_page_config(page_title="E-Kaunseling SMKDDS", page_icon="💬", layout="centered")
conn = sqlite3.connect('kaunseling.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS bookings (id INTEGER PRIMARY KEY AUTOINCREMENT, nama TEXT, kelas TEXT, no_tel TEXT, kategori TEXT, tarikh TEXT, masa TEXT, keterangan TEXT, status TEXT, tarikh_mohon TEXT)''')
conn.commit()

st.markdown("<h1 style='text-align: center; color: #1E88E5;'>💬 E-Kaunseling SMK DDS</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Sistem Tempahan Sesi Kaunseling - Sulit & Selamat</p>", unsafe_allow_html=True)
st.divider()

menu = st.sidebar.selectbox("Log Masuk Sebagai:", ["🎓 Pelajar", "👩‍🏫 Kaunselor", "📊 Admin"])

if menu == "🎓 Pelajar":
    st.subheader("📝 Borang Permohonan Sesi Kaunseling")
    with st.form("booking_form"):
        nama = st.text_input("Nama Penuh")
        kelas = st.text_input("Kelas (cth: 5 Amanah)")
        no_tel = st.text_input("No. WhatsApp")
        kategori = st.selectbox("Kategori Isu", ["Akademik", "Kerjaya", "Sahsiah", "Keluarga", "Emosi / Stress", "Buli", "Lain-lain"])
        tarikh = st.date_input("Tarikh Pilihan", min_value=date.today())
        masa = st.selectbox("Masa", ["8:00-9:00 AM", "9:00-10:00 AM", "10:20-11:20 AM", "11:20-12:20 PM", "2:00-3:00 PM"])
        keterangan = st.text_area("Ringkasan masalah")
        submit = 
