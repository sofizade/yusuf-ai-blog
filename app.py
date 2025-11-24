import streamlit as st
import google.generativeai as genai

# --- RENK PALETİ ---
PRIMARY_COLOR = "#4A6B4A"   # Koyu Yeşil (Başlıklar, Butonlar)
BG_COLOR_LIGHT = "#E3F0E3"  # Açık Yeşil (Genel Arka Plan, Sidebar)
BG_COLOR_WHITE = "#FFFFFF"  # Beyaz (İçerik Alanı)
TEXT_COLOR_MAIN = "#1A2B1A" # Okunabilir Koyu Yeşile Çalan Siyah (DÜZELTİLDİ)

# --- SAYFA AYARLARI ---
st.set_page_config(
    page_title="Yusuf Can Aydın | AI Blog",
    page_icon="🌿",
    layout="wide"
)

# --- DÜZELTİLMİŞ CSS (OKUNABİLİRLİK İÇİN) ---
st.markdown(f"""
<style>
    /* 1. TÜM SAYFA GENELİ */
    .stApp {{
        background-color: {BG_COLOR_LIGHT};
    }}
    
    /* 2. TÜM YAZILARI KOYU YAP (ZORUNLU) */
    p, span, div, li {{
        color: {TEXT_COLOR_MAIN} !important;
    }}
    
    /* 3. BAŞLIKLAR */
    h1, h2, h3, h4, h5, h6 {{
        color: {PRIMARY_COLOR} !important;
        font-family: 'Helvetica', sans-serif;
    }}
    
    /* 4. SIDEBAR (YAN MENÜ) DÜZELTMESİ */
    section[data-testid="stSidebar"] {{
        background-color: {BG_COLOR_LIGHT};
        border-right: 2px solid #CADBCA;
    }}
    section[data-testid="stSidebar"] p, section[data-testid="stSidebar"] span {{
        color: {TEXT_COLOR_MAIN} !important;
    }}
    section[data-testid="stSidebar"] div {{
        color: {TEXT_COLOR_MAIN} !important;
    }}

    /* 5. SOHBET KUTUCUKLARI */
    .stChatMessage {{
        background-color: {BG_COLOR_WHITE};
        border-radius: 15px;
        padding: 10px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        border: 1px solid #CADBCA;
    }}
    /* Sohbet Balonu İçindeki Yazılar Kesinlikle Koyu Olsun */
    .stChatMessage p {{
        color: {TEXT_COLOR_MAIN} !important;
    }}
    
    /* 6. LİNKLER */
    a {{
        color: {PRIMARY_COLOR} !important;
        text-decoration: none;
        font-weight: bold;
    }}
    a:hover {{
        text-decoration: underline;
    }}

    /* 7. BUTONLAR */
    button[kind="secondary"] {{
        background-color: {PRIMARY_COLOR} !important;
        color: white !important; /* Buton içi yazı beyaz kalsın */
        border: none !important;
    }}
    /* Buton içindeki p etiketini beyaz yap (üstteki kuralı ezmek için) */
    button[kind="secondary"] p {{
        color: white !important; 
    }}
    
    /* Üst menü çizgisini gizle */
    header[data-testid="stHeader"] {{
        background-color: transparent;
    }}
</style>
""", unsafe_allow_html=True)

# --- İÇERİK ---

# Başlık
st.markdown(f"<h1 style='text-align: center; color: {PRIMARY_COLOR};'>🌿 Yusuf Can Aydın - Dijital Asistan</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; font-size: 1.1em; color: {TEXT_COLOR_MAIN};'>Yusuf'un kariyeri ve projeleri hakkında merak ettiklerini yapay zekaya sor.</p>", unsafe_allow_html=True)
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
    st.link_button("LinkedIn Profiline Git", "https://www.linkedin.com/in/yusuf-can-ayd%C4%B1n-138389194")
    
    st.divider()
    st.info("Bu asistan, özel renk paletiyle tasarlanmıştır.")

# --- GEMINI AYARLARI ---
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
except:
    st.error("⚠️ API Anahtarı bulunamadı! Lütfen Streamlit ayarlarından ekleyin.")
    st.stop()

system_prompt = """
Sen Yusuf Can Aydın'ın kişisel web sitesindeki yapay zeka asistanısın. Adın "Yusuf AI".
Ziyaretçiler sana Yusuf'un kariyeri, projeleri ve yetenekleri hakkında sorular soracak.
Senin görevin, Yusuf'u profesyonel, yetkin ve samimi bir dille temsil etmektir.
Biri sana 'Merhaba' derse kendini tanıt.

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

# --- SOHBET ARAYÜZÜ ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mesajları göster
for message in st.session_state.messages:
    avatar = "🧑‍💻" if message["role"] == "user" else "🌿"
    with st.chat_message(message["role"], avatar=avatar):
        st.write(message["content"])

# Kullanıcı Girişi
if user_input := st.chat_input("Sorunu buraya yaz..."):
    # Mesajı ekle ve göster
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user", avatar="🧑‍💻"):
        st.write(user_input)

    # Cevabı üret
    try:
        chat = model.start_chat(history=[
            {"role": m["role"], "parts": [m["content"]]} 
            for m in st.session_state.messages[:-1]
        ])
        response = chat.send_message(user_input)
        ai_response = response.text

        # Cevabı göster
        with st.chat_message("assistant", avatar="🌿"):
            st.write(ai_response)
        
        st.session_state.messages.append({"role": "model", "content": ai_response})
        
    except Exception as e:
        st.error(f"Bir hata oluştu: {e}")
