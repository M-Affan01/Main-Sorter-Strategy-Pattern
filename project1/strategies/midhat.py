import streamlit as st
from pathlib import Path
import subprocess
import shutil
from strategies.utils import setup_page, save_uploaded_file, clear_directory

UPLOAD_DIR = Path('uploads/midhat_videos')

def get_video_duration(file_path: Path) -> float:
    try:
        cmd = [
            'ffprobe', '-v', 'error',
            '-show_entries', 'format=duration',
            '-of', 'default=noprint_wrappers=1:nokey=1',
            str(file_path)
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        if result.returncode == 0 and result.stdout.strip():
            return float(result.stdout.strip())
    except Exception:
        pass
    return 0.0

def run():
    setup_page("Midhat - Videos (Duration)", "⏳")
    
    st.markdown("### ⏳ Sort Videos by Duration & Size")
    
    # Dependency Check
    if shutil.which("ffprobe") is None:
        st.error("⚠️ `ffprobe` not found! Please install FFmpeg to use this sorter.")
        return

    uploaded_files = st.file_uploader("Choose Videos", type=['mp4', 'mov', 'avi', 'mkv', 'webm', 'wmv'], accept_multiple_files=True, key="midhat_uploader")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Sort by Duration", type="primary", use_container_width=True):
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
        
        # Sort logic: Duration DESC, then Size
        # We need to compute duration for all to sort
        video_items = []
        with st.spinner("Analyzing videos..."):
            for p in files:
                duration = get_video_duration(p)
                size_mb = p.stat().st_size / (1024 * 1024)
                video_items.append({'path': p, 'duration': duration, 'size': size_mb})
        
        # Sort
        video_items.sort(key=lambda x: (x['duration'], x['size']), reverse=True)
        
        if video_items:
            for item in video_items:
                p = item['path']
                mins, secs = divmod(item['duration'], 60)
                st.markdown(f"""
                <div class="glass-card" style="padding: 1rem; margin-bottom: 0.5rem; animation: none;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="font-weight: 600; font-family: 'Outfit';">🎬 {p.name}</span>
                        <div style="text-align: right;">
                            <span style="color: #60a5fa; font-weight: bold; margin-right: 15px;">{int(mins)}m {int(secs)}s</span>
                            <span style="color: #94a3b8; font-size: 0.9rem;">{item['size']:.1f} MB</span>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                with st.expander("Play Video"):
                    st.video(str(p))
        else:
            st.info("No videos found.")
