import streamlit as st
import streamlit.components.v1 as components
import sqlite3
import random
import streamlit as st

# --- 1. SETTING HALAMAN & NAVIGASI ---
if "halaman" not in st.session_state:
    st.session_state.halaman = "home"

# Fungsi pindah halaman
def pindah_halaman(nama_hal):
    st.session_state.halaman = nama_hal
    st.rerun()

# --- 2. LOGIKA HALAMAN ---
if st.session_state.halaman == "home":
    # --- ISI HALAMAN HOME (Kodingan Akang nu tiasa scroll ka handap) ---
    st.markdown("### 🏠 HALAMAN UTAMA S2 SEJATISLOT")
    # ... (Lebetkeun kodingan banner, game, dll di dieu) ...

    # Tombol Chat nu ngarahkeun ka Halaman 2
    st.markdown("""
    <style>
        .float-ai {
            position: fixed; bottom: 100px; right: 20px;
            width: 60px; height: 60px; background: #007bff;
            border-radius: 50%; display: flex; justify-content: center;
            align-items: center; z-index: 99; cursor: pointer;
            box-shadow: 0 4px 10px rgba(0,0,0,0.3);
        }
    </style>
    """, unsafe_allow_html=True)

    if st.button("💬", key="btn_ai"):
        pindah_halaman("chat_ai")

elif st.session_state.halaman == "chat_ai":
    # --- 3. HALAMAN CHAT AI (MIRIP VIDEO) ---

    # Tombol Balik ka Home
    if st.button("⬅️ Balik ka Home"):
        pindah_halaman("home")

    st.markdown("""
    <div style="background: #ffd700; padding: 15px; border-radius: 10px 10px 0 0; color: #000; font-weight:>
        🎧 CS S2 SEJATISLOT (AI Support)
    </div>
    <div style="background: #1a1a1a; padding: 15px; border: 1px solid #ffd700; color: #fff; font-size: 13px>
        AKONGCUAN LIVECHAT 🔥<br>
        BONUS NEW MEMBER 100%<br>
        KHUSUS SLOT JANGAN LUPA KLAIM BOSKU!!
    </div>
    """, unsafe_allow_html=True)

    # Form Input User ID (Mirip Video)
    user_id = st.text_input("USER ID *", placeholder="S2sejatislot")

    # Checkbox Masalah (Mirip Video)
    st.write("Masalah apa yang perlu kita bantu bosku? *")
    st.checkbox("PROSES DEPOSIT")
    st.checkbox("PROSES WITHDRAW")
    st.checkbox("KLAIM BONUS FREESPIN")
    st.checkbox("ERROR PERMAINAN")

    if st.button("Mulai Obrolan", use_container_width=True):
        st.success("Nyambungkeun ka AI...")

    # Wadah Chat AI
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ketik pesan di sini..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Jawaban Otomatis
        response = f"Halo {user_id}, abdi AI S2. Aya nu tiasa dibantos ngeunaan masalah kasebat?"
        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(response)

# --- 1. SISTEM DATABASE ---
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

m_aktif = st.query_params.get("m", "SLOT")

# --- 3. CSS GLOBAL ---
st.markdown("""
<style>
    header, footer, #MainMenu, .stDeployButton { visibility: hidden !important; display: none !important; }
    .stApp {
        background-image: url("https://i.imgur.com/0sCszBw.png");
        background-attachment: fixed; background-size: cover; background-position: center;
    }
    .block-container { padding: 0.5rem !important; padding-bottom: 160px !important; }
    .stTextInput input {
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

# --- 6. FITUR VISUAL ---
fitur_html = f"""
<style>
    .slider-container {{ width: 100%; overflow: hidden; border-radius: 15px; margin-bottom:10px; }}
    .slider {{ display: flex; overflow-x: auto; scroll-snap-type: x mandatory; scroll-behavior: smooth; }}
    .slider::-webkit-scrollbar {{ display: none; }}
    .slider img {{ width: 100%; flex-shrink: 0; scroll-snap-align: start; }}

    .rgb-border {{
        margin-top: 10px; padding: 3px; border-radius: 10px;
        background: linear-gradient(90deg, #ff0000, #ffff00, #00ff00, #00ffff, #0000ff, #ff00ff, #ff0000);
        background-size: 400% 400%; animation: rgb-move 5s linear infinite;
    }}
    .inner-marquee {{ background: #1a1d24; border-radius: 8px; padding: 10px; overflow: hidden; }}
    .scrolling-text {{ display: inline-block; white-space: nowrap; color: #ffd700; font-weight: bold; anima>

    .scroll-container {{
        display: flex; overflow-x: auto; white-space: nowrap; gap: 15px; padding: 15px 5px;
        background: rgba(0,0,0,0.5); border-radius: 10px; margin-top:10px;
    }}
    .scroll-container::-webkit-scrollbar {{ display: none; }}
    .brand-item {{ flex: 0 0 auto; width: 70px; text-align: center; color: #ffd700; font-size: 10px; font-w>
    .brand-item img {{ width: 55px; height: 55px; border-radius: 50%; border: 2px solid #ffd700; background>
    .active img {{ border-color: #00ff00; box-shadow: 0 0 10px #00ff00; }}
 .winner-box {{
        background: rgba(0, 0, 0, 0.85); border-radius: 12px; border: 1px solid #ffd700;
        margin-top: 15px; height: 110px; overflow: hidden; position: relative;
    }}
    .win-header {{
        background: #1a1d24; color: #ffd700; font-size: 11px; font-weight: bold;
        text-align: center; padding: 6px 0; border-bottom: 1px solid #ffd700;
        position: sticky; top: 0; z-index: 10;
    }}
    .win-list-container {{ padding: 0 10px; animation: scroll-up 12s linear infinite; }}
    .win-item {{
        display: flex; justify-content: space-between; padding: 8px 0;
        color: #fff; font-size: 11px; border-bottom: 1px solid rgba(255,255,255,0.1);
    }}

    .jp-wrapper {{ margin-top: 10px; background: #000; border: 2px solid #ffd700; border-radius: 10px; padd>
    .jp-num {{ color: #ff0000; font-size: 24px; font-weight: 900; text-shadow: 0 0 10px #ff0000; }}

    @keyframes scroll-up {{ 0% {{ transform: translateY(0); }} 100% {{ transform: translateY(-50%); }} }}
    @keyframes rgb-move {{ 0%{{background-position:0% 50%}} 100%{{background-position:100% 50%}} }}
    @keyframes jalan-terus {{ from {{ transform: translateX(100%); }} to {{ transform: translateX(-100%); }>
</style>

<div class="slider-container">
    <div class="slider" id="mainSlider">
        <img src="https://i.imgur.com/IA1m2GF.png">
        <img src="https://i.imgur.com/vUeCcl3.png">
        <img src="https://i.imgur.com/kek6NF4.png">
    </div>
</div>

<div class="rgb-border">
    <div class="inner-marquee"><div class="scrolling-text">🔥 SELAMAT DATANG DI S2 SEJATI SLOT - PROSES DEP>
</div>

<div class="scroll-container">
    <div class="brand-item {'active' if m_aktif == 'SLOT' else ''}" onclick="window.parent.location.href='?>
        <img src="https://akongads.store/images/menu-icon/slot.webp"><br>SLOT
    </div>
    <div class="brand-item {'active' if m_aktif == 'CASINO' else ''}" onclick="window.parent.location.href=>
        <img src="https://i.ibb.co/S769989/pragmatic.png"><br>CASINO
    </div>
    <div class="brand-item {'active' if m_aktif == 'SPORT' else ''}" onclick="window.parent.location.href='>
        <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR_x_q8hZ68o2fIuN7VlZ1t2H6Y-f5K6-r-w>
    </div>
    <div class="brand-item {'active' if m_aktif == 'TOGEL' else ''}" onclick="window.parent.location.href='>
        <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR0R_B8n1lG4_u7yS6Wv3U4J_Y_6rB8v8_oO>
    </div>
</div>

<div class="winner-box">
    <div class="win-header">🏆 LIVE WINNER REAL-TIME</div>
    <div class="win-list-container">
        <div class="win-item"><span>User***Jp</span><span style="color:#ffd700;">[Olympus]</span><span styl>
        <div class="win-item"><span>M***x91</span><span style="color:#ffd700;">[Mahjong]</span><span style=>
        <div class="win-item"><span>R***ky_A</span><span style="color:#ffd700;">[Princess]</span><span styl>
        <div class="win-item"><span>S2***Slot</span><span style="color:#ffd700;">[Bonanza]</span><span styl>
        <div class="win-item"><span>User***Jp</span><span style="color:#ffd700;">[Olympus]</span><span styl>
        <div class="win-item"><span>M***x91</span><span style="color:#ffd700;">[Mahjong]</span><span style=>
        <div class="win-item"><span>R***ky_A</span><span style="color:#ffd700;">[Princess]</span><span styl>
        <div class="win-item"><span>S2***Slot</span><span style="color:#ffd700;">[Bonanza]</span><span styl>
    </div>
</div>

<div class="jp-wrapper">
    <div style="color:#ffd700; font-size:10px; font-weight:bold;">✨ PROGRESSIVE JACKPOT ✨</div>
    <div class="jp-num">RP <span id="jp-val">8.715.784.119</span></div>
</div>

<script>
    let sIdx = 0; setInterval(() => {{
        sIdx = (sIdx + 1) % 3;
        let s = document.getElementById('mainSlider');
        if(s) s.scrollTo({{left: sIdx * s.clientWidth, behavior: 'smooth'}});
    }}, 3000);
    let jVal = 8715784119; setInterval(() => {{
        jVal += Math.floor(Math.random()*5000);
        let jv = document.getElementById('jp-val');
        if(jv) jv.innerText = jVal.toLocaleString('id-ID');
    }}, 100);
</script>
"""
components.html(fitur_html, height=520)

# --- 7. TAMPILAN GAME SCROLL ---
st.markdown(f"#### 🎮 KUMPULAN GAME: {m_aktif}")
game_data = {
    "SLOT": [{"n": "Pragmatic", "i": "https://i.ibb.co/S769989/pragmatic.png"}, {"n": "PG Soft", "i": "http>
    "CASINO": [{"n": "Sexy Casino", "i": "https://i.ibb.co/S769989/pragmatic.png"}],
    "TOGEL": [{"n": "HK", "i": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR0R_B8n1lG4_u7yS6Wv3U>
}
current_games = game_data.get(m_aktif, game_data["SLOT"])
game_scroll = f"""
<div style="display: flex; overflow-x: auto; gap: 12px; padding: 10px;">
    {''.join([f'<div style="flex:0 0 auto; width:100px; text-align:center;"><img src="{g["i"]}" style="widt>
</div>
"""
components.html(game_scroll, height=150)

# --- 8. LOGIN UTAMA ---
st.markdown("### 🔑 LOGIN UTAMA")
st.text_input("Username", key="main_u")
st.text_input("Password", type="password", key="main_p")
st.button("MASUK SEKARANG", type="primary", use_container_width=True)
# --- 9. NAVIGASI BAWAH + POPUP LIVE CHAT (FINAL PREMIUM) ---
st.markdown("""
<style>
    /* 1. TRIK CSS: Sembunyikan checkbox logika */
    #toggle-chat { display: none; }

    /* 2. TOMBOL CHAT MELAYANG (Animasi Pulse) */
    .btn-chat-float {
        position: fixed; bottom: 95px; right: 20px;
        width: 65px; height: 65px;
        background: linear-gradient(180deg, #ffd700, #ff8c00);
        border-radius: 50%; display: flex; justify-content: center; align-items: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.6); cursor: pointer; z-index: 100000;
        animation: pulse-gold 2s infinite; border: 2px solid #fff;
    }
    .btn-chat-float img { width: 35px; }

    @keyframes pulse-gold {
        0% { box-shadow: 0 0 0 0 rgba(255, 215, 0, 0.7); }
        70% { box-shadow: 0 0 0 15px rgba(255, 215, 0, 0); }
        100% { box-shadow: 0 0 0 0 rgba(255, 215, 0, 0); }
    }

    /* 3. LAYAR GELAP (Overlay) */
    .chat-overlay {
        position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
        background: rgba(0,0,0,0.85); z-index: 100001;
        opacity: 0; visibility: hidden; transition: all 0.3s ease-in-out; cursor: pointer;
    }

    /* 4. KOTAK POPUP */
    .chat-box {
        position: fixed; top: 50%; left: 50%;
        transform: translate(-50%, -50%) scale(0.8);
        width: 320px; max-width: 90%; background: #111;
        border: 2px solid #ffd700; border-radius: 15px; z-index: 100002;
        opacity: 0; visibility: hidden; transition: all 0.3s ease-in-out;
        overflow: hidden; box-shadow: 0 0 25px rgba(255, 215, 0, 0.5);
    }

    /* 5. LOGIKA KLIK (Tanpa Javascript) */
    #toggle-chat:checked ~ .chat-overlay { opacity: 1; visibility: visible; }
    #toggle-chat:checked ~ .chat-box { opacity: 1; visibility: visible; transform: translate(-50%, -50%) sc>

    /* HEADER KOTAK */
    .chat-header {
        background: linear-gradient(90deg, #ffd700, #b8860b);
        color: #000; padding: 12px 15px; font-weight: 900;
        display: flex; justify-content: space-between; align-items: center; font-size: 14px;
    }
    .chat-close { font-size: 26px; font-weight: bold; cursor: pointer; line-height: 1; color: #000; }

    /* DAFTAR SOSMED */
    .sosmed-container { padding: 10px; background: #1a1a1a; }
    .sosmed-item {
        display: flex; justify-content: space-between; align-items: center;
        background: #222; margin-bottom: 10px; padding: 12px 15px;
        border-radius: 8px; text-decoration: none; border: 1px solid #333; transition: 0.3s;
    }
    .sosmed-item:hover { background: #333; border-color: #ffd700; transform: translateX(5px); }
    .sosmed-left { display: flex; align-items: center; gap: 12px; color: #fff; font-weight: bold; font-size>
    .sosmed-icon { width: 25px; height: 25px; }

    .btn-klik {
        background: linear-gradient(180deg, #ffd700, #ff8c00);
        color: #000; padding: 6px 15px; border-radius: 20px;
        font-size: 11px; font-weight: 900; box-shadow: 0 2px 5px rgba(0,0,0,0.5);
        animation: getar 3s infinite;
    }

    @keyframes getar {
        0%, 100% { transform: rotate(0deg); }
        5%, 15% { transform: rotate(-5deg); }
        10%, 20% { transform: rotate(5deg); }
        25% { transform: rotate(0deg); }
    }

    .teks-bawah { padding: 5px 15px 15px; text-align: center; color: #ccc; font-size: 11px; line-height: 1.>

    /* 6. NAVIGASI BAWAH */
    .nav-container {
        position: fixed; bottom: 0; left: 0; width: 100%; height: 75px;
        background: #111; display: flex; justify-content: space-around;
        align-items: center; border-top: 2px solid #ffd700; z-index: 99999;
    }
    .floating-center {
        position: fixed; bottom: 25px; left: 50%; transform: translateX(-50%);
        width: 75px; height: 75px; background: linear-gradient(180deg, #ffd700, #b8860b);
        border-radius: 50%; border: 4px solid #111; display: flex;
        justify-content: center; align-items: center; z-index: 100000;
        box-shadow: 0 0 15px #ffd700; cursor: pointer;
    }
    .nav-link { text-align: center; color: white; text-decoration: none; width: 20%; font-size: 10px; curso>
</style>

<input type="checkbox" id="toggle-chat">

<label for="toggle-chat" class="btn-chat-float">
    <img src="https://cdn-icons-png.flaticon.com/512/5968/5968771.png" alt="Chat S2">
</label>

<label for="toggle-chat" class="chat-overlay"></label>

<div class="chat-box">
    <div class="chat-header">
        <span>🎧 CUSTOMER SERVICE S2</span>
        <label for="toggle-chat" class="chat-close">&times;</label>
 </div>
    <img src="https://i.supaimg.com/e2052feb-b9dd-4dac-b762-c0dee9b0bd7b/8501f28f-3d3c-4440-8af2-b9a41789e2>
    <div class="sosmed-container">
        <a href="https://wa.me/6285724785177" target="_blank" class="sosmed-item">
            <div class="sosmed-left">
                <img src="https://upload.wikimedia.org/wikipedia/commons/6/6b/WhatsApp.svg" class="sosmed-i>
                <span>WhatsApp</span>
            </div>
            <div class="btn-klik">Klik Disini</div>
        </a>
        <a href="https://t.me/aldiafnd07" target="_blank" class="sosmed-item">
            <div class="sosmed-left">
                <img src="https://upload.wikimedia.org/wikipedia/commons/8/82/Telegram_logo.svg" class="sos>
                <span>Telegram</span>
            </div>
            <div class="btn-klik">Klik Disini</div>
        </a>
        <a href="https://www.facebook.com/aldi.pehul.12" target="_blank" class="sosmed-item">
            <div class="sosmed-left">
                <img src="https://upload.wikimedia.org/wikipedia/commons/b/b8/2021_Facebook_icon.svg" class>
                <span>Facebook</span>
            </div>
            <div class="btn-klik">Klik Disini</div>
        </a>
    </div>
    <div class="teks-bawah">
        Halo! Hubungi CS <b>S2 SEJATISLOT</b> melalui kontak resmi di atas. Kami siap melayani keluhan dan >
    </div>
</div>

<div class="floating-center" onclick="window.parent.location.reload();">
    <b style="color:black; font-size:11px;">MASUK</b>
