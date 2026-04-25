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

    # Fitur Visual
    fitur_html = f"""
    <style>
        .slider-container {{ width: 100%; overflow: hidden; border-radius: 15px; margin-bottom:10px; }}
        .slider {{ display: flex; overflow-x: auto; scroll-snap-type: x mandatory; scroll-behavior: smooth; }}
        .slider::-webkit-scrollbar {{ display: none; }}
        .slider img {{ width: 100%; flex-shrink: 0; scroll-snap-align: start; }}
        .rgb-border {{ margin-top: 10px; padding: 3px; border-radius: 10px; background: linear-gradient(90deg, #ff0000, #ffff00, #00ff00, #00ffff, #0000ff, #ff00ff, #ff0000); background-size: 400% 400%; animation: rgb-move 5s linear infinite; }}
        .inner-marquee {{ background: #1a1d24; border-radius: 8px; padding: 10px; overflow: hidden; }}
        .scrolling-text {{ display: inline-block; white-space: nowrap; color: #ffd700; font-weight: bold; animation: jalan-terus 15s linear infinite; }}
        .scroll-container {{ display: flex; overflow-x: auto; white-space: nowrap; gap: 15px; padding: 15px 5px; background: rgba(0,0,0,0.5); border-radius: 10px; margin-top:10px; }}
        .brand-item {{ flex: 0 0 auto; width: 70px; text-align: center; color: #ffd700; font-size: 10px; font-weight: bold; cursor: pointer; }}
        .brand-item img {{ width: 55px; height: 55px; border-radius: 50%; border: 2px solid #ffd700; background: #000; }}
        .active img {{ border-color: #00ff00; box-shadow: 0 0 10px #00ff00; }}
        .winner-box {{ background: rgba(0, 0, 0, 0.85); border-radius: 12px; border: 1px solid #ffd700; margin-top: 15px; height: 110px; overflow: hidden; position: relative; }}
        .win-header {{ background: #1a1d24; color: #ffd700; font-size: 11px; font-weight: bold; text-align: center; padding: 6px 0; border-bottom: 1px solid #ffd700; position: sticky; top: 0; z-index: 10; }}
        .win-list-container {{ padding: 0 10px; animation: scroll-up 12s linear infinite; }}
        .win-item {{ display: flex; justify-content: space-between; padding: 8px 0; color: #fff; font-size: 11px; border-bottom: 1px solid rgba(255,255,255,0.1); }}
        .jp-wrapper {{ margin-top: 10px; background: #000; border: 2px solid #ffd700; border-radius: 10px; padding: 10px; text-align: center; }}
        .jp-num {{ color: #ff0000; font-size: 24px; font-weight: 900; text-shadow: 0 0 10px #ff0000; }}
        @keyframes scroll-up {{ 0% {{ transform: translateY(0); }} 100% {{ transform: translateY(-50%); }} }}
        @keyframes rgb-move {{ 0%{{background-position:0% 50%}} 100%{{background-position:100% 50%}} }}
        @keyframes jalan-terus {{ from {{ transform: translateX(100%); }} to {{ transform: translateX(-100%); }} }}
    </style>
    <div class="slider-container"><div class="slider" id="mainSlider"><img src="https://i.imgur.com/IA1m2GF.png"><img src="https://i.imgur.com/vUeCcl3.png"></div></div>
    <div class="rgb-border"><div class="inner-marquee"><div class="scrolling-text">🔥 SELAMAT DATANG DI S2 SEJATISLOT - SITUS GACOR TERPERCAYA 🔥</div></div></div>
    <div class="scroll-container">
        <div class="brand-item {'active' if m_aktif == 'SLOT' else ''}"><img src="https://akongads.store/images/menu-icon/slot.webp"><br>SLOT</div>
        <div class="brand-item"><img src="https://i.ibb.co/S769989/pragmatic.png"><br>CASINO</div>
    </div>
    <div class="winner-box">
        <div class="win-header">🏆 LIVE WINNER</div>
        <div class="win-list-container">
            <div class="win-item"><span>User***Jp</span><span style="color:#00ff00;">IDR 2.500.000</span></div>
            <div class="win-item"><span>S2***Slot</span><span style="color:#00ff00;">IDR 5.750.000</span></div>
            <div class="win-item"><span>User***Jp</span><span style="color:#00ff00;">IDR 2.500.000</span></div>
        </div>
    </div>
    <div class="jp-wrapper"><div class="jp-num">RP <span id="jp-val">8.715.784.119</span></div></div>
    <script>
        let jVal = 8715784119; setInterval(() => {{
            jVal += Math.floor(Math.random()*5000);
            let jv = document.getElementById('jp-val');
            if(jv) jv.innerText = jVal.toLocaleString('id-ID');
        }}, 100);
    </script>
    """
    components.html(fitur_html, height=520)

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

# --- 5. NAVIGASI BAWAH & POPUP SOSMED (GLOBAL) ---
footer_html = f"""
<style>
    #toggle-chat {{ display: none; }}
    .btn-chat-float {{
        position: fixed; bottom: 95px; right: 20px;
        width: 65px; height: 65px;
        background: linear-gradient(180deg, #ffd700, #ff8c00);
        border-radius: 50%; display: flex; justify-content: center; align-items: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.6); cursor: pointer; z-index: 100000;
        animation: pulse 2s infinite; border: 2px solid #fff;
    }}
    .chat-box {{
        position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%);
        width: 300px; background: #111; border: 2px solid #ffd700; border-radius: 15px;
        z-index: 100002; display: none; overflow: hidden;
    }}
    #toggle-chat:checked ~ .chat-box {{ display: block; }}
    @keyframes pulse {{ 0% {{ box-shadow: 0 0 0 0 rgba(255,215,0,0.7); }} 70% {{ box-shadow: 0 0 0 15px rgba(255,215,0,0); }} }}
</style>
<input type="checkbox" id="toggle-chat">
<label for="toggle-chat" class="btn-chat-float"><img src="https://cdn-icons-png.flaticon.com/512/5968/5968771.png" width="35"></label>
<div class="chat-box">
    <div style="background:#ffd700; color:black; padding:10px; font-weight:bold; display:flex; justify-content:space-between;">
        <span>HUBUNGI CS</span><label for="toggle-chat" style="cursor:pointer;">✖</label>
    </div>
    <div style="padding:15px; text-align:center;">
        <a href="https://wa.me/6285724785177" style="display:block; background:#25d366; color:white; padding:10px; margin-bottom:10px; text-decoration:none; border-radius:5px;">WHATSAPP</a>
        <a href="https://t.me/aldiafnd07" style="display:block; background:#0088cc; color:white; padding:10px; text-decoration:none; border-radius:5px;">TELEGRAM</a>
    </div>
</div>
"""
components.html(footer_html, height=100)

