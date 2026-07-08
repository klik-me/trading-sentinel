import streamlit as st
from google import genai
from PIL import Image

# --- KONFIGURASI HALAMAN UTAMA ---
st.set_page_config(
    page_title="AI Trading Sentinel",
    page_icon="🛡️",
    layout="centered"
)

# Kunci API Anda (Sudah tertanam aman)
API_KEY = "AQ.Ab8RN6Ipyee4PB046qNKplYWaRSQucTi75o01_yP5bEXUF3iZQ"

# Inisialisasi Gemini
@st.cache_resource
def get_gemini_client():
    return genai.Client(api_key=API_KEY)

client = get_gemini_client()

# --- TAMPILAN ANTARMUKA WEB ---
st.title("🛡️ AI Trading Sentinel")
st.markdown("### *Stop Kontrol Emosi, Percayakan pada Sistem*")
st.caption("Gunakan aplikasi ini saat Anda merasakan dorongan kuat untuk melakukan intervensi manual di tengah volatilitas pasar.")

st.markdown("---")

# 1. Input Psikologis
st.markdown("#### 🧠 1. Apa yang sedang Anda Rasakan?")
user_feeling = st.text_area(
    "Jelaskan firasat Anda atau tindakan manual apa yang ingin diambil:",
    placeholder="Contoh: Saya panik melihat candle merah panjang di XAUUSD, rasanya ingin langsung cut loss manual padahal SL dari bot belum kena...",
    label_visibility="collapsed"
)

# 2. Input Gambar Chart
st.markdown("#### 📸 2. Upload Screenshot Chart (TradingView / MT5)")
uploaded_file = st.file_uploader("Pilih gambar dari galeri HP Anda:", type=["jpg", "jpeg", "png"])

st.markdown("<br>", unsafe_allow_html=True)

# 3. Tombol Eksekusi
if st.button("🚨 AUDIT LOGIKA TRADING SAYA", use_container_width=True):
    if not user_feeling.strip():
        st.warning("Silakan tuliskan firasat atau alasan Anda terlebih dahulu!")
    elif uploaded_file is None:
        st.warning("Silakan unggah screenshot chart TradingView / MT5 Anda!")
    else:
        with st.spinner("Gemini sedang menganalisis grafik dan mendiagnosis tingkat emosi Anda..."):
            try:
                # Memuat gambar dari Streamlit Uploader
                chart_image = Image.open(uploaded_file)
                
                # Instruksi khusus untuk Gemini
                prompt = f"""
                Bertindaklah sebagai psikolog trading profesional sekaligus analis teknikal senior yang sangat dingin dan objektif.
                Klien Anda sedang melihat market dan merasakan dorongan emosional/firasat untuk melakukan intervensi manual.
                
                Firasat/Tindakan Klien: "{user_feeling}"
                
                Tugas Anda:
                1. Analisis Gambar Chart: Lihat gambar TradingView/MT5 yang dilampirkan. Analisis tren, candlestick, atau indikator (seperti EMA/Volume jika terlihat) secara objektif.
                2. Audit Logika: Apakah "feeling" klien sejalan dengan data teknikal yang terlihat di gambar chart, atau ini hanya kepanikan/FOMO sesaat?
                3. Berikan nasihat psikologis yang tegas agar mereka tetap disiplin pada trading plan/bot mereka.
                4. Berikan kesimpulan akhir di bagian paling bawah dengan format huruf tebal: **REKOMENDASI AKHIR: [TETAP PADA SISTEM / INTERVENSI DIIZINKAN]**
                """
                
                # Memanggil AI
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=[chart_image, prompt],
                )
                
                # Menampilkan Hasil dengan Desain Rapi
                st.success("Analisis Selesai!")
                st.markdown("---")
                st.markdown("### 📋 Hasil Audit AI Sentinel:")
                st.markdown(response.text)
                st.markdown("---")
                st.caption("Pengingat: Pasar digerakkan oleh data, bukan oleh ketakutan kita.")
                
            except Exception as e:
                st.error(f"Terjadi kesalahan teknis: {e}")

