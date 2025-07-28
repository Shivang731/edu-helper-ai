# 📚 Smart Study-Aid Generator

An intelligent Streamlit application that transforms your study materials into summaries, flashcards, and audio notes using AI.

## Features

- **📄 Document Processing**: Upload PDF and TXT files
- **🤖 AI Summarization**: Generate concise summaries using BART model
- **🃏 Flashcard Generation**: Create interactive flashcards for review
- **🔊 Text-to-Speech**: Convert summaries to audio for listening
- **🔍 Semantic Search**: Search through your documents intelligently
- **📊 Document Analysis**: Extract key terms and statistics
- **💾 Export Options**: Save your study aids in multiple formats

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd smart-study-aid-generator
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   streamlit run app/main.py
   ```

## Usage

1. **Upload a Document**: Use the sidebar to upload your PDF or TXT file
2. **Adjust Settings**: Configure summary length, flashcard count, and audio options
3. **Generate Study Aids**: Click the action buttons to create summaries, flashcards, and audio
4. **Search Content**: Use the search feature to find specific information
5. **Export Results**: Save your study aids in Markdown or PDF format

## Project Structure

```
├── app/
│   └── main.py              # Main Streamlit application
├── core/
│   ├── fetcher.py           # Document text extraction
│   ├── parser.py            # Text cleaning and preprocessing
│   ├── summarizer.py        # AI-powered summarization
│   ├── quizgen.py           # Flashcard and quiz generation
│   └── tts.py              # Text-to-speech conversion
├── services/
│   ├── embeddings.py        # Semantic search functionality
│   ├── storage.py           # Data persistence
│   └── exporter.py          # Export utilities
├── ui/
│   ├── sidebar.py           # Sidebar components
│   ├── views.py             # Display components
│   └── controls.py          # Interactive controls
├── data/                    # Storage directory
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## Dependencies

- **Streamlit**: Web application framework
- **Transformers**: Hugging Face models for AI tasks
- **PyPDF**: PDF text extraction
- **NLTK**: Natural language processing
- **gTTS**: Google Text-to-Speech
- **FAISS**: Vector similarity search
- **Sentence Transformers**: Text embeddings

## Troubleshooting

- **Slow processing**: Try shorter documents or reduce flashcard count
- **Poor text extraction**: Ensure your PDF has selectable text, not just images
- **Audio not working**: Check your browser's audio settings
- **Search not finding results**: Try different keywords or phrases

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is open source and available under the MIT License.