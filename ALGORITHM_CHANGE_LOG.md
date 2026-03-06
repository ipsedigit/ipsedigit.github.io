# Modifica Algoritmo di Selezione - Sistema a Pesi vs Filtri Hard

## Data: 2026-03-06

## Problema Originale
L'algoritmo utilizzava un **filtro hard** che escludeva completamente articoli non appartenenti alle NICHE_CATEGORIES:
```python
if cat not in NICHE_CATEGORIES:
    continue  # ❌ Articolo scartato a priori
```

Questo causava:
- ❌ Esclusione totale di contenuti di qualità da altre categorie
- ❌ Bias eccessivo verso le 5 nicchie (AI, Security, Cloud, DevTools, Software-Engineering)
- ❌ Perdita di potenziali articoli virali su topic emergenti

## Soluzione Implementata
Sostituito il filtro hard con un **sistema di pesi graduati**:

```python
if cat in NICHE_CATEGORIES:
    score += 15  # ✅ Bonus per nicchie preferite
else:
    score += 0   # ✅ Nessuna penalità per altre categorie
```

## Modifiche ai File

### 1. `const.py`
Aggiunte costanti per configurare il sistema di pesi:
```python
NICHE_CATEGORY_BONUS = 15    # Bonus per nicchie preferite
OTHER_CATEGORY_PENALTY = 0   # No penalità per altri topic
```

### 2. `news.py`
- **Rimossi filtri hard** in `find_best_post()` e `_scan_all_sources()`
- **Modificato `calculate_score()`** per usare il bonus graduato
- **Aggiornata documentazione** nelle docstring

## Esempi Pratici

### Scenario 1: Articolo AI vs General a parità di base
- **AI** (base 50): 50 + 15 (bonus) = **65 punti**
- **General** (base 50): 50 + 0 = **50 punti**
- **Vince AI** ✅

### Scenario 2: Articolo General eccellente vs AI medio
- **AI** (base 50): 50 + 15 = **65 punti**
- **General** (base 70): 70 + 0 = **70 punti**
- **Vince General** ✅ (la qualità prevale sul bonus)

### Scenario 3: Articolo Databases molto buono vs AI buono
- **AI** (base 60): 60 + 15 = **75 punti**
- **Databases** (base 60): 60 + 0 = **60 punti**
- **Vince AI** ✅ (il bonus fa la differenza a parità di base)

## Vantaggi

✅ **Flessibilità**: Non esclude a priori contenuti di qualità
✅ **Bilanciamento**: Le nicchie preferite hanno vantaggio, ma non monopolio
✅ **Meritocrazia**: Un articolo eccellente può sempre vincere indipendentemente dalla categoria
✅ **Diversità**: Apre la porta a topic emergenti e trend inaspettati
✅ **Tuning facile**: Il bonus (15 punti) è configurabile in `const.py`

## Impact sul Funzionamento

### Prima (filtro hard):
- 100 articoli scansionati
- 60 scartati perché non in NICHE_CATEGORIES
- 40 candidati rimasti

### Dopo (sistema a pesi):
- 100 articoli scansionati
- 0 scartati per categoria (solo per score < MIN_SCORE)
- ~80-100 candidati (dipende dalla qualità)
- Le nicchie preferite mantengono vantaggio competitivo del +15%

## Configurazione Consigliata

Il valore attuale di **NICHE_CATEGORY_BONUS = 15** è calibrato per:
- Non dominare completamente lo scoring (che va 0-150+)
- Dare vantaggio significativo ma non insormontabile
- Permettere articoli eccellenti di altre categorie di emergere

**Per aumentare il bias verso le nicchie**: aumentare a 20-25
**Per ridurre il bias**: ridurre a 10 o 5
**Per rimuovere completamente il bias**: impostare a 0

## Testing
Eseguire `python test_new_scoring.py` per verificare il comportamento del nuovo sistema.

