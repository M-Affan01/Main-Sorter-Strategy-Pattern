import streamlit as st
from pathlib import Path
from strategies.utils import setup_page, save_uploaded_file, clear_directory

UPLOAD_DIR = Path('uploads/audio')

def run():
    setup_page("Abdullah - Audio (Size)", "📊")
    
    st.markdown("### 📊 Upload and Audio by Size")
    
    uploaded_files = st.file_uploader("Choose Audio Files", type=['mp3', 'wav', 'aac', 'flac', 'ogg'], accept_multiple_files=True, key="abdullah_uploader")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Sort by Size", type="primary", use_container_width=True):
            if uploaded_files:
                for f in uploaded_files:
                    save_uploaded_file(f, UPLOAD_DIR)
            st.rerun()
            
    with col2:
        if st.button("Clear Audio", type="secondary", use_container_width=True):
            clear_directory(UPLOAD_DIR)
            st.rerun()

    if UPLOAD_DIR.exists():
        files = [p for p in UPLOAD_DIR.iterdir() if p.is_file() and p.suffix.lower() in {'.mp3', '.wav', '.aac', '.flac', '.ogg'}]
        # Sort by Size
        files.sort(key=lambda p: p.stat().st_size)
        
        if files:
            for f in files:
                with st.container():
                    st.markdown(f"""
                    <div style="background: rgba(30, 41, 59, 0.7); padding: 1rem; border-radius: 0.5rem; margin-bottom: 0.5rem; border: 1px solid rgba(255,255,255,0.1);">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                            <span style="font-weight: 600;">📀 {f.name}</span>
                            <span style="color: #10b981; font-weight: bold;">{f.stat().st_size / (1024*1024):.1f} MB</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    st.audio(str(f))
        else:
            st.info("No audio files found.")
