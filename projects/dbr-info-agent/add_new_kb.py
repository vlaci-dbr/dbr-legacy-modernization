#!/usr/bin/env python3
"""
Script to add the new knowledge base to the agent's prompt config
"""

import requests
import json

API_KEY = "eeb7e217308426f2230aa4806db82fc6dabf78be1cff68ea0ef28eaffcb1450e"
AGENT_ID = "agent_0101kg36cz3qez9tjhxemsapxrg0"
BASE_URL = "https://api.elevenlabs.io/v1"

headers = {
    "xi-api-key": API_KEY,
    "Content-Type": "application/json"
}

# All KB IDs including the new one - with names
ALL_KBS = [
    {"id": "Wh7F7M3CVuAwDCyT4VaB", "name": "kb_company_info"},
    {"id": "sUgnnGNnoA4J7Gkw2vMH", "name": "kb_faq"},
    {"id": "VAkzZgplCm8J2WVuI0Mw", "name": "kb_data_security"},
    {"id": "OVzwUl2aS9d1n0G5Toum", "name": "kb_reverse_engineering"},
    {"id": "9R0NrtUthxIjvtcD4qOR", "name": "kb_coderevive"},
    {"id": "oGfeylY1bZm45HvdXqB8", "name": "kb_legacy_modernization"},
]

def main():
    url = f"{BASE_URL}/convai/agents/{AGENT_ID}"

    # Build knowledge base config
    knowledge_base_config = []
    for kb in ALL_KBS:
        knowledge_base_config.append({
            "type": "text",
            "id": kb["id"],
            "name": kb["name"],
            "usage_mode": "auto"
        })

    # Update payload - need to update the nested prompt config
    payload = {
        "conversation_config": {
            "agent": {
                "prompt": {
                    "knowledge_base": knowledge_base_config
                }
            }
        }
    }

    print("Updating agent with knowledge base configuration...")
    print(f"Adding {len(ALL_KBS)} knowledge bases")
    print(json.dumps(payload, indent=2))

    response = requests.patch(url, headers=headers, json=payload)

    if response.status_code == 200:
        print("\nSuccess! Agent updated with new knowledge base.")

        # Verify
        verify_response = requests.get(url, headers={"xi-api-key": API_KEY})
        if verify_response.status_code == 200:
            agent = verify_response.json()
            kb_list = agent.get('conversation_config', {}).get('agent', {}).get('prompt', {}).get('knowledge_base', [])
            print(f"\nAgent now has {len(kb_list)} knowledge bases:")
            for kb in kb_list:
                print(f"  - {kb.get('name', 'unknown')}: {kb.get('id')}")
    else:
        print(f"\nFailed to update agent: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    main()
