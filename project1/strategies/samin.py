import streamlit as st
import re

class URLObj:
    def __init__(self, url_string):
        self.url_string = url_string
        self.domain = self._extract_domain()

    def _extract_domain(self):
        raw = re.sub(r'^https?://', '', self.url_string)
        raw = re.sub(r'^www\.', '', raw)
        match = re.match(r'^([^/\s]+)', raw)
        return match.group(1) if match else raw

def run():
    st.set_page_config(page_title="Samin - URL Sorter", page_icon="🔗", layout="wide")
    
    # Custom CSS for Premium Look
    st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle at top right, #1e293b, #0f172a); color: #f1f5f9; }
    .stTextArea textarea { background-color: rgba(30, 41, 59, 0.6); color: white; border: 1px solid rgba(255,255,255,0.1); }
    </style>
    """, unsafe_allow_html=True)
    
    st.title("🔗 Samin - URL Sorter")
    st.markdown("### Organise URLs by Domain or Path")

    if 'samin_urls' not in st.session_state:
        st.session_state.samin_urls = ""

    text_input = st.text_area("Paste URLs (one per line or comma separated)", height=200, key="samin_input")
    
    col1, col2 = st.columns(2)
    sort_mode = col1.selectbox("Sort Mode", [
        "Domain Ascending (A → Z)",
        "Domain Descending (Z → A)",
        "Alphabetical by Full URL"
    ])
    
    if col1.button("Sort URLs", type="primary", use_container_width=True):
        st.session_state.samin_urls = text_input
    
    if st.session_state.samin_urls:
        # Parse logic
        raw_text = st.session_state.samin_urls
        lines = re.split(r'\r?\n|,\s*', raw_text)
        url_objs = []
        for s in lines:
            s = s.strip()
            if not s: continue
            if not re.match(r'(?i)^https?://', s):
                s = "https://" + s
            url_objs.append(URLObj(s))
            
        # Sort logic
        if "Domain Ascending" in sort_mode:
            url_objs.sort(key=lambda u: u.domain.lower())
        elif "Domain Descending" in sort_mode:
            url_objs.sort(key=lambda u: u.domain.lower(), reverse=True)
        else:
            url_objs.sort(key=lambda u: u.url_string.lower())
            
        st.divider()
        st.subheader("Results")
        for u in url_objs:
            st.markdown(f"🔗 [{u.url_string}]({u.url_string}) <span style='color:#94a3b8; font-size:0.8rem;'>({u.domain})</span>", unsafe_allow_html=True)
