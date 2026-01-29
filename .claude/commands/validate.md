# /validate - Projekt Validálása

## Leírás

Ellenőrzöm a projekt konfigurációját és struktúráját.

## Folyamat

1. Projekt mappa meghatározása
2. Struktúra ellenőrzés
3. JSON schema validálás
4. Referencia integritás ellenőrzés
5. Prompt minőség ellenőrzés
6. Eredmény összefoglalás

## Ellenőrzések

### Struktúra
- [ ] config/project.json létezik
- [ ] config/workflow.json létezik (ha multi-agent)
- [ ] agents/ mappa és prompt fájlok
- [ ] knowledge-bases/ mappa (opcionális)

### Schema Validálás
- [ ] project.json → project.schema.json
- [ ] workflow.json → workflow.schema.json
- [ ] Agent konfigok (ha JSON-ban)

### Referencia Integritás
- [ ] Workflow node-ok létező agent-ekre mutatnak
- [ ] KB hozzárendelések valid agent ID-k
- [ ] Transfer célpontok léteznek

### Prompt Minőség
- [ ] 6-pillar struktúra megvan (PERSONALITY, ENVIRONMENT, TONE, GOAL, GUARDRAILS, TOOLS)
- [ ] GUARDRAILS nem üres
- [ ] Transfer szabályok definiáltak (orchestrator esetén)

## Lépések

### 1. Projekt kiválasztás
```
Melyik projektet validáljam?
1. projects/eub-callcenter
2. projects/techcorp-support
3. [Más útvonal megadása]
```

### 2. Struktúra ellenőrzés
```
Struktúra ellenőrzése: projects/eub-callcenter

✓ config/project.json
✓ config/workflow.json
✓ agents/receptionist.md
✓ agents/health-specialist.md
✓ agents/vehicle-specialist.md
✓ agents/finalizer.md
✓ knowledge-bases/company-info.md
✓ knowledge-bases/general-faq.md
```

### 3. Schema validálás
```
Schema validálás:

✓ project.json - Valid
✓ workflow.json - Valid
```

### 4. Referencia ellenőrzés
```
Referencia integritás:

✓ Workflow node 'node_receptionist' → agents/receptionist.md
✓ Workflow node 'node_health_specialist' → agents/health-specialist.md
✓ KB 'kb-company-info' → knowledge-bases/company-info.md
⚠ KB 'kb-claim-procedures' - Fájl nem található
```

### 5. Prompt ellenőrzés
```
Prompt minőség ellenőrzése:

receptionist.md:
✓ PERSONALITY szekció
✓ ENVIRONMENT szekció
✓ TONE szekció
✓ GOAL szekció
✓ GUARDRAILS szekció
✓ TOOLS szekció

health-specialist.md:
✓ PERSONALITY szekció
⚠ GUARDRAILS szekció - Csak 2 szabály (ajánlott: 5+)
✓ GOAL szekció - Gyűjtendő adatok definiálva
```

### 6. Összefoglaló
```
═══════════════════════════════════════
Projekt validálás: eub-callcenter
═══════════════════════════════════════

✓ Struktúra: OK (8/8 fájl)
✓ Schema: OK
⚠ Referencia: 1 figyelmeztetés
  - kb-claim-procedures nem található
✓ Prompt minőség: OK (1 ajánlás)

═══════════════════════════════════════
Összesítés: 3 OK, 1 figyelmeztetés, 0 hiba
Státusz: DEPLOYOLHATÓ (figyelmeztetésekkel)
═══════════════════════════════════════
```

## Output Formátum

```
Projekt validálás: <projekt-nev>

✓ Struktúra: OK
✓ Schema: OK
⚠ Referencia: 1 figyelmeztetés
  - agents/specialist.md: KB referencia 'kb-missing' nem található
✓ Prompt minőség: OK

Összesítés: 3 OK, 1 figyelmeztetés, 0 hiba
```

## Státusz Szintek

| Státusz | Jelentés |
|---------|----------|
| ✓ OK | Minden rendben |
| ⚠ Figyelmeztetés | Nem blokkoló, de javítandó |
| ✗ Hiba | Blokkoló, javítás szükséges |

## Végső Státuszok

| Összesítés | Döntés |
|------------|--------|
| Csak OK | DEPLOYOLHATÓ |
| OK + Figyelmeztetés | DEPLOYOLHATÓ (figyelmeztetésekkel) |
| Bármilyen Hiba | NEM DEPLOYOLHATÓ |

## Javítási Javaslatok

Ha hibát talál, adj konkrét javítási javaslatot:

```
✗ Hiba: workflow.json - 'node_support' nem létező agent-re mutat

Javítás:
1. Hozd létre az agent-et: /generate-agent
2. Vagy távolítsd el a node-ot a workflow-ból
```
