# /generate-kb - Knowledge Base Generálása

## Leírás

Tudásbázis tartalmat generálok template alapján.

## Folyamat

1. Olvasd be: `.claude/guides/kb-generation-guide.md`
2. Kérdezd meg a KB típusát
3. Olvasd be a template-et
4. Gyűjtsd össze a tartalmat interaktívan
5. Generáld a KB-t
6. Rendeld hozzá a megfelelő agent-ekhez

## KB Típusok

| Típus | Template | Használat |
|-------|----------|-----------|
| faq | faq.md | Kérdés-válasz |
| product-catalog | product-catalog.md | Termékek/szolgáltatások |
| company-info | company-info.md | Céginfo, elérhetőségek |
| procedures | procedures.md | Eljárásrendek |
| domain-knowledge | domain-knowledge.md | Szakterületi tudás |

## Lépések

### 1. KB típus kiválasztás
```
Milyen típusú tudásbázist szeretne létrehozni?
1. faq - Gyakran ismételt kérdések
2. product-catalog - Termékek és szolgáltatások
3. company-info - Cég bemutatkozás
4. procedures - Eljárásrendek, folyamatok
5. domain-knowledge - Szakterületi fogalmak
```

### 2. KB azonosító megadása
```
KB azonosító (kb- prefixszel, pl. kb-company-faq):
```

### 3. Template beolvasása
```
framework/templates/knowledge-bases/<tipus>.md
```

### 4. Tartalom gyűjtése

**FAQ esetén:**
```
Hány kategóriát szeretne?
> 3

1. kategória neve:
> Elérhetőség

1. kategória kérdései:
- Mik a nyitvatartási idők?
- Hogyan érhetem el az ügyfélszolgálatot?

(és így tovább...)
```

**Product Catalog esetén:**
```
Hány termékkategória van?
> 2

1. kategória neve:
> Biztosítási csomagok

1. kategória termékei:
- Prémium Utasbiztosítás: Teljes körű fedezet, napi 1500 Ft
- Alap Utasbiztosítás: Alapvető fedezet, napi 800 Ft

(és így tovább...)
```

**Company Info esetén:**
```
Cég neve:
Cég leírása:
Alapítás éve:
Székhely:
Elérhetőségek:
Szolgáltatások:
```

**Procedures esetén:**
```
Hány eljárás van?
> 2

1. eljárás neve:
> Egészségügyi kár bejelentése

Mikor alkalmazandó:
> Külföldi egészségügyi ellátás költségeinek igénylése

Szükséges adatok:
- Kötvényszám
- Biztosított neve
- ...

Lépések:
1. Személyes adatok felvétele
2. Esemény részleteinek rögzítése
3. ...
```

**Domain Knowledge esetén:**
```
Szakterület neve:
> Utasbiztosítás

Alapfogalmak (név: definíció):
- Kötvény: A biztosítási szerződést igazoló dokumentum
- Önrész: A kár azon része, amit a biztosított fizet
- ...

Szabályok:
- 48 órás bejelentési szabály
- Eredeti számla szabály
- ...
```

### 5. KB generálása
A template struktúrája szerint.

### 6. Agent hozzárendelés
```
Melyik agent-ekhez rendeljük a KB-t?
[ ] receptionist
[x] health-specialist
[x] vehicle-specialist
[ ] finalizer
```

### 7. Mentés
```
knowledge-bases/<kb-id>.md
```

## Output

`knowledge-bases/<kb-id>.md`

## Példa

```
/generate-kb

> Típus: faq
> KB ID: kb-general-faq
> Kategóriák: Elérhetőség, Biztosítás, Kárigény

✓ KB létrehozva: knowledge-bases/kb-general-faq.md
  - 3 kategória
  - 9 kérdés-válasz pár
  - Hozzárendelve: receptionist
```

## Formázási Szabályok

- Rövid válaszok (max 3-4 mondat)
- Konkrét adatok (számok, dátumok)
- Egyszerű, közérthető nyelv
- Nincs redundancia
