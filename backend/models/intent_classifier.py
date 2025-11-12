"""
Intent Classifier for Multi-Purpose Chatbot
Uses TF-IDF and cosine similarity for intent classification
"""

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import logging
from typing import Tuple, Dict, Any, List
import joblib
import os

class IntentClassifier:
    """
    Classifies user intents using TF-IDF and cosine similarity
    """
    
    def __init__(self, max_features: int = 5000, min_confidence: float = 0.3):
        """
        Initialize the intent classifier
        
        Args:
            max_features: Maximum number of features for TF-IDF
            min_confidence: Minimum confidence threshold for classification
        """
        self.logger = logging.getLogger(__name__)
        self.max_features = max_features
        self.min_confidence = min_confidence
        
        self.vectorizer = TfidfVectorizer(
            analyzer='word',
            stop_words='english',
            max_features=max_features,
            lowercase=True,
            ngram_range=(1, 2)
        )
        
        self.trained = False
        self.patterns: List[str] = []
        self.tags: List[Dict[str, str]] = []
        self.X = None
        
        self.logger.info("Intent Classifier initialized")
    
    def train(self, training_data: Dict[str, Any]) -> bool:
        """
        Train the intent classification model
        
        Args:
            training_data: Training data dictionary
            
        Returns:
            True if training successful, False otherwise
        """
        try:
            all_patterns = []
            all_tags = []
            
            # Extract patterns and tags from training data
            for app_name, app_data in training_data.get("applications", {}).items():
                patterns = app_data.get("patterns", [])
                tags = app_data.get("tags", [])
                
                if len(patterns) != len(tags):
                    self.logger.warning(f"Patterns and tags count mismatch for {app_name}")
                    continue
                
                all_patterns.extend(patterns)
                all_tags.extend([{"application": app_name, "tag": tag} for tag in tags])
            
            if not all_patterns:
                self.logger.error("No training patterns found")
                return False
            
            self.patterns = all_patterns
            self.tags = all_tags
            
            # Fit TF-IDF vectorizer
            self.X = self.vectorizer.fit_transform(all_patterns)
            self.trained = True
            
            self.logger.info(f"Model trained with {len(all_patterns)} patterns across {len(training_data.get('applications', {}))} applications")
            return True
            
        except Exception as e:
            self.logger.error(f"Training error: {e}")
            self.trained = False
            return False
    
    def predict(self, text: str, application: str, context: Dict[str, Any] = None) -> Tuple[str, float]:
        """
        Predict intent for given text
        
        Args:
            text: Input text to classify
            application: Current application context
            context: User context for contextual classification
            
        Returns:
            Tuple of (intent_tag, confidence_score)
        """
        if not self.trained:
            self.logger.warning("Model not trained, returning default intent")
            return "unknown", 0.0
        
        try:
            # Vectorize input text
            text_vector = self.vectorizer.transform([text])
            
            # Calculate similarity scores
            similarities = cosine_similarity(text_vector, self.X)
            best_match_idx = np.argmax(similarities)
            confidence = similarities[0, best_match_idx]
            
            # Apply confidence threshold
            if confidence >= self.min_confidence:
                best_tag_info = self.tags[best_match_idx]
                
                # Consider application context in scoring
                contextual_confidence = self._apply_context_scoring(
                    confidence, best_tag_info, application, context
                )
                
                # Return the tag from the best matching pattern
                return best_tag_info["tag"], contextual_confidence
            else:
                return "unknown", confidence
                
        except Exception as e:
            self.logger.error(f"Prediction error: {e}")
            return "unknown", 0.0
    
    def _apply_context_scoring(self, confidence: float, tag_info: Dict[str, str], 
                             application: str, context: Dict[str, Any]) -> float:
        """
        Apply context-based scoring adjustments
        
        Args:
            confidence: Original confidence score
            tag_info: Tag information
            application: Current application
            context: User context
            
        Returns:
            Adjusted confidence score
        """
        adjusted_confidence = confidence
        
        # Boost confidence if tag matches current application
        if tag_info["application"] == application:
            adjusted_confidence *= 1.1  # 10% boost
            adjusted_confidence = min(adjusted_confidence, 1.0)  # Cap at 1.0
        
        # Consider conversation history if available
        if context and 'conversation_history' in context:
            history = context['conversation_history']
            if history:
                # Boost if similar to recent intents
                recent_intents = [msg.get('intent', '') for msg in list(history)[-3:]]
                if tag_info["tag"] in recent_intents:
                    adjusted_confidence *= 1.05  # 5% boost
        
        return adjusted_confidence
    
    def get_similar_intents(self, text: str, top_k: int = 3) -> List[Tuple[str, float]]:
        """
        Get top K similar intents for the given text
        
        Args:
            text: Input text
            top_k: Number of top intents to return
            
        Returns:
            List of (intent_tag, confidence) tuples
        """
        if not self.trained:
            return []
        
        try:
            text_vector = self.vectorizer.transform([text])
            similarities = cosine_similarity(text_vector, self.X)
            
            # Get top K indices
            top_indices = np.argsort(similarities[0])[-top_k:][::-1]
            
            results = []
            for idx in top_indices:
                if similarities[0, idx] > 0:
                    tag_info = self.tags[idx]
                    results.append((tag_info["tag"], float(similarities[0, idx])))
            
            return results
            
        except Exception as e:
            self.logger.error(f"Error getting similar intents: {e}")
            return []
    
    def retrain(self, new_data: Dict[str, Any]) -> bool:
        """
        Retrain model with new data
        
        Args:
            new_data: New training data
            
        Returns:
            True if retraining successful, False otherwise
        """
        self.logger.info("Retraining model with new data...")
        return self.train(new_data)
    
    def save_model(self, filepath: str) -> bool:
        """
        Save trained model to file
        
        Args:
            filepath: Path to save the model
            
        Returns:
            True if save successful, False otherwise
        """
        try:
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            
            model_data = {
                'vectorizer': self.vectorizer,
                'patterns': self.patterns,
                'tags': self.tags,
                'X': self.X,
                'trained': self.trained
            }
            
            joblib.dump(model_data, filepath)
            self.logger.info(f"Model saved to {filepath}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error saving model: {e}")
            return False
    
    def load_model(self, filepath: str) -> bool:
        """
        Load trained model from file
        
        Args:
            filepath: Path to load the model from
            
        Returns:
            True if load successful, False otherwise
        """
        try:
            if not os.path.exists(filepath):
                self.logger.warning(f"Model file not found: {filepath}")
                return False
            
            model_data = joblib.load(filepath)
            
            self.vectorizer = model_data['vectorizer']
            self.patterns = model_data['patterns']
            self.tags = model_data['tags']
            self.X = model_data['X']
            self.trained = model_data['trained']
            
            self.logger.info(f"Model loaded from {filepath}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error loading model: {e}")
            return False
    
    def get_model_info(self) -> Dict[str, Any]:
        """
        Get information about the current model
        
        Returns:
            Model information dictionary
        """
        return {
            'trained': self.trained,
            'pattern_count': len(self.patterns),
            'applications': list(set(tag_info['application'] for tag_info in self.tags)),
            'feature_count': self.vectorizer.get_feature_names_out().shape[0] if self.trained else 0,
            'min_confidence': self.min_confidence
        }