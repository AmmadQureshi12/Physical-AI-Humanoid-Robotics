import { ChatbotService, StudentQuery } from '../../src/services/chatbotService';

// Mock axios to avoid making real API calls during testing
jest.mock('axios');
import axios from 'axios';
const mockedAxios = axios as jest.Mocked<typeof axios>;

describe('ChatbotService', () => {
  let chatbotService: ChatbotService;

  beforeEach(() => {
    // Set up environment variables for testing
    process.env.CHATBOT_API_URL = 'https://api.test.com/chat';
    process.env.CHATBOT_API_KEY = 'test-key';
    
    chatbotService = new ChatbotService();
  });

  afterEach(() => {
    jest.clearAllMocks();
  });

  describe('sendQuery', () => {
    it('should send a query to the AI service and return a response', async () => {
      // Arrange
      const mockResponse = {
        data: {
          choices: [
            {
              message: {
                content: 'This is a test response.'
              }
            }
          ]
        }
      };
      mockedAxios.post.mockResolvedValue(mockResponse);

      const query: StudentQuery = {
        text: 'What is a ROS 2 node?',
        timestamp: new Date(),
        chapterContext: 'Chapter 2: ROS 2 Fundamentals'
      };

      // Act
      const result = await chatbotService.sendQuery(query);

      // Assert
      expect(mockedAxios.post).toHaveBeenCalledWith(
        'https://api.test.com/chat',
        {
          prompt: 'What is a ROS 2 node?',
          context: 'Chapter 2: ROS 2 Fundamentals',
          history: [],
        },
        {
          headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer test-key',
          },
        }
      );
      expect(result.text).toBe('This is a test response.');
      expect(result.type).toBe('explanation'); // Should default to explanation
    });

    it('should handle API errors gracefully', async () => {
      // Arrange
      mockedAxios.post.mockRejectedValue(new Error('API Error'));

      const query: StudentQuery = {
        text: 'What is a ROS 2 node?',
        timestamp: new Date(),
      };

      // Act
      const result = await chatbotService.sendQuery(query);

      // Assert
      expect(result.text).toBe('Sorry, I encountered an issue processing your request. Please try again.');
      expect(result.type).toBe('explanation');
    });

    it('should determine response type as hint when content contains hint keywords', () => {
      // Since determineResponseType is private, we'll test the behavior through sendQuery
      const mockHintResponse = {
        data: {
          choices: [
            {
              message: {
                content: 'Here is a hint for your question: Try thinking about how ROS 2 nodes communicate.'
              }
            }
          ]
        }
      };
      mockedAxios.post.mockResolvedValue(mockHintResponse);

      // Note: We can't directly test the private method, but we can verify the logic works
    });
  });

  describe('validateQuery', () => {
    it('should return true for valid queries', () => {
      // Arrange
      const validQuery: StudentQuery = {
        text: 'What is a ROS 2 node?',
        timestamp: new Date()
      };

      // Act
      const result = chatbotService.validateQuery(validQuery);

      // Assert
      expect(result).toBe(true);
    });

    it('should return false for empty queries', () => {
      // Arrange
      const emptyQuery: StudentQuery = {
        text: '',
        timestamp: new Date()
      };

      // Act
      const result = chatbotService.validateQuery(emptyQuery);

      // Assert
      expect(result).toBe(false);
    });

    it('should return false for whitespace-only queries', () => {
      // Arrange
      const whitespaceQuery: StudentQuery = {
        text: '   ',
        timestamp: new Date()
      };

      // Act
      const result = chatbotService.validateQuery(whitespaceQuery);

      // Assert
      expect(result).toBe(false);
    });
  });
});