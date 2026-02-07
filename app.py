import streamlit as st
from PIL import Image
import io
import time

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="FormEZ - Gen Z Edition",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- THEME MANAGEMENT ---
if 'theme' not in st.session_state:
    st.session_state.theme = 'Dark 🌑'

# --- CSS STYLING ---
def get_css(theme):
    if "Dark" in theme:
        bg_color = "#0a0a0a"
        card_bg = "rgba(255, 255, 255, 0.05)"
        text_color = "#ffffff"
        accent_gradient = "linear-gradient(90deg, #FF4B4B, #FF914D)"
        border_color = "rgba(255, 255, 255, 0.1)"
    else:
        bg_color = "#f4f4f5"
        card_bg = "rgba(255, 255, 255, 0.8)"
        text_color = "#18181b"
        accent_gradient = "linear-gradient(90deg, #3B82F6, #8B5CF6)"
        border_color = "rgba(0, 0, 0, 0.1)"

    return f"""
    <style>
    .stApp {{
        background-color: {bg_color};
        color: {text_color};
    }}
    .stSelectbox > div > div {{
        background-color: {card_bg};
        color: {text_color};
        border-radius: 12px;
    }}
    .stButton>button {{
        background: {accent_gradient};
        color: white;
        border: none;
        padding: 0.75rem;
        border-radius: 12px;
        font-weight: 700;
        transition: transform 0.2s;
    }}
    .stButton>button:hover {{
        transform: scale(1.02);
    }}
    h1, h2, h3 {{
        background: {accent_gradient};
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-family: 'Inter', sans-serif;
    }}
    </style>
    """

# --- SIDEBAR ---
with st.sidebar:
    st.title("⚙️ Settings")
    st.session_state.theme = st.radio("Choose Vibe", ["Dark 🌑", "Light ☀️"])
    st.markdown("---")
    st.caption("Built for Gen Z 🚀")

st.markdown(get_css(st.session_state.theme), unsafe_allow_html=True)

# --- HEADER ---
st.title("⚡ FormEZ")
st.markdown("### The Ultimate Exam Photo Fixer")
st.caption("Auto-resize your pics for JEE, NEET, UPSC & more.")

# --- EXAM DATA ---
exam_options = {
    "JEE Mains 2026": {"min": 10, "max": 200, "w": 350, "h": 450},
    "NEET UG": {"min": 10, "max": 200, "w": 350, "h": 450},
    "RRB NTPC": {"min": 20, "max": 50, "w": 350, "h": 450},
    "SSC CGL": {"min": 20, "max": 50, "w": 413, "h": 531},
    "UPSC Civil Services": {"min": 20, "max": 300, "w": 350, "h": 350},
    "Passport Size": {"min": 20, "max": 100, "w": 350, "h": 450}
}

# --- MAIN UI ---
col1, col2 = st.columns([1, 1.5], gap="large")

with col1:
    st.subheader("1️⃣ Select Exam")
    selected_exam = st.selectbox("Target Exam", list(exam_options.keys()))
    rules = exam_options[selected_exam]
    st.info(f"**Specs:** {rules['w']}x{rules['h']}px | {rules['min']}-{rules['max']}KB")

with col2:
    st.subheader("2️⃣ Upload Photo")
    uploaded_file = st.file_uploader("Drop image here", type=['jpg', 'png', 'jpeg'])

# --- IMAGE PROCESSING ---
def process_image(image, rules):
    img_byte_arr = io.BytesIO()
    image = image.resize((rules['w'], rules['h']), Image.Resampling.LANCZOS)
    
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    quality = 95
    while quality > 10:
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='JPEG', quality=quality)
        if (img_byte_arr.tell() / 1024) <= rules['max']:
            break
        quality -= 5
        
    return img_byte_arr.getvalue(), img_byte_arr.tell() / 1024

if uploaded_file:
    st.markdown("---")
    image = Image.open(uploaded_file)
    
    c1, c2, c3 = st.columns([1, 0.5, 1])
    with c1:
        st.image(image, caption="Original", use_container_width=True)
    
    with c3:
        if st.button("✨ Glow Up Photo"):
            with st.spinner("Processing..."):
                time.sleep(0.5)
                final_bytes, final_size = process_image(image, rules)
            
            st.image(final_bytes, caption=f"Fixed ({final_size:.1f} KB)", use_container_width=True)
            st.balloons()
            st.download_button("⬇️ Download", final_bytes, file_name="fixed.jpg", mime="image/jpeg")

# --- NEWSLETTER ---
st.markdown("---")
st.subheader("📩 Stay Updated")
email = st.text_input("Enter email for daily updates")
if st.button("Subscribe 🔔"):
    if email:
        st.toast("Welcome to the squad! 🔥")
    else:
        st.error("Please enter an email!")
