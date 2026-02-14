import streamlit as st
from strategies.utils import setup_page

def run():
    setup_page("Ahmed Shah - People Sorter", "👥")
    st.markdown("### 👥 People Sorter (by Occupation)")
    
    # Initialize session state for people list
    if 'ahmed_people' not in st.session_state:
        st.session_state.ahmed_people = []

    # Input Form
    with st.form("add_person_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Name")
        with col2:
            occupation = st.text_input("Occupation")
        
        submitted = st.form_submit_button("Add Person")
        if submitted and name and occupation:
            st.session_state.ahmed_people.append({'name': name, 'occupation': occupation})
            st.success(f"Added {name} ({occupation})")

    # Display & Sorting
    if st.session_state.ahmed_people:
        # Sort by occupation
        sorted_people = sorted(st.session_state.ahmed_people, key=lambda x: x['occupation'].lower())
        
        st.divider()
        st.markdown(f"**Sorted List ({len(sorted_people)})**")
        
        for p in sorted_people:
            st.markdown(f"""
            <div style="background: rgba(30, 41, 59, 0.7); padding: 1rem; border-radius: 0.5rem; margin-bottom: 0.5rem; border: 1px solid rgba(255,255,255,0.1); border-left: 4px solid #2dd4bf; display: flex; justify-content: space-between; align-items: center;">
                <span style="font-size: 1.1rem; font-weight: 600;">{p['name']}</span>
                <span style="background: rgba(45, 212, 191, 0.15); color: #2dd4bf; padding: 4px 10px; border-radius: 20px; font-size: 0.85rem; font-weight: 600; text-transform: uppercase;">{p['occupation']}</span>
            </div>
            """, unsafe_allow_html=True)
            
        if st.button("Clear List", type="secondary"):
            st.session_state.ahmed_people = []
            st.rerun()
    else:
        st.info("List is empty. Add people above.")
