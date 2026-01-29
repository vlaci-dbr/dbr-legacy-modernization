# DBR Legacy Modernizáció - Landing Page

Landing page a DBR Kft. legacy modernizációs szolgáltatásához, ElevenLabs voice widget integrációval.

## GitHub Pages Deployment

### 1. Repository létrehozása

```bash
cd docs
git init
git add .
git commit -m "Initial commit - DBR Legacy Modernization landing page"
git branch -M main
git remote add origin https://github.com/<username>/dbr-legacy-modernization.git
git push -u origin main
```

### 2. GitHub Pages bekapcsolása

1. Menj a repository **Settings** oldalára
2. Válaszd a **Pages** menüpontot (bal oldali menü)
3. **Source** alatt válaszd: "Deploy from a branch"
4. **Branch** alatt válaszd: `main` és `/docs` mappa (vagy `/root` ha a docs tartalmát másoltad a root-ba)
5. Kattints **Save**

### 3. Elérhetőség

A site elérhető lesz: `https://<username>.github.io/dbr-legacy-modernization/`

## Fájlok

- `docs/index.html` - A teljes landing page (HTML + CSS inline)
- `docs/.nojekyll` - Jekyll feldolgozás kikapcsolása
- `docs/CNAME` - Egyéni domain beállításához (opcionális)

## ElevenLabs Widget

A widget automatikusan betöltődik a lap alján:

```html
<elevenlabs-convai agent-id="agent_0101kg36cz3qez9tjhxemsapxrg0"></elevenlabs-convai>
<script src="https://elevenlabs.io/convai-widget/index.js" async type="text/javascript"></script>
```

## Testreszabás

### Színek módosítása

A CSS változók a `<style>` blokk elején találhatók:

```css
:root {
    --primary-color: #1a365d;      /* Sötétkék - elsődleges szín */
    --accent-color: #2792dc;       /* Világoskék - kiemelő szín */
    --success-color: #38a169;      /* Zöld - sikeres elemek */
    --warning-color: #dd6b20;      /* Narancssárga - figyelmeztetések */
}
```

### Agent ID módosítása

Ha új agent-et hozol létre, cseréld ki az agent ID-t:

```html
<elevenlabs-convai agent-id="YOUR_NEW_AGENT_ID"></elevenlabs-convai>
```
