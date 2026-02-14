import streamlit as st
from pathlib import Path
from strategies.utils import setup_page, save_uploaded_file, clear_directory
from PIL import Image

UPLOAD_DIR = Path('uploads/bilal_imtiaz_images')

def get_format(path):
    try:
        with Image.open(path) as img:
            return img.format.upper() if img.format else "UNKNOWN"
    except Exception:
        return "UNKNOWN"

def run():
    setup_page("Bilal Imtiaz - Image Format", "🖼️")
    st.markdown("### 🖼️ Sort Images by Format Type")
    
    uploaded_files = st.file_uploader("Upload Images", type=['jpg', 'jpeg', 'png', 'gif', 'webp', 'bmp', 'tiff'], accept_multiple_files=True, key="bilal_imtiaz_uploader")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Identify Formats", type="primary", use_container_width=True):
            if uploaded_files:
                for f in uploaded_files:
                    save_uploaded_file(f, UPLOAD_DIR)
            st.rerun()

    with col2:
        if st.button("Reset All", type="secondary", use_container_width=True):
            clear_directory(UPLOAD_DIR)
            st.rerun()

    if UPLOAD_DIR.exists():
        images_by_fmt = {}
        files = [p for p in UPLOAD_DIR.iterdir() if p.is_file()]
        
        for p in files:
            fmt = get_format(p)
            if fmt not in images_by_fmt:
                images_by_fmt[fmt] = []
            images_by_fmt[fmt].append(p)
            
        if images_by_fmt:
            for fmt in sorted(images_by_fmt.keys()):
                with st.expander(f"📂 {fmt} ({len(images_by_fmt[fmt])})", expanded=True):
                    cols = st.columns(4)
                    for idx, p in enumerate(images_by_fmt[fmt]):
                        with cols[idx % 4]:
                            st.image(str(p), use_container_width=True)
                            st.caption(p.name)
        else:
            st.info("No images uploaded.")
