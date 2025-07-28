"""
Flashcard and quiz-question generation utilities.

Approach:
1. Keyword extraction → candidate concepts
2. Cloze (fill-in-the-blank) or Q&A templates
3. Simple randomness for variety
"""
from __future__ import annotations

import random
import re
from typing import List

import nltk
from transformers import pipeline

# Ensure NLTK resources are present once per session
nltk.download("punkt", quiet=True)
nltk.download("averaged_perceptron_tagger", quiet=True)
nltk.download("words", quiet=True)

_qa_model = pipeline("question-generation")


def _split_sentences(text: str) -> List[str]:
    return nltk.sent_tokenize(text)


def _extract_keywords(sentence: str, top_n: int = 2) -> List[str]:
    """Naïve noun extraction as keyword proxy."""
    tokens = nltk.word_tokenize(sentence)
    tagged = nltk.pos_tag(tokens)
    nouns = [word for word, tag in tagged if tag.startswith("NN")]
    return nouns[:top_n]


def _make_cloze(sentence: str, keyword: str) -> str:
    """Replace the keyword with a blank."""
    blank = "_____"  # could adjust length
    pattern = re.compile(re.escape(keyword), re.IGNORECASE)
    return pattern.sub(blank, sentence, count=1)


def generate_flashcards(text: str, num_cards: int = 10):
    """
    Return a list of {'question', 'answer'} dicts suitable for flashcards.
    """
    sentences = _split_sentences(text)
    random.shuffle(sentences)

    flashcards = []
    for sentence in sentences:
        keywords = _extract_keywords(sentence)
        if not keywords:
            continue
        answer = keywords[0]
        question = _make_cloze(sentence, answer)
        flashcards.append({"question": question, "answer": answer})
        if len(flashcards) >= num_cards:
            break
    return flashcards


def generate_quiz(text: str, num_questions: int = 5):
    """
    Produce multiple-choice questions via a transformer question generator.

    Returns a list of:
    { "question": str, "options": [a,b,c,d], "answer": str }
    """
    sentences = random.sample(_split_sentences(text), k=min(30, len(text)))
    raw_questions = _qa_model(sentences)

    quiz = []
    for item in raw_questions:
        if len(quiz) >= num_questions:
            break
        q, correct = item["question"], item["answer"]
        # fabricate 3 random distractors
        distractors = random.sample(
            [w for w in nltk.corpus.words.words() if w.lower() != correct.lower()],
            k=3
        )
        options = distractors + [correct]
        random.shuffle(options)
        quiz.append({"question": q, "options": options, "answer": correct})
    return quiz
