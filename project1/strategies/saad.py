import streamlit as st
from pathlib import Path
from strategies.utils import setup_page, save_uploaded_file, clear_directory

UPLOAD_DIR = Path('uploads/saad_files')

def format_size(size_bytes: int) -> str:
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.2f} KB"
    elif size_bytes < 1024 * 1024 * 1024:
        return f"{size_bytes / (1024 * 1024):.2f} MB"
    else:
        return f"{size_bytes / (1024 * 1024 * 1024):.2f} GB"

def run():
    setup_page("Saad - File Browser", "📂")
    
    st.markdown("### 📂 Advanced File Browser")
    
    uploaded_files = st.file_uploader("Upload Any Files", accept_multiple_files=True, key="saad_uploader")
    
    if st.button("Upload Files", type="primary"):
        if uploaded_files:
            for f in uploaded_files:
                save_uploaded_file(f, UPLOAD_DIR)
            st.rerun()

    if UPLOAD_DIR.exists():
        files = []
        for p in UPLOAD_DIR.iterdir():
            if p.is_file():
                files.append((p.name, p.stat().st_size))
        
        if files:
            # Sorting Controls
            col1, col2, col3 = st.columns([2,2,1])
            sort_by = col1.selectbox("Sort By", ["Name", "Size"])
            order = col2.radio("Order", ["Ascending", "Descending"], horizontal=True)
            
            if col3.button("Clear All", type="secondary"):
                clear_directory(UPLOAD_DIR)
                st.rerun()

            # Apply Sort
            reverse = (order == "Descending")
            if sort_by == "Name":
                files.sort(key=lambda x: x[0].lower(), reverse=reverse)
            else:
                files.sort(key=lambda x: x[1], reverse=reverse)
            
            # Display
            total_size = sum(f[1] for f in files)
            st.caption(f"Total: {len(files)} files | {format_size(total_size)}")
            
            st.markdown("""
            <div style="display: flex; font-weight: bold; padding: 10px; border-bottom: 1px solid #ffffff33;">
                <div style="flex: 3;">File Name</div>
                <div style="flex: 1; text-align: right;">Size</div>
            </div>
            """, unsafe_allow_html=True)
            
            for name, size in files:
                st.markdown(f"""
                <div style="display: flex; padding: 10px; border-bottom: 1px solid #ffffff11; align-items: center;">
                    <div style="flex: 3; display: flex; align-items: center;">
                        <span style="margin-right: 10px; color: #3b82f6;">📄</span> {name}
                    </div>
                    <div style="flex: 1; text-align: right; font-family: monospace; color: #94a3b8;">{format_size(size)}</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No files uploaded.")
