#!/usr/bin/env python3
"""
Script to update knowledge base on ElevenLabs
"""

import requests
import os

API_KEY = "eeb7e217308426f2230aa4806db82fc6dabf78be1cff68ea0ef28eaffcb1450e"
AGENT_ID = "agent_0101kg36cz3qez9tjhxemsapxrg0"
BASE_URL = "https://api.elevenlabs.io/v1"

headers = {
    "xi-api-key": API_KEY
}

def read_kb_file(filepath):
    """Read knowledge base content from file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

def create_knowledge_base(name, content):
    """Create a new knowledge base"""
    url = f"{BASE_URL}/convai/knowledge-base"

    files = {
        'file': (f'{name}.md', content.encode('utf-8'), 'text/markdown')
    }
    data = {
        'name': name
    }

    response = requests.post(url, headers=headers, files=files, data=data)

    if response.status_code in [200, 201]:
        result = response.json()
        print(f"Created KB: {name} -> ID: {result.get('id', 'unknown')}")
        return result
    else:
        print(f"Failed to create KB {name}: {response.status_code}")
        print(response.text)
        return None

def get_agent():
    """Get current agent config"""
    url = f"{BASE_URL}/convai/agents/{AGENT_ID}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    return None

def update_agent_knowledge_bases(kb_ids):
    """Update agent with new knowledge base IDs"""
    url = f"{BASE_URL}/convai/agents/{AGENT_ID}"

    # Get current agent config
    agent = get_agent()
    if not agent:
        print("Failed to get agent config")
        return False

    # Prepare update payload
    payload = {
        "knowledge_base_ids": kb_ids
    }

    response = requests.patch(url, headers=headers, json=payload)

    if response.status_code == 200:
        print("Agent updated successfully with new knowledge bases")
        return True
    else:
        print(f"Failed to update agent: {response.status_code}")
        print(response.text)
        return False

def main():
    project_dir = "/config/workspace/conversational-ai-template/projects/dbr-info-agent"

    # Knowledge bases to upload (the new comprehensive one)
    kb_files = {
        "kb-legacy-modernization": f"{project_dir}/knowledge-bases/kb-legacy-modernization.md"
    }

    print("=" * 60)
    print("Uploading new knowledge base to ElevenLabs")
    print("=" * 60)

    # Upload the new KB
    new_kb_ids = []
    for kb_name, kb_path in kb_files.items():
        print(f"\nUploading: {kb_name}")
        content = read_kb_file(kb_path)
        result = create_knowledge_base(kb_name, content)
        if result and 'id' in result:
            new_kb_ids.append(result['id'])

    # Get existing KB IDs from agent
    print("\n" + "=" * 60)
    print("Getting current agent configuration...")
    agent = get_agent()
    if agent:
        existing_kb_ids = agent.get('knowledge_base', [])
        if isinstance(existing_kb_ids, list):
            # Extract IDs if they are objects
            existing_ids = []
            for kb in existing_kb_ids:
                if isinstance(kb, dict):
                    existing_ids.append(kb.get('id', kb.get('knowledge_base_id')))
                else:
                    existing_ids.append(kb)
            existing_kb_ids = [id for id in existing_ids if id]
        print(f"Existing KB IDs: {existing_kb_ids}")

        # Combine existing and new
        all_kb_ids = existing_kb_ids + new_kb_ids
        print(f"All KB IDs (combined): {all_kb_ids}")

        # Update agent
        print("\n" + "=" * 60)
        print("Updating agent with all knowledge bases...")
        update_agent_knowledge_bases(all_kb_ids)
    else:
        print("Could not retrieve agent config, adding only new KB")
        update_agent_knowledge_bases(new_kb_ids)

    print("\n" + "=" * 60)
    print("New KB IDs created:")
    for kb_id in new_kb_ids:
        print(f"  - {kb_id}")
    print("=" * 60)

if __name__ == "__main__":
    main()
