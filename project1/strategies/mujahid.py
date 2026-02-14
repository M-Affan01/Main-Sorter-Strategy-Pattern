import streamlit as st
from pathlib import Path
from strategies.utils import setup_page, save_uploaded_file, clear_directory

UPLOAD_DIR = Path('uploads/mujahid')

def run():
    setup_page("Mujahid - Images (Size)", "⚖️")
    
    st.markdown("### ⚖️ Sort Images by File Size")
    
    uploaded_files = st.file_uploader("Choose Images", type=['jpg', 'png', 'gif', 'bmp', 'webp'], accept_multiple_files=True, key="mujahid_uploader")
    
    col1, col2, col3 = st.columns(3)
    sort_order = st.radio("Sort Order", ["Ascending (Smallest First)", "Descending (Largest First)"], horizontal=True)
    
    with col1:
        if st.button("Save & Sort", type="primary", use_container_width=True):
            if uploaded_files:
                for f in uploaded_files:
                    save_uploaded_file(f, UPLOAD_DIR)
            st.rerun()

    with col3:
        if st.button("Clear All", type="secondary", use_container_width=True):
            clear_directory(UPLOAD_DIR)
            st.rerun()

    if UPLOAD_DIR.exists():
        files = [p for p in UPLOAD_DIR.iterdir() if p.is_file() and p.suffix.lower() in {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'}]
        
        reverse = "Descending" in sort_order
        files.sort(key=lambda p: p.stat().st_size, reverse=reverse)
        
        if files:
            # Grid display
            cols = st.columns(4)
            for idx, f in enumerate(files):
                size_kb = f.stat().st_size / 1024
                with cols[idx % 4]:
                    st.image(str(f), use_container_width=True)
                    st.caption(f"{f.name}")
                    st.markdown(f"**{size_kb:.1f} KB**")
        else:
            st.info("No images found.")
