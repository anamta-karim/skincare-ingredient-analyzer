import streamlit as st
import tempfile
import os
from ocr_utils import extract_ingredients
from analysis_utils import analyze_ingredients, calculate_safety_score

# Page config
st.set_page_config(page_title="Skincare Ingredient Analyzer", page_icon="🧴")

# Title
st.title("🧴 Skincare Ingredient Analyzer")
st.write("Upload a product label photo to analyze ingredients based on your skin type.")

# Skin type selection
skin_types = st.multiselect(
    "Select your skin type(s)",
    ["Sensitive", "Dry", "Oily", "Acne-Prone", "Combination", "Eczema"]
)

skin_type = skin_types if skin_types else None

# File upload
uploaded_file = st.file_uploader("Upload product label image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Show the uploaded image
    uploaded_file.seek(0)
    st.image(uploaded_file, caption="Uploaded Label", use_container_width=True)
        
    # Save uploaded file temporarily so EasyOCR can read it
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name
    
    # Run OCR
    with st.spinner("Extracting ingredients from image..."):
        ingredients = extract_ingredients(tmp_path)
    
    # Clean up temp file
    os.unlink(tmp_path)
    
    # Show extracted ingredients in editable text box
    st.subheader("Extracted Ingredients")
    st.write("Review and correct if needed:")
    ingredients_text = st.text_area(
        "Ingredient list",
        value=', '.join(ingredients),
        height=150
    )
    
    # Analyze button
    if st.button("Analyze Ingredients"):
        # Parse the (possibly edited) ingredient list
        final_ingredients = [i.strip().lower() for i in ingredients_text.split(',') if i.strip()]
        
        # Run analysis
        results = analyze_ingredients(final_ingredients, skin_type=skin_type)
        score = calculate_safety_score(results)
        
        # Display safety score
        st.subheader("Safety Analysis")
        if skin_type:
            st.write(f"Analysis for **{', '.join(skin_type)}** skin type")
        
        # Score display
        if score >= 80:
            st.success(f"Safety Score: {score}/100")
        elif score >= 60:
            st.warning(f"Safety Score: {score}/100")
        else:
            st.error(f"Safety Score: {score}/100")
        
        # Stats
        col1, col2, col3 = st.columns(3)
        col1.metric("Safe", results['safe_count'])
        col2.metric("Caution", results['caution_count'])
        col3.metric("Avoid", results['avoid_count'])
        
        # Flagged ingredients
        if results['flagged']:
            st.subheader("⚠️ Flagged Ingredients")
            for item in results['flagged']:
                if item['concern_level'] == 'Avoid':
                    st.error(f"**{item['ingredient_name']}** — {item['explanation']}")
                else:
                    st.warning(f"**{item['ingredient_name']}** — {item['explanation']}")
        else:
            st.success("✓ No flagged ingredients for your skin type.")
        
        # Not found
        if results['not_found']:
            st.subheader("❓ Not Found in Database")
            st.write("These ingredients could not be matched:")
            st.write(', '.join(results['not_found']))