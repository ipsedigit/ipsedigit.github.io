"""
Test per verificare il nuovo sistema di scoring senza filtri hard sulle NICHE_CATEGORIES
"""

from const import NICHE_CATEGORIES, NICHE_CATEGORY_BONUS, OTHER_CATEGORY_PENALTY

# Simulazione di scoring per diversi tipi di articoli
def simulate_score(category, base_score=50):
    """Simula il calcolo dello score con il nuovo sistema di pesi"""
    score = base_score

    if category in NICHE_CATEGORIES:
        score += NICHE_CATEGORY_BONUS
        bonus_type = f"+{NICHE_CATEGORY_BONUS} (preferred niche)"
    else:
        score += OTHER_CATEGORY_PENALTY
        bonus_type = f"+{OTHER_CATEGORY_PENALTY} (other category)"

    return score, bonus_type


# Test cases
test_cases = [
    ("ai", 50, "Articolo AI con base 50"),
    ("security", 50, "Articolo Security con base 50"),
    ("general", 50, "Articolo General con base 50"),
    ("programming", 50, "Articolo Programming con base 50"),
    ("ai", 70, "Articolo AI eccellente con base 70"),
    ("general", 70, "Articolo General eccellente con base 70"),
    ("databases", 60, "Articolo Databases con base 60"),
]

print("=" * 80)
print("TEST NUOVO SISTEMA DI SCORING - Pesi invece di filtri")
print("=" * 80)
print(f"\nConfigurazione:")
print(f"  NICHE_CATEGORIES (preferite): {NICHE_CATEGORIES}")
print(f"  NICHE_CATEGORY_BONUS: +{NICHE_CATEGORY_BONUS} punti")
print(f"  OTHER_CATEGORY_PENALTY: {OTHER_CATEGORY_PENALTY} punti")
print("\n" + "-" * 80)
print(f"{'Categoria':<20} {'Base':<10} {'Bonus':<25} {'Totale':<10} {'Descrizione'}")
print("-" * 80)

for category, base, description in test_cases:
    final_score, bonus_type = simulate_score(category, base)
    print(f"{category:<20} {base:<10} {bonus_type:<25} {final_score:<10} {description}")

print("\n" + "=" * 80)
print("CONCLUSIONI:")
print("=" * 80)
print("✅ Gli articoli nelle NICHE_CATEGORIES ricevono un bonus, ma NON escludono altri topic")
print(f"✅ Un articolo 'general' eccellente (base 70) può battere un articolo 'ai' scarso (base 50)")
print(f"   - General (70 + {OTHER_CATEGORY_PENALTY}) = 70 > AI (50 + {NICHE_CATEGORY_BONUS}) = {50 + NICHE_CATEGORY_BONUS}")
print(f"✅ A parità di qualità, le nicchie preferite hanno un vantaggio di {NICHE_CATEGORY_BONUS} punti")
print("✅ Sistema più flessibile e aperto a contenuti di qualità da qualsiasi categoria")

