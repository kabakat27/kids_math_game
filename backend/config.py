"""
Configuration management for different environments
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Base configuration"""
    DEBUG = False
    TESTING = False
    CORS_ORIGINS = ["http://localhost:3000", "http://localhost:5000"]
    API_VERSION = "v1"


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    ENV = "development"
    CORS_ORIGINS = ["http://localhost:3000", "http://localhost:5000", "http://127.0.0.1:3000"]


class StagingConfig(Config):
    """Staging configuration"""
    DEBUG = False
    ENV = "staging"
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "https://staging.example.com").split(",")


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    ENV = "production"
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "https://kids-math-game.example.com").split(",")


class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True
    ENV = "testing"


# Map environment names to config classes
config_by_name = {
    'development': DevelopmentConfig,
    'staging': StagingConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}


def get_config(env: str = None) -> Config:
    """
    Get configuration object based on environment.
    
    Args:
        env: Environment name (dev, staging, prod, testing)
             If None, reads from FLASK_ENV or defaults to 'development'
    
    Returns:
        Config object for the specified environment
    """
    if env is None:
        env = os.getenv('FLASK_ENV', 'development')
    
    return config_by_name.get(env, DevelopmentConfig)
