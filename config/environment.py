"""
Environment-specific configuration settings
"""

import os
from typing import Dict, Any

class Environment:
    """Environment configuration handler"""
    
    DEVELOPMENT = 'development'
    PRODUCTION = 'production'
    TESTING = 'testing'
    
    def __init__(self):
        self.current_env = self._detect_environment()
    
    def _detect_environment(self) -> str:
        """Detect the current environment"""
        env = os.getenv('FLASK_ENV', '').lower()
        if env in [self.DEVELOPMENT, self.PRODUCTION, self.TESTING]:
            return env
        
        # Auto-detect based on common patterns
        if os.getenv('PYTHON_ENV'):
            return os.getenv('PYTHON_ENV').lower()
        
        if os.getenv('SERVER_SOFTWARE', '').startswith('gunicorn'):
            return self.PRODUCTION
        
        # Default to development
        return self.DEVELOPMENT
    
    def get_environment_config(self) -> Dict[str, Any]:
        """Get environment-specific configuration overrides"""
        base_config = {}
        
        if self.current_env == self.DEVELOPMENT:
            base_config = {
                'app': {
                    'debug': True,
                    'testing': False
                },
                'logging': {
                    'level': 'DEBUG'
                },
                'security': {
                    'cors_origins': ['*']
                }
            }
        
        elif self.current_env == self.PRODUCTION:
            base_config = {
                'app': {
                    'debug': False,
                    'testing': False
                },
                'logging': {
                    'level': 'WARNING'
                },
                'security': {
                    'cors_origins': ['https://yourdomain.com']
                }
            }
        
        elif self.current_env == self.TESTING:
            base_config = {
                'app': {
                    'debug': False,
                    'testing': True
                },
                'data': {
                    'data_file': 'backend/data/test_chatbot_data.json'
                },
                'logging': {
                    'level': 'CRITICAL'
                }
            }
        
        return base_config
    
    def is_development(self) -> bool:
        return self.current_env == self.DEVELOPMENT
    
    def is_production(self) -> bool:
        return self.current_env == self.PRODUCTION
    
    def is_testing(self) -> bool:
        return self.current_env == self.TESTING
    
    def get_current(self) -> str:
        return self.current_env

# Global environment instance
_env_instance = None

def get_environment() -> Environment:
    """Get environment instance"""
    global _env_instance
    if _env_instance is None:
        _env_instance = Environment()
    return _env_instance