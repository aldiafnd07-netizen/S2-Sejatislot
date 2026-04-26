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

# --- 3. CSS & VIDEO BACKGROUND ---
def get_base64_video():
    nama_video = "undefined - Imgur.mp4"
    paths = [nama_video, f"/sdcard/Download/{nama_video}"]
    for p in paths:
        if os.path.exists(p):
            with open(p, "rb") as f:
                return base64.b64encode(f.read()).decode()
    return None

bin_str = get_base64_video()

if bin_str:
    st.markdown(f'''
    <style>
        header, footer, #MainMenu, .stDeployButton {{ visibility: hidden !important; }}
        .stApp {{ background: transparent !important; }}
        #video-container {{ position: fixed; top: 0; left: 0; width: 100%; height: 100%; z-index: -1; overflow: hidden; }}
        #bg-video {{ width: 100%; height: 100%; object-fit: cover; }}
        .block-container {{ padding: 0.5rem !important; padding-bottom: 160px !important; background-color: rgba(0,0,0,0.5); }}
    </style>
    <div id="video-container">
        <video autoplay loop muted playsinline id="bg-video">
            <source src="data:video/mp4;base64,{bin_str}" type="video/mp4">
        </video>
    </div>
    ''', unsafe_allow_html=True)
else:
    st.markdown('<style>header, footer, #MainMenu, .stDeployButton { visibility: hidden !important; }</style>', unsafe_allow_html=True)

# Styling Global Input & Tombol
st.markdown("""
<style>
    .stTextInput input { background-color: rgba(26, 29, 36, 0.9) !important; color: #00e676 !important; border: 1px solid #ffd700 !important; }
    div.stButton > button[kind="primary"] {
        background: linear-gradient(180deg, #00e676 0%, #00c853 100%) !important;
        color: white !important; font-weight: 800 !important;
        border: 2px solid #ffd700 !important; border-radius: 12px !important;
    }
</style>
""", unsafe_allow_html=True)

# --- 4. POPUP DIALOGS ---
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

# --- 5. HEADER & TOP NAV ---
c1, c2 = st.columns([2, 1])
with c1: st.image("https://i.imgur.com/pjj1xQo.png", width=200)
with c2:
    if st.button("MASUK", use_container_width=True): login_dialog()
    if st.button("DAFTAR", use_container_width=True): register_dialog()

# --- 6. GAME MAHJONG WAYS 3+ (SISIPAN BARU) ---
st.markdown("<h3 style='color: #FFD700; text-align: center; margin-top: 10px;'>🎰 MAHJONG WAYS 3+ DEMO</h3>", unsafe_allow_html=True)
SOURCE_GAME = "https://demogamesfree.5ggames.top/gs2c/openGame.do?gameSymbol=vs20mahjong3"
game_html = f"""
<div style="position: relative; width: 100%; padding-top: 160%; overflow: hidden; border: 2px solid #FFD700; border-radius: 15px; margin-bottom: 20px;">
    <iframe src="{SOURCE_GAME}" 
            style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: none;"
            allow="autoplay; fullscreen; encrypted-media" allowfullscreen>
    </iframe>
</div>
"""
components.html(game_html, height=650)

# --- 7. HTML KOMPONEN LENGKAP (SLIDER, JP, & GAME LIST) ---
fitur_html = """
<style>
    .s-container { width: 100%; overflow: hidden; border-radius: 15px; border: 2px solid #ffd700; position: relative; margin-top: 10px; }
    .s-wrapper { display: flex; overflow-x: auto; scroll-snap-type: x mandatory; scrollbar-width: none; }
    .s-wrapper::-webkit-scrollbar { display: none; }
    .s-wrapper img { width: 100%; flex-shrink: 0; scroll-snap-align: start; }
    .marquee-rgb { margin-top: 10px; padding: 3px; border-radius: 10px; background: linear-gradient(90deg, red, yellow, lime, cyan, blue, magenta, red); background-size: 400%; animation: rgb 5s linear infinite; }
    .marquee-inner { background: #1a1d24; border-radius: 8px; padding: 10px; overflow: hidden; }
    .m-text { display: inline-block; white-space: nowrap; color: #ffd700; font-weight: bold; animation: jalan 15s linear infinite; }
    .jp-card { background: #000; border: 2px solid #ffd700; border-radius: 15px; padding: 10px; text-align: center; margin-top: 10px; }
    .jp-text { color: red; font-size: 24px; font-weight: 900; text-shadow: 0 0 5px red; font-family: monospace; }
    .game-section { position: relative; margin-top: 15px; }
    .game-header { color: gold; font-weight: bold; font-size: 14px; margin-bottom: 8px; }
    .game-scroll { display: flex; overflow-x: auto; gap: 12px; scrollbar-width: none; }
    .game-card { flex: 0 0 130px; background: #111; border: 1px solid gold; border-radius: 12px; overflow: hidden; }
    .game-card img { width: 100%; height: 130px; object-fit: cover; }
    .rtp-fill { height: 100%; display: flex; align-items: center; justify-content: center; font-size: 10px; color: black; font-weight: bold; border-radius: 20px; }
    #chat-btn { position: fixed; bottom: 100px; right: 20px; width: 60px; height: 60px; background: radial-gradient(circle, #ffd700, #ff8c00); border-radius: 50%; display: flex; justify-content: center; align-items: center; font-size: 30px; z-index: 999; border: 2px solid white; box-shadow: 0 0 15px gold; cursor: pointer; }
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
    <div class="marquee-inner"><div class="m-text">🔥 S2 SEJATI - SITUS GACOR TERPERCAYA - WD BERAPAPUN PASTI DIBAYAR LUNAS 🔥</div></div>
</div>

<div class="jp-card">
    <div style="color:#ffd700; font-size:10px; font-weight:bold;">✨ PROGRESSIVE JACKPOT ✨</div>
    <div class="jp-text">RP <span id="jp-val">8.715.820.442</span></div>
</div>

<div class="game-section">
    <div class="game-header">🎰 GAME HOT HARI INI</div>
    <div class="game-scroll">
        <div class="game-card"><img src="https://i.imgur.com/Bt3aCqC.jpeg"><div style="background:#333; height:16px; margin:5px;"><div class="rtp-fill" style="width:98%; background:#00e676;">98%</div></div></div>
        <div class="game-card"><img src="https://i.imgur.com/qI9UKNO.jpeg"><div style="background:#333; height:16px; margin:5px;"><div class="rtp-fill" style="width:97%; background:#00e676;">97%</div></div></div>
        <div class="game-card"><img src="https://i.imgur.com/Sh4Y4Jz.jpeg"><div style="background:#333; height:16px; margin:5px;"><div class="rtp-fill" style="width:95%; background:#ffd700;">95%</div></div></div>
    </div>
</div>

<script>
    const slider = document.getElementById('slider');
    let idx = 0;
    setInterval(() => { if(slider){ idx = (idx + 1) % 3; slider.scrollTo({left: slider.offsetWidth * idx, behavior: 'smooth'}); }}, 4500);
    
    let jpVal = 8715820442;
    setInterval(() => { 
        jpVal += Math.floor(Math.random() * 100);
        document.getElementById('jp-val').innerText = jpVal.toLocaleString('id-ID');
    }, 200);
</script>
"""
components.html(fitur_html, height=550)

# --- 8. LOGIN AREA UTAMA ---
st.markdown("### 🔑 LOGIN UTAMA")
u_m = st.text_input("Username", key="main_u")
p_m = st.text_input("Password", type="password", key="main_p")
if st.button("MASUK SEKARANG", type="primary", use_container_width=True):
    if cek_login(u_m, p_m): st.success("✅ Login Berhasil!"); st.balloons()
    else: st.error("⚠️ Username/Password salah!")

# --- 9. NAVIGASI BAWAH (FOOTER) ---
st.markdown("""
<style>
    .nav { position: fixed; bottom: 0; left: 0; width: 100%; height: 75px; background: #111; display: flex; align-items: center; border-top: 2px solid #ffd700; z-index: 1000; }
    .nav-item { text-align: center; color: white; font-size: 10px; font-weight: bold; width: 20%; }
    .btn-center { position: fixed; bottom: 25px; left: 50%; transform: translateX(-50%); width: 75px; height: 75px; background: radial-gradient(circle, #00e676, #00c853); border: 4px solid #ffd700; border-radius: 50%; display: flex; justify-content: center; align-items: center; color: white; font-weight: 900; font-size: 12px; z-index: 1001; box-shadow: 0 0 20px #00e676; }
</style>
<div class="btn-center">MASUK</div>
<div class="nav">
    <div class="nav-item">🏠<br>HOME</div>
    <div class="nav-item">🎁<br>PROMO</div>
    <div style="width:20%"></div>
    <div class="nav-item">📲<br>APK</div>
    <div class="nav-item">💬<br>CHAT</div>
</div>
""", unsafe_allow_html=True)

