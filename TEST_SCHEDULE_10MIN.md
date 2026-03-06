# ⚡ CONFIGURAZIONE TEST RAPIDO - Pubblicazione ogni 10 minuti

## 🎯 Modifiche Applicate (06/03/2026)

### 1. GitHub Actions Workflow
**File:** `.github/workflows/dailynewspublisher.yml`

**PRIMA:**
```yaml
schedule:
  - cron: '0 1 * * *'   # Ogni 4 ore
  - cron: '0 3 * * *'
  # ... 8 volte al giorno
```

**ADESSO (TEST):**
```yaml
schedule:
  - cron: '*/10 * * * *'   # Ogni 10 minuti ⚡
```

### 2. Limiti di Pubblicazione
**File:** `const.py`

| Parametro | Prima | Adesso (TEST) |
|-----------|-------|---------------|
| `DAILY_TARGET` | 12 | 100 |
| `MAX_POSTS_PER_NICHE_PER_DAY` | 3 | 20 |
| `MAX_PER_TYPE` | 4 | 20 |

---

## 📊 Cosa Aspettarsi

### Timeline di Test:
```
12:00 - Primo post pubblicato
12:10 - Secondo post
12:20 - Terzo post
12:30 - Quarto post
...
14:00 - ~12 post pubblicati (se ci sono abbastanza candidati)
```

### Durata Stimata:
- **2 ore** = ~12 post (simulazione giornata normale)
- **4 ore** = ~24 post (vedere effetto algoritmo su volume alto)
- **8 ore** = ~48 post (stress test completo)

---

## 🔙 RIPRISTINO VALORI NORMALI

### ⚠️ IMPORTANTE: Dopo il test, ripristinare i valori originali!

### Step 1: Ripristinare Workflow
**File:** `.github/workflows/dailynewspublisher.yml`

```yaml
schedule:
  # Run 8 times/day: every 4 hours around the clock (UTC)
  - cron: '0 1 * * *'
  - cron: '0 3 * * *'
  - cron: '0 5 * * *'
  - cron: '0 7 * * *'
  - cron: '0 11 * * *'
  - cron: '0 15 * * *'
  - cron: '0 19 * * *'
  - cron: '0 23 * * *'
```

### Step 2: Ripristinare Limiti
**File:** `const.py`

```python
MAX_POSTS_PER_NICHE_PER_DAY = 3     # Era 20
DAILY_TARGET = 12                    # Era 100
MAX_PER_TYPE = 4                     # Era 20
```

---

## 🧪 Cosa Monitorare Durante il Test

1. **Diversità categorie** - Il nuovo algoritmo a pesi funziona?
2. **Qualità post** - Gli articoli pubblicati sono rilevanti?
3. **Performance** - Il sistema gestisce pubblicazioni frequenti?
4. **Bilanciamento** - Rapporto tra nicchie preferite e altre categorie

---

## 📝 Comandi Utili

### Eseguire Manualmente (locale):
```bash
python main.py --action=news
```

### Eseguire Workflow Manualmente (GitHub):
1. Vai su GitHub → Actions → Daily News Publisher
2. Click "Run workflow"
3. (Opzionale) Specifica una nicchia

### Vedere gli ultimi post pubblicati:
```bash
ls -lt docs/_posts/ | head -20
```

### Controllare quanti post oggi:
```bash
grep "$(date +%Y-%m-%d)" news/daily_categories.txt | wc -l
```

---

## 🚨 Note Importanti

1. **GitHub Actions ha un limite di 1000 esecuzioni/mese** (gratis)
   - 10 minuti × 6 esecuzioni/ora × 24 ore = **144 esecuzioni/giorno**
   - NON lasciare attivo per più di 2-3 giorni!

2. **Il file `news/daily_categories.txt` si resetta automaticamente ogni giorno**
   - Basato sulla data corrente
   - Ogni giorno parte da 0 post

3. **Candidati limitati**
   - Se non ci sono abbastanza articoli con score ≥ 70, si fermerà
   - Potresti vedere meno pubblicazioni dopo le prime ore

---

## 📅 Checklist Post-Test

- [ ] Ripristinare cron schedule in `.github/workflows/dailynewspublisher.yml`
- [ ] Ripristinare DAILY_TARGET = 12 in `const.py`
- [ ] Ripristinare MAX_POSTS_PER_NICHE_PER_DAY = 3 in `const.py`
- [ ] Ripristinare MAX_PER_TYPE = 4 in `const.py`
- [ ] Commit e push modifiche
- [ ] Verificare che il workflow sia tornato normale su GitHub Actions

---

**Data configurazione:** 2026-03-06  
**Scopo:** Test rapido nuovo algoritmo di selezione  
**Durata prevista test:** 2-4 ore (pranzo → pomeriggio)  
**Status:** ⚡ ATTIVO - Ricordati di ripristinare!

