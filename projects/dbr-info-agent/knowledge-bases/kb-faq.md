# DBR Kft. - Gyakori Kérdések (FAQ)

## Általános kérdések a cégről

### Ki a DBR Kft.?
A Digitális Banki Rendszerek Kft. (DBR) egy több mint 30 éve működő magyar bankinformatikai megoldásszállító. ISO 9001 minősítéssel rendelkezünk 2002 óta, és a legnagyobb hazai és nemzetközi bankok partnerei vagyunk.

### Milyen referenciáik vannak?
Büszke partnereink között szerepel a BNP Paribas, CIB Bank, Citibank, MBH Bank, OTP Bank, Raiffeisen Bank, Allianz és Budapest Bank, valamint számos további pénzügyi intézmény.

### Hogyan vehetem fel a kapcsolatot?
- **Email:** mail@dbr.hu
- **Telefon:** +36 20 961 2356
- **Cím:** H-1116 Budapest, Fehérvári út 108-112

---

## Legacy Rendszer Modernizáció

### Mi az a legacy rendszer?
Legacy rendszernek nevezzük azokat az informatikai rendszereket, amelyek régebbi technológiákon alapulnak (például COBOL, PL/1, Fortran), de még mindig kritikus üzleti funkciókat látnak el. Globálisan több mint 220 milliárd sor COBOL kód fut ma is éles rendszerekben, és a banki core rendszerek 43%-a még mindig COBOL alapú.

### Miért érdemes modernizálni a legacy rendszereket?
- **Növekvő karbantartási költségek:** Az IT költségvetések 70-80%-a megy legacy rendszerek fenntartására
- **Szakemberhiány:** A COBOL fejlesztők átlagéletkora 55+ év, egyre kevesebben vannak
- **Biztonsági kockázatok:** A régi rendszerek nem rendelkeznek modern biztonsági funkciókkal
- **Korlátozott skálázhatóság:** Nehéz integrálni új szolgáltatásokkal
- **Megfelelőségi problémák:** GDPR, PCI-DSS és más szabályozásoknak való megfelelés nehézkes

### Mi az a CodeRevive platform?
A CodeRevive a DBR saját fejlesztésű, AI-vezérelt legacy rendszer modernizációs platformja. Mesterséges intelligenciát használunk a forráskód elemzésére, dokumentálására és modern technológiákra való átültetésére.

### Milyen eredményeket érhetünk el a CodeRevive-val?
- **3-5x gyorsabb** modernizáció a hagyományos módszereknél
- **30-50% költségmegtakarítás**
- **83% automatizáltsági fok** a kód konverzióban
- **93% funkcionális ekvivalencia** már első körben
- **60%-kal alacsonyabb projekt bukási ráta**

### Milyen nyelvekről tudnak konvertálni?
Jelenleg támogatott forrásnyelvek:
- **COBOL** (leggyakoribb banki legacy nyelv)
- **PL/1**
- **Fortran**

Célnyelvek:
- **Java** (leggyakrabban használt)
- **Python**
- Modern mikroszerviz architektúrák

### Mennyi ideig tart egy modernizációs projekt?
A hagyományos módszerekkel 12-18 hónap lenne egy átlagos projekt. A CodeRevive platformmal ez **6-10 hónapra** csökkenthető. A pontos időtartam függ:
- A forráskód méretétől (kódsorok száma)
- A rendszer komplexitásától
- A dokumentáltság szintjétől
- A célarchitektúrától

### Mennyibe kerül egy modernizációs projekt?
A hagyományos modernizáció költsége $8-$25 / kódsor. A CodeRevive platform alapú megközelítésünkkel ez **$4-$12 / kódsorra** csökkenthető. Átlagos projektméret: 250,000 - 1,500,000 EUR.

Kérjen egyedi árajánlatot a konkrét rendszer felmérése alapján!

---

## A Modernizációs Folyamat

### Hogyan zajlik a modernizációs folyamat?
1. **Felmérés és elemzés** - A meglévő rendszer átvizsgálása
2. **Dokumentáció generálás** - AI-alapú automatikus dokumentálás
3. **Üzleti logika kinyerése** - Rejtett szabályok és folyamatok feltárása
4. **Kód konverzió** - Automatizált átalakítás modern nyelvre
5. **Tesztelés és validáció** - Funkcionális ekvivalencia ellenőrzése
6. **Mikroszerviz dekompozíció** - Modern architektúra kialakítása
7. **Élesítés és átállás** - Fokozatos, kockázatmentes migráció

### Mi történik, ha nincs dokumentáció a régi rendszerhez?
Ez nagyon gyakori probléma - a legacy rendszerek többségénél hiányzik vagy elavult a dokumentáció. Az AI platformunk képes:
- A forráskódból automatikusan dokumentációt generálni
- Az üzleti logikát kinyerni és érthetően leírni
- A rejtett függőségeket és kapcsolatokat feltárni

### Garantált a 100%-os funkcionális megfelelőség?
Igen! A CodeRevive platform egyik legfontosabb jellemzője az **integritás megőrzése**. Automatikus teszt generálással és szigorú validációval biztosítjuk, hogy a modernizált rendszer pontosan ugyanazt a funkcionalitást nyújtsa, mint az eredeti.

---

## Technikai Kérdések

### Milyen AI technológiát használnak?
- **Specializált LLM-ek** (Large Language Models) a legacy kódok elemzésére
- **Validált átalakítási lánc** garantált minőséggel
- **Önjavító visszacsatolási hurok** automatikus teszt generálással
- **Domain-specifikus finomhangolás** banki és ipari rendszerekre

### Mi az a mikroszerviz architektúra?
A mikroszerviz architektúra egy modern szoftvertervezési megközelítés, ahol a nagy, monolitikus alkalmazást kisebb, önálló szolgáltatásokra bontjuk. Előnyei:
- Könnyebb karbantarthatóság
- Független skálázhatóság
- Gyorsabb fejlesztési ciklusok
- Jobb hibatűrés

### Támogatják a felhőbe költözést is?
Igen! A modernizált rendszereket fel lehet készíteni cloud-native működésre:
- AWS, Azure, GCP kompatibilitás
- Konténerizáció (Docker, Kubernetes)
- CI/CD pipeline kialakítás

---

## Egyéb Szolgáltatások

### Milyen egyéb szolgáltatásokat nyújt a DBR?
- **Szoftverfejlesztés:** Banki CORE rendszerek, VISA/Mastercard authorizáció
- **Hardverfejlesztés:** Biometrikus automaták, minibank terminálok
- **Rendszer üzemeltetés:** Központi távfelügyelet, országos szerviz

### Mi az a netBAR és CheckSign?
- **netBAR:** Központi Hitelinformációs Rendszer (KHR) kapcsolat
- **CheckSign:** Aláírás és rendelkezési jog ellenőrző rendszer

---

## Kapcsolatfelvétel

### Hogyan kérhetek árajánlatot?
Vegye fel velünk a kapcsolatot:
- **Email:** mail@dbr.hu
- **Telefon:** +36 20 961 2356

Készséggel készítünk ingyenes előzetes felmérést a rendszeréről!

### Van lehetőség demo bemutatóra?
Igen! Szívesen bemutatjuk a CodeRevive platform működését élőben. Kérjen időpontot a mail@dbr.hu címen!
