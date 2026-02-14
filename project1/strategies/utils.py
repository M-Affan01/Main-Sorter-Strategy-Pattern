import streamlit as st
import base64
from pathlib import Path
import shutil

def setup_page(title: str, icon: str):
    """Configures the Streamlit page with a premium design system."""
    st.set_page_config(page_title=f"{title} - Strategy Hub", page_icon=icon, layout="wide")
    
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&family=Inter:wght@300;400;600;800&display=swap');
    
    .stApp {
        background: radial-gradient(circle at top right, #1e293b, #0f172a);
        color: #f1f5f9;
        font-family: 'Outfit', 'Inter', sans-serif;
    }
    .premium-header {
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.2) 0%, rgba(37, 99, 235, 0.1) 100%);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        padding: 3rem 2rem;
        border-radius: 24px;
        text-align: center;
        margin-bottom: 3rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4);
        animation: fadeInDown 0.8s ease-out;
    }
    @keyframes fadeInDown {
        from { opacity: 0; transform: translateY(-20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .premium-header h1 {
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(to right, #60a5fa, #a855f7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
        letter-spacing: -1px;
    }
    .premium-header p {
        color: #94a3b8;
        font-size: 1.2rem;
        margin-top: 1rem;
    }
    .glass-card {
        background: rgba(30, 41, 59, 0.4);
        backdrop-filter: blur(8px);
        -webkit-backdrop-filter: blur(8px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 20px;
        padding: 2rem;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        height: 100%;
        display: flex;
        flex-direction: column;
        animation: fadeInUp 0.6s ease-out;
    }
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .glass-card:hover {
        transform: translateY(-8px) scale(1.02);
        border-color: rgba(96, 165, 250, 0.4);
        background: rgba(30, 41, 59, 0.6);
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
    }
    .stTextInput > div > div > input {
        background: rgba(15, 23, 42, 0.6) !important;
        border-radius: 12px !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        color: white !important;
    }
    .stButton > button {
        border-radius: 12px !important;
        padding: 0.5rem 2rem !important;
        font-weight: 600 !important;
        transition: all 0.3s !important;
    }
    .stAlert {
        border-radius: 16px !important;
        border: none !important;
        backdrop-filter: blur(4px);
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="premium-header">
        <h1>{icon} {title}</h1>
        <p>Premium Strategy Implementation • High-Performance Framework</p>
    </div>
    """, unsafe_allow_html=True)

def save_uploaded_file(uploaded_file, target_dir: Path) -> Path:
    """Saves an uploaded file to the specified directory."""
    target_dir.mkdir(parents=True, exist_ok=True)
    file_path = target_dir / uploaded_file.name
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path

def clear_directory(target_dir: Path):
    """Safely clears a directory."""
    if target_dir.exists():
        shutil.rmtree(target_dir)
        target_dir.mkdir(parents=True, exist_ok=True)

def display_file_grid(files, title_func=lambda x: x.name):
    """Helper to display files in a grid (placeholder)."""
    # This is a generic helper; specific strategies might implement their own.
    pass
