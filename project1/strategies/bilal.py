import streamlit as st
from pathlib import Path
from strategies.utils import setup_page, save_uploaded_file, clear_directory
import logging

# Try imports
try:
    from pypdf import PdfReader
except ImportError:
    try:
        from PyPDF2 import PdfFileReader as PdfReader
    except ImportError:
        PdfReader = None

UPLOAD_DIR = Path('uploads/bilal_pdfs')

def get_page_count(path):
    if not PdfReader:
        return 0
    try:
        reader = PdfReader(str(path))
        # PyPDF2 uses getNumPages(), pypdf uses len(reader.pages)
        if hasattr(reader, 'pages'):
             return len(reader.pages)
        elif hasattr(reader, 'getNumPages'):
             return reader.getNumPages()
    except Exception:
        return 0
    return 0

def shell_sort(arr):
    # arr is list of tuples (path, pages)
    n = len(arr)
    gap = n // 2
    while gap > 0:
        for i in range(gap, n):
            temp = arr[i]
            j = i
            while j >= gap and arr[j - gap][1] > temp[1]:
                arr[j] = arr[j - gap]
                j -= gap
            arr[j] = temp
        gap //= 2
    return arr

def run():
    setup_page("Bilal - PDF Pages", "📑")
    
    st.markdown("### 📑 Sort PDFs by Page Count")
    
    if not PdfReader:
        st.error("⚠️ `pypdf` or `PyPDF2` not installed. Cannot count pages.")
        return

    uploaded_files = st.file_uploader("Upload PDFs", type=['pdf'], accept_multiple_files=True, key="bilal_uploader")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Sort PDFs", type="primary", use_container_width=True):
            if uploaded_files:
                for f in uploaded_files:
                    save_uploaded_file(f, UPLOAD_DIR)
            st.rerun()

    with col2:
        if st.button("Reset All", type="secondary", use_container_width=True):
            clear_directory(UPLOAD_DIR)
            st.rerun()

    if UPLOAD_DIR.exists():
        files = [p for p in UPLOAD_DIR.iterdir() if p.is_file() and p.suffix.lower() == '.pdf']
        
        pdf_data = []
        for p in files:
            pdf_data.append((p, get_page_count(p)))
            
        sorted_pdfs = shell_sort(pdf_data)
        
        if sorted_pdfs:
            for p, pages in sorted_pdfs:
                color = "#10b981" if pages <= 20 else "#f59e0b" if pages <= 50 else "#ef4444"
                st.markdown(f"""
                <div style="background: rgba(30, 41, 59, 0.7); padding: 1rem; border-radius: 0.5rem; margin-bottom: 0.5rem; border-left: 5px solid {color};">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="font-weight: 600;">📄 {p.name}</span>
                        <span style="background: {color}; color: white; padding: 2px 10px; border-radius: 10px; font-size: 0.8rem;">{pages} Pages</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No PDFs found.")
