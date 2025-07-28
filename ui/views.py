import streamlit as st
from typing import List, Dict, Any, Optional

def render_document_preview(text: str, filename: str):
    """Render document preview with modern styling."""
    st.markdown("""
    <style>
    .document-preview {
        background: rgba(255,255,255,0.02);
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        border: 1px solid rgba(255,255,255,0.1);
        backdrop-filter: blur(10px);
    }
    .preview-header {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        margin-bottom: 1rem;
        padding-bottom: 0.75rem;
        border-bottom: 1px solid rgba(255,255,255,0.1);
    }
    .preview-title {
        color: #e1e5e9;
        font-weight: 600;
        font-size: 1.2rem;
        margin: 0;
    }
    .preview-stats {
        display: flex;
        gap: 1.5rem;
        margin-bottom: 1rem;
        flex-wrap: wrap;
    }
    .stat-badge {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 500;
        border: 1px solid rgba(255,255,255,0.2);
    }
    .text-preview {
        background: rgba(0,0,0,0.2);
        border-radius: 8px;
        padding: 1rem;
        font-family: 'SF Mono', 'Monaco', 'Inconsolata', monospace;
        font-size: 0.9rem;
        line-height: 1.5;
        color: #d1d5db;
        border: 1px solid rgba(255,255,255,0.05);
        max-height: 300px;
        overflow-y: auto;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Calculate stats
    word_count = len(text.split())
    char_count = len(text)
    estimated_reading_time = max(1, word_count // 200)
    
    st.markdown('<div class="document-preview">', unsafe_allow_html=True)
    
    # Header
    st.markdown(f'''
    <div class="preview-header">
        <span style="font-size: 1.5rem;">📄</span>
        <div class="preview-title">{filename}</div>
    </div>
    ''', unsafe_allow_html=True)
    
    # Stats
    st.markdown(f'''
    <div class="preview-stats">
        <div class="stat-badge">📊 {word_count:,} words</div>
        <div class="stat-badge">📝 {char_count:,} characters</div>
        <div class="stat-badge">⏱️ ~{estimated_reading_time} min read</div>
    </div>
    ''', unsafe_allow_html=True)
    
    # Text preview
    preview_text = text[:2000] + "..." if len(text) > 2000 else text
    st.markdown(f'<div class="text-preview">{preview_text}</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_summary_view(summary: str):
    """Render summary with modern styling."""
    st.markdown("""
    <style>
    .summary-container {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid rgba(102, 126, 234, 0.2);
        backdrop-filter: blur(10px);
    }
    .summary-header {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        margin-bottom: 1rem;
        padding-bottom: 0.75rem;
        border-bottom: 1px solid rgba(102, 126, 234, 0.3);
    }
    .summary-title {
        color: #e1e5e9;
        font-weight: 600;
        font-size: 1.3rem;
        margin: 0;
    }
    .summary-content {
        color: #d1d5db;
        font-size: 1rem;
        line-height: 1.7;
        text-align: justify;
    }
    .summary-actions {
        margin-top: 1rem;
        padding-top: 1rem;
        border-top: 1px solid rgba(102, 126, 234, 0.2);
        display: flex;
        gap: 0.5rem;
        flex-wrap: wrap;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="summary-container">', unsafe_allow_html=True)
    
    # Header
    st.markdown('''
    <div class="summary-header">
        <span style="font-size: 1.5rem;">📝</span>
        <div class="summary-title">AI-Generated Summary</div>
    </div>
    ''', unsafe_allow_html=True)
    
    # Content
    st.markdown(f'<div class="summary-content">{summary}</div>', unsafe_allow_html=True)
    
    # Actions
    st.markdown('<div class="summary-actions">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📋 Copy to Clipboard", key="copy_summary", use_container_width=True):
            st.success("Summary copied!")
    with col2:
        if st.button("🔊 Generate Audio", key="summary_audio", use_container_width=True):
            st.rerun()
    with col3:
        if st.button("📤 Export Summary", key="export_summary", use_container_width=True):
            st.success("Summary exported!")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_flashcards_view(flashcards: List[Dict[str, str]]):
    """Render flashcards with interactive design."""
    if not flashcards:
        st.warning("No flashcards generated.")
        return
    
    st.markdown("""
    <style>
    .flashcards-container {
        background: rgba(255,255,255,0.02);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid rgba(255,255,255,0.1);
    }
    .flashcards-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 1.5rem;
        padding-bottom: 0.75rem;
        border-bottom: 1px solid rgba(255,255,255,0.1);
    }
    .flashcards-title {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        color: #e1e5e9;
        font-weight: 600;
        font-size: 1.3rem;
        margin: 0;
    }
    .card-counter {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 500;
    }
    .flashcard {
        background: linear-gradient(135deg, rgba(255,255,255,0.05) 0%, rgba(255,255,255,0.02) 100%);
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        border: 1px solid rgba(255,255,255,0.1);
        transition: all 0.3s ease;
        position: relative;
        backdrop-filter: blur(10px);
    }
    .flashcard:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 20px rgba(102, 126, 234, 0.3);
    }
    .card-type {
        position: absolute;
        top: 1rem;
        right: 1rem;
        background: rgba(102, 126, 234, 0.8);
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 500;
    }
    .card-question {
        color: #e1e5e9;
        font-weight: 600;
        font-size: 1.1rem;
        margin-bottom: 1rem;
        padding-right: 5rem;
    }
    .card-answer {
        color: #d1d5db;
        font-size: 1rem;
        line-height: 1.5;
        background: rgba(0,0,0,0.2);
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #667eea;
    }
    .card-navigation {
        display: flex;
        justify-content: center;
        gap: 1rem;
        margin-top: 1.5rem;
        padding-top: 1rem;
        border-top: 1px solid rgba(255,255,255,0.1);
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Initialize card index in session state
    if 'current_card_index' not in st.session_state:
        st.session_state.current_card_index = 0
    
    st.markdown('<div class="flashcards-container">', unsafe_allow_html=True)
    
    # Header
    st.markdown(f'''
    <div class="flashcards-header">
        <div class="flashcards-title">
            <span style="font-size: 1.5rem;">🃏</span>
            <span>Interactive Flashcards</span>
        </div>
        <div class="card-counter">{len(flashcards)} cards</div>
    </div>
    ''', unsafe_allow_html=True)
    
    # Current card
    current_index = st.session_state.current_card_index % len(flashcards)
    card = flashcards[current_index]
    
    card_type = card.get('type', 'unknown').replace('_', ' ').title()
    
    st.markdown(f'''
    <div class="flashcard">
        <div class="card-type">{card_type}</div>
        <div class="card-question">Q: {card.get('question', 'No question available')}</div>
        <div class="card-answer">A: {card.get('answer', 'No answer available')}</div>
    </div>
    ''', unsafe_allow_html=True)
    
    # Navigation
    st.markdown('<div class="card-navigation">', unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("⏮️ First", key="first_card", use_container_width=True):
            st.session_state.current_card_index = 0
            st.rerun()
    
    with col2:
        if st.button("⬅️ Previous", key="prev_card", use_container_width=True):
            st.session_state.current_card_index = max(0, st.session_state.current_card_index - 1)
            st.rerun()
    
    with col3:
        if st.button("➡️ Next", key="next_card", use_container_width=True):
            st.session_state.current_card_index = min(len(flashcards) - 1, st.session_state.current_card_index + 1)
            st.rerun()
    
    with col4:
        if st.button("⏭️ Last", key="last_card", use_container_width=True):
            st.session_state.current_card_index = len(flashcards) - 1
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Progress indicator
    progress = (current_index + 1) / len(flashcards)
    st.progress(progress)
    st.markdown(f"<div style='text-align: center; color: #9ca3af; font-size: 0.9rem; margin-top: 0.5rem;'>Card {current_index + 1} of {len(flashcards)}</div>", unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_audio_view(audio_bytes: bytes):
    """Render audio player with modern styling."""
    st.markdown("""
    <style>
    .audio-container {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(5, 150, 105, 0.1) 100%);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid rgba(16, 185, 129, 0.2);
        backdrop-filter: blur(10px);
    }
    .audio-header {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        margin-bottom: 1rem;
    }
    .audio-title {
        color: #e1e5e9;
        font-weight: 600;
        font-size: 1.3rem;
        margin: 0;
    }
    .audio-controls {
        margin-top: 1rem;
        display: flex;
        gap: 0.5rem;
        flex-wrap: wrap;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="audio-container">', unsafe_allow_html=True)
    
    # Header
    st.markdown('''
    <div class="audio-header">
        <span style="font-size: 1.5rem;">🔊</span>
        <div class="audio-title">Audio Summary</div>
    </div>
    ''', unsafe_allow_html=True)
    
    # Audio player
    st.audio(audio_bytes, format="audio/mp3")
    
    # Controls
    st.markdown('<div class="audio-controls">', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📥 Download Audio", key="download_audio", use_container_width=True):
            st.download_button(
                label="💾 Save MP3",
                data=audio_bytes,
                file_name="summary_audio.mp3",
                mime="audio/mp3"
            )
    with col2:
        if st.button("🔄 Regenerate", key="regen_audio", use_container_width=True):
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_search_view(results: List[Dict[str, Any]], query: str):
    """Render search results with modern styling."""
    st.markdown("""
    <style>
    .search-container {
        background: rgba(255,255,255,0.02);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid rgba(255,255,255,0.1);
    }
    .search-header {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        margin-bottom: 1.5rem;
        padding-bottom: 0.75rem;
        border-bottom: 1px solid rgba(255,255,255,0.1);
    }
    .search-title {
        color: #e1e5e9;
        font-weight: 600;
        font-size: 1.3rem;
        margin: 0;
    }
    .search-result {
        background: linear-gradient(135deg, rgba(255,255,255,0.05) 0%, rgba(255,255,255,0.02) 100%);
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 0.75rem;
        border-left: 4px solid #667eea;
        transition: all 0.3s ease;
    }
    .search-result:hover {
        transform: translateX(4px);
        background: linear-gradient(135deg, rgba(255,255,255,0.08) 0%, rgba(255,255,255,0.05) 100%);
    }
    .result-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 0.5rem;
    }
    .result-rank {
        background: rgba(102, 126, 234, 0.8);
        color: white;
        padding: 0.25rem 0.5rem;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 600;
    }
    .result-relevance {
        font-size: 0.8rem;
        color: #9ca3af;
        font-weight: 500;
    }
    .result-text {
        color: #d1d5db;
        font-size: 0.95rem;
        line-height: 1.5;
    }
    .result-score {
        font-size: 0.8rem;
        color: #6b7280;
        margin-top: 0.5rem;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="search-container">', unsafe_allow_html=True)
    
    # Header
    st.markdown(f'''
    <div class="search-header">
        <span style="font-size: 1.5rem;">🔍</span>
        <div class="search-title">Search Results for "{query}"</div>
    </div>
    ''', unsafe_allow_html=True)
    
    if not results:
        st.info("No results found. Try adjusting your search query.")
    else:
        for result in results:
            relevance_color = {
                'High': '#10b981',
                'Medium': '#f59e0b', 
                'Low': '#ef4444'
            }.get(result.get('relevance', 'Low'), '#6b7280')
            
            st.markdown(f'''
            <div class="search-result">
                <div class="result-header">
                    <div class="result-rank">#{result.get('rank', 1)}</div>
                    <div class="result-relevance" style="color: {relevance_color}">
                        {result.get('relevance', 'Unknown')} Relevance
                    </div>
                </div>
                <div class="result-text">{result.get('text', 'No content available')[:300]}...</div>
                <div class="result-score">Similarity Score: {result.get('score', 0):.3f}</div>
            </div>
            ''', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
