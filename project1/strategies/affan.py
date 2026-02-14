import streamlit as st
from pathlib import Path
from strategies.utils import setup_page, save_uploaded_file, clear_directory

UPLOAD_DIR = Path('uploads/affan_files')
PRIORITY = {'.txt': 1, '.docx': 2, '.xlsx': 3, '.pptx': 4}

def shell_sort(arr):
    n = len(arr)
    gap = n // 2
    while gap > 0:
        for i in range(gap, n):
            temp = arr[i]
            j = i
            # Compare priorities (lower number = higher priority)
            while j >= gap and PRIORITY.get(arr[j - gap].suffix.lower(), 99) > PRIORITY.get(temp.suffix.lower(), 99):
                arr[j] = arr[j - gap]
                j -= gap
            arr[j] = temp
        gap //= 2
    return arr

def run():
    setup_page("Affan - Priority Sort", "⚡")
    
    st.markdown("### ⚡ Sort Files by Priority (Shell Sort)")
    st.info("Priority: .txt (1) > .docx (2) > .xlsx (3) > .pptx (4)")
    
    uploaded_files = st.file_uploader("Upload Files", type=['txt', 'docx', 'xlsx', 'pptx'], accept_multiple_files=True, key="affan_uploader")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Sort Files", type="primary", use_container_width=True):
            if uploaded_files:
                for f in uploaded_files:
                    save_uploaded_file(f, UPLOAD_DIR)
            st.rerun()
            
    with col2:
        if st.button("Reset All", type="secondary", use_container_width=True):
            clear_directory(UPLOAD_DIR)
            st.rerun()

    if UPLOAD_DIR.exists():
        files = [p for p in UPLOAD_DIR.iterdir() if p.is_file() and p.suffix.lower() in PRIORITY]
        sorted_files = shell_sort(files)
        
        if sorted_files:
            for f in sorted_files:
                ext = f.suffix.lower()
                color = "#10b981" if ext == '.txt' else "#3b82f6" if ext == '.docx' else "#0ea5e9" if ext == '.xlsx' else "#a855f7"
                icon = "📄" if ext == '.txt' else "📝" if ext == '.docx' else "📊" if ext == '.xlsx' else "📽️"
                
                st.markdown(f"""
                <div style="background: rgba(30, 41, 59, 0.7); padding: 1rem; border-radius: 0.5rem; margin-bottom: 0.5rem; border-left: 5px solid {color};">
                    <div style="display: flex; align-items: center;">
                        <span style="font-size: 1.5rem; margin-right: 1rem;">{icon}</span>
                        <div>
                            <div style="font-weight: 600;">{f.name}</div>
                            <div style="font-size: 0.8rem; color: {color}; text-transform: uppercase; font-weight: bold;">Priority {PRIORITY.get(ext)}</div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No supported files found.")
