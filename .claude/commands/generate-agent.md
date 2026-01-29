# /generate-agent - Agent Prompt Generálása

## Leírás

Egyedi agent promptot generálok a megfelelő template alapján.

## Folyamat

1. Olvasd be: `.claude/guides/agent-generation-guide.md`
2. Kérdezd meg az agent típusát (orchestrator/specialist/finalizer)
3. Olvasd be a megfelelő template-et: `framework/templates/agents/<tipus>.md`
4. Gyűjtsd össze a szükséges változókat
5. Generáld a promptot
6. Mentsd el a megadott helyre

## Agent Típusok

| Típus | Template | Leírás |
|-------|----------|--------|
| orchestrator | orchestrator.md | Belépési pont, routing |
| specialist | specialist.md | Szakterületi adatgyűjtés |
| finalizer | finalizer.md | Összegzés, lezárás |

## Szükséges Adatok

### Minden Agent-hez
- Agent technikai név (kebab-case, pl. `health-specialist`)
- Megjelenített név (pl. Zsófi, Kata, Péter)
- Cég neve
- Nyelv és stílus (tegezés/magázás)

### Orchestrator-hoz Még
- Üdvözlő üzenet (first_message)
- Transfer célpontok listája (specialist nevek)
- Transfer szabályok (ki, mikor, miért)

### Specialist-hoz Még
- Szakterület leírás
- Gyűjtendő adatok listája
- Validációs szabályok (formátumok, kötelező mezők)
- Transfer forrás (orchestrator neve)

### Finalizer-hez Még
- Lezáró tool-ok (email küldés, ügyszám generálás)
- Összegzendő adatok
- Sikeres/sikertelen üzenetek

## Lépések

### 1. Agent típus kiválasztás
```
Milyen típusú agent-et szeretne létrehozni?
1. orchestrator - Belépési pont, fogadás és irányítás
2. specialist - Szakterületi adatgyűjtés
3. finalizer - Összegzés és lezárás
```

### 2. Alapadatok bekérése
```
- Agent technikai neve (pl. receptionist):
- Megjelenített név (pl. Zsófi):
- Cég neve:
- Magázás vagy tegezés?
```

### 3. Típus-specifikus adatok
*Az agent típusától függően*

### 4. Template beolvasása
```
framework/templates/agents/<tipus>.md
```

### 5. Prompt generálása
A 6-pillar struktúra szerint:
- PERSONALITY
- ENVIRONMENT
- TONE
- GOAL
- GUARDRAILS
- TOOLS

### 6. Snippet-ek beillesztése (ha szükséges)
- `snippets/common-guardrails.md`
- `snippets/hungarian-names.md`
- `snippets/data-collection.md`

### 7. Fájl mentése
```
projects/<projekt>/agents/<agent-id>.md
```

## Output

Generált prompt fájl: `agents/<agent-id>.md`

## Példa

```
/generate-agent

> Milyen típusú agent?
specialist

> Agent technikai neve:
health-specialist

> Megjelenített név:
Kata

> Szakterület:
Egészségügyi és baleseti károk

> Gyűjtendő adatok:
- Kötvényszám
- Biztosított neve
- Esemény dátuma és helyszíne
- Ellátás típusa
- Költség összege

✓ Agent prompt létrehozva: agents/health-specialist.md
```
