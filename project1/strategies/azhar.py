import streamlit as st
from pathlib import Path
from strategies.utils import setup_page, save_uploaded_file, clear_directory

UPLOAD_DIR = Path('uploads/images')

def run():
    setup_page("Azhar - Images", "🖼️")
    
    st.markdown("### 🖼️ Image Gallery (A-Z)")
    
    uploaded_files = st.file_uploader("Choose Images", type=['jpg', 'jpeg', 'png', 'gif', 'bmp', 'webp'], accept_multiple_files=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Sort & Display", type="primary", use_container_width=True):
            if uploaded_files:
                for f in uploaded_files:
                    save_uploaded_file(f, UPLOAD_DIR)
            st.rerun()
            
    with col2:
        if st.button("Clear Images", type="secondary", use_container_width=True):
            clear_directory(UPLOAD_DIR)
            st.rerun()

    if UPLOAD_DIR.exists():
        files = [p for p in UPLOAD_DIR.iterdir() if p.is_file() and p.suffix.lower() in {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.tiff'}]
        # Sort by Name
        files.sort(key=lambda p: p.name.lower())
        
        if files:
            # Grid Layout
            cols = st.columns(4) # 4 columns for grid
            for idx, f in enumerate(files):
                with cols[idx % 4]:
                    st.image(str(f), use_container_width=True)
                    st.caption(f"{f.name} ({f.stat().st_size / 1024:.1f} KB)")
        else:
            st.info("No images found.")
