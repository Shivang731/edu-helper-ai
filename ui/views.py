import streamlit as st

def render_about_contact():
    st.markdown('''<a name="about"></a>''', unsafe_allow_html=True)
    st.markdown("## About")
    st.markdown(
        """
        **Smart Study-Aid Generator** saves you hours of manual note-taking by:
        - Auto-summarizing lengthy PDFs/TXT  
        - Generating interactive flashcards  
        - Creating audio notes for on-the-go learning  
        - Providing instant semantic search  
        """)
    st.markdown('''<a name="contact"></a>''', unsafe_allow_html=True)
    st.markdown("## Connect")
    st.markdown(
        """
        • Email: [shivangdubey731@gmail.com](mailto:shivangdubey731@gmail.com)  
        • Instagram: [@shivang.skd](https://instagram.com/shivang.skd)  
        • GitHub: [shivang731](https://github.com/shivang731)  
        """)
    st.markdown("---")
