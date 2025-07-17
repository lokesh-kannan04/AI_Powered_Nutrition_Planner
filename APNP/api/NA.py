import requests
import streamlit as st
import os
from dotenv import load_dotenv

# Set page config - must be first Streamlit command
st.set_page_config(
    page_title="Nutrition Facts Explorer",
    page_icon="🥗",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Load API keys securely
load_dotenv()
NUTRITIONIX_API_KEY = os.getenv("NUTRITIONIX_API_KEY", "6a02c7b6d6d16c04d049db34bcd3fd11")
NUTRITIONIX_APP_ID = os.getenv("NUTRITIONIX_APP_ID", "fedc4497")

# USDA Nutrient IDs with proper units
USDA_NUTRIENT_IDS = {
    'calories': {'id': 208, 'unit': ''},
    'protein': {'id': 203, 'unit': 'g'},
    'fat': {'id': 204, 'unit': 'g'},
    'carbs': {'id': 205, 'unit': 'g'},
    'fiber': {'id': 291, 'unit': 'g'},
    'sugar': {'id': 269, 'unit': 'g'},
    'calcium': {'id': 301, 'unit': 'mg'},
    'iron': {'id': 303, 'unit': 'mg'},
    'potassium': {'id': 306, 'unit': 'mg'},
    'sodium': {'id': 307, 'unit': 'mg'},
    'vitamin_a': {'id': 318, 'unit': 'µg'},
    'thiamin_b1': {'id': 404, 'unit': 'mg'},
    'riboflavin_b2': {'id': 405, 'unit': 'mg'},
    'niacin_b3': {'id': 406, 'unit': 'mg'},
    'pantothenic_acid_b5': {'id': 410, 'unit': 'mg'},
    'vitamin_b6': {'id': 415, 'unit': 'mg'},
    'folate_b9': {'id': 417, 'unit': 'µg'},
    'vitamin_b12': {'id': 418, 'unit': 'µg'},
    'vitamin_c': {'id': 401, 'unit': 'mg'},
    'vitamin_d': {'id': 324, 'unit': 'µg'},
    'vitamin_e': {'id': 323, 'unit': 'mg'},
    'vitamin_k': {'id': 430, 'unit': 'µg'},
    'cholesterol': {'id': 601, 'unit': 'mg'},
    'saturated_fat': {'id': 606, 'unit': 'g'},
    'trans_fat': {'id': 605, 'unit': 'g'}
}

def get_nutrition_info(food_item):
    url = "https://trackapi.nutritionix.com/v2/natural/nutrients"
    headers = {
        "x-app-id": NUTRITIONIX_APP_ID,
        "x-app-key": NUTRITIONIX_API_KEY,
        "Content-Type": "application/json"
    }
    body = {"query": food_item}

    try:
        response = requests.post(url, headers=headers, json=body)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"API Error: {str(e)}")
        return None

def format_nutrient_value(value, unit):
    if value is None:
        return f"0{unit}"
    if value == 0:
        return f"0{unit}"
    if value < 0.1:
        return f"{round(value, 3)}{unit}"
    return f"{round(value, 1)}{unit}"

def get_nutrient_data(food_data):
    nutrients = {}
    
    if not food_data or 'foods' not in food_data or not food_data['foods']:
        return nutrients
    
    food = food_data['foods'][0]
    full_nutrients = {n['attr_id']: n['value'] for n in food.get('full_nutrients', [])}
    
    for name, info in USDA_NUTRIENT_IDS.items():
        direct_field = f'nf_{name}'
        value = food.get(direct_field)
        
        if value is None and info['id'] in full_nutrients:
            value = full_nutrients[info['id']]
        
        nutrients[name] = format_nutrient_value(value, info['unit'])
    
    return nutrients

# ========== CSS STYLING ==========
st.markdown("""
<style>
:root {
    --primary: #2E7D32;
    --primary-light: #4CAF50;
    --primary-dark: #1B5E20;
    --secondary: #388E3C;
    --accent: #7CB342;
    --light-bg: #F8F9FA;
    --card-bg: #FFFFFF;
    --text-dark: #212529;
    --text-medium: #495057;
    --text-light: #6C757D;
    --border-radius: 12px;
    --box-shadow: 0 4px 20px rgba(0,0,0,0.08);
    --transition: all 0.3s ease;
}

.main-container {
    max-width: 800px;
    margin: 0 auto;
    padding: 0 16px;
}

.app-header {
    text-align: center;
    margin-bottom: 32px;
    padding-bottom: 16px;
    border-bottom: 1px solid rgba(0,0,0,0.1);
}

.app-title {
    color: var(--primary-dark);
    font-size: 2.2rem;
    font-weight: 700;
    margin-bottom: 8px;
}

.app-subtitle {
    color: var(--text-medium);
    font-size: 1rem;
    font-weight: 400;
}

.stTextInput>div>div>input {
    border: 1px solid #CED4DA !important;
    border-radius: var(--border-radius) !important;
    padding: 12px 16px !important;
    font-size: 1rem !important;
    transition: var(--transition) !important;
}

.stTextInput>div>div>input:focus {
    border-color: var(--primary) !important;
    box-shadow: 0 0 0 2px rgba(46, 125, 50, 0.25) !important;
}

.stButton>button {
    background-color: var(--primary) !important;
    color: white !important;
    border: none !important;
    border-radius: var(--border-radius) !important;
    padding: 12px 24px !important;
    font-weight: 500 !important;
    transition: var(--transition) !important;
    width: 100% !important;
}

.stButton>button:hover {
    background-color: var(--primary-dark) !important;
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(46, 125, 50, 0.2) !important;
}

.nutrition-card {
    background: var(--card-bg);
    border-radius: var(--border-radius);
    padding: 24px;
    box-shadow: var(--box-shadow);
    margin-bottom: 24px;
    border: 1px solid rgba(0,0,0,0.05);
    transition: var(--transition);
}

.header-card {
    background: linear-gradient(135deg, var(--primary), var(--secondary));
    color: white;
    border-radius: var(--border-radius);
    padding: 20px;
    margin-bottom: 24px;
    box-shadow: var(--box-shadow);
}

.header-title {
    font-size: 1.5rem;
    font-weight: 600;
    margin: 0;
}

.header-subtitle {
    font-size: 0.9rem;
    opacity: 0.9;
    margin: 4px 0 0 0;
}

.nutrient-card {
    background: var(--card-bg);
    border-radius: calc(var(--border-radius) - 4px);
    padding: 16px;
    margin: 12px 0;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    border-left: 4px solid var(--primary);
}

.macro-card {
    background: #F0F7F1;
    border-left-color: var(--primary);
}

.micro-card {
    background: #F5F9F6;
    border-left-color: var(--accent);
}

.vitamin-a-card { border-left-color: #FF9E4F; background: #FFF9F2; }
.vitamin-b-card { border-left-color: #4D8FAC; background: #F0F7FA; }
.vitamin-c-card { border-left-color: #FF6B6B; background: #FFF0F0; }
.vitamin-d-card { border-left-color: #FFD166; background: #FFF9E6; }
.vitamin-e-card { border-left-color: #84DCC6; background: #F0FAF7; }
.vitamin-k-card { border-left-color: #A37AFC; background: #F5F0FF; }

.nutrient-label {
    color: var(--primary-dark);
    font-size: 1rem;
    font-weight: 600;
    margin-bottom: 4px;
}

.nutrient-value {
    font-weight: 600;
    color: var(--text-dark);
    font-size: 1.1rem;
}

.sub-item {
    font-size: 0.85rem;
    color: var(--text-medium);
    margin-top: 6px;
}

.section-header {
    font-size: 1.4rem;
    font-weight: 800;
    color: var(--primary-dark);
    margin: 24px 0 12px 0;
    padding-bottom: 8px;
    border-bottom: 2px solid rgba(0,0,0,0.1);
}

.food-image {
    border-radius: var(--border-radius);
    object-fit: cover;
    width: 100%;
    max-height: 180px;
    box-shadow: var(--box-shadow);
}

.calorie-highlight {
    font-size: 2.2rem;
    font-weight: 700;
    color: var(--primary);
    text-align: center;
    margin: 8px 0;
}

.macronutrient-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 16px;
    margin: 20px 0;
}

.vitamin-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
    gap: 12px;
    margin-top: 16px;
}

.app-footer {
    text-align: center;
    margin-top: 40px;
    padding-top: 20px;
    border-top: 1px solid rgba(0,0,0,0.1);
    color: var(--text-light);
    font-size: 0.85rem;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}

.fade-in {
    animation: fadeIn 0.4s ease-out;
}
</style>
""", unsafe_allow_html=True)

# ========== MAIN APP UI ==========
st.markdown("""
<div class="main-container">
    <div class="app-header">
        <h1 class="app-title">🍏 Nutrition Facts Explorer</h1>
        <p class="app-subtitle">Comprehensive nutritional analysis for any food item</p>
    </div>
</div>
""", unsafe_allow_html=True)

# Search bar
search_col, clear_col = st.columns([5, 1])
with search_col:
    food_query = st.text_input(
        "Search for any food:",
        placeholder="e.g., 1 medium apple, 100g chicken breast",
        key="food_search",
        label_visibility="collapsed"
    )
with clear_col:
    if st.button("Clear", use_container_width=True):
        st.session_state.food_search = ""

if food_query:
    with st.spinner('🔍 Analyzing nutrition information...'):
        result = get_nutrition_info(food_query)
    
    if result and 'foods' in result and result['foods']:
        food = result['foods'][0]
        nutrients = get_nutrient_data(result)
        
        # Ensure all vitamin keys exist
        for key in ['vitamin_a', 'thiamin_b1', 'riboflavin_b2', 'niacin_b3', 
                   'pantothenic_acid_b5', 'vitamin_b6', 'folate_b9', 'vitamin_b12',
                   'vitamin_c', 'vitamin_d', 'vitamin_e', 'vitamin_k']:
            if key not in nutrients:
                nutrients[key] = f"0{USDA_NUTRIENT_IDS[key]['unit']}"
        
        # Header card
        st.markdown(f"""
        <div class="header-card fade-in">
            <h2 class="header-title">{food.get('food_name', 'Food').title()}</h2>
            <p class="header-subtitle">
            Serving: {food.get('serving_qty', '')} {food.get('serving_unit', '')} • {food.get('serving_weight_grams', '')}g
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Image and calories
        img_col, cal_col = st.columns([1, 2])
        with img_col:
            st.image(
                food['photo']['thumb'],
                use_container_width=True,
                caption=""
            )
        with cal_col:
            st.markdown(f"""
            <div class="nutrition-card fade-in" style="text-align:center;">
                <h3 style="margin:0 0 8px 0;color:var(--text-medium);">Calories</h3>
                <div class="calorie-highlight">{nutrients['calories']}</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Macronutrients grid
        st.markdown('<div class="section-header fade-in">Macronutrients</div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="macronutrient-grid">
            <div class="nutrient-card macro-card">
                <div class="nutrient-label">Total Fat</div>
                <div class="nutrient-value">{nutrients['fat']}</div>
                <div class="sub-item">Saturated Fat {nutrients['saturated_fat']}</div>
                <div class="sub-item">Trans Fat {nutrients['trans_fat']}</div>
            </div>
        """, unsafe_allow_html=True)
        st.markdown(f"""
            <div class="nutrient-card macro-card">
                <div class="nutrient-label">Carbohydrates</div>
                <div class="nutrient-value">{nutrients['carbs']}</div>
                <div class="sub-item">Fiber {nutrients['fiber']}</div>
                <div class="sub-item">Sugars {nutrients['sugar']}</div>
            </div>
        """, unsafe_allow_html=True)
        st.markdown(f"""
            <div class="nutrient-card macro-card">
                <div class="nutrient-label">Protein</div>
                <div class="nutrient-value">{nutrients['protein']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Other nutrients
        st.markdown(f"""
        <div class="nutrient-card fade-in">
            <div style="display: flex; justify-content: space-between;">
                <div>
                    <div class="nutrient-label">Cholesterol</div>
                    <div class="nutrient-value">{nutrients['cholesterol']}</div>
                </div>
                <div>
                    <div class="nutrient-label">Sodium</div>
                    <div class="nutrient-value">{nutrients['sodium']}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Vitamins & Minerals
        st.markdown('<div class="section-header fade-in">Minerals</div>', unsafe_allow_html=True)
        
        # Minerals
        mcol1, mcol2 = st.columns(2)
        with mcol1:
            st.markdown(f"""
            <div class="nutrient-card micro-card fade-in">
                <div class="nutrient-label">Calcium</div>
                <div class="nutrient-value">{nutrients['calcium']}</div>
            </div>
            """, unsafe_allow_html=True)
        with mcol2:
            st.markdown(f"""
            <div class="nutrient-card micro-card fade-in">
                <div class="nutrient-label">Iron</div>
                <div class="nutrient-value">{nutrients['iron']}</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="nutrient-card micro-card fade-in">
            <div class="nutrient-label">Potassium</div>
            <div class="nutrient-value">{nutrients['potassium']}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Vitamins grid
        st.markdown('<div class="section-header fade-in">Vitamins</div>', unsafe_allow_html=True)
        vitamins_html = f"""
        <div class="vitamin-grid fade-in">
            <div class="nutrient-card vitamin-a-card">
                <div class="nutrient-label">Vitamin A</div>
                <div class="nutrient-value">{nutrients['vitamin_a']}</div>
            </div>
            <div class="nutrient-card vitamin-b-card">
                <div class="nutrient-label">Thiamin (B1)</div>
                <div class="nutrient-value">{nutrients['thiamin_b1']}</div>
            </div>
            <div class="nutrient-card vitamin-b-card">
                <div class="nutrient-label">Riboflavin (B2)</div>
                <div class="nutrient-value">{nutrients['riboflavin_b2']}</div>
            </div>
            <div class="nutrient-card vitamin-b-card">
                <div class="nutrient-label">Niacin (B3)</div>
                <div class="nutrient-value">{nutrients['niacin_b3']}</div>
            </div>
            <div class="nutrient-card vitamin-b-card">
                <div class="nutrient-label">Pantothenic Acid (B5)</div>
                <div class="nutrient-value">{nutrients['pantothenic_acid_b5']}</div>
            </div>
            <div class="nutrient-card vitamin-b-card">
                <div class="nutrient-label">Vitamin B6</div>
                <div class="nutrient-value">{nutrients['vitamin_b6']}</div>
            </div>
            <div class="nutrient-card vitamin-b-card">
                <div class="nutrient-label">Folate (B9)</div>
                <div class="nutrient-value">{nutrients['folate_b9']}</div>
            </div>
            <div class="nutrient-card vitamin-b-card">
                <div class="nutrient-label">Vitamin B12</div>
                <div class="nutrient-value">{nutrients['vitamin_b12']}</div>
            </div>
            <div class="nutrient-card vitamin-c-card">
                <div class="nutrient-label">Vitamin C</div>
                <div class="nutrient-value">{nutrients['vitamin_c']}</div>
            </div>
            <div class="nutrient-card vitamin-d-card">
                <div class="nutrient-label">Vitamin D</div>
                <div class="nutrient-value">{nutrients['vitamin_d']}</div>
            </div>
            <div class="nutrient-card vitamin-e-card">
                <div class="nutrient-label">Vitamin E</div>
                <div class="nutrient-value">{nutrients['vitamin_e']}</div>
            </div>
            <div class="nutrient-card vitamin-k-card">
                <div class="nutrient-label">Vitamin K</div>
                <div class="nutrient-value">{nutrients['vitamin_k']}</div>
            </div>
        </div>
        """
        st.markdown(vitamins_html, unsafe_allow_html=True)
        
        st.caption("* Percent Daily Values are based on a 2,000 calorie diet.")

        # Summary expander
        with st.expander("📊 Quick Nutrition Summary"):
            col1, col2, col3 = st.columns(3)
            col1.metric("Calories", nutrients['calories'])
            col2.metric("Protein", nutrients['protein'])
            col3.metric("Carbs", nutrients['carbs'])
            
            col1, col2 = st.columns(2)
            col1.metric("Total Fat", nutrients['fat'])
            col2.metric("Fiber", nutrients['fiber'])
        
        with st.expander("🔍 View Raw API Data"):
            st.json(food)
    else:
        st.error("No nutrition data found. Please try a different food item or more specific description.")

# Footer
st.markdown("---")
st.markdown("💡 **Pro Tip:** For best results, be specific with quantities and preparation methods")
st.markdown("""
<div class="app-footer">
    Nutrition data provided by Nutritionix API | 🍎 Made with care for health-conscious users
</div>
""", unsafe_allow_html=True)