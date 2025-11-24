import streamlit as st
import google.generativeai as genai
import time # Klavye efekti için gerekli kütüphane

# --- RENK PALETİ ---
PRIMARY_COLOR = "#4A6B4A"   # Koyu Yeşil
BG_COLOR_LIGHT = "#E3F0E3"  # Açık Yeşil
BG_COLOR_WHITE = "#FFFFFF"  # Beyaz
TEXT_COLOR_MAIN = "#1A2B1A" # Koyu Metin Rengi

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
    
    /* 2. TÜM YAZILARI KOYU YAP */
    p, span, div, li {{
        color: {TEXT_COLOR_MAIN} !important;
    }}
    
    /* 3. BAŞLIKLAR */
    h1, h2, h3, h4, h5, h6 {{
        color: {PRIMARY_COLOR} !important;
        font-family: 'Helvetica', sans-serif;
    }}
    
    /* 4. SIDEBAR DÜZENİ */
    section[data-testid="stSidebar"] {{
        background-color: {BG_COLOR_LIGHT};
        border-right: 2px solid #CADBCA;
    }}
    
    /* 5. SOHBET KUTUSU */
    .stChatMessage {{
        background-color: {BG_COLOR_WHITE};
        border-radius: 15px;
        padding: 10px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        border: 1px solid #CADBCA;
    }}
    
    /* 6. LİNKLER VE BUTONLAR */
    a {{ color: {PRIMARY_COLOR} !important; text-decoration: none; font-weight: bold; }}
    button[kind="secondary"] {{ background-color: {PRIMARY_COLOR} !important; color: white !important; border: none !important; }}
    button[kind="secondary"] p {{ color: white !important; }}
    
    header[data-testid="stHeader"] {{ background-color: transparent; }}
</style>
""", unsafe_allow_html=True)

# --- BAŞLIK ---
# "Yusuf AI" yerine daha havalı olan "Nexa" ismini kullandım.
st.markdown(f"<h1 style='text-align: center; color: {PRIMARY_COLOR};'>🌿 Nexa - Yusuf'un Dijital Asistanı</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; font-size: 1.1em; color: {TEXT_COLOR_MAIN};'>Ben Nexa. Yusuf'un teknik yetkinlikleri ve projeleri hakkında her şeyi bana sorabilirsin.</p>", unsafe_allow_html=True)
st.divider()

# --- YAN MENÜ ---
with st.sidebar:
    st.write("# 👨‍💻 Profil") 
    st.write("**Yusuf Can Aydın**")
    st.write("📍 Kalıp Tasarımcısı & Teknik Ressam")
    st.write("🏢 Farplas")
    st.divider()
    st.write("### 📬 İletişim")
    st.write("📧 yca4134@gmail.com")
    # Senin yeşil rengine (#4A6B4A) boyanmış resmi LinkedIn butonu
    linkedin_url = "https://www.linkedin.com/in/yusuf-can-ayd%C4%B1n-138389194"
    st.markdown(f"""
    <a href="{linkedin_url}" target="_blank">
        <img src="https://img.shields.io/badge/LinkedIn-4A6B4A?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn Profilim" style="width: 100%; border-radius: 5px;">
    </a>
    """, unsafe_allow_html=True)

# --- GEMINI MODEL AYARLARI ---
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
except:
    st.error("⚠️ API Anahtarı bulunamadı!")
    st.stop()

# İsim burada da güncellendi: "Nexa"
system_prompt = """
Sen Yusuf Can Aydın'ın kişisel web sitesindeki yapay zeka asistanısın. Adın "YCA Bot".
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

# --- KLAVYE EFEKTİ FONKSİYONU ---
def stream_data(text):
    for word in text.split(" "):
        yield word + " "
        time.sleep(0.05) # Yazma hızı (Düşürürsen hızlanır)

# --- SOHBET ARAYÜZÜ ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Geçmiş mesajları göster
for message in st.session_state.messages:
    avatar = "🧑‍💻" if message["role"] == "user" else "🌿"
    with st.chat_message(message["role"], avatar=avatar):
        st.write(message["content"])

# KULLANICI GİRİŞİ VE CEVAP ALANI
if user_input := st.chat_input("Nexa'ya sor... (Örn: Yusuf hangi programları kullanıyor?)"):
    
    # 1. Kullanıcı mesajını ekle
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user", avatar="🧑‍💻"):
        st.write(user_input)

    # 2. Cevabı üret ve KLAVYE EFEKTİYLE yaz
    try:
        # Sohbet geçmişini modele ver
        chat = model.start_chat(history=[
            {"role": m["role"], "parts": [m["content"]]} 
            for m in st.session_state.messages[:-1]
        ])
        
        response = chat.send_message(user_input)
        ai_response = response.text

        # BURASI SİHİRLİ KISIM (Klavye Efekti)
        with st.chat_message("assistant", avatar="🌿"):
            # st.write_stream, metni parça parça ekrana basar
            st.write_stream(stream_data(ai_response))
        
        # Cevabı hafızaya kaydet
        st.session_state.messages.append({"role": "model", "content": ai_response})
        
    except Exception as e:
        st.error(f"Bir hata oluştu: {e}")
