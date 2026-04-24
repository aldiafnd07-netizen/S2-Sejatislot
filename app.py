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

init_db()

# --- 2. LOGIKA NAVIGASI MENU (FITUR ANYAR) ---
if 'menu_aktif' not in st.session_state:
    st.session_state.menu_aktif = "SLOT"

# Cek upami aya parobahan menu tina URL
q = st.query_params
if "m" in q:
    st.session_state.menu_aktif = q["m"]

# --- 3. FITUR HTML & CSS (BANNER, MARQUEE, MENU KLIK) ---
fitur_html = f"""
<style>
    .slider {{ display: flex; overflow-x: auto; scroll-snap-type: x mandatory; border-radius: 15px; margin-bottom:10px; }}
    .slider::-webkit-scrollbar {{ display: none; }}
    .slider img {{ width: 100%; flex-shrink: 0; scroll-snap-align: start; }}

    .rgb-border {{
        margin-top: 10px; padding: 3px; border-radius: 10px;
        background: linear-gradient(90deg, #ff0000, #ffff00, #00ff00, #00ffff, #0000ff, #ff00ff, #ff0000);
        background-size: 400% 400%; animation: rgb-move 5s linear infinite;
    }}
    .inner-marquee {{ background: #1a1d24; border-radius: 8px; padding: 10px; overflow: hidden; }}
    .scrolling-text {{ display: inline-block; white-space: nowrap; color: #ffd700; font-weight: bold; animation: jalan 15s linear infinite; }}

    .scroll-container {{ display: flex; overflow-x: auto; gap: 15px; padding: 15px 5px; background: rgba(0,0,0,0.5); border-radius: 10px; }}
    .scroll-container::-webkit-scrollbar {{ display: none; }}
    .brand-item {{ flex: 0 0 auto; width: 70px; text-align: center; color: #ffd700; font-size: 10px; font-weight: bold; cursor: pointer; }}
    .brand-item img {{ width: 55px; height: 55px; border-radius: 50%; border: 2px solid #ffd700; background: #222; }}
    .active img {{ border-color: #00ff00; box-shadow: 0 0 10px #2ecc71; }}

    @keyframes rgb-move {{ 0%{{background-position:0% 50%}} 100%{{background-position:100% 50%}} }}
    @keyframes jalan {{ from {{ transform: translateX(100%); }} to {{ transform: translateX(-100%); }} }}
</style>

<div class="slider">
    <img src="https://i.imgur.com/vUeCcl3.png">
    <img src="https://i.imgur.com/kek6NF4.png">
</div>

<div class="rgb-border">
    <div class="inner-marquee"><div class="scrolling-text">🔥 SELAMAT DATANG DI S2 SEJATI SLOT - SITUS GACOR TERPERCAYA 🔥</div></div>
</div>

<div class="scroll-container">
    <div class="brand-item {'active' if st.session_state.menu_aktif == 'SLOT' else ''}" onclick="window.parent.location.href='?m=SLOT'">
        <img src="https://akongads.store/images/menu-icon/slot.webp"><br>SLOT
    </div>
    <div class="brand-item {'active' if st.session_state.menu_aktif == 'CASINO' else ''}" onclick="window.parent.location.href='?m=CASINO'">
        <img src="https://i.ibb.co/S769989/pragmatic.png"><br>CASINO
    </div>
    <div class="brand-item {'active' if st.session_state.menu_aktif == 'SPORT' else ''}" onclick="window.parent.location.href='?m=SPORT'">
        <img src="https://i.ibb.co/0YmYVf8/pgsoft.png"><br>SPORT+
    </div>
    <div class="brand-item {'active' if st.session_state.menu_aktif == 'TOGEL' else ''}" onclick="window.parent.location.href='?m=TOGEL'">
        <img src="https://i.ibb.co/XW3px3P/habanero.png"><br>TOGEL
    </div>
    <div class="brand-item {'active' if st.session_state.menu_aktif == 'IKAN' else ''}" onclick="window.parent.location.href='?m=IKAN'">
        <img src="https://i.ibb.co/fM8vXz3/joker.png"><br>IKAN
    </div>
</div>
"""
components.html(fitur_html, height=380)

# --- 4. DATA GAME DUMASAR MENU (SCROLL GAMBAR GAME) ---
st.subheader(f"🎮 {st.session_state.menu_aktif} GAMES")

game_list = {
    "SLOT": [
        {"n": "Pragmatic", "img": "https://i.ibb.co/S769989/pragmatic.png"},
        {"n": "PG Soft", "img": "https://i.ibb.co/0YmYVf8/pgsoft.png"},
        {"n": "Habanero", "img": "https://i.ibb.co/XW3px3P/habanero.png"},
        {"n": "Microgame", "img": "https://i.ibb.co/fM8vXz3/joker.png"},
        {"n": "CQ9", "img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTzR_eYp-o6T-0W-KqS-6Q6W_U&s"}
    ],
    "CASINO": [
        {"n": "Baccarat", "img": "https://i.ibb.co/S769989/pragmatic.png"},
        {"n": "Roulette", "img": "https://i.ibb.co/0YmYVf8/pgsoft.png"}
    ],
    "TOGEL": [
        {"n": "HK", "img": "https://i.ibb.co/XW3px3P/habanero.png"},
        {"n": "SGP", "img": "https://i.ibb.co/fM8vXz3/joker.png"}
    ]
}

current_games = game_list.get(st.session_state.menu_aktif, game_list["SLOT"])

# Fitur Scroll Game Gambar (Otomatis & Manual)
scroll_js = f"""
<div style="display: flex; overflow-x: auto; gap: 10px; padding: 10px; background: #000; border-radius: 10px;">
    {''.join([f'''
        <div style="flex: 0 0 auto; width: 110px; text-align: center;">
            <img src="{g['img']}" style="width: 100px; height: 100px; border-radius: 12px; border: 2px solid #ffd700;">
            <p style="color: white; font-size: 10px; margin-top: 5px;">{g['n']}</p>
        </div>
    ''' for g in current_games])}
</div>
"""
components.html(scroll_js, height=160)

# --- 5. INPUT LOGIN (FITUR ASLI) ---
st.markdown("### 🔐 LOGIN UTAMA")
u_name = st.text_input("Username", key="m_u")
p_word = st.text_input("Password", type="password", key="m_p")

if st.button("MASUK SEKARANG", type="primary", use_container_width=True):
    user = cek_login(u_name, p_word)
    if user:
        st.success(f"Selamat Datang {u_name}!")
    else:
        st.error("Username/Password Salah!")

# --- 6. NAVBAR BAWAH ---
st.markdown("""
<style>
    .nav-bawah { position: fixed; bottom: 0; left: 0; width: 100%; background: #111; display: flex; justify-content: space-around; padding: 10px; border-top: 2px solid #ffd700; z-index: 999; }
    .nav-item { text-align: center; color: white; font-size: 10px; text-decoration: none; }
</style>
<div class="nav-bawah">
    <a href="/" class="nav-item">🏠<br>HOME</a>
    <a href="#" class="nav-item">🎁<br>PROMO</a>
    <a href="#" class="nav-item" style="color:#ffd700; font-weight:bold;">💰<br>DEPOSIT</a>
    <a href="#" class="nav-item">💬<br>CHAT</a>
    <a href="#" class="nav-item">👤<br>AKUN</a>
</div>
""", unsafe_allow_html=True)

