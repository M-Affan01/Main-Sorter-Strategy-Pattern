import streamlit as st
import importlib
from strategies.utils import setup_page

# Strategy mapping for the hub
STRATEGIES = {
    "Sukaina - Audio (Name)": ("strategies.sukaina", "🎵"),
    "Abdullah - Audio (Size)": ("strategies.abdullah", "📊"),
    "Azhar - Image Gallery": ("strategies.azhar", "🖼️"),
    "Habiba - Video Player": ("strategies.habiba", "🎥"),
    "Shaheer - Universal Organizer": ("strategies.shaheer", "📦"),
    "Midhat - Video Metadata": ("strategies.midhat", "🎞️"),
    "Mujahid - Image Sorter": ("strategies.mujahid", "📐"),
    "Affan - Priority Sort": ("strategies.affan", "⚡"),
    "Bilal - PDF Pages": ("strategies.bilal", "📄"),
    "Zaid - Aspect Ratio": ("strategies.zaid", "🎯"),
    "Ezaz - Audio Filter": ("strategies.ezaz", "🎧"),
    "Huzaifa - Vehicle Sorter": ("strategies.huzaifa", "🚗"),
    "Ammar - Document Date": ("strategies.ammar", "📅"),
    "Samin - URL Sorter": ("strategies.samin", "🔗"),
    "Saad - File Browser": ("strategies.saad", "📂"),
    "Yahya - Audio Duration": ("strategies.yahya", "⏱️"),
    "Fabiha - Image Date": ("strategies.fabiha", "📆"),
    "Maryam - Audio Newest": ("strategies.maryam", "⬇️"),
    "Bilal Imtiaz - Format Sorter": ("strategies.bilal_imtiaz", "🖼️"),
    "Noor - Image Browser": ("strategies.noor", "📷"),
    "Ahmed Shah - People Sorter": ("strategies.ahmed_shah", "👥"),
    "Daniyal - Color Palette": ("strategies.daniyal", "🎨"),
    "Laiba - Image Intensity": ("strategies.laiba", "💡"),
    "Fatima - Fruit Intensity": ("strategies.fatima", "🍎"),
}

def main():
    # Sidebar Navigation Styling
    st.sidebar.markdown("""
    <style>
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%);
        border-right: 1px solid rgba(255,255,255,0.05);
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.sidebar.title("🚀 Strategy Hub")
    selected_name = st.sidebar.selectbox("Select Strategy", ["Main Hub"] + list(STRATEGIES.keys()))
    
    st.sidebar.divider()
    st.sidebar.markdown("### 🛠️ Quick Stats")
    st.sidebar.info(f"Total Strategies: {len(STRATEGIES)}\n\nFramework: Streamlit 1.x")
    
    if selected_name == "Main Hub":
        setup_page("Strategy Pattern Hub", "💎")
        
        st.markdown("""
        <div style="text-align: center; margin-bottom: 4rem;">
            <p style="font-size: 1.4rem; color: #94a3b8; max-width: 800px; margin: 0 auto;">
                An enterprise-grade file management suite leveraging the <b>Strategy Design Pattern</b> 
                to provide modular, high-performance sorting algorithms.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Display Grid of Cards
        cols = st.columns(3)
        for idx, (name, (module, icon)) in enumerate(STRATEGIES.items()):
            with cols[idx % 3]:
                st.markdown(f"""
                <div class="glass-card">
                    <div style="font-size: 3.5rem; margin-bottom: 1rem; filter: drop-shadow(0 0 10px rgba(96, 165, 250, 0.3));">{icon}</div>
                    <div style="font-weight: 800; font-size: 1.3rem; color: #f1f5f9; margin-bottom: 0.5rem; font-family: 'Outfit';">{name}</div>
                    <div style="color: #94a3b8; font-size: 0.95rem; line-height: 1.6;">Modular algorithm for advanced file organization and processing.</div>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"Launch {icon}", key=f"btn_{idx}", use_container_width=True):
                    # We can't really "change" the selectbox from here easily in Streamlit 
                    # without session state, so we'll just advise using the sidebar.
                    st.toast(f"Please select '{name}' from the sidebar menu.", icon="👈")
    else:
        module_name, icon = STRATEGIES[selected_name]
        try:
            module = importlib.import_module(module_name)
            if hasattr(module, "run"):
                module.run()
            else:
                st.error(f"Module {module_name} does not have a run() function.")
        except Exception as e:
            st.error(f"Error loading {selected_name}: {e}")

if __name__ == "__main__":
    main()
