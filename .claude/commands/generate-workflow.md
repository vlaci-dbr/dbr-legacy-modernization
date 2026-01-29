# /generate-workflow - Workflow Generálása

## Leírás

ElevenLabs native workflow JSON-t generálok a meglévő agent-ek alapján.

## Folyamat

1. Olvasd be: `.claude/guides/workflow-generation-guide.md`
2. Határozd meg a workflow típusát
3. Olvasd be a megfelelő template-et
4. Az agent-ek alapján generáld a node-okat és edge-eket
5. Validáld a workflow.schema.json alapján
6. Mentsd el

## Workflow Típusok

| Típus | Mikor |
|-------|-------|
| linear | 2-3 agent, egyszerű lánc |
| branching | Orchestrator → N specialist → Finalizer |
| hub-and-spoke | Visszatérés az orchestrator-hoz |
| transfer-tool | 2 agent, egyszerű transfer |

## Input

- Projekt agent-ek listája (config/project.json vagy agents/ mappa)
- Workflow típus

## Lépések

### 1. Projekt kiválasztás
```
Melyik projekt workflow-ját generáljam?
(vagy adj meg egy új projekt útvonalat)
```

### 2. Agent-ek felismerése
```
Talált agent-ek:
- receptionist (orchestrator)
- health-specialist (specialist)
- vehicle-specialist (specialist)
- finalizer (finalizer)
```

### 3. Workflow típus meghatározása
```
Ajánlott workflow típus: branching
(orchestrator → specialists → finalizer)

Elfogadod, vagy másikat választasz?
```

### 4. Routing szabályok bekérése
```
Mikor irányítson a receptionist a health-specialist-hoz?
> Ha az ügyfél egészségügyi kárról beszél

Mikor irányítson a receptionist a vehicle-specialist-hoz?
> Ha az ügyfél gépjármű kárról beszél
```

### 5. Template beolvasása
```
framework/templates/workflows/<tipus>.json
```

### 6. Workflow generálása

Node-ok létrehozása minden agent-hez:
- start_node (type: start)
- node_<agent-id> (type: override_agent)

Edge-ek létrehozása:
- edge_start_to_<orchestrator>
- edge_<orchestrator>_to_<specialist> (minden specialist-hoz)
- edge_<specialist>_to_<finalizer> (minden specialist-hoz)

### 7. Validálás
```
✓ Node-ok: 5 db
✓ Edge-ek: 7 db
✓ Minden node elérhető
✓ Minden edge valid
```

### 8. Mentés
```
config/workflow.json
```

## Output

`config/workflow.json` - ElevenLabs native formátumban

## Példa Output

```json
{
  "workflow": {
    "nodes": {
      "start_node": {
        "type": "start",
        "edge_order": ["edge_start_to_receptionist"]
      },
      "node_receptionist": {
        "type": "override_agent",
        "label": "Zsófi",
        "edge_order": ["edge_to_health", "edge_to_vehicle"],
        "conversation_config": { ... }
      },
      ...
    },
    "edges": {
      "edge_start_to_receptionist": {
        "source": "start_node",
        "target": "node_receptionist",
        "forward_condition": { "type": "unconditional" }
      },
      "edge_to_health": {
        "source": "node_receptionist",
        "target": "node_health_specialist",
        "forward_condition": {
          "type": "llm",
          "condition": "Ha az ügyfél egészségügyi kárról beszél."
        }
      },
      ...
    }
  }
}
```

## Fontos Szabályok

- Node típusok: CSAK "start" és "override_agent"
- Condition típusok: CSAK "unconditional" és "llm"
- A condition szöveg természetes nyelvű legyen
- Az edge_order sorrendje fontos (LLM kiértékelés sorrendje)
