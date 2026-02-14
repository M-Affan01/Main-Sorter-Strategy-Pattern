import streamlit as st
from pathlib import Path
from strategies.utils import setup_page, save_uploaded_file, clear_directory

UPLOAD_DIR = Path('uploads/videos')

def run():
    setup_page("Habiba - Videos", "🎥")
    
    st.markdown("### 🎥 Video Player (A-Z)")
    
    uploaded_files = st.file_uploader("Choose Videos", type=['mp4', 'mov', 'avi', 'mkv', 'webm'], accept_multiple_files=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Sort & Play", type="primary", use_container_width=True):
            if uploaded_files:
                for f in uploaded_files:
                    save_uploaded_file(f, UPLOAD_DIR)
            st.rerun()
            
    with col2:
        if st.button("Clear Videos", type="secondary", use_container_width=True):
            clear_directory(UPLOAD_DIR)
            st.rerun()

    if UPLOAD_DIR.exists():
        files = [p for p in UPLOAD_DIR.iterdir() if p.is_file() and p.suffix.lower() in {'.mp4', '.mov', '.avi', '.mkv', '.webm', '.flv', '.wmv'}]
        # Sort by Name
        files.sort(key=lambda p: p.name.lower())
        
        if files:
            for f in files:
                with st.expander(f"🎬 {f.name} ({f.stat().st_size / (1024*1024):.1f} MB)", expanded=True):
                    st.video(str(f))
        else:
            st.info("No videos found.")
