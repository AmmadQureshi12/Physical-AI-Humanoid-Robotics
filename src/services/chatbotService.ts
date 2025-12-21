import axios from 'axios';

// Define types for our chatbot entities based on the backend API
interface ChatRequest {
  message: string;
  user_id?: string;
  session_id?: string;
  context?: string;
}

interface ChatResponse {
  response: string;
  message_type: 'hint' | 'explanation' | 'resource_link';
  session_id: string;
  timestamp: Date;
}

interface Session {
  userId?: string;
  sessionId?: string;
}

/**
 * Chatbot service to handle API calls to the backend AI service
 */
class ChatbotService {
  private apiUrl: string;

  constructor() {
    // The backend runs on port 8000
    this.apiUrl = 'http://localhost:8000/api/v1/chat';
  }

  /**
   * Send a query to the AI service and return a response
   */
  async sendQuery(message: string, session?: Session, context?: string): Promise<ChatResponse> {
    try {
      const requestBody: ChatRequest = {
        message: message,
        user_id: session?.userId,
        session_id: session?.sessionId,
        context: context,
      };

      const response = await axios.post(this.apiUrl, requestBody, {
        headers: {
          'Content-Type': 'application/json',
        },
      });

      // The backend returns a ChatResponse object
      return response.data;
    } catch (error) {
      console.error('Error calling chatbot API:', error);
      // Return a custom error response that matches the ChatResponse interface
      return {
        response: 'Sorry, I encountered an issue processing your request. Please try again.',
        message_type: 'explanation',
        session_id: session?.sessionId || '',
        timestamp: new Date(),
      };
    }
  }

  /**
   * Validate if a query is appropriate based on our requirements
   */
  validateQuery(message: string): boolean {
    // Implement validation logic as per requirements
    return message && message.trim().length > 0;
  }
}

export { ChatbotService, ChatRequest, ChatResponse, Session };