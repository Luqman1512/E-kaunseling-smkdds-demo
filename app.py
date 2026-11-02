import streamlit as st
import google.generativeai as genai
import requests
from datetime import date, time

st.set_page_config(page_title="E-KAUNSELING SMKDDS", layout="centered", page_icon="🎓")

# === API & TOKEN KAU - DAH SIAP MASUK ===
GEMINI_API_KEY = "AQ.Ab8RN6KXKqr46Q_ytwLjYFip1NoLqEhx3axuSIDxGtrmMJT1fQ"
TELEGRAM_BOT_TOKEN = "9111688021:AAH0lo40LDLHHQhDJrT5D93pllniN8qCat4"
TELEGRAM_CHAT_ID = "6927735989"
# =======================================

try:
    genai.configure(api_key=GEMINI_API_KEY)
except Exception as e:
    pass

def hantar_telegram(nama, tel, isu, kelas, cg, tarikh, masa):
    mesej = f"🚨 *TEMUJANJI BARU SMKDDS*\n\n👤 Nama: {nama}\n📞 Tel: {tel}\n🏫 Kelas: {kelas}\n📝 Isu: {isu}\n👨‍🏫 Cikgu: {cg}\n📅 Tarikh: {tarikh} {masa}\n\n_Dari E-KAUNSELING_"
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    try:
        r = requests.post(url, json={"chat_id": TELEGRAM_CHAT_ID, "text": mesej, "parse_mode": "Markdown"})
        return r.status_code == 200
    except:
        return False

if "login" not in st.session_state: st.session_state.login=False
if "user" not in st.session_state: st.session_state.user=""
if "chat" not in st.session_state: st.session_state.chat=[]
if "buntu" not in st.session_state: st.session_state.buntu=False

if not st.session_state.login:
    st.markdown("<h1 style='text-align:center'>SMKDDS</h1><h3 style='text-align:center'>E-KAUNSELING AI CHATBOT</h3>", unsafe_allow_html=True)
    t1,t2=st.tabs(["Log Masuk","Daftar"])
    with t1:
        n=st.text_input("Email / Nama",key="l1",placeholder="ali@smkdds.edu.my")
        p=st.text_input("Kata Laluan",type="password",key="l2")
        if st.button("Log Masuk",type="primary",use_container_width=True):
            if n and p:
                st.session_state.login=True
                st.session_state.user=n
                st.session_state.chat=[{"role":"assistant","content":f"Hai {n}, saya AI Kaunselor SMKDDS. Cerita la apa buat kau stress hari ni?"}]
                st.rerun()
    with t2:
        nn=st.text_input("Nama Penuh",placeholder="Ahmad bin Ali")
        kk=st.text_input("Kelas",placeholder="5 Sains 2")
        ee=st.text_input("Email",placeholder="email@smkdds.edu.my")
        pp=st.text_input("Cipta Password",type="password")
        if st.button("Daftar Akaun",use_container_width=True):
            if nn and ee and pp:
                st.session_state.login=True
                st.session_state.user=nn
                st.session_state.chat=[{"role":"assistant","content":f"Hai {nn} ({kk}), akaun dah siap. Jom luah."}]
                st.rerun()
else:
    with st.sidebar:
        st.write(f"👤 {st.session_state.user}\n\nSMK DDS")
        if st.button("➕ New Chat",use_container_width=True):
            st.session_state.chat=[{"role":"assistant","content":"Sesi baru bermula. Apa khabar?"}]
            st.session_state.buntu=False
            st.rerun()
        if st.button("🚪 Log Keluar",use_container_width=True):
            st.session_state.login=False
            st.rerun()
    st.markdown(f"### 🤖 AI Kaunselor - {st.session_state.user}")
    for m in st.session_state.chat:
        with st.chat_message(m["role"]): st.write(m["content"])
    if st.session_state.buntu:
        st.warning("💡 AI detect isu ni berat, sila tempah sesi F2F dengan cikgu di bawah.")
    if prompt:=st.chat_input("Taip luahan anda (cth: saya stress SPM)..."):
        st.session_state.chat.append({"role":"user","content":prompt})
        if any(k in prompt.lower() for k in ["stress sangat","give up","gagal","sedih sangat","buntu","tak boleh","penat","nak berhenti"]):
            st.session_state.buntu=True
        try:
            model=genai.GenerativeModel("gemini-1.5-flash", system_instruction="Kau AI Kaunselor SMKDDS, cakap Melayu santai, empatik, bagi nasihat pendek 3-4 point, jika pelajar sangat stress suruh booking cikgu.")
            res=model.generate_content(prompt)
            rep=res.text
        except Exception as e:
            rep="Saya faham perasaan tu berat sangat. Untuk bantuan lanjut, saya sangat cadang kau booking terus dengan Cikgu Kaunseling di bawah ya."
            st.session_state.buntu=True
        st.session_state.chat.append({"role":"assistant","content":rep})
        st.rerun()
    if st.session_state.buntu or st.checkbox("📅 Nak tempah temujanji kaunseling?"):
        st.write("---")
        st.markdown("### 📅 Tempah Temujanji Kaunseling")
        with st.form("book"):
            nf=st.text_input("Nama",value=st.session_state.user)
            tf=st.text_input("No Tel",placeholder="012-3456789")
            iss=st.text_input("Isu",placeholder="Stress / Keluarga / SPM")
            kf=st.text_input("Kelas",placeholder="5 Sains 2")
            cf=st.selectbox("Pilih Cikgu Kaunseling", ["Cg Aswari","Cg Zulika","Cg Shamimi"])
            c1,c2=st.columns(2)
            with c1: df=st.date_input("Tarikh",value=date.today())
            with c2: mf=st.time_input("Masa",value=time(10,0))
            if st.form_submit_button("Sahkan & Hantar ke Telegram Cikgu ✅",type="primary",use_container_width=True):
                if tf and iss and kf:
                    ok=hantar_telegram(nf,tf,iss,kf,cf,df,mf)
                    if ok:
                        st.success(f"✅ BERJAYA! Temujanji dengan {cf} dah masuk Telegram kau (ID: 6927735989). Check fon!")
                        st.balloons()
                        st.session_state.buntu=False
                    else:
                        st.error("Gagal hantar Telegram. Check Token/Bot.")
                else:
                    st.error("Isi No Tel, Isu, Kelas dulu")
