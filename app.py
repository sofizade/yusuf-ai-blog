import streamlit as st
import google.generativeai as genai
import time

# --- RENK PALETİ ---
PRIMARY_COLOR = "#4A6B4A"   # Koyu Yeşil
BG_COLOR_LIGHT = "#E3F0E3"  # Açık Yeşil
BG_COLOR_WHITE = "#FFFFFF"  # Beyaz
TEXT_COLOR_MAIN = "#1A2B1A" # Koyu Metin

# --- SAYFA AYARLARI ---
st.set_page_config(
    page_title="Nexa | Dijital Asistan",
    page_icon="🌿",
    layout="wide"
)

# --- CSS (TASARIM) ---
st.markdown(f"""
<style>
    /* 1. TÜM SAYFA GENELİ */
    .stApp {{
        background-color: {BG_COLOR_LIGHT};
        color: {TEXT_COLOR_MAIN};
    }}
    
    /* 2. YAZILARI KOYU YAP */
    p, span, div, li {{
        color: {TEXT_COLOR_MAIN} !important;
    }}
    
    /* 3. BAŞLIKLAR */
    h1, h2, h3 {{
        color: {PRIMARY_COLOR} !important;
        font-family: 'Helvetica', sans-serif;
    }}

    /* 4. SOHBET KUTUSU */
    .stChatMessage {{
        background-color: {BG_COLOR_WHITE};
        border-radius: 15px;
        padding: 10px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        border: 1px solid #CADBCA;
    }}
    
    /* 5. GİZLİ ÜST MENÜ */
    header[data-testid="stHeader"] {{ background-color: transparent; }}
    
    /* 6. LINKLER */
    a {{
        text-decoration: none;
        transition: opacity 0.3s;
    }}
    a:hover {{
        opacity: 0.8;
    }}
</style>
""", unsafe_allow_html=True)

# --- BAŞLIK VE AÇIKLAMA ---
st.markdown(f"<h1 style='text-align: center; color: {PRIMARY_COLOR}; margin-bottom: 0px;'>🌿 Nexa - Yusuf'un Dijital Asistanı</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; font-size: 1.1em; margin-top: 10px;'>Ben Nexa. Yusuf'un teknik yetkinlikleri ve projeleri hakkında her şeyi bana sorabilirsin.</p>", unsafe_allow_html=True)

# --- İLETİŞİM LİNKLERİ (HEADER KISMI) ---
# Gmail ve LinkedIn'i yan yana ortalayarak koyuyoruz
email_address = "yca4134@gmail.com"
linkedin_url = "https://www.linkedin.com/in/yusuf-can-ayd%C4%B1n-138389194"

st.markdown(f"""
<div style="display: flex; justify-content: center; align-items: center; gap: 20px; margin-bottom: 30px;">
    <a href="mailto:{email_address}" style="
        background-color: {BG_COLOR_WHITE}; 
        color: {PRIMARY_COLOR}; 
        padding: 8px 15px; 
        border-radius: 5px; 
        border: 1px solid {PRIMARY_COLOR}; 
        font-weight: bold; 
        display: flex; 
        align-items: center; 
        gap: 8px;">
        📧 {email_address}
    </a>

    <a href="{linkedin_url}" target="_blank" style="display: flex; align-items: center;">
        <img src="https://img.shields.io/badge/LinkedIn-4A6B4A?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn" style="height: 38px; border-radius: 4px;">
    </a>
</div>
""", unsafe_allow_html=True)

st.divider()

# --- GEMINI MODEL AYARLARI ---
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
except:
    st.error("⚠️ API Anahtarı bulunamadı!")
    st.stop()

# Nexa Karakteri
system_prompt = """
Sen Yusuf Can Aydın'ın kişisel web sitesindeki yapay zeka asistanısın. Adın "Nexa".
İsmin Siemens NX yazılımına ve teknolojiye bir göndermedir.
Ziyaretçiler sana Yusuf'un kariyeri, projeleri ve yetenekleri hakkında sorular soracak.
Senin görevin, Yusuf'u profesyonel, yetkin ve samimi bir dille temsil etmektir.
Biri sana 'Merhaba' derse kendini "Ben Nexa, Yusuf'un dijital asistanıyım" diye tanıt.

BİLGİ BANKASI:
[GENEL]
Yusuf Can Aydın, İstanbul'da yaşayan, Farplas bünyesinde çalışan bir Kalıp Tasarımcısıdır.
Togg, Renault, Ford gibi büyük projelerde deneyimlidir.

[DENEYİM]
* Farplas - Kalıp Tasarımcısı (Ocak 2025 - Günümüz)
* Farplas - Kıdemli Teknik Ressam (Ocak 2024 - Mart 2025)
* Farplas - Teknik Ressam (Ocak 2021 - Ocak 2024): Renault BJA, Togg C-SUV, Toyota 025D, Ford V710.
* Farplas - Proje Teknikeri (Kasım 2019 - Ocak 2021): Hyundai AC3/BC3.

[YETENEKLER]
* Siemens Nx (İleri Seviye), Moldex3D, Kalıp Tasarımı.
* İngilizce (Sınırlı çalışma yetkinliği).

[EĞİTİM]
* Anadolu Üni. Yönetim Bilgi Sistemleri (Lisans - 2021)
* Uludağ Üni. Mekatronik (Önlisans - 2019)
* Hatice Bayraktar ATL - Makine İmalatı (Lise - 2016)
"""

model = genai.GenerativeModel(
    model_name="gemini-2.0-flash",
    system_instruction=system_prompt
)

# --- KLAVYE EFEKTİ ---
def stream_data(text):
    for word in text.split(" "):
        yield word + " "
        time.sleep(0.05)

# --- SOHBET ARAYÜZÜ ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mesajları göster
for message in st.session_state.messages:
    avatar = "🧑‍💻" if message["role"] == "user" else "🌿"
    with st.chat_message(message["role"], avatar=avatar):
        st.write(message["content"])

# Giriş Alanı
if user_input := st.chat_input("Nexa'ya sor... (Örn: Yusuf hangi programları kullanıyor?)"):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user", avatar="🧑‍💻"):
        st.write(user_input)

    try:
        chat = model.start_chat(history=[
            {"role": m["role"], "parts": [m["content"]]} 
            for m in st.session_state.messages[:-1]
        ])
        
        response = chat.send_message(user_input)
        ai_response = response.text

        with st.chat_message("assistant", avatar="🌿"):
            st.write_stream(stream_data(ai_response))
        
        st.session_state.messages.append({"role": "model", "content": ai_response})
        
    except Exception as e:
        st.error(f"Bir hata oluştu: {e}")
