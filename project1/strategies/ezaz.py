import streamlit as st
from pathlib import Path
from strategies.utils import setup_page, save_uploaded_file, clear_directory
import shutil

UPLOAD_DIR = Path('uploads/ezaz_audio')

class AudioFile:
    def __init__(self, path: Path):
        self.path = path
        self.filename = path.name

    def get_format(self):
        return self.path.suffix.lower().lstrip('.')

def run():
    setup_page("Ezaz - Audio Filter", "🎵")
    
    st.markdown("### 🎵 Filter Audio Files (MP3 / WAV)")
    
    uploaded_files = st.file_uploader("Upload Audio", type=['mp3', 'wav'], accept_multiple_files=True, key="ezaz_uploader")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Upload & Filter", type="primary", use_container_width=True):
            if uploaded_files:
                for f in uploaded_files:
                    save_uploaded_file(f, UPLOAD_DIR)
            st.rerun()

    with col2:
        if st.button("Reset All", type="secondary", use_container_width=True):
            clear_directory(UPLOAD_DIR)
            st.rerun()

    # Filter Controls
    filter_option = st.radio("Show Format:", ["All", "MP3", "WAV"], horizontal=True)

    if UPLOAD_DIR.exists():
        files = [p for p in UPLOAD_DIR.iterdir() if p.is_file() and p.suffix.lower() in {'.mp3', '.wav'}]
        
        filtered_files = []
        for p in files:
            audio = AudioFile(p)
            fmt = audio.get_format()
            if filter_option == "All":
                filtered_files.append((p, fmt))
            elif filter_option == "MP3" and fmt == 'mp3':
                filtered_files.append((p, fmt))
            elif filter_option == "WAV" and fmt == 'wav':
                filtered_files.append((p, fmt))
        
        if filtered_files:
            st.markdown(f"**Found {len(filtered_files)} files**")
            for p, fmt in filtered_files:
                color = "#3b82f6" if fmt == 'mp3' else "#ec4899"
                st.markdown(f"""
                <div class="glass-card" style="padding: 1rem; margin-bottom: 0.5rem; border-left: 5px solid {color}; animation: none;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="font-weight: 600; font-family: 'Outfit';">📀 {p.name}</span>
                        <span style="background: {color}; color: white; padding: 2px 10px; border-radius: 10px; font-size: 0.8rem; text-transform: uppercase; font-weight: 800;">{fmt}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                st.audio(str(p), format=f'audio/{fmt}')
        else:
            if files:
                st.info(f"No {filter_option} files found.")
            else:
                st.info("No audio files uploaded.")
