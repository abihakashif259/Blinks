import streamlit as st
import sqlite3
import random

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Blink Social Hub 🌸",
    page_icon="🖤",
    layout="wide"
)

# =========================================================
# DATABASE
# =========================================================

DB_NAME = "blink.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    # Game score
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS game (
            id INTEGER PRIMARY KEY,
            score INTEGER DEFAULT 0
        )
    """)

    # Diary
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS diary (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            entry TEXT NOT NULL
        )
    """)

    # Polls
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS polls (
            member TEXT PRIMARY KEY,
            votes INTEGER DEFAULT 0
        )
    """)

    # Pins
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            image_url TEXT NOT NULL
        )
    """)

    # Badges
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS badges (
            name TEXT PRIMARY KEY
        )
    """)

    # Create game record
    cursor.execute("""
        INSERT OR IGNORE INTO game (id, score)
        VALUES (1, 0)
    """)

    # Create poll members
    members = ["Jisoo", "Jennie", "Rosé", "Lisa"]

    for member in members:
        cursor.execute("""
            INSERT OR IGNORE INTO polls (member, votes)
            VALUES (?, 0)
        """, (member,))

    conn.commit()
    conn.close()


create_tables()


# =========================================================
# DATABASE FUNCTIONS
# =========================================================

def get_score():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT score FROM game WHERE id = 1")
    result = cursor.fetchone()

    conn.close()

    return result[0] if result else 0


def add_score():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE game
        SET score = score + 1
        WHERE id = 1
    """)

    conn.commit()
    conn.close()


def get_diary():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, entry
        FROM diary
        ORDER BY id DESC
    """)

    data = cursor.fetchall()

    conn.close()

    return data


def add_diary(entry):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO diary (entry) VALUES (?)",
        (entry,)
    )

    conn.commit()
    conn.close()


def delete_diary(entry_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM diary WHERE id = ?",
        (entry_id,)
    )

    conn.commit()
    conn.close()


def get_polls():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT member, votes
        FROM polls
    """)

    data = dict(cursor.fetchall())

    conn.close()

    return data


def add_vote(member):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE polls
        SET votes = votes + 1
        WHERE member = ?
    """, (member,))

    conn.commit()
    conn.close()


def get_pins():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, title, image_url
        FROM pins
        ORDER BY id DESC
    """)

    data = cursor.fetchall()

    conn.close()

    return data


def add_pin(title, image_url):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO pins (title, image_url)
        VALUES (?, ?)
    """, (title, image_url))

    conn.commit()
    conn.close()


def delete_pin(pin_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM pins WHERE id = ?",
        (pin_id,)
    )

    conn.commit()
    conn.close()


def get_badges():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM badges")

    data = [row[0] for row in cursor.fetchall()]

    conn.close()

    return data


def add_badge(name):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR IGNORE INTO badges (name)
        VALUES (?)
    """, (name,))

    conn.commit()
    conn.close()


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

.stApp {
    background: linear-gradient(135deg, #fff7fb, #f7edff);
    color: #222222 !important;
}

.block-container {
    padding-top: 2rem;
}

/* Main text */

p, span, label {
    color: #222222;
}

h1, h2, h3, h4, h5, h6 {
    color: #241326 !important;
}

/* Sidebar */

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #160d18, #2b132d);
}

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3,
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] span {
    color: white !important;
}

/* Cards */

.card {
    background: white;
    padding: 25px;
    border-radius: 22px;
    margin-bottom: 20px;
    box-shadow: 0 8px 25px rgba(0,0,0,0.08);
    border: 1px solid #f0d9e8;
}

.card h2,
.card h3,
.card p {
    color: #222222 !important;
}

/* Buttons */

.stButton > button {
    background: white;
    color: #222222 !important;
    border: 1px solid #e3c4da;
    border-radius: 15px;
    font-weight: bold;
}

.stButton > button:hover {
    color: #d63384 !important;
    border-color: #d63384;
}

/* Inputs */

input,
textarea {
    color: #222222 !important;
    background: white !important;
}

input::placeholder,
textarea::placeholder {
    color: #888888 !important;
}

/* Select */

div[data-baseweb="select"] * {
    color: #222222 !important;
}

/* Tabs */

button[data-baseweb="tab"] {
    color: #444444 !important;
}

button[data-baseweb="tab"][aria-selected="true"] {
    color: #d63384 !important;
}

/* Metric */

.metric-card {
    background: white;
    padding: 18px;
    border-radius: 18px;
    text-align: center;
    box-shadow: 0 5px 18px rgba(0,0,0,0.06);
}

.metric-card h2 {
    color: #d63384 !important;
}

.metric-card p {
    color: #555555 !important;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("🖤 BLINK")
st.sidebar.write("### Social Hub 🌸")

page = st.sidebar.radio(
    "Navigate",
    [
        "🏠 Home",
        "🎮 Song Game",
        "📝 Fan Diary",
        "🎤 Polls",
        "🎵 Music",
        "📌 Pin Board",
        "🏆 Achievements"
    ]
)

st.sidebar.divider()
st.sidebar.caption("BLACKPINK in your area")


# =========================================================
# HOME
# =========================================================

if page == "🏠 Home":

    st.markdown(
        "<h1 style='text-align:center;'>🖤 BLINK SOCIAL HUB 🌸</h1>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<p style='text-align:center;color:#666;'>"
        "A cozy place for Blinks to play, share & vibe ✨"
        "</p>",
        unsafe_allow_html=True
    )

    score = get_score()
    diary = get_diary()
    polls = get_polls()
    pins = get_pins()

    total_votes = sum(polls.values())

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric("🎮 Game Score", score)

    with c2:
        st.metric("📝 Memories", len(diary))

    with c3:
        st.metric("🎤 Votes", total_votes)

    with c4:
        st.metric("📌 Pins", len(pins))

    st.write("")

    st.markdown("""
    <div class="card">
        <h2>💗 Welcome, Blink!</h2>
        <p>
        Explore games, save your favorite memories,
        vote in polls, enjoy music and create your own pin board.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("🌸 The Four Icons")

    members = [
        ("🩷", "JISOO", "Visual • Vocal"),
        ("🖤", "JENNIE", "Rapper • Vocal"),
        ("💗", "ROSÉ", "Vocal • Guitar"),
        ("💜", "LISA", "Dancer • Rapper")
    ]

    cols = st.columns(4)

    for col, member in zip(cols, members):

        with col:

            st.markdown(f"""
            <div class="card" style="text-align:center;">
                <div style="font-size:45px;">{member[0]}</div>
                <h2>{member[1]}</h2>
                <p>{member[2]}</p>
            </div>
            """, unsafe_allow_html=True)


# =========================================================
# SONG GAME
# =========================================================

elif page == "🎮 Song Game":

    st.title("🎮 Guess the Song")

    songs = {
        "Hit you with that...": "DDU-DU DDU-DU",
        "I'm going solo...": "SOLO",
        "Look at me, look at you...": "Kill This Love",
        "Taste that pink venom...": "Pink Venom",
        "BLACKPINK in your area...": "BOOMBAYAH"
    }

    if "current_song" not in st.session_state:
        st.session_state.current_song = random.choice(
            list(songs.keys())
        )

    clue = st.session_state.current_song

    st.markdown(f"""
    <div class="card">
        <h2>🎧 Lyric Clue</h2>
        <h3>"{clue}"</h3>
        <p>Can you guess the song?</p>
    </div>
    """, unsafe_allow_html=True)

    guess = st.text_input(
        "Your Answer",
        placeholder="Type the song name..."
    )

    c1, c2 = st.columns(2)

    with c1:

        if st.button(
            "💗 Check Answer",
            use_container_width=True
        ):

            if guess.strip().lower() == songs[clue].lower():

                add_score()

                st.success("🎉 Correct! Blink power!")

                if get_score() >= 5:
                    add_badge("Song Master")

                st.session_state.current_song = random.choice(
                    list(songs.keys())
                )

                st.rerun()

            else:

                st.error("Oops! Try again 💗")

    with c2:

        if st.button(
            "🔄 New Song",
            use_container_width=True
        ):

            st.session_state.current_song = random.choice(
                list(songs.keys())
            )

            st.rerun()

    st.divider()

    st.metric("🏆 Total Score", get_score())


# =========================================================
# FAN DIARY
# =========================================================

elif page == "📝 Fan Diary":

    st.title("📝 Fan Diary")

    st.write(
        "Save your favorite Blink memories permanently 💗"
    )

    entry = st.text_area(
        "Write your memory",
        placeholder="Today I listened to..."
    )

    if st.button(
        "💾 Save Memory",
        use_container_width=True
    ):

        if entry.strip():

            add_diary(entry)

            if len(get_diary()) >= 3:
                add_badge("Memory Keeper")

            st.success("Memory saved permanently 🌸")

            st.rerun()

        else:

            st.warning("Please write something first.")

    st.divider()

    memories = get_diary()

    if not memories:

        st.info(
            "Your diary is empty. Write your first memory! 💕"
        )

    else:

        for entry_id, text in memories:

            with st.container(border=True):

                st.subheader("🌸 Blink Memory")
                st.write(text)

                if st.button(
                    "🗑️ Delete",
                    key=f"delete_diary_{entry_id}"
                ):

                    delete_diary(entry_id)

                    st.success("Memory deleted.")

                    st.rerun()


# =========================================================
# POLLS
# =========================================================

elif page == "🎤 Polls":

    st.title("🎤 Blink Polls")

    st.write(
        "Vote for your favorite member 💗"
    )

    polls = get_polls()

    member = st.radio(
        "🌸 Choose your bias:",
        list(polls.keys())
    )

    if st.button(
        "💗 Submit Vote",
        use_container_width=True
    ):

        add_vote(member)

        st.success("Your vote has been saved! 🌸")

        st.rerun()

    st.divider()

    st.subheader("📊 Live Results")

    polls = get_polls()

    total = max(sum(polls.values()), 1)

    for name, votes in polls.items():

        st.write(
            f"**{name}** — {votes} votes"
        )

        st.progress(votes / total)


# =========================================================
# MUSIC
# =========================================================

elif page == "🎵 Music":

    st.title("🎵 Music Room")

    st.write(
        "Put on your headphones and enjoy the vibes 🎧🖤"
    )

    st.subheader("🔥 Featured")

    st.video(
        "https://www.youtube.com/watch?v=POe9SOEKotk"
    )

    st.divider()

    st.subheader("🎧 Playlist")

    playlist = {
        "💗 Pink Venom":
            "https://www.youtube.com/watch?v=POe9SOEKotk",

        "🖤 Kill This Love":
            "https://www.youtube.com/watch?v=2S24-y0Ij3Y",

        "🌸 DDU-DU DDU-DU":
            "https://www.youtube.com/watch?v=IHNzOHi8sJs"
    }

    for name, link in playlist.items():

        st.write(f"### {name}")

        st.video(link)

    st.divider()

    st.subheader("🎶 Your Own Track")

    music_link = st.text_input(
        "Paste your music link:"
    )

    if music_link:

        st.success("Track added to this session 🎧")
        st.write(music_link)


# =========================================================
# PIN BOARD
# =========================================================

elif page == "📌 Pin Board":

    st.title("📌 Blink Pin Board")

    st.write(
        "Create your own aesthetic collection ✨"
    )

    st.subheader("➕ Add Your Pin")

    title = st.text_input(
        "Pin Title",
        placeholder="Jennie aesthetic..."
    )

    image_url = st.text_input(
        "Image URL",
        placeholder="Paste image URL..."
    )

    if st.button(
        "📌 Add Pin",
        use_container_width=True
    ):

        if title.strip() and image_url.strip():

            add_pin(title, image_url)

            if len(get_pins()) >= 3:
                add_badge("Pin Collector")

            st.success("Pin saved permanently 🌸")

            st.rerun()

        else:

            st.warning(
                "Please enter both title and image URL."
            )

    st.divider()

    pins = get_pins()

    if not pins:

        st.info(
            "No pins yet. Add your first one! 💗"
        )

    else:

        cols = st.columns(3)

        for i, (pin_id, title, image_url) in enumerate(pins):

            with cols[i % 3]:

                st.image(
                    image_url,
                    caption=title,
                    use_container_width=True
                )

                if st.button(
                    "🗑️ Remove",
                    key=f"delete_pin_{pin_id}"
                ):

                    delete_pin(pin_id)

                    st.success("Pin removed.")

                    st.rerun()


# =========================================================
# ACHIEVEMENTS
# =========================================================

elif page == "🏆 Achievements":

    st.title("🏆 Blink Achievements")

    st.write(
        "Complete activities to unlock badges! ✨"
    )

    badges = get_badges()

    achievements = [
        (
            "🎮",
            "Song Master",
            "Get 5 correct answers."
        ),

        (
            "📝",
            "Memory Keeper",
            "Save 3 diary memories."
        ),

        (
            "📌",
            "Pin Collector",
            "Create 3 pins."
        )
    ]

    for icon, name, description in achievements:

        if name in badges:

            st.success(
                f"{icon} **{name}** — UNLOCKED 🎉"
            )

        else:

            st.info(
                f"🔒 **{name}** — {description}"
            )

    st.divider()

    st.subheader("🏅 Your Badges")

    badges = get_badges()

    if badges:

        for badge in badges:
            st.write(f"🏅 **{badge}**")

    else:

        st.write(
            "No badges yet. Keep exploring! 💗"
        )


# =========================================================
# FOOTER
# =========================================================

st.markdown("---")

st.markdown(
    """
    <div style="text-align:center;color:#777;">
        🖤 Blink Social Hub 
    """,
    unsafe_allow_html=True
)
