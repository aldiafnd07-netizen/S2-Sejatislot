import streamlit as st
import streamlit.components.v1 as components
import sqlite3
import random

# --- 1. SETTING HALAMAN ---
st.set_page_config(page_title="S2 SEJATISLOT", layout="centered")

if "halaman" not in st.session_state:
    st.session_state.halaman = "home"

def pindah_halaman(nama_hal):
    st.session_state.halaman = nama_hal
    st.rerun()

# --- 2. SISTEM DATABASE ---
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

# --- 3. CSS GLOBAL ---
st.markdown("""
<style>
    header, footer, #MainMenu, .stDeployButton { visibility: hidden !important; display: none !important; }
    .stApp {
        background-image: url("https://i.imgur.com/0sCszBw.png");
        background-attachment: fixed; background-size: cover; background-position: center;
    }
    .block-container { padding: 0.5rem !important; padding-bottom: 120px !important; }
    .stTextInput input, .stSelectbox div[data-baseweb="select"] {
        background-color: rgba(26, 29, 36, 0.9) !important;
        color: #00e676 !important;
        border: 1px solid #00e676 !important;
    }
    div.stButton > button[kind="primary"] {
        background: linear-gradient(180deg, #00e676 0%, #00c853 100%) !important;
        color: white !important; font-weight: 800 !important;
        border: 2px solid #ffd700 !important; border-radius: 12px !important;
    }
</style>
""", unsafe_allow_html=True)

# --- 4. LOGIKA HALAMAN ---

# --- A. HALAMAN CHAT AI ---
if st.session_state.halaman == "chat_ai":
    if st.button("⬅️ BALIK KA LOBBY"):
        pindah_halaman("home")

    st.markdown("""
    <div style="background: linear-gradient(90deg, #ffd700, #b8860b); padding: 15px; border-radius: 10px 10px 0 0; color: #000; font-weight: bold; text-align: center;">
        🎧 CS S2 SEJATISLOT (AI Support)
    </div>
    <div style="background: #1a1a1a; padding: 15px; border: 1px solid #ffd700; color: #fff; font-size: 13px; text-align: center; margin-bottom: 20px;">
        S2 SEJATISLOT LIVECHAT 🔥<br>
        BONUS NEW MEMBER 100%<br>
        KHUSUS SLOT JANGAN LUPA KLAIM BOSKU!!
    </div>
    """, unsafe_allow_html=True)

    user_id_ai = st.text_input("USER ID *", placeholder="S2sejatislot", key="ai_user_id")
    st.write("Masalah apa yang perlu kita bantu bosku? *")
    st.checkbox("PROSES DEPOSIT")
    st.checkbox("PROSES WITHDRAW")
    st.checkbox("KLAIM BONUS FREESPIN")
    st.checkbox("ERROR PERMAINAN")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Ketik pesan di sini..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        resp = f"Halo Boss {user_id_ai if user_id_ai else 'Member'}, abdi AI S2. Keluhan '{prompt}' nuju dicek ku tim terkait. Mangga antos sakedap!"
        st.session_state.messages.append({"role": "assistant", "content": resp})
        with st.chat_message("assistant"):
            st.markdown(resp)

# --- B. HALAMAN HOME ---
else:
    # Dialogs
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
        v_code = str(random.randint(1000, 9999))
        st.markdown(f"**Kode Validasi: :red[{v_code}]**")
        v_in = st.text_input("* Masukkan Kode", key="reg_v")
        if st.button("DAFTAR SEKARANG", type="primary", use_container_width=True):
            if p != p2: st.error("❌ Kata sandi tidak cocok!")
            elif v_in != v_code: st.error("❌ Kode validasi salah!")
            elif u and p and nr and na:
                if simpan_pendaftar(u, p, e, t, b, nr, na, ref):
                    st.success("✅ Berhasil! Silakan Login.")
                else:
                    st.error("⚠️ Username sudah ada!")

    # Top Navigation
    c1, c2 = st.columns([2, 1])
    with c1: st.image("https://i.imgur.com/pjj1xQo.png", width=200)
    with c2:
        if st.button("MASUK", use_container_width=True): login_dialog()
        if st.button("DAFTAR", use_container_width=True): register_dialog()

    m_aktif = st.query_params.get("m", "SLOT")
# --- 6. FITUR VISUAL (VIDEO BANNER & MARQUEE) ---
fitur_html = f"""
<style>
    .main-container {{
        width: 100%;
        display: flex;
        flex-direction: column;
        align-items: center; /* Ngatengahkeun sadayana */
    }}
    
    .video-container {{
        width: 100%;
        max-width: 500px; /* Supados teu ageung teuing di HP */
        overflow: hidden;
        border-radius: 15px;
        border: 2px solid #ffd700;
        box-shadow: 0 0 15px rgba(255, 215, 0, 0.3);
    }}

    video {{
        width: 100%;
        display: block;
    }}

    .rgb-border {{
        width: 100%;
        margin-top: 10px; padding: 3px; border-radius: 10px;
        background: linear-gradient(90deg, #ff0000, #ffff00, #00ff00, #00ffff, #0000ff, #ff00ff, #ff0000);
        background-size: 400% 400%; animation: rgb-move 5s linear infinite;
    }}
    .inner-marquee {{ background: #1a1d24; border-radius: 8px; padding: 10px; overflow: hidden; }}
    .scrolling-text {{ 
        display: inline-block; white-space: nowrap; color: #ffd700; 
        font-weight: bold; animation: jalan-terus 15s linear infinite; 
    }}

    @keyframes rgb-move {{ 0%{{background-position:0% 50%}} 100%{{background-position:100% 50%}} }}
    @keyframes jalan-terus {{ from {{ transform: translateX(100%); }} to {{ transform: translateX(-100%); }} }}
</style>

<div class="main-container">
    <div class="video-container">
        <video autoplay muted loop playsinline>
            <source src="https://files.catbox.moe/6v0m9i.mp4" type="video/mp4">
            Your browser does not support the video tag.
        </video>
    </div>

    <div class="rgb-border">
        <div class="inner-marquee">
            <div class="scrolling-text">🔥 SELAMAT DATANG DI S2 SEJATI SLOT SITUS GACOR AMAN TERPERCAYA - PROSES DEPO & WD PASTI DIBAYAR TERCEPAT SE-INDONESIA - SALAM JP BOSS🔥</div>
        </div>
    </div>
</div>
"""
components.html(fitur_html, height=350)


    # Game Scroll Section
    st.markdown(f"#### 🎮 GAME TERPOPULER: {m_aktif}")
    game_list = [
        {"n": "Pragmatic", "i": "https://i.ibb.co/S769989/pragmatic.png"},
        {"n": "PG Soft", "i": "https://akongads.store/images/menu-icon/slot.webp"}
    ]
    game_scroll = f"""
    <div style="display: flex; overflow-x: auto; gap: 12px; padding: 10px;">
        {''.join([f'<div style="flex:0 0 auto; width:100px; text-align:center;"><img src="{g["i"]}" style="width:80px; border-radius:10px; border:1px solid #ffd700;"><br><span style="color:white; font-size:10px;">{g["n"]}</span></div>' for g in game_list])}
    </div>
    """
    components.html(game_scroll, height=150)

    # Main Login Form
    st.markdown("### 🔑 LOGIN UTAMA")
    st.text_input("Username", key="main_u")
    st.text_input("Password", type="password", key="main_p")
    st.button("MASUK SEKARANG", type="primary", use_container_width=True)

    # Floating AI Button at Home
    if st.button("🤖 CHAT SUPPORT AI"):
        pindah_halaman("chat_ai")

# --- 9. NAVIGASI BAWAH + POPUP LIVE CHAT (VERSI FIX ANTI-ERROR) ---
footer_pro = f"""
<style>
    /* Sembunyikan Checkbox Logika */
    #toggle-chat {{ display: none; }}

    /* Tombol Chat Melayang */
    .btn-chat-float {{
        position: fixed; bottom: 90px; right: 20px;
        width: 60px; height: 60px;
        background: linear-gradient(180deg, #ffd700, #ff8c00);
        border-radius: 50%; display: flex; justify-content: center; align-items: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.6); cursor: pointer; z-index: 100000;
        animation: pulse-gold 2s infinite; border: 2px solid #fff;
    }}
    .btn-chat-float img {{ width: 30px; }}

    @keyframes pulse-gold {{
        0% {{ box-shadow: 0 0 0 0 rgba(255, 215, 0, 0.7); }}
        70% {{ box-shadow: 0 0 0 15px rgba(255, 215, 0, 0); }}
        100% {{ box-shadow: 0 0 0 0 rgba(255, 215, 0, 0); }}
    }}

    /* Overlay Layar Gelap */
    .chat-overlay {{
        position: fixed; top: 0; left: 0; width: 100%; height: 100%;
        background: rgba(0,0,0,0.8); z-index: 100001;
        opacity: 0; visibility: hidden; transition: 0.3s;
    }}

    /* Kotak Popup Menu */
    .chat-box {{
        position: fixed; top: 50%; left: 50%;
        transform: translate(-50%, -50%) scale(0.8);
        width: 300px; background: #111;
        border: 2px solid #ffd700; border-radius: 15px; z-index: 100002;
        opacity: 0; visibility: hidden; transition: 0.3s;
        overflow: hidden;
    }}

    /* Logika Buka Tutup */
    #toggle-chat:checked ~ .chat-overlay {{ opacity: 1; visibility: visible; }}
    #toggle-chat:checked ~ .chat-box {{ opacity: 1; visibility: visible; transform: translate(-50%, -50%) scale(1); }}

    .chat-header {{
        background: linear-gradient(90deg, #ffd700, #b8860b);
        color: #000; padding: 12px; font-weight: bold;
        display: flex; justify-content: space-between; align-items: center;
    }}

    .sosmed-container {{ padding: 15px; background: #1a1a1a; }}
    .sosmed-item {{
        display: flex; justify-content: space-between; align-items: center;
        background: #222; margin-bottom: 10px; padding: 12px;
        border-radius: 8px; text-decoration: none; border: 1px solid #333;
    }}
    .sosmed-left {{ display: flex; align-items: center; gap: 10px; color: #fff; font-size: 14px; font-weight: bold; }}

    /* Navigasi Bar Bawah */
    .nav-container {{
        position: fixed; bottom: 0; left: 0; width: 100%; height: 70px;
        background: #111; display: flex; justify-content: space-around;
        align-items: center; border-top: 2px solid #ffd700; z-index: 99999;
    }}
    .nav-item {{ text-align: center; color: #fff; font-size: 10px; text-decoration: none; cursor: pointer; }}
</style>

<input type="checkbox" id="toggle-chat">

<label for="toggle-chat" class="btn-chat-float">
    <img src="https://cdn-icons-png.flaticon.com/512/5968/5968771.png">
</label>

<label for="toggle-chat" class="chat-overlay"></label>

<div class="chat-box">
    <div class="chat-header">
        <span>🎧 CS S2 SEJATISLOT</span>
        <label for="toggle-chat" style="cursor:pointer;">✕</label>
    </div>
    <div class="sosmed-container">
        <a href="https://wa.me/6285724785177" target="_blank" class="sosmed-item">
            <div class="sosmed-left">
                <img src="https://upload.wikimedia.org/wikipedia/commons/6/6b/WhatsApp.svg" width="20">
                <span>WhatsApp</span>
            </div>
            <div style="color:#ffd700; font-size:10px;">HUBUNGI</div>
        </a>
        <a href="https://t.me/aldiafnd07" target="_blank" class="sosmed-item">
            <div class="sosmed-left">
                <img src="https://upload.wikimedia.org/wikipedia/commons/8/82/Telegram_logo.svg" width="20">
                <span>Telegram</span>
            </div>
            <div style="color:#ffd700; font-size:10px;">HUBUNGI</div>
        </a>
        <a href="https://facebook.com/aldi.pehul.12" target="_blank" class="sosmed-item">
            <div class="sosmed-left">
                <img src="https://upload.wikimedia.org/wikipedia/commons/b/b8/2021_Facebook_icon.svg" width="20">
                <span>Facebook</span>
            </div>
            <div style="color:#ffd700; font-size:10px;">HUBUNGI</div>
        </a>
    </div>
</div>

<div class="nav-container">
    <div class="nav-item" onclick="window.parent.location.reload()">🏠<br>HOME</div>
    <div class="nav-item">🎁<br>PROMO</div>
    <div style="background:#ffd700; width:60px; height:60px; border-radius:50%; border:4px solid #111; margin-top:-30px; display:flex; justify-content:center; align-items:center; color:#000; font-weight:bold; cursor:pointer;" onclick="window.parent.location.reload()">MASUK</div>
    <div class="nav-item">💰<br>DEPO</div>
    <label for="toggle-chat" class="nav-item">🎧<br>CHAT</label>
</div>
"""
components.html(footer_pro, height=100)

