# 💰 Guida alla Monetizzazione di ipsedigit

Questa guida ti spiega come iniziare a guadagnare dal sito.

---

## 📋 Checklist Pre-Monetizzazione

Prima di iniziare, assicurati di avere:

- [ ] **Traffico minimo**: Almeno 100-500 visite/giorno (verifica su Google Analytics)
- [ ] **Contenuti**: Almeno 30-50 post pubblicati
- [ ] **Età dominio**: Sito attivo da almeno 1-3 mesi

---

## 1️⃣ Google AdSense (Consigliato - Guadagno Passivo)

**Guadagno stimato**: €1-5 per 1000 visite (varia molto)

### Setup:

1. Vai su [Google AdSense](https://www.google.com/adsense)
2. Registrati con il tuo account Google
3. Aggiungi il sito `ipsedigit.github.io`
4. Attendi approvazione (1-14 giorni)
5. Una volta approvato, copia il tuo `Publisher ID` (es: `ca-pub-1234567890123456`)
6. Apri `docs/_config.yml` e aggiungi:

```yaml
adsense_id: ca-pub-XXXXXXXXXX  # Sostituisci con il tuo ID
```

7. Vai su AdSense > Ads > By ad unit > Create new ad unit
8. Crea 3 ad unit:
   - `TOP_AD_SLOT` - Banner orizzontale per homepage top
   - `MID_AD_SLOT` - Auto ads per feed
   - `BOTTOM_AD_SLOT` - Banner per footer

9. Sostituisci `TOP_AD_SLOT`, `MID_AD_SLOT`, `BOTTOM_AD_SLOT` in `docs/index.md` con gli slot ID reali

**Nota**: GitHub Pages è supportato da AdSense.

---

## 2️⃣ Buy Me a Coffee / Ko-fi (Donazioni)

**Guadagno stimato**: €0-50/mese (dipende dalla community)

### Setup Buy Me a Coffee:

1. Vai su [buymeacoffee.com](https://www.buymeacoffee.com)
2. Crea account gratuito
3. Personalizza la tua pagina
4. Apri `docs/_config.yml` e aggiungi:

```yaml
buymeacoffee: tuo-username
```

### Setup Ko-fi:

1. Vai su [ko-fi.com](https://ko-fi.com)
2. Crea account gratuito
3. Apri `docs/_config.yml` e aggiungi:

```yaml
kofi: tuo-username
```

---

## 3️⃣ Affiliate Marketing (Futuro)

**Guadagno stimato**: €10-100/mese se ben implementato

Quando hai traffico sufficiente, considera:

- **Amazon Associates**: Link a libri tech, hardware
- **Digital Ocean / Vultr**: $100+ per referral hosting
- **Corso Udemy/Coursera**: 10-50% commissione

*Implementazione futura: Lo script può aggiungere automaticamente link affiliati basati sui tag del post.*

---

## 4️⃣ Sponsored Posts (Avanzato)

**Guadagno stimato**: €50-500 per post

Quando hai 5000+ visite/mese:

1. Crea una pagina "Advertise"
2. Contatta aziende tech per sponsored content
3. Prezzo suggerito: €0.05-0.10 per visita media

---

## 📊 Tracking & Ottimizzazione

### Google Analytics già configurato
Controlla regolarmente:
- Visite giornaliere
- Fonti di traffico (Google, social, direct)
- Post più popolari

### Google Search Console
1. Vai su [search.google.com/search-console](https://search.google.com/search-console)
2. Aggiungi `ipsedigit.github.io`
3. Verifica via DNS o HTML file
4. Monitora:
   - Keyword che portano traffico
   - Errori di indicizzazione
   - Click-through rate

---

## 🎯 Obiettivi Realistici

| Visite/giorno | AdSense/mese | Totale stimato |
|---------------|--------------|----------------|
| 100           | €3-15        | €5-20          |
| 500           | €15-75       | €20-100        |
| 1000          | €30-150      | €50-200        |
| 5000          | €150-750     | €200-1000      |

---

## ⚠️ Note Importanti

1. **Pazienza**: I primi guadagni arrivano dopo 2-3 mesi
2. **SEO**: Continua a pubblicare contenuti per crescere
3. **No click fraud**: Non cliccare mai sui tuoi ads
4. **Qualità**: Google premia siti con contenuti utili

---

*Ultimo aggiornamento: Febbraio 2026*

