# Adatgyűjtési Snippet-ek

> **UTASÍTÁS CLAUDE-NAK:** Ezeket az adatgyűjtési mintákat használd a specialist agent promptokban.

---

## Általános Adatgyűjtési Technikák

### Nyitott vs Zárt Kérdések

**Nyitott kérdések (részletek gyűjtésére):**
```
- "Mi történt pontosan?"
- "Hogyan történt az esemény?"
- "Mikor vette észre először?"
- "Milyen körülmények között?"
```

**Zárt kérdések (konkrét adatok gyűjtésére):**
```
- "A kötvényszám 10 számjegyből áll, mi az?"
- "Melyik országban történt?"
- "Ez [dátum]-án volt?"
- "Igen vagy nem?"
```

---

## Kötelező Adat Típusok Szerinti Minták

### Személyes Adatok

```markdown
**Név bekérése:**
"Kérem, mondja be a biztosított teljes nevét, ahogy a kötvényen szerepel."

**Validálás:**
- Minimum 2 szó
- Nem tartalmazhat számokat
- Ékezetek megengedettek
```

### Kötvényszám

```markdown
**Bekérés:**
"A kötvényszámra lenne szükségem. Ez egy 10 számjegyből álló szám, ami a biztosítási dokumentumon található."

**Ha nem találja:**
"A kötvényszám a szerződés jobb felső sarkában található, vagy az email visszaigazolásban is megtalálja."

**Validálás:**
- Pontosan 10 számjegy
- Csak számok (0-9)
```

### Dátum

```markdown
**Bekérés:**
"Mikor történt az esemény? Kérem, mondja év, hónap, nap formátumban."

**Pontosítás:**
"Ez [visszamondott dátum] volt, igaz?"

**Validálás:**
- Nem lehet jövőbeli dátum
- Érvényes dátum formátum
- A kötvény érvényességi idején belül
```

### Helyszín

```markdown
**Bekérés:**
"Melyik országban és városban történt az esemény?"

**Pontosítás:**
"Ez [visszamondott helyszín], jól értettem?"

**Validálás:**
- Ország kötelező
- Város ajánlott
- Külföldön történt (utasbiztosításnál)
```

### Összeg és Pénznem

```markdown
**Bekérés:**
"Mekkora költsége volt az ellátásnak? Kérem, a pénznemet is mondja meg."

**Példa:**
"Például 500 euró, vagy 200 ezer forint."

**Validálás:**
- Pozitív szám
- Ismert pénznem (EUR, USD, HUF, stb.)
```

### Telefonszám

```markdown
**Bekérés:**
"Milyen telefonszámon érhetjük el, ha kérdésünk lenne?"

**Formátum segítség:**
"Kérem, az előhívóval együtt mondja be, például +36 30 123 4567."

**Validálás:**
- Minimum 9 számjegy
- Lehet előhívó (+36, 06)
```

### Email cím

```markdown
**Bekérés:**
"Milyen email címre küldhetjük a visszaigazolást?"

**Pontosítás:**
"Betűzné a kukac előtti részt?"
"Ez @gmail.com / @freemail.hu, igaz?"

**Validálás:**
- Tartalmaz @-ot
- Tartalmaz domain-t
```

---

## Hiányzó Adat Kezelése

### Türelmes Megközelítés

```markdown
**Ha az ügyfél nem találja az adatot:**
"Semmi gond, ráér megnézni. Megvárom."
"Ha nincs most kéznél, a többi adatot felvesszük, és ezt később is beküldheti emailben."

**Ha az ügyfél bizonytalan:**
"Nem baj, ha nem emlékszik pontosan. Körülbelül mikor lehetett?"
"Próbáljon visszaemlékezni, nem kell teljesen pontos legyen."
```

### Alternatívák Felajánlása

```markdown
**Email küldés opció:**
"Ha most nem találja a [dokumentumot/adatot], elküldheti később emailben a [email cím] címre."

**Visszahívás opció:**
"Szeretné, ha később visszahívnánk, amikor már megvan az adat?"

**Online opció:**
"Ezt az adatot a honlapunkon is megadhatja: [url]"
```

---

## Adatvalidálás Script-ek

### Összefoglaló és Megerősítés

```markdown
**Összefoglalás minta:**
"Hadd foglaljam össze az eddig felvett adatokat:
- Név: [NÉV]
- Kötvényszám: [SZÁM]
- Dátum: [DÁTUM]
- Helyszín: [HELY]
Ezek helyesek?"
```

### Javítási Lehetőség

```markdown
**Ha az ügyfél javítani szeretne:**
"Melyik adatot szeretné módosítani?"
"Rendben, akkor a [mező] nem [régi érték], hanem [új érték]. Jól értem?"
```

---

## Speciális Esetek

### Harmadik Személyre Vonatkozó Adat

```markdown
"A biztosított [NÉV], de Ön a bejelentő.
Ön milyen kapcsolatban áll a biztosítottal?"
"Rendelkezik felhatalmazással az ügyintézésre?"
```

### Érzékeny Adatok

```markdown
**Egészségügyi:**
"Csak az ügyintézéshez szükséges egészségügyi információt kérem."
"Nem szükséges részletezni a diagnózist, elég a típusa (baleset/betegség)."

**Pénzügyi:**
"A pontos költségre van szükségem a feldolgozáshoz."
```

### Dokumentumok Bekérése

```markdown
**Lista a szükséges dokumentumokról:**
"A feldolgozáshoz a következő dokumentumokra lesz szükség:
1. Számlák eredeti példánya
2. Orvosi dokumentáció (ha van)
3. Utazási dokumentumok másolata

Ezeket a [email cím] címre küldheti."
```
