# API Documentation

## Base URL

`http://localhost:5000/api`

## Endpoints

### POST /api/chat

Send a message to the chatbot.

**Request Body:**

```json
{
  "message": "Hello, I need help with my order",
  "user_id": "user_123",
  "application": "customer_support"
}
