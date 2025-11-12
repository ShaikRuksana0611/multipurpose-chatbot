import nltk
import string
from nltk.stem import WordNetLemmatizer
import re

class TextPreprocessor:
    def __init__(self):
        nltk.download('punkt', quiet=True)
        nltk.download('wordnet', quiet=True)
        self.lemmatizer = WordNetLemmatizer()
    
    def process(self, text):
        """Full text preprocessing pipeline"""
        text = self._clean_text(text)
        tokens = self._tokenize(text)
        tokens = self._lemmatize(tokens)
        return ' '.join(tokens)
    
    def _clean_text(self, text):
        """Clean and normalize text"""
        text = text.lower().strip()
        text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
        return text
    
    def _tokenize(self, text):
        """Tokenize text into words"""
        return nltk.word_tokenize(text)
    
    def _lemmatize(self, tokens):
        """Lemmatize tokens"""
        return [self.lemmatizer.lemmatize(token) for token in tokens]