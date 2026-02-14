import streamlit as st
from pathlib import Path
from strategies.utils import setup_page, save_uploaded_file, clear_directory
import datetime
import shutil
import os

UPLOAD_DIR = Path('uploads/fabiha_images')

def organize_by_date(folder: Path):
    if not folder.exists():
        return {}
        
    organized = {}
    files = [p for p in folder.rglob('*') if p.is_file() and p.suffix.lower() in {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'}]
    
    for p in files:
        # Get creation date
        timestamp = p.stat().st_ctime
        date_folder = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
        
        target_dir = folder / date_folder
        target_dir.mkdir(exist_ok=True)
        target_path = target_dir / p.name
        
        if p.parent != target_dir:
            try:
                shutil.move(str(p), str(target_path))
                p = target_path # Update path pointer
            except Exception:
                pass
        
        if date_folder not in organized:
            organized[date_folder] = []
        organized[date_folder].append(p)
    
    return organized

def run():
    setup_page("Fabiha - Image Date", "📅")
    st.markdown("### 📅 Organize Images by Date (YYYY-MM-DD)")
    
    uploaded_files = st.file_uploader("Upload Images", type=['jpg', 'jpeg', 'png', 'gif'], accept_multiple_files=True, key="fabiha_uploader")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Organize Now", type="primary", use_container_width=True):
            if uploaded_files:
                for f in uploaded_files:
                    save_uploaded_file(f, UPLOAD_DIR)
            st.rerun()

    with col2:
        if st.button("Reset All", type="secondary", use_container_width=True):
            clear_directory(UPLOAD_DIR)
            st.rerun()

    if UPLOAD_DIR.exists():
        organized = organize_by_date(UPLOAD_DIR)
        
        if organized:
            for date in sorted(organized.keys(), reverse=True):
                with st.expander(f"📆 {date} ({len(organized[date])} images)", expanded=True):
                    cols = st.columns(4)
                    for idx, p in enumerate(organized[date]):
                        with cols[idx % 4]:
                            st.image(str(p), use_container_width=True)
                            st.caption(p.name)
        else:
            st.info("No images found.")
