# /sync-elevenlabs - ElevenLabs Szinkronizálás

## Leírás

Szinkronizálja a lokális projekt fájlokat az ElevenLabs platformmal. Frissíti a meglévő agent-eket és tudásbázisokat.

## Műveletek

| Művelet | Leírás |
|---------|--------|
| `push` | Lokális változtatások feltöltése ElevenLabs-ra |
| `pull` | ElevenLabs konfiguráció letöltése lokálisan |
| `status` | Szinkronizációs állapot ellenőrzése |
| `diff` | Különbségek megjelenítése |

## Előfeltételek

1. **ELEVENLABS_API_KEY** környezeti változó beállítva
2. Projekt már egyszer deployolva (agent-ids.json létezik)

## Lépések

### Status Ellenőrzés

```
/sync-elevenlabs status
```

Output:
```
═══════════════════════════════════════
Szinkronizáció: tech-konferencia-2026
═══════════════════════════════════════

Agent-ek:
  event-info-agent
    Lokális:     2026-01-28 10:30 (módosítva)
    ElevenLabs:  2026-01-27 15:00
    Állapot:     ⚠ MÓDOSULT LOKÁLISAN

Knowledge Base-ek:
  kb-event-info
    Lokális:     2026-01-28 09:00
    ElevenLabs:  2026-01-28 09:00
    Állapot:     ✓ SZINKRONBAN

  kb-venue
    Lokális:     2026-01-28 11:00 (módosítva)
    ElevenLabs:  2026-01-27 15:00
    Állapot:     ⚠ MÓDOSULT LOKÁLISAN

Widget:
  Állapot:     ✓ SZINKRONBAN

Összesítés: 2 módosult, 2 szinkronban
═══════════════════════════════════════
```

### Különbségek Megjelenítése

```
/sync-elevenlabs diff
```

Output:
```
═══════════════════════════════════════
Különbségek: tech-konferencia-2026
═══════════════════════════════════════

agents/event-info-agent.md:
  + Hozzáadva: új GUARDRAILS szabály (15. sor)
  ~ Módosítva: GOAL szekció (42-48. sor)

knowledge-bases/kb-venue.md:
  + Hozzáadva: "Parkolás" szekció
  ~ Módosítva: "Megközelítés" szekció

═══════════════════════════════════════
```

### Push (Feltöltés)

```
/sync-elevenlabs push
```

Folyamat:
```
Változtatások feltöltése ElevenLabs-ra...

[1/3] Agent frissítés: event-info-agent
  ✓ Prompt frissítve
  ✓ Konfiguráció frissítve

[2/3] KB frissítés: kb-venue
  ✓ Tartalom frissítve

[3/3] Ellenőrzés...
  ✓ Minden szinkronban

═══════════════════════════════════════
Push SIKERES!
Frissítve: 1 agent, 1 KB
═══════════════════════════════════════
```

### Pull (Letöltés)

```
/sync-elevenlabs pull
```

Folyamat:
```
ElevenLabs konfiguráció letöltése...

⚠ Figyelmeztetés: A lokális fájlok felülíródnak!

Érintett fájlok:
  - agents/event-info-agent.md
  - knowledge-bases/kb-event-info.md

Folytatja? (i/n): i

[1/2] Agent letöltés: event-info-agent
  ✓ Prompt mentve

[2/2] KB letöltés: kb-event-info
  ✓ Tartalom mentve

═══════════════════════════════════════
Pull SIKERES!
Letöltve: 1 agent, 1 KB
═══════════════════════════════════════
```

## Használat

### Állapot ellenőrzés
```
/sync-elevenlabs status
```

### Különbségek
```
/sync-elevenlabs diff
```

### Feltöltés
```
/sync-elevenlabs push
```

### Letöltés
```
/sync-elevenlabs pull
```

### Csak agent-ek
```
/sync-elevenlabs push --agents-only
```

### Csak KB-k
```
/sync-elevenlabs push --kb-only
```

### Dry-run
```
/sync-elevenlabs push --dry-run
```

## Hibakezelés

### API kulcs hiányzik
```
✗ Hiba: ELEVENLABS_API_KEY nincs beállítva

Megoldás:
export ELEVENLABS_API_KEY="your-api-key"
```

### Projekt nincs deployolva
```
✗ Hiba: Projekt még nem volt deployolva

Megoldás:
Futtasd először: /deploy
```

### Konfliktus
```
⚠ Konfliktus: event-info-agent

Mindkét helyen módosult a fájl:
- Lokális: 2026-01-28 10:30
- ElevenLabs: 2026-01-28 09:00

Mit tegyek?
1. Lokális felülírja (push --force)
2. ElevenLabs felülírja (pull --force)
3. Manuális összefésülés
```

## Figyelmeztetések

- A `pull` felülírja a lokális fájlokat
- A `push` felülírja az ElevenLabs-on lévő konfigurációt
- Konfliktus esetén manuális beavatkozás szükséges
- Ajánlott git commit push/pull előtt
