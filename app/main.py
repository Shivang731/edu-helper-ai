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

# CRITICAL FIX: Inject CSS properly for Streamlit Cloud
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display:none;}
    
    /* Reset padding */
    .main > div {
        padding-top: 0rem;
        padding-left: 1rem;
        padding-right: 1rem;
    }
    
    /* Font */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Hero section */
    .hero-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        text-align: center;
        padding: 4rem 2rem;
        margin: -1rem -1rem 2rem -1rem;
        border-radius: 0 0 20px 20px;
    }
    
    .hero-title {
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 1rem;
        line-height: 1.2;
    }
    
    .hero-subtitle {
        font-size: 1.2rem;
        opacity: 0.9;
        margin-bottom: 0;
    }
    
    /* Feature cards */
    .feature-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 1.5rem;
        margin: 2rem 0;
    }
    
    .feature-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border: 1px solid #e2e8f0;
        text-align: center;
        transition: transform 0.2s, box-shadow 0.2s;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
    }
    
    .feature-icon {
        font-size: 2.5rem;
        margin-bottom: 1rem;
        display: block;
    }
    
    .feature-title {
        font-size: 1.1rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
        color: #2d3748;
    }
    
    .feature-desc {
        color: #718096;
        font-size: 0.9rem;
        line-height: 1.5;
    }
    
    /* Demo section */
    .demo-section {
        background: #f8fafc;
        padding: 2rem;
        border-radius: 12px;
        margin: 2rem 0;
    }
    
    .demo-card {
        background: white;
        padding: 1.5rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    /* Testimonials */
    .testimonial-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 1.5rem;
        margin: 2rem 0;
    }
    
    .testimonial-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border-left: 4px solid #667eea;
    }
    
    .testimonial-text {
        font-style: italic;
        color: #4a5568;
        margin-bottom: 1rem;
    }
    
    .testimonial-author {
        font-weight: 600;
        color: #2d3748;
    }
    
    .testimonial-role {
        color: #718096;
        font-size: 0.85rem;
    }
    
    /* About section */
    .about-section {
        background: linear-gradient(135deg, #2d3748 0%, #4a5568 100%);
        color: white;
        padding: 3rem 2rem;
        margin: 2rem -1rem;
        border-radius: 12px;
        text-align: center;
    }
    
    .about-title {
        font-size: 1.8rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    
    .about-name {
        font-size: 1.3rem;
        font-weight: 600;
        color: #667eea;
        margin-bottom: 1rem;
    }
    
    .social-links {
        display: flex;
        justify-content: center;
        gap: 1rem;
        margin-top: 1.5rem;
        flex-wrap: wrap;
    }
    
    .social-link {
        background: #667eea;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 6px;
        text-decoration: none;
        font-weight: 500;
        transition: background 0.2s;
    }
    
    .social-link:hover {
        background: #5a67d8;
        color: white;
        text-decoration: none;
    }
    
    /* CTA section */
    .cta-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 3rem 2rem;
        text-align: center;
        border-radius: 12px;
        margin: 2rem 0;
    }
    
    .cta-title {
        font-size: 2rem;
        font-weight: 600;
        margin-bottom: 1rem;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.2s;
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
    }
    
    /* Mobile responsive */
    @media (max-width: 768px) {
        .hero-title {
            font-size: 2rem;
        }
        .feature-container {
            grid-template-columns: 1fr;
        }
        .testimonial-container {
            grid-template-columns: 1fr;
        }
    }
</style>
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

    # Hero Section
    st.markdown("""
    <div class="hero-section">
        <h1 class="hero-title">Transform Your Notes.<br>Accelerate Your Learning.</h1>
        <p class="hero-subtitle">Summarize textbooks, generate flashcards, and listen to notes instantly with Edu Helper.</p>
    </div>
    """, unsafe_allow_html=True)

    # Features Section
    st.markdown("## Why Use Edu Helper?")
    st.markdown("Your AI-powered study assistant that transforms how you learn and retain information.")
    
    st.markdown("""
    <div class="feature-container">
        <div class="feature-card">
            <div class="feature-icon">📝</div>
            <h3 class="feature-title">Instant AI Summaries</h3>
            <p class="feature-desc">Save hours with intelligent summaries of your textbooks and lecture notes.</p>
        </div>
        
        <div class="feature-card">
            <div class="feature-icon">🃏</div>
            <h3 class="feature-title">Automatic Flashcards</h3>
            <p class="feature-desc">Turn text into interactive flashcards for effective spaced repetition learning.</p>
        </div>
        
        <div class="feature-card">
            <div class="feature-icon">🔊</div>
            <h3 class="feature-title">Audio Notes</h3>
            <p class="feature-desc">Listen to your notes anytime, anywhere. Perfect for learning on the go.</p>
        </div>
        
        <div class="feature-card">
            <div class="feature-icon">🔍</div>
            <h3 class="feature-title">Semantic Search</h3>
            <p class="feature-desc">Ask questions in natural language and get answers from your own materials.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Demo Section
    st.markdown("## See It In Action")
    st.markdown("Here's how Edu Helper transforms your study materials:")
    
    st.markdown("""
    <div class="demo-section">
        <div class="demo-card">
            <h3>Machine Learning Fundamentals</h3>
            <p><strong>Key Concepts:</strong> Machine learning is a subset of AI focused on developing algorithms that learn from data. It includes supervised learning (labeled data), unsupervised learning (unlabeled data), and reinforcement learning (reward-based).</p>
            <p><strong>Applications:</strong> Used in recommendation systems, image recognition, natural language processing, and predictive analytics.</p>
            <p><strong>Important Algorithms:</strong> Linear regression, decision trees, neural networks, and k-means clustering.</p>
            <p><strong>Challenges:</strong> Overfitting, underfitting, bias in data, and computational complexity.</p>
            <p style="font-style: italic; color: #718096;">Generated from: "Introduction to Machine Learning.pdf" (32 pages)</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Testimonials Section
    st.markdown("## What Students Say")
    st.markdown("Hear from students who transformed their study habits with Edu Helper:")
    
    st.markdown("""
    <div class="testimonial-container">
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
    """, unsafe_allow_html=True)

    # About Section
    st.markdown("""
    <div class="about-section">
        <h2 class="about-title">About the Creator</h2>
        <h3 class="about-name">Shivang Kumar Dubey</h3>
        <p>First-year Scaler School of Technology student. Passionate about AI/ML and helping students succeed. Created Edu Helper to solve real problems faced by students in managing and absorbing large amounts of study material.</p>
        
        <div class="social-links">
            <a href="mailto:shivangdubey731@gmail.com" class="social-link">📧 Email</a>
            <a href="https://instagram.com/shivang.skd" target="_blank" class="social-link">📷 Instagram</a>
            <a href="https://github.com/shivang731" target="_blank" class="social-link">💻 GitHub</a>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # CTA and Upload Section
    st.markdown("""
    <div class="cta-section">
        <h2 class="cta-title">Ready to Transform Your Study Habits?</h2>
        <p>Upload your first document and see the magic happen in seconds. No credit card required.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # File Upload Section
    st.markdown("### 📁 Upload Your Study Material")
    uploaded_file = st.file_uploader(
        "Choose a PDF or TXT file",
        type=["pdf", "txt"],
        help="Upload your study materials to get started"
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
                
                # Show preview
                with st.expander("📄 Document Preview", expanded=False):
                    st.text_area("Extracted Text", cleaned_text[:1000] + "..." if len(cleaned_text) > 1000 else cleaned_text, height=200)
                
                # Action buttons
                st.markdown("### 🚀 Generate Study Materials")
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    if st.button("📝 Generate Summary", use_container_width=True):
                        with st.spinner("Generating summary..."):
                            try:
                                summary = generate_summary(cleaned_text)
                                st.session_state.summary = summary
                                st.session_state.storage_service.save_summary(uploaded_file.name, summary)
                                
                                st.markdown("#### 📝 AI Summary")
                                st.write(summary)
                            except Exception as e:
                                st.error(f"Error generating summary: {str(e)}")
                
                with col2:
                    if st.button("🃏 Create Flashcards", use_container_width=True):
                        with st.spinner("Generating flashcards..."):
                            try:
                                flashcards = generate_flashcards(cleaned_text, 5)
                                st.session_state.flashcards = flashcards
                                
                                st.markdown("#### 🃏 Flashcards")
                                for i, card in enumerate(flashcards):
                                    with st.expander(f"Card {i+1}: {card.get('front', 'Question')[:50]}..."):
                                        st.write(f"**Question:** {card.get('front', 'No question')}")
                                        st.write(f"**Answer:** {card.get('back', 'No answer')}")
                            except Exception as e:
                                st.error(f"Error generating flashcards: {str(e)}")
                
                with col3:
                    if st.button("🔊 Generate Audio", use_container_width=True):
                        if hasattr(st.session_state, 'summary') and st.session_state.summary:
                            with st.spinner("Generating audio..."):
                                try:
                                    audio_bytes = text_to_speech(st.session_state.summary)
                                    if audio_bytes:
                                        st.session_state.audio_bytes = audio_bytes
                                        st.markdown("#### 🔊 Audio Notes")
                                        st.audio(audio_bytes)
                                    else:
                                        st.error("Could not generate audio. Please try again.")
                                except Exception as e:
                                    st.error(f"Error generating audio: {str(e)}")
                        else:
                            st.warning("Generate a summary first before creating audio.")
                
                # Search functionality
                st.markdown("### 🔍 Search Your Document")
                search_query = st.text_input("Ask a question about your document:", placeholder="e.g., What are the main concepts?")
                
                if search_query and st.button("Search", use_container_width=True):
                    try:
                        results = st.session_state.search_service.search(search_query, top_k=3)
                        
                        st.markdown(f"#### 🔍 Search Results for: \"{search_query}\"")
                        
                        if results:
                            for i, result in enumerate(results):
                                st.markdown(f"**Result {i+1}:** {result}")
                        else:
                            st.info("No results found. Try a different search term.")
                    except Exception as e:
                        st.error(f"Error searching: {str(e)}")
                
            else:
                st.error("Could not extract text from the document. Please try a different file.")
        
        except Exception as e:
            st.error(f"An error occurred while processing your file: {str(e)}")

if __name__ == "__main__":
    main()
