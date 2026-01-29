# /deploy - Projekt Feltöltése ElevenLabs-ra

## Leírás

A projektet feltöltöm az ElevenLabs platformra a Python utility segítségével.

## Előfeltételek

1. **ELEVENLABS_API_KEY** környezeti változó beállítva
2. Projekt validálva (`/validate` sikeres)
3. Python utility elérhető (`utility/` mappa)

## Folyamat

1. Pre-flight ellenőrzés
2. Dry-run opció felajánlása
3. Knowledge base-ek feltöltése
4. Agent-ek létrehozása
5. Workflow beállítása
6. Agent ID-k mentése

## Lépések

### 1. Projekt kiválasztás
```
Melyik projektet töltse fel?
1. projects/eub-callcenter
2. projects/techcorp-support
3. [Más útvonal megadása]
```

### 2. Pre-flight ellenőrzés
```
Pre-flight ellenőrzés...

✓ ELEVENLABS_API_KEY beállítva
✓ Python utility elérhető
✓ Projekt struktúra OK
✓ /validate sikeres (0 hiba)

Folytathatjuk a deploy-t.
```

### 3. Dry-run opció
```
Szeretne először dry-run-t futtatni?
1. Igen, dry-run (teszt mód, nem tölt fel semmit)
2. Nem, éles deploy
```

### 4. Dry-run futtatás (ha választotta)
```bash
cd utility && python main.py --project ../projects/<projekt> --dry-run
```

Dry-run output:
```
[DRY-RUN] Következő műveletek lennének végrehajtva:
- KB létrehozás: kb-company-info (company-info.md)
- KB létrehozás: kb-general-faq (general-faq.md)
- Agent létrehozás: receptionist
- Agent létrehozás: health-specialist
- Agent létrehozás: vehicle-specialist
- Agent létrehozás: finalizer
- Workflow beállítás: branching (4 node, 6 edge)

Minden rendben? Folytassuk éles deploy-jal?
```

### 5. Éles deploy
```bash
cd utility && python main.py --project ../projects/<projekt>
```

### 6. Deploy output
```
═══════════════════════════════════════
Deploy: eub-callcenter
═══════════════════════════════════════

[1/6] Knowledge Base-ek feltöltése...
  ✓ kb-company-info → kb_abc123def456
  ✓ kb-general-faq → kb_789ghi012jkl

[2/6] Agent-ek létrehozása...
  ✓ receptionist → agent_111222333
  ✓ health-specialist → agent_444555666
  ✓ vehicle-specialist → agent_777888999
  ✓ finalizer → agent_000111222

[3/6] KB hozzárendelések...
  ✓ kb-company-info → receptionist
  ✓ kb-general-faq → receptionist, health-specialist

[4/6] Workflow beállítása...
  ✓ 4 node konfigurálva
  ✓ 6 edge konfigurálva

[5/6] Deployment info mentése...
  ✓ deployment/agent-ids.json
  ✓ deployment/kb-ids.json
  ✓ deployment/deploy.log

[6/6] Végső ellenőrzés...
  ✓ Minden agent elérhető
  ✓ Workflow aktív

═══════════════════════════════════════
Deploy SIKERES!
═══════════════════════════════════════

Agent ID-k:
- receptionist: agent_111222333
- health-specialist: agent_444555666
- vehicle-specialist: agent_777888999
- finalizer: agent_000111222

Fő agent (hívható): agent_111222333

Tesztelés: https://elevenlabs.io/app/conversational-ai/agent_111222333
```

## Használat (CLI)

### Dry-run (teszt)
```bash
cd utility && python main.py --project ../projects/<projekt> --dry-run
```

### Éles deploy
```bash
cd utility && python main.py --project ../projects/<projekt>
```

### Verbose mód
```bash
cd utility && python main.py --project ../projects/<projekt> --verbose
```

## Output

Deploy után létrejön:
```
projects/<projekt>/deployment/
├── agent-ids.json      # ElevenLabs agent ID-k
├── kb-ids.json         # Knowledge base ID-k
└── deploy.log          # Deploy napló
```

### agent-ids.json példa
```json
{
  "receptionist": "agent_111222333",
  "health-specialist": "agent_444555666",
  "vehicle-specialist": "agent_777888999",
  "finalizer": "agent_000111222",
  "main_agent": "agent_111222333",
  "deployed_at": "2024-01-15T10:30:00Z"
}
```

### kb-ids.json példa
```json
{
  "kb-company-info": "kb_abc123def456",
  "kb-general-faq": "kb_789ghi012jkl",
  "deployed_at": "2024-01-15T10:30:00Z"
}
```

## Hibakezelés

### API kulcs hiányzik
```
✗ Hiba: ELEVENLABS_API_KEY nincs beállítva

Megoldás:
export ELEVENLABS_API_KEY="your-api-key"
```

### Validációs hiba
```
✗ Hiba: Projekt nem validált

Megoldás:
Futtasd először: /validate
```

### API hiba
```
✗ Hiba: ElevenLabs API hiba (429 - Rate limit)

Megoldás:
Várj 1 percet és próbáld újra.
```

### Részleges deploy hiba
```
⚠ Figyelmeztetés: Részleges deploy történt

Sikerült:
- kb-company-info
- receptionist

Sikertelen:
- health-specialist (API timeout)

Megoldás:
Futtasd újra: /deploy --resume
```

## Figyelmeztetések

- Deploy előtt MINDIG futtass `/validate`-et
- Dry-run ajánlott első alkalommal
- Meglévő agent-ek felülírása: a utility kezeli (update vs create)
- API rate limit: max 10 request/sec
- Nagy KB-k: max 5MB méret

## Következő lépések

Deploy után:
1. Teszteld a webes felületen
2. Próbáld ki telefonon
3. Finomhangold a promptokat ha szükséges
4. Újra deploy: `/deploy`
