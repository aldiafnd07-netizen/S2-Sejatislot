import streamlit as st
import streamlit.components.v1 as components
import sqlite3
import random
import time

# --- 1. SETTING HALAMAN & NAVIGASI (Wajib di luhur pisan) ---
if "halaman" not in st.session_state:
    st.session_state.halaman = "home"
if "messages" not in st.session_state:
    st.session_state.messages = []

def pindah_halaman(nama_hal):
    st.session_state.halaman = nama_hal
    st.rerun()

# --- 2. SISTEM DATABASE & LOGIKA (Tetep aya) ---
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
</style>
""", unsafe_allow_html=True)

# ==========================================================
# --- HALAMAN 2: CHAT AI (DIPISAH SANGKAN PROFESIONAL) ---
# ==========================================================
if st.session_state.halaman == "chat_ai":
    # Tombol Balik
    if st.button("⬅️ KEMBALI KE PERMAINAN"):
        pindah_halaman("home")

    st.markdown("""
    <div style="background: linear-gradient(90deg, #ffd700, #b8860b); padding: 15px; border-radius: 10px 10px 0 0; color: #000; font-weight: 900; text-align:center;">
        🎧 CUSTOMER SERVICE S2 SEJATISLOT (AI Support)
    </div>
    <div style="background: #1a1a1a; padding: 15px; border: 1px solid #ffd700; color: #fff; font-size: 13px; text-align:center;">
        <b>BANTUAN LIVECHAT 24 JAM</b> 🔥<br>
        PROSES DEPO/WD TERCEPAT & AMAN
    </div>
    """, unsafe_allow_html=True)

    # Form Pra-Chat (Niru Video)
    with st.container():
        u_id = st.text_input("MASUKKAN USER ID *", placeholder="S2sejatislot")
        st.write("---")
        st.write("Apa yang bisa kami bantu? *")
        depo = st.checkbox("MASALAH DEPOSIT")
        wd = st.checkbox("MASALAH WITHDRAW")
        bonus = st.checkbox("KLAIM BONUS / PROMO")
        error = st.checkbox("ERROR DALAM GAME")
        
        if st.button("MULAI CHAT SEKARANG", use_container_width=True, type="primary"):
            if u_id:
                with st.spinner("Menghubungkan ke Server AI..."):
                    time.sleep(1.5)
                    st.success(f"Terhubung! Halo {u_id}, silakan ketik pesan Anda di bawah.")
            else:
                st.error("Isi User ID dulu bosku!")

    # Wadah Pesan Chat
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ketik pesan bantuan di sini..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Logika AI Sederhana
        with st.chat_message("assistant"):
            response = f"Baik Bosku **{u_id}**, laporan mengenai masalah tersebut sudah kami terima. Harap tunggu sebentar sementara AI kami mengecek akun Anda."
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

# ==========================================================
# --- HALAMAN 1: HOME (KODE ASLI AKANG) ---
# ==========================================================
else:
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

    # TAMPILAN ATAS
    c1, c2 = st.columns([2, 1])
    with c1: st.image("https://i.imgur.com/pjj1xQo.png", width=200)
    with c2:
        if st.button("MASUK", use_container_width=True): login_dialog()
        if st.button("DAFTAR", use_container_width=True): register_dialog()

    # FITUR VISUAL (SLIDER, MARQUEE, DLL)
    fitur_html = f"""
    <style>
        .slider-container {{ width: 100%; overflow: hidden; border-radius: 15px; margin-bottom:10px; }}
        .slider {{ display: flex; overflow-x: auto; scroll-snap-type: x mandatory; scroll-behavior: smooth; }}
        .slider img {{ width: 100%; flex-shrink: 0; }}
        .rgb-border {{ margin-top: 10px; padding: 3px; border-radius: 10px; background: linear-gradient(90deg, red, yellow, green, blue); background-size: 400%; animation: rgb-move 5s linear infinite; }}
        .inner-marquee {{ background: #1a1d24; border-radius: 8px; padding: 10px; overflow: hidden; }}
        .scrolling-text {{ display: inline-block; white-space: nowrap; color: #ffd700; font-weight: bold; animation: jalan-terus 15s linear infinite; }}
        @keyframes rgb-move {{ 0%{{background-position:0%}} 100%{{background-position:100%}} }}
        @keyframes jalan-terus {{ from {{ transform: translateX(100%); }} to {{ transform: translateX(-100%); }} }}
    </style>

    <div class="slider-container">
        <div class="slider" id="mainSlider">
            <img src="https://i.imgur.com/IA1m2GF.png">
            <img src="https://i.imgur.com/vUeCcl3.png">
            <img src="https://i.imgur.com/kek6NF4.png">
        </div>
    </div>

    <div class="rgb-border">
        <div class="inner-marquee"><div class="scrolling-text">🔥 SELAMAT DATANG DI S2 SEJATI SLOT - PROSES DEPO/WD KILAT 24 JAM 🔥</div></div>
    </div>

    <div class="jp-wrapper" style="text-align:center; background:#000; border:2px solid #ffd700; border-radius:10px; padding:10px; margin-top:10px;">
        <div style="color:#ffd700; font-size:10px; font-weight:bold;">✨ PROGRESSIVE JACKPOT ✨</div>
        <div style="color:red; font-size:24px; font-weight:900;">RP <span id="jp-val">8.715.784.119</span></div>
    </div>
    """
    components.html(fitur_html, height=350)

    # LOGIN UTAMA DI TENAH
    st.markdown("### 🔑 LOGIN UTAMA")
    st.text_input("Username", key="main_u")
    st.text_input("Password", type="password", key="main_p")
    st.button("MASUK SEKARANG", type="primary", use_container_width=True)

    # --- 9. NAVIGASI BAWAH + POPUP (TOMBOL KE AI) ---
    st.markdown("""
    <style>
        #toggle-chat { display: none; }
        .nav-container {
            position: fixed; bottom: 0; left: 0; width: 100%; height: 75px;
            background: #111; display: flex; justify-content: space-around;
            align-items: center; border-top: 2px solid #ffd700; z-index: 9999;
        }
        .nav-link { text-align: center; color: white; text-decoration: none; font-size: 10px; cursor: pointer; }
    </style>
    """, unsafe_allow_html=True)

    # Tombol Chat husus anu mun diklik pindah ka halaman AI
    col_ai1, col_ai2, col_ai3 = st.columns([1,2,1])
    with col_ai2:
        if st.button("💬 CHAT AI (BANTUAN)", use_container_width=True):
            pindah_halaman("chat_ai")

    st.markdown("""
    <div class="nav-container">
        <div class="nav-link" onclick="window.parent.location.reload();">🏠<br>HOME</div>
        <div class="nav-link">🎁<br>PROMO</div>
        <div style="width: 20%;"></div>
        <div class="nav-link">📲<br>APK</div>
        <div class="nav-link" onclick="document.querySelector('button[kind=secondary]').click()">💬<br>CHAT</div>
    </div>
    """, unsafe_allow_html=True)

