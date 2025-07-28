import re
import random
from typing import List, Dict, Tuple, Optional
import spacy
from collections import Counter

class FlashcardGenerator:
    """Generate flashcards and quizzes from study material."""
    
    def __init__(self):
        # Try to load spaCy model
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            print("spaCy model not found. Install with: python -m spacy download en_core_web_sm")
            self.nlp = None
        
        # Common question words and patterns
        self.question_patterns = {
            'what': ['What is', 'What are', 'What does', 'What do'],
            'who': ['Who is', 'Who are', 'Who was', 'Who were'],
            'when': ['When did', 'When does', 'When is', 'When was'],
            'where': ['Where is', 'Where are', 'Where did', 'Where does'],
            'why': ['Why is', 'Why are', 'Why did', 'Why does'],
            'how': ['How is', 'How are', 'How did', 'How does', 'How do']
        }
    
    def extract_key_concepts(self, text: str) -> List[str]:
        """Extract key concepts from text using NLP."""
        if self.nlp:
            doc = self.nlp(text)
            # Extract named entities and noun phrases
            concepts = []
            
            # Named entities
            for ent in doc.ents:
                if ent.label_ in ['PERSON', 'ORG', 'GPE', 'EVENT', 'LAW', 'LANGUAGE']:
                    concepts.append(ent.text)
            
            # Important noun phrases
            for chunk in doc.noun_chunks:
                if len(chunk.text.split()) <= 4 and len(chunk.text) > 3:
                    concepts.append(chunk.text)
            
            return list(set(concepts))
        else:
            # Simple fallback method
            return self._extract_concepts_simple(text)
    
    def _extract_concepts_simple(self, text: str) -> List[str]:
        """Simple concept extraction without spaCy."""
        # Find capitalized terms
        capitalized = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', text)
        
        # Find terms in quotes
        quoted = re.findall(r'"([^"]+)"', text)
        
        # Find terms with special formatting (if any)
        bold_terms = re.findall(r'\*\*(.*?)\*\*', text)
        
        concepts = capitalized + quoted + bold_terms
        # Remove duplicates and filter
        concepts = list(set([c for c in concepts if len(c) > 2 and len(c.split()) <= 4]))
        return concepts[:50]  # Limit to 50 concepts
    
    def generate_fill_in_blank(self, text: str, num_cards: int = 10) -> List[Dict[str, str]]:
        """Generate fill-in-the-blank flashcards."""
        sentences = [s.strip() for s in re.split(r'[.!?]+', text) if len(s.strip()) > 20]
        
        if len(sentences) < num_cards:
            num_cards = len(sentences)
        
        selected_sentences = random.sample(sentences, num_cards)
        flashcards = []
        
        for sentence in selected_sentences:
            # Extract potential key terms to blank out
            if self.nlp:
                doc = self.nlp(sentence)
                candidates = []
                
                # Look for nouns, proper nouns, and numbers
                for token in doc:
                    if (token.pos_ in ['NOUN', 'PROPN', 'NUM'] and 
                        len(token.text) > 2 and 
                        not token.is_stop):
                        candidates.append(token.text)
                
                # Also check named entities
                for ent in doc.ents:
                    candidates.append(ent.text)
                
                candidates = list(set(candidates))
            else:
                # Simple fallback
                words = sentence.split()
                candidates = [w for w in words if len(w) > 3 and w[0].isupper()]
            
            if candidates:
                # Choose a term to blank out
                term_to_blank = random.choice(candidates)
                
                # Create the fill-in-the-blank question
                question = sentence.replace(term_to_blank, "_" * len(term_to_blank))
                
                flashcard = {
                    'type': 'fill_in_blank',
                    'question': question,
                    'answer': term_to_blank,
                    'full_text': sentence
                }
                flashcards.append(flashcard)
        
        return flashcards
    
    def generate_qa_pairs(self, text: str, num_cards: int = 10) -> List[Dict[str, str]]:
        """Generate question-answer pairs from text."""
        sentences = [s.strip() for s in re.split(r'[.!?]+', text) if len(s.strip()) > 15]
        
        if len(sentences) < num_cards:
            num_cards = len(sentences)
        
        selected_sentences = random.sample(sentences, num_cards)
        qa_pairs = []
        
        for sentence in selected_sentences:
            # Generate different types of questions
            question_type = random.choice(['what', 'who', 'when', 'where', 'why', 'how'])
            
            # Simple question generation based on sentence structure
            if 'is' in sentence.lower() or 'are' in sentence.lower():
                if question_type == 'what':
                    question = f"What {sentence.lower()}?"
                elif question_type == 'who' and any(name in sentence for name in ['Mr.', 'Ms.', 'Dr.', 'President']):
                    question = f"Who {sentence.lower()}?"
                else:
                    question = f"What can you tell me about the following: {sentence}?"
            else:
                question_starters = self.question_patterns.get(question_type, ['What'])
                starter = random.choice(question_starters)
                question = f"{starter} mentioned in this statement: {sentence}?"
            
            qa_pair = {
                'type': 'qa_pair',
                'question': question,
                'answer': sentence,
                'category': question_type
            }
            qa_pairs.append(qa_pair)
        
        return qa_pairs
    
    def generate_definition_cards(self, text: str, num_cards: int = 5) -> List[Dict[str, str]]:
        """Generate definition-style flashcards."""
        # Look for definition patterns
        definition_patterns = [
            r'([A-Z][^.]*?)\s+is\s+([^.]+\.)',
            r'([A-Z][^.]*?)\s+are\s+([^.]+\.)',
            r'([A-Z][^.]*?)\s+refers to\s+([^.]+\.)',
            r'([A-Z][^.]*?)\s+means\s+([^.]+\.)',
            r'([A-Z][^.]*?):\s+([^.]+\.)'
        ]
        
        definition_cards = []
        
        for pattern in definition_patterns:
            matches = re.findall(pattern, text)
            for term, definition in matches:
                if len(definition_cards) >= num_cards:
                    break
                
                card = {
                    'type': 'definition',
                    'question': f"Define: {term.strip()}",
                    'answer': definition.strip(),
                    'term': term.strip()
                }
                definition_cards.append(card)
        
        return definition_cards

def generate_flashcards(text: str, num_cards: int = 15) -> List[Dict[str, str]]:
    """
    Generate a variety of flashcards from the input text.
    
    Args:
        text (str): Input text to generate flashcards from
        num_cards (int): Total number of flashcards to generate
        
    Returns:
        List[Dict[str, str]]: List of flashcard dictionaries
    """
    if not text or len(text.strip()) < 50:
        return [{'type': 'error', 'question': 'Error', 'answer': 'Text too short to generate flashcards'}]
    
    generator = FlashcardGenerator()
    
    # Distribute cards across different types
    fill_blank_count = num_cards // 2
    qa_count = num_cards // 3
    definition_count = num_cards - fill_blank_count - qa_count
    
    flashcards = []
    
    try:
        # Generate fill-in-the-blank cards
        fill_blank_cards = generator.generate_fill_in_blank(text, fill_blank_count)
        flashcards.extend(fill_blank_cards)
        
        # Generate Q&A pairs
        qa_cards = generator.generate_qa_pairs(text, qa_count)
        flashcards.extend(qa_cards)
        
        # Generate definition cards
        definition_cards = generator.generate_definition_cards(text, definition_count)
        flashcards.extend(definition_cards)
        
        # Shuffle the cards
        random.shuffle(flashcards)
        
        return flashcards[:num_cards]
        
    except Exception as e:
        return [{'type': 'error', 'question': 'Error', 'answer': f'Error generating flashcards: {str(e)}'}]

def generate_quiz(text: str, num_questions: int = 10) -> List[Dict[str, any]]:
    """
    Generate a multiple-choice quiz from the text.
    
    Args:
        text (str): Input text
        num_questions (int): Number of questions to generate
        
    Returns:
        List[Dict]: List of quiz questions with multiple choices
    """
    if not text or len(text.strip()) < 50:
        return [{'question': 'Error: Text too short to generate quiz', 'options': [], 'correct': 0}]
    
    generator = FlashcardGenerator()
    sentences = [s.strip() for s in re.split(r'[.!?]+', text) if len(s.strip()) > 15]
    
    if len(sentences) < num_questions:
        num_questions = len(sentences)
    
    quiz_questions = []
    used_sentences = set()
    
    for _ in range(num_questions):
        # Select a sentence that hasn't been used
        available_sentences = [s for s in sentences if s not in used_sentences]
        if not available_sentences:
            break
            
        sentence = random.choice(available_sentences)
        used_sentences.add(sentence)
        
        # Extract key concepts for multiple choice options
        concepts = generator.extract_key_concepts(sentence)
        
        if len(concepts) >= 3:
            correct_answer = random.choice(concepts)
            
            # Create distractors (wrong answers)
            all_concepts = generator.extract_key_concepts(text)
            distractors = [c for c in all_concepts if c != correct_answer]
            random.shuffle(distractors)
            
            # Create question by blanking out the correct answer
            question_text = sentence.replace(correct_answer, "______")
            
            # Build options
            options = [correct_answer] + distractors[:3]
            random.shuffle(options)
            correct_index = options.index(correct_answer)
            
            quiz_question = {
                'question': f"Fill in the blank: {question_text}",
                'options': options,
                'correct': correct_index,
                'explanation': sentence
            }
            quiz_questions.append(quiz_question)
    
    return quiz_questions
