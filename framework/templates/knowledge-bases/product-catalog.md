# Product Catalog Knowledge Base MINTA

> **UTASÍTÁS CLAUDE-NAK:** Ezt a mintát használd termék/szolgáltatás katalógus típusú tudásbázis generálásához.

---

## KB TARTALOM KEZDETE

# COMPANY_NAME - Termékek és Szolgáltatások

## PRODUCT_CATEGORY_1_NAME

### PRODUCT_1_NAME
- **Leírás:** PRODUCT_1_DESCRIPTION
- **Ár:** PRODUCT_1_PRICE
- **Elérhetőség:** PRODUCT_1_AVAILABILITY
- **Főbb jellemzők:**
  - FEATURE_1
  - FEATURE_2
  - FEATURE_3

### PRODUCT_2_NAME
- **Leírás:** PRODUCT_2_DESCRIPTION
- **Ár:** PRODUCT_2_PRICE
- **Elérhetőség:** PRODUCT_2_AVAILABILITY

---

## PRODUCT_CATEGORY_2_NAME

### PRODUCT_3_NAME
- **Leírás:** PRODUCT_3_DESCRIPTION
- **Ár:** PRODUCT_3_PRICE
- **Elérhetőség:** PRODUCT_3_AVAILABILITY

---

## KB TARTALOM VÉGE

---

## STRUKTÚRA SZABÁLYOK

### Kötelező mezők termékenként
- Leírás (1-2 mondat)
- Ár (ha van, pénznemmel)
- Elérhetőség (készleten/rendelésre/nem elérhető)

### Opcionális mezők
- Főbb jellemzők (lista)
- Műszaki adatok
- Garancia
- Megjegyzések

### Formátum
- Kategóriák `##` fejléccel
- Termékek `###` fejléccel
- Mezők `- **Mezőnév:**` formátumban
- Listák `-` kezdettel

---

## PÉLDA TARTALOM

# EUB Biztosító - Biztosítási Csomagok

## Utasbiztosítások

### Prémium Utasbiztosítás
- **Leírás:** Teljes körű utasbiztosítás korlátlan orvosi költségtérítéssel külföldön.
- **Ár:** Napi 1.500 Ft-tól
- **Elérhetőség:** Online és telefonon
- **Főbb jellemzők:**
  - Korlátlan orvosi költség
  - Poggyász biztosítás 200.000 Ft-ig
  - Útlemondás fedezet
  - 24 órás segítségnyújtás

### Alap Utasbiztosítás
- **Leírás:** Kedvező árú biztosítás alapvető fedezettel.
- **Ár:** Napi 800 Ft-tól
- **Elérhetőség:** Online és telefonon
- **Főbb jellemzők:**
  - Orvosi költség 10 millió Ft-ig
  - Poggyász biztosítás 100.000 Ft-ig
  - Balesetbiztosítás

### Családi Csomag
- **Leírás:** Kedvezményes biztosítás 2 felnőtt + max. 3 gyermek részére.
- **Ár:** Napi 3.500 Ft-tól (család)
- **Elérhetőség:** Online és telefonon
- **Főbb jellemzők:**
  - Prémium fedezet mindenkinek
  - 20% családi kedvezmény
  - Közös poggyász limit

---

## Kiegészítő Szolgáltatások

### Extrém Sport Kiegészítő
- **Leírás:** Fedezet extrém sportokhoz (síelés, búvárkodás, stb.)
- **Ár:** +500 Ft/nap
- **Elérhetőség:** Csak Prémium csomaghoz

### Útlemondás Kiegészítő
- **Leírás:** Bővített útlemondási fedezet bármilyen okból.
- **Ár:** Az utazás árának 3%-a
- **Elérhetőség:** Minden csomaghoz

---

## Összehasonlító Táblázat

| Jellemző | Alap | Prémium | Családi |
|----------|------|---------|---------|
| Orvosi költség | 10M Ft | Korlátlan | Korlátlan |
| Poggyász | 100.000 Ft | 200.000 Ft | 300.000 Ft |
| Útlemondás | Nem | Igen | Igen |
| Ár/nap | 800 Ft | 1.500 Ft | 3.500 Ft |
