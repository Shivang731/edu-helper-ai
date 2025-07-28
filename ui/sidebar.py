import streamlit as st
from typing import Dict, Any, Tuple, Optional
from core.tts import get_supported_languages

def render_file_upload_sidebar() -> Tuple[Optional[Any], Optional[Dict[str, Any]]]:
    """
    Render the file upload section in the sidebar with modern styling.
    
    Returns:
        Tuple of (uploaded_file, file_stats)
    """
    st.markdown("""
    <style>
    .upload-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 1rem;
        border: 1px solid rgba(255,255,255,0.1);
    }
    .upload-title {
        color: white;
        font-weight: 600;
        font-size: 1.1rem;
        margin-bottom: 0.5rem;
    }
    .file-stats {
        background: rgba(255,255,255,0.1);
        border-radius: 8px;
        padding: 0.75rem;
        margin-top: 0.5rem;
        backdrop-filter: blur(10px);
    }
    .stat-item {
        color: rgba(255,255,255,0.9);
        font-size: 0.85rem;
        margin: 0.2rem 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="upload-section">', unsafe_allow_html=True)
    st.markdown('<div class="upload-title">📂 Upload Document</div>', unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "",
        type=["pdf", "txt"],
        help="Upload your study materials (PDF or TXT files)",
        label_visibility="collapsed"
    )
    
    file_stats = None
    if uploaded_file:
        # Calculate file stats
        file_size = len(uploaded_file.getvalue())
        if file_size < 1024:
            size_str = f"{file_size} bytes"
        elif file_size < 1024 * 1024:
            size_str = f"{file_size / 1024:.1f} KB"
        else:
            size_str = f"{file_size / (1024 * 1024):.1f} MB"
        
        file_stats = {
            'name': uploaded_file.name,
            'size': file_size,
            'size_str': size_str,
            'type': uploaded_file.type
        }
        
        # Display file stats with modern styling
        st.markdown('<div class="file-stats">', unsafe_allow_html=True)
        st.markdown(f'<div class="stat-item">📄 <strong>{uploaded_file.name}</strong></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="stat-item">📊 {size_str}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="stat-item">🔖 {uploaded_file.type}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    return uploaded_file, file_stats

def render_settings_sidebar() -> Dict[str, Any]:
    """
    Render settings section with modern controls.
    
    Returns:
        Dict containing all settings
    """
    st.markdown("""
    <style>
    .settings-section {
        background: rgba(255,255,255,0.02);
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 1rem;
        border: 1px solid rgba(255,255,255,0.1);
    }
    .settings-title {
        color: #e1e5e9;
        font-weight: 600;
        font-size: 1.1rem;
        margin-bottom: 0.75rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    .setting-group {
        margin-bottom: 1rem;
        padding: 0.5rem;
        background: rgba(255,255,255,0.03);
        border-radius: 8px;
    }
    .setting-label {
        color: #b4bcc8;
        font-size: 0.9rem;
        font-weight: 500;
        margin-bottom: 0.3rem;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="settings-section">', unsafe_allow_html=True)
    st.markdown('<div class="settings-title">⚙️ Settings</div>', unsafe_allow_html=True)
    
    settings = {}
    
    # Summary Settings
    st.markdown('<div class="setting-group">', unsafe_allow_html=True)
    st.markdown('<div class="setting-label">📝 Summary</div>', unsafe_allow_html=True)
    summary_length = st.select_slider(
        "",
        options=["short", "medium", "long"],
        value="medium",
        key="summary_length",
        label_visibility="collapsed"
    )
    settings['summary'] = {'length': summary_length}
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Flashcard Settings
    st.markdown('<div class="setting-group">', unsafe_allow_html=True)
    st.markdown('<div class="setting-label">🃏 Flashcards</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        flashcard_count = st.number_input(
            "Count",
            min_value=5,
            max_value=50,
            value=15,
            step=5,
            key="flashcard_count",
            label_visibility="collapsed"
        )
    
    with col2:
        flashcard_difficulty = st.selectbox(
            "Difficulty",
            ["easy", "medium", "hard"],
            index=1,
            key="flashcard_difficulty",
            label_visibility="collapsed"
        )
    
    settings['flashcards'] = {
        'count': flashcard_count,
        'difficulty': flashcard_difficulty
    }
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Audio Settings
    st.markdown('<div class="setting-group">', unsafe_allow_html=True)
    st.markdown('<div class="setting-label">🔊 Audio</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        supported_languages = get_supported_languages()
        audio_language = st.selectbox(
            "Language",
            options=list(supported_languages.keys()),
            format_func=lambda x: supported_languages[x],
            index=0,
            key="audio_language",
            label_visibility="collapsed"
        )
    
    with col2:
        audio_speed = st.selectbox(
            "Speed",
            ["normal", "slow"],
            index=0,
            key="audio_speed",
            label_visibility="collapsed"
        )
    
    settings['audio'] = {
        'language': audio_language,
        'speed': audio_speed
    }
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Search Settings
    st.markdown('<div class="setting-group">', unsafe_allow_html=True)
    st.markdown('<div class="setting-label">🔍 Search</div>', unsafe_allow_html=True)
    search_results = st.slider(
        "",
        min_value=3,
        max_value=15,
        value=5,
        key="search_results",
        label_visibility="collapsed",
        help="Number of search results to display"
    )
    settings['search'] = {'max_results': search_results}
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    return settings

def render_help_sidebar():
    """Render help and tips section."""
    st.markdown("""
    <style>
    .help-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 12px;
        padding: 1rem;
        margin-top: 1rem;
        border: 1px solid rgba(255,255,255,0.1);
    }
    .help-title {
        color: white;
        font-weight: 600;
        font-size: 1.1rem;
        margin-bottom: 0.75rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    .help-content {
        color: rgba(255,255,255,0.9);
        font-size: 0.85rem;
        line-height: 1.4;
    }
    .help-tip {
        background: rgba(255,255,255,0.1);
        border-radius: 6px;
        padding: 0.5rem;
        margin: 0.5rem 0;
        backdrop-filter: blur(10px);
    }
    .tip-icon {
        display: inline-block;
        margin-right: 0.5rem;
    }
    </style>
    """, unsafe_allow_html=True)
    
    with st.expander("💡 Quick Tips", expanded=False):
        st.markdown("""
        **Getting Started:**
        1. Upload a PDF or TXT file
        2. Generate a summary first
        3. Create flashcards for active learning
        4. Use audio for hands-free review
        
        **Best Practices:**
        - Use clear, well-formatted documents
        - Adjust settings based on content complexity
        - Export your materials for offline study
        - Regular review improves retention
        
        **File Support:**
        - PDF files (text-based, not scanned images)
        - Plain text files (.txt)
        - Maximum recommended size: 10MB
        """)
    
    # Quick stats if available
    if 'storage_service' in st.session_state:
        with st.expander("📊 Session Stats", expanded=False):
            stats = st.session_state.storage_service.get_database_stats()
            if stats:
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Documents", stats.get('documents', 0))
                    st.metric("Summaries", stats.get('summaries', 0))
                with col2:
                    st.metric("Flashcards", stats.get('flashcards', 0))
                    st.metric("Sessions", stats.get('sessions', 0))

def render_recent_documents_sidebar():
    """Render recent documents section."""
    if 'storage_service' not in st.session_state:
        return
    
    with st.expander("📚 Recent Documents", expanded=False):
        recent_docs = st.session_state.storage_service.get_recent_documents(limit=5)
        
        if recent_docs:
            for doc in recent_docs:
                st.markdown(f"""
                **{doc['filename']}**
                - Size: {doc.get('file_size', 0) / 1024:.1f} KB
                - Uploaded: {doc['upload_date'][:10]}
                """)
        else:
            st.info("No recent documents found.")
