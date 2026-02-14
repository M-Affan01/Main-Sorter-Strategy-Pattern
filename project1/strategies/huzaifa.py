import streamlit as st
from pathlib import Path
from strategies.utils import setup_page, save_uploaded_file, clear_directory
import shutil

UPLOAD_DIR = Path('uploads/huzaifa_vehicles')

SEARCH_MAP = {
    'SUV': ['suv', 'jeep', 'pajero', 'fortuner', 'prado', 'land rover', '4x4', 'vigo', 'revo', 'v8', 'cruiser', 'land cruiser', 'parado', 'surf', 'brv', 'sportage', 'tucson', 'rocco', 'titan'],
    'Bike': ['bike', 'motorcycle', 'cycle', 'scooter', 'yamaha', 'honda', 'suzuki', 'heavy bike', 'cd70', 'cg125', 'kawasaki', 'vespa', '70cc', '125cc', '150cc'],
    'Truck': ['truck', 'lorry', 'pickup', 'isuzu', 'hilux', 'daewoo', 'mazda', 'shehzore', 'dumper', 'trailer'],
    'Sedan': ['sedan', 'car', 'toyota', 'corolla', 'civic', 'bmw', 'audi', 'mercedes', 'honda city', 'vitz', 'alto', 'mehran', 'cultus', 'swift', 'passo', 'aqua', 'prius', 'wagonr']
}

def sort_vehicles(base_dir: Path):
    categories = list(SEARCH_MAP.keys()) + ['Miscellaneous']
    for cat in categories:
        (base_dir / cat).mkdir(exist_ok=True)

    for file_path in base_dir.iterdir():
        if file_path.is_file() and file_path.suffix.lower() in {'.jpg', '.jpeg', '.png', '.gif', '.webp'}:
            name_lower = file_path.name.lower()
            moved = False
            for cat, keywords in SEARCH_MAP.items():
                if any(kw in name_lower for kw in keywords):
                    shutil.move(str(file_path), str(base_dir / cat / file_path.name))
                    moved = True
                    break
            
            if not moved:
                shutil.move(str(file_path), str(base_dir / 'Miscellaneous' / file_path.name))

def run():
    setup_page("Huzaifa - Vehicle Sorter", "🚗")
    
    st.markdown("### 🚗 Sort Vehicles by Type (Keyword Based)")
    st.caption("Classifies images into SUV, Bike, Truck, Sedan based on filename keywords.")
    
    uploaded_files = st.file_uploader("Upload Vehicle Images", type=['jpg', 'png', 'jpeg', 'webp'], accept_multiple_files=True, key="huzaifa_uploader")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Sort Vehicles", type="primary", use_container_width=True):
            if uploaded_files:
                for f in uploaded_files:
                    save_uploaded_file(f, UPLOAD_DIR)
                sort_vehicles(UPLOAD_DIR)
            st.rerun()

    with col2:
        if st.button("Reset All", type="secondary", use_container_width=True):
            clear_directory(UPLOAD_DIR)
            st.rerun()

    if UPLOAD_DIR.exists():
        categories = list(SEARCH_MAP.keys()) + ['Miscellaneous']
        found_any = False
        
        for cat in categories:
            cat_dir = UPLOAD_DIR / cat
            if cat_dir.exists():
                files = list(cat_dir.glob('*'))
                if files:
                    found_any = True
                    with st.expander(f"📂 {cat} ({len(files)} files)", expanded=True):
                        cols = st.columns(4)
                        for idx, f in enumerate(files):
                            with cols[idx % 4]:
                                st.image(str(f), use_container_width=True)
                                st.caption(f.name)
        
        if not found_any and not any(p.is_file() for p in UPLOAD_DIR.iterdir()):
             st.info("No images uploaded.")
