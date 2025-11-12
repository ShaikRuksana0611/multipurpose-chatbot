"""
Training Data Manager for Multi-Purpose Chatbot
Handles loading, saving, and managing training data
"""

import json
import os
from typing import Dict, Any, List, Optional
import logging

class TrainingDataManager:
    """
    Manages training data for the chatbot
    """
    
    def __init__(self, data_file: str = "backend/data/chatbot_data.json"):
        """
        Initialize the training data manager
        
        Args:
            data_file: Path to the training data file
        """
        self.logger = logging.getLogger(__name__)
        self.data_file = data_file
        self.data: Dict[str, Any] = {}
        
        self.logger.info(f"TrainingDataManager initialized with data file: {data_file}")
    
    def load_data(self) -> Dict[str, Any]:
        """
        Load training data from file
        
        Returns:
            Training data dictionary
        """
        try:
            # If data file exists, load it
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    self.data = json.load(f)
                self.logger.info(f"Loaded training data from {self.data_file}")
            else:
                # Create default data structure
                self.data = self._create_default_data()
                self.save_data()
                self.logger.info(f"Created new training data file at {self.data_file}")
            
            return self.data
            
        except Exception as e:
            self.logger.error(f"Error loading training data: {e}")
            # Return default data as fallback
            return self._create_default_data()
    
    def _create_default_data(self) -> Dict[str, Any]:
        """
        Create default training data structure
        
        Returns:
            Default training data dictionary
        """
        return {
            "applications": {
                "customer_support": {
                    "patterns": [
                        "hello", "hi", "hey", "good morning", "good afternoon",
                        "i need help with my order", "order status", "track my package",
                        "return policy", "refund request", "cancel order",
                        "product not working", "broken item", "defective product",
                        "shipping delay", "when will my order arrive", "delivery time",
                        "payment issue", "billing problem", "charge dispute"
                    ],
                    "responses": [
                        "Hello! I'm here to help with your customer service needs.",
                        "I can check your order status. Please provide your order number.",
                        "Our return policy allows returns within 30 days of purchase.",
                        "I'm sorry to hear you're having issues. Let me help you with that.",
                        "For shipping delays, I can check the current status for you.",
                        "I can help with payment issues. What seems to be the problem?"
                    ],
                    "tags": [
                        "greeting", "greeting", "greeting", "greeting", "greeting",
                        "order_help", "order_status", "order_status",
                        "return_policy", "refund", "cancel_order",
                        "product_issue", "product_issue", "product_issue",
                        "shipping", "shipping", "shipping",
                        "payment", "payment", "payment"
                    ]
                },
                "college_helpdesk": {
                    "patterns": [
                        "admission requirements", "how to apply", "application deadline",
                        "tuition fees", "scholarships", "financial aid",
                        "course registration", "class schedule", "prerequisites",
                        "campus facilities", "library hours", "computer lab"
                    ],
                    "responses": [
                        "Admission requirements include a completed application and transcripts.",
                        "The application deadline for fall semester is August 1st.",
                        "Tuition fees vary by program. I can check specific costs for you.",
                        "We offer various scholarships based on academic performance.",
                        "Course registration opens two weeks before each semester.",
                        "The library is open from 8 AM to 10 PM on weekdays."
                    ],
                    "tags": [
                        "admissions", "admissions", "admissions",
                        "fees", "financial", "financial",
                        "registration", "schedule", "courses",
                        "facilities", "facilities", "facilities"
                    ]
                },
                "hr_recruitment": {
                    "patterns": [
                        "job openings", "current vacancies", "career opportunities",
                        "application process", "how to apply", "submit resume",
                        "interview process", "hiring stages", "technical interview",
                        "salary range", "compensation", "benefits package"
                    ],
                    "responses": [
                        "We have openings in engineering, marketing, and sales departments.",
                        "You can apply through our careers portal with your resume.",
                        "Our interview process typically includes 3-4 stages.",
                        "Salary ranges are competitive and based on experience.",
                        "We offer comprehensive health benefits and retirement plans."
                    ],
                    "tags": [
                        "openings", "openings", "openings",
                        "application", "application", "application",
                        "interview", "interview", "interview",
                        "compensation", "compensation", "benefits"
                    ]
                },
                "personal_assistant": {
                    "patterns": [
                        "what's the time", "current time", "time please",
                        "weather today", "weather forecast", "will it rain",
                        "set reminder", "remind me to", "schedule meeting",
                        "tell me a joke", "make me laugh", "something funny"
                    ],
                    "responses": [
                        "I can check the time for you. One moment...",
                        "For weather information, I recommend checking a weather app.",
                        "I can help you set reminders. What should I remind you about?",
                        "Why don't scientists trust atoms? Because they make up everything!",
                        "Here's a joke: Why did the scarecrow win an award? He was outstanding in his field!"
                    ],
                    "tags": [
                        "time", "time", "time",
                        "weather", "weather", "weather",
                        "reminder", "reminder", "schedule",
                        "joke", "joke", "joke"
                    ]
                }
            }
        }
    
    def save_data(self) -> bool:
        """
        Save training data to file
        
        Returns:
            True if successful, False otherwise
        """
        try:
            os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
            
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"Training data saved to {self.data_file}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error saving training data: {e}")
            return False
    
    def add_example(self, application: str, pattern: str, response: str, tag: str) -> bool:
        """
        Add a new training example
        
        Args:
            application: Target application
            pattern: User input pattern
            response: Bot response
            tag: Intent tag
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Ensure application exists
            if application not in self.data["applications"]:
                self.data["applications"][application] = {
                    "patterns": [],
                    "responses": [],
                    "tags": []
                }
            
            # Add the new example
            self.data["applications"][application]["patterns"].append(pattern)
            self.data["applications"][application]["responses"].append(response)
            self.data["applications"][application]["tags"].append(tag)
            
            # Save the updated data
            success = self.save_data()
            
            if success:
                self.logger.info(f"Added training example to {application}: {tag}")
            else:
                self.logger.error(f"Failed to save training data after adding example")
            
            return success
            
        except Exception as e:
            self.logger.error(f"Error adding training example: {e}")
            return False
    
    def get_application_data(self, application: str) -> Optional[Dict[str, Any]]:
        """
        Get training data for a specific application
        
        Args:
            application: Application name
            
        Returns:
            Application data or None if not found
        """
        return self.data["applications"].get(application)
    
    def get_all_applications(self) -> List[str]:
        """
        Get list of all available applications
        
        Returns:
            List of application names
        """
        return list(self.data["applications"].keys())
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the training data
        
        Returns:
            Statistics dictionary
        """
        total_patterns = 0
        total_responses = 0
        application_stats = {}
        
        for app_name, app_data in self.data["applications"].items():
            patterns_count = len(app_data["patterns"])
            responses_count = len(app_data["responses"])
            tags_count = len(app_data["tags"])
            
            application_stats[app_name] = {
                "patterns": patterns_count,
                "responses": responses_count,
                "tags": tags_count
            }
            
            total_patterns += patterns_count
            total_responses += responses_count
        
        return {
            "total_applications": len(self.data["applications"]),
            "total_patterns": total_patterns,
            "total_responses": total_responses,
            "applications": application_stats
        }