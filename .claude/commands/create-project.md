# /create-project - Új Voice Agent Projekt Létrehozása

## Leírás

Interaktívan létrehozok egy új ElevenLabs voice agent projektet sablon alapján.

## Folyamat

1. Olvasd be: `.claude/guides/project-setup-guide.md`
2. Kérdezd meg a felhasználótól a projekt típusát
3. A sablon manifest alapján gyűjtsd össze a szükséges adatokat
4. Generáld a projekt fájlokat a megfelelő template-ek és guide-ok alapján
5. Validáld a generált JSON-öket
6. Mutasd meg az összefoglalót

## Elérhető Sablonok

| Sablon | Leírás |
|--------|--------|
| insurance-call-center | Biztosítási kárigény bejelentő |
| customer-service | Ügyfélszolgálat termékszakértővel |
| appointment-booking | Egyszerű időpontfoglaló |
| info-hotline | FAQ-alapú információs vonal |

## Szükséges Adatok

Az alábbi adatokat gyűjtsd össze interaktívan:
- Projekt neve (technikai azonosító, kebab-case)
- Cég adatok (név, telefon, email)
- Agent nevek és beállítások
- Szakterületek / témakörök listája (sablon-függő)

## Lépések

### 1. Sablon kiválasztás
```
Melyik sablont szeretné használni?
1. insurance-call-center - Biztosítási kárigény bejelentő
2. customer-service - Ügyfélszolgálat
3. appointment-booking - Időpontfoglaló
4. info-hotline - Információs vonal
```

### 2. Alapadatok bekérése
```
Kérem a következő adatokat:
- Cég neve:
- Telefon:
- Email:
- Nyitvatartás:
```

### 3. Projekt ID generálás
A cég nevéből kebab-case formátumban: `abc-biztosito`

### 4. Agent nevek bekérése
A sablon alapján kérdezd meg az agent neveket vagy használd a javaslatokat.

### 5. Szakterületek/témák bekérése (ha releváns)
Insurance és customer-service esetén kérdezd meg a szakterületeket.

### 6. Fájlok generálása

Generálandó fájlok:
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

### 7. Összefoglaló megjelenítése
```
✓ Projekt létrehozva: <projekt-id>
  - Agent-ek: X db
  - KB-k: X db
  - Workflow: <típus>

Következő lépések:
  - /validate - Projekt ellenőrzése
  - Szerkeszd a promptokat: projects/<projekt-id>/agents/*.md
  - /deploy - Feltöltés ElevenLabs-ra
```

## Output Struktúra

```
projects/<projekt-nev>/
├── config/
│   ├── project.json
│   └── workflow.json
├── agents/
│   └── *.md
└── knowledge-bases/
    └── *.md
```

## Következő Lépés

Projekt létrehozása után:
- `/validate` - Projekt ellenőrzése
- `/deploy` - Feltöltés ElevenLabs-ra
- Vagy: manuális testreszabás a promptokban
