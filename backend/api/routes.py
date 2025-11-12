from flask import jsonify, request
from chatbot_core import MultiPurposeChatbot
import logging

# Initialize chatbot
chatbot = MultiPurposeChatbot()
logger = logging.getLogger(__name__)

def register_routes(app):
    """Register all API routes"""
    
    @app.route('/api/chat', methods=['POST'])
    def chat():
        try:
            data = request.get_json()
            user_input = data.get('message', '')
            user_id = data.get('user_id', 'default')
            application = data.get('application', 'customer_support')
            
            if not user_input:
                return jsonify({"error": "No message provided"}), 400
            
            result = chatbot.process_message(user_input, user_id, application)
            return jsonify({
                "success": True,
                **result
            })
            
        except Exception as e:
            logger.error(f"Chat endpoint error: {e}")
            return jsonify({"error": "Internal server error"}), 500
    
    @app.route('/api/train', methods=['POST'])
    def train():
        try:
            data = request.get_json()
            success = chatbot.add_training_example(
                data.get('application'),
                data.get('pattern'),
                data.get('response'),
                data.get('tag', 'general')
            )
            
            return jsonify({
                "success": success,
                "message": "Training data added" if success else "Failed to add data"
            })
            
        except Exception as e:
            logger.error(f"Train endpoint error: {e}")
            return jsonify({"error": "Internal server error"}), 500
    
    @app.route('/api/health', methods=['GET'])
    def health_check():
        return jsonify({"status": "healthy", "service": "chatbot"})