import streamlit as st
import sys
from pathlib import Path
import streamlit.components.v1 as components

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

# CRITICAL: Use components.html for better rendering
def inject_custom_css():
    components.html("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        /* Hide Streamlit branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .stDeployButton {display: none;}
        
        /* Global font and reset */
        .main > div {
            padding-top: 0rem;
            font-family: 'Inter', sans-serif;
        }
        
        /* Hero section styling */
        .hero-section {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            text-align: center;
            padding: 4rem 2rem;
            margin: -1rem -1rem 3rem -1rem;
            border-radius: 0 0 20px 20px;
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
            margin-bottom: 0;
            max-width: 600px;
            margin-left: auto;
            margin-right: auto;
        }
        
        /* Section styling */
        .section-header {
            text-align: center;
            margin-bottom: 3rem;
        }
        
        .section-title {
            font-size: 2.5rem;
            font-weight: 600;
            color: #1a202c;
            margin-bottom: 1rem;
        }
        
        .section-subtitle {
            font-size: 1.1rem;
            color: #718096;
            max-width: 600px;
            margin: 0 auto;
        }
        
        /* Feature cards */
        .features-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 2rem;
            margin: 2rem 0;
        }
        
        .feature-card {
            background: white;
            padding: 2rem;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            border: 1px solid #e2e8f0;
            text-align: center;
            transition: all 0.3s ease;
        }
        
        .feature-card:hover {
            transform: translateY(-8px);
            box-shadow: 0 12px 30px rgba(0, 0, 0, 0.15);
        }
        
        .feature-icon {
            font-size: 3rem;
            margin-bottom: 1rem;
            display: block;
        }
        
        .feature-title {
            font-size: 1.25rem;
            font-weight: 600;
            margin-bottom: 0.75rem;
            color: #2d3748;
        }
        
        .feature-description {
            color: #718096;
            line-height: 1.6;
        }
        
        /* Demo section */
        .demo-section {
            background: #f8fafc;
            padding: 3rem 2rem;
            margin: 3rem -1rem;
            border-radius: 12px;
        }
        
        .demo-card {
            background: white;
            padding: 2rem;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            max-width: 800px;
            margin: 0 auto;
        }
        
        .demo-title {
            font-size: 1.5rem;
            font-weight: 600;
            color: #2d3748;
            margin-bottom: 1rem;
        }
        
        /* Testimonials */
        .testimonials-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 2rem;
            margin: 2rem 0;
        }
        
        .testimonial-card {
            background: white;
            padding: 2rem;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            border-left: 4px solid #667eea;
        }
        
        .testimonial-text {
            font-style: italic;
            color: #4a5568;
            margin-bottom: 1rem;
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
        
        /* About section */
        .about-section {
            background: linear-gradient(135deg, #2d3748 0%, #4a5568 100%);
            color: white;
            padding: 4rem 2rem;
            margin: 3rem -1rem;
            border-radius: 12px;
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
            margin-bottom: 1rem;
        }
        
        .about-description {
            opacity: 0.9;
            line-height: 1.6;
            margin-bottom: 2rem;
            max-width: 600px;
            margin-left: auto;
            margin-right: auto;
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
            padding: 0.75rem 1.5rem;
            border-radius: 8px;
            text-decoration: none;
            font-weight: 500;
            transition: all 0.2s;
        }
        
        .social-link:hover {
            background: #5a67d8;
            transform: translateY(-2px);
            color: white;
            text-decoration: none;
        }
        
        /* CTA section */
        .cta-section {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 4rem 2rem;
            text-align: center;
            border-radius: 12px;
            margin: 3rem 0;
        }
        
        .cta-title {
            font-size: 2.5rem;
            font-weight: 600;
            margin-bottom: 1rem;
        }
        
        .cta-subtitle {
            font-size: 1.1rem;
            opacity: 0.9;
            margin-bottom: 0;
        }
        
        /* Mobile responsive */
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
            .features-grid {
                grid-template-columns: 1fr;
            }
            .testimonials-grid {
                grid-template-columns: 1fr;
            }
        }
    </style>
    """, height=0)

def render_hero_section():
    st.markdown("""
    <div class="hero-section">
        <h1 class="hero-title">Transform Your Notes.<br>Accelerate Your Learning.</h1>
        <p class="hero-subtitle">Summarize textbooks, generate flashcards, and listen to notes instantly with Edu Helper.</p>
    </div>
    """, unsafe_allow_html=True)

def render_features_section():
    st.markdown("""
    <div class="section-header">
        <h2 class="section-title">Why Use Edu Helper?</h2>
        <p class="section-subtitle">Your AI-powered study assistant that transforms how you learn and retain information.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Use components.html for better icon rendering
    components.html("""
    <div class="features-grid">
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
        </div>
        """, height=400)
