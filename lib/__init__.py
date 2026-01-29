"""
Conversational AI Template Framework - Python Library

This library provides tools for managing ElevenLabs Conversational AI projects.
"""

from .elevenlabs_client import (
    ElevenLabsClient,
    ElevenLabsClientError,
    APIResponse,
    APIErrorCode,
)
from .config_loader import ConfigLoader, ConfigError
from .schema_validator import SchemaValidator, ValidationError

__version__ = "1.0.0"
__all__ = [
    "ElevenLabsClient",
    "ElevenLabsClientError",
    "APIResponse",
    "APIErrorCode",
    "ConfigLoader",
    "ConfigError",
    "SchemaValidator",
    "ValidationError",
]
