import streamlit as st
from pathlib import Path
from strategies.utils import setup_page, save_uploaded_file, clear_directory
from PIL import Image

UPLOAD_DIR = Path('uploads/fatima_fruits')

def get_luminance(path):
    try:
        with Image.open(path) as img:
            img = img.convert("RGB")
            pixels = list(img.getdata())
            if not pixels: return 0
            
            r_tot = sum(p[0] for p in pixels)
            g_tot = sum(p[1] for p in pixels)
            b_tot = sum(p[2] for p in pixels)
            count = len(pixels)
            
            r_avg = r_tot / count
            g_avg = g_tot / count
            b_avg = b_tot / count
            
            # Perceived luminance
            return 0.299 * r_avg + 0.587 * g_avg + 0.114 * b_avg
    except Exception:
        return 0.0

def run():
    setup_page("Fatima - Fruit Intensity", "🍎")
    st.markdown("### 🍎 Fruit Sorter (Perceived Luminance)")
    
    uploaded_files = st.file_uploader("Upload Fruit Images", type=['jpg', 'jpeg', 'png', 'webp'], accept_multiple_files=True, key="fatima_uploader")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Analyze Fruits", type="primary", use_container_width=True):
            if uploaded_files:
                for f in uploaded_files:
                    save_uploaded_file(f, UPLOAD_DIR)
            st.rerun()

    with col2:
        if st.button("Reset All", type="secondary", use_container_width=True):
            clear_directory(UPLOAD_DIR)
            st.rerun()

    if UPLOAD_DIR.exists():
        fruits = []
        for p in UPLOAD_DIR.iterdir():
            if p.is_file():
                fruits.append({'path': p, 'lum': get_luminance(p)})
        
        # Sort
        fruits.sort(key=lambda x: x['lum'])
        
        if fruits:
            st.markdown(f"**Sorted {len(fruits)} Fruits**")
            cols = st.columns(4)
            for idx, item in enumerate(fruits):
                p = item['path']
                lum = item['lum']
                with cols[idx % 4]:
                    st.image(str(p), use_container_width=True)
                    st.caption(f"{p.name}")
                    st.progress(min(lum / 255.0, 1.0))
                    st.markdown(f"<div style='text-align:center; font-size:0.8rem;'>Luminance: {lum:.1f}</div>", unsafe_allow_html=True)
        else:
            st.info("No fruit images uploaded.")
