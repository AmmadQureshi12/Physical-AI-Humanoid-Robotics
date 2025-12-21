"""
Rate limiter middleware for managing 60 requests per minute per IP.
"""
import time
from typing import Dict, Optional
from fastapi import Request, HTTPException
from fastapi.responses import Response
from collections import defaultdict, deque


class RateLimiter:
    """In-memory rate limiter using a sliding window approach."""
    
    def __init__(self, max_requests: int, window_size: int):
        """
        Initialize rate limiter.
        
        Args:
            max_requests: Maximum number of requests allowed in the window
            window_size: Time window in seconds
        """
        self.max_requests = max_requests
        self.window_size = window_size
        self.requests: Dict[str, deque] = defaultdict(deque)
    
    def is_allowed(self, identifier: str) -> bool:
        """
        Check if a request from the given identifier is allowed.
        
        Args:
            identifier: Unique identifier for the requester (e.g., IP address)
            
        Returns:
            True if request is allowed, False otherwise
        """
        now = time.time()
        # Remove requests that are outside the current window
        while (self.requests[identifier] and 
               now - self.requests[identifier][0] > self.window_size):
            self.requests[identifier].popleft()
        
        # Check if we're under the limit
        if len(self.requests[identifier]) < self.max_requests:
            # Add the current request timestamp
            self.requests[identifier].append(now)
            return True
        
        return False


# Global rate limiter instance - in production, consider using Redis for distributed rate limiting
rate_limiter = RateLimiter(max_requests=60, window_size=60)  # 60 requests per minute


def rate_limit_middleware(request: Request) -> Response:
    """
    Middleware function to enforce rate limiting.
    
    Args:
        request: The incoming request
        
    Returns:
        Response if request is allowed
        
    Raises:
        HTTPException with 429 status if rate limit is exceeded
    """
    # Get client IP address (consider X-Forwarded-For header if behind proxy)
    client_ip = request.client.host
    
    if not rate_limiter.is_allowed(client_ip):
        raise HTTPException(
            status_code=429,
            detail={
                "error": "RATE_LIMIT_EXCEEDED",
                "message": f"Rate limit exceeded. Maximum {rate_limiter.max_requests} requests per {rate_limiter.window_size} seconds."
            }
        )
    
    # Continue with the request if allowed
    return None  # Returning None means continue processing