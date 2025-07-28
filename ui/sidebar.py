(cd "$(git rev-parse --show-toplevel)" && git apply --3way <<'EOF'
diff --git a/ui/sidebar.py b/ui/sidebar.py
--- a/ui/sidebar.py
+++ b/ui/sidebar.py
@@ -1,266 +1,269 @@
-"""
-Sidebar components 
-
-Contains file upload interface, settings panels, and navigation elements
-that appear in the Streamlit sidebar.
-"""
-
-import streamlit as st
-from typing import Tuple, Optional
-
-
-def render_file_upload_sidebar() -> Tuple[Optional[object the file upload section in the sidebar.
-    
-    Returns:
-        tuple: (uploaded_file, file_stats) where file_stats contains metadata
-    """
-    st.header("📂 Upload Study Material")
-    st.markdown("Upload your notes, textbooks, or research papers to get started!")
-    
-    uploaded_file = st.file_uploader(
-        "Choose a PDF or TXT file",
-        type=["pdf", "txt"],
-        help="Supported formats: PDF, TXT. Max size: 200MB",
-        accept_multiple_files=False
-    )
-    
-    file_stats = {}
-    
-    if uploaded_file is not None:
-        # Display file information
-        file_stats = {
-            'name': uploaded_file.name,
-            'size': uploaded_file.size,
-            'type': uploaded_file.type
-        }
-        
-        # Show file details in a nice format
-        st.success(f"✅ **{uploaded_file.name}** uploaded successfully!")
-        
-        # File size in human-readable format
-        size_mb = uploaded_file.size / (1024 * 1024)
-        if size_mb < 1:
-            size_str = f"{uploaded_file.size / 1024:.1f} KB"
-        else:
-            size_str = f"{size_mb:.1f} MB"
-        
-        st.info(f"""
-        **File Details:**
-        - **Size:** {size_str}
-        - **Type:** {uploaded_file.type}
-        """)
-        
-        # Warning for large files
-        if size_mb > 50:
-            st.warning("⚠️ Large file detected. Processing may take longer.")
-    
-    else:
-        st.info("👆 Upload a document to begin creating study aids!")
-    
-    return uploaded_file, file_stats
-
-
-def render_settings_sidebar() -> dict:
-    """
-    Render the settings and configuration panel in the sidebar.
-    
-    Returns:
-        dict: Dictionary containing all user settings
-    """
-    st.markdown("---")  # Divider
-    st.header("⚙️ Study Aid Settings")
-    
-    # Summary settings
-    st.subheader("📝 Summary Options")
-    summary_length = st.selectbox(
-        "Summary Length",
-        options=["Short (50-100 words)", "Medium (100-200 words)", "Long (200-300 words)"],
-        index=1,
-        help="Choose how detailed you want your AI summary to be"
-    )
-    
-    summary_style = st.radio(
-        "Summary Style",
-        options=["Academic", "Simple", "Bullet Points"],
-        index=0,
-        help="Select the writing style for your summary"
-    )
-    
-    # Flashcard settings
-    st.subheader("🃏 Flashcard Options")
-    num_flashcards = st.slider(
-        "Number of Flashcards",
-        min_value=5,
-        max_value=25,
-        value=10,
-        step=1,
-        help="How many flashcards to generate from your document"
-    )
-    
-    flashcard_difficulty = st.selectbox(
-        "Difficulty Level",
-        options=["Easy", "Medium", "Hard"],
-        index=1,
-        help="Choose the complexity of questions and answers"
-    )
-    
-    # Audio settings
-    st.subheader("🔊 Audio Options")
-    tts_language = st.selectbox(
-        "Language",
-        options=[
-            ("English", "en"),
-            ("Spanish", "es"), 
-            ("French", "fr"),
-            ("German", "de"),
-            ("Italian", "it")
-        ],
-        format_func=lambda x: x[0],
-        index=0,
-        help="Select the language for text-to-speech"
-    )
-    
-    speech_speed = st.selectbox(
-        "Speech Speed",
-        options=["Slow", "Normal", "Fast"],
-        index=1,
-        help="Choose how fast the audio should be spoken"
-    )
-    
-    # Search settings
-    st.subheader("🔍 Search Options")
-    search_results_count = st.slider(
-        "Search Results",
-        min_value=3,
-        max_value=10,
-        value=5,
-        help="Number of relevant passages to show in search results"
-    )
-    
-    # Export settings
-    st.subheader("📄 Export Options")
-    export_format = st.multiselect(
-        "Export Formats",
-        options=["PDF", "Markdown", "Plain Text"],
-        default=["PDF"],
-        help="Choose which formats to export your study aids to"
-    )
-    
-    # Compile all settings into a dictionary
-    settings = {
-        'summary': {
-            'length': summary_length,
-            'style': summary_style
-        },
-        'flashcards': {
-            'count': num_flashcards,
-            'difficulty': flashcard_difficulty
-        },
-        'audio': {
-            'language': tts_language[1],  # Get the language code
-            'language_name': tts_language[0],  # Get the display name
-            'speed': speech_speed.lower()
-        },
-        'search': {
-            'results_count': search_results_count
-        },
-        'export': {
-            'formats': export_format
-        }
-    }
-    
-    return settings
-
-
-def render_help_sidebar():
-    """
-    Render a help and tips section in the sidebar.
-    """
-    st.markdown("---")
-    st.header("💡 Tips & Help")
-    
-    with st.expander("📚 How to Use"):
-        st.markdown("""
-        **Step 1:** Upload your study material (PDF or TXT)
-        
-        **Step 2:** Adjust settings in the sidebar
-        
-        **Step 3:** Use the tabs to:
-        - Generate AI summaries
-        - Create flashcards for review
-        - Convert text to audio
-        - Search through your content
-        
-        **Step 4:** Export your study aids when ready!
-        """)
-    
-    with st.expander("🎯 Best Practices"):
-        st.markdown("""
-        - **Upload quality documents:** Clear, well-formatted PDFs work best
-        - **Use descriptive filenames:** This helps with organization
-        - **Start with summaries:** Get an overview before diving into flashcards
-        - **Try audio mode:** Great for reviewing while commuting
-        - **Use search frequently:** Find specific topics quickly
-        """)
-    
-    with st.expander("⚡ Troubleshooting"):
-        st.markdown("""
-        - **Slow processing?** Try shorter documents or reduce flashcard count
-        - **Poor text extraction?** Ensure your PDF has selectable text, not just images
-        - **Audio not working?** Check your browser's audio settings
-        - **Search not finding results?** Try different keywords or phrases
-        """)
-    
-    # Contact/feedback section
-    st.markdown("---")
-    st.markdown("**Need Help?**")
-    st.markdown("📧 Contact: [your-email@domain.com]")
-    st.markdown("⭐ [Rate this app](your-feedback-link)")
-
-
-def render_progress_sidebar(current_step: str = "upload"):
-    """
-    Render a progress indicator showing the current step in the workflow.
-    
-    Args:
-        current_step (str): Current step ('upload', 'processing', 'results', 'export')
-    """
-    st.markdown("---")
-    st.header("📊 Progress")
-    
-    steps = {
-        'upload': '📂 Upload Document',
-        'processing': '🤖 AI Processing', 
-        'results': '📋 Review Results',
-        'export': '💾 Export & Save'
-    }
-    
-    step_order = ['upload', 'processing', 'results', 'export']
-    current_index = step_order.index(current_step) if current_step in step_order else 0
-    
-    for i, (step_key, step_name) in enumerate(steps.items()):
-        if i < current_index:
-            st.success(f"✅ {step_name}")
-        elif i == current_index:
-            st.info(f"🔄 {step_name}")
-        else:
-            st.write(f"⏳ {step_name}")
-
-
-# Example usage and testing
-if __name__ == "__main__":
-    st.set_page_config(page_title="Sidebar Test", layout="wide")
-    
-    with st.sidebar:
-        uploaded_file, file_stats = render_file_upload_sidebar()
-        settings = render_settings_sidebar()
-        render_help_sidebar()
-        render_progress_sidebar("processing")
-    
-    # Show results in main area for testing
-    st.title("Sidebar Components Test")
-    
-    if uploaded_file:
-        st.write("**File Info:**", file_stats)
-    
-    st.write("**Settings:**", settings)
+"""
+Sidebar components 
+
+Contains file upload interface, settings panels, and navigation elements
+that appear in the Streamlit sidebar.
+"""
+
+import streamlit as st
+from typing import Tuple, Optional
+
+
+def render_file_upload_sidebar() -> Tuple[Optional[object], dict]:
+    """
+    Render the file upload section in the sidebar.
+    
+    Returns:
+        tuple: (uploaded_file, file_stats) where file_stats contains metadata
+    """
+    st.header("📂 Upload Study Material")
+    st.markdown("Upload your notes, textbooks, or research papers to get started!")
+    
+    uploaded_file = st.file_uploader(
+        "Choose a PDF or TXT file",
+        type=["pdf", "txt"],
+        help="Supported formats: PDF, TXT. Max size: 200MB",
+        accept_multiple_files=False
+    )
+    
+    file_stats = {}
+    
+    if uploaded_file is not None:
+        # Display file information
+        file_stats = {
+            'name': uploaded_file.name,
+            'size': uploaded_file.size,
+            'type': uploaded_file.type
+        }
+        
+        # Show file details in a nice format
+        st.success(f"✅ **{uploaded_file.name}** uploaded successfully!")
+        
+        # File size in human-readable format
+        size_mb = uploaded_file.size / (1024 * 1024)
+        if size_mb < 1:
+            size_str = f"{uploaded_file.size / 1024:.1f} KB"
+        else:
+            size_str = f"{size_mb:.1f} MB"
+        
+        st.info(f"""
+        **File Details:**
+        - **Size:** {size_str}
+        - **Type:** {uploaded_file.type}
+        """)
+        
+        # Warning for large files
+        if size_mb > 50:
+            st.warning("⚠️ Large file detected. Processing may take longer.")
+    
+    else:
+        st.info("👆 Upload a document to begin creating study aids!")
+    
+    return uploaded_file, file_stats
+
+
+def render_settings_sidebar() -> dict:
+    """
+    Render the settings and configuration panel in the sidebar.
+    
+    Returns:
+        dict: Dictionary containing all user settings
+    """
+    st.markdown("---")  # Divider
+    st.header("⚙️ Study Aid Settings")
+    
+    # Summary settings
+    st.subheader("📝 Summary Options")
+    summary_length = st.selectbox(
+        "Summary Length",
+        options=["Short (50-100 words)", "Medium (100-200 words)", "Long (200-300 words)"],
+        index=1,
+        help="Choose how detailed you want your AI summary to be"
+    )
+    
+    summary_style = st.radio(
+        "Summary Style",
+        options=["Academic", "Simple", "Bullet Points"],
+        index=0,
+        help="Select the writing style for your summary"
+    )
+    
+    # Flashcard settings
+    st.subheader("🃏 Flashcard Options")
+    num_flashcards = st.slider(
+        "Number of Flashcards",
+        min_value=5,
+        max_value=25,
+        value=10,
+        step=1,
+        help="How many flashcards to generate from your document"
+    )
+    
+    flashcard_difficulty = st.selectbox(
+        "Difficulty Level",
+        options=["Easy", "Medium", "Hard"],
+        index=1,
+        help="Choose the complexity of questions and answers"
+    )
+    
+    # Audio settings
+    st.subheader("🔊 Audio Options")
+    tts_language = st.selectbox(
+        "Language",
+        options=[
+            ("English", "en"),
+            ("Spanish", "es"), 
+            ("French", "fr"),
+            ("German", "de"),
+            ("Italian", "it")
+        ],
+        format_func=lambda x: x[0],
+        index=0,
+        help="Select the language for text-to-speech"
+    )
+    
+    speech_speed = st.selectbox(
+        "Speech Speed",
+        options=["Slow", "Normal", "Fast"],
+        index=1,
+        help="Choose how fast the audio should be spoken"
+    )
+    
+    # Search settings
+    st.subheader("🔍 Search Options")
+    search_results_count = st.slider(
+        "Search Results",
+        min_value=3,
+        max_value=10,
+        value=5,
+        help="Number of relevant passages to show in search results"
+    )
+    
+    # Export settings
+    st.subheader("📄 Export Options")
+    export_format = st.multiselect(
+        "Export Formats",
+        options=["PDF", "Markdown", "Plain Text"],
+        default=["PDF"],
+        help="Choose which formats to export your study aids to"
+    )
+    
+    # Compile all settings into a dictionary
+    settings = {
+        'summary': {
+            'length': summary_length,
+            'style': summary_style
+        },
+        'flashcards': {
+            'count': num_flashcards,
+            'difficulty': flashcard_difficulty
+        },
+        'audio': {
+            'language': tts_language[1],  # Get the language code
+            'language_name': tts_language[0],  # Get the display name
+            'speed': speech_speed.lower()
+        },
+        'search': {
+            'results_count': search_results_count
+        },
+        'export': {
+            'formats': export_format
+        }
+    }
+    
+    return settings
+
+
+def render_help_sidebar():
+    """
+    Render a help and tips section in the sidebar.
+    """
+    st.markdown("---")
+    st.header("💡 Tips & Help")
+    
+    with st.expander("📚 How to Use"):
+        st.markdown("""
+        **Step 1:** Upload your study material (PDF or TXT)
+        
+        **Step 2:** Adjust settings in the sidebar
+        
+        **Step 3:** Use the tabs to:
+        - Generate AI summaries
+        - Create flashcards for review
+        - Convert text to audio
+        - Search through your content
+        
+        **Step 4:** Export your study aids when ready!
+        """)
+    
+    with st.expander("🎯 Best Practices"):
+        st.markdown("""
+        - **Upload quality documents:** Clear, well-formatted PDFs work best
+        - **Use descriptive filenames:** This helps with organization
+        - **Start with summaries:** Get an overview before diving into flashcards
+        - **Try audio mode:** Great for reviewing while commuting
+        - **Use search frequently:** Find specific topics quickly
+        """)
+    
+    with st.expander("⚡ Troubleshooting"):
+        st.markdown("""
+        - **Slow processing?** Try shorter documents or reduce flashcard count
+        - **Poor text extraction?** Ensure your PDF has selectable text, not just images
+        - **Audio not working?** Check your browser's audio settings
+        - **Search not finding results?** Try different keywords or phrases
+        """)
+    
+    # Contact/feedback section
+    st.markdown("---")
+    st.markdown("**Need Help?**")
+    st.markdown("📧 Contact: [your-email@domain.com]")
+    st.markdown("⭐ [Rate this app](your-feedback-link)")
+
+
+def render_progress_sidebar(current_step: str = "upload"):
+    """
+    Render a progress indicator showing the current step in the workflow.
+    
+    Args:
+        current_step (str): Current step ('upload', 'processing', 'results', 'export')
+    """
+    st.markdown("---")
+    st.header("📊 Progress")
+    
+    steps = {
+        'upload': '📂 Upload Document',
+        'processing': '🤖 AI Processing', 
+        'results': '📋 Review Results',
+        'export': '💾 Export & Save'
+    }
+    
+    step_order = ['upload', 'processing', 'results', 'export']
+    current_index = step_order.index(current_step) if current_step in step_order else 0
+    
+    for i, (step_key, step_name) in enumerate(steps.items()):
+        if i < current_index:
+            st.success(f"✅ {step_name}")
+        elif i == current_index:
+            st.info(f"🔄 {step_name}")
+        else:
+            st.write(f"⏳ {step_name}")
+
+
+# Example usage and testing
+if __name__ == "__main__":
+    st.set_page_config(page_title="Sidebar Test", layout="wide")
+    
+    with st.sidebar:
+        uploaded_file, file_stats = render_file_upload_sidebar()
+        settings = render_settings_sidebar()
+        render_help_sidebar()
+        render_progress_sidebar("processing")
+    
+    # Show results in main area for testing
+    st.title("Sidebar Components Test")
+    
+    if uploaded_file:
+        st.write("**File Info:**", file_stats)
+    
+    st.write("**Settings:**", settings)
+
EOF
)
