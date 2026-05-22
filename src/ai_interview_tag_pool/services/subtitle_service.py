"""
Subtitle Service - Fetches and extracts subtitles from YouTube videos

This service handles:
1. Download video metadata from YouTube
2. Extract subtitles/captions from the video
3. Return structured subtitle data

Uses libraries:
- yt-dlp: Download video info
- youtube-transcript-api: Extract captions
- requests: Make HTTP calls
"""

from typing import Any, Dict, List, Optional
from .base_service import BaseService
import logging

try:
    from youtube_transcript_api import YouTubeTranscriptApi
except ImportError:
    YouTubeTranscriptApi = None

try:
    import yt_dlp
except ImportError:
    yt_dlp = None


class SubtitleService(BaseService):
    """
    Service for fetching and extracting subtitles from YouTube videos.
    
    Workflow:
    1. Parse YouTube URL to get video ID
    2. Fetch video metadata (title, duration, etc)
    3. Extract available subtitles in multiple languages
    4. Return structured subtitle data
    """
    
    def __init__(self, config):
        """
        Initialize SubtitleService with configuration.
        
        Args:
            config: Config object containing:
                - YOUTUBE_API_KEY: API key for YouTube
                - TIMEOUT: Max seconds to wait for API
                - MAX_RETRIES: Number of retries on failure
                - DEBUG: Verbose logging
        """
        super().__init__(config)
        self.timeout = config.TIMEOUT
        self.max_retries = config.MAX_RETRIES
        self.debug = config.DEBUG
        self.log_info("SubtitleService ready")
    
    def execute(self, video_url: str) -> Dict[str, Any]:
        """
        Main method: Fetch subtitles from a YouTube video.
        
        Args:
            video_url: YouTube video URL
                      e.g., "https://www.youtube.com/watch?v=abc123"
        
        Returns:
            {
                "success": True/False,
                "data": {
                    "video_id": "abc123",
                    "title": "Video Title",
                    "duration": 3600,  # seconds
                    "subtitles": [
                        {
                            "time": 0,
                            "duration": 5,
                            "text": "Hello everyone"
                        },
                        ...
                    ],
                    "languages": ["en", "zh"]
                },
                "error": None or error message
            }
        """
        try:
            self.log_info(f"Processing: {video_url}")
            
            # Step 1: Extract video ID from URL
            video_id = self._extract_video_id(video_url)
            if not video_id:
                return self.error_result("Invalid YouTube URL")
            
            self.log_debug(f"Video ID: {video_id}")
            
            # Step 2: Get video metadata
            video_info = self._get_video_info(video_id)
            if not video_info:
                return self.error_result("Could not fetch video metadata")
            
            self.log_debug(f"Title: {video_info.get('title')}")
            
            # Step 3: Extract subtitles
            subtitles = self._extract_subtitles(video_id)
            if not subtitles:
                return self.error_result("No subtitles found for this video")
            
            self.log_info(f"Successfully extracted {len(subtitles)} subtitle entries")
            
            # Step 4: Return success
            return self.success_result({
                "video_id": video_id,
                "title": video_info.get("title"),
                "duration": video_info.get("duration"),
                "subtitles": subtitles,
                "languages": list(set([s.get("language", "en") for s in subtitles]))
            })
        
        except Exception as e:
            self.log_error("Failed to extract subtitles", e)
            return self.error_result("Subtitle extraction failed", e)
    
    def _extract_video_id(self, url: str) -> Optional[str]:
        """
        Extract video ID from various YouTube URL formats.
        
        Handles:
        - https://www.youtube.com/watch?v=abc123
        - https://youtu.be/abc123
        - abc123 (direct ID)
        
        Returns:
            Video ID string or None if invalid
        """
        self.log_debug(f"Extracting video ID from: {url}")
        
        # If it's already just an ID (11 chars)
        if len(url) == 11 and url.isalnum():
            return url
        
        # Try to extract from youtube.com/watch?v=
        if "youtube.com/watch?v=" in url:
            video_id = url.split("watch?v=")[1].split("&")[0]
            return video_id if len(video_id) == 11 else None
        
        # Try to extract from youtu.be/
        if "youtu.be/" in url:
            video_id = url.split("youtu.be/")[1].split("?")[0]
            return video_id if len(video_id) == 11 else None
        
        return None
    
    def _get_video_info(self, video_id: str) -> Optional[Dict]:
        """
        Get video metadata (title, duration, etc) using yt-dlp.
        
        Args:
            video_id: YouTube video ID
        
        Returns:
            Dictionary with video info or None if failed
        """
        if not yt_dlp:
            self.log_warning("yt-dlp not installed, skipping video metadata")
            return {"title": "Unknown", "duration": 0}
        
        try:
            self.log_debug(f"Fetching metadata for: {video_id}")
            
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'socket_timeout': self.timeout,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(f"https://www.youtube.com/watch?v={video_id}", download=False)
                
                return {
                    "title": info.get("title", "Unknown"),
                    "duration": info.get("duration", 0),
                    "uploader": info.get("uploader", "Unknown"),
                    "upload_date": info.get("upload_date", "Unknown"),
                }
        
        except Exception as e:
            self.log_warning(f"Could not fetch video metadata: {str(e)}")
            return None
    
    def _extract_subtitles(self, video_id: str) -> List[Dict]:
        """
        Extract subtitles from YouTube video.
        
        Tries multiple languages:
        1. English (preferred)
        2. Auto-generated captions
        3. Other available languages
        
        Args:
            video_id: YouTube video ID
        
        Returns:
            List of subtitle entries:
            [
                {
                    "time": 0,
                    "duration": 5.5,
                    "text": "Hello world",
                    "language": "en"
                },
                ...
            ]
        """
        if not YouTubeTranscriptApi:
            self.log_error("youtube-transcript-api not installed")
            return []
        
        try:
            self.log_debug(f"Extracting subtitles for: {video_id}")
            
            # Get list of available transcripts
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
            
            # Try to get English subtitles first
            transcript = None
            try:
                transcript = transcript_list.find_transcript(['en'])
            except:
                pass
            
            # If no English, try auto-generated
            if not transcript:
                try:
                    transcript = transcript_list.find_transcript(['en'], include_generated_subtitles=True)
                except:
                    pass
            
            # If still no luck, get any available
            if not transcript:
                if transcript_list.manually_created_transcripts:
                    transcript = list(transcript_list.manually_created_transcripts.values())[0]
                elif transcript_list.generated_transcripts:
                    transcript = list(transcript_list.generated_transcripts.values())[0]
            
            if not transcript:
                self.log_warning("No subtitles available in any language")
                return []
            
            # Get subtitle entries
            entries = transcript.fetch()
            
            # Format subtitle data
            subtitles = []
            for entry in entries:
                subtitles.append({
                    "time": entry.get("start", 0),
                    "duration": entry.get("duration", 0),
                    "text": entry.get("text", ""),
                    "language": transcript.language
                })
            
            self.log_info(f"Extracted {len(subtitles)} subtitle entries")
            return subtitles
        
        except Exception as e:
            self.log_error(f"Failed to extract subtitles from {video_id}", e)
            return []
