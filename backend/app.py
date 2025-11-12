from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import random
import json
import os
import re
from datetime import datetime
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Get the project root directory
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES_DIR = os.path.join(PROJECT_ROOT, 'frontend', 'templates')
STATIC_DIR = os.path.join(PROJECT_ROOT, 'frontend', 'static')

print(f"📁 Project root: {PROJECT_ROOT}")
print(f"📁 Templates directory: {TEMPLATES_DIR}")
print(f"📁 Static directory: {STATIC_DIR}")

# Simple text preprocessing without NLTK
class SimpleTextPreprocessor:
    def preprocess_text(self, text):
        """Basic text preprocessing without NLTK"""
        if not text:
            return ""
        
        # Convert to lowercase and remove punctuation
        text = text.lower()
        text = re.sub(r'[^\w\s]', '', text)
        
        # Simple tokenization
        words = text.split()
        
        # Basic lemmatization replacements
        lemmatization_map = {
            'are': 'be', 'am': 'be', 'is': 'be', 'was': 'be', 'were': 'be',
            'running': 'run', 'ran': 'run', 'runs': 'run',
            'going': 'go', 'went': 'go', 'goes': 'go',
            'having': 'have', 'had': 'have', 'has': 'have',
            'doing': 'do', 'did': 'do', 'does': 'do',
            'saying': 'say', 'said': 'say', 'says': 'say',
            'orders': 'order', 'ordered': 'order',
            'returns': 'return', 'returned': 'return',
            'problems': 'problem', 'issues': 'issue'
        }
        
        processed_words = [lemmatization_map.get(word, word) for word in words]
        return ' '.join(processed_words)

# Simple chatbot without scikit-learn
class SimpleChatbot:
    def __init__(self):
        self.preprocessor = SimpleTextPreprocessor()
        self.conversation_context = {}
        
        # Simple pattern matching data
        self.pattern_responses = self._load_pattern_responses()
        logger.info("✅ Simple Chatbot initialized successfully")
    
    def _load_pattern_responses(self):
        """Load pattern-response mappings"""
        return {
            "customer_support": {
                "patterns": [
                    (["hello", "hi", "hey"], ["Hello! How can I help with customer support today?", "Hi there! What can I assist you with today?"]),
                    (["order", "status", "track", "package"], ["I can help you track your order. Do you have an order number?", "For order status, I'll need your order number."]),
                    (["return", "refund", "cancel"], ["Our return policy allows returns within 30 days. Can you tell me more about your situation?", "I can help with returns and refunds. What would you like to return?"]),
                    (["problem", "issue", "broken", "not working", "defective"], ["I'm sorry you're having issues. Let me help you troubleshoot the problem.", "I can help with technical issues. What seems to be the problem?"]),
                    (["shipping", "delivery", "when", "arrive"], ["I can check shipping status for you. What's your order number?", "For delivery information, I'll need your order details."]),
                    (["payment", "billing", "charge", "credit card"], ["I can help with payment issues. What seems to be the problem?", "For billing questions, I'll need more information about the charge."])
                ]
            },
            "college_helpdesk": {
                "patterns": [
                    (["admission", "apply", "application", "requirements"], ["Admission requirements include a completed application and transcripts.", "The application deadline for fall semester is August 1st."]),
                    (["tuition", "fees", "scholarship", "financial", "aid"], ["Tuition fees vary by program. I can check specific costs for you.", "We offer various scholarships based on academic performance."]),
                    (["course", "register", "class", "schedule"], ["Course registration opens two weeks before each semester.", "You can check the class schedule on our student portal."]),
                    (["campus", "library", "facility", "hours"], ["The library is open from 8 AM to 10 PM on weekdays.", "Most campus facilities are open from 7 AM to 10 PM."])
                ]
            },
            "hr_recruitment": {
                "patterns": [
                    (["job", "opening", "vacancy", "career", "position"], ["We have openings in engineering, marketing, and sales departments.", "You can view all current openings on our careers page."]),
                    (["apply", "application", "resume", "cv"], ["You can apply through our careers portal with your resume.", "The application process typically takes 2-3 weeks."]),
                    (["interview", "process", "hiring", "stage"], ["Our interview process typically includes 3-4 stages.", "The hiring process includes resume screening and multiple interviews."]),
                    (["salary", "compensation", "benefit", "pay"], ["Salary ranges are competitive and based on experience.", "We offer comprehensive health benefits and retirement plans."])
                ]
            },
            "personal_assistant": {
                "patterns": [
                    (["time", "current", "clock"], [f"The current time is {datetime.now().strftime('%H:%M')}.", f"It's currently {datetime.now().strftime('%I:%M %p')}."]),
                    (["weather", "forecast", "rain", "temperature"], ["I recommend checking a weather app for current conditions.", "For accurate weather information, try a dedicated weather service."]),
                    (["remind", "reminder", "schedule", "meeting"], ["I can help you set reminders. What should I remind you about?", "For scheduling, you can use calendar apps like Google Calendar."]),
                    (["joke", "funny", "laugh", "humor"], ["Why don't scientists trust atoms? Because they make up everything!", "Why did the scarecrow win an award? He was outstanding in his field!"])
                ]
            }
        }
    
    def get_response(self, user_input, user_id, application="customer_support"):
        """Get response using simple pattern matching"""
        try:
            if not user_input or not user_input.strip():
                return {
                    "response": "Please type a message so I can help you!",
                    "confidence": 0.0,
                    "application": application,
                    "context_used": False
                }
            
            # Initialize user context
            if user_id not in self.conversation_context:
                self.conversation_context[user_id] = {
                    "conversation_history": [],
                    "current_application": application,
                    "user_name": None
                }
            
            # Preprocess input
            processed_input = self.preprocessor.preprocess_text(user_input)
            
            # Get application patterns
            app_patterns = self.pattern_responses.get(application, {}).get("patterns", [])
            
            # Find best matching pattern
            best_response = None
            best_confidence = 0.0
            
            for pattern_group, responses in app_patterns:
                match_count = sum(1 for pattern in pattern_group if pattern in processed_input)
                confidence = match_count / len(pattern_group) if pattern_group else 0
                
                if confidence > best_confidence:
                    best_confidence = confidence
                    best_response = random.choice(responses)
            
            # Fallback responses
            if not best_response or best_confidence < 0.3:
                fallbacks = {
                    "customer_support": [
                        "I'm here to help with customer support. How can I assist you today?",
                        "For customer support, I can help with orders, returns, and technical issues. What do you need help with?",
                        "I specialize in customer service. Tell me about your concern."
                    ],
                    "college_helpdesk": [
                        "I can help with college information, admissions, and campus services. What would you like to know?",
                        "As a college helpdesk assistant, I can answer questions about admissions, courses, and campus life.",
                        "How can I assist you with college-related matters today?"
                    ],
                    "hr_recruitment": [
                        "I can help with job openings, applications, and company information. What would you like to know?",
                        "For HR and recruitment questions, I'm here to help. What information are you looking for?",
                        "I specialize in career and employment information. How can I assist you?"
                    ],
                    "personal_assistant": [
                        "I can help with time, reminders, and general information. What do you need?",
                        "As your personal assistant, I can provide information and help with various tasks.",
                        "How can I assist you today?"
                    ]
                }
                best_response = random.choice(fallbacks.get(application, ["How can I help you today?"]))
                best_confidence = 0.1
            
            # Extract user name if mentioned
            if "my name is" in user_input.lower():
                name_start = user_input.lower().find("my name is") + 10
                potential_name = user_input[name_start:].strip().split()[0]
                if len(potential_name) > 1:
                    self.conversation_context[user_id]["user_name"] = potential_name
                    best_response = f"Nice to meet you, {potential_name}! {best_response}"
            
            # Personalize response if we know user's name
            elif self.conversation_context[user_id]["user_name"]:
                name = self.conversation_context[user_id]["user_name"]
                if any(word in processed_input for word in ["how", "what", "when", "where"]):
                    best_response = f"{best_response} By the way, {name}!"
            
            # Update context
            self.conversation_context[user_id]["conversation_history"].append({
                "user": user_input,
                "bot": best_response,
                "timestamp": datetime.now().isoformat(),
                "application": application
            })
            
            # Keep only last 5 messages
            if len(self.conversation_context[user_id]["conversation_history"]) > 5:
                self.conversation_context[user_id]["conversation_history"] = \
                    self.conversation_context[user_id]["conversation_history"][-5:]
            
            context_used = len(self.conversation_context[user_id]["conversation_history"]) > 1
            
            return {
                "response": best_response,
                "confidence": best_confidence,
                "application": application,
                "context_used": context_used
            }
            
        except Exception as e:
            logger.error(f"Error in get_response: {e}")
            return {
                "response": "I apologize, but I'm having trouble right now. Please try again.",
                "confidence": 0.0,
                "application": application,
                "context_used": False
            }

def create_app():
    """Create and configure Flask app with correct template paths"""
    # Create Flask app with explicit template and static folders
    app = Flask(__name__, 
                template_folder=TEMPLATES_DIR,
                static_folder=STATIC_DIR)
    
    # Basic configuration
    app.config.update(
        SECRET_KEY='dev-key-123',
        DEBUG=True
    )
    
    # Enable CORS
    CORS(app)
    
    # Initialize chatbot
    chatbot = SimpleChatbot()
    
    @app.route('/')
    def index():
        return render_template('index.html')
    
    @app.route('/api/chat', methods=['POST'])
    def chat():
        try:
            data = request.get_json()
            if not data:
                return jsonify({"error": "No JSON data provided"}), 400
                
            user_input = data.get('message', '').strip()
            user_id = data.get('user_id', 'default_user')
            application = data.get('application', 'customer_support')
            
            if not user_input:
                return jsonify({"error": "No message provided"}), 400
            
            logger.info(f"Chat request: '{user_input}' for {application} (user: {user_id})")
            
            result = chatbot.get_response(user_input, user_id, application)
            
            return jsonify({
                "success": True,
                "response": result["response"],
                "confidence": result["confidence"],
                "application": result["application"],
                "context_used": result["context_used"]
            })
            
        except Exception as e:
            logger.error(f"Chat endpoint error: {e}")
            return jsonify({
                "success": False,
                "response": "Sorry, I'm having trouble processing your request right now.",
                "confidence": 0.0,
                "application": "customer_support",
                "context_used": False
            })
    
    @app.route('/api/train', methods=['POST'])
    def train():
        """Simple training endpoint - for future enhancement"""
        return jsonify({
            "success": True,
            "message": "Training feature will be available in the advanced version"
        })
    
    @app.route('/api/applications', methods=['GET'])
    def get_applications():
        applications = ["customer_support", "college_helpdesk", "hr_recruitment", "personal_assistant"]
        return jsonify({"applications": applications})
    
    @app.route('/api/health', methods=['GET'])
    def health_check():
        return jsonify({
            "status": "healthy", 
            "service": "simple-chatbot",
            "timestamp": datetime.now().isoformat()
        })
    
    return app

if __name__ == '__main__':
    # Check if template directory exists
    if not os.path.exists(TEMPLATES_DIR):
        print(f"❌ ERROR: Templates directory not found at: {TEMPLATES_DIR}")
        print("💡 Please create the directory structure:")
        print("   mkdir -p frontend/templates frontend/static/css frontend/static/js")
        print("   Then create frontend/templates/index.html with the template content")
        exit(1)
    
    if not os.path.exists(os.path.join(TEMPLATES_DIR, 'index.html')):
        print(f"❌ ERROR: index.html not found in: {TEMPLATES_DIR}")
        print("💡 Please create frontend/templates/index.html with the template content")
        exit(1)
    
    app = create_app()
    print("🚀 Starting Multi-Purpose Chatbot...")
    print("📁 Using templates from:", TEMPLATES_DIR)
    print("🌐 Access the chatbot at: http://localhost:5000")
    print("💡 Try asking about: orders, admissions, jobs, or time!")
    app.run(host='0.0.0.0', port=5000, debug=True)