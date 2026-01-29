"""
ElevenLabs API Client

Handles all ElevenLabs Conversational AI API calls.
"""

import logging
import requests
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field
from enum import Enum

logger = logging.getLogger(__name__)


class HTTPMethod(Enum):
    """HTTP methods"""
    GET = "GET"
    POST = "POST"
    PATCH = "PATCH"
    DELETE = "DELETE"


class APIErrorCode(Enum):
    """API error codes"""
    SUCCESS = 0
    TIMEOUT = 1
    CONNECTION_ERROR = 2
    INVALID_RESPONSE = 3
    AUTHENTICATION_ERROR = 4
    NOT_FOUND = 5
    RATE_LIMITED = 6
    SERVER_ERROR = 7
    UNKNOWN = 99


@dataclass
class APIResponse:
    """API response wrapper"""
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    error_code: APIErrorCode = APIErrorCode.SUCCESS
    status_code: int = 0
    raw_response: Optional[str] = field(default=None, repr=False)

    def __post_init__(self):
        """Validation after initialization"""
        if self.success and self.error:
            logger.warning("APIResponse: success=True but error is set")
        if not self.success and not self.error:
            self.error = "Unknown error"


class ElevenLabsClientError(Exception):
    """ElevenLabs client error"""
    def __init__(self, message: str, error_code: APIErrorCode = APIErrorCode.UNKNOWN):
        super().__init__(message)
        self.error_code = error_code


class ElevenLabsClient:
    """ElevenLabs Conversational AI API client"""

    BASE_URL = "https://api.elevenlabs.io/v1"
    DEFAULT_TIMEOUT = 30
    MAX_RETRIES = 3
    RETRY_DELAY = 1.0

    def __init__(self, api_key: str, timeout: int = DEFAULT_TIMEOUT):
        """
        Initialize the client.

        Args:
            api_key: ElevenLabs API key
            timeout: Default timeout in seconds

        Raises:
            ElevenLabsClientError: If api_key is empty
        """
        if not api_key or not api_key.strip():
            raise ElevenLabsClientError(
                "API key cannot be empty",
                APIErrorCode.AUTHENTICATION_ERROR
            )

        self._api_key = api_key.strip()
        self._timeout = timeout
        self._session: Optional[requests.Session] = None
        self._created_agents: Dict[str, str] = {}
        self._created_tools: Dict[str, str] = {}
        self._created_kb_docs: Dict[str, str] = {}

    @property
    def session(self) -> requests.Session:
        """Lazy session initialization"""
        if self._session is None:
            self._session = requests.Session()
            self._session.headers.update({
                "xi-api-key": self._api_key,
                "Content-Type": "application/json",
                "User-Agent": "Conversational-AI-Template/1.0"
            })
        return self._session

    def close(self):
        """Close the session"""
        if self._session:
            self._session.close()
            self._session = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        return False

    def _classify_error(self, status_code: int) -> APIErrorCode:
        """Determine error code based on HTTP status code"""
        if status_code == 401 or status_code == 403:
            return APIErrorCode.AUTHENTICATION_ERROR
        elif status_code == 404:
            return APIErrorCode.NOT_FOUND
        elif status_code == 429:
            return APIErrorCode.RATE_LIMITED
        elif 500 <= status_code < 600:
            return APIErrorCode.SERVER_ERROR
        else:
            return APIErrorCode.UNKNOWN

    def _parse_error_message(self, response: requests.Response) -> str:
        """Extract error message from response"""
        try:
            error_data = response.json()
            if isinstance(error_data, dict):
                if "detail" in error_data:
                    detail = error_data["detail"]
                    if isinstance(detail, str):
                        return detail
                    elif isinstance(detail, dict):
                        return detail.get("message", str(detail))
                    elif isinstance(detail, list) and detail:
                        return str(detail[0])
                if "message" in error_data:
                    return error_data["message"]
                if "error" in error_data:
                    return error_data["error"]
            return response.text[:500] if response.text else f"HTTP {response.status_code}"
        except (ValueError, KeyError):
            return response.text[:500] if response.text else f"HTTP {response.status_code}"

    def _request(
        self,
        method: HTTPMethod,
        endpoint: str,
        data: Optional[Dict] = None,
        files: Optional[Dict] = None,
        timeout: Optional[int] = None,
        retry_count: int = 0
    ) -> APIResponse:
        """
        Execute an API call.

        Args:
            method: HTTP method
            endpoint: API endpoint (e.g., /convai/agents/create)
            data: Request body (JSON)
            files: Files for multipart upload
            timeout: Timeout in seconds (None = default)
            retry_count: Current retry count

        Returns:
            APIResponse object
        """
        url = f"{self.BASE_URL}{endpoint}"
        effective_timeout = timeout or self._timeout

        logger.debug(f"API Request: {method.value} {endpoint}")

        try:
            if files:
                headers = {
                    "xi-api-key": self._api_key,
                    "User-Agent": "Conversational-AI-Template/1.0"
                }
                response = self.session.request(
                    method=method.value,
                    url=url,
                    data=data,
                    files=files,
                    headers=headers,
                    timeout=effective_timeout
                )
            else:
                response = self.session.request(
                    method=method.value,
                    url=url,
                    json=data,
                    timeout=effective_timeout
                )

            logger.debug(f"API Response: {response.status_code}")

            if response.status_code in (200, 201, 204):
                response_data = None
                if response.text:
                    try:
                        response_data = response.json()
                    except ValueError:
                        response_data = {"raw": response.text}

                return APIResponse(
                    success=True,
                    data=response_data or {},
                    status_code=response.status_code,
                    raw_response=response.text
                )

            if response.status_code == 429 and retry_count < self.MAX_RETRIES:
                import time
                retry_after = float(response.headers.get("Retry-After", self.RETRY_DELAY))
                logger.warning(f"Rate limited, retrying in {retry_after}s...")
                time.sleep(retry_after)
                return self._request(method, endpoint, data, files, timeout, retry_count + 1)

            error_code = self._classify_error(response.status_code)
            error_msg = self._parse_error_message(response)

            return APIResponse(
                success=False,
                error=f"HTTP {response.status_code}: {error_msg}",
                error_code=error_code,
                status_code=response.status_code,
                raw_response=response.text
            )

        except requests.exceptions.Timeout:
            logger.error(f"Request timeout: {endpoint}")
            return APIResponse(
                success=False,
                error=f"Request timeout after {effective_timeout}s",
                error_code=APIErrorCode.TIMEOUT,
                status_code=0
            )

        except requests.exceptions.ConnectionError as e:
            logger.error(f"Connection error: {endpoint} - {e}")
            return APIResponse(
                success=False,
                error=f"Connection error: {str(e)}",
                error_code=APIErrorCode.CONNECTION_ERROR,
                status_code=0
            )

        except requests.exceptions.RequestException as e:
            logger.error(f"Request error: {endpoint} - {e}")
            return APIResponse(
                success=False,
                error=f"Request failed: {str(e)}",
                error_code=APIErrorCode.UNKNOWN,
                status_code=0
            )

    # =========================================================================
    # Validation
    # =========================================================================

    def validate_api_key(self) -> APIResponse:
        """Validate the API key."""
        return self._request(HTTPMethod.GET, "/user")

    # =========================================================================
    # Voice Management
    # =========================================================================

    def list_voices(self) -> APIResponse:
        """List available voices."""
        return self._request(HTTPMethod.GET, "/voices")

    def get_voice(self, voice_id: str) -> APIResponse:
        """Get a specific voice."""
        if not voice_id or not voice_id.strip():
            raise ElevenLabsClientError(
                "Voice ID cannot be empty",
                APIErrorCode.INVALID_RESPONSE
            )
        return self._request(HTTPMethod.GET, f"/voices/{voice_id.strip()}")

    # =========================================================================
    # Agent Management
    # =========================================================================

    def create_agent(
        self,
        name: str,
        first_message: str,
        system_prompt: str,
        llm: str = "gpt-4o",
        language: str = "hu",
        voice_id: Optional[str] = None,
        voice_settings: Optional[Dict[str, float]] = None,
        turn_settings: Optional[Dict[str, int]] = None,
        tools: Optional[List[Dict[str, Any]]] = None,
        knowledge_base_ids: Optional[List[str]] = None
    ) -> APIResponse:
        """
        Create a new agent.

        Args:
            name: Agent name
            first_message: First message
            system_prompt: System prompt
            llm: LLM model (gpt-4o, gemini-2.0-flash-001, etc.)
            language: Language code
            voice_id: ElevenLabs voice ID
            voice_settings: Voice settings (stability, similarity_boost, style)
            turn_settings: Turn settings (turn_timeout, max_duration_seconds)
            tools: Tool definitions list
            knowledge_base_ids: Knowledge base document IDs

        Returns:
            APIResponse with agent_id
        """
        if not name or not name.strip():
            raise ElevenLabsClientError("Agent name cannot be empty")
        if not first_message:
            raise ElevenLabsClientError("First message cannot be empty")
        if not system_prompt:
            raise ElevenLabsClientError("System prompt cannot be empty")

        prompt_config: Dict[str, Any] = {
            "prompt": system_prompt,
            "llm": llm,
            "max_tokens": 1024
        }

        if tools:
            prompt_config["tools"] = tools

        if knowledge_base_ids:
            prompt_config["knowledge_base"] = [
                {
                    "type": "text",
                    "id": kb_id,
                    "name": f"kb_{kb_id[:8]}",
                    "usage_mode": "auto"
                }
                for kb_id in knowledge_base_ids
            ]

        agent_config: Dict[str, Any] = {
            "first_message": first_message,
            "language": language,
            "prompt": prompt_config
        }

        tts_config: Dict[str, Any] = {
            "model_id": "eleven_turbo_v2_5"
        }

        if voice_id:
            tts_config["voice_id"] = voice_id.strip()

        if voice_settings:
            for key in ("stability", "similarity_boost", "style"):
                if key in voice_settings:
                    tts_config[key] = voice_settings[key]

        turn_config: Dict[str, Any] = {}
        if turn_settings and "turn_timeout" in turn_settings:
            turn_config["turn_timeout"] = turn_settings["turn_timeout"]

        conversation_config: Dict[str, Any] = {}
        if turn_settings and "max_duration_seconds" in turn_settings:
            conversation_config["max_duration_seconds"] = turn_settings["max_duration_seconds"]

        request_data: Dict[str, Any] = {
            "name": name.strip(),
            "conversation_config": {
                "agent": agent_config,
                "tts": tts_config,
                "asr": {
                    "quality": "high",
                    "provider": "elevenlabs"
                }
            }
        }

        if turn_config:
            request_data["conversation_config"]["turn"] = turn_config

        if conversation_config:
            request_data["conversation_config"]["conversation"] = conversation_config

        return self._request(HTTPMethod.POST, "/convai/agents/create", request_data, timeout=60)

    def update_agent(self, agent_id: str, updates: Dict[str, Any]) -> APIResponse:
        """Update an existing agent."""
        if not agent_id or not agent_id.strip():
            raise ElevenLabsClientError("Agent ID cannot be empty")
        if not updates:
            raise ElevenLabsClientError("Updates cannot be empty")

        return self._request(HTTPMethod.PATCH, f"/convai/agents/{agent_id.strip()}", updates)

    def get_agent(self, agent_id: str) -> APIResponse:
        """Get an agent."""
        if not agent_id or not agent_id.strip():
            raise ElevenLabsClientError("Agent ID cannot be empty")

        return self._request(HTTPMethod.GET, f"/convai/agents/{agent_id.strip()}")

    def list_agents(self) -> APIResponse:
        """List all agents."""
        return self._request(HTTPMethod.GET, "/convai/agents")

    def delete_agent(self, agent_id: str) -> APIResponse:
        """Delete an agent."""
        if not agent_id or not agent_id.strip():
            raise ElevenLabsClientError("Agent ID cannot be empty")

        return self._request(HTTPMethod.DELETE, f"/convai/agents/{agent_id.strip()}")

    # =========================================================================
    # Knowledge Base Management
    # =========================================================================

    def create_knowledge_base_from_text(
        self,
        text: str,
        name: Optional[str] = None
    ) -> APIResponse:
        """Create a knowledge base document from text."""
        if not text or not text.strip():
            raise ElevenLabsClientError("Text content cannot be empty")

        data: Dict[str, str] = {"text": text}
        if name:
            data["name"] = name.strip()

        return self._request(HTTPMethod.POST, "/convai/knowledge-base/text", data, timeout=60)

    def create_knowledge_base_from_file(
        self,
        file_path: str,
        name: Optional[str] = None
    ) -> APIResponse:
        """Create a knowledge base document from file."""
        import os

        if not file_path:
            raise ElevenLabsClientError("File path cannot be empty")
        if not os.path.exists(file_path):
            raise ElevenLabsClientError(f"File not found: {file_path}")

        try:
            with open(file_path, "rb") as f:
                files = {"file": (os.path.basename(file_path), f)}
                data: Dict[str, str] = {}
                if name:
                    data["name"] = name.strip()
                return self._request(
                    HTTPMethod.POST,
                    "/convai/knowledge-base/file",
                    data=data,
                    files=files,
                    timeout=120
                )
        except IOError as e:
            raise ElevenLabsClientError(f"Cannot read file: {e}")

    def get_knowledge_base_document(self, doc_id: str) -> APIResponse:
        """Get a knowledge base document."""
        if not doc_id or not doc_id.strip():
            raise ElevenLabsClientError("Document ID cannot be empty")

        return self._request(HTTPMethod.GET, f"/convai/knowledge-base/{doc_id.strip()}")

    def delete_knowledge_base_document(self, doc_id: str) -> APIResponse:
        """Delete a knowledge base document."""
        if not doc_id or not doc_id.strip():
            raise ElevenLabsClientError("Document ID cannot be empty")

        return self._request(HTTPMethod.DELETE, f"/convai/knowledge-base/{doc_id.strip()}")

    # =========================================================================
    # Tool Management
    # =========================================================================

    def create_tool(self, tool_config: Dict[str, Any]) -> APIResponse:
        """Create a new tool."""
        if not tool_config:
            raise ElevenLabsClientError("Tool config cannot be empty")

        return self._request(HTTPMethod.POST, "/convai/tools", {"tool_config": tool_config})

    def create_client_tool(
        self,
        name: str,
        description: str,
        parameters: Optional[Dict[str, Any]] = None
    ) -> APIResponse:
        """Create a client tool (mock tool for MVP)."""
        if not name or not name.strip():
            raise ElevenLabsClientError("Tool name cannot be empty")
        if not description:
            raise ElevenLabsClientError("Tool description cannot be empty")

        tool_config: Dict[str, Any] = {
            "type": "client",
            "name": name.strip(),
            "description": description,
            "expects_response": True,
            "response_timeout_secs": 30
        }

        if parameters:
            tool_config["parameters"] = parameters

        return self.create_tool(tool_config)

    def create_system_tool(
        self,
        name: str,
        system_tool_type: str,
        description: Optional[str] = None,
        params: Optional[Dict[str, Any]] = None
    ) -> APIResponse:
        """Create a system tool (e.g., transfer_to_agent)."""
        if not name or not name.strip():
            raise ElevenLabsClientError("Tool name cannot be empty")
        if not system_tool_type:
            raise ElevenLabsClientError("System tool type cannot be empty")

        tool_config: Dict[str, Any] = {
            "type": "system",
            "name": name.strip(),
            "params": {
                "system_tool_type": system_tool_type
            }
        }

        if description:
            tool_config["description"] = description

        if params:
            tool_config["params"].update(params)

        return self.create_tool(tool_config)

    def get_tool(self, tool_id: str) -> APIResponse:
        """Get a tool."""
        if not tool_id or not tool_id.strip():
            raise ElevenLabsClientError("Tool ID cannot be empty")

        return self._request(HTTPMethod.GET, f"/convai/tools/{tool_id.strip()}")

    def delete_tool(self, tool_id: str) -> APIResponse:
        """Delete a tool."""
        if not tool_id or not tool_id.strip():
            raise ElevenLabsClientError("Tool ID cannot be empty")

        return self._request(HTTPMethod.DELETE, f"/convai/tools/{tool_id.strip()}")

    # =========================================================================
    # Registry (tracking created items)
    # =========================================================================

    def register_agent(self, local_id: str, elevenlabs_id: str) -> None:
        """Register a created agent."""
        if local_id and elevenlabs_id:
            self._created_agents[local_id] = elevenlabs_id

    def get_agent_id(self, local_id: str) -> Optional[str]:
        """Get ElevenLabs agent ID by local ID."""
        return self._created_agents.get(local_id)

    def register_tool(self, name: str, tool_id: str) -> None:
        """Register a created tool."""
        if name and tool_id:
            self._created_tools[name] = tool_id

    def get_tool_id(self, name: str) -> Optional[str]:
        """Get tool ID by name."""
        return self._created_tools.get(name)

    def register_kb_doc(self, name: str, doc_id: str) -> None:
        """Register a created KB document."""
        if name and doc_id:
            self._created_kb_docs[name] = doc_id

    def get_kb_doc_id(self, name: str) -> Optional[str]:
        """Get KB doc ID by name."""
        return self._created_kb_docs.get(name)

    def get_all_created_agents(self) -> Dict[str, str]:
        """Get all created agents."""
        return self._created_agents.copy()

    def get_all_created_tools(self) -> Dict[str, str]:
        """Get all created tools."""
        return self._created_tools.copy()

    def get_all_created_kb_docs(self) -> Dict[str, str]:
        """Get all created KB documents."""
        return self._created_kb_docs.copy()
