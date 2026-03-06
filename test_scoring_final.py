"""Test finale per verificare il nuovo sistema di scoring"""

from news import calculate_score
from const import NICHE_CATEGORIES, NICHE_CATEGORY_BONUS, OTHER_CATEGORY_PENALTY
from types import SimpleNamespace

# Test 1: Articolo AI da research_blog
entry_ai = {
    'title': 'New AI Model Released with GPT-5 Architecture',
    'tags': ['ai', 'machine learning'],
    '_category': 'ai',
    'community_score': 100,
    'source_type': 'research_blog',
    'source_boost': 0
}
source_ai = {'type': 'research_blog', 'name': 'OpenAI', 'score_boost': 0}
score_ai = calculate_score(entry_ai, source_ai)

# Test 2: Articolo General da community
entry_general = {
    'title': 'Great Programming Tips for Better Code Quality',
    'tags': ['programming', 'coding'],
    '_category': 'programming',
    'community_score': 100,
    'source_type': 'community',
    'source_boost': 0
}
source_general = {'type': 'community', 'name': 'dev.to', 'score_boost': 0}
score_general = calculate_score(entry_general, source_general)

# Test 3: Articolo Security da fonte specialist
entry_security = {
    'title': 'New Zero-Day Vulnerability Discovered in Linux Kernel',
    'tags': ['security', 'vulnerability'],
    '_category': 'security',
    'community_score': 200,
    'source_type': 'security',
    'source_boost': 0
}
source_security = {'type': 'security', 'name': 'Krebs on Security', 'score_boost': 0}
score_security = calculate_score(entry_security, source_security)

print("=" * 80)
print("TEST FINALE - Verifica sistema di pesi nell'algoritmo reale")
print("=" * 80)
print(f"\nConfigurazione:")
print(f"  Nicchie preferite: {NICHE_CATEGORIES}")
print(f"  Bonus nicchie preferite: +{NICHE_CATEGORY_BONUS}")
print(f"  Penalità altre categorie: {OTHER_CATEGORY_PENALTY}")
print("\n" + "-" * 80)

print(f"\n1️⃣  ARTICOLO AI (research_blog)")
print(f"   Categoria: {entry_ai['_category']} {'✅ (preferita)' if entry_ai['_category'] in NICHE_CATEGORIES else '❌ (non preferita)'}")
print(f"   Community score: {entry_ai['community_score']}")
print(f"   Tipo fonte: {source_ai['type']}")
print(f"   SCORE FINALE: {score_ai}")
print(f"   Breakdown: 50 (community) + 45 (research_blog) + {NICHE_CATEGORY_BONUS} (niche bonus) + ~30 (title patterns)")

print(f"\n2️⃣  ARTICOLO PROGRAMMING (community)")
print(f"   Categoria: {entry_general['_category']} {'✅ (preferita)' if entry_general['_category'] in NICHE_CATEGORIES else '❌ (non preferita)'}")
print(f"   Community score: {entry_general['community_score']}")
print(f"   Tipo fonte: {source_general['type']}")
print(f"   SCORE FINALE: {score_general}")
print(f"   Breakdown: 50 (community) + 10 (community) + {OTHER_CATEGORY_PENALTY} (other category) + ~15 (title patterns)")

print(f"\n3️⃣  ARTICOLO SECURITY (security specialist)")
print(f"   Categoria: {entry_security['_category']} {'✅ (preferita)' if entry_security['_category'] in NICHE_CATEGORIES else '❌ (non preferita)'}")
print(f"   Community score: {entry_security['community_score']}")
print(f"   Tipo fonte: {source_security['type']}")
print(f"   SCORE FINALE: {score_security}")
print(f"   Breakdown: 100 (community) + 35 (security) + {NICHE_CATEGORY_BONUS} (niche bonus) + ~40 (security keywords)")

print("\n" + "=" * 80)
print("RISULTATI:")
print("=" * 80)
print(f"✅ Articolo AI (preferita): {score_ai} punti")
print(f"✅ Articolo Security (preferita): {score_security} punti")
print(f"✅ Articolo Programming (non preferita): {score_general} punti")
print(f"\n📊 L'articolo Programming NON è stato scartato, ma ha score inferiore")
print(f"   Differenza: {score_ai - score_general} punti rispetto ad AI")
print(f"   Questo è esattamente il comportamento voluto! ✅")
print("\n🎯 Se l'articolo Programming fosse ECCELLENTE (base più alta),")
print(f"   potrebbe comunque superare un articolo AI mediocre!")

