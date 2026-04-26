import streamlit as st
import streamlit.components.v1 as components
import sqlite3
import random
import hashlib
import base64
import os  


# --- 0. KEAMANAN DATA ---
def hash_password(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

# --- 1. SISTEM DATABASE (FITUR UTAMA) ---
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
    p_hashed = hash_password(p)
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (u, p_hashed))
    data = c.fetchone()
    conn.close()
    return data

def simpan_pendaftar(u, p, e, t, b, nr, na, ref):
    try:
        conn = sqlite3.connect('database_s2.db')
        c = conn.cursor()
        p_hashed = hash_password(p)
        c.execute("INSERT INTO users VALUES (?,?,?,?,?,?,?,?)", (u, p_hashed, e, t, b, nr, na, ref))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False

init_db()

# --- 2. LOGIKA STATE ---
if 'v_code' not in st.session_state:
    st.session_state.v_code = str(random.randint(1000, 9999))

# --- 3. CSS & VIDEO BACKGROUND (VERSI DEPLOY) ---
def get_base64_video():
    nama_video = "undefined - Imgur.mp4"
    paths = [nama_video, f"/sdcard/Download/{nama_video}"]
    
    for p in paths:
        if os.path.exists(p):
            with open(p, "rb") as f:
                return base64.b64encode(f.read()).decode()
    return None


bin_str = get_base64_video()


bin_str = get_base64_video()

if bin_str:
    st.markdown(f'''
    <style>
        header, footer, #MainMenu, .stDeployButton {{ visibility: hidden !important; }}
        .stApp {{ background: transparent !important; }}
        #video-container {{ position: fixed; top: 0; left: 0; width: 100%; height: 100%; z-index: -1; overflow: hidden; }}
        #bg-video {{ width: 100%; height: 100%; object-fit: cover; }}
        .block-container {{ padding: 0.5rem !important; padding-bottom: 160px !important; background-color: rgba(0, 0, 0, 0.4); }}
    </style>
    <div id="video-container">
        <video autoplay loop muted playsinline id="bg-video">
            <source src="data:video/mp4;base64,{bin_str}" type="video/mp4">
        </video>
    </div>
    ''', unsafe_allow_html=True)
else:
    st.error("⚠️ File 'undefined - Imgur.mp4' tidak ditemukan di folder Download.")
    st.markdown('<style>header, footer, #MainMenu, .stDeployButton { visibility: hidden !important; } .stApp { background-image: url("https://i.imgur.com/0sCszBw.png"); background-size: cover; }</style>', unsafe_allow_html=True)

# Styling Input & Tombol
st.markdown("""
<style>
    .stTextInput input { background-color: rgba(26, 29, 36, 0.9) !important; color: #00e676 !important; border: 1px solid #00e676 !important; }
    div.stButton > button[kind="primary"] {
        background: linear-gradient(180deg, #00e676 0%, #00c853 100%) !important;
        color: white !important; font-weight: 800 !important;
        border: 2px solid #ffd700 !important; border-radius: 12px !important;
    }
</style>
""", unsafe_allow_html=True)

# --- 4. POPUP LOGIN & DAFTAR ---
@st.dialog("HALAMAN MASUK")
def login_dialog():
    u = st.text_input("User Name", key="l_u")
    p = st.text_input("Kata Sandi", type="password", key="l_p")
    if st.button("PROSES MASUK", type="primary", use_container_width=True):
        if cek_login(u, p): 
            st.success(f"✅ Halo {u}, Selamat Bermain!"); st.balloons()
        else: st.error("⚠️ Akun tidak ditemukan!")

@st.dialog("PENDAFTARAN", width="large")
def register_dialog():
    st.markdown("### 📝 DAFTAR AKUN BARU")
    col1, col2 = st.columns(2)
    with col1:
        u = st.text_input("* User Name", key="reg_u")
        p = st.text_input("* Kata sandi", type="password", key="reg_p")
        p2 = st.text_input("* Ulang Kata sandi", type="password", key="reg_p2")
    with col2:
        t = st.text_input("* No Telepon", key="reg_t")
        b = st.selectbox("* Bank", ["BCA", "MANDIRI", "BNI", "BRI", "DANA", "OVO", "GOPAY"])
        nr = st.text_input("* Nomor Rekening", key="reg_nr")
    
    na = st.text_input("* Nama Pemilik Rekening", key="reg_na")
    st.markdown(f"**Kode Validasi: :red[{st.session_state.v_code}]**")
    v_in = st.text_input("* Masukkan Kode", key="reg_v")

    if st.button("DAFTAR SEKARANG", type="primary", use_container_width=True):
        if p != p2: st.error("❌ Kata sandi tidak cocok!")
        elif v_in != st.session_state.v_code: st.error("❌ Kode validasi salah!")
        elif u and p and nr and na:
            if simpan_pendaftar(u, p, "", t, b, nr, na, ""):
                st.success("✅ Berhasil! Silakan Login.")
                st.session_state.v_code = str(random.randint(1000, 9999))
            else: st.error("⚠️ Username sudah ada!")

# --- 5. HEADER ---
c1, c2 = st.columns([2, 1])
with c1: st.image("https://i.imgur.com/pjj1xQo.png", width=200)
with c2:
    if st.button("MASUK", use_container_width=True): login_dialog()
    if st.button("DAFTAR", use_container_width=True): register_dialog()

# --- 6. HTML KOMPONEN LENGKAP (SLIDER, JP, & GAME LIST) ---
fitur_html = """
<style>
    /* Slider Utama */
    .s-container { width: 100%; overflow: hidden; border-radius: 15px; border: 2px solid #ffd700; position: relative; }
    .s-wrapper { display: flex; overflow-x: auto; scroll-snap-type: x mandatory; scrollbar-width: none; scroll-behavior: smooth; }
    .s-wrapper::-webkit-scrollbar { display: none; }
    .s-wrapper img { width: 100%; flex-shrink: 0; scroll-snap-align: start; }

    /* Marquee RGB */
    .marquee-rgb { margin-top: 10px; padding: 3px; border-radius: 10px; background: linear-gradient(90deg, red, yellow, green, cyan, blue, magenta, red); background-size: 400%; animation: rgb 5s linear infinite; }
    .marquee-inner { background: #1a1d24; border-radius: 8px; padding: 10px; overflow: hidden; }
    .m-text { display: inline-block; white-space: nowrap; color: #ffd700; font-weight: bold; animation: jalan 15s linear infinite; }

    /* Jackpot */
    .jp-card { background: #000; border: 2px solid #ffd700; border-radius: 15px; padding: 10px; text-align: center; margin-top: 10px; box-shadow: 0 0 10px #ffd700; }
    .jp-text { color: red; font-size: 24px; font-weight: 900; text-shadow: 0 0 5px red; font-family: monospace; }

    /* FITUR GAME LIST GACOR */
    .game-section { position: relative; margin-top: 15px; padding: 0 5px; }
    .game-header { color: gold; font-weight: bold; font-size: 14px; margin-bottom: 8px; text-shadow: 1px 1px black; display: flex; align-items: center; gap: 5px; }
    .game-scroll { display: flex; overflow-x: auto; scroll-behavior: smooth; gap: 12px; scrollbar-width: none; padding: 5px 0; }
    .game-scroll::-webkit-scrollbar { display: none; }
    
    .game-card { flex: 0 0 130px; background: #111; border: 1px solid gold; border-radius: 12px; overflow: hidden; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.5); }
    .game-card img { width: 100%; height: 130px; object-fit: cover; border-bottom: 1px solid #333; }
    .game-info { padding: 6px 2px; font-size: 11px; color: white; font-weight: bold; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
    
    .rtp-container { background: #333; border-radius: 20px; margin: 0 8px 8px 8px; height: 16px; position: relative; overflow: hidden; border: 1px solid #555; }
    .rtp-fill { height: 100%; display: flex; align-items: center; justify-content: center; font-size: 10px; font-weight: 900; color: black; transition: width 0.5s ease; }
    
    .btn-nav { position: absolute; top: 55%; transform: translateY(-50%); background: rgba(0,0,0,0.8); color: gold; border: 1px solid gold; width: 30px; height: 30px; display: flex; justify-content: center; align-items: center; cursor: pointer; z-index: 10; border-radius: 50%; font-size: 16px; box-shadow: 0 0 5px gold; }
    .btn-prev { left: -10px; }
    .btn-next { right: -10px; }

    /* Pop Chat */
    #chat-btn { position: fixed; bottom: 100px; right: 20px; width: 60px; height: 60px; background: radial-gradient(circle, #00fbff, #0072ff); border-radius: 50%; display: flex; justify-content: center; align-items: center; font-size: 30px; z-index: 9999; border: 3px solid white; cursor: pointer; box-shadow: 0 0 15px #00fbff; }
    #chat-overlay { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.8); z-index: 10000; }
    #chat-popup { display: none; position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 85%; max-width: 350px; background: #1a1a1a; border: 2px solid #ffd700; border-radius: 20px; z-index: 10001; overflow: hidden; }
    .chat-row { display: flex; justify-content: space-between; align-items: center; padding: 12px 20px; border-bottom: 1px solid #333; color: white !important; text-decoration: none !important; font-weight: bold; font-size: 13px; }
    .action-btn { background: #ffd700; color: black; padding: 4px 8px; border-radius: 5px; font-size: 10px; }

    @keyframes rgb { 0%{background-position:0%} 100%{background-position:100%} }
    @keyframes jalan { from { transform: translateX(100%); } to { transform: translateX(-100%); } }
</style>

<div class="s-container">
    <div class="s-wrapper" id="slider">
        <img src="https://i.imgur.com/IA1m2GF.png">
        <img src="https://i.imgur.com/vUeCcl3.png">
        <img src="https://i.imgur.com/kek6NF4.png">
    </div>
</div>

<div class="marquee-rgb">
    <div class="marquee-inner"><div class="m-text">🔥 S2 SEJATI - SITUS GACOR TERPERCAYA - WD BERAPAPUN PASTI DIBAYAR LUNAS! 🔥</div></div>
</div>

<div class="jp-card">
    <div style="color:#ffd700; font-size:10px; font-weight:bold;">✨ PROGRESSIVE JACKPOT ✨</div>
    <div class="jp-text">RP <span id="jp-val">8.715.820.442</span></div>
</div>

<div class="game-section">
    <div class="game-header">🎰 GAME HOT HARI INI</div>
    <div class="btn-nav btn-prev" onclick="scrollGame(-142)">&#10094;</div>
    <div class="btn-nav btn-next" onclick="scrollGame(142)">&#10095;</div>
    <div class="game-scroll" id="gameScroll">
        <div class="game-card">
            <img src="https://i.imgur.com/Bt3aCqC.jpeg">
            <div class="game-info">Gates of Olympus</div>
            <div class="rtp-container"><div class="rtp-fill" style="width: 98%; background: #00e676;">98%</div></div>
        </div>
        <div class="game-card">
            <img src="https://i.imgur.com/qI9UKNO.jpeg">
            <div class="game-info">Starlight Princess</div>
            <div class="rtp-container"><div class="rtp-fill" style="width: 97%; background: #00e676;">97%</div></div>
        </div>
        <div class="game-card">
            <img src="https://i.imgur.com/Sh4Y4Jz.jpeg">
            <div class="game-info">Mahjong Ways 2</div>
            <div class="rtp-container"><div class="rtp-fill" style="width: 95%; background: #ffd700;">95%</div></div>
        </div>
        <div class="game-card">
            <img src="https://i.imgur.com/VGBYN8F.jpeg">
            <div class="game-info">Sweet Bonanza</div>
            <div class="rtp-container"><div class="rtp-fill" style="width: 94%; background: #ffd700;">94%</div></div>
        </div>
        <div class="game-card">
            <img src="https://i.imgur.com/0lo0ydJ.jpeg">
            <div class="game-info">Sugar Rush</div>
            <div class="rtp-container"><div class="rtp-fill" style="width: 96%; background: #00e676;">96%</div></div>
        </div>
    </div>
</div>

<div id="chat-btn" onclick="toggleChat(true)">💬</div>
<div id="chat-overlay" onclick="toggleChat(false)"></div>
<div id="chat-popup">
    <div style="background:linear-gradient(90deg,#ffd700,#ff8c00); padding:15px; color:black; font-weight:bold; display:flex; justify-content:space-between;">
        <span>👤 CUSTOMER SERVICE</span>
        <span onclick="toggleChat(false)" style="cursor:pointer; font-size:20px;">&times;</span>
    </div>
    <img src="https://i.supaimg.com/e2052feb-b9dd-4dac-b762-c0dee9b0bd7b/8501f28f-3d3c-4440-8af2-b9a41789e2e6.jpg" style="width:100%;">
    <a href="https://wa.me/6285724785177" target="_blank" class="chat-row"><span>🟢 WhatsApp</span><span class="action-btn">CHAT</span></a>
    <a href="https://t.me/aldiafnd07" target="_blank" class="chat-row"><span>🔵 Telegram</span><span class="action-btn">CHAT</span></a>
    <a href="https://ig.me/m/aldiafnd_" target="_blank" class="chat-row"><span>📸 Instagram</span><span class="action-btn">CHAT</span></a>
    <a href="https://www.facebook.com/aldi.pehul.12" target="_blank" class="chat-row"><span>🔵 Facebook</span><span class="action-btn">CHAT</span></a>
</div>

<script>
// --- 1. Script Slider Atas ---
const slider = document.getElementById('slider');
let idx = 0;
setInterval(() => {
    if (slider) {
        idx = (idx + 1) % 3;
        slider.scrollTo({ left: slider.offsetWidth * idx, behavior: 'smooth' });
    }
}, 4500);

// --- 2. Script Jackpot (Nambah otomatis & Rapi) ---
let jpVal = 8715820442;
setInterval(() => {
    jpVal += Math.floor(Math.random() * 100);
    const jpElement = document.getElementById('jp-val');
    if (jpElement) {
        jpElement.innerText = jpVal.toLocaleString('id-ID');
    }
}, 200);

// --- 3. Script Game Scroll (Hot Game) ---
const gScroll = document.getElementById('gameScroll');
function scrollGame(val) {
    if (gScroll) gScroll.scrollBy({ left: val, behavior: 'smooth' });
}

setInterval(() => {
    if (gScroll) {
        if (gScroll.scrollLeft + gScroll.offsetWidth >= gScroll.scrollWidth - 10) {
            gScroll.scrollTo({ left: 0, behavior: 'smooth' });
        } else {
            gScroll.scrollBy({ left: 142, behavior: 'smooth' });
        }
    }
}, 5000);

// --- 4. Fungsi Live Chat (Tombol Popup) ---
function toggleChat(show) {
    const overlay = document.getElementById('chat-overlay');
    const popup = document.getElementById('chat-popup');
    if (overlay && popup) {
        overlay.style.display = show ? 'block' : 'none';
        popup.style.display = show ? 'block' : 'none';
    }
}
</script>

"""
components.html(fitur_html, height=800)

# --- 7. LOGIN AREA ---
st.markdown("### 🔑 LOGIN UTAMA")
u_m = st.text_input("Username", key="main_u")
p_m = st.text_input("Password", type="password", key="main_p")
if st.button("MASUK SEKARANG", type="primary", use_container_width=True):
    if cek_login(u_m, p_m): st.success("✅ Login Berhasil!"); st.balloons()
    else: st.error("⚠️ Username/Password salah!")

# --- 8. NAVIGASI BAWAH ---
st.markdown("""
<style>
    .nav { position: fixed; bottom: 0; left: 0; width: 100%; height: 75px; background: #111; display: flex; justify-content: space-around; align-items: center; border-top: 2px solid #ffd700; z-index: 999; }
    .nav-item { text-align: center; color: white; font-size: 10px; font-weight: bold; width: 20%; }
    .btn-center { position: fixed; bottom: 25px; left: 50%; transform: translateX(-50%); width: 75px; height: 75px; background: linear-gradient(180deg, #ffd700, #ff8c00); border-radius: 50%; border: 4px solid #111; display: flex; justify-content: center; align-items: center; z-index: 1000; color: black; font-weight: bold; font-size: 11px; box-shadow: 0 0 15px #ffd700; }
</style>
<div class="btn-center">MASUK</div>
<div class="nav">
    <div class="nav-item">🏠<br>HOME</div>
    <div class="nav-item">🎁<br>PROMO</div>
    <div style="width:20%"></div>
    <div class="nav-item">📲<br>APK</div>
    <div class="nav-item" onclick="toggleChat(true)">💬<br>CHAT</div>
</div>
""", unsafe_allow_html=True)

