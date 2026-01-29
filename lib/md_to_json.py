"""
Markdown to JSON Converter

Converts knowledge base markdown files to structured JSON format.
"""

import re
import json
from pathlib import Path
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Section:
    """Represents a section in the markdown document"""
    title: str
    level: int
    content: str = ""
    items: List[str] = field(default_factory=list)
    subsections: List["Section"] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        result: Dict[str, Any] = {"title": self.title}

        if self.content and not self.items:
            result["content"] = self.content
        elif self.items:
            result["items"] = self.items
            if self.content:
                result["content"] = self.content

        if self.subsections:
            result["subsections"] = [s.to_dict() for s in self.subsections]

        return result


class MarkdownToJsonConverter:
    """Converts markdown knowledge base files to JSON format"""

    def __init__(self):
        self._heading_pattern = re.compile(r"^(#{1,6})\s+(.+)$")
        self._list_item_pattern = re.compile(r"^[-*+]\s+(.+)$")
        self._numbered_item_pattern = re.compile(r"^\d+\.\s+(.+)$")

    def convert(
        self,
        markdown_content: str,
        kb_id: Optional[str] = None,
        kb_type: str = "domain-knowledge",
        language: str = "hu"
    ) -> Dict[str, Any]:
        """
        Convert markdown content to structured JSON.

        Args:
            markdown_content: Markdown content to convert
            kb_id: Knowledge base identifier
            kb_type: Type of knowledge base
            language: Language code

        Returns:
            Structured JSON representation
        """
        lines = markdown_content.split("\n")
        sections = self._parse_sections(lines)

        # Extract document name from first H1
        doc_name = kb_id or "knowledge-base"
        for section in sections:
            if section.level == 1:
                doc_name = section.title
                break

        # Filter out H1 from sections (it becomes the document name)
        filtered_sections = [s for s in sections if s.level > 1]

        result: Dict[str, Any] = {
            "id": kb_id or self._generate_id(doc_name),
            "name": doc_name,
            "type": kb_type,
            "language": language,
            "sections": [self._section_to_json(s) for s in filtered_sections],
            "metadata": {
                "version": "1.0.0",
                "last_updated": datetime.now().isoformat()
            }
        }

        return result

    def _generate_id(self, name: str) -> str:
        """Generate an ID from a name"""
        # Convert to lowercase, replace spaces with hyphens
        id_str = name.lower()
        id_str = re.sub(r"[^a-z0-9\s-]", "", id_str)
        id_str = re.sub(r"\s+", "-", id_str)
        id_str = re.sub(r"-+", "-", id_str)
        id_str = id_str.strip("-")

        if not id_str.startswith("kb-"):
            id_str = f"kb-{id_str}"

        return id_str

    def _parse_sections(self, lines: List[str]) -> List[Section]:
        """Parse markdown lines into sections"""
        sections: List[Section] = []
        current_section: Optional[Section] = None
        content_buffer: List[str] = []
        items_buffer: List[str] = []

        def flush_buffers():
            nonlocal current_section, content_buffer, items_buffer
            if current_section:
                if content_buffer:
                    current_section.content = "\n".join(content_buffer).strip()
                if items_buffer:
                    current_section.items = items_buffer.copy()
            content_buffer = []
            items_buffer = []

        for line in lines:
            heading_match = self._heading_pattern.match(line)

            if heading_match:
                flush_buffers()

                level = len(heading_match.group(1))
                title = heading_match.group(2).strip()

                new_section = Section(title=title, level=level)

                if current_section is None or level == 1:
                    sections.append(new_section)
                elif level > current_section.level:
                    current_section.subsections.append(new_section)
                else:
                    # Find appropriate parent
                    parent = self._find_parent(sections, level)
                    if parent:
                        parent.subsections.append(new_section)
                    else:
                        sections.append(new_section)

                current_section = new_section
                continue

            list_match = self._list_item_pattern.match(line) or self._numbered_item_pattern.match(line)

            if list_match:
                items_buffer.append(list_match.group(1).strip())
                continue

            # Regular content
            stripped = line.strip()
            if stripped:
                content_buffer.append(stripped)

        flush_buffers()
        return sections

    def _find_parent(self, sections: List[Section], level: int) -> Optional[Section]:
        """Find the appropriate parent section for a given level"""
        if not sections:
            return None

        # Look in the last section and its subsections
        last = sections[-1]

        def find_in_section(section: Section) -> Optional[Section]:
            if section.level < level:
                if section.subsections:
                    result = find_in_section(section.subsections[-1])
                    if result:
                        return result
                return section
            return None

        return find_in_section(last)

    def _section_to_json(self, section: Section) -> Dict[str, Any]:
        """Convert a section to JSON representation"""
        result: Dict[str, Any] = {"title": section.title}

        if section.content:
            result["content"] = section.content

        if section.items:
            result["items"] = section.items

        if section.subsections:
            result["subsections"] = [self._section_to_json(s) for s in section.subsections]

        return result

    def convert_file(
        self,
        input_path: str,
        output_path: Optional[str] = None,
        kb_type: str = "domain-knowledge",
        language: str = "hu"
    ) -> Dict[str, Any]:
        """
        Convert a markdown file to JSON.

        Args:
            input_path: Path to input markdown file
            output_path: Path to output JSON file (optional)
            kb_type: Type of knowledge base
            language: Language code

        Returns:
            Converted JSON data
        """
        input_file = Path(input_path)

        if not input_file.exists():
            raise FileNotFoundError(f"Input file not found: {input_path}")

        with open(input_file, "r", encoding="utf-8") as f:
            content = f.read()

        # Generate KB ID from filename
        kb_id = f"kb-{input_file.stem}"
        if kb_id.startswith("kb-kb-"):
            kb_id = kb_id[3:]  # Remove duplicate kb- prefix

        result = self.convert(content, kb_id=kb_id, kb_type=kb_type, language=language)

        if output_path:
            output_file = Path(output_path)
            output_file.parent.mkdir(parents=True, exist_ok=True)

            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(result, f, indent=2, ensure_ascii=False)

        return result

    def convert_directory(
        self,
        input_dir: str,
        output_dir: str,
        kb_type: str = "domain-knowledge",
        language: str = "hu"
    ) -> List[Dict[str, Any]]:
        """
        Convert all markdown files in a directory to JSON.

        Args:
            input_dir: Path to input directory
            output_dir: Path to output directory
            kb_type: Type of knowledge base
            language: Language code

        Returns:
            List of converted JSON data
        """
        input_path = Path(input_dir)
        output_path = Path(output_dir)

        if not input_path.exists():
            raise FileNotFoundError(f"Input directory not found: {input_dir}")

        output_path.mkdir(parents=True, exist_ok=True)

        results = []

        for md_file in input_path.glob("*.md"):
            json_file = output_path / f"{md_file.stem}.json"
            result = self.convert_file(
                str(md_file),
                str(json_file),
                kb_type=kb_type,
                language=language
            )
            results.append(result)

        return results


def convert_kb_to_json(
    markdown_content: str,
    kb_id: Optional[str] = None,
    kb_type: str = "domain-knowledge",
    language: str = "hu"
) -> Dict[str, Any]:
    """
    Convenience function to convert markdown to JSON.

    Args:
        markdown_content: Markdown content
        kb_id: Knowledge base identifier
        kb_type: Type of knowledge base
        language: Language code

    Returns:
        Structured JSON representation
    """
    converter = MarkdownToJsonConverter()
    return converter.convert(markdown_content, kb_id, kb_type, language)
