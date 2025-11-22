# app.py — Final Memory Flipbook (Option A)
# - Memory page with simple slide-style transitions (stable)
# - Separate letter page (no glitch between Next/Previous/Letter)
# - Soft pink diary aesthetic (CSS)
# - Copy -> paste into your project root (memory_flipbook/app.py)
#
# Note: You previously uploaded a heart sticker at:
# /mnt/data/a4e98056-4d96-40c6-bb87-101ca6cb6f2a.png
# (kept here as reference only; no stickers are used in this version)

import streamlit as st
from PIL import Image
import os

# ---------------------------
# Page config
# ---------------------------
st.set_page_config(page_title="Our Memory Flipbook 💝", page_icon="💞", layout="wide")

# ---------------------------
# CSS (soft pink diary look + simple slide)
# ---------------------------
st.markdown(
    """
    <style>
    :root {
      --pink-1: #ffe6f2;
      --pink-2: #fff6ff;
      --accent: #d63384;
    }
    body {
      background: linear-gradient(to bottom right, var(--pink-1), var(--pink-2));
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial;
    }
    .page-wrap {
      max-width: 920px;
      margin: 18px auto;
    }
    .memory-card {
      background: rgba(255,255,255,0.70);
      backdrop-filter: blur(8px);
      border-radius: 18px;
      padding: 18px;
      box-shadow: 0 10px 30px rgba(255,100,150,0.12);
      transition: transform 0.45s ease, opacity 0.45s ease;
      overflow: hidden;
    }
    .slide-in-left { transform: translateX(-8px); opacity: 1; }
    .slide-in-right { transform: translateX(8px); opacity: 1; }
    .polaroid {
      padding: 8px;
      background: white;
      border-radius: 10px;
      box-shadow: 0 6px 18px rgba(0,0,0,0.12);
      position: relative;
    }
    .title-text {
      font-size: 28px;
      font-weight: 700;
      text-align: center;
      color: var(--accent);
      margin-bottom: 6px;
    }
    .excerpt {
      font-size: 15px;
      margin-top: 8px;
      color: #333;
    }
    .meta {
      color: #666;
      font-size: 13px;
      margin-top: 4px;
    }
    .letter-box {
      background: white;
      padding: 24px;
      border-radius: 14px;
      box-shadow: 0 6px 20px rgba(0,0,0,0.06);
    }
    .nav-button {
      background: white;
      border-radius: 8px;
      padding: 8px 12px;
      box-shadow: 0 3px 10px rgba(0,0,0,0.06);
      border: none;
      cursor: pointer;
    }
    /* responsive */
    @media (max-width: 720px) {
      .title-text { font-size: 22px; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------
# Your memories (keep as you wrote them)
# ---------------------------
memories = [
    {
        "title": "our first concert",
        "date": "20th december 2024",
        "image": "images/IMG-20251122-WA0011.jpg",
        "excerpt": "WE WENT TO THE SHAAN CONCERT TOGETHER BABE",
        "letter": """
i was genuinely so happy , more so because i was experiencing it with you.
i saw you waiting for me at the end of the metro in that cute green sweatshirt, so nonchalant 
until u looked at me and smiled and literally stole my heart. every moment from running towards the venue,
sitting on ur lap almost the whole concert to dancing our literal hearts out meant alot to me. 
"""
    },
    {
        "title": "a cute/funny date",
        "date": "2nd may 2025",
        "image": "images/IMG-20251122-WA0013.jpg",
        "excerpt": "HOW DID WE RUN INTO YOU EX BABE",
        "letter": """
i remember arguing with you this day and then gundu asked me to meet him at church st. i was still mad but ok.
i love being with you so. i was waiting for u and then you popped up, hiding something, flowers. awwwwwww i love you
you made it upto me and we went to eat food and ran into ur ex and we had salty laphing. then we went to mcd where
we just talked for hours and hours and had so much fun. what a weirdly nice day.
"""
    },
    {
        "title": "just another day made special",
        "date": "15th april 2025",
        "image": "images/IMG-20251122-WA0012.jpg",
        "excerpt": "IM WEARING YOUR SHIRT BETTER THAN YOU BABE",
        "letter": """
i came over had so much in my mind, all chaos. saw you, hugged you, kissed you and all of it disappeared into thin air.
hung out with scooby like always hes a gundu. had some good food (you) and took a nice hot shower. decided to take pics
ofc you wont question it and got some cute pics(for my wallpaper ofc). had some good kebab n biryani and slept like a baby
in your bed ofc. called it a day. just another day, made special by you.
"""
    },
    {
        "title": "bakrid special",
        "date": "7th june 2025",
        "image": "images/IMG-20251122-WA0017.jpg",
        "excerpt": "FINALLY SOME TRADITIONAL PICS BABE",
        "letter": """
u came over after i just had a long day spending bakrid with family. still in my outfit cuz i wanted you to see me 
and call me your beautiful girl. you did as soon as you saw me. then kissed me. again wanted some pics and ofc u were
acting goofy in more than half of them. still my fav. the way we cant be serious in any picture(ur fault). 
made u eat the biryani i made(u better have loved it). went to sleep hugging each other peacefully.
"""
    },
    {
        "title": "after 3 months",
        "date": "17th september 2025",
        "image": "images/IMG-20251122-WA0015.jpg",
        "excerpt": "AFTER 3 GUT WRENCHING MONTHS THAT ALMOST KILLED ME BABE",
        "letter": """
YOU finally came to meet me after so fucking long 3 months felt like an eternity almost. but oh my god the happiness i felt
that day seeing you could not even be measured. hugging you and kissing you just being in your arms after so long felt like home.
i wished it could be like this always. we talked and talked, went to eat kfc, hit the gym together came back and well ykw happened haha
and played uno (im better) and had yummy dinner wow everything felt as if its meant to be like this. 
it felt real. everything with you.
"""
    },
    {
        "title": "bike ride",
        "date": "18th september 2025",
        "image": "images/IMG-20251122-WA0020.jpg",
        "excerpt": "BIKE RIDE BABE",
        "letter": """
we rode so much this day my butt hurt but u see that smile its because i was riding with you
"""
    },
    {
        "title": "dancing day",
        "date": "10th october 2025",
        "image": "images/IMG-20251122-WA0022.jpg",
        "excerpt": "LEARNT A DANCE TOGETHER BABE",
        "letter": """
i was so happy we spent the whole time dancing together and you did so well gundu, learnt new dances and
did the just dance thing which was the best part of the whole day tbh.
"""
    },
    {
        "title": "idli day",
        "date": "8th october 2025",
        "image": "images/IMG-20251122-WA0023.jpg",
        "excerpt": "ATE BREAKFAST TOGETHER BABE",
        "letter": """
its like a ritual for us, i eat idli u eat masala dosa and we have the best time ever making pointless vlogs.
"""
    },
    {
        "title": "your first show",
        "date": "17th october 2025",
        "image": "images/IMG-20251122-WA0025.jpg",
        "excerpt": "YOU HOSTED A WHOLE ASS GAMESHOW BABE",
        "letter": """
i couldnt be more proud of you. i was almost about to cry. you did so well, you managed everything as if
it just comes easily to you, you were such a good host, you made everyone who cares about you so damn proud.
you put your all into it. i am so so proud of you. i would never not be.
"""
    },
    {
        "title": "our first diwali",
        "date": "20th october 2025",
        "image": "images/IMG-20251122-WA0024.jpg",
        "excerpt": "DIWALI PARTY BABE",
        "letter": """
went to a cute diwali party with you. i was so excited. had so much fun playing cute games meeting new people
all of it with you. got some cute pics and food went home and literally passed out together.
"""
    },
    {
        "title": "gaming together",
        "date": "21th october 2025",
        "image": "images/IMG-20251122-WA0027.jpg",
        "excerpt": "GAMING CAFE BABE",
        "letter": """
made me the mic because its funny. very funny. you look so happy while playing, or doing anything you love
fills my heart with joy just looking at you being happy.
"""
    },
    {
        "title": "my happy baby",
        "date": "should always be",
        "image": "images/IMG-20251122-WA0031.jpg",
        "excerpt": "AWWW",
        "letter": """
nothing just my happy baby
"""
    },
    {
        "title": "my silly baby",
        "date": "should always be",
        "image": "images/IMG-20251122-WA0030.jpg",
        "excerpt": "AWWW",
        "letter": """
nothing just my silly baby
"""
    },
    {
        "title": "my clueless baby",
        "date": "should always be",
        "image": "images/IMG-20251122-WA0033.jpg",
        "excerpt": "AWWW",
        "letter": """
nothing just my clueless baby
"""
    },
    {
        "title": "my handsome baby",
        "date": "should always be",
        "image": "images/IMG-20251122-WA0032.jpg",
        "excerpt": "AWWW",
        "letter": """
nothing just my handsome baby
"""
    },
    {
        "title": "my nonchalant baby",
        "date": "should always be",
        "image": "images/IMG-20251122-WA0034.jpg",
        "excerpt": "AWWW",
        "letter": """
nothing just my nonchalant baby
"""
    },
    {
        "title": "my strong baby",
        "date": "should always be",
        "image": "images/IMG-20251122-WA0026.jpg",
        "excerpt": "AWWW",
        "letter": """
nothing just my strong baby
"""
    },
    {
        "title": "my aloo baby",
        "date": "should always be",
        "image": "images/IMG-20251122-WA0029.jpg",
        "excerpt": "AWWW",
        "letter": """
happy birthday meri jaan i love you so much. you will always be my aloo motu cutu baby. every single moment ive spent
with you this past year is worth more that i can express with my words here. i wanna tell you that you mean the whole damn universe
to me. i wish i could give you everything you deserve and more. but for now my love is all i have. you have always made me so proud
everything you do, every little thing, even when you annoy the living shit out of me is just adorable. i remember saying
beign with you feels like a dream. i was wrong. being with you is the most real thing ive ever felt. like a peaceful home
you wanna stay in forever. where you forget all your worries, problems , better yet solve them. you've grown alot this past year
and im so proud of you for that. you always learn from everything you do, you worry about your loved ones even if they hurt you.
i know how hard that is, and you are so strong for always just being there. you are so strong for never giving up. you are
so strong for always having hope despite everything. you are so strong for overcoming everything that has come your way.
lastly i just want you to know i will always cheer the loudest for you, stand beside you and support you in whatever situation 
that may come our way. baby you are enough. and i will love you always and forever.
"""
    },
]

# ---------------------------
# Session state (stable nav)
# ---------------------------
if "page" not in st.session_state:
    st.session_state.page = 0
if "view" not in st.session_state:
    st.session_state.view = "memory"  # or "letter"
if "direction" not in st.session_state:
    st.session_state.direction = "none"  # "left" or "right" used for styling briefly

total = len(memories)
current = memories[st.session_state.page]

# helper functions
def go_next():
    st.session_state.direction = "right"
    st.session_state.page = (st.session_state.page + 1) % total

def go_prev():
    st.session_state.direction = "left"
    st.session_state.page = (st.session_state.page - 1) % total

def open_letter():
    st.session_state.view = "letter"

def back_to_memory():
    st.session_state.view = "memory"

# ---------------------------
# Letter page (separate, stable)
# ---------------------------
if st.session_state.view == "letter":
    st.markdown("<div class='page-wrap'>", unsafe_allow_html=True)
    st.markdown(f"<div class='memory-card'>", unsafe_allow_html=True)
    st.markdown(f"<h2 class='title-text'>{current['title']}  💌</h2>", unsafe_allow_html=True)
    st.write(f"**{current['date']}**")
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<div class='letter-box'>", unsafe_allow_html=True)
    st.write(current["letter"])
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # navigation row
    col1, col2, col3, col4 = st.columns([1,1,1,1])
    with col1:
        if st.button("⬅ Back to Memory"):
            back_to_memory()
    with col2:
        if st.button("⬅ Previous Letter"):
            go_prev()
            # stay on letter view after changing page
            st.session_state.view = "letter"
    with col3:
        if st.button("Next Letter ➡"):
            go_next()
            st.session_state.view = "letter"
    with col4:
        if st.button("🏠 Home"):
            back_to_memory()

    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# ---------------------------
# Memory page (main)
# ---------------------------
st.markdown("<div class='page-wrap'>", unsafe_allow_html=True)

# Title
st.markdown(f"<h1 class='title-text'>Our Memory Flipbook ✨</h1>", unsafe_allow_html=True)
st.write("")

# Card with optional simple slide class
slide_class = ""
if st.session_state.direction == "left":
    slide_class = "slide-in-left"
elif st.session_state.direction == "right":
    slide_class = "slide-in-right"

st.markdown(f"<div class='memory-card {slide_class}'>", unsafe_allow_html=True)

# Image
if os.path.exists(current["image"]):
    try:
        img = Image.open(current["image"])
        # show image
        st.markdown("<div class='polaroid'>", unsafe_allow_html=True)
        st.image(img, use_column_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    except Exception as e:
        st.write("Image couldn't be opened:", e)
else:
    st.write("Image not found:", current["image"])

# Title / meta / excerpt
st.markdown(f"### {current['title']}  ✨", unsafe_allow_html=True)
st.markdown(f"**{current['date']}**", unsafe_allow_html=True)
st.markdown(f"<div class='excerpt'>{current['excerpt']}</div>", unsafe_allow_html=True)

# Read letter button (opens separate page)
if st.button("Read my full letter 💌"):
    st.session_state.view = "letter"
    st.experimental_rerun()


st.markdown("</div>", unsafe_allow_html=True)

# Navigation buttons
# --- Navigation buttons (fixed, stable) ---
col_l, col_mid, col_r = st.columns([1, 1, 1])

with col_l:
    if st.button("⬅ Previous"):
        st.session_state.direction = "left"
        st.session_state.page = (st.session_state.page - 1) % total
        st.session_state.view = "memory"
        st.experimental_rerun()

with col_r:
    if st.button("Next ➡"):
        st.session_state.direction = "right"
        st.session_state.page = (st.session_state.page + 1) % total
        st.session_state.view = "memory"
        st.experimental_rerun()



# small helper: reset direction so animation doesn't persist forever
# (this keeps styling simple; it's safe to leave as-is)
st.session_state.direction = "none"
