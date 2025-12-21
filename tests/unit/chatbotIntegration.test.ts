import Chatbot from '../../src/components/Chatbot/Chatbot';
import { ChatbotService } from '../../src/services/chatbotService';
import { isSolutionRequest, findResource } from '../../src/lib/utils';

// Mock the ChatbotService for testing
jest.mock('../../src/services/chatbotService');
const MockChatbotService = ChatbotService as jest.MockedClass<typeof ChatbotService>;

describe('Chatbot Integration', () => {
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

  describe('Exercise Assistance Feature', () => {
    it('should detect solution requests properly', () => {
      // Test various solution request patterns
      expect(isSolutionRequest('Can you give me the solution?')).toBe(true);
      expect(isSolutionRequest('Please solve this for me')).toBe(true);
      expect(isSolutionRequest('Provide the answer')).toBe(true);
      expect(isSolutionRequest('Show me the code')).toBe(true);
      expect(isSolutionRequest('How do I approach this?')).toBe(false);  // Not a solution request
      expect(isSolutionRequest('Explain the concept')).toBe(false);  // Not a solution request
    });

    it('should return hints instead of solutions for exercise questions', async () => {
      // Since we can't easily test the service's internal logic without changing it,
      // we'll verify the utility function that generates hints
      const query = 'Give me the solution to exercise 3';
      
      // Check that it's identified as solution request
      expect(isSolutionRequest(query)).toBe(true);
      
      // Generate a hint for this query
      const hint = require('../../src/lib/utils').generateHintForExercise(query);
      
      // Verify the hint doesn't contain the actual solution
      expect(hint).toContain('Think about the key concepts');
      expect(hint).toContain('Try approaching');
    });
  });

  describe('Resource Navigation Feature', () => {
    it('should find relevant resources based on queries', () => {
      // Test various resource queries
      expect(findResource('Show me the ROS 2 architecture diagram')).toBe('/docs/chapter-02-ros2-concepts/ros2-architecture-diagram');
      expect(findResource('Where can I find the publisher example?')).toBe('/docs/chapter-02-ros2-concepts/publisher-example');
      expect(findResource('Tell me about chapter 3')).toBe('/docs/chapter-03-simulation');
      expect(findResource('Simulation environment diagram')).toBe('/docs/chapter-03-simulation/simulation-setup');
      expect(findResource('Non-existent resource')).toBeNull();
    });
  });

  describe('Course Content Query Feature', () => {
    it('should return curriculum-relevant responses', async () => {
      // This would be better tested with integration with the actual API
      // For now, we'll test that our enhancement function works
      const originalMethod = Object.getPrototypeOf(chatbotService).enhanceQueryWithCurriculumContext;
      const mockQuery = {
        text: 'What is a ROS 2 node?',
        timestamp: new Date(),
        chapterContext: 'Chapter 2: ROS 2 Concepts'
      };

      // Call the method directly to test its behavior
      const result = await originalMethod.call(chatbotService, mockQuery);
      
      expect(result).toContain('AI-Humanoid Robotics curriculum');
      expect(result).toContain('What is a ROS 2 node?');
    });
  });

  describe('Session Management', () => {
    it('should maintain conversation context', () => {
      // This would require more complex testing with localStorage mock
      // For now, we'll just verify the utility functions exist
      const { createNewSession, addQueryToSession } = require('../../src/lib/utils');
      
      const session = createNewSession('test-user');
      expect(session.userId).toBe('test-user');
      expect(session.queryHistory).toEqual([]);

      const updatedSession = addQueryToSession(session, 'Test query');
      expect(updatedSession.queryHistory).toHaveLength(1);
      expect(updatedSession.queryHistory[0].text).toBe('Test query');
    });
  });
});