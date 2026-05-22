"""Services Module - Business Logic Layer

This package contains all the "worker" services.
Each service handles one specific job:
- SubtitleService: Fetch subtitles
- TaggingService: Add tags to subtitles
- StorageService: Save data to files/database
- BaseService: Abstract template for all services
"""

from .base_service import BaseService
from .subtitle_service import SubtitleService
from .tagging_service import TaggingService
from .storage_service import StorageService

__all__ = [
    "BaseService",
    "SubtitleService",
    "TaggingService",
    "StorageService",
]
