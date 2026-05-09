"""Application configuration loaded from environment variables."""
from __future__ import annotations

import os
from dotenv import load_dotenv

# Load variables from .env into the process environment
load_dotenv()


class Config:
    """Base configuration class for Flask app."""

    SECRET_KEY = os.getenv("SECRET_KEY", "change-me-in-prod")
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:postgres@localhost:5432/task_management_db",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"

