import streamlit as st
from pathlib import Path
from strategies.utils import setup_page, save_uploaded_file
from PIL import Image
import colorsys
import collections

UPLOAD_DIR = Path('uploads/daniyal_colors')

def extract_colors(image_path, max_colors=40):
    try:
        with Image.open(image_path) as img:
            img = img.convert('RGB')
            img.thumbnail((400, 400))
            pixels = list(img.getdata())
            
            # Quantize
            quantized = []
            quantization = 16
            for r, g, b in pixels:
                qr = (r // quantization) * quantization
                qg = (g // quantization) * quantization
                qb = (b // quantization) * quantization
                quantized.append((qr, qg, qb))
            
            counter = collections.Counter(quantized)
            total = len(quantized)
            min_freq = max(1, total // 10000)
            
            colors = []
            for rgb, count in counter.most_common(max_colors):
                if count >= min_freq:
                    colors.append({'rgb': rgb, 'count': count})
            return colors
    except Exception:
        return []

def rgb_to_hex(rgb):
    return '#{:02x}{:02x}{:02x}'.format(*rgb)

def rgb_to_hsl(rgb):
    r, g, b = [x/255.0 for x in rgb]
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    return h * 360, s * 100, l * 100

def get_brightness(rgb):
    return (0.299 * rgb[0] + 0.587 * rgb[1] + 0.114 * rgb[2]) / 255.0 * 100

def run():
    setup_page("Daniyal - Color Palette", "🎨")
    st.markdown("### 🎨 Parametric Color Extraction")
    
    uploaded_file = st.file_uploader("Upload Image", type=['jpg', 'jpeg', 'png', 'webp'], key="daniyal_uploader")
    
    if uploaded_file:
        col1, col2 = st.columns([1, 2])
        with col1:
            st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)
            
        # Analysis
        with col2:
            sort_mode = st.selectbox("Sort Palette By", ["Hue", "Brightness", "Saturation", "Frequency"])
            
            with st.spinner("Extracting colors..."):
                path = save_uploaded_file(uploaded_file, UPLOAD_DIR)
                raw_colors = extract_colors(path)
                
                # Sort
                if sort_mode == "Hue":
                    raw_colors.sort(key=lambda x: (rgb_to_hsl(x['rgb'])[0], -rgb_to_hsl(x['rgb'])[1]))
                elif sort_mode == "Brightness":
                    raw_colors.sort(key=lambda x: get_brightness(x['rgb']), reverse=True)
                elif sort_mode == "Saturation":
                    raw_colors.sort(key=lambda x: rgb_to_hsl(x['rgb'])[1], reverse=True)
                elif sort_mode == "Frequency":
                    raw_colors.sort(key=lambda x: x['count'], reverse=True)
                
                st.markdown(f"**Extracted {len(raw_colors)} Colors**")
                
                # Display Palette
                cols = st.columns(5)
                for idx, c in enumerate(raw_colors):
                    rgb = c['rgb']
                    hex_code = rgb_to_hex(rgb)
                    with cols[idx % 5]:
                        st.markdown(f"""
                        <div style="background-color: {hex_code}; height: 60px; border-radius: 8px; margin-bottom: 5px; box-shadow: 0 2px 5px rgba(0,0,0,0.2);"></div>
                        <div style="text-align: center; font-size: 0.7rem; font-family: monospace;">{hex_code}</div>
                        """, unsafe_allow_html=True)
