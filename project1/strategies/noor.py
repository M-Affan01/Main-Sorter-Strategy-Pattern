import streamlit as st
from pathlib import Path
from strategies.utils import setup_page, save_uploaded_file, clear_directory
from PIL import Image

UPLOAD_DIR = Path('uploads/noor_images')

def run():
    setup_page("Noor - Image Browser", "📷")
    st.markdown("### 📷 Premium Image Browser")
    
    uploaded_files = st.file_uploader("Upload Images", type=['jpg', 'png', 'jpeg', 'webp'], accept_multiple_files=True, key="noor_uploader")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Upload to Gallery", type="primary", use_container_width=True):
            if uploaded_files:
                for f in uploaded_files:
                    save_uploaded_file(f, UPLOAD_DIR)
            st.rerun()

    with col2:
        if st.button("Clear Gallery", type="secondary", use_container_width=True):
            clear_directory(UPLOAD_DIR)
            st.rerun()

    if UPLOAD_DIR.exists():
        images = []
        for p in UPLOAD_DIR.iterdir():
            if p.is_file():
                try:
                    with Image.open(p) as img:
                        w, h = img.size
                        pixels = w * h
                        images.append({
                            'path': p,
                            'name': p.name,
                            'res': f"{w} x {h}",
                            'pixels': pixels,
                            'size': p.stat().st_size
                        })
                except Exception:
                    pass
        
        if images:
            # Sorting
            sort_mode = st.radio("Sort By:", ["Name", "Resolution (Pixels)"], horizontal=True)
            order = st.radio("Order:", ["Ascending", "Descending"], horizontal=True)
            
            reverse = (order == "Descending")
            if sort_mode == "Name":
                images.sort(key=lambda x: x['name'].lower(), reverse=reverse)
            else:
                images.sort(key=lambda x: x['pixels'], reverse=reverse)
            
            # Display Grid
            st.markdown(f"**Showing {len(images)} images**")
            cols = st.columns(3)
            for idx, item in enumerate(images):
                with cols[idx % 3]:
                    st.image(str(item['path']), use_container_width=True)
                    st.markdown(f"""
                    <div style="font-weight: bold; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">{item['name']}</div>
                    <div style="color: #6366f1; font-size: 0.8rem;">📏 {item['res']}</div>
                    """, unsafe_allow_html=True)
        else:
            st.info("Gallery is empty.")
