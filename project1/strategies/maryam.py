import streamlit as st
from pathlib import Path
from strategies.utils import setup_page, save_uploaded_file, clear_directory
import shutil
import re
import datetime

UPLOAD_DIR = Path('uploads/maryam_audio')

def sort_and_rename(folder: Path):
    if not folder.exists():
        return []
    
    files = [p for p in folder.iterdir() if p.is_file() and p.suffix.lower() in {'.mp3', '.wav', '.m4a', '.aac', '.ogg', '.flac'}]
    
    # Sort by creation time (Newest First)
    files.sort(key=lambda p: p.stat().st_ctime, reverse=True)
    
    renamed = []
    for idx, p in enumerate(files, 1):
        original_name = p.name
        # Remove existing prefix if any
        clean_name = re.sub(r"^\d{3}_", "", original_name)
        new_name = f"{idx:03d}_{clean_name}"
        new_path = p.parent / new_name
        
        if p != new_path:
            try:
                p.rename(new_path)
            except Exception:
                new_path = p 
        
        renamed.append((new_path, new_path.stat().st_ctime))
    return renamed

def format_date(ts):
    return datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

def run():
    setup_page("Maryam - Audio Newest", "⬇️")
    st.markdown("### ⬇️ Sort Audio Newest First (Auto-Rename)")
    st.caption("Files will be renamed with `001_`, `002_` prefixes based on creation time.")
    
    uploaded_files = st.file_uploader("Upload Audio", type=['mp3', 'wav', 'm4a'], accept_multiple_files=True, key="maryam_uploader")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Sort & Rename", type="primary", use_container_width=True):
            if uploaded_files:
                for f in uploaded_files:
                    save_uploaded_file(f, UPLOAD_DIR)
            st.rerun()

    with col2:
        if st.button("Reset All", type="secondary", use_container_width=True):
            clear_directory(UPLOAD_DIR)
            st.rerun()

    if UPLOAD_DIR.exists():
        tracks = sort_and_rename(UPLOAD_DIR)
        
        if tracks:
            st.markdown(f"**Total Tracks: {len(tracks)}**")
            for idx, (p, ts) in enumerate(tracks):
                date_str = format_date(ts)
                st.markdown(f"""
                <div style="background: rgba(30, 41, 59, 0.7); padding: 1rem; border-radius: 0.5rem; margin-bottom: 0.5rem; border: 1px solid rgba(255,255,255,0.1); display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <div style="font-weight: 600; color: #f1f5f9;">{p.name}</div>
                        <div style="font-size: 0.8rem; color: #94a3b8;">📅 {date_str}</div>
                    </div>
                    <div style="background: #06b6d4; color: white; font-weight: bold; padding: 5px 10px; border-radius: 5px;">#{idx+1}</div>
                </div>
                """, unsafe_allow_html=True)
                st.audio(str(p))
        else:
            st.info("No audio files found.")
