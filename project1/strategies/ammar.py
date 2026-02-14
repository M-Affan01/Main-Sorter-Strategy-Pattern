import streamlit as st
from pathlib import Path
from strategies.utils import setup_page, save_uploaded_file, clear_directory
import datetime
import time

UPLOAD_DIR = Path('uploads/ammar_docs')

class Document:
    def __init__(self, path: Path, timestamp: float):
        self.path = path
        self.timestamp = timestamp
        dt = datetime.datetime.fromtimestamp(timestamp)
        # Format: DD/MM/YYYY H:MM am/pm
        formatted = dt.strftime('%d/%m/%Y %I:%M %p').lower()
        parts = formatted.split(' ')
        if parts[1].startswith('0'):
            parts[1] = parts[1][1:]
        self.creation_date = " ".join(parts)

def run():
    setup_page("Ammar - Document Date", "📅")
    
    st.markdown("### 📅 Sort Documents by Date")
    
    uploaded_files = st.file_uploader("Upload Documents", accept_multiple_files=True, key="ammar_uploader")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Sort by Date", type="primary", use_container_width=True):
            if uploaded_files:
                for f in uploaded_files:
                    path = save_uploaded_file(f, UPLOAD_DIR)
                    # Attempt to preserve modification time if possible is tricky via browser
                    # We'll just rely on system mtime of the saved file for now, 
                    # as true client-side mtime isn't easily accessible in standard Streamlit file_uploader without custom components.
                    # The original Flask app tried to parse complex JSON from client-side JS which we can't easily replicate here 1:1 without component.
                    # We will use the time.time() or the saved file's mtime (which is now).
                    # NOTE: For a real app, we'd need a custom component to get client-side mtime. 
                    pass
            st.rerun()

    with col2:
        if st.button("Reset All", type="secondary", use_container_width=True):
            clear_directory(UPLOAD_DIR)
            st.rerun()

    if UPLOAD_DIR.exists():
        files = [p for p in UPLOAD_DIR.iterdir() if p.is_file()]
        
        docs = []
        for p in files:
            mtime = p.stat().st_mtime
            docs.append(Document(p, mtime))
        
        # Sort Oldest to Newest
        docs.sort(key=lambda x: x.timestamp)
        
        if docs:
            # Table Header
            col_h1, col_h2 = st.columns([3, 2])
            col_h1.markdown("**Document Name**")
            col_h2.markdown("**Date Modified**")
            st.divider()
            
            for doc in docs:
                c1, c2 = st.columns([3, 2])
                c1.markdown(f"📄 {doc.path.name}")
                c2.markdown(f"📅 {doc.creation_date}")
                st.markdown("""<hr style="margin: 0.5rem 0; opacity: 0.1;">""", unsafe_allow_html=True)
        else:
            st.info("No documents found.")
