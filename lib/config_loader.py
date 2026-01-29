"""
Configuration Loader

Handles loading and managing project configurations.
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field


class ConfigError(Exception):
    """Configuration error"""
    pass


@dataclass
class ProjectConfig:
    """Project configuration container"""
    id: str
    name: str
    language: str
    agents: List[Dict[str, Any]]
    description: Optional[str] = None
    company: Optional[Dict[str, Any]] = None
    knowledge_bases: List[Dict[str, Any]] = field(default_factory=list)
    workflow: Optional[Dict[str, Any]] = None
    version: str = "1.0.0"

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ProjectConfig":
        """Create ProjectConfig from dictionary"""
        return cls(
            id=data["id"],
            name=data["name"],
            language=data.get("language", "hu"),
            agents=data.get("agents", []),
            description=data.get("description"),
            company=data.get("company"),
            knowledge_bases=data.get("knowledge_bases", []),
            workflow=data.get("workflow"),
            version=data.get("version", "1.0.0")
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        result = {
            "id": self.id,
            "name": self.name,
            "language": self.language,
            "agents": self.agents,
            "version": self.version
        }
        if self.description:
            result["description"] = self.description
        if self.company:
            result["company"] = self.company
        if self.knowledge_bases:
            result["knowledge_bases"] = self.knowledge_bases
        if self.workflow:
            result["workflow"] = self.workflow
        return result


class ConfigLoader:
    """Configuration loader for voice agent projects"""

    def __init__(self, framework_root: Optional[str] = None):
        """
        Initialize the config loader.

        Args:
            framework_root: Path to framework root directory.
                           If None, uses environment variable or current directory.
        """
        if framework_root:
            self._framework_root = Path(framework_root)
        else:
            env_root = os.environ.get("CAI_FRAMEWORK_ROOT")
            if env_root:
                self._framework_root = Path(env_root)
            else:
                self._framework_root = Path.cwd()

        self._cache: Dict[str, Any] = {}

    @property
    def framework_root(self) -> Path:
        """Get framework root path"""
        return self._framework_root

    @property
    def schemas_dir(self) -> Path:
        """Get schemas directory path"""
        return self._framework_root / "framework" / "schemas"

    @property
    def templates_dir(self) -> Path:
        """Get templates directory path"""
        return self._framework_root / "framework" / "templates"

    @property
    def defaults_dir(self) -> Path:
        """Get defaults directory path"""
        return self._framework_root / "framework" / "defaults"

    @property
    def projects_dir(self) -> Path:
        """Get projects directory path"""
        return self._framework_root / "projects"

    def clear_cache(self):
        """Clear the configuration cache"""
        self._cache.clear()

    def _load_json(self, path: Path, use_cache: bool = True) -> Dict[str, Any]:
        """
        Load a JSON file.

        Args:
            path: Path to JSON file
            use_cache: Whether to use cache

        Returns:
            Parsed JSON data

        Raises:
            ConfigError: If file cannot be loaded
        """
        cache_key = str(path)

        if use_cache and cache_key in self._cache:
            return self._cache[cache_key]

        if not path.exists():
            raise ConfigError(f"Config file not found: {path}")

        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)

            if use_cache:
                self._cache[cache_key] = data

            return data
        except json.JSONDecodeError as e:
            raise ConfigError(f"Invalid JSON in {path}: {e}")
        except IOError as e:
            raise ConfigError(f"Cannot read {path}: {e}")

    def _load_text(self, path: Path) -> str:
        """
        Load a text file.

        Args:
            path: Path to text file

        Returns:
            File content

        Raises:
            ConfigError: If file cannot be loaded
        """
        if not path.exists():
            raise ConfigError(f"File not found: {path}")

        try:
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        except IOError as e:
            raise ConfigError(f"Cannot read {path}: {e}")

    def load_schema(self, schema_name: str) -> Dict[str, Any]:
        """
        Load a JSON schema.

        Args:
            schema_name: Schema name (e.g., "project", "agent")

        Returns:
            Schema definition
        """
        if not schema_name.endswith(".schema.json"):
            schema_name = f"{schema_name}.schema.json"

        return self._load_json(self.schemas_dir / schema_name)

    def load_default(self, default_name: str) -> Dict[str, Any]:
        """
        Load a default configuration.

        Args:
            default_name: Default name (e.g., "llm-settings", "voices")

        Returns:
            Default configuration
        """
        if not default_name.endswith(".json"):
            default_name = f"{default_name}.json"

        return self._load_json(self.defaults_dir / default_name)

    def load_project_template(self, template_name: str) -> Dict[str, Any]:
        """
        Load a project template.

        Args:
            template_name: Template name (e.g., "customer-service")

        Returns:
            Project template
        """
        if not template_name.endswith(".json"):
            template_name = f"{template_name}.json"

        return self._load_json(self.templates_dir / "projects" / template_name)

    def load_workflow_template(self, template_name: str) -> Dict[str, Any]:
        """
        Load a workflow template.

        Args:
            template_name: Template name (e.g., "linear", "branching")

        Returns:
            Workflow template
        """
        if not template_name.endswith(".json"):
            template_name = f"{template_name}.json"

        return self._load_json(self.templates_dir / "workflows" / template_name)

    def load_agent_template(self, template_name: str) -> str:
        """
        Load an agent prompt template.

        Args:
            template_name: Template name (e.g., "orchestrator", "specialist")

        Returns:
            Agent prompt template content
        """
        if not template_name.endswith(".md"):
            template_name = f"{template_name}.md"

        return self._load_text(self.templates_dir / "agents" / template_name)

    def load_kb_template(self, template_name: str) -> str:
        """
        Load a knowledge base template.

        Args:
            template_name: Template name (e.g., "faq", "company-info")

        Returns:
            KB template content
        """
        if not template_name.endswith(".md"):
            template_name = f"{template_name}.md"

        return self._load_text(self.templates_dir / "knowledge-bases" / template_name)

    def load_snippet(self, snippet_name: str) -> str:
        """
        Load an agent prompt snippet.

        Args:
            snippet_name: Snippet name (e.g., "common-guardrails")

        Returns:
            Snippet content
        """
        if not snippet_name.endswith(".md"):
            snippet_name = f"{snippet_name}.md"

        return self._load_text(self.templates_dir / "agents" / "snippets" / snippet_name)

    def load_project(self, project_id: str) -> ProjectConfig:
        """
        Load a project configuration.

        Args:
            project_id: Project identifier

        Returns:
            ProjectConfig object
        """
        project_dir = self.projects_dir / project_id
        config_path = project_dir / "config" / "project.json"

        data = self._load_json(config_path, use_cache=False)
        return ProjectConfig.from_dict(data)

    def load_project_workflow(self, project_id: str) -> Dict[str, Any]:
        """
        Load a project's workflow configuration.

        Args:
            project_id: Project identifier

        Returns:
            Workflow configuration
        """
        project_dir = self.projects_dir / project_id
        workflow_path = project_dir / "config" / "workflow.json"

        return self._load_json(workflow_path, use_cache=False)

    def load_project_agent(self, project_id: str, agent_id: str) -> str:
        """
        Load a project's agent prompt.

        Args:
            project_id: Project identifier
            agent_id: Agent identifier

        Returns:
            Agent prompt content
        """
        project_dir = self.projects_dir / project_id
        agent_path = project_dir / "agents" / f"{agent_id}.md"

        return self._load_text(agent_path)

    def load_project_kb(self, project_id: str, kb_id: str) -> str:
        """
        Load a project's knowledge base content.

        Args:
            project_id: Project identifier
            kb_id: Knowledge base identifier

        Returns:
            KB content
        """
        project_dir = self.projects_dir / project_id
        kb_path = project_dir / "knowledge-bases" / f"{kb_id}.md"

        return self._load_text(kb_path)

    def list_projects(self) -> List[str]:
        """
        List all available projects.

        Returns:
            List of project IDs
        """
        if not self.projects_dir.exists():
            return []

        projects = []
        for item in self.projects_dir.iterdir():
            if item.is_dir() and (item / "config" / "project.json").exists():
                projects.append(item.name)

        return sorted(projects)

    def list_project_templates(self) -> List[str]:
        """
        List all available project templates.

        Returns:
            List of template names
        """
        templates_path = self.templates_dir / "projects"
        if not templates_path.exists():
            return []

        templates = []
        for item in templates_path.iterdir():
            if item.is_file() and item.suffix == ".json":
                templates.append(item.stem)

        return sorted(templates)

    def list_workflow_templates(self) -> List[str]:
        """
        List all available workflow templates.

        Returns:
            List of template names
        """
        templates_path = self.templates_dir / "workflows"
        if not templates_path.exists():
            return []

        templates = []
        for item in templates_path.iterdir():
            if item.is_file() and item.suffix == ".json":
                templates.append(item.stem)

        return sorted(templates)

    def save_project(self, config: ProjectConfig) -> Path:
        """
        Save a project configuration.

        Args:
            config: ProjectConfig object

        Returns:
            Path to saved config file
        """
        project_dir = self.projects_dir / config.id
        config_dir = project_dir / "config"
        config_dir.mkdir(parents=True, exist_ok=True)

        config_path = config_dir / "project.json"

        try:
            with open(config_path, "w", encoding="utf-8") as f:
                json.dump(config.to_dict(), f, indent=2, ensure_ascii=False)
            return config_path
        except IOError as e:
            raise ConfigError(f"Cannot save config: {e}")

    def save_workflow(self, project_id: str, workflow: Dict[str, Any]) -> Path:
        """
        Save a project's workflow configuration.

        Args:
            project_id: Project identifier
            workflow: Workflow configuration

        Returns:
            Path to saved workflow file
        """
        project_dir = self.projects_dir / project_id
        config_dir = project_dir / "config"
        config_dir.mkdir(parents=True, exist_ok=True)

        workflow_path = config_dir / "workflow.json"

        try:
            with open(workflow_path, "w", encoding="utf-8") as f:
                json.dump(workflow, f, indent=2, ensure_ascii=False)
            return workflow_path
        except IOError as e:
            raise ConfigError(f"Cannot save workflow: {e}")

    def save_agent(self, project_id: str, agent_id: str, content: str) -> Path:
        """
        Save a project's agent prompt.

        Args:
            project_id: Project identifier
            agent_id: Agent identifier
            content: Agent prompt content

        Returns:
            Path to saved agent file
        """
        project_dir = self.projects_dir / project_id
        agents_dir = project_dir / "agents"
        agents_dir.mkdir(parents=True, exist_ok=True)

        agent_path = agents_dir / f"{agent_id}.md"

        try:
            with open(agent_path, "w", encoding="utf-8") as f:
                f.write(content)
            return agent_path
        except IOError as e:
            raise ConfigError(f"Cannot save agent: {e}")

    def save_kb(self, project_id: str, kb_id: str, content: str) -> Path:
        """
        Save a project's knowledge base content.

        Args:
            project_id: Project identifier
            kb_id: Knowledge base identifier
            content: KB content

        Returns:
            Path to saved KB file
        """
        project_dir = self.projects_dir / project_id
        kb_dir = project_dir / "knowledge-bases"
        kb_dir.mkdir(parents=True, exist_ok=True)

        kb_path = kb_dir / f"{kb_id}.md"

        try:
            with open(kb_path, "w", encoding="utf-8") as f:
                f.write(content)
            return kb_path
        except IOError as e:
            raise ConfigError(f"Cannot save KB: {e}")

    def get_env_variable(self, name: str, default: Optional[str] = None) -> Optional[str]:
        """
        Get an environment variable value.

        Args:
            name: Variable name
            default: Default value if not set

        Returns:
            Variable value or default
        """
        return os.environ.get(name, default)

    def load_env_file(self, env_file: Optional[str] = None) -> Dict[str, str]:
        """
        Load environment variables from .env file.

        Args:
            env_file: Path to .env file. If None, uses .env in framework root.

        Returns:
            Dictionary of loaded variables
        """
        if env_file:
            env_path = Path(env_file)
        else:
            env_path = self._framework_root / ".env"

        if not env_path.exists():
            return {}

        variables: Dict[str, str] = {}

        try:
            with open(env_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    if "=" in line:
                        key, value = line.split("=", 1)
                        key = key.strip()
                        value = value.strip().strip('"').strip("'")
                        variables[key] = value
                        os.environ[key] = value
        except IOError:
            pass

        return variables
