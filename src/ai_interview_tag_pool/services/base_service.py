"""
Base Service Class - Abstract Template for All Services

This is the BLUEPRINT that all worker services inherit from.
Think of it as: "Every service must follow these rules"

Why?
- Consistency: Every service works the same way
- Easy to extend: Add new services without changing core logic
- Easy to test: Can test any service the same way
- Easy to debug: Same structure everywhere
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
import logging


class BaseService(ABC):
    """
    Abstract base class for all services.
    
    All services (SubtitleService, TaggingService, StorageService) 
    will inherit from this and follow the same pattern.
    
    Pattern:
    1. Every service has __init__ that takes config
    2. Every service has execute() method
    3. Every service has logging built-in
    4. Every service handles errors consistently
    """
    
    def __init__(self, config):
        """
        Initialize service with configuration.
        
        Args:
            config: Config object from config.py
                   (contains API keys, paths, settings)
        """
        self.config = config
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.debug(f"{self.__class__.__name__} initialized")
    
    @abstractmethod
    def execute(self, *args, **kwargs) -> Dict[str, Any]:
        """
        Execute the service's main logic.
        
        This MUST be implemented by every service.
        
        Args:
            *args: Positional arguments (varies by service)
            **kwargs: Keyword arguments (varies by service)
        
        Returns:
            Dictionary with result:
            {
                "success": bool,
                "data": any,
                "error": str (optional)
            }
        
        Example:
            result = service.execute(video_url)
            if result["success"]:
                data = result["data"]
            else:
                error = result["error"]
        """
        pass
    
    def log_info(self, message: str) -> None:
        """
        Log information message.
        
        Args:
            message: What to log
        
        Example:
            self.log_info("Processing started")
        """
        self.logger.info(message)
    
    def log_error(self, message: str, exc: Optional[Exception] = None) -> None:
        """
        Log error message with optional exception details.
        
        Args:
            message: Error description
            exc: Optional exception object
        
        Example:
            try:
                api_call()
            except Exception as e:
                self.log_error("API call failed", e)
        """
        if exc:
            self.logger.error(f"{message}: {str(exc)}", exc_info=True)
        else:
            self.logger.error(message)
    
    def log_warning(self, message: str) -> None:
        """
        Log warning message.
        
        Args:
            message: Warning description
        
        Example:
            self.log_warning("Retry attempt 1 of 3")
        """
        self.logger.warning(message)
    
    def log_debug(self, message: str) -> None:
        """
        Log debug message (only shown if DEBUG=true in .env).
        
        Args:
            message: Debug information
        
        Example:
            self.log_debug(f"Processing item {i}")
        """
        self.logger.debug(message)
    
    def success_result(self, data: Any, message: str = "Success") -> Dict[str, Any]:
        """
        Create a success result dictionary.
        
        Args:
            data: The result data
            message: Optional success message
        
        Returns:
            Formatted result dict
        
        Example:
            return self.success_result(
                data={"subtitles": [...]},
                message="Fetched 100 subtitles"
            )
        """
        self.log_info(message)
        return {
            "success": True,
            "data": data,
            "message": message
        }
    
    def error_result(self, error: str, exc: Optional[Exception] = None) -> Dict[str, Any]:
        """
        Create an error result dictionary.
        
        Args:
            error: Error description
            exc: Optional exception object
        
        Returns:
            Formatted error dict
        
        Example:
            return self.error_result(
                error="API rate limit exceeded",
                exc=e
            )
        """
        self.log_error(error, exc)
        return {
            "success": False,
            "data": None,
            "error": error
        }
    
    def __repr__(self) -> str:
        """String representation of service."""
        return f"{self.__class__.__name__}(debug={self.config.DEBUG})"
