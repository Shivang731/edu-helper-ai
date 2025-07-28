import re
import random
from typing import List, Dict

def generate_flashcards(text: str, num_cards: int = 5) -> List[Dict[str, str]]:
    """Generate flashcards from text."""
    
    if not text or text.strip() == "":
        return []
    
    # Split text into sentences
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 30]
    
    if not sentences:
        return []
    
    flashcards = []
    
    # Generate different types of flashcards
    for i in range(min(num_cards, len(sentences))):
        sentence = sentences[i]
        
        if i % 2 == 0:
            # Cloze deletion cards
            card = _create_cloze_card(sentence)
        else:
            # Definition cards
            card = _create_definition_card(sentence)
        
        if card:
            flashcards.append(card)
    
    return flashcards

def _create_cloze_card(sentence: str) -> Dict[str, str]:
    """Create a cloze deletion flashcard."""
    words = sentence.split()
    if len(words) < 6:
        return None
    
    # Find important words to blank out (nouns, adjectives, etc.)
    # Simple heuristic: words that are longer or capitalized
    important_words = []
    for i, word in enumerate(words):
        clean_word = re.sub(r'[^\w]', '', word)
        if len(clean_word) > 4 or word[0].isupper():
            important_words.append((i, word, clean_word))
    
    if not important_words:
        # Fallback: use middle word
        middle_idx = len(words) // 2
        important_words = [(middle_idx, words[middle_idx], re.sub(r'[^\w]', '', words[middle_idx]))]
    
    # Choose a random important word
    word_idx, original_word, clean_word = random.choice(important_words)
    
    # Create the cloze
    cloze_sentence = words.copy()
    cloze_sentence[word_idx] = "_____"
    
    return {
        "front": " ".join(cloze_sentence),
        "back": clean_word,
        "type": "cloze"
    }

def _create_definition_card(sentence: str) -> Dict[str, str]:
    """Create a definition-style flashcard."""
    # Look for patterns like "X is Y" or "X refers to Y"
    
    # Pattern 1: "X is Y"
    is_match = re.search(r'^([^,]+)\s+is\s+(.+)$', sentence, re.IGNORECASE)
    if is_match:
        term = is_match.group(1).strip()
        definition = is_match.group(2).strip()
        return {
            "front": f"What is {term}?",
            "back": definition,
            "type": "definition"
        }
    
    # Pattern 2: "X refers to Y"
    refers_match = re.search(r'^([^,]+)\s+refers?\s+to\s+(.+)$', sentence, re.IGNORECASE)
    if refers_match:
        term = refers_match.group(1).strip()
        definition = refers_match.group(2).strip()
        return {
            "front": f"What does {term} refer to?",
            "back": definition,
            "type": "definition"
        }
    
    # Pattern 3: "X includes Y" or "X contains Y"
    includes_match = re.search(r'^([^,]+)\s+(includes?|contains?)\s+(.+)$', sentence, re.IGNORECASE)
    if includes_match:
        term = includes_match.group(1).strip()
        content = includes_match.group(3).strip()
        return {
            "front": f"What does {term} include?",
            "back": content,
            "type": "definition"
        }
    
    # Fallback: use the whole sentence as a Q&A
    if len(sentence) > 50:
        # Take first part as question context, last part as answer
        parts = sentence.split(',')
        if len(parts) >= 2:
            question_part = parts[0].strip()
            answer_part = ', '.join(parts[1:]).strip()
            
            return {
                "front": f"Complete: {question_part}...",
                "back": answer_part,
                "type": "completion"
            }
    
    return None

def generate_quiz(text: str, num_questions: int = 3) -> List[Dict]:
    """Generate multiple choice quiz questions."""
    
    flashcards = generate_flashcards(text, num_questions * 2)
    quiz_questions = []
    
    for card in flashcards[:num_questions]:
        if card['type'] == 'cloze':
            # Convert cloze to multiple choice
            question = {
                "question": card['front'].replace("_____", "______"),
                "correct_answer": card['back'],
                "options": [card['back']],
                "type": "multiple_choice"
            }
            
            # Add dummy options (this is a simple implementation)
            dummy_options = ["option A", "option B", "option C"]
            question["options"].extend(dummy_options[:3])
            random.shuffle(question["options"])
            
            quiz_questions.append(question)
    
    return quiz_questions
