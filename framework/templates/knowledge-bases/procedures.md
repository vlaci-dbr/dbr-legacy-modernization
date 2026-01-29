# Procedures Knowledge Base MINTA

> **UTASÍTÁS CLAUDE-NAK:** Ezt a mintát használd eljárásrend típusú tudásbázis generálásához.
> Lépésről-lépésre útmutatók és folyamatok leírása.

---

## KB TARTALOM KEZDETE

# DOMAIN_NAME - Eljárásrendek

## PROCEDURE_1_NAME

### Mikor alkalmazandó
PROCEDURE_1_WHEN

### Szükséges adatok
- REQUIRED_DATA_1
- REQUIRED_DATA_2
- REQUIRED_DATA_3

### Lépések
1. **STEP_1_TITLE**
   STEP_1_DESCRIPTION

2. **STEP_2_TITLE**
   STEP_2_DESCRIPTION

3. **STEP_3_TITLE**
   STEP_3_DESCRIPTION

### Eredmény
PROCEDURE_1_OUTCOME

### Gyakori kérdések
- **K:** FAQ_1_QUESTION
- **V:** FAQ_1_ANSWER

---

## PROCEDURE_2_NAME

### Mikor alkalmazandó
PROCEDURE_2_WHEN

### Lépések
1. **STEP_1_TITLE**
   STEP_1_DESCRIPTION

### Eredmény
PROCEDURE_2_OUTCOME

---

## KB TARTALOM VÉGE

---

## STRUKTÚRA SZABÁLYOK

### Kötelező elemek eljárásonként
- Mikor alkalmazandó (előfeltételek)
- Szükséges adatok (lista)
- Lépések (számozott)
- Eredmény (mi történik a végén)

### Opcionális elemek
- Gyakori kérdések
- Speciális esetek
- Hibakezelés
- Kapcsolódó eljárások

### Formátum
- Lépések számozva: `1.`, `2.`, `3.`
- Lépés címe félkövér: `**Lépés címe**`
- Adatok listája: `-` kezdettel

---

## PÉLDA TARTALOM

# Kárigény Bejelentés - Eljárásrendek

## Egészségügyi kár bejelentése

### Mikor alkalmazandó
Külföldön bekövetkezett egészségügyi ellátás költségeinek igénylése esetén. Az eseménynek a kötvény érvényességi idején belül kellett történnie.

### Szükséges adatok
- Kötvényszám (10 számjegy)
- Biztosított neve (ahogy a kötvényen szerepel)
- Utazás időpontja (mettől-meddig)
- Utazás helyszíne (ország, város)
- Esemény dátuma
- Esemény leírása (mi történt)
- Ellátás típusa (orvosi/kórházi/gyógyszer)
- Költség összege (pénznemmel)
- Számlák megléte (igen/nem)

### Lépések
1. **Személyes adatok felvétele**
   Kérje el az ügyfél nevét, kötvényszámát és visszahívási számát. Ellenőrizze a kötvény érvényességét.

2. **Utazás adatainak rögzítése**
   Rögzítse az utazás időtartamát és helyszínét. Győződjön meg róla, hogy az esemény külföldön és az érvényességi időn belül történt.

3. **Esemény részleteinek rögzítése**
   Kérdezze meg, mi történt pontosan: mikor, hol, milyen körülmények között. Ne kérjen orvosi diagnózist, csak az esemény típusát (baleset/betegség).

4. **Költségek és dokumentumok**
   Kérdezze meg a költség összegét és pénznemét. Tájékoztassa, hogy milyen dokumentumokat kell benyújtani (számlák, orvosi papírok).

5. **Ügyszám generálása**
   Generáljon ügyszámot és tájékoztassa az ügyfelet a következő lépésekről.

### Eredmény
- Ügyszám generálva (formátum: KAR-YYYY-NNNNN)
- Email visszaigazolás küldve
- Dokumentum bekérő levél küldve

### Gyakori kérdések
- **K:** Mi van, ha nincs számlám?
- **V:** Próbálja beszerezni a számlákat az egészségügyi intézménytől. Számla nélkül a kártérítés nem garantált.

- **K:** Mennyi idő alatt dolgozzák fel?
- **V:** A teljes dokumentáció beérkezésétől számított 15 munkanapon belül.

### Speciális esetek
- **Kórházi ellátás:** Ha az ügyfél még kórházban van, kapcsolja a segélyvonalhoz közvetlen segítségért.
- **Nagyösszegű kár (500.000 Ft felett):** Jelezze, hogy felettes jóváhagyás szükséges lehet.

---

## Gépjármű kár bejelentése

### Mikor alkalmazandó
Külföldön bekövetkezett gépjármű káresemény (baleset, lopás, rongálás) esetén.

### Szükséges adatok
- Kötvényszám
- Gépjármű rendszáma
- Esemény helyszíne és ideje
- Kár leírása
- Rendőrségi jegyzőkönyv száma (ha van)
- Becsült kárérték

### Lépések
1. **Alapadatok felvétele**
   Kötvényszám, rendszám, biztosított neve.

2. **Esemény részletei**
   Mikor, hol, mi történt. Van-e rendőrségi jegyzőkönyv.

3. **Kár felmérése**
   Milyen sérülések vannak a járművön. Van-e becsült kárérték.

4. **Dokumentumok tájékoztatás**
   Szükséges: rendőrségi jegyzőkönyv, fényképek, szerviz árajánlat.

### Eredmény
- Ügyszám generálva
- Kárszakértő kirendelése (ha szükséges)
- Dokumentum bekérő küldve

---

## Poggyász kár bejelentése

### Mikor alkalmazandó
Elveszett, késve érkezett vagy megsérült poggyász esetén.

### Szükséges adatok
- Kötvényszám
- Légitársaság neve
- Járatszám
- PIR szám (légitársaság által kiadott)
- Hiányzó/sérült tárgyak listája
- Becsült érték

### Lépések
1. **Alapadatok és légitársaság**
   Kötvényszám, járatszám, légitársaság neve.

2. **PIR szám bekérése**
   A légitársaságtól kapott Property Irregularity Report száma KÖTELEZŐ.

3. **Tárgyak listázása**
   Milyen tárgyak hiányoznak/sérültek, becsült értékük.

4. **Tájékoztatás**
   Eredeti számlák szükségesek a tárgyakról (ha vannak).

### Eredmény
- Ügyszám generálva
- Dokumentum bekérő küldve
- Légitársasági kártérítés levonásra kerül

### Fontos szabály
A légitársaság kártérítése levonásra kerül a biztosítási összegből (nem dupla térítés).
