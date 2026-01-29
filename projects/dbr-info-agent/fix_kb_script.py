#!/usr/bin/env python3
"""
Script to fix knowledge bases - add all KB IDs to agent
"""

import requests

API_KEY = "eeb7e217308426f2230aa4806db82fc6dabf78be1cff68ea0ef28eaffcb1450e"
AGENT_ID = "agent_0101kg36cz3qez9tjhxemsapxrg0"
BASE_URL = "https://api.elevenlabs.io/v1"

headers = {
    "xi-api-key": API_KEY
}

# Previous KB IDs from initial deployment + new one
ALL_KB_IDS = [
    "Wh7F7M3CVuAwDCyT4VaB",  # kb-company-info
    "sUgnnGNnoA4J7Gkw2vMH",  # kb-faq
    "VAkzZgplCm8J2WVuI0Mw",  # kb-data-security
    "OVzwUl2aS9d1n0G5Toum",  # kb-reverse-engineering
    "9R0NrtUthxIjvtcD4qOR",  # kb-coderevive (original)
    "oGfeylY1bZm45HvdXqB8",  # kb-legacy-modernization (NEW)
]

def get_agent():
    """Get current agent config"""
    url = f"{BASE_URL}/convai/agents/{AGENT_ID}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    return None

def update_agent_knowledge_bases(kb_ids):
    """Update agent with knowledge base IDs"""
    url = f"{BASE_URL}/convai/agents/{AGENT_ID}"

    payload = {
        "knowledge_base_ids": kb_ids
    }

    response = requests.patch(url, headers=headers, json=payload)

    if response.status_code == 200:
        print("Agent updated successfully with all knowledge bases")
        return True
    else:
        print(f"Failed to update agent: {response.status_code}")
        print(response.text)
        return False

def main():
    print("=" * 60)
    print("Updating agent with ALL knowledge bases")
    print("=" * 60)

    print("\nKB IDs to add:")
    for kb_id in ALL_KB_IDS:
        print(f"  - {kb_id}")

    print("\nUpdating agent...")
    update_agent_knowledge_bases(ALL_KB_IDS)

    # Verify
    print("\n" + "=" * 60)
    print("Verifying agent configuration...")
    agent = get_agent()
    if agent:
        kb_list = agent.get('knowledge_base', [])
        print(f"Agent now has {len(kb_list)} knowledge bases")
        for kb in kb_list:
            if isinstance(kb, dict):
                print(f"  - {kb.get('name', 'unknown')}: {kb.get('id', 'unknown')}")

if __name__ == "__main__":
    main()
