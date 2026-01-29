# /init-project - Új Projekt Létrehozása Wizard

## Leírás

Interaktív wizard új ElevenLabs voice agent projekt létrehozásához. A wizard végigvezet a projekt konfigurálásán és létrehozza az összes szükséges fájlt.

## Elérhető Sablonok

| Sablon | Leírás | Agent szám |
|--------|--------|------------|
| customer-service | Ügyfélszolgálat specialistákkal | 3-5 |
| appointment-booking | Időpontfoglaló rendszer | 2-3 |
| info-hotline | Információs vonal (FAQ alapú) | 1-2 |
| event-guide | Rendezvény információs asszisztens | 1 |
| insurance-call-center | Biztosítási kárigény bejelentő | 3-5 |

## Folyamat

```
1. /init-project parancs indítása
       ↓
2. Sablon kiválasztás
       ↓
3. Alapadatok bekérése (wizard kérdések)
       ↓
4. Projekt ID generálás
       ↓
5. Fájlok generálása sablonok alapján
       ↓
6. Validálás és összefoglaló
```

## Lépések

### 1. Sablon Kiválasztás
```
Melyik projekt típust szeretné létrehozni?

1. customer-service - Ügyfélszolgálat specialistákkal
2. appointment-booking - Időpontfoglaló rendszer
3. info-hotline - Információs vonal (FAQ alapú)
4. event-guide - Rendezvény információs asszisztens
5. insurance-call-center - Biztosítási kárigény bejelentő

Választás (1-5):
```

### 2. Alapadatok Bekérése

A sablon wizard_questions alapján interaktívan kérdezz rá az adatokra.

Példa event-guide esetén:
```
Mi az esemény neve? [kötelező]
> Tech Konferencia 2026

Mikor lesz az esemény? [kötelező]
> 2026. március 15-16.

Milyen típusú esemény?
1. Konferencia
2. Fesztivál
3. Sportesemény
4. Kiállítás
5. Egyéb
> 1

Mi a helyszín neve? [kötelező]
> Budapest Kongresszusi Központ

Mi a helyszín címe? [kötelező]
> 1123 Budapest, Jagelló út 1-3.

Mi legyen az asszisztens neve? [opcionális, alapértelmezett: Asszisztens]
> Emma

Ki a szervező? [opcionális]
> TechCorp Kft.

Kapcsolattartási email? [opcionális]
> info@techconf.hu

Milyen nyelven kommunikáljon?
1. hu (Magyar)
2. en (English)
> 1
```

### 3. Projekt ID Generálás

A projekt nevéből automatikusan generálj kebab-case ID-t:
- "Tech Konferencia 2026" → `tech-konferencia-2026`
- Ékezetek eltávolítása
- Speciális karakterek törlése
- Szóközök → kötőjelek

### 4. Fájlok Generálása

A sablon `files_to_generate` alapján hozd létre a fájlokat:

```
projects/tech-konferencia-2026/
├── config/
│   ├── project.json        ← Wizard adatokból
│   ├── workflow.json       ← Sablon alapján
│   ├── deployment.json     ← Alapértelmezett
│   └── widget.json         ← Alapértelmezett
├── agents/
│   └── event-info-agent.md ← Template + adatok
├── knowledge-bases/
│   ├── kb-event-info.md    ← Sablon + adatok
│   ├── kb-venue.md         ← Sablon + adatok
│   ├── kb-schedule.md      ← Üres sablon
│   └── kb-faq.md           ← Üres sablon
├── web/
│   └── index.html          ← Widget landing page
├── deployment/
│   ├── agent-ids.json      ← Üres
│   └── kb-ids.json         ← Üres
└── README.md               ← Projekt dokumentáció
```

### 5. Összefoglaló

```
═══════════════════════════════════════
✓ Projekt létrehozva: tech-konferencia-2026
═══════════════════════════════════════

Generált fájlok:
  - config/project.json
  - config/workflow.json
  - agents/event-info-agent.md
  - knowledge-bases/kb-event-info.md
  - knowledge-bases/kb-venue.md
  - knowledge-bases/kb-schedule.md
  - knowledge-bases/kb-faq.md
  - web/index.html
  - deployment/agent-ids.json
  - deployment/kb-ids.json

Következő lépések:
  1. Töltsd ki a tudásbázis fájlokat:
     - knowledge-bases/kb-schedule.md (programterv)
     - knowledge-bases/kb-faq.md (GYIK)

  2. Szerkeszd az agent promptot ha szükséges:
     - agents/event-info-agent.md

  3. Validáld a projektet:
     /validate

  4. Deploy ElevenLabs-ra:
     /deploy

═══════════════════════════════════════
```

## Használat

```
/init-project
```

Vagy közvetlenül sablon megadásával:
```
/init-project event-guide
```

## Fontos

- A wizard interaktívan kérdezi az adatokat
- Kötelező mezők kitöltése nélkül nem folytatható
- Opcionális mezők kihagyhatók (Enter)
- Generálás előtt megjeleníti az összefoglalót
- Megerősítést kér a generálás előtt

## Következő Parancsok

Projekt létrehozása után:
- `/validate` - Projekt ellenőrzése
- `/deploy` - ElevenLabs feltöltés
- `/preview` - Lokális előnézet
