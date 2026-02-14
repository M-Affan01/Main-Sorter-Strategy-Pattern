import streamlit as st
from pathlib import Path
from strategies.utils import setup_page, save_uploaded_file, clear_directory

UPLOAD_DIR = Path('uploads/audio')

def run():
    setup_page("Sukaina - Audio (A-Z)", "🎵")
    
    st.markdown("### 🎵 Upload and Sort Audio (A-Z)")
    
    # Upload Section
    uploaded_files = st.file_uploader("Choose Audio Files", type=['mp3', 'wav', 'aac', 'flac', 'ogg'], accept_multiple_files=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Sort & Play", type="primary", use_container_width=True):
            if uploaded_files:
                for f in uploaded_files:
                    save_uploaded_file(f, UPLOAD_DIR)
            st.rerun()
            
    with col2:
        if st.button("Clear Audio", type="secondary", use_container_width=True):
            clear_directory(UPLOAD_DIR)
            st.rerun()

    # Display Logic
    if UPLOAD_DIR.exists():
        files = [p for p in UPLOAD_DIR.iterdir() if p.is_file() and p.suffix.lower() in {'.mp3', '.wav', '.aac', '.flac', '.ogg'}]
        # Sort by Name
        files.sort(key=lambda p: p.name.lower())
        
        if files:
            for f in files:
                with st.container():
                    st.markdown(f"""
                    <div class="glass-card" style="padding: 1rem; margin-bottom: 0.5rem; animation: none;">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                            <span style="font-weight: 600; font-family: 'Outfit';">📀 {f.name}</span>
                            <span style="color: #94a3b8; font-size: 0.9rem;">{f.stat().st_size / (1024*1024):.1f} MB</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    st.audio(str(f))
        else:
            st.info("No audio files found. Upload some to get started!")
