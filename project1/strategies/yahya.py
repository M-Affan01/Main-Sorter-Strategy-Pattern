import streamlit as st
from pathlib import Path
from strategies.utils import setup_page, save_uploaded_file, clear_directory
import shutil
import subprocess
import wave

# Optional imports
try:
    from mutagen import File as MutagenFile
except ImportError:
    MutagenFile = None

UPLOAD_DIR = Path('uploads/yahya_files')

def get_duration(path: Path) -> float:
    # 1. Try Mutagen
    if MutagenFile:
        try:
            audio = MutagenFile(str(path))
            if audio and hasattr(audio, 'info') and hasattr(audio.info, 'length'):
                return float(audio.info.length)
        except Exception:
            pass
            
    # 2. Try Wave (if wav)
    if path.suffix.lower() == '.wav':
        try:
            with wave.open(str(path), "rb") as wav:
                frames = wav.getnframes()
                rate = wav.getframerate()
                if rate > 0:
                    return frames / float(rate)
        except Exception:
            pass

    # 3. Try ffprobe
    if shutil.which("ffprobe"):
        try:
            cmd = [
                'ffprobe', '-v', 'error',
                '-show_entries', 'format=duration',
                '-of', 'default=noprint_wrappers=1:nokey=1',
                str(path)
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
            if result.returncode == 0 and result.stdout.strip():
                return float(result.stdout.strip())
        except Exception:
            pass
            
    return 0.0

def format_duration(seconds: float) -> str:
    mins, secs = divmod(int(round(seconds)), 60)
    return f"{minutes:02d}:{secs:02d}"

def run():
    setup_page("Yahya - Audio Duration", "⏱️")
    st.markdown("### ⏱️ Sort Audio by Duration (Shortest to Longest)")
    
    if not MutagenFile and not shutil.which("ffprobe"):
        st.warning("⚠️ `mutagen` library or `ffprobe` not found. Duration detection might be limited to WAV files.", icon="⚠️")

    uploaded_files = st.file_uploader("Upload Audio", type=['mp3', 'wav', 'aac', 'flac', 'ogg', 'm4a', 'opus'], accept_multiple_files=True, key="yahya_uploader")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Sort Results", type="primary", use_container_width=True):
            if uploaded_files:
                for f in uploaded_files:
                    save_uploaded_file(f, UPLOAD_DIR)
            st.rerun()

    with col2:
        if st.button("Clear All", type="secondary", use_container_width=True):
            clear_directory(UPLOAD_DIR)
            st.rerun()

    if UPLOAD_DIR.exists():
        files = [p for p in UPLOAD_DIR.iterdir() if p.is_file()]
        
        tracks = []
        with st.spinner("Analyzing audio duration..."):
            for p in files:
                dur = get_duration(p)
                tracks.append((p, dur))
        
        # Sort: Shortest first
        tracks.sort(key=lambda x: x[1])
        
        if tracks:
            # Stats
            if tracks:
                shortest = tracks[0][1]
                longest = tracks[-1][1]
                st.caption(f"Total Tracks: {len(tracks)} | Shortest: {format_duration(shortest)} | Longest: {format_duration(longest)}")

            for idx, (p, dur) in enumerate(tracks, 1):
                dur_str = format_duration(dur) if dur > 0 else "Unknown"
                st.markdown(f"""
                <div style="background: rgba(30, 41, 59, 0.7); padding: 1rem; border-radius: 0.5rem; margin-bottom: 0.5rem; border: 1px solid rgba(255,255,255,0.1);">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="font-weight: 600;">#{idx} {p.name}</span>
                        <span style="background: linear-gradient(135deg, #8b5cf6, #6366f1); color: white; padding: 2px 10px; border-radius: 10px; font-size: 0.8rem;">{dur_str}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                st.audio(str(p))
        else:
            if files:
               st.info("No audio files analyzed.") 
            else:
               st.info("No audio files uploaded.")
