"""
Campus Resource Hub - Configuration Module
AiDD 2025 Capstone Project

Defines configuration classes for different environments (Development, Testing, Production).
Per .clinerules: Security-first approach with environment-based configs.
"""

import os
from pathlib import Path
from typing import Optional


# Base directory of the project
BASE_DIR = Path(__file__).parent.parent.absolute()


class Config:
    """Base configuration class with common settings."""

    # Flask Core Settings
    SECRET_KEY: str = os.environ.get("SECRET_KEY") or "dev-secret-key-change-in-production"

    # Database Settings
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    SQLALCHEMY_ECHO: bool = False

    # Security Settings (per .clinerules)
    WTF_CSRF_ENABLED: bool = True
    WTF_CSRF_TIME_LIMIT: Optional[int] = None  # No time limit for CSRF tokens
    SESSION_COOKIE_SECURE: bool = False  # Set to True in production with HTTPS
    SESSION_COOKIE_HTTPONLY: bool = True  # Prevent JavaScript access to session cookie
    SESSION_COOKIE_SAMESITE: str = "Lax"  # CSRF protection
    PERMANENT_SESSION_LIFETIME: int = 3600  # 1 hour session timeout

    # File Upload Settings (per .clinerules security requirements)
    MAX_CONTENT_LENGTH: int = 2 * 1024 * 1024  # 2MB max file size
    UPLOAD_FOLDER: Path = BASE_DIR / "src" / "static" / "uploads"
    ALLOWED_EXTENSIONS: set = {"png", "jpg", "jpeg", "gif"}

    # Pagination
    ITEMS_PER_PAGE: int = 20

    # Flask-Login
    REMEMBER_COOKIE_DURATION: int = 86400  # 1 day
    REMEMBER_COOKIE_SECURE: bool = False  # Set to True in production
    REMEMBER_COOKIE_HTTPONLY: bool = True

    # Application Settings
    APP_NAME: str = "Campus Resource Hub"
    APP_VERSION: str = "0.1.0"

    @staticmethod
    def init_app(app):
        """Initialize application with this configuration."""
        # Ensure upload folder exists
        Config.UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)


class DevelopmentConfig(Config):
    """Development environment configuration."""

    DEBUG: bool = True
    TESTING: bool = False

    # Development database (SQLite)
    SQLALCHEMY_DATABASE_URI: str = f'sqlite:///{BASE_DIR / "instance" / "dev_campus_hub.db"}'
    SQLALCHEMY_ECHO: bool = True  # Log all SQL queries in dev

    # Less strict security for development
    WTF_CSRF_ENABLED: bool = True  # Keep CSRF enabled even in dev for testing

    # Flask-DebugToolbar
    DEBUG_TB_ENABLED: bool = True
    DEBUG_TB_INTERCEPT_REDIRECTS: bool = False


class TestingConfig(Config):
    """Testing environment configuration."""

    DEBUG: bool = False
    TESTING: bool = True

    # In-memory SQLite database for tests
    SQLALCHEMY_DATABASE_URI: str = "sqlite:///:memory:"

    # Disable CSRF for easier testing
    WTF_CSRF_ENABLED: bool = False

    # Faster password hashing for tests
    BCRYPT_LOG_ROUNDS: int = 4  # Faster for testing


class ProductionConfig(Config):
    """Production environment configuration."""

    DEBUG: bool = False
    TESTING: bool = False

    # Production database (PostgreSQL recommended, falls back to SQLite)
    SQLALCHEMY_DATABASE_URI: str = (
        os.environ.get("DATABASE_URL")
        or f'sqlite:///{BASE_DIR / "instance" / "prod_campus_hub.db"}'
    )

    # Production security settings (per .clinerules)
    SESSION_COOKIE_SECURE: bool = True  # HTTPS only
    REMEMBER_COOKIE_SECURE: bool = True  # HTTPS only

    # Stronger password hashing
    BCRYPT_LOG_ROUNDS: int = 13

    @staticmethod
    def init_app(app):
        """Production-specific initialization."""
        Config.init_app(app)

        # Log to stderr in production
        import logging
        from logging import StreamHandler

        handler = StreamHandler()
        handler.setLevel(logging.INFO)
        app.logger.addHandler(handler)


# Configuration dictionary
config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}


def get_config(config_name: Optional[str] = None) -> type[Config]:
    """
    Get configuration class by name.

    Args:
        config_name: Name of configuration ('development', 'testing', 'production')
                    If None, uses FLASK_ENV environment variable or 'development'

    Returns:
        Configuration class
    """
    if config_name is None:
        config_name = os.environ.get("FLASK_ENV", "development")

    return config.get(config_name, DevelopmentConfig)
