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

# --- 3. CSS GLOBAL ---
st.markdown("""
<style>
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

# --- 6. LOGIKA MENU & VISUAL (VERSI GACOR) ---
if 'menu_aktif' not in st.session_state:
    st.session_state.menu_aktif = "SLOT"

# CSS pikeun ngaleungitkeun padding standar streamlit sangkan rapih
st.markdown("""<style>.block-container {padding-top: 1rem;}</style>""", unsafe_allow_html=True)
# Cék menu mana anu nuju aktif tina URL
query_params = st.query_params
menu_aktif = query_params.get("menu", "SLOT") # Defaultna SLOT mun kakara buka

fitur_html = """
<style>
    /* CSS Dasar & Reset */
    body { margin: 0; font-family: sans-serif; background: #0c0e12; color: white; }
    
    /* Slider Banner Otomatis */
    .slider-container { width: 100%; overflow: hidden; border-radius: 15px; margin-bottom:10px; }
    .slider { display: flex; overflow-x: auto; scroll-snap-type: x mandatory; scroll-behavior: smooth; }
    .slider::-webkit-scrollbar { display: none; }
    .slider img { width: 100%; flex-shrink: 0; scroll-snap-align: start; }

    /* RGB Marquee */
    .rgb-border {
        margin: 10px 0; padding: 2px; border-radius: 10px;
        background: linear-gradient(90deg, #ff0000, #ffff00, #00ff00, #00ffff, #0000ff, #ff00ff, #ff0000);
        background-size: 400% 400%; animation: rgb-move 5s linear infinite;
    }
    .inner-marquee { background: #1a1d24; border-radius: 8px; padding: 8px; overflow: hidden; }
    .scrolling-text {
        display: inline-block; white-space: nowrap; color: #ffd700; font-weight: bold; font-size: 12px;
        animation: jalan-terus 15s linear infinite;
    }

    /* Scroll Brand Menu (Bisa di-klik) */
    .scroll-container {
        display: flex; overflow-x: auto; white-space: nowrap; gap: 12px; padding: 15px 10px;
        background: rgba(0,0,0,0.6); border-radius: 12px; margin-bottom: 15px;
    }
    .scroll-container::-webkit-scrollbar { display: none; }
    .brand-item { flex: 0 0 auto; width: 65px; text-align: center; cursor: pointer; transition: 0.3s; }
    .brand-item:active { transform: scale(0.9); }
    .brand-item img { width: 55px; height: 55px; border-radius: 50%; border: 2px solid #ffd700; background: #222; margin-bottom: 5px; }
    .brand-item span { color: #ffd700; font-size: 10px; font-weight: bold; display: block; }

    /* Winner Box & JP */
    .winner-box { background: rgba(26, 29, 36, 0.95); border-radius: 12px; border: 1px solid #333; padding: 10px; margin-bottom: 10px; }
    .win-content { display: flex; justify-content: space-between; color: white; font-size: 11px; margin-top: 5px; }
    .jp-wrapper { background: #000; border: 2px solid #ffd700; border-radius: 10px; padding: 8px; text-align: center; }
    .jp-num { color: #ff0000; font-size: 22px; font-weight: 900; text-shadow: 0 0 5px rgba(255,0,0,0.5); }

    /* Animations */
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
        <div class="scrolling-text">🔥 SELAMAT DATANG DI S2 SEJATI SLOT - SITUS GACOR TERPERCAYA - PROSES DEPO & WD TERCEPAT! 🔥</div>
    </div>
</div>
<div class="scroll-container">
    <div class="brand-item" onclick="window.parent.location.href='?menu=SLOT'">
        <img src="https://akongads.store/images/menu-icon/slot.webp"><br>SLOT
    </div>
    <div class="brand-item" onclick="window.parent.location.href='?menu=CASINO'">
        <img src="https://i.ibb.co/S769989/pragmatic.png"><br>CASINO
    </div>
    <div class="brand-item" onclick="window.parent.location.href='?menu=SPORT'">
        <img src="https://i.ibb.co/0YmYVf8/pgsoft.png"><br>SPORT+
    </div>
    <div class="brand-item" onclick="window.parent.location.href='?menu=TOGEL'">
        <img src="https://i.ibb.co/XW3px3P/habanero.png"><br>TOGEL
    </div>
    <div class="brand-item" onclick="window.parent.location.href='?menu=IKAN'">
        <img src="https://i.ibb.co/fM8vXz3/joker.png"><br>IKAN
    </div>
</div>
<div class="winner-box">
    <div style="color:#ffd700; font-size:11px; font-weight:bold; border-bottom:1px solid #333; padding-bottom:5px;">🏆 LIVE WINNER REAL-TIME</div>
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

<script>
    // Logic Kirim Menu ka Streamlit
    function sendMenu(val) {
        window.parent.postMessage({type: 'set_menu', value: val}, '*');
    }

    // Slider Otomatis
    let sIdx = 0; setInterval(() => { 
        sIdx = (sIdx + 1) % 3; 
        const s = document.getElementById('mainSlider');
        if(s) s.scrollTo({left: sIdx * s.clientWidth, behavior: 'smooth'});
    }, 3000);

    // Winner Box Update
    const us = ["J***p", "R***ky", "S2***ot", "A***ng", "M***ky"];
    const gs = ["Olympus", "Mahjong 2", "Princess"];
    setInterval(() => {
        document.getElementById('u-win').innerText = us[Math.floor(Math.random()*us.length)];
        document.getElementById('g-win').innerText = "[" + gs[Math.floor(Math.random()*gs.length)] + "]";
        document.getElementById('a-win').innerText = "IDR " + (Math.floor(Math.random()*5000)+100) + ".000";
    }, 3000);

    // Jackpot Counter
    let jVal = 8715784119; setInterval(() => { 
        jVal += Math.floor(Math.random()*5000); 
        document.getElementById('jp-val').innerText = jVal.toLocaleString('id-ID'); 
    }, 100);
</script>
"""

# Handle Menu ti HTML
from streamlit_gsheets import GSheetsConnection # Conto bisi peryogi, mun henteu keun wae
import streamlit.components.v1 as components

# Ieu penting sangkan bisa nangkep klik tina HTML
st.components.v1.html(fitur_html, height=480)

# KUMPULAN GAME (MANUAL & OTOMATIS SCROLL)
st.subheader(f"🎮 DAFTAR GAME {st.session_state.menu_aktif}")

def list_game_scroll(daftar):
    # CSS pikeun game card
    game_style = """
    <style>
        .g-container { display: flex; overflow-x: auto; gap: 12px; padding: 10px 5px; }
        .g-container::-webkit-scrollbar { display: none; }
        .g-card { flex: 0 0 auto; width: 110px; background: #1a1d24; border: 1px solid #333; border-radius: 10px; text-align: center; padding: 8px; }
        .g-card img { width: 100%; border-radius: 8px; margin-bottom: 5px; border: 1px solid #444; }
        .g-card p { color: #eee; font-size: 10px; margin: 0; font-weight: bold; overflow: hidden; white-space: nowrap; }
    </style>
    """
    items = "".join([f'<div class="g-card"><img src="{i["img"]}"><p>{i["nama"]}</p></div>' for i in daftar])
    components.html(game_style + f'<div class="g-container">{items}</div>', height=160)
st.markdown(f"### 🎰 {menu_aktif} GAMES")

# Wadah Scroll Gambar Game
if menu_aktif == "SLOT":
    # Ieu daptar brand slot saperti dina video
    slot_brands = [
        "https://i.ibb.co/S769989/pragmatic.png",
        "https://i.ibb.co/0YmYVf8/pgsoft.png",
        "https://i.ibb.co/XW3px3P/habanero.png",
        "https://i.ibb.co/fM8vXz3/joker.png",
        "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTzR_eYp-o6T-0W-KqS-6Q6W_U&s" # CQ9
    ]
    
    # Bikin scroll horizontal manual pake HTML
    game_list_html = f"""
    <div style="display: flex; overflow-x: auto; gap: 10px; padding: 10px;">
        {''.join([f'<img src="{link}" style="width:100px; height:100px; border-radius:10px; border:1px solid #ffd700;">' for link in slot_brands])}
    </div>
    """
    st.components.v1.html(game_list_html, height=130)

elif menu_aktif == "CASINO":
    st.write("Daptar Live Casino...")
    # Tambahkeun gambar brand Casino di dieu

elif menu_aktif == "SPORT":
    st.write("Daptar Sportbook...")
    # Tambahkeun gambar brand Sport di dieu

# DATA GAME DUMASAR MENU
if st.session_state.menu_aktif == "SLOT":
    data = [
        {"nama": "Pragmatic", "img": "https://i.ibb.co/S769989/pragmatic.png"},
        {"nama": "PG Soft", "img": "https://i.ibb.co/0YmYVf8/pgsoft.png"},
        {"nama": "Habanero", "img": "https://i.ibb.co/XW3px3P/habanero.png"},
        {"nama": "Microgame", "img": "https://i.ibb.co/fM8vXz3/joker.png"},
        {"nama": "CQ9", "img": "https://akongads.store/images/menu-icon/slot.webp"}
    ]
    list_game_scroll(data)

elif st.session_state.menu_aktif == "CASINO":
    data = [
        {"nama": "Live Casino", "img": "https://i.ibb.co/S769989/pragmatic.png"},
        {"nama": "Baccarat", "img": "https://i.ibb.co/0YmYVf8/pgsoft.png"}
    ]
    list_game_scroll(data)

# ... tambahkeun menu liana (TOGEL, IKAN, SPORT) di dieu

# --- 7. INPUT LOGIN TENGAH ---
st.markdown("### 🔑 LOGIN UTAMA")
st.text_input("Username", key="m_u")
st.text_input("Password", type="password", key="m_p")
st.button("MASUK SEKARANG", type="primary", use_container_width=True)

# --- 9. NAVIGASI BAR BAWAH ---
st.markdown("""
<style>
    .nav-container {
        position: fixed; bottom: 0; left: 0; width: 100%; height: 75px;
        background: #111; display: flex; justify-content: space-around;
        align-items: center; border-top: 2px solid #ffd700; z-index: 9999;
    }
    .floating-center {
        position: fixed; bottom: 25px; left: 50%; transform: translateX(-50%);
        width: 75px; height: 75px; background: linear-gradient(180deg, #ffd700, #b8860b);
        border-radius: 50%; border: 4px solid #111; display: flex; justify-content: center;
        align-items: center; z-index: 10000; box-shadow: 0 0 15px #ffd700;
    }
    .nav-link { text-align: center; color: white; text-decoration: none; width: 20%; font-size: 10px; }
</style>
<div class="floating-center" onclick="window.parent.location.reload();"><b style="color:black; font-size:11px;">MASUK</b></div>
<div class="nav-container">
    <div class="nav-link">🏠<br>HOME</div>
    <div class="nav-link">🎁<br>PROMO</div>
    <div style="width: 20%;"></div>
    <div class="nav-link">📲<br>APK</div>
    <div class="nav-link" onclick="document.getElementById('btn-chat-s2').click()">💬<br>CHAT</div>
</div>
""", unsafe_allow_html=True)

