"""
Configuration loader for Multi-Purpose Chatbot
"""

import os
import yaml
from typing import Dict, Any, Optional
import logging

class Config:
    """Configuration class for the chatbot application"""
    
    def __init__(self):
        self._config = self._load_configuration()
    
    def _load_configuration(self) -> Dict[str, Any]:
        """Load configuration from multiple sources with fallbacks"""
        # Default configuration
        default_config = {
            'app': {
                'name': 'Multi-Purpose Chatbot',
                'version': '1.0.0',
                'debug': True,
                'secret_key': 'dev-key-change-in-production'
            },
            'server': {
                'host': '0.0.0.0',
                'port': 5000,
                'workers': 4
            },
            'chatbot': {
                'confidence_threshold': 0.3,
                'max_context_length': 10,
                'response_timeout': 30,
                'applications': [
                    'customer_support',
                    'college_helpdesk', 
                    'hr_recruitment',
                    'personal_assistant'
                ]
            },
            'nlp': {
                'max_features': 5000,
                'stop_words': 'english',
                'min_pattern_length': 2
            },
            'data': {
                'data_file': 'backend/data/chatbot_data.json',
                'models_dir': 'backend/data/models/',
                'backup_dir': 'backend/data/backups/'
            },
            'logging': {
                'level': 'INFO',
                'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                'file': 'backend/logs/chatbot.log',
                'max_file_size': 10485760,
                'backup_count': 5
            },
            'security': {
                'cors_origins': ['*'],
                'rate_limit_per_minute': 100,
                'api_key_required': False
            }
        }
        
        return default_config
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value using dot notation"""
        keys = key.split('.')
        value = self._config
        
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default

# Global configuration instance
_config_instance = None

def load_config() -> Config:
    """Load and return configuration instance"""
    global _config_instance
    if _config_instance is None:
        _config_instance = Config()
    return _config_instance

def get_config(key: str = None, default: Any = None) -> Any:
    """Get configuration value or entire config"""
    config = load_config()
    if key is None:
        return config._config
    return config.get(key, default)