import pandas as pd
from rapidfuzz import process, fuzz

# Load database
db = pd.read_csv('data/ingredients_database.csv', encoding='latin-1')

# Build search index
search_terms = []
for idx, row in db.iterrows():
    search_terms.append((row['ingredient_name'].lower().strip(), idx))
    if pd.notna(row['common_aliases']):
        for alias in row['common_aliases'].split(','):
            alias = alias.lower().strip()
            if alias:
                search_terms.append((alias, idx))

terms_only = [term for term, idx in search_terms]


def match_ingredient(ingredient, threshold=80):
    result = process.extractOne(ingredient, terms_only, scorer=fuzz.token_sort_ratio)
    if result is None:
        return None
    matched_term, score, term_index = result
    if score < threshold:
        return None
    db_index = search_terms[term_index][1]
    return db.iloc[db_index].to_dict()


def analyze_ingredients(ingredient_list, skin_type=None):
    results = {
        'matched': [],
        'not_found': [],
        'flagged': [],
        'safe_count': 0,
        'caution_count': 0,
        'avoid_count': 0
    }
    
    for ingredient in ingredient_list:
        match = match_ingredient(ingredient)
        if match is None:
            results['not_found'].append(ingredient)
            continue
        results['matched'].append(match)
        if match['concern_level'] == 'Safe':
            results['safe_count'] += 1
        elif match['concern_level'] == 'Caution':
            results['caution_count'] += 1
        elif match['concern_level'] == 'Avoid':
            results['avoid_count'] += 1
        if match['concern_level'] in ['Caution', 'Avoid']:
            if skin_type:
                skin_types_to_avoid = str(match['skin_types_to_avoid']).lower()
                if any(s.lower() in skin_types_to_avoid for s in skin_type):
                    results['flagged'].append(match)
            else:
                results['flagged'].append(match)
    
    return results

def calculate_safety_score(results):
    total = len(results['matched'])
    if total == 0:
        return 0
    avoid_count = sum(1 for item in results['flagged'] if item['concern_level'] == 'Avoid')
    caution_count = sum(1 for item in results['flagged'] if item['concern_level'] == 'Caution')
    deductions = (avoid_count * 10) + (caution_count * 3)
    return max(0, 100 - deductions)