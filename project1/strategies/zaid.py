import streamlit as st
from pathlib import Path
from strategies.utils import setup_page, save_uploaded_file, clear_directory
from PIL import Image

UPLOAD_DIR = Path('uploads/zaid_images')

def get_aspect_ratio(path):
    try:
        with Image.open(path) as img:
            w, h = img.size
            return w / h if h != 0 else 0
    except Exception:
        return 0

def run():
    setup_page("Zaid - Aspect Ratio", "📐")
    
    st.markdown("### 📐 Sort Images by Aspect Ratio (Width/Height)")
    
    uploaded_files = st.file_uploader("Upload Images", type=['jpg', 'png', 'jpeg'], accept_multiple_files=True, key="zaid_uploader")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Sort Images", type="primary", use_container_width=True):
            if uploaded_files:
                for f in uploaded_files:
                    save_uploaded_file(f, UPLOAD_DIR)
            st.rerun()

    with col2:
        if st.button("Reset All", type="secondary", use_container_width=True):
            clear_directory(UPLOAD_DIR)
            st.rerun()

    if UPLOAD_DIR.exists():
        files = [p for p in UPLOAD_DIR.iterdir() if p.is_file()]
        
        # Sort logic
        data = []
        for p in files:
            ratio = get_aspect_ratio(p)
            if ratio > 0:
                data.append((p, ratio))
        
        data.sort(key=lambda x: x[1])
        
        if data:
            cols = st.columns(3)
            for idx, (p, ratio) in enumerate(data):
                with cols[idx % 3]:
                    st.image(str(p), use_container_width=True)
                    st.caption(f"{p.name}")
                    st.markdown(f"**Ratio: {ratio:.2f}**")
        else:
            st.info("No valid images found.")
