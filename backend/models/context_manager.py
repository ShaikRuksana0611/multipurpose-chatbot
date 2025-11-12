"""
Context Manager for maintaining conversation context and user state
"""

import json
import time
from datetime import datetime
from typing import Dict, Any, List, Optional
import logging
from collections import deque

class ContextManager:
    """
    Manages conversation context and user state across multiple interactions
    """
    
    def __init__(self, max_context_length: int = 10, session_timeout: int = 3600):
        """
        Initialize the context manager
        
        Args:
            max_context_length: Maximum number of messages to keep in context
            session_timeout: Session timeout in seconds (default 1 hour)
        """
        self.logger = logging.getLogger(__name__)
        self.max_context_length = max_context_length
        self.session_timeout = session_timeout
        
        # In-memory storage for user contexts (in production, use Redis or database)
        self.user_contexts: Dict[str, Dict[str, Any]] = {}
        
        self.logger.info("Context Manager initialized")
    
    def get_context(self, user_id: str) -> Dict[str, Any]:
        """
        Get or create context for a user
        
        Args:
            user_id: Unique identifier for the user
            
        Returns:
            User context dictionary
        """
        self._cleanup_expired_sessions()
        
        if user_id not in self.user_contexts:
            self.user_contexts[user_id] = self._create_new_context(user_id)
        else:
            # Update last activity timestamp
            self.user_contexts[user_id]['last_activity'] = datetime.now().isoformat()
        
        return self.user_contexts[user_id]
    
    def _create_new_context(self, user_id: str) -> Dict[str, Any]:
        """
        Create a new context for a user
        
        Args:
            user_id: Unique identifier for the user
            
        Returns:
            New context dictionary
        """
        return {
            'user_id': user_id,
            'conversation_history': deque(maxlen=self.max_context_length),
            'current_application': 'customer_support',
            'user_name': None,
            'user_preferences': {},
            'session_start': datetime.now().isoformat(),
            'last_activity': datetime.now().isoformat(),
            'message_count': 0,
            'context_variables': {}
        }
    
    def update_context(self, user_id: str, user_input: str, bot_response: str, 
                      intent: str, application: str) -> None:
        """
        Update user context with new conversation exchange
        
        Args:
            user_id: Unique identifier for the user
            user_input: User's message
            bot_response: Bot's response
            intent: Detected intent
            application: Current application context
        """
        context = self.get_context(user_id)
        
        # Update conversation history
        context['conversation_history'].append({
            'timestamp': datetime.now().isoformat(),
            'user_input': user_input,
            'bot_response': bot_response,
            'intent': intent,
            'application': application
        })
        
        # Update current application
        context['current_application'] = application
        
        # Update message count
        context['message_count'] += 1
        
        # Extract and store user name if mentioned
        self._extract_user_name(context, user_input)
        
        # Update context variables based on conversation
        self._update_context_variables(context, user_input, intent)
        
        self.logger.debug(f"Updated context for user {user_id}: {intent} in {application}")
    
    def _extract_user_name(self, context: Dict[str, Any], user_input: str) -> None:
        """
        Extract and store user name from conversation
        
        Args:
            context: User context
            user_input: User's message
        """
        user_input_lower = user_input.lower()
        
        # Check for name introduction patterns
        name_patterns = [
            "my name is",
            "i'm called",
            "i am",
            "call me",
            "you can call me"
        ]
        
        for pattern in name_patterns:
            if pattern in user_input_lower:
                # Extract name after the pattern
                name_start = user_input_lower.find(pattern) + len(pattern)
                potential_name = user_input[name_start:].strip()
                
                # Clean up the name (remove punctuation, take first word)
                name = potential_name.split()[0] if potential_name.split() else None
                if name and len(name) > 1:  # Basic validation
                    context['user_name'] = name
                    self.logger.info(f"Extracted user name: {name}")
                break
    
    def _update_context_variables(self, context: Dict[str, Any], user_input: str, intent: str) -> None:
        """
        Update context variables based on user input and intent
        
        Args:
            context: User context
            user_input: User's message
            intent: Detected intent
        """
        user_input_lower = user_input.lower()
        
        # Example: Track if user is having issues
        if any(word in user_input_lower for word in ['problem', 'issue', 'error', 'not working']):
            context['context_variables']['has_issues'] = True
        
        # Example: Track if user is asking about specific topics
        if 'order' in user_input_lower:
            context['context_variables']['discussing_orders'] = True
        
        # Example: Track user sentiment keywords
        positive_words = ['great', 'good', 'excellent', 'thanks', 'thank you', 'awesome']
        negative_words = ['bad', 'terrible', 'awful', 'horrible', 'disappointed']
        
        for word in positive_words:
            if word in user_input_lower:
                context['context_variables']['last_sentiment'] = 'positive'
                break
        
        for word in negative_words:
            if word in user_input_lower:
                context['context_variables']['last_sentiment'] = 'negative'
                break
    
    def get_conversation_history(self, user_id: str, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Get conversation history for a user
        
        Args:
            user_id: Unique identifier for the user
            limit: Maximum number of history items to return
            
        Returns:
            List of conversation history items
        """
        context = self.get_context(user_id)
        history = list(context['conversation_history'])
        
        if limit and limit > 0:
            return history[-limit:]
        
        return history
    
    def get_user_preference(self, user_id: str, preference_key: str, default: Any = None) -> Any:
        """
        Get user preference
        
        Args:
            user_id: Unique identifier for the user
            preference_key: Preference key to retrieve
            default: Default value if preference not found
            
        Returns:
            Preference value
        """
        context = self.get_context(user_id)
        return context['user_preferences'].get(preference_key, default)
    
    def set_user_preference(self, user_id: str, preference_key: str, value: Any) -> None:
        """
        Set user preference
        
        Args:
            user_id: Unique identifier for the user
            preference_key: Preference key to set
            value: Preference value
        """
        context = self.get_context(user_id)
        context['user_preferences'][preference_key] = value
        self.logger.debug(f"Set preference {preference_key} for user {user_id}")
    
    def switch_application(self, user_id: str, application: str) -> None:
        """
        Switch user to a different application context
        
        Args:
            user_id: Unique identifier for the user
            application: New application context
        """
        context = self.get_context(user_id)
        old_application = context['current_application']
        context['current_application'] = application
        
        self.logger.info(f"User {user_id} switched from {old_application} to {application}")
    
    def get_context_summary(self, user_id: str) -> Dict[str, Any]:
        """
        Get a summary of user context
        
        Args:
            user_id: Unique identifier for the user
            
        Returns:
            Context summary
        """
        context = self.get_context(user_id)
        
        return {
            'user_id': context['user_id'],
            'user_name': context['user_name'],
            'current_application': context['current_application'],
            'message_count': context['message_count'],
            'session_duration': self._get_session_duration(context),
            'recent_intents': [msg['intent'] for msg in list(context['conversation_history'])[-3:]],
            'has_issues': context['context_variables'].get('has_issues', False),
            'last_sentiment': context['context_variables'].get('last_sentiment', 'neutral')
        }
    
    def _get_session_duration(self, context: Dict[str, Any]) -> int:
        """
        Calculate session duration in seconds
        
        Args:
            context: User context
            
        Returns:
            Session duration in seconds
        """
        session_start = datetime.fromisoformat(context['session_start'])
        now = datetime.now()
        return int((now - session_start).total_seconds())
    
    def _cleanup_expired_sessions(self) -> None:
        """
        Clean up expired user sessions to prevent memory leaks
        """
        current_time = datetime.now()
        expired_users = []
        
        for user_id, context in self.user_contexts.items():
            last_activity = datetime.fromisoformat(context['last_activity'])
            session_age = (current_time - last_activity).total_seconds()
            
            if session_age > self.session_timeout:
                expired_users.append(user_id)
        
        for user_id in expired_users:
            del self.user_contexts[user_id]
            self.logger.info(f"Cleaned up expired session for user {user_id}")
    
    def clear_context(self, user_id: str) -> bool:
        """
        Clear context for a specific user
        
        Args:
            user_id: Unique identifier for the user
            
        Returns:
            True if context was cleared, False if user not found
        """
        if user_id in self.user_contexts:
            del self.user_contexts[user_id]
            self.logger.info(f"Cleared context for user {user_id}")
            return True
        return False
    
    def get_all_active_sessions(self) -> List[Dict[str, Any]]:
        """
        Get information about all active sessions
        
        Returns:
            List of active session information
        """
        self._cleanup_expired_sessions()
        
        active_sessions = []
        for user_id, context in self.user_contexts.items():
            active_sessions.append({
                'user_id': user_id,
                'user_name': context['user_name'],
                'current_application': context['current_application'],
                'message_count': context['message_count'],
                'session_duration': self._get_session_duration(context),
                'last_activity': context['last_activity']
            })
        
        return active_sessions
    
    def export_context(self, user_id: str) -> Optional[Dict[str, Any]]:
        """
        Export user context for persistence
        
        Args:
            user_id: Unique identifier for the user
            
        Returns:
            Context data or None if user not found
        """
        if user_id in self.user_contexts:
            # Convert deque to list for JSON serialization
            context = self.user_contexts[user_id].copy()
            context['conversation_history'] = list(context['conversation_history'])
            return context
        return None
    
    def import_context(self, user_id: str, context_data: Dict[str, Any]) -> bool:
        """
        Import user context from persisted data
        
        Args:
            user_id: Unique identifier for the user
            context_data: Context data to import
            
        Returns:
            True if import successful, False otherwise
        """
        try:
            # Convert list back to deque
            if 'conversation_history' in context_data:
                context_data['conversation_history'] = deque(
                    context_data['conversation_history'], 
                    maxlen=self.max_context_length
                )
            
            self.user_contexts[user_id] = context_data
            self.logger.info(f"Imported context for user {user_id}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to import context for user {user_id}: {e}")
            return False