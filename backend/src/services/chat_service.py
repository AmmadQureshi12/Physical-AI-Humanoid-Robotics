"""
Chat service for the educational chatbot
Implements the core functionality of the chatbot including:
- Processing user queries
- Providing curriculum-relevant responses
- Exercise assistance without giving direct solutions
- Resource navigation
"""
import os
import logging
import re
from datetime import datetime
from typing import Optional, Tuple, Dict, Any
from urllib.parse import urljoin

# Use the proper generation service that connects to Cohere
from src.services.generation_service import generation_service
from src.utils.token_utils import get_token_count, truncate_text_to_token_limit

logger = logging.getLogger(__name__)


class ChatService:
    def __init__(self):
        self.generation_service = generation_service
        self.curriculum_content = self._load_curriculum_content()
        self.resource_map = self._build_resource_map()

    def _load_curriculum_content(self) -> str:
        """
        Load curriculum content from the book/docs directory.
        """
        curriculum_content = ""
        for root, dirs, files in os.walk("book/docs"):
            for file in files:
                if file.endswith(".md"):
                    with open(os.path.join(root, file), "r", encoding="utf-8") as f:
                        curriculum_content += f.read()
        return curriculum_content

    def _build_resource_map(self) -> Dict[str, str]:
        """
        Build a map of keywords to curriculum resources
        """
        base_url = os.getenv("BASE_DOCS_URL", "/docs/")
        return {
            # Diagrams
            "ros 2 architecture": urljoin(base_url, "chapter-02-ros2-concepts/ros2-architecture-diagram"),
            "node graph": urljoin(base_url, "chapter-02-ros2-concepts/node-graph-structure"),
            "topic architecture": urljoin(base_url, "chapter-02-ros2-concepts/topic-architecture-diagram"),
            "service communication": urljoin(base_url, "chapter-02-ros2-concepts/service-communication-diagram"),
            "action architecture": urljoin(base_url, "chapter-02-ros2-concepts/action-architecture-diagram"),
            "simulation environment": urljoin(base_url, "chapter-03-simulation/simulation-setup"),
            "gazebo interface": urljoin(base_url, "chapter-03-simulation/gazebo-interface-diagram"),
            "vlm architecture": urljoin(base_url, "chapter-04-vla/vlm-architecture-diagram"),
            "vla implementation": urljoin(base_url, "chapter-04-vla/vla-implementation-diagram"),
            "capstone architecture": urljoin(base_url, "chapter-05-capstone/capstone-architecture-diagram"),

            # Code examples
            "publisher example": urljoin(base_url, "chapter-02-ros2-concepts/publisher-example"),
            "subscriber example": urljoin(base_url, "chapter-02-ros2-concepts/subscriber-example"),
            "service server example": urljoin(base_url, "chapter-02-ros2-concepts/service-server-example"),
            "action server example": urljoin(base_url, "chapter-02-ros2-concepts/action-server-example"),
            "simulation launch": urljoin(base_url, "chapter-03-simulation/launch-files"),
            "camera integration": urljoin(base_url, "chapter-04-vla/camera-integration"),
            "robot control": urljoin(base_url, "chapter-04-vla/robot-control"),

            # Chapters
            "chapter 1": urljoin(base_url, "chapter-01-specification"),
            "chapter 2": urljoin(base_url, "chapter-02-ros2-concepts"),
            "chapter 3": urljoin(base_url, "chapter-03-simulation"),
            "chapter 4": urljoin(base_url, "chapter-04-vla"),
            "chapter 5": urljoin(base_url, "chapter-05-capstone"),
            "introduction": urljoin(base_url, "chapter-01-specification"),
            "ros 2 concepts": urljoin(base_url, "chapter-02-ros2-concepts"),
            "simulation": urljoin(base_url, "chapter-03-simulation"),
            "vla concepts": urljoin(base_url, "chapter-04-vla"),
            "capstone project": urljoin(base_url, "chapter-05-capstone"),
        }

    async def get_response(self, user_message: str, context: Optional[str] = None,
                    user_id: Optional[str] = None, session_id: Optional[str] = None) -> Tuple[str, str]:
        """
        Process a user message and return a response along with its type
        """
        try:
            # Check if this is a request for a direct solution
            if self._is_solution_request(user_message):
                hint = self._generate_exercise_hint(user_message)
                return hint, "hint"

            # Check if this is a resource navigation request
            resource_path = self._find_resource(user_message)
            if resource_path:
                response_text = f"I found a resource that might help: [{user_message}]({resource_path})"
                return response_text, "resource_link"

            # Otherwise, process as a curriculum question
            # This would involve RAG with the curriculum content
            enhanced_prompt = self._enhance_query_with_context(
                query=user_message,
                context=context,
                curriculum_content=self.curriculum_content
            )

            # Truncate the prompt to prevent token limit errors
            max_tokens = 800000  # Conservatively set below the limit
            truncated_prompt = truncate_text_to_token_limit(enhanced_prompt, max_tokens)

            response = await self.generation_service.generate_response(truncated_prompt)

            # For now, assume it's an explanation
            return response, "explanation"
        except Exception as e:
            logger.error(f"Error in chat service: {e}")
            return "Sorry, I encountered an issue processing your request. Please try again.", "explanation"

    def _is_solution_request(self, query: str) -> bool:
        """
        Check if the query is requesting a direct solution
        """
        solution_keywords = [
            'solution', 'solve', 'answer', 'code', 'implementation',
            'directly', 'complete', 'full', 'entire', 'copy', 'paste',
            'give me', 'provide', 'send', 'tell me'
        ]

        lower_query = query.lower()
        return any(keyword in lower_query for keyword in solution_keywords)

    def _generate_exercise_hint(self, query: str) -> str:
        """
        Generate a helpful hint for an exercise question without providing the solution
        """
        hints = [
            f"Think about the key concepts covered in this chapter related to: {query}",
            "Consider breaking the problem into smaller, manageable parts.",
            "Review the examples in the curriculum that are similar to your question.",
            "What are the fundamental principles that apply to this problem?",
            "Try approaching the problem from a different angle or perspective."
        ]

        import random
        return random.choice(hints)

    def _find_resource(self, query: str) -> Optional[str]:
        """
        Find a relevant resource based on the query
        """
        lower_query = query.lower().strip()

        # Check if the query is asking for a specific resource (e.g., "show me", "where can I find", "diagram", "example")
        query_is_resource_request = self._is_resource_request(lower_query)

        # If it's a resource request, we can use broader matching
        if query_is_resource_request:
            # Look for exact matches first
            for keyword, path in self.resource_map.items():
                if keyword in lower_query:
                    return path

            # Then try broader matching
            query_words = set(lower_query.split())
            for keyword, path in self.resource_map.items():
                keyword_words = keyword.split()
                # Check if all words of the keyword appear in the query in sequence or separately
                if self._keyword_matches_query(keyword_words, query_words, lower_query):
                    return path
        else:
            # For non-resource requests, only match exact phrases that are specifically resource-related
            # rather than general curriculum concepts
            for keyword, path in self.resource_map.items():
                # Only match if the keyword is multi-word (likely a specific resource) or
                # if the keyword is clearly a resource type (diagram, example, etc.)
                if keyword in lower_query and self._is_specific_resource(keyword):
                    return path

        return None

    def _is_specific_resource(self, keyword: str) -> bool:
        """
        Determine if a keyword represents a specific resource rather than a general concept
        """
        # Multi-word keywords are more likely to be specific resources
        if len(keyword.split()) > 1:
            return True

        # Keywords that clearly indicate specific resources
        resource_indicators = [
            "diagram", "example", "chapter", "section", "figure", "image",
            "code", "tutorial", "guide", "reference", "resource", "link",
            "architecture", "environment", "interface", "implementation"
        ]

        for indicator in resource_indicators:
            if indicator in keyword:
                return True

        # General concepts like "simulation", "ros 2", etc. are not specific resources
        return False

    def _is_resource_request(self, query: str) -> bool:
        """
        Determine if the query is asking for a specific resource rather than an explanation
        """
        resource_indicators = [
            "show me", "where can i find", "where is", "diagram", "figure", "image",
            "example", "code", "sample", "resource", "link", "reference", "documentation",
            "chapter", "section", "guide", "tutorial", "how to find", "location of"
        ]

        for indicator in resource_indicators:
            if indicator in query:
                return True

        # Check for question patterns typically asking for resources
        resource_question_patterns = [
            "where.*located", "where.*find", "show.*me", "link.*to", "reference.*for",
            "resource.*on", "example.*for", "diagram.*of", "figure.*for"
        ]

        import re
        for pattern in resource_question_patterns:
            if re.search(pattern, query):
                return True

        return False

    def _keyword_matches_query(self, keyword_words: list, query_words: set, lower_query: str) -> bool:
        """
        Check if the keyword matches the query considering word boundaries and sequence
        """
        # Exact phrase match
        if ' '.join(keyword_words) in lower_query:
            return True

        # Check if all words in the keyword are present in the query
        keyword_set = set(keyword_words)
        if keyword_set.issubset(query_words):
            # Additional check: make sure the words appear in a meaningful way
            # e.g., "ros 2" should be close together in the query
            query_word_positions = []
            for word in keyword_words:
                pos = lower_query.find(word)
                if pos != -1:
                    query_word_positions.append(pos)

            # If we found all words, check if they appear in sequence (with a tolerance for other words in-between)
            if len(query_word_positions) == len(keyword_words):
                # Sort positions to check if they're roughly in sequence
                query_word_positions.sort()

                # Check if max distance between first and last word is reasonable
                # Allow up to 2 words between first and last keyword word
                max_reasonable_distance = sum(len(w) for w in keyword_words) + 2 * (len(keyword_words) - 1) + 6  # +6 for buffer
                if query_word_positions[-1] - query_word_positions[0] <= max_reasonable_distance:
                    return True

        return False

    def _enhance_query_with_context(self, query: str, context: Optional[str], curriculum_content: Optional[str]) -> str:
        """
        Enhance the user's query with curriculum context for better relevance
        """
        prompt = f"Please answer this question based on the AI-Humanoid Robotics curriculum: {query}"
        
        if context:
            prompt = f"Based on the context '{context}', {prompt}"
        
        if curriculum_content:
            prompt += f"\n\nHere is the curriculum content to help you answer:\n{curriculum_content}"
            
        return prompt