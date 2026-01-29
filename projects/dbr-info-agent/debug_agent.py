#!/usr/bin/env python3
"""
Debug script to check agent configuration
"""

import requests
import json

API_KEY = "eeb7e217308426f2230aa4806db82fc6dabf78be1cff68ea0ef28eaffcb1450e"
AGENT_ID = "agent_0101kg36cz3qez9tjhxemsapxrg0"
BASE_URL = "https://api.elevenlabs.io/v1"

headers = {
    "xi-api-key": API_KEY
}

def main():
    url = f"{BASE_URL}/convai/agents/{AGENT_ID}"
    response = requests.get(url, headers=headers)

    print("Agent Configuration:")
    print("=" * 60)
    print(json.dumps(response.json(), indent=2))

if __name__ == "__main__":
    main()
