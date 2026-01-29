"""
Schema Validator

Validates configurations against JSON schemas.
"""

import json
from pathlib import Path
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field


class ValidationError(Exception):
    """Validation error with details"""
    def __init__(self, message: str, errors: Optional[List[str]] = None):
        super().__init__(message)
        self.errors = errors or []


@dataclass
class ValidationResult:
    """Validation result container"""
    valid: bool
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

    def add_error(self, error: str):
        """Add an error"""
        self.errors.append(error)
        self.valid = False

    def add_warning(self, warning: str):
        """Add a warning"""
        self.warnings.append(warning)

    def merge(self, other: "ValidationResult"):
        """Merge another validation result"""
        self.errors.extend(other.errors)
        self.warnings.extend(other.warnings)
        if not other.valid:
            self.valid = False


class SchemaValidator:
    """JSON Schema validator for voice agent configurations"""

    def __init__(self, schemas_dir: Optional[str] = None):
        """
        Initialize the validator.

        Args:
            schemas_dir: Path to schemas directory.
                        If None, uses default location.
        """
        if schemas_dir:
            self._schemas_dir = Path(schemas_dir)
        else:
            self._schemas_dir = Path.cwd() / "framework" / "schemas"

        self._schemas: Dict[str, Dict[str, Any]] = {}
        self._jsonschema_available = self._check_jsonschema()

    def _check_jsonschema(self) -> bool:
        """Check if jsonschema library is available"""
        try:
            import jsonschema
            return True
        except ImportError:
            return False

    def _load_schema(self, schema_name: str) -> Dict[str, Any]:
        """Load a schema by name"""
        if schema_name in self._schemas:
            return self._schemas[schema_name]

        if not schema_name.endswith(".schema.json"):
            schema_name = f"{schema_name}.schema.json"

        schema_path = self._schemas_dir / schema_name

        if not schema_path.exists():
            raise ValidationError(f"Schema not found: {schema_name}")

        try:
            with open(schema_path, "r", encoding="utf-8") as f:
                schema = json.load(f)
            self._schemas[schema_name] = schema
            return schema
        except json.JSONDecodeError as e:
            raise ValidationError(f"Invalid schema JSON: {e}")
        except IOError as e:
            raise ValidationError(f"Cannot read schema: {e}")

    def validate(
        self,
        data: Dict[str, Any],
        schema_name: str
    ) -> ValidationResult:
        """
        Validate data against a schema.

        Args:
            data: Data to validate
            schema_name: Schema name (e.g., "project", "agent")

        Returns:
            ValidationResult
        """
        result = ValidationResult(valid=True)

        if not self._jsonschema_available:
            result.add_warning("jsonschema library not available, using basic validation")
            return self._basic_validate(data, schema_name, result)

        try:
            import jsonschema

            schema = self._load_schema(schema_name)

            validator = jsonschema.Draft7Validator(schema)
            errors = list(validator.iter_errors(data))

            for error in errors:
                path = ".".join(str(p) for p in error.absolute_path) or "(root)"
                result.add_error(f"{path}: {error.message}")

        except ValidationError as e:
            result.add_error(str(e))
        except Exception as e:
            result.add_error(f"Validation error: {e}")

        return result

    def _basic_validate(
        self,
        data: Dict[str, Any],
        schema_name: str,
        result: ValidationResult
    ) -> ValidationResult:
        """
        Basic validation without jsonschema library.

        Args:
            data: Data to validate
            schema_name: Schema name
            result: ValidationResult to update

        Returns:
            Updated ValidationResult
        """
        if schema_name in ("project", "project.schema.json"):
            return self._validate_project(data, result)
        elif schema_name in ("agent", "agent.schema.json"):
            return self._validate_agent(data, result)
        elif schema_name in ("workflow", "workflow.schema.json"):
            return self._validate_workflow(data, result)
        elif schema_name in ("knowledge-base", "knowledge-base.schema.json"):
            return self._validate_kb(data, result)
        else:
            result.add_warning(f"No basic validation available for schema: {schema_name}")

        return result

    def _validate_project(
        self,
        data: Dict[str, Any],
        result: ValidationResult
    ) -> ValidationResult:
        """Basic validation for project config"""
        required = ["id", "name", "language", "agents"]

        for field in required:
            if field not in data:
                result.add_error(f"Missing required field: {field}")

        if "id" in data:
            id_val = data["id"]
            if not isinstance(id_val, str) or not id_val:
                result.add_error("id must be a non-empty string")
            elif not all(c.isalnum() or c == "-" for c in id_val):
                result.add_error("id must be kebab-case (lowercase letters, numbers, hyphens)")

        if "language" in data:
            allowed_langs = ["hu", "en", "de", "fr", "es", "it"]
            if data["language"] not in allowed_langs:
                result.add_error(f"language must be one of: {allowed_langs}")

        if "agents" in data:
            if not isinstance(data["agents"], list) or len(data["agents"]) == 0:
                result.add_error("agents must be a non-empty array")

        return result

    def _validate_agent(
        self,
        data: Dict[str, Any],
        result: ValidationResult
    ) -> ValidationResult:
        """Basic validation for agent config"""
        required = ["id", "name", "role", "voice"]

        for field in required:
            if field not in data:
                result.add_error(f"Missing required field: {field}")

        if "role" in data:
            allowed_roles = ["orchestrator", "specialist", "finalizer"]
            if data["role"] not in allowed_roles:
                result.add_error(f"role must be one of: {allowed_roles}")

        if "role" in data and data["role"] == "orchestrator":
            if "first_message" not in data:
                result.add_error("orchestrator role requires first_message")

        if "voice" in data:
            if not isinstance(data["voice"], dict):
                result.add_error("voice must be an object")
            elif "voice_id" not in data["voice"]:
                result.add_error("voice.voice_id is required")

        return result

    def _validate_workflow(
        self,
        data: Dict[str, Any],
        result: ValidationResult
    ) -> ValidationResult:
        """Basic validation for workflow config"""
        if "workflow" not in data:
            result.add_error("Missing required field: workflow")
            return result

        workflow = data["workflow"]

        if "nodes" not in workflow:
            result.add_error("Missing required field: workflow.nodes")
        if "edges" not in workflow:
            result.add_error("Missing required field: workflow.edges")

        if "nodes" in workflow:
            nodes = workflow["nodes"]
            start_count = 0

            for node_id, node in nodes.items():
                if not isinstance(node, dict):
                    result.add_error(f"Node {node_id} must be an object")
                    continue

                if "type" not in node:
                    result.add_error(f"Node {node_id} missing type")
                elif node["type"] == "start":
                    start_count += 1
                elif node["type"] not in ["start", "override_agent"]:
                    result.add_error(f"Node {node_id} has invalid type: {node['type']}")

                if "label" not in node:
                    result.add_error(f"Node {node_id} missing label")

            if start_count == 0:
                result.add_error("Workflow must have exactly one start node")
            elif start_count > 1:
                result.add_error(f"Workflow has {start_count} start nodes (should be 1)")

        if "edges" in workflow and "nodes" in workflow:
            nodes = workflow["nodes"]
            edges = workflow["edges"]

            for edge_id, edge in edges.items():
                if not isinstance(edge, dict):
                    result.add_error(f"Edge {edge_id} must be an object")
                    continue

                for field in ["source", "target", "forward_condition"]:
                    if field not in edge:
                        result.add_error(f"Edge {edge_id} missing {field}")

                if "source" in edge and edge["source"] not in nodes:
                    result.add_error(f"Edge {edge_id} source '{edge['source']}' not found")
                if "target" in edge and edge["target"] not in nodes:
                    result.add_error(f"Edge {edge_id} target '{edge['target']}' not found")

        return result

    def _validate_kb(
        self,
        data: Dict[str, Any],
        result: ValidationResult
    ) -> ValidationResult:
        """Basic validation for knowledge base config"""
        required = ["id", "name", "type"]

        for field in required:
            if field not in data:
                result.add_error(f"Missing required field: {field}")

        if "id" in data:
            id_val = data["id"]
            if not isinstance(id_val, str) or not id_val.startswith("kb-"):
                result.add_error("id must start with 'kb-' prefix")

        if "type" in data:
            allowed_types = ["faq", "product-catalog", "company-info", "procedures", "domain-knowledge"]
            if data["type"] not in allowed_types:
                result.add_error(f"type must be one of: {allowed_types}")

        has_source = "source_file" in data
        has_content = "content" in data

        if not has_source and not has_content:
            result.add_error("Either source_file or content is required")

        return result

    def validate_project(self, data: Dict[str, Any]) -> ValidationResult:
        """Validate project configuration"""
        return self.validate(data, "project")

    def validate_agent(self, data: Dict[str, Any]) -> ValidationResult:
        """Validate agent configuration"""
        return self.validate(data, "agent")

    def validate_workflow(self, data: Dict[str, Any]) -> ValidationResult:
        """Validate workflow configuration"""
        return self.validate(data, "workflow")

    def validate_knowledge_base(self, data: Dict[str, Any]) -> ValidationResult:
        """Validate knowledge base configuration"""
        return self.validate(data, "knowledge-base")

    def validate_all(
        self,
        project: Dict[str, Any],
        workflow: Optional[Dict[str, Any]] = None
    ) -> ValidationResult:
        """
        Validate a complete project with all its components.

        Args:
            project: Project configuration
            workflow: Optional workflow configuration

        Returns:
            Combined ValidationResult
        """
        result = ValidationResult(valid=True)

        # Validate project
        project_result = self.validate_project(project)
        result.merge(project_result)

        # Validate each agent
        if "agents" in project and isinstance(project["agents"], list):
            for i, agent in enumerate(project["agents"]):
                agent_result = self.validate_agent(agent)
                for error in agent_result.errors:
                    result.add_error(f"agents[{i}].{error}")
                result.warnings.extend(agent_result.warnings)

        # Validate each knowledge base
        if "knowledge_bases" in project and isinstance(project["knowledge_bases"], list):
            for i, kb in enumerate(project["knowledge_bases"]):
                kb_result = self.validate_knowledge_base(kb)
                for error in kb_result.errors:
                    result.add_error(f"knowledge_bases[{i}].{error}")
                result.warnings.extend(kb_result.warnings)

        # Validate workflow if provided
        if workflow:
            workflow_result = self.validate_workflow(workflow)
            for error in workflow_result.errors:
                result.add_error(f"workflow.{error}")
            result.warnings.extend(workflow_result.warnings)

        # Cross-reference validation
        result.merge(self._validate_cross_references(project, workflow))

        return result

    def _validate_cross_references(
        self,
        project: Dict[str, Any],
        workflow: Optional[Dict[str, Any]]
    ) -> ValidationResult:
        """Validate cross-references between project components"""
        result = ValidationResult(valid=True)

        # Collect agent IDs
        agent_ids = set()
        if "agents" in project and isinstance(project["agents"], list):
            for agent in project["agents"]:
                if "id" in agent:
                    agent_ids.add(agent["id"])

        # Collect KB IDs
        kb_ids = set()
        if "knowledge_bases" in project and isinstance(project["knowledge_bases"], list):
            for kb in project["knowledge_bases"]:
                if "id" in kb:
                    kb_ids.add(kb["id"])

        # Check agent KB references
        if "agents" in project and isinstance(project["agents"], list):
            for agent in project["agents"]:
                if "knowledge_bases" in agent:
                    for kb_ref in agent["knowledge_bases"]:
                        if kb_ref not in kb_ids:
                            result.add_error(
                                f"Agent '{agent.get('id', '?')}' references "
                                f"unknown KB: {kb_ref}"
                            )

        # Check workflow node references
        if workflow and "workflow" in workflow:
            wf = workflow["workflow"]
            if "nodes" in wf:
                for node_id, node in wf["nodes"].items():
                    if node.get("type") == "override_agent":
                        # Node label typically matches agent name, not ID
                        # This is a warning, not an error
                        pass

        return result
