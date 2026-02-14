import streamlit as st
from pathlib import Path
import shutil
import mimetypes
from strategies.utils import setup_page, save_uploaded_file

ROOT_DIR = Path('uploads')
CATEGORY_CONFIG = {
    'Images': ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.tiff'),
    'Videos': ('.mp4', '.mov', '.avi', '.mkv', '.webm', '.flv', '.wmv'),
    'Audio': ('.mp3', '.wav', '.aac', '.flac', '.ogg'),
    'Archives': ('.zip', '.rar', '.7z', '.tar', '.gz', '.bz2'),
    'Documents': ('.pdf', '.doc', '.docx', '.txt', '.csv')
}

def get_category(filename):
    ext = Path(filename).suffix.lower()
    for cat, exts in CATEGORY_CONFIG.items():
        if ext in exts:
            return cat
    return 'Other'

def run():
    setup_page("Shaheer - Universal Organizer", "📂")
    
    st.markdown("### 📂 Auto-Sort & Organize Files")
    
    uploaded_files = st.file_uploader("Upload Any Files", accept_multiple_files=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Auto-Organize", type="primary", use_container_width=True):
            if uploaded_files:
                for f in uploaded_files:
                    cat = get_category(f.name)
                    target_dir = ROOT_DIR / cat
                    save_uploaded_file(f, target_dir)
                st.success(f"Organized {len(uploaded_files)} files!")
            st.rerun()

    with col2:
        if st.button("Clear All Files", type="secondary", use_container_width=True):
            if ROOT_DIR.exists():
                for item in ROOT_DIR.iterdir():
                     if item.is_dir():
                         shutil.rmtree(item)
                     else:
                         item.unlink()
            st.rerun()

    # Inventory Display
    st.markdown("---")
    st.subheader("📦 File Inventory")
    
    categories = list(CATEGORY_CONFIG.keys()) + ['Other']
    
    cols = st.columns(len(categories))
    
    for idx, cat in enumerate(categories):
        cat_dir = ROOT_DIR / cat
        count = len(list(cat_dir.iterdir())) if cat_dir.exists() else 0
        
        with cols[idx]:
            st.metric(label=cat, value=count)
            if count > 0:
                with st.expander(f"View {cat}"):
                    for f in cat_dir.iterdir():
                        st.text(f"📄 {f.name}")
                        # Optional: Download button?
                        with open(f, "rb") as file:
                            st.download_button(f"⬇️", file, file_name=f.name, key=f"dl_{f.name}")

