# Projekt Létrehozási Útmutató

## Áttekintés

Ez az útmutató elmagyarázza, hogyan hozz létre új ElevenLabs voice agent projektet sablon alapján.

---

## Elérhető Sablonok

| Sablon | Leírás | Agent-ek | Workflow |
|--------|--------|----------|----------|
| **insurance-call-center** | Biztosítási kárigény bejelentő | 5 | branching |
| **customer-service** | Általános ügyfélszolgálat | 4 | branching |
| **appointment-booking** | Időpontfoglaló | 2 | linear |
| **info-hotline** | Információs vonal | 3 | hub-and-spoke |

---

## Projekt Létrehozási Folyamat

### 1. Sablon kiválasztása

Kérdezd meg a felhasználótól:
- Milyen típusú projektet szeretne?
- Hány agent-re van szükség?
- Kell-e visszatérni az orchestrator-hoz?

**Döntési segítség:**

| Ha a cél... | Sablon |
|-------------|--------|
| Kárigény/bejelentés több szakterülettel | insurance-call-center |
| Termékek + támogatás | customer-service |
| Egyszerű időpontfoglalás | appointment-booking |
| FAQ, több téma, visszatérő | info-hotline |

### 2. Sablon beolvasása

Olvasd be a választott sablont:
```
framework/templates/projects/<sablon>.json
```

### 3. Alapadatok gyűjtése

A sablon `required_inputs` alapján kérdezd meg:
- Cég neve
- Telefonszám, email
- Nyitvatartás
- Szakterületek/szolgáltatások

### 4. Agent-ek testreszabása

Minden agent-hez:
1. **Név kiválasztása** (a sablon javasol)
2. **Voice style kiválasztása** (voices.json-ból)
3. **Üdvözlő üzenet** (orchestrator esetén)
4. **Szakterület adatok** (specialist esetén)

### 5. Projekt fájlok generálása

A sablon `output_structure` alapján:

```
projects/<projekt-id>/
├── config/
│   ├── project.json
│   └── workflow.json
├── agents/
│   └── *.md
└── knowledge-bases/
    └── *.md
```

### 6. Validálás

- Minden generált fájl helyén van?
- A project.json valid?
- A workflow.json valid?
- Az agent promptok teljesek?

---

## Sablon Részletek

### insurance-call-center

**Használat:** Biztosítási kárigény bejelentő, több szakterülettel

**Agent-ek:**
- Receptionist (orchestrator) - fogadás, irányítás
- Health Specialist - egészségügyi károk
- Vehicle Specialist - gépjármű károk
- Luggage Specialist - poggyász, útlemondás
- Finalizer - összegzés, lezárás

**Workflow:** Branching (Receptionist → [Specialists] → Finalizer)

**KB-k:**
- Company info (minden agent)
- General FAQ (receptionist)
- Claim procedures (specialists, finalizer)
- Insurance terms (specialists)

---

### customer-service

**Használat:** Általános ügyfélszolgálat termék és támogatás kérdésekre

**Agent-ek:**
- Receptionist (orchestrator) - fogadás
- Sales Specialist - termékek, vásárlás
- Support Specialist - hibaelhárítás
- Finalizer - lezárás

**Workflow:** Branching (Receptionist → [Sales|Support] → Finalizer)

**KB-k:**
- Company info
- Product catalog
- Support FAQ
- Troubleshooting procedures

---

### appointment-booking

**Használat:** Egyszerű időpontfoglaló (orvos, fodrász, stb.)

**Agent-ek:**
- Booking Agent (orchestrator) - adatgyűjtés
- Finalizer - megerősítés

**Workflow:** Linear (Booking Agent → Finalizer)

**Gyűjtendő adatok:**
- Ügyfél neve
- Telefonszám
- Szolgáltatás típusa
- Kívánt dátum és idő

**KB-k:**
- Company info
- Services catalog
- Booking FAQ

---

### info-hotline

**Használat:** Információs vonal, több téma, visszatérő workflow

**Agent-ek:**
- Info Hub (orchestrator) - központi pont
- Topic Expert 1 - első téma
- Topic Expert 2 - második téma
- (Nincs finalizer - visszatér a hub-hoz)

**Workflow:** Hub-and-spoke (Hub ↔ Experts)

**Speciális:** Az ügyfél több témában is kérdezhet egy hívás alatt.

**KB-k:**
- Company info
- General FAQ
- Topic-specific knowledge bases

---

## Project.json Generálás

```json
{
  "id": "<projekt-id>",
  "name": "<Projekt Megjelenített Név>",
  "description": "<Rövid leírás>",
  "language": "hu",
  "version": "1.0.0",
  "company": {
    "name": "<Cég neve>",
    "phone": "<Telefonszám>",
    "email": "<Email>",
    "opening_hours": "<Nyitvatartás>"
  },
  "agents": [
    {
      "id": "<agent-id>",
      "name": "<Agent név>",
      "role": "<orchestrator|specialist|finalizer>",
      "prompt_file": "agents/<agent-id>.md",
      "voice": {
        "voice_id": "<ElevenLabs voice ID>"
      }
    }
  ],
  "knowledge_bases": [
    {
      "id": "<kb-id>",
      "name": "<KB név>",
      "type": "<faq|product-catalog|...>",
      "source_file": "knowledge-bases/<kb-id>.md",
      "assigned_agents": ["<agent-id>", "..."]
    }
  ],
  "workflow": {
    "type": "<linear|branching|hub-and-spoke>",
    "config_file": "config/workflow.json"
  }
}
```

---

## Workflow.json Generálás

A workflow generáláshoz olvasd be:
- `.claude/guides/workflow-generation-guide.md`
- A megfelelő workflow template-et

---

## Agent Promptok Generálása

Minden agent-hez:
1. Határozd meg a típust (orchestrator/specialist/finalizer)
2. Olvasd be a megfelelő template-et
3. Töltsd ki a változókat a projekt adataival
4. Mentsd el: `projects/<projekt>/agents/<agent-id>.md`

---

## KB-k Generálása

Minden KB-hoz:
1. Határozd meg a típust (faq/product-catalog/...)
2. Olvasd be a megfelelő template-et
3. Gyűjtsd össze a tartalmat a felhasználótól
4. Mentsd el: `projects/<projekt>/knowledge-bases/<kb-id>.md`

---

## Minőségi Ellenőrzés

### Projekt létrehozás után ellenőrizd:

**Struktúra:**
- [ ] config/project.json létezik és valid
- [ ] config/workflow.json létezik és valid
- [ ] Minden agent-hez van .md fájl
- [ ] Minden KB-hoz van .md fájl

**Tartalom:**
- [ ] Project.json tartalmaz minden agent-et
- [ ] Workflow node-ok egyeznek az agent-ekkel
- [ ] KB hozzárendelések helyesek
- [ ] Agent promptok teljesek (6-pillar)

**Konzisztencia:**
- [ ] Agent ID-k egyeznek mindenhol
- [ ] KB ID-k egyeznek mindenhol
- [ ] Voice ID-k érvényesek

---

## Példa: Teljes Projekt Létrehozás

### Input
```
Sablon: insurance-call-center
Cég: ABC Biztosító
Telefon: +36 1 999 8888
Email: info@abc.hu
Nyitvatartás: H-P 8:00-18:00
Szakterületek: Egészség, Autó, Utazás
```

### Generált struktúra
```
projects/abc-biztosito/
├── config/
│   ├── project.json
│   └── workflow.json
├── agents/
│   ├── receptionist.md
│   ├── health-specialist.md
│   ├── auto-specialist.md
│   ├── travel-specialist.md
│   └── finalizer.md
└── knowledge-bases/
    ├── company-info.md
    ├── general-faq.md
    ├── claim-procedures.md
    └── insurance-terms.md
```

---

## Következő lépések

Projekt létrehozása után:
1. `/validate` - Ellenőrizd a projektet
2. Testreszabás - Szerkeszd a promptokat szükség szerint
3. `/deploy` - Töltsd fel ElevenLabs-ra
