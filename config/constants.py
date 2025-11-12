"""
Application constants
"""

# Application Constants
APP_NAME = "Multi-Purpose Chatbot"
APP_VERSION = "1.0.0"
SUPPORTED_LANGUAGES = ['en', 'es', 'fr', 'de']

# Chatbot Applications
APPLICATIONS = {
    'customer_support': {
        'name': 'Customer Support',
        'description': 'Order tracking, returns, technical support',
        'icon': '🏪'
    },
    'college_helpdesk': {
        'name': 'College Helpdesk', 
        'description': 'Admissions, courses, campus information',
        'icon': '🎓'
    },
    'hr_recruitment': {
        'name': 'HR Recruitment',
        'description': 'Job openings, interviews, company info',
        'icon': '💼'
    },
    'personal_assistant': {
        'name': 'Personal Assistant',
        'description': 'Time, reminders, jokes, calculations',
        'icon': '⏰'
    }
}

# NLP Constants
DEFAULT_CONFIDENCE_THRESHOLD = 0.3
MAX_INPUT_LENGTH = 500
MIN_INPUT_LENGTH = 1

# Response Constants
DEFAULT_RESPONSES = {
    'unknown': [
        "I'm not sure I understand. Could you rephrase that?",
        "That's an interesting question. Let me think about how to help you.",
        "I'm still learning. Could you try asking that differently?",
        "I don't have an answer for that right now. Try asking something else!"
    ],
    'greeting': [
        "Hello! How can I help you today?",
        "Hi there! What can I assist you with?",
        "Hey! Nice to see you. How can I help?"
    ],
    'farewell': [
        "Goodbye! Have a great day!",
        "See you later! Take care!",
        "Bye! Feel free to come back if you have more questions!"
    ]
}

# Error Messages
ERROR_MESSAGES = {
    'invalid_input': "Please provide a valid message.",
    'server_error': "I'm experiencing technical difficulties. Please try again later.",
    'timeout': "The request took too long. Please try again.",
    'training_failed': "Failed to add training data. Please check the inputs."
}

# API Constants
MAX_MESSAGE_LENGTH = 1000
MAX_TRAINING_PATTERNS = 1000
RATE_LIMIT_REQUESTS = 100
RATE_LIMIT_WINDOW = 60  # seconds

# File Constants
SUPPORTED_FILE_TYPES = ['.json', '.yaml', '.yml']
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

# UI Constants
THEMES = ['default', 'dark', 'light', 'professional']
DEFAULT_THEME = 'default'