# /preview - Lokális Előnézet

## Leírás

Lokális előnézet indítása a projekt webes felületéhez. Egy egyszerű HTTP szervert indít, ahol tesztelheted a widget megjelenését és az agent működését.

## Előfeltételek

1. Projekt létezik a `projects/` mappában
2. `web/index.html` generálva
3. Python 3.x telepítve
4. (Opcionális) ElevenLabs agent ID már deployolva

## Folyamat

1. Projekt kiválasztás
2. Widget konfiguráció ellenőrzése
3. HTTP szerver indítása
4. Böngésző megnyitása

## Lépések

### 1. Projekt Kiválasztás
```
Melyik projekt előnézetét szeretné?

1. projects/tech-konferencia-2026
2. projects/eub-callcenter
3. [Más projekt]

Választás:
```

### 2. Konfiguráció Ellenőrzése
```
Projekt: tech-konferencia-2026

Widget konfiguráció ellenőrzése...
✓ web/index.html létezik
✓ config/widget.json létezik
⚠ deployment/agent-ids.json - Agent ID nincs beállítva

Figyelmeztetés: Az agent még nincs deployolva.
A widget mock módban fog működni.

Folytatja? (i/n):
```

### 3. HTTP Szerver Indítása
```bash
cd projects/<projekt>/web && python -m http.server 8080
```

### 4. Előnézet Megnyitás
```
═══════════════════════════════════════
Preview indítva: tech-konferencia-2026
═══════════════════════════════════════

URL: http://localhost:8080

Nyisd meg a böngészőben:
  http://localhost:8080

A szerver fut. Leállításhoz: Ctrl+C
═══════════════════════════════════════
```

## Használat

### Alapértelmezett port (8080)
```
/preview
```

### Egyéni port
```
/preview --port 3000
```

### Konkrét projekt
```
/preview tech-konferencia-2026
```

## Widget Tesztelés

### Mock Mód (agent nélkül)

Ha az agent még nincs deployolva, a widget mock módban működik:
- Gomb megjelenik
- Kattintásra animáció
- Valós beszélgetés nem indul

### Éles Mód (deployolt agent)

Ha az agent deployolva van:
- Teljes funkcionalitás
- Valós beszélgetés ElevenLabs-szal
- Szükséges: érvényes ELEVENLABS_API_KEY

## Hibakezelés

### Port foglalt
```
✗ Hiba: Port 8080 foglalt

Megoldás:
/preview --port 8081
```

### index.html hiányzik
```
✗ Hiba: web/index.html nem található

Megoldás:
Futtasd: /init-project vagy hozd létre manuálisan
```

### Agent ID hiányzik
```
⚠ Figyelmeztetés: Agent ID nincs beállítva

A widget mock módban fog működni.
Deployoláshoz: /deploy
```

## Megjegyzések

- A preview szerver csak fejlesztési célra
- Éles használathoz proper hosting szükséges
- HTTPS nélkül a mikrofon nem működik éles módban
- Ctrl+C a szerver leállításához
