import streamlit as st
import streamlit.components.v1 as components
import sqlite3
import random

# --- 1. SETTING HALAMAN & NAVIGASI ---
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

# --- 3. CSS GLOBAL (PREMIUM STYLE) ---
st.markdown("""
<style>
    header, footer, #MainMenu, .stDeployButton { visibility: hidden !important; display: none !important; }
    .stApp {
        background-image: url("https://i.imgur.com/0sCszBw.png");
        background-attachment: fixed; background-size: cover; background-position: center;
    }
    .block-container { padding: 0.5rem !important; padding-bottom: 120px !important; }
    
    /* Input Style */
    .stTextInput input, .stSelectbox div[data-baseweb="select"] {
        background-color: rgba(26, 29, 36, 0.9) !important;
        color: #00e676 !important;
        border: 1px solid #00e676 !important;
    }
    
    /* Button Style */
    div.stButton > button {
        border-radius: 8px !important;
    }
    div.stButton > button[kind="primary"] {
        background: linear-gradient(180deg, #00e676 0%, #00c853 100%) !important;
        color: white !important; font-weight: 800 !important;
        border: 2px solid #ffd700 !important;
    }
    
    /* Tombol Floating AI di Home */
    .float-ai-btn {
        position: fixed; bottom: 170px; right: 20px;
        width: 60px; height: 60px; background: #007bff;
        border-radius: 50%; display: flex; justify-content: center;
        align-items: center; z-index: 9999; cursor: pointer;
        box-shadow: 0 4px 15px rgba(0,123,255,0.5);
        border: 2px solid white; color: white; font-size: 30px;
    }
</style>
""", unsafe_allow_html=True)

# --- 4. LOGIKA HALAMAN ---

# --- HALAMAN CHAT AI ---
if st.session_state.halaman == "chat_ai":
    if st.button("⬅️ KEMBALI KE LOBBY"):
        pindah_halaman("home")

    st.markdown("""
    <div style="background: linear-gradient(90deg, #ffd700, #b8860b); padding: 15px; border-radius: 10px 10px 0 0; color: #000; font-weight: bold; text-align: center;">
        🎧 CS S2 SEJATISLOT (AI Support 24/7)
    </div>
    <div style="background: #1a1a1a; padding: 15px; border: 1px solid #ffd700; color: #fff; font-size: 13px; text-align: center; margin-bottom: 20px;">
        <span style="color: #ffd700; font-weight: bold;">S2 SEJATISLOT LIVECHAT 🔥</span><br>
        PROSES DEPO/WD KILAT | BONUS NEW MEMBER 100%<br>
        SILAKAN HUBUNGI AI KAMI JIKA ADA KENDALA
    </div>
    """, unsafe_allow_html=True)

    user_id = st.text_input("MASUKKAN USER ID *", placeholder="Contoh: S2SejatiSlot88")
    
    st.write("**Apa kendala Anda hari ini?**")
    c1, c2 = st.columns(2)
    with c1:
        st.checkbox("PROSES DEPOSIT")
        st.checkbox("PROSES WITHDRAW")
    with c2:
        st.checkbox("KLAIM BONUS")
        st.checkbox("LUPA PASSWORD")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ketik pesan di sini..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        response = f"Halo Boss **{user_id if user_id else 'Member S2'}**, keluhan '{prompt}' sedang kami proses. Mohon tunggu sebentar ya bosku!"
        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(response)

# --- HALAMAN HOME (UTAMA) ---
else:
    # Floating Button AI Shortcut
    if st.button("🤖", help="Chat AI Support"):
        pindah_halaman("chat_ai")

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

    # Header
    c1, c2 = st.columns([2, 1])
    with c1: st.image("https://i.imgur.com/pjj1xQo.png", width=200)
    with c2:
        if st.button("MASUK", use_container_width=True): login_dialog()
        if st.button("DAFTAR", use_container_width=True): register_dialog()

    # Banner & Marquee
    m_aktif = st.query_params.get("m", "SLOT")
    
    fitur_html = f"""
    <style>
        .slider-container {{ width: 100%; overflow: hidden; border-radius: 15px; }}
        .slider {{ display: flex; overflow-x: auto; scroll-snap-type: x mandatory; }}
        .slider img {{ width: 100%; flex-shrink: 0; }}
        .rgb-border {{ margin-top: 10px; padding: 3px; border-radius: 10px; background: linear-gradient(90deg, #ff0000, #ffff00, #00ff00, #00ffff, #0000ff, #ff00ff, #ff0000); background-size: 400% 400%; animation: rgb-move 5s linear infinite; }}
        .inner-marquee {{ background: #1a1d24; border-radius: 8px; padding: 10px; overflow: hidden; }}
        .scrolling-text {{ display: inline-block; white-space: nowrap; color: #ffd700; font-weight: bold; animation: jalan-terus 15s linear infinite; }}
        @keyframes jalan-terus {{ from {{ transform: translateX(100%); }} to {{ transform: translateX(-100%); }} }}
        @keyframes rgb-move {{ 0%{{background-position:0% 50%}} 100%{{background-position:100% 50%}} }}
    </style>
    <div class="slider-container"><div class="slider"><img src="https://i.imgur.com/IA1m2GF.png"></div></div>
    <div class="rgb-border"><div class="inner-marquee"><div class="scrolling-text">🔥 SELAMAT DATANG DI S2 SEJATI SLOT - SITUS TERPERCAYA ANTI RUNGKAT 🔥</div></div></div>
    """
    components.html(fitur_html, height=220)

    # Game Categories
    st.markdown("### 🎮 KATEGORI GAME")
    col_g = st.columns(4)
    with col_g[0]: st.button("🎰 SLOT", use_container_width=True)
    with col_g[1]: st.button("🃏 CASINO", use_container_width=True)
    with col_g[2]: st.button("⚽ SPORT", use_container_width=True)
    with col_g[3]: st.button("🔢 TOGEL", use_container_width=True)

    # Login Form Utama
    st.markdown("---")
    st.markdown("### 🔑 LOGIN MEMBER")
    st.text_input("Username", key="main_u")
    st.text_input("Password", type="password", key="main_p")
    st.button("MASUK SEKARANG", type="primary", use_container_width=True)

# --- 9. NAVIGASI BAWAH + POPUP LIVE CHAT ---
footer_html = f"""
<style>
    #toggle-chat {{ display: none; }}
    .btn-chat-float {{
        position: fixed; bottom: 95px; right: 20px;
        width: 65px; height: 65px;
        background: linear-gradient(180deg, #ffd700, #ff8c00);
        border-radius: 50%; display: flex; justify-content: center; align-items: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.6); cursor: pointer; z-index: 100000;
        animation: pulse-gold 2s infinite; border: 2px solid #fff;
    }}
    @keyframes pulse-gold {{
        0% {{ box-shadow: 0 0 0 0 rgba(255, 215, 0, 0.7); }}
        70% {{ box-shadow: 0 0 0 15px rgba(255, 215, 0, 0); }}
        100% {{ box-shadow: 0 0 0 0 rgba(255, 215, 0, 0); }}
    }}
    .chat-box {{
        position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%);
        width: 300px; background: #111; border: 2px solid #ffd700; border-radius: 15px;
        z-index: 100002; display: none; overflow: hidden;
    }}
    #toggle-chat:checked ~ .chat-box {{ display: block; }}
    .nav-container {{
        position: fixed; bottom: 0; left: 0; width: 100%; height: 70px;
        background: #111; display: flex; justify-content: space-around;
        align-items: center; border-top: 2px solid #ffd700; z-index: 99999;
    }}
</style>

<input type="checkbox" id="toggle-chat">
<label for="toggle-chat" class="btn-chat-float">
    <img src="https://cdn-icons-png.flaticon.com/512/5968/5968771.png" width="35">
</label>

<div class="chat-box">
    <div style="background:#ffd700; color:black; padding:10px; font-weight:bold; display:flex; justify-content:space-between;">
        <span>CS S2 SEJATISLOT</span>
        <label for="toggle-chat" style="cursor:pointer;">✖</label>
    </div>
    <div style="padding:15px; text-align:center;">
        <a href="https://wa.me/6285724785177" style="display:block; background:#25d366; color:white; padding:10px; margin-bottom:10px; text-decoration:none; border-radius:5px;">WhatsApp</a>
        <a href="https://t.me/aldiafnd07" style="display:block; background:#0088cc; color:white; padding:10px; text-decoration:none; border-radius:5px;">Telegram</a>
    </div>
</div>

<div class="nav-container">
    <div style="color:white; text-align:center; font-size:10px;">🏠<br>HOME</div>
    <div style="color:white; text-align:center; font-size:10px;">🎁<br>PROMO</div>
    <div style="background:#ffd700; width:60px; height:60px; border-radius:50%; border:3px solid #111; margin-top:-30px; display:flex; justify-content:center; align-items:center; color:black; font-weight:bold; font-size:10px;">MASUK</div>
    <div style="color:white; text-align:center; font-size:10px;">📞<br>CONTACT</div>
    <div style="color:white; text-align:center; font-size:10px;">🏆<br>LUCKY</div>
</div>
"""
components.html(footer_html, height=100)

