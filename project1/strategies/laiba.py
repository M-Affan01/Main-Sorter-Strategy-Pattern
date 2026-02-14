import streamlit as st
from pathlib import Path
from strategies.utils import setup_page, save_uploaded_file, clear_directory
from PIL import Image
import numpy as np

UPLOAD_DIR = Path('uploads/laiba_intensity')

def get_intensity(path):
    try:
        with Image.open(path) as img:
            gray = img.convert('L')
            return np.mean(np.array(gray))
    except Exception:
        return 0.0

def run():
    setup_page("Laiba - Image Intensity", "💡")
    st.markdown("### 💡 Sort Images by Intensity (Darkest to Brightest)")
    
    uploaded_files = st.file_uploader("Upload Images", type=['jpg', 'jpeg', 'png', 'webp'], accept_multiple_files=True, key="laiba_uploader")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Sort by Intensity", type="primary", use_container_width=True):
            if uploaded_files:
                for f in uploaded_files:
                    save_uploaded_file(f, UPLOAD_DIR)
            st.rerun()

    with col2:
        if st.button("Reset All", type="secondary", use_container_width=True):
            clear_directory(UPLOAD_DIR)
            st.rerun()

    if UPLOAD_DIR.exists():
        images = []
        for p in UPLOAD_DIR.iterdir():
            if p.is_file():
                images.append({'path': p, 'intensity': get_intensity(p)})
        
        # Sort Darkest -> Brightest
        images.sort(key=lambda x: x['intensity'])
        
        if images:
            st.markdown(f"**Sorted {len(images)} Images**")
            cols = st.columns(4)
            for idx, item in enumerate(images):
                p = item['path']
                val = item['intensity']
                with cols[idx % 4]:
                    st.image(str(p), use_container_width=True)
                    st.caption(f"{p.name}")
                    st.progress(val / 255.0)
                    st.markdown(f"<div style='text-align:center; font-size:0.8rem;'>Intensity: {val:.1f}</div>", unsafe_allow_html=True)
        else:
            st.info("No images uploaded.")
