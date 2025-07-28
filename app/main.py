import streamlit as st
import sys
from pathlib import Path

# Add the project root to Python path for imports
sys.path.append(str(Path(__file__).parent.parent))

from core.fetcher import extract_text_from_pdf, extract_text_from_txt
from core.summarizer import generate_summary
from core.quizgen import generate_flashcards
from core.tts import text_to_speech
from core.parser import StudyMaterialParser
from services.embeddings import SemanticSearchService
from services.storage import StorageService
from services.exporter import ExporterService

# Configure the Streamlit page
st.set_page_config(
    page_title="Edu Helper - Transform Your Notes",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for the modern UI
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .main > div {
        padding-top: 0rem;
    }
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .hero-section {
        text-align: center;
        padding: 80px 20px 60px 20px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        margin: -1rem -1rem 0 -1rem;
    }
    
    .hero-title {
        font-size: 3.5rem;
        font-weight: 700;
        margin-bottom: 1rem;
        line-height: 1.2;
    }
    
    .hero-subtitle {
        font-size: 1.25rem;
        opacity: 0.9;
        margin-bottom: 2rem;
        max-width: 600px;
        margin-left: auto;
        margin-right: auto;
    }
    
    .section {
        padding: 60px 20px;
        max-width: 1200px;
        margin: 0 auto;
    }
    
    .section-title {
        font-size: 2.5rem;
        font-weight: 600;
        text-align: center;
        margin-bottom: 1rem;
        color: #1a202c;
    }
    
    .section-subtitle {
        font-size: 1.1rem;
        text-align: center;
        color: #718096;
        margin-bottom: 3rem;
        max-width: 600px;
        margin-left: auto;
        margin-right: auto;
    }
    
    .feature-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 2rem;
        margin-bottom: 3rem;
    }
    
    .feature-card {
        background: white;
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.07);
        border: 1px solid #e2e8f0;
        transition: transform 0.2s, box-shadow 0.2s;
    }
    
    .feature-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
    }
    
    .feature-icon {
        font-size: 2.5rem;
        margin-bottom: 1rem;
    }
    
    .feature-title {
        font-size: 1.25rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
        color: #2d3748;
    }
    
    .feature-description {
        color: #718096;
        line-height: 1.6;
    }
    
    .demo-section {
        background: #f7fafc;
        padding: 60px 20px;
        margin: 0 -1rem;
    }
    
    .demo-card {
        background: white;
        border-radius: 12px;
        padding: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.07);
        max-width: 800px;
        margin: 0 auto;
    }
    
    .demo-title {
        font-size: 1.5rem;
        font-weight: 600;
        color: #2d3748;
        margin-bottom: 1rem;
    }
    
    .testimonial-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 2rem;
    }
    
    .testimonial-card {
        background: white;
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.07);
        border-left: 4px solid #667eea;
    }
    
    .testimonial-text {
        font-style: italic;
        margin-bottom: 1rem;
        color: #4a5568;
        line-height: 1.6;
    }
    
    .testimonial-author {
        font-weight: 600;
        color: #2d3748;
    }
    
    .testimonial-role {
        color: #718096;
        font-size: 0.9rem;
    }
    
    .about-section {
        background: #2d3748;
        color: white;
        padding: 60px 20px;
        margin: 0 -1rem;
    }
    
    .about-card {
        max-width: 600px;
        margin: 0 auto;
        text-align: center;
    }
    
    .about-title {
        font-size: 2rem;
        font-weight: 600;
        margin-bottom: 1rem;
    }
    
    .about-name {
        font-size: 1.5rem;
        font-weight: 600;
        color: #667eea;
        margin-bottom: 0.5rem;
    }
    
    .about-description {
        opacity: 0.9;
        line-height: 1.6;
        margin-bottom: 2rem;
    }
    
    .social-links {
        display: flex;
        justify-content: center;
        gap: 1rem;
        flex-wrap: wrap;
    }
    
    .social-link {
        background: #667eea;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        text-decoration: none;
        font-weight: 500;
        transition: background 0.2s;
    }
    
    .social-link:hover {
        background: #5a67d8;
        color: white;
        text-decoration: none;
    }
    
    .cta-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 80px 20px;
        text-align: center;
        margin: 0 -1rem;
    }
    
    .cta-title {
        font-size: 2.5rem;
        font-weight: 600;
        margin-bottom: 1rem;
    }
    
    .cta-subtitle {
        font-size: 1.1rem;
        opacity: 0.9;
        margin-bottom: 2rem;
    }
    
    .upload-area {
        background: rgba(255, 255, 255, 0.1);
        border: 2px dashed rgba(255, 255, 255, 0.3);
        border-radius: 12px;
        padding: 3rem 2rem;
        margin: 2rem auto;
        max-width: 500px;
        transition: all 0.3s;
    }
    
    .upload-area:hover {
        background: rgba(255, 255, 255, 0.15);
        border-color: rgba(255, 255, 255, 0.5);
    }
    
    .action-button {
        background: #667eea;
        color: white;
        border: none;
        padding: 12px 24px;
        border-radius: 8px;
        font-weight: 600;
        cursor: pointer;
        transition: background 0.2s;
        margin: 0.5rem;
    }
    
    .action-button:hover {
        background: #5a67d8;
    }
    
    .stButton > button {
        width: 100%;
        background: #667eea;
        color: white;
        border: none;
        padding: 12px 24px;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.2s;
    }
    
    .stButton > button:hover {
        background: #5a67d8;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
    }
    
    .result-card {
        background: white;
        border-radius: 12px;
        padding: 2rem;
        margin: 2rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.07);
        border-left: 4px solid #667eea;
    }
    
    .result-title {
        font-size: 1.25rem;
        font-weight: 600;
        color: #2d3748;
        margin-bottom: 1rem;
    }
    
    @media (max-width: 768px) {
        .hero-title {
            font-size: 2.5rem;
        }
        
        .section-title {
            font-size: 2rem;
        }
        
        .cta-title {
            font-size: 2rem;
        }
    }
</style>
""", unsafe_allow_html=True)

def render_hero_section():
    st.markdown("""
    <div class="hero-section">
        <h1 class="hero-title">Transform Your Notes.<br>Accelerate Your Learning.</h1>
        <p class="hero-subtitle">Summarize textbooks, generate flashcards, and listen to notes instantly with Edu Helper.</p>
    </div>
    """, unsafe_allow_html=True)

def render_features_section():
    st.markdown("""
    <div class="section">
        <h2 class="section-title">Why Use Edu Helper?</h2>
        <p class="section-subtitle">Your AI-powered study assistant that transforms how you learn and retain information.</p>
        
        <div class="feature-grid">
            <div class="feature-card">
                <div class="feature-icon">📝</div>
                <h3 class="feature-title">Instant AI Summaries</h3>
                <p class="feature-description">Save hours with intelligent summaries of your textbooks and lecture notes.</p>
            </div>
            
            <div class="feature-card">
                <div class="feature-icon">🃏</div>
                <h3 class="feature-title">Automatic Flashcards</h3>
                <p class="feature-description">Turn text into interactive flashcards for effective spaced repetition learning.</p>
            </div>
            
            <div class="feature-card">
                <div class="feature-icon">🔊</div>
                <h3 class="feature-title">Audio Notes</h3>
                <p class="feature-description">Listen to your notes anytime, anywhere. Perfect for learning on the go.</p>
            </div>
            
            <div class="feature-card">
                <div class="feature-icon">🔍</div>
                <h3 class="feature-title">Semantic Search</h3>
                <p class="feature-description">Ask questions in natural language and get answers from your own materials.</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_demo_section():
    st.markdown("""
    <div class="demo-section">
        <div class="section">
            <h2 class="section-title">See It In Action</h2>
            <p class="section-subtitle">Here's how Edu Helper transforms your study materials</p>
            
            <div class="demo-card">
                <h3 class="demo-title">Machine Learning Fundamentals</h3>
                <p><strong>Key Concepts:</strong> Machine learning is a subset of AI focused on developing algorithms that learn from data. It includes supervised learning (labeled data), unsupervised learning (unlabeled data), and reinforcement learning (reward-based).</p>
                
                <p><strong>Applications:</strong> Used in recommendation systems, image recognition, natural language processing, and predictive analytics.</p>
                
                <p><strong>Important Algorithms:</strong> Linear regression, decision trees, neural networks, and k-means clustering.</p>
                
                <p><strong>Challenges:</strong> Overfitting, underfitting, bias in data, and computational complexity.</p>
                
                <p style="font-style: italic; color: #718096; margin-top: 1rem;">Generated from: "Introduction to Machine Learning.pdf" (32 pages)</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_testimonials_section():
    st.markdown("""
    <div class="section">
        <h2 class="section-title">What Students Say</h2>
        <p class="section-subtitle">Hear from students who transformed their study habits with Edu Helper</p>
        
        <div class="testimonial-grid">
            <div class="testimonial-card">
                <p class="testimonial-text">"This saved me before midterms! I uploaded my psychology textbook and got perfect summaries and flashcards. The audio feature let me review while walking to class."</p>
                <p class="testimonial-author">Aisha K.</p>
                <p class="testimonial-role">Psychology Major</p>
            </div>
            
            <div class="testimonial-card">
                <p class="testimonial-text">"The Q&A feature is incredible. I uploaded my data structures notes and could literally ask questions about complex algorithms. It's like having a tutor available 24/7."</p>
                <p class="testimonial-author">Raj P.</p>
                <p class="testimonial-role">Computer Science</p>
            </div>
            
            <div class="testimonial-card">
                <p class="testimonial-text">"I used to spend hours making flashcards by hand. Now I just upload my lecture notes and get them instantly. My grades have improved and I have so much more free time!"</p>
                <p class="testimonial-author">Maya L.</p>
                <p class="testimonial-role">Biology Major</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_about_section():
    st.markdown("""
    <div class="about-section">
        <div class="section">
            <div class="about-card">
                <h2 class="about-title">About the Creator</h2>
                <h3 class="about-name">Shivang Kumar Dubey</h3>
                <p class="about-description">First-year Scaler School of Technology student. Passionate about AI/ML and helping students succeed. Created Edu Helper to solve real problems faced by students in managing and absorbing large amounts of study material.</p>
                
                <div class="social-links">
                    <a href="mailto:shivangdubey731@gmail.com" class="social-link">📧 Email</a>
                    <a href="https://instagram.com/shivang.skd" target="_blank" class="social-link">📷 Instagram</a>
                    <a href="https://github.com/shivang731" target="_blank" class="social-link">💻 GitHub</a>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_cta_and_upload_section():
    st.markdown("""
    <div class="cta-section">
        <h2 class="cta-title">Ready to Transform Your Study Habits?</h2>
        <p class="cta-subtitle">Upload your first document and see the magic happen in seconds. No credit card required.</p>
    </div>
    """, unsafe_allow_html=True)

def main():
    # Initialize services
    if 'parser' not in st.session_state:
        st.session_state.parser = StudyMaterialParser()
    if 'search_service' not in st.session_state:
        st.session_state.search_service = SemanticSearchService()
    if 'storage_service' not in st.session_state:
        st.session_state.storage_service = StorageService()
    if 'exporter_service' not in st.session_state:
        st.session_state.exporter_service = ExporterService()

    # Render landing page sections
    render_hero_section()
    render_features_section()
    render_demo_section()
    render_testimonials_section()
    render_about_section()
    render_cta_and_upload_section()
    
    # Main functionality section
    st.markdown('<div class="section">', unsafe_allow_html=True)
    
    # File upload
    uploaded_file = st.file_uploader(
        "Choose a PDF or TXT file",
        type=["pdf", "txt"],
        help="Upload your study materials to get started",
        label_visibility="collapsed"
    )
    
    if uploaded_file:
        st.success(f"📄 **{uploaded_file.name}** uploaded successfully!")
        
        # Extract text from the uploaded file
        try:
            if uploaded_file.type == "application/pdf":
                document_text = extract_text_from_pdf(uploaded_file)
            elif uploaded_file.type == "text/plain":
                document_text = extract_text_from_txt(uploaded_file)
            else:
                st.error("Unsupported file type")
                return
            
            if document_text and not document_text.startswith("Error"):
                # Clean the text using the parser
                cleaned_text = st.session_state.parser.clean_extracted_text(document_text)
                
                # Setup search service
                st.session_state.search_service.setup_index(cleaned_text)
                
                # Action buttons
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    if st.button("📝 Generate Summary", use_container_width=True):
                        with st.spinner("Generating summary..."):
                            summary = generate_summary(cleaned_text)
                            st.session_state.summary = summary
                            st.session_state.storage_service.save_summary(uploaded_file.name, summary)
                        
                        st.markdown(f"""
                        <div class="result-card">
                            <h3 class="result-title">📝 AI Summary</h3>
                            <p>{summary}</p>
                        </div>
                        """, unsafe_allow_html=True)
                
                with col2:
                    if st.button("🃏 Create Flashcards", use_container_width=True):
                        with st.spinner("Generating flashcards..."):
                            flashcards = generate_flashcards(cleaned_text, 5)
                            st.session_state.flashcards = flashcards
                        
                        st.markdown('<div class="result-card"><h3 class="result-title">🃏 Flashcards</h3>', unsafe_allow_html=True)
                        for i, card in enumerate(flashcards):
                            with st.expander(f"Card {i+1}: {card['front'][:50]}..."):
                                st.write(f"**Question:** {card['front']}")
                                st.write(f"**Answer:** {card['back']}")
                        st.markdown('</div>', unsafe_allow_html=True)
                
                with col3:
                    if st.button("🔊 Generate Audio", use_container_width=True):
                        if hasattr(st.session_state, 'summary') and st.session_state.summary:
                            with st.spinner("Generating audio..."):
                                audio_bytes = text_to_speech(st.session_state.summary)
                                st.session_state.audio_bytes = audio_bytes
                            
                            st.markdown(f"""
                            <div class="result-card">
                                <h3 class="result-title">🔊 Audio Notes</h3>
                                <p>Listen to your summary:</p>
                            </div>
                            """, unsafe_allow_html=True)
                            st.audio(audio_bytes)
                        else:
                            st.warning("Generate a summary first before creating audio.")
                
                # Search functionality
                st.markdown("### 🔍 Search Your Document")
                search_query = st.text_input("Ask a question about your document:")
                
                if search_query and st.button("Search"):
                    results = st.session_state.search_service.search(search_query, top_k=3)
                    
                    st.markdown(f"""
                    <div class="result-card">
                        <h3 class="result-title">🔍 Search Results for: "{search_query}"</h3>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    for i, result in enumerate(results):
                        st.markdown(f"**Result {i+1}:** {result}")
                
            else:
                st.error("Could not extract text from the document.")
        
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
    
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
