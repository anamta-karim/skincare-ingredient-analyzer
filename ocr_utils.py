import easyocr
import re

reader = easyocr.Reader(['en'])

def extract_ingredients(image_path, confidence_threshold=0.3):
    
    # Step 1: OCR
    result = reader.readtext(image_path)
    lines = []
    for (bbox, text, confidence) in result:
        if confidence > confidence_threshold:
            lines.append(text)
    
    # Step 2: Join and basic cleaning
    raw_text = ' '.join(lines)
    
    ocr_corrections = {
        '1oo': '100',
        '10o': '100',
        '0o': '00',
        'o0': '00',
        '2O': '20',
        '- ': '-',
        '_': '',
    }
    
    for wrong, correct in ocr_corrections.items():
        raw_text = raw_text.replace(wrong, correct)
    
    raw_text = raw_text.replace(';', ',')
    raw_text = raw_text.strip()
    
    # Step 3: Find ingredients section
    raw_lower = raw_text.lower()
    if 'ingredient' in raw_lower:
        start = raw_lower.find('ingredient')
        start = raw_text.find(',', start)
        raw_text = raw_text[start+1:]
    
    # Step 4: Split by comma
    ingredients = raw_text.split(',')
    
    # Step 5: Clean each ingredient
    cleaned = []
    for ingredient in ingredients:
        ingredient = ingredient.strip()
        ingredient = ingredient.strip('.')
        ingredient = re.sub(r'^\d+\s*', '', ingredient)
        ingredient = re.sub(r'\s+', ' ', ingredient).strip()
        ingredient = ingredient.lower()
        if len(ingredient) > 2:
            cleaned.append(ingredient)
    
    # Step 6: Fix full stop merges
    further_cleaned = []
    for ingredient in cleaned:
        if '.' in ingredient:
            parts = ingredient.split('.')
            for part in parts:
                part = part.strip()
                if len(part) > 2:
                    further_cleaned.append(part)
        else:
            further_cleaned.append(ingredient)
    
    # Step 7: Fix ceramide type merges
    final_ingredients = []
    for ingredient in further_cleaned:
        if 'ceramide' in ingredient and ingredient.count('ceramide') > 1:
            parts = re.split(r'(?<!^)(?=ceramide)', ingredient)
            for part in parts:
                part = part.strip()
                if len(part) > 2:
                    final_ingredients.append(part)
        else:
            final_ingredients.append(ingredient)
    
    return final_ingredients