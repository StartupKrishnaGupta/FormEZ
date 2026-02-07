import streamlit as st
from PIL import Image
import io

# --- PAGE SETUP ---
st.set_page_config(page_title="FormEZ - Exam Photo Fixer", page_icon="⚡", layout="centered")

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: white; }
    .stButton>button { width: 100%; background-color: #FF4B4B; color: white; font-weight: bold; border-radius: 8px;}
    .stDownloadButton>button { width: 100%; background-color: #00C853; color: white; font-weight: bold; border-radius: 8px;}
    </style>
    """, unsafe_allow_html=True)

# --- BACKEND LOGIC ---
def process_image(image, target_min_kb, target_max_kb, target_w, target_h, format="JPEG"):
    img_byte_arr = io.BytesIO()
    
    # Resize
    image = image.resize((target_w, target_h))
    
    # Convert to RGB
    if image.mode in ("RGBA", "P"):
        image = image.convert("RGB")
        
    # Compress Loop
    quality = 95
    step = 5
    image.save(img_byte_arr, format=format, quality=quality)
    
    while (img_byte_arr.tell() / 1024) > target_max_kb and quality > 10:
        img_byte_arr = io.BytesIO()
        quality -= step
        image.save(img_byte_arr, format=format, quality=quality)
        
    return img_byte_arr.getvalue(), img_byte_arr.tell() / 1024

# --- FRONTEND UI ---
with st.sidebar:
    st.title("⚡ FormEZ")
    st.write("## Instructions")
    st.write("1. Select your exam.")
    st.write("2. Upload your photo.")
    st.write("3. Click 'Fix Photo'.")
    st.write("4. Download result.")
    st.info("Privacy: Photos are processed in memory and not saved.")

st.title("⚡ Fix Your Exam Photo")
st.write("Resize & Compress photos for RRB, SSC, GATE, and UPSC instantly.")

# Exam Selection
exam_options = {
    "RRB NTPC": {"min": 20, "max": 50, "w": 350, "h": 450},
    "SSC CGL/CHSL": {"min": 20, "max": 50, "w": 413, "h": 531},
    "GATE 2026": {"min": 5, "max": 200, "w": 480, "h": 640},
    "UPSC Civil Services": {"min": 20, "max": 300, "w": 350, "h": 350},
    "Passport Size (Generic)": {"min": 20, "max": 100, "w": 350, "h": 450}
}

selected_exam = st.selectbox("Select Exam Requirement", list(exam_options.keys()))
rules = exam_options[selected_exam]

st.caption(f"Target: {rules['w']}x{rules['h']} px | Size: {rules['min']}-{rules['max']} KB")

# Upload
uploaded_file = st.file_uploader("Upload your photo (JPG/PNG)", type=['jpg', 'png', 'jpeg'])

if uploaded_file:
    image = Image.open(uploaded_file)
    col1, col2 = st.columns(2)
    
    with col1:
        st.image(image, caption="Original Photo", use_column_width=True)
        
    with col2:
        if st.button("⚡ FIX PHOTO NOW"):
            with st.spinner("Processing..."):
                final_bytes, final_size = process_image(
                    image, rules['min'], rules['max'], rules['w'], rules['h']
                )
            
            st.success(f"Success! New Size: {final_size:.2f} KB")
            st.image(final_bytes, caption="Fixed Photo", use_column_width=True)
            
            st.download_button(
                label="Download Image ⬇️",
                data=final_bytes,
                file_name=f"{selected_exam.replace(' ', '_')}_fixed.jpg",
                mime="image/jpeg"
            )
