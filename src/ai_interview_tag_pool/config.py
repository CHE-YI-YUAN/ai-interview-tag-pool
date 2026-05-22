"""
Configuration Management Module

This file is the CENTRAL HUB for all settings.
Think of it as a control panel that reads from .env and provides values everywhere.

Flow:
.env (your secrets) → config.py (reads & validates) → services/ (use the values)
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """
    Base Configuration Class
    
    Contains all settings your app needs.
    Every service will get an instance of this.
    """
    
    # ============ DIRECTORY PATHS ============
    # Get the root directory of the project
    PROJECT_ROOT = Path(__file__).parent.parent.parent  # Goes up to ai-interview-tag-pool/
    
    # Create data directories if they don't exist
    DATA_DIR = PROJECT_ROOT / "data"
    SUBS_DIR = PROJECT_ROOT / "subs"
    LOGS_DIR = PROJECT_ROOT / "logs"
    
    # Ensure directories exist
    DATA_DIR.mkdir(exist_ok=True)
    SUBS_DIR.mkdir(exist_ok=True)
    LOGS_DIR.mkdir(exist_ok=True)
    
    # ============ API KEYS (from .env) ============
    # These come from your .env file
    # If .env is not set, defaults to empty string
    MIMO_API_KEY = os.getenv("MIMO_API_KEY", "")
    YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY", "")
    
    # ============ FEATURE FLAGS ============
    # Control behavior without changing code
    DEBUG = os.getenv("DEBUG", "false").lower() == "true"
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    
    # ============ SERVICE CONFIGURATIONS ============
    # Tuning knobs for processing
    BATCH_SIZE = int(os.getenv("BATCH_SIZE", "10"))
    MAX_RETRIES = int(os.getenv("MAX_RETRIES", "3"))
    TIMEOUT = int(os.getenv("TIMEOUT", "30"))
    
    # ============ INTERNAL SETTINGS ============
    # Index file for tracking processed videos
    INDEX_FILE = DATA_DIR / "index.json"
    
    @classmethod
    def validate(cls):
        """
        Validate that required settings are present.
        Useful for catching configuration errors early.
        """
        required_keys = ["MIMO_API_KEY", "YOUTUBE_API_KEY"]
        missing = [key for key in required_keys if not getattr(cls, key)]
        
        if missing and not cls.DEBUG:
            # In production, missing keys are a problem
            raise ValueError(f"Missing required configuration: {', '.join(missing)}")
        elif missing:
            # In development, just warn
            print(f"⚠️  Warning: Missing config keys: {', '.join(missing)}")


class DevelopmentConfig(Config):
    """
    Development Environment Configuration
    
    Used when ENV=development (default)
    - Debug mode ON
    - Detailed logging
    - Less strict validation
    """
    DEBUG = True
    LOG_LEVEL = "DEBUG"


class ProductionConfig(Config):
    """
    Production Environment Configuration
    
    Used when ENV=production
    - Debug mode OFF
    - Minimal logging
    - Strict validation
    - Optimized for performance
    """
    DEBUG = False
    LOG_LEVEL = "INFO"
    BATCH_SIZE = 50  # Process more at once in production


class TestingConfig(Config):
    """
    Testing Environment Configuration
    
    Used when running tests
    - Uses mock data
    - Shorter timeouts
    - Verbose logging for debugging
    """
    DEBUG = True
    LOG_LEVEL = "DEBUG"
    TIMEOUT = 5  # Faster timeouts for tests
    MAX_RETRIES = 1  # Don't retry in tests


def get_config():
    """
    Factory function to get the right config based on ENV variable.
    
    Returns:
        Config object (DevelopmentConfig, ProductionConfig, or TestingConfig)
    
    Usage:
        config = get_config()
        api_key = config.MIMO_API_KEY
        debug_mode = config.DEBUG
    """
    env = os.getenv("ENV", "development").lower()
    
    if env == "production":
        return ProductionConfig()
    elif env == "testing":
        return TestingConfig()
    else:
        return DevelopmentConfig()


# ============ GLOBAL CONFIG INSTANCE ============
# Most of the time, you'll use this
config = get_config()


# ============ CONVENIENCE FUNCTIONS ============
def get_data_dir():
    """Get the data directory path."""
    return config.DATA_DIR


def get_subs_dir():
    """Get the subtitles directory path."""
    return config.SUBS_DIR


def get_logs_dir():
    """Get the logs directory path."""
    return config.LOGS_DIR


def is_debug():
    """Check if debug mode is enabled."""
    return config.DEBUG


def get_batch_size():
    """Get the batch processing size."""
    return config.BATCH_SIZE
