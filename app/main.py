import streamlit as st

st.set_page_config(page_title="Edu Helper AI", page_icon="📚", layout="wide")

# Inject CSS
st.markdown("""
    <style>
    body { background-color: #151929 !important; }
    .main { background-color: #151929; }
    .block-container { padding-top: 2rem; }
    .css-1q8dd3e, .stButton > button {
        background: linear-gradient(90deg, #7046ec 0%, #5b21b6 100%) !important;
        color: #fff !important;
        border-radius: 8px !important;
    }
    .stButton > button { padding: 0.5rem 2rem; font-weight: bold;}
    .feature-card {
        background: #23263f;
        padding: 1.2rem 1rem;
        border-radius: 15px;
        box-shadow: 0 2px 16px rgba(120, 69, 246, 0.10);
        margin-bottom: 1rem;
        min-height: 145px;
        display: flex;
        flex-direction: column;
        align-items: start;
    }
    .feature-icon {
        font-size: 2.2rem;
        margin-bottom: 0.3rem;
        color: #8b5cf6;
    }
    .testimonial {
        background: #23263f;
        padding: 1.0rem 1rem;
        border-radius: 12px;
        margin-bottom: 0.8rem;
    }
    .about-card {
        background: #23263f;
        padding: 1.0rem 1rem;
        border-radius: 12px;
        margin: 0 auto;
        text-align: center;
    }
    a { color: #8b5cf6; }
    </style>
""", unsafe_allow_html=True)

# Hero Section
cols = st.columns([2,2])
with cols[0]:
    st.markdown("#### Transform Your Notes.<br>Accelerate <span style='color:#8b5cf6;'>Your Learning.</span>", unsafe_allow_html=True)
    st.write("A smart tool to turn textbooks, papers, and lectures to quick summaries, audio notes & more. Easily, in one click.")
    st.markdown('<a href="#trydemo" style="text-decoration:none;"><button style="margin-top:15px">🚀 Try the Demo</button></a>', unsafe_allow_html=True)
with cols[1]:
    st.image("images/hero-img.png", use_column_width=True)

st.markdown("### Why Use Edu Helper?")
features = [
    {
        "icon": "📄",
        "title": "AI Summarization",
        "desc": "Quickly condense large texts or PDFs into easy-to-learn summaries using AI."
    },
    {
        "icon": "🚀",
        "title": "Instant Flashcards",
        "desc": "Generate flashcards from your notes instantly for effective revision."
    },
    {
        "icon": "🔊",
        "title": "Audio Notes",
        "desc": "Convert summaries into audio for on-the-go learning."
    },
    {
        "icon": "🔎",
        "title": "Semantic Search",
        "desc": "Quickly find concepts or definitions from your files."
    }
]
cols = st.columns(4)
for i, f in enumerate(features):
    with cols[i]:
        st.markdown(f"<div class='feature-card'><span class='feature-icon'>{f['icon']}</span><b>{f['title']}</b><br><span>{f['desc']}</span></div>", unsafe_allow_html=True)

# Demo Section
st.markdown("## <span id='trydemo'></span>See Edu Helper in Action", unsafe_allow_html=True)
with st.expander("📄 Summarize PDF / Text", expanded=True):
    uploaded_file = st.file_uploader("Upload a PDF file or paste text below", type=["pdf"], key="demo_pdf")
    text_input = st.text_area("Or paste your text here")
    if st.button("Summarize"):
        # Here you call your summarize() function
        st.success("Mock summary output. (Replace with your backend summarize function's output)")

# Testimonials
st.markdown("### What Students Say")
testimonials = [
    {"user": "Akshay J.", "desc": "Helped me cover my syllabus faster before exams. Game changer!", "stars": "⭐️⭐️⭐️⭐️⭐️"},
    {"user": "Swati M.", "desc": "The audio notes let me revise during commute. Love it!", "stars": "⭐️⭐️⭐️⭐️⭐️"},
    {"user": "Irfan Q.", "desc": "Semantic search has saved me HOURS looking for where I wrote concepts.", "stars": "⭐️⭐️⭐️⭐️⭐️"},
]
cols = st.columns(3)
for i, t in enumerate(testimonials):
    with cols[i]:
        st.markdown(
            f"<div class='testimonial'>{t['stars']}<br>"
            f"<i>\"{t['desc']}\"</i><br><b>{t['user']}</b></div>", unsafe_allow_html=True
        )

# About the Creator
st.markdown("### About the Creator")
st.markdown(
    "<div class='about-card'><b>Shivang Kumar Dubey</b><br>"
    "An AI/ML enthusiast, full-stack & product builder. Created Edu Helper to make studying accessible & effortless for everyone."
    "<br><br><a href='https://github.com/Shivang731'>GitHub</a> | <a href='https://x.com/shivang_731'>X (Twitter)</a>"
    "</div>",
    unsafe_allow_html=True
)

# Final CTA + Contact Form
st.markdown("## Ready to Transform Your Study Experience?")
st.markdown("<a href='#trydemo'><button>🎓 Launch Edu Helper Now</button></a>", unsafe_allow_html=True)

st.markdown("### Connect With Us")
with st.form(key="contact_form"):
    cols = st.columns(2)
    with cols[0]:
        name = st.text_input("Your Name")
    with cols[1]:
        email = st.text_input("Email")
    message = st.text_area("Message")
    submit = st.form_submit_button("Send Message")
    if submit and name and email and message:
        st.success("Thank you for reaching out! We'll get back soon.")

st.markdown('<div style="text-align:center;color:gray;font-size:0.9em;margin-top:2rem;">© 2024 Edu Helper | Made by Shivang Kumar Dubey</div>', unsafe_allow_html=True)
