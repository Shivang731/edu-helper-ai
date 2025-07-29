# app/main.py
"""
Study Aid Generator - Main Streamlit Application
A comprehensive tool for PDF```ocessing, summarization, quiz generation,```d more.
"""

import streamlit as```
import sys
import os
from path``` import Path

# Add project root to path```oject_root = Path(__file__).parent.parent
sys.path.appen```tr(project_root))

# Core imports
from core import```from ui.sidebar import render```debar
from ui.controls import render_controls
from ui.```ws import render_main_content```om ui.styles import loa```ustom_css
from services.storage```port initialize_database, get_user```ssion

def main():
    """Main application entry point."""
    try:
        # Page configuration
        st.set_page_```fig(
            page_title="```dy Aid Generator",
            page_icon="📚",
            layout```ide",
            initial_sidebar_state="expanded"```      )
        
        # Loa```ustom styles
        load_custom_css()
        
        # Initialize database```      initialize_database()
        
        # Initialize session state```      if 'user_i```not in st.session_state:
            st.session_state```er_id = "default_```r"
        if 'uploaded_content```ot in st.session_state:
            st.session_state```loaded_content = ""
        if 'current```mmary' not in st.session_state```           st.session_state```rrent_summary = ""
        if 'flash```ds' not in st.session_state:
            st.session```ate.flashcards = []
        if 'semantic```dex' not in st.session_state```           st.session_state.semantic_index = None```      
        # Render UI```mponents
        with st.sidebar:
            render_```ebar()
        
        # Main content area
        render```in_content()
        
    except Exception as e:
        st.error(f"Application```ror: {str(e)}")
        st.info```lease refresh the page or contact support if the issue persists.")

if __name__ == "__main__":
    main()
