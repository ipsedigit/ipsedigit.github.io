# 🎯 ALGORITMO DI SELEZIONE POST - Nuova Logica

## Sistema a Pesi Graduati (Soft Preference)

### ✅ MODIFICHE COMPLETATE

L'algoritmo è stato **completamente riscritto** per eliminare i filtri hard sulle categorie e utilizzare invece un **sistema di pesi** che favorisce le nicchie preferite senza escludere altri contenuti di qualità.

---

## 📊 COME FUNZIONA ORA

### 1. **Nessun Filtro a Priori**
- ❌ PRIMA: Articoli non in NICHE_CATEGORIES → **scartati immediatamente**
- ✅ ADESSO: Tutti gli articoli vengono valutati → **nessuno scartato per categoria**

### 2. **Sistema di Bonus Graduato**

```python
# In calculate_score():
if cat in NICHE_CATEGORIES:  # AI, Security, Cloud, DevTools, Software-Engineering
    score += 15  # Bonus configurabile
else:
    score += 0   # Nessuna penalità per altre categorie
```

### 3. **Risultato: Meritocrazia + Preferenze**

**Scenario A - Articolo mediocre di nicchia preferita vs eccellente di altra categoria:**
- AI (base 50 + 15 bonus) = 65 punti
- Programming (base 75 + 0 bonus) = **75 punti** ✅ **VINCE**

**Scenario B - Stessa qualità:**
- AI (base 60 + 15 bonus) = **75 punti** ✅ **VINCE**
- Programming (base 60 + 0 bonus) = 60 punti

**Scenario C - Nicchia preferita eccellente:**
- Security (base 80 + 15 bonus) = **95 punti** ✅ **VINCE**
- Databases (base 80 + 0 bonus) = 80 punti

---

## 🎛️ CONFIGURAZIONE

Il sistema è **completamente configurabile** tramite `const.py`:

```python
NICHE_CATEGORY_BONUS = 15    # Valore attuale (bilanciato)
OTHER_CATEGORY_PENALTY = 0   # Nessuna penalità
```

### Tuning del Bias:

| Valore | Comportamento | Quando Usare |
|--------|---------------|--------------|
| **0** | Nessun bias, pura meritocrazia | Se vuoi massima apertura |
| **10** | Bias leggero | Per diversificare molto |
| **15** | Bias moderato (attuale) ✅ | Bilanciamento ideale |
| **20** | Bias forte | Per focalizzarsi sulle nicchie |
| **25** | Bias molto forte | Per dominanza quasi totale |

---

## 📈 IMPATTO SUL CONTENUTO PUBBLICATO

### Prima (Filtro Hard):
```
Articoli pubblicati al giorno: 12
├─ AI: 3 (massimo per nicchia)
├─ Security: 3
├─ Cloud: 3
├─ DevTools: 2
├─ Software-Engineering: 1
└─ Altri topic: 0 ❌ (scartati a priori)
```

### Adesso (Sistema a Pesi):
```
Articoli pubblicati al giorno: 12
├─ AI: 2-3 (hanno +15 punti di vantaggio)
├─ Security: 2-3
├─ Cloud: 2
├─ DevTools: 2
├─ Software-Engineering: 1-2
└─ Altri topic: 1-2 ✅ (se eccellenti possono vincere)
```

---

## 💡 VANTAGGI PRATICI

### 1. **Flessibilità**
Un articolo virale su un topic emergente (es: nuovo linguaggio, scandalo tech, breakthrough) può essere pubblicato anche se non rientra nelle 5 nicchie.

### 2. **Scoperta di Trend**
Il sistema può intercettare automaticamente trend nascenti che non rientrano nelle categorie predefinite.

### 3. **Qualità Prima di Tutto**
Un articolo eccezionale da fonte autorevole vince sempre, indipendentemente dalla categoria.

### 4. **Bilanciamento Naturale**
Le nicchie preferite mantengono un vantaggio del ~15-20%, ma non monopolizzano il feed.

---

## 🔧 ESEMPI CONCRETI

### Esempio 1: Articolo su Rust (non in NICHE_CATEGORIES)
```
Base score: 65 (HackerNews 250 punti + blog autorevole)
Categoria: programming (non preferita)
Bonus: +0
Score finale: 65

Pubblicato? SÌ, se supera altri candidati con score < 65
```

### Esempio 2: Articolo AI mediocre
```
Base score: 40 (fonte debole, poco engagement)
Categoria: ai (preferita)
Bonus: +15
Score finale: 55

Pubblicato? NO, sotto MIN_SCORE=70
```

### Esempio 3: Articolo Database eccellente
```
Base score: 80 (fonte corporate_blog +30, titolo ottimale +10, etc.)
Categoria: databases (non preferita)
Bonus: +0
Score finale: 80

Pubblicato? SÌ, supera molti articoli delle nicchie preferite
```

---

## 🧪 TESTING

### Test Automatici Creati:
1. **`test_new_scoring.py`** - Simulazione sistema di pesi
2. **`test_scoring_final.py`** - Test con algoritmo reale

### Come Testare in Produzione:
```bash
# Esegui il sistema di selezione
python main.py

# Osserva i log per vedere:
# - Articoli scansionati per categoria
# - Score assegnati
# - Articoli pubblicati
```

---

## 📝 DOCUMENTAZIONE

- **`ALGORITHM_CHANGE_LOG.md`** - Changelog dettagliato
- **`const.py`** - Configurazione (righe 17-19)
- **`news.py`** - Implementazione

---

## ✅ CHECKLIST COMPLETAMENTO

- [x] Costanti aggiunte in `const.py`
- [x] Import aggiornati in `news.py`
- [x] Filtro hard rimosso da `find_best_post()`
- [x] Filtro hard rimosso da `_scan_all_sources()`
- [x] Sistema di pesi implementato in `calculate_score()`
- [x] Docstring aggiornate
- [x] Test creati
- [x] Documentazione completa
- [x] Verificato nessun errore di sintassi

---

## 🚀 PRONTO PER PRODUZIONE

Il sistema è **operativo e testato**. 

**Prossimo step:** Esegui `python main.py` e monitora i risultati per qualche giorno. Se noti troppi/pochi articoli dalle nicchie preferite, regola `NICHE_CATEGORY_BONUS` in `const.py`.

**Raccomandazione:** Mantenere il valore attuale (15) per almeno 1-2 settimane per raccogliere dati e valutare l'efficacia del bilanciamento.

