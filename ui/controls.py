import streamlit as st
from typing import Dict, Any, List

def render_action_buttons(document_loaded: bool = False) -> Dict[str, bool]:
    """
    Render main action buttons with modern styling.
    
    Args:
        document_loaded (bool): Whether a document is loaded
        
    Returns:
        Dict[str, bool]: Button states
    """
    if not document_loaded:
        return {}
    
    st.markdown("""
    <style>
    .action-buttons-container {
        background: rgba(255,255,255,0.02);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid rgba(255,255,255,0.1);
    }
    .buttons-title {
        color: #e1e5e9;
        font-weight: 600;
        font-size: 1.1rem;
        margin-bottom: 1rem;
        text-align: center;
    }
    .action-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin-bottom: 1rem;
    }
    .action-button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border: none;
        border-radius: 12px;
        padding: 1rem;
        color: white;
        font-weight: 600;
        font-size: 1rem;
        cursor: pointer;
        transition: all 0.3s ease;
        text-align: center;
        text-decoration: none;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.5rem;
        min-height: 60px;
    }
    .action-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 20px rgba(102, 126, 234, 0.4);
    }
    .action-button:active {
        transform: translateY(0);
    }
    .secondary-actions {
        display: flex;
        gap: 0.5rem;
        margin-top: 1rem;
        flex-wrap: wrap;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="action-buttons-container">', unsafe_allow_html=True)
    st.markdown('<div class="buttons-title">🚀 Generate Study Materials</div>', unsafe_allow_html=True)
    
    # Main action buttons
    col1, col2, col3 = st.columns(3)
    
    actions = {}
    
    with col1:
        actions['summary'] = st.button(
            "📝 Generate Summary",
            key="btn_summary",
            use_container_width=True,
            type="primary"
        )
    
    with col2:
        actions['flashcards'] = st.button(
            "🃏 Create Flashcards",
            key="btn_flashcards", 
            use_container_width=True,
            type="primary"
        )
    
    with col3:
        actions['audio'] = st.button(
            "🔊 Generate Audio",
            key="btn_audio",
            use_container_width=True,
            type="primary"
        )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    return actions

def render_flashcard_controls() -> Dict[str, Any]:
    """Render flashcard-specific controls."""
    st.markdown("""
    <style>
    .flashcard-controls {
        background: rgba(255,255,255,0.02);
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        border: 1px solid rgba(255,255,255,0.05);
    }
    .control-title {
        color: #e1e5e9;
        font-weight: 600;
        font-size: 0.9rem;
        margin-bottom: 0.5rem;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="flashcard-controls">', unsafe_allow_html=True)
    st.markdown('<div class="control-title">📚 Flashcard Options</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    controls = {}
    
    with col1:
        controls['shuffle'] = st.button(
            "🔀 Shuffle Cards",
            key="shuffle_cards",
            help="Randomize flashcard order"
        )
    
    with col2:
        controls['reset'] = st.button(
            "🔄 Reset Progress",
            key="reset_cards",
            help="Go back to first card"
        )
    
    with col3:
        controls['practice_mode'] = st.button(
            "🎯 Practice Mode",
            key="practice_mode",
            help="Hide answers initially"
        )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    return controls

def render_search_controls() -> Dict[str, Any]:
    """Render semantic search controls."""
    st.markdown("""
    <style>
    .search-container {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(5, 150, 105, 0.1) 100%);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid rgba(16, 185, 129, 0.2);
        backdrop-filter: blur(10px);
    }
    .search-header {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        margin-bottom: 1rem;
    }
    .search-title {
        color: #e1e5e9;
        font-weight: 600;
        font-size: 1.2rem;
        margin: 0;
    }
    .search-form {
        display: flex;
        gap: 0.75rem;
        align-items: end;
        flex-wrap: wrap;
    }
    .search-input {
        flex: 1;
        min-width: 200px;
    }
    .search-settings {
        display: flex;
        gap: 1rem;
        margin-top: 0.75rem;
        align-items: center;
        flex-wrap: wrap;
    }
    .search-tip {
        color: #9ca3af;
        font-size: 0.85rem;
        font-style: italic;
        margin-top: 0.5rem;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="search-container">', unsafe_allow_html=True)
    
    # Header
    st.markdown('''
    <div class="search-header">
        <span style="font-size: 1.5rem;">🔍</span>
        <div class="search-title">Semantic Search</div>
    </div>
    ''', unsafe_allow_html=True)
    
    # Search form
    col1, col2, col3 = st.columns([3, 1, 1])
    
    controls = {}
    
    with col1:
        controls['query'] = st.text_input(
            "",
            placeholder="Ask a question about your document...",
            key="search_query",
            label_visibility="collapsed"
        )
    
    with col2:
        controls['k'] = st.number_input(
            "Results",
            min_value=1,
            max_value=15,
            value=5,
            key="search_k",
            help="Number of results"
        )
    
    with col3:
        controls['go'] = st.button(
            "🔍 Search",
            key="search_go",
            use_container_width=True,
            type="primary"
        )
    
    # Search tips
    st.markdown('''
    <div class="search-tip">
        💡 Try asking: "What are the key concepts?", "Explain the main topic", or "What are the important points?"
    </div>
    ''', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    return controls

def render_export_controls(available_exports: List[str]) -> Dict[str, Any]:
    """Render export controls."""
    if not available_exports:
        return {}
    
    st.markdown("""
    <style>
    .export-container {
        background: linear-gradient(135deg, rgba(245, 158, 11, 0.1) 0%, rgba(217, 119, 6, 0.1) 100%);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid rgba(245, 158, 11, 0.2);
        backdrop-filter: blur(10px);
    }
    .export-header {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        margin-bottom: 1rem;
    }
    .export-title {
        color: #e1e5e9;
        font-weight: 600;
        font-size: 1.2rem;
        margin: 0;
    }
    .export-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
        gap: 0.75rem;
        margin-bottom: 1rem;
    }
    .export-options {
        display: flex;
        gap: 0.75rem;
        align-items: end;
        flex-wrap: wrap;
    }
    .available-badge {
        background: rgba(16, 185, 129, 0.8);
        color: white;
        padding: 0.25rem 0.5rem;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 500;
        margin-left: 0.5rem;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="export-container">', unsafe_allow_html=True)
    
    # Header
    st.markdown('''
    <div class="export-header">
        <span style="font-size: 1.5rem;">📤</span>
        <div class="export-title">Export Study Materials</div>
    </div>
    ''', unsafe_allow_html=True)
    
    # Available items
    st.markdown("**Available for export:**")
    export_items = []
    if 'summary' in available_exports:
        export_items.append("📝 Summary")
    if 'flashcards' in available_exports:
        export_items.append("🃏 Flashcards")
    
    st.markdown(" • ".join(export_items))
    
    # Export options
    col1, col2, col3 = st.columns([2, 1, 1])
    
    controls = {}
    
    with col1:
        format_options = {
            'markdown': '📄 Markdown (.md)',
            'text': '📝 Plain Text (.txt)',
            'json': '🔧 JSON (.json)',
            'complete': '📚 Study Package (.md)'
        }
        
        controls['format'] = st.selectbox(
            "Format",
            options=list(format_options.keys()),
            format_func=lambda x: format_options[x],
            key="export_format"
        )
    
    with col2:
        controls['include_metadata'] = st.checkbox(
            "Include metadata",
            value=True,
            key="export_metadata",
            help="Include timestamps and file info"
        )
    
    with col3:
        controls['export'] = st.button(
            "📤 Export",
            key="export_go",
            use_container_width=True,
            type="primary"
        )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    return controls

def render_study_mode_controls() -> Dict[str, Any]:
    """Render study mode and practice controls."""
    st.markdown("""
    <style>
    .study-mode-container {
        background: rgba(255,255,255,0.02);
        border-radius: 12px;
        padding: 1rem;
        margin: 1rem 0;
        border: 1px solid rgba(255,255,255,0.1);
    }
    .study-mode-header {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin-bottom: 0.75rem;
    }
    .study-mode-title {
        color: #e1e5e9;
        font-weight: 600;
        font-size: 1rem;
        margin: 0;
    }
    .mode-buttons {
        display: flex;
        gap: 0.5rem;
        flex-wrap: wrap;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="study-mode-container">', unsafe_allow_html=True)
    
    # Header
    st.markdown('''
    <div class="study-mode-header">
        <span style="font-size: 1.2rem;">🎯</span>
        <div class="study-mode-title">Study Modes</div>
    </div>
    ''', unsafe_allow_html=True)
    
    # Mode buttons
    col1, col2, col3, col4 = st.columns(4)
    
    controls = {}
    
    with col1:
        controls['review_mode'] = st.button(
            "📖 Review",
            key="review_mode",
            help="Sequential review of all materials"
        )
    
    with col2:
        controls['quiz_mode'] = st.button(
            "❓ Quiz",
            key="quiz_mode", 
            help="Interactive quiz mode"
        )
    
    with col3:
        controls['speed_drill'] = st.button(
            "⚡ Speed Drill",
            key="speed_drill",
            help="Rapid flashcard practice"
        )
    
    with col4:
        controls['focus_mode'] = st.button(
            "🎯 Focus",
            key="focus_mode",
            help="Distraction-free study"
        )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    return controls
