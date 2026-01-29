# Domain Knowledge Base MINTA

> **UTASÍTÁS CLAUDE-NAK:** Ezt a mintát használd szakterületi tudásbázis generálásához.
> Fogalmak, szabályok és domain-specifikus információk.

---

## KB TARTALOM KEZDETE

# DOMAIN_NAME - Szakterületi Tudás

## Alapfogalmak

### TERM_1
**Definíció:** TERM_1_DEFINITION
**Példa:** TERM_1_EXAMPLE

### TERM_2
**Definíció:** TERM_2_DEFINITION
**Példa:** TERM_2_EXAMPLE

---

## Szabályok és Feltételek

### RULE_1_NAME
RULE_1_DESCRIPTION

**Alkalmazás:**
- RULE_1_APPLICATION_1
- RULE_1_APPLICATION_2

### RULE_2_NAME
RULE_2_DESCRIPTION

---

## Gyakori Esetek

### CASE_1_NAME
**Leírás:** CASE_1_DESCRIPTION
**Teendő:** CASE_1_ACTION

---

## KB TARTALOM VÉGE

---

## STRUKTÚRA SZABÁLYOK

### Kötelező szekciók
- Alapfogalmak (definíciók)
- Szabályok és feltételek

### Opcionális szekciók
- Gyakori esetek
- Kivételek
- Kapcsolódó területek

### Formátum
- Fogalmak: `### Fogalom név` + `**Definíció:**`
- Példák: `**Példa:**` formátumban
- Szabályok: leírás + alkalmazási lista

---

## PÉLDA TARTALOM

# Utasbiztosítás - Szakterületi Tudás

## Alapfogalmak

### Kötvény
**Definíció:** A biztosítási szerződést igazoló dokumentum, amely tartalmazza a biztosítás feltételeit és érvényességi idejét.
**Példa:** "A kötvényszáma 10 számjegyből áll, például 1234567890."

### Biztosított
**Definíció:** Az a személy, akire a biztosítás vonatkozik és akinek javára a biztosító teljesít.
**Példa:** "A biztosított neve megegyezik a kötvényen szereplő névvel."

### Önrész
**Definíció:** A kár azon része, amelyet a biztosított saját maga visel, nem téríti a biztosító.
**Példa:** "10.000 Ft önrész esetén egy 50.000 Ft-os kárból 40.000 Ft-ot térít a biztosító."

### Területi hatály
**Definíció:** Az a földrajzi terület, ahol a biztosítás érvényes.
**Példa:** "Az utasbiztosítás általában külföldön érvényes, belföldön nem."

### Várakozási idő
**Definíció:** A biztosítás megkötése és hatályba lépése közötti időszak.
**Példa:** "Ha ma köti meg, holnaptól érvényes (24 óra várakozási idő)."

### Káresemény
**Definíció:** Olyan váratlan esemény, amely a biztosítás alapján térítésre jogosít.
**Példa:** "Baleset, betegség, poggyász elvesztése."

---

## Szabályok és Feltételek

### 48 órás bejelentési szabály
A káreseményt 48 órán belül be kell jelenteni a biztosítónak.

**Alkalmazás:**
- Sürgősségi ellátás esetén kivétel tehető
- A 48 óra az esemény bekövetkeztétől számít
- Késedelmes bejelentés esetén a térítés csökkenhet

### Eredeti számla szabály
Csak eredeti számlák alapján történik kártérítés.

**Alkalmazás:**
- Másolat nem elfogadható
- A számla tartalmazza a szolgáltatás leírását
- A pénznem és összeg egyértelműen olvasható

### Területi korlátozás
Az utasbiztosítás CSAK külföldön érvényes.

**Alkalmazás:**
- Magyarországi események nem téríthetők
- A határ átlépésétől érvényes
- Hazaérkezésig tart

### Előzetes betegség kizárás
Előzetes betegségek kezelése általában nem térül.

**Alkalmazás:**
- Krónikus betegségek akut rosszabbodása: igen
- Tervezett kezelés: nem
- Kérdéses esetben orvosi vélemény szükséges

---

## Gyakori Esetek

### Ügyfél külföldön kórházban van
**Leírás:** Az ügyfél jelenleg külföldi kórházban tartózkodik és segítséget kér.
**Teendő:** Azonnal kapcsolja a 24 órás segélyvonalhoz (+36 1 234 5680). Ők koordinálják a kórházzal és szükség esetén a hazaszállítást.

### Ügyfél nem találja a kötvényszámát
**Leírás:** Az ügyfél nem tudja a kötvényszámát.
**Teendő:** Kérje el a nevét és születési dátumát, ezekkel is azonosítható a rendszerben. Alternatíva: email cím, amelyre a kötvényt küldték.

### Kár összege meghaladja a limitet
**Leírás:** A kárigény összege meghaladja a biztosítási összeget.
**Teendő:** Tájékoztassa az ügyfelet, hogy a biztosítás maximum összegéig térít. A különbözetet az ügyfél viseli.

### Több káresemény egy utazás alatt
**Leírás:** Az ügyfélnek több különböző kára is keletkezett (pl. betegség ÉS poggyász).
**Teendő:** Mindegyiket külön ügyszámon kell kezelni. A limitek típusonként külön számítanak.

---

## Speciális Szabályok

### Extrém sport fedezet
**Szabály:** Extrém sportok (síelés, búvárkodás, stb.) csak külön kiegészítővel fedezettek.
**Ellenőrzés:** A kötvényen szerepel-e "Extrém Sport Kiegészítő"
**Ha nincs:** Az extrém sport közben bekövetkezett kár nem térül

### Alkohol hatása
**Szabály:** Alkoholos befolyásoltság alatt bekövetkezett károk nem térülnek.
**Kivétel:** Ha bizonyítható, hogy az alkohol nem volt oka a kárnak
**Megjegyzés:** Ezt érzékenyen kell kezelni, ne vádolja az ügyfelet

### Háború és terrorizmus
**Szabály:** Háborús övezetek és terrorcselekmények általában kizártak.
**Kivétel:** Egyes prémium csomagok korlátozott terrorbiztosítást tartalmaznak
**Ellenőrzés:** A kötvény részletes feltételeiben található
