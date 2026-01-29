# Workflow Generálási Útmutató

## Áttekintés

Ez az útmutató elmagyarázza, hogyan generálj ElevenLabs native workflow JSON-t.

---

## Döntési Fa: Melyik Workflow Típust Használd?

```
Hány agent van?
├── 2 agent → Transfer Tool (transfer-tool.json)
├── 3+ agent, egyszerű lánc → Linear (linear.json)
├── 3+ agent, elágazó → Branching (branching.json)
└── 3+ agent, vissza lehet térni → Hub-and-Spoke (hub-and-spoke.json)
```

---

## Workflow Típusok

| Típus | Template | Mikor használd |
|-------|----------|----------------|
| **Linear** | `linear.json` | Egyszerű lánc: A → B → C |
| **Branching** | `branching.json` | Elágazó: O → [S1\|S2\|S3] → F |
| **Hub-and-Spoke** | `hub-and-spoke.json` | Visszatérős: O ↔ S1, O ↔ S2 |
| **Transfer Tool** | `transfer-tool.json` | 2 agent, egyszerű transfer |

---

## Generálási Folyamat

### 1. Workflow típus kiválasztása

Kérdezd meg:
- Hány agent lesz?
- Van-e elágazás?
- Vissza lehet-e térni az orchestrator-hoz?
- Van-e finalizer?

### 2. Template beolvasása

Olvasd be a megfelelő template fájlt:
```
framework/templates/workflows/<tipus>.json
```

### 3. Node-ok generálása

Minden agent-hez:

1. **Egyedi node ID generálása**
   - Formátum: `node_<agent-id>`
   - Példa: `node_receptionist`, `node_health_specialist`

2. **Pozíció beállítása**
   ```
   Start:        x: 400, y: 50
   Orchestrator: x: 400, y: 200
   Specialists:  x: 100/400/700, y: 450
   Finalizer:    x: 400, y: 700
   ```

3. **conversation_config kitöltése**
   - `voice_id`: voices.json-ból
   - `prompt`: az agent prompt fájlból
   - `llm`: llm-settings.json-ból
   - `first_message`: csak orchestrator-nál

### 4. Edge-ek generálása

Minden átmenethez:

1. **Egyedi edge ID generálása**
   - Formátum: `edge_<source>_to_<target>`
   - Példa: `edge_orchestrator_to_health`

2. **Source és target beállítása**
   - Source: honnan indul
   - Target: hova érkezik

3. **Condition definiálása**
   - `unconditional`: mindig (start → orchestrator)
   - `llm`: természetes nyelvi feltétel

### 5. Condition szövegek írása

A condition mezőnek **természetes nyelvű** utasításnak kell lennie:

**JÓ példák:**
```
"Ha az ügyfél egészségügyi kárról vagy balesetről beszél."
"Ha az adatgyűjtés befejeződött és minden kötelező mezőt megkaptunk."
"Ha az ügyfél gépjármű kárról beszél."
"Ha az ügyfélnek más témában is van kérdése."
```

**ROSSZ példák:**
```
"type == 'health'"  ← nem természetes nyelv
"true"              ← nem informatív
"goto: health"      ← nem természetes nyelv
```

### 6. Edge_order beállítása

Az `edge_order` tömb határozza meg a kiértékelés sorrendjét:
- Az LLM ebben a sorrendben értékeli ki a feltételeket
- Fontosabb/gyakoribb útvonalak előre

```json
"edge_order": ["edge_to_health", "edge_to_vehicle", "edge_to_luggage"]
```

### 7. Validálás

Ellenőrizd:
- [ ] Van `start_node` (type: "start")
- [ ] Minden node elérhető a start_node-ból
- [ ] Minden edge source/target létező node-ra mutat
- [ ] LLM condition-öknél van condition szöveg
- [ ] edge_order konzisztens az edge-ekkel
- [ ] Nincs árva node (nem elérhető és nincs kimenete)

### 8. Fájl mentése

```
projects/<projekt>/config/workflow.json
```

---

## ElevenLabs Struktúra Referencia

### Node típusok

| Típus | Használat |
|-------|-----------|
| `start` | Belépési pont (pontosan 1 db) |
| `override_agent` | Agent node |

### Condition típusok

| Típus | Használat |
|-------|-----------|
| `unconditional` | Mindig teljesül |
| `llm` | LLM értékeli ki a condition szöveget |

### Node struktúra

```json
{
  "type": "override_agent",
  "label": "Megjelenített név",
  "position": { "x": 400.0, "y": 200.0 },
  "edge_order": ["edge_1", "edge_2"],
  "conversation_config": {
    "tts": { "voice_id": "..." },
    "agent": {
      "first_message": "Üdvözlő üzenet (opcionális)",
      "prompt": {
        "prompt": "Agent prompt szöveg",
        "llm": "gpt-4o-mini",
        "temperature": 0.0
      }
    }
  },
  "additional_prompt": "",
  "additional_knowledge_base": [],
  "additional_tool_ids": []
}
```

### Edge struktúra

```json
{
  "source": "node_orchestrator",
  "target": "node_specialist",
  "forward_condition": {
    "type": "llm",
    "label": null,
    "condition": "Természetes nyelvű feltétel szöveg."
  },
  "backward_condition": null
}
```

---

## Példák

### Linear Workflow (3 agent)

```
Receptionist → Specialist → Finalizer
```

**Nodes:** start_node, node_receptionist, node_specialist, node_finalizer
**Edges:** start→receptionist (unconditional), receptionist→specialist (llm), specialist→finalizer (llm)

### Branching Workflow (5 agent)

```
           ┌→ Health Specialist ─┐
Orchestrator → Vehicle Specialist → Finalizer
           └→ Luggage Specialist ─┘
```

**Nodes:** start_node, node_orchestrator, node_health, node_vehicle, node_luggage, node_finalizer
**Edges:**
- start→orchestrator (unconditional)
- orchestrator→health/vehicle/luggage (llm - 3 db)
- health/vehicle/luggage→finalizer (llm - 3 db)

### Hub-and-Spoke Workflow

```
      ↔ Billing Specialist
Hub Agent
      ↔ Technical Specialist
```

**Nodes:** start_node, node_hub, node_billing, node_technical
**Edges:**
- start→hub (unconditional)
- hub→billing, hub→technical (llm)
- billing→hub, technical→hub (llm - vissza)

---

## Specialist Node Hozzáadása (Dinamikus)

Ha több specialist kell, mint a template-ben:

1. **Másolod a specialist node-ot**
2. **Új node ID-t adsz** (pl. `node_specialist_3`)
3. **Pozíciót állítasz** (x koordináta eltolva)
4. **Új edge-eket adsz hozzá**
5. **Frissíted az orchestrator edge_order-jét**

```json
"edge_order": [
  "edge_orchestrator_to_specialist_1",
  "edge_orchestrator_to_specialist_2",
  "edge_orchestrator_to_specialist_3"
]
```

---

## Hibakeresés

### "Node nem elérhető" hiba
- Ellenőrizd, hogy van edge ami a node-ra mutat

### "Végtelen ciklus" lehetőség
- Hub-and-spoke esetén OK (szándékos)
- Branching esetén NEM OK

### "Condition nem működik"
- A condition szöveg legyen egyértelmű
- Kerüld a túl általános feltételeket
- Tesztelj a ElevenLabs konzolban

---

## Transfer Tool (Egyszerű Eset)

Ha csak 2 agent van és egyszerű transfer kell:

```json
{
  "type": "system",
  "name": "transfer_to_agent",
  "params": {
    "system_tool_type": "transfer_to_agent",
    "transfers": [
      {
        "agent_id": "TARGET_AGENT_ID",
        "condition": "Ha az ügyfél X témáról beszél",
        "delay_ms": 500,
        "transfer_message": "Máris kapcsolom a kollégát",
        "enable_transferred_agent_first_message": true
      }
    ]
  }
}
```

Ez az agent `tools` listájába kerül, nem külön workflow fájlba.
