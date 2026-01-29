#!/usr/bin/env python3
"""
Deploy script for dbr-info-agent
"""

import os
import sys
import json
from datetime import datetime

# Add lib to path
sys.path.insert(0, '/config/workspace/conversational-ai-template/lib')

from elevenlabs_client import ElevenLabsClient, ElevenLabsClientError

# Configuration
API_KEY = os.environ.get('ELEVENLABS_API_KEY', 'eeb7e217308426f2230aa4806db82fc6dabf78be1cff68ea0ef28eaffcb1450e')
PROJECT_DIR = '/config/workspace/conversational-ai-template/projects/dbr-info-agent'

def load_file(path):
    """Load file content"""
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def load_json(path):
    """Load JSON file"""
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(path, data):
    """Save JSON file"""
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def main():
    print("=" * 60)
    print("Deploy: dbr-info-agent")
    print("=" * 60)
    print()

    # Initialize client
    print("[1/4] Initializing ElevenLabs client...")
    try:
        client = ElevenLabsClient(API_KEY)

        # Validate API key
        result = client.validate_api_key()
        if result.success:
            print("  ✓ API kulcs valid")
        else:
            print(f"  ✗ API kulcs hiba: {result.error}")
            return 1
    except ElevenLabsClientError as e:
        print(f"  ✗ Client hiba: {e}")
        return 1

    # Load project config
    project = load_json(f"{PROJECT_DIR}/config/project.json")
    print(f"  ✓ Projekt betöltve: {project['name']}")
    print()

    # Upload Knowledge Bases
    print("[2/4] Knowledge Base-ek feltöltése...")
    kb_ids = {}

    for kb in project['knowledge_bases']:
        kb_id = kb['id']
        kb_name = kb['name']
        kb_file = f"{PROJECT_DIR}/{kb['file']}"

        print(f"  → Feltöltés: {kb_name}...")

        try:
            content = load_file(kb_file)
            result = client.create_knowledge_base_from_text(content, name=kb_name)

            if result.success:
                doc_id = result.data.get('id')
                kb_ids[kb_id] = doc_id
                client.register_kb_doc(kb_id, doc_id)
                print(f"    ✓ {kb_id} → {doc_id}")
            else:
                print(f"    ✗ Hiba: {result.error}")
        except Exception as e:
            print(f"    ✗ Exception: {e}")

    print()

    # Create Agent
    print("[3/4] Agent létrehozása...")
    agent_config = project['agents'][0]

    # Load prompt
    prompt_file = f"{PROJECT_DIR}/{agent_config['prompt_file']}"
    system_prompt = load_file(prompt_file)

    agent_name = agent_config['name']
    first_message = agent_config['first_message']
    voice_id = agent_config['voice']['voice_id']
    llm_model = agent_config['llm']['model']
    temperature = agent_config['llm'].get('temperature', 0.3)

    print(f"  → Agent: {agent_name}")
    print(f"  → Voice ID: {voice_id}")
    print(f"  → LLM: {llm_model}")

    # Get KB IDs for this agent
    agent_kb_ids = list(kb_ids.values())

    try:
        result = client.create_agent(
            name=agent_name,
            first_message=first_message,
            system_prompt=system_prompt,
            llm=llm_model,
            language=project['language'],
            voice_id=voice_id,
            knowledge_base_ids=agent_kb_ids
        )

        if result.success:
            agent_id = result.data.get('agent_id')
            print(f"  ✓ Agent létrehozva: {agent_id}")
        else:
            print(f"  ✗ Hiba: {result.error}")
            agent_id = None
    except Exception as e:
        print(f"  ✗ Exception: {e}")
        agent_id = None

    print()

    # Save deployment info
    print("[4/4] Deployment info mentése...")

    # Save agent IDs
    agent_ids_data = {
        "info-agent": agent_id,
        "main_agent": agent_id,
        "deployed_at": datetime.now().isoformat()
    }
    save_json(f"{PROJECT_DIR}/deployment/agent-ids.json", agent_ids_data)
    print(f"  ✓ deployment/agent-ids.json")

    # Save KB IDs
    kb_ids_data = {
        **kb_ids,
        "deployed_at": datetime.now().isoformat()
    }
    save_json(f"{PROJECT_DIR}/deployment/kb-ids.json", kb_ids_data)
    print(f"  ✓ deployment/kb-ids.json")

    print()
    print("=" * 60)
    if agent_id:
        print("Deploy SIKERES!")
        print("=" * 60)
        print()
        print("Agent ID-k:")
        print(f"  - info-agent: {agent_id}")
        print()
        print(f"Tesztelés: https://elevenlabs.io/app/conversational-ai/{agent_id}")
    else:
        print("Deploy SIKERTELEN!")
        print("=" * 60)
        return 1

    return 0

if __name__ == "__main__":
    sys.exit(main())
