# Knowledge Base Generálási Útmutató

## Áttekintés

Ez az útmutató elmagyarázza, hogyan generálj tudásbázis tartalmakat a template-ekből.

---

## KB Típusok

| Típus | Template | Mikor használd |
|-------|----------|----------------|
| **FAQ** | `faq.md` | Kérdés-válasz formátum |
| **Product Catalog** | `product-catalog.md` | Termékek/szolgáltatások |
| **Company Info** | `company-info.md` | Cég bemutatkozás |
| **Procedures** | `procedures.md` | Lépésről-lépésre útmutató |
| **Domain Knowledge** | `domain-knowledge.md` | Szakterületi fogalmak |

---

## Generálási Folyamat

### 1. KB típus meghatározása

Kérdezd meg:
- Mi a KB célja?
- Milyen kérdésekre kell választ adnia?
- Melyik agent(ek) fogják használni?

**Döntési segítség:**

| Ha az ügyfél kérdez... | KB típus |
|------------------------|----------|
| "Mik a nyitvatartási idők?" | FAQ vagy Company Info |
| "Mennyibe kerül X?" | Product Catalog |
| "Hogyan működik a bejelentés?" | Procedures |
| "Mi az az önrész?" | Domain Knowledge |

### 2. Template beolvasása

Olvasd be a megfelelő template-et:
```
framework/templates/knowledge-bases/<tipus>.md
```

### 3. Tartalom gyűjtése

Kérdezd meg a felhasználótól:

**FAQ-hoz:**
- Kategóriák (pl. Nyitvatartás, Szolgáltatások, Árak)
- Leggyakoribb kérdések kategóriánként
- Válaszok (röviden, lényegre törően)

**Product Catalog-hoz:**
- Termékkategóriák
- Termékek neve, leírása, ára
- Főbb jellemzők

**Company Info-hoz:**
- Cég neve és leírása
- Elérhetőségek (cím, telefon, email)
- Nyitvatartás
- Főbb szolgáltatások

**Procedures-hez:**
- Milyen folyamatokat kell leírni?
- Lépések minden folyamathoz
- Szükséges adatok
- Eredmény/kimenet

**Domain Knowledge-hoz:**
- Szakterület neve
- Alapfogalmak és definíciók
- Szabályok és feltételek
- Gyakori esetek

### 4. KB generálása

A template struktúráját követve:
- Tartsd meg a formázási szabályokat
- Használj rövid, lényegre törő mondatokat
- Kerüld a redundanciát
- Adj konkrét példákat

### 5. Fájl mentése

Mentsd el:
```
projects/<projekt>/knowledge-bases/<kb-id>.md
```

A `kb-id` formátuma: `kb-<leíró-név>` (pl. `kb-company-faq`, `kb-health-procedures`)

---

## Formázási Szabályok

### Markdown szintaxis
- `#` Fő cím (KB neve)
- `##` Kategória/szekció
- `###` Alcím/tétel
- `**Félkövér:**` Mezőnév
- `-` Listaelem
- `---` Elválasztó

### Hosszúság irányelvek
- Válaszok: Max 3-4 mondat
- Leírások: Max 2 mondat
- Lista elemek: Max 10-15 szó

### Stílus
- Egyszerű, közérthető nyelv
- Kerüld a szakzsargont (vagy magyarázd el)
- Aktív megfogalmazás
- Konkrét számok és adatok (ne "körülbelül")

---

## Agent-KB Hozzárendelés

### Általános szabályok

| KB típus | Ajánlott agent-ek |
|----------|-------------------|
| Company Info | Minden agent (általános információ) |
| FAQ | Orchestrator (gyakori kérdések gyors válaszokhoz) |
| Product Catalog | Specialist (termékszakértő) |
| Procedures | Specialist + Finalizer (folyamatok) |
| Domain Knowledge | Specialist (szakterületi tudás) |

### Példa hozzárendelések

**Biztosítási projekt:**
- `kb-company-info` → Minden agent
- `kb-general-faq` → Receptionist (orchestrator)
- `kb-health-procedures` → Health Specialist
- `kb-insurance-terms` → Minden specialist

**Ügyfélszolgálat projekt:**
- `kb-company-info` → Minden agent
- `kb-product-catalog` → Sales Specialist
- `kb-support-procedures` → Support Specialist

---

## KB ID Konvenciók

### Formátum
```
kb-<típus>-<téma>
```

### Példák
- `kb-company-faq` - Cég általános GYIK
- `kb-health-procedures` - Egészségügyi eljárások
- `kb-product-insurance` - Biztosítási termékek
- `kb-terms-glossary` - Fogalomtár

### Szabályok
- Mindig `kb-` prefix
- Kebab-case (kötőjeles)
- Angol nyelven (a kód konzisztenciájáért)
- Leíró, de rövid

---

## Minőségi Ellenőrzés

### Generálás után ellenőrizd:

- [ ] A struktúra követi a template-et?
- [ ] Nincsenek üres szekciók?
- [ ] A válaszok rövidek és lényegre törőek?
- [ ] Konkrét adatok vannak (nem "körülbelül")?
- [ ] Nincs redundancia (ismétlődő információ)?
- [ ] A fogalmak érthetőek (vagy meg vannak magyarázva)?
- [ ] A formázás konzisztens?

### Gyakori hibák

1. **Túl hosszú válaszok** - Max 3-4 mondat
2. **Hiányzó konkrét adatok** - Számok, dátumok kellenek
3. **Szakzsargon** - Vagy kerüld, vagy magyarázd el
4. **Redundancia** - Egy információ egy helyen legyen
5. **Elavult információ** - Ellenőrizd az aktualitást

---

## Példa: Teljes KB Generálás

### Input

```
Típus: FAQ
Cég: ABC Biztosító
Kategóriák: Elérhetőség, Biztosítás, Kárigény
```

### Generált output

```markdown
# ABC Biztosító - Gyakran Ismételt Kérdések

## Kategória: Elérhetőség

### K: Mik a nyitvatartási idők?
**V:** Hétfőtől péntekig 8:00-17:00 között vagyunk elérhetők.

### K: Hogyan érhetem el az ügyfélszolgálatot?
**V:** Telefonon: +36 1 234 5678, emailben: info@abc.hu

---

## Kategória: Biztosítás

### K: Milyen biztosításokat kínálnak?
**V:** Utasbiztosítást kínálunk külföldi utazásokhoz, orvosi költség és poggyász fedezettel.

### K: Mennyibe kerül a biztosítás?
**V:** Napi 800 Ft-tól, az utazás hosszától és a csomagtól függően.

---

## Kategória: Kárigény

### K: Hogyan jelenthetek be kárt?
**V:** Telefonon vagy emailben a kötvényszám megadásával.

### K: Mennyi idő a feldolgozás?
**V:** Maximum 15 munkanap a dokumentumok beérkezésétől.
```

---

## KB Frissítés

Ha egy meglévő KB-t kell frissíteni:

1. Olvasd be a jelenlegi KB-t
2. Azonosítsd a változásokat
3. Frissítsd a releváns szekciókat
4. Ellenőrizd a konzisztenciát
5. Mentsd el ugyanarra a helyre

**Figyelem:** Ne törölj információt, ha nem vagy biztos benne, hogy elavult!
