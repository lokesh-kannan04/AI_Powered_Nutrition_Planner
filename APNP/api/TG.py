import requests
import streamlit as st
import os
from dotenv import load_dotenv
import logging
from datetime import datetime
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set page config - must be first Streamlit command
st.set_page_config(
    page_title="Nutrition Tracker",
    page_icon="🍏",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Load environment variables
load_dotenv()
st.title("Received Nutritional Data")

# Get all query parameters
data = st.query_params
print(data)
fq = None
if data.fq:
    print(data.fq)
    fq = data.fq
st.title("Query Parameters Received")

def split_value_unit(s):
    """Split numeric value and unit using regex."""
    match = re.match(r"([\d.]+)([a-zA-Z\/]*)", s)
    if match:
        value = float(match.group(1))
        unit = match.group(2) or None
        return value, unit
    return float(s), None  # If no unit, assume numeric

parsed = {
    "calories": {
        "goal": {"value": float(data["goal_calories"]), "unit": "kcal"},
        "taken": {"value": float(data["calories_taken"]), "unit": "kcal"}
    },
    "protein": {
        "goal": dict(zip(["value", "unit"], split_value_unit(data["protein_goal"]))),
        "taken": dict(zip(["value", "unit"], split_value_unit(data["protein_taken"])))
    },
    "fat": {
        "goal": dict(zip(["value", "unit"], split_value_unit(data["fat_goal"]))),
        "taken": dict(zip(["value", "unit"], split_value_unit(data["fat_taken"])))
    },
    "carbs": {
        "goal": dict(zip(["value", "unit"], split_value_unit(data["carbs_goal"]))),
        "taken": dict(zip(["value", "unit"], split_value_unit(data["carbs_taken"])))
    },
    "fiber": {
        "goal": dict(zip(["value", "unit"], split_value_unit(data["fiber_goal"]))),
        "taken": dict(zip(["value", "unit"], split_value_unit(data["fiber_taken"])))
    },
    "micronutrients": []
}

# Handle micronutrients dynamically
for i in range(1, 4):
    name = data[f"micro{i}_name"]
    goal_value, goal_unit = split_value_unit(data[f"micro{i}_goal"])
    taken_value, taken_unit = split_value_unit(data[f"micro{i}_taken"])
    parsed["micronutrients"].append({
        "name": name,
        "goal": {"value": goal_value, "unit": goal_unit},
        "taken": {"value": taken_value, "unit": taken_unit}
    })

# Nutritionix API credentials
NUTRITIONIX_API_KEY = os.getenv("NUTRITIONIX_API_KEY", "6a02c7b6d6d16c04d049db34bcd3fd11")
NUTRITIONIX_APP_ID = os.getenv("NUTRITIONIX_APP_ID", "fedc4497")

# USDA Standard Nutrient IDs with units
USDA_NUTRIENT_IDS = {
    'calories': {'id': 208, 'unit': 'kcal'},
    'protein': {'id': 203, 'unit': 'g'},
    'fat': {'id': 204, 'unit': 'g'},
    'carbs': {'id': 205, 'unit': 'g'},
    'fiber': {'id': 291, 'unit': 'g'},
    'sugar': {'id': 269, 'unit': 'g'},
    'calcium': {'id': 301, 'unit': 'mg'},
    'iron': {'id': 303, 'unit': 'mg'},
    'anemia': {'id': 303, 'unit': 'mg'},
    'ironanemia': {'id': 303, 'unit': 'mg'},
    'magnesium': {'id': 304, 'unit': 'mg'},
    'potassium': {'id': 306, 'unit': 'mg'},
    'sodium': {'id': 307, 'unit': 'mg'},
    'zinc': {'id': 309, 'unit': 'mg'},
    'vitamina': {'id': 318, 'unit': 'µg'},
    'vitaminb1': {'id': 404, 'unit': 'mg'},
    'vitaminb2': {'id': 405, 'unit': 'mg'},
    'vitaminb3': {'id': 406, 'unit': 'mg'},
    'vitaminb5': {'id': 410, 'unit': 'mg'},
    'vitaminb6': {'id': 415, 'unit': 'mg'},
    'vitaminb9': {'id': 417, 'unit': 'µg'},
    'folates': {'id': 417, 'unit': 'µg'},
    'folate': {'id': 417, 'unit': 'µg'},
    'folic': {'id': 417, 'unit': 'µg'},
    'vitaminb12': {'id': 418, 'unit': 'µg'},
    'vitaminc': {'id': 401, 'unit': 'mg'},
    'vitamind': {'id': 324, 'unit': 'µg'},
    'vitamine': {'id': 323, 'unit': 'mg'},
    'vitamink': {'id': 430, 'unit': 'µg'},
    'cholesterol': {'id': 601, 'unit': 'mg'},
    'saturated_fat': {'id': 606, 'unit': 'g'},
    'trans_fat': {'id': 605, 'unit': 'g'}
}

class NutritionalGoal:
    def __init__(self, parsed_data):
        self.data = parsed_data

    def get_goals(self):
        goals = {
            "calories": self.data["calories"]["goal"]["value"],
            "protein": self.data["protein"]["goal"]["value"],
            "fat": self.data["fat"]["goal"]["value"],
            "carbs": self.data["carbs"]["goal"]["value"],
            "fiber": self.data["fiber"]["goal"]["value"]
        }
        for micro in self.data.get("micronutrients", []):
            goals[micro["name"]] = micro["goal"]["value"]
        return goals

    def get_taken(self):
        taken = {
            "calories": self.data["calories"]["taken"]["value"],
            "protein": self.data["protein"]["taken"]["value"],
            "fat": self.data["fat"]["taken"]["value"],
            "carbs": self.data["carbs"]["taken"]["value"],
            "fiber": self.data["fiber"]["taken"]["value"]
        }
        for micro in self.data.get("micronutrients", []):
            taken[micro["name"]] = micro["taken"]["value"]
        return taken
    
    def get_broken(self):
        taken = {
            "calories": 0*self.data["calories"]["taken"]["value"],
            "protein": 0*self.data["protein"]["taken"]["value"],
            "fat": 0*self.data["fat"]["taken"]["value"],
            "carbs": 0*self.data["carbs"]["taken"]["value"],
            "fiber": 0*self.data["fiber"]["taken"]["value"]
        }
        for micro in self.data.get("micronutrients", []):
            taken[micro["name"]] = 0*micro["taken"]["value"]
        return taken

# Initialize nutritional goals
nutrition_goals = NutritionalGoal(parsed)
NUTRITIONAL_GOALS = nutrition_goals.get_goals()

# Initialize session state
if "nutrition_intake" not in st.session_state:
    st.session_state.nutrition_intake = nutrition_goals.get_taken()
if "food_history" not in st.session_state:
    st.session_state.food_history = []
if 'last_update' not in st.session_state:
    st.session_state.last_update = datetime.now()

# Custom CSS for beautiful UI
st.markdown("""
<style>
/* Main card styling */
.nutrition-card {
    background: white;
    border-radius: 16px;
    padding: 24px;
    box-shadow: 0 6px 18px rgba(0,0,0,0.08);
    margin-bottom: 24px;
    border: 1px solid #f0f0f0;
}

/* Header with gradient */
.header-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border-radius: 12px;
    padding: 18px;
    margin-bottom: 20px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

/* Nutrient cards */
.nutrient-card {
    background: #ffffff;
    border-radius: 12px;
    padding: 16px;
    margin: 10px 0;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    border-left: 4px solid #667eea;
    transition: transform 0.2s;
}

.nutrient-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

/* Macronutrient cards */
.macro-card {
    background: #f8faff;
    border-left: 4px solid #667eea;
}

/* Micronutrient cards */
.micro-card {
    background: #f5f7ff;
    border-left: 4px solid #a78bfa;
}

/* Vitamin-specific colors */
.vitamin-a-card { border-left-color: #FF9E4F; background: #FFF5ED; }
.vitamin-b-card { border-left-color: #6DD3CE; background: #EDF9F8; }
.vitamin-c-card { border-left-color: #FF6B6B; background: #FFEEEE; }
.vitamin-d-card { border-left-color: #FFD166; background: #FFF9E6; }
.vitamin-e-card { border-left-color: #84DCC6; background: #EEFAF7; }
.vitamin-k-card { border-left-color: #A37AFC; background: #F4EFFE; }

/* Text styling */
.nutrient-card b {
    color: #4f46e5;
    font-size: 15px;
}

.nutrient-value {
    font-weight: 600;
    color: #4b5563;
}

/* Food image */
.food-image {
    border-radius: 12px;
    object-fit: cover;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

/* Section headers */
.section-header {
    font-size: 18px;
    font-weight: 600;
    color: #374151;
    margin: 20px 0 10px 0;
    padding-bottom: 6px;
    border-bottom: 2px solid #e5e7eb;
}

/* Vitamin grid */
.vitamin-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
    gap: 12px;
    margin-top: 15px;
}

/* History items */
.history-item {
    padding: 12px;
    border-radius: 8px;
    margin-bottom: 8px;
    background: black;
    border-left: 3px solid #6366f1;
    transition: all 0.2s;
}

.history-item:hover {
    background: black;
    transform: translateX(2px);
}

/* Progress bars */
.stProgress > div > div > div {
    background-color: #fff;
}
</style>
""", unsafe_allow_html=True)

def update_django_nutrition(user_id, nutrients):
    """Send nutrition data to Django backend"""
    DJANGO_API_URL = "http://127.0.0.1:8000/api/update-nutrition/"  # Update this
    
    # Prepare the data to match your Django model fields
    update_data = {
        'user_id': user_id,
        'calories_taken': str(st.session_state.nutrition_intake['calories']),
        'protein_taken': f"{st.session_state.nutrition_intake['protein']}g",
        'fat_taken': f"{st.session_state.nutrition_intake['fat']}g",
        'carbs_taken': f"{st.session_state.nutrition_intake['carbs']}g",
        'fiber_taken': f"{st.session_state.nutrition_intake['fiber']}g",
    }
    
    # Add micronutrients
    for i, micro in enumerate(nutrition_goals.data.get("micronutrients", []), start=1):
        name = micro["name"]
        update_data[f"micro{i}_name"] = name
        update_data[f"micro{i}_taken"] = f"{st.session_state.nutrition_intake[name]}{micro['taken']['unit'] or ''}"
    
    try:
        response = requests.post(
            DJANGO_API_URL,
            json=update_data,
            headers={'Content-Type': 'application/json'}
        )
        response.raise_for_status()
        logger.info("Successfully updated Django nutrition data")
        return response
    except Exception as e:
        return None
    
def update_django_nutrition_monthly(user_id, nutrients):
    """Send nutrition data to Django backend"""
    DJANGO_API_URL = "http://127.0.0.1:8000/api/add_monthly_nutrition_intake/"  # Update this
    
    # Prepare the data to match your Django model fields
    update_data = {
        'user_id': user_id,
        'calories_taken': str(st.session_state.nutrition_intake['calories']),
        'protein_taken': f"{st.session_state.nutrition_intake['protein']}g",
        'fat_taken': f"{st.session_state.nutrition_intake['fat']}g",
        'carbs_taken': f"{st.session_state.nutrition_intake['carbs']}g",
        'fiber_taken': f"{st.session_state.nutrition_intake['fiber']}g",
    }
    
    # Add micronutrients
    for i, micro in enumerate(nutrition_goals.data.get("micronutrients", []), start=1):
        name = micro["name"]
        update_data[f"micro{i}_name"] = name
        update_data[f"micro{i}_taken"] = f"{st.session_state.nutrition_intake[name]}{micro['taken']['unit'] or ''}"
    
    try:
        response = requests.post(
            DJANGO_API_URL,
            json=update_data,
            headers={'Content-Type': 'application/json'}
        )
        response.raise_for_status()
        logger.info("Successfully updated Django nutrition data")
        return response
    except Exception as e:
        logger.error(f"Failed to update Django: {str(e)}")
        return None

def get_nutrition_info(food_query):
    """Fetch nutrition data for all food items in the query"""
    url = "https://trackapi.nutritionix.com/v2/natural/nutrients"
    headers = {
        "x-app-id": NUTRITIONIX_APP_ID,
        "x-app-key": NUTRITIONIX_API_KEY,
        "Content-Type": "application/json"
    }
    body = {"query": food_query}

    try:
        response = requests.post(url, headers=headers, json=body)
        response.raise_for_status()
        data = response.json()
        
        # Check if we got multiple foods
        if 'foods' in data and len(data['foods']) > 1:
            return data
        elif 'foods' in data and len(data['foods']) == 1:
            # If only one food returned, try splitting the query and making individual requests
            return handle_multiple_foods_separately(food_query)
        else:
            return None
            
    except Exception as e:
        logger.error(f"API Error: {str(e)}")
        # st.error(f"Failed to fetch nutrition data: {str(e)}")
        return None

def handle_multiple_foods_separately(food_query):
    """Handle cases where combined query doesn't work by splitting foods"""
    # Simple splitting logic - you might want to improve this
    food_items = [item.strip() for item in food_query.split(',') if item.strip()]
    
    combined_data = {'foods': []}
    
    for item in food_items:
        url = "https://trackapi.nutritionix.com/v2/natural/nutrients"
        headers = {
            "x-app-id": NUTRITIONIX_APP_ID,
            "x-app-key": NUTRITIONIX_API_KEY,
            "Content-Type": "application/json"
        }
        body = {"query": item}
        
        try:
            response = requests.post(url, headers=headers, json=body)
            response.raise_for_status()
            item_data = response.json()
            if 'foods' in item_data and item_data['foods']:
                combined_data['foods'].extend(item_data['foods'])
        except Exception as e:
            # logger.error(f"Failed to get data for {item}: {str(e)}")
            continue
    
    return combined_data if combined_data['foods'] else None

def extract_nutrients(food_data):
    """Extract and sum nutrients from all foods in the response"""
    nutrients = {name: 0 for name in USDA_NUTRIENT_IDS}
    
    if not food_data or 'foods' not in food_data or not food_data['foods']:
        return nutrients
    
    # Sum nutrients across all foods
    for food in food_data['foods']:
        # Extract from full_nutrients array first
        full_nutrients = {n['attr_id']: n['value'] for n in food.get('full_nutrients', [])}
        
        for name, info in USDA_NUTRIENT_IDS.items():
            # Check full nutrients first
            if info['id'] in full_nutrients:
                nutrients[name] += full_nutrients[info['id']]
            # Fall back to direct fields
            elif f'nf_{name}' in food:
                nutrients[name] += food[f'nf_{name}']
        
        # Special case for calories which might come from different field
        if 'nf_calories' in food:
            nutrients['calories'] += food['nf_calories']
    
    return nutrients

def format_nutrient_value(value, unit):
    """Format nutrient values properly with correct units"""
    if value is None:
        return f"0{unit}"
    return f"{round(value, 1)}{unit}"

def display_nutrition_card(food_data):
    """Display nutrition card showing all foods and combined nutrients"""
    if not food_data or 'foods' not in food_data or not food_data['foods']:
        st.error("No nutrition data available")
        return
    
    nutrients = extract_nutrients(food_data)
    
    # Main card container
    with st.container():
        # Header with all food names
        food_names = ", ".join([f.get('food_name', 'Food').title() for f in food_data['foods']])
        st.markdown(f"""
        <div class="header-card">
            <h2 style="margin:0;color:white;font-weight:600;">{food_names}</h2>
            <p style="margin:0;opacity:0.9;font-size:14px;">
            Individual nutrition details for each item
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Display each food item with its details
        for food in food_data['foods']:
            with st.expander(f"{food.get('food_name', 'Food').title()} - {format_nutrient_value(food.get('nf_calories', 0), 'kcal')}", expanded=True):
                col1, col2 = st.columns([1, 2])
                
                with col1:
                    # Show food image if available
                    if 'photo' in food and 'thumb' in food['photo']:
                        st.image(
                            food['photo']['thumb'],
                            width=140,
                            use_container_width=False,
                            output_format="JPEG",
                            caption=f"Serving size: {food.get('serving_qty', 'N/A')} {food.get('serving_unit', 'unit')}"
                        )
                    else:
                        st.write(f"Serving size: {food.get('serving_qty', 'N/A')} {food.get('serving_unit', 'unit')}")
                
                with col2:
                    # Display key nutritional information
                    st.markdown(f"""
                    <div style="padding:12px;">
                        <h3 style="margin:0 0 8px 0;color:#4b5563;">Nutrition Facts</h3>
                        <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 8px;">
                            <div style="font-size:16px;">
                                <b>Calories:</b> {format_nutrient_value(food.get('nf_calories', 0), 'kcal')}
                            </div>
                            <div style="font-size:16px;">
                                <b>Protein:</b> {format_nutrient_value(food.get('nf_protein', 0), 'g')}
                            </div>
                            <div style="font-size:16px;">
                                <b>Carbs:</b> {format_nutrient_value(food.get('nf_total_carbohydrate', 0), 'g')}
                            </div>
                            <div style="font-size:16px;">
                                <b>Fat:</b> {format_nutrient_value(food.get('nf_total_fat', 0), 'g')}
                            </div>
                            <div style="font-size:16px;">
                                <b>Sugar:</b> {format_nutrient_value(food.get('nf_sugars', 0), 'g')}
                            </div>
                            <div style="font-size:16px;">
                                <b>Fiber:</b> {format_nutrient_value(food.get('nf_dietary_fiber', 0), 'g')}
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        
        # Macronutrients section
        st.markdown('<div class="section-header">Macronutrients</div>', unsafe_allow_html=True)
        
        # Fat card
        st.markdown(f"""
        <div class="nutrient-card macro-card">
            <b>Total Fat</b> <span class="nutrient-value">{format_nutrient_value(nutrients['fat'], 'g')}</span>
            <div style="margin-top:8px;">
                <span style="font-size:14px;">Saturated Fat {format_nutrient_value(nutrients['saturated_fat'], 'g')}</span> • 
                <span style="font-size:14px;">Trans Fat {format_nutrient_value(nutrients['trans_fat'], 'g')}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Carbs and Protein in columns
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
            <div class="nutrient-card macro-card">
                <b>Carbohydrates</b> <span class="nutrient-value">{format_nutrient_value(nutrients['carbs'], 'g')}</span>
                <div style="margin-top:8px;">
                    <span style="font-size:14px;">Fiber {format_nutrient_value(nutrients['fiber'], 'g')}</span> • 
                    <span style="font-size:14px;">Sugars {format_nutrient_value(nutrients['sugar'], 'g')}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class="nutrient-card macro-card">
                <b>Protein</b> <span class="nutrient-value">{format_nutrient_value(nutrients['protein'], 'g')}</span>
            </div>
            """, unsafe_allow_html=True)
        
        # Other important nutrients
        st.markdown(f"""
        <div class="nutrient-card">
            <b>Cholesterol</b> <span class="nutrient-value">{format_nutrient_value(nutrients['cholesterol'], 'mg')}</span> • 
            <b>Sodium</b> <span class="nutrient-value">{format_nutrient_value(nutrients['sodium'], 'mg')}</span> • 
            <b>Potassium</b> <span class="nutrient-value">{format_nutrient_value(nutrients['potassium'], 'mg')}</span>
        </div>
        """, unsafe_allow_html=True)
        
        # Vitamins & Minerals section
        st.markdown('<div class="section-header">Vitamins & Minerals</div>', unsafe_allow_html=True)
        
        # All Vitamins in a grid layout
        st.markdown("**Vitamins**")
        vitamins_html = f"""
        <div class="vitamin-grid">
            <div class="nutrient-card vitamin-a-card">
                <b>Vitamin A</b> <span class="nutrient-value">{format_nutrient_value(nutrients['vitamina'], 'µg')}</span>
            </div>
            <div class="nutrient-card vitamin-b-card">
                <b>Thiamin (B1)</b> <span class="nutrient-value">{format_nutrient_value(nutrients['vitaminb1'], 'mg')}</span>
            </div>
            <div class="nutrient-card vitamin-b-card">
                <b>Riboflavin (B2)</b> <span class="nutrient-value">{format_nutrient_value(nutrients['vitaminb2'], 'mg')}</span>
            </div>
            <div class="nutrient-card vitamin-b-card">
                <b>Niacin (B3)</b> <span class="nutrient-value">{format_nutrient_value(nutrients['vitaminb3'], 'mg')}</span>
            </div>
            <div class="nutrient-card vitamin-b-card">
                <b>Pantothenic Acid (B5)</b> <span class="nutrient-value">{format_nutrient_value(nutrients['vitaminb5'], 'mg')}</span>
            </div>
            <div class="nutrient-card vitamin-b-card">
                <b>Vitamin B6</b> <span class="nutrient-value">{format_nutrient_value(nutrients['vitaminb6'], 'mg')}</span>
            </div>
            <div class="nutrient-card vitamin-b-card">
                <b>Folate (B9)</b> <span class="nutrient-value">{format_nutrient_value(nutrients['vitaminb9'], 'µg')}</span>
            </div>
            <div class="nutrient-card vitamin-b-card">
                <b>Vitamin B12</b> <span class="nutrient-value">{format_nutrient_value(nutrients['vitaminb12'], 'µg')}</span>
            </div>
            <div class="nutrient-card vitamin-c-card">
                <b>Vitamin C</b> <span class="nutrient-value">{format_nutrient_value(nutrients['vitaminc'], 'mg')}</span>
            </div>
            <div class="nutrient-card vitamin-d-card">
                <b>Vitamin D</b> <span class="nutrient-value">{format_nutrient_value(nutrients['vitamind'], 'µg')}</span>
            </div>
            <div class="nutrient-card vitamin-e-card">
                <b>Vitamin E</b> <span class="nutrient-value">{format_nutrient_value(nutrients['vitamine'], 'mg')}</span>
            </div>
            <div class="nutrient-card vitamin-k-card">
                <b>Vitamin K</b> <span class="nutrient-value">{format_nutrient_value(nutrients['vitamink'], 'µg')}</span>
            </div>
        </div>
        """
        st.markdown(vitamins_html, unsafe_allow_html=True)
        
        # Minerals section
        st.markdown("**Minerals**")
        minerals_col1, minerals_col2 = st.columns(2)
        with minerals_col1:
            st.markdown(f"""
            <div class="nutrient-card micro-card">
                <b>Calcium</b> <span class="nutrient-value">{format_nutrient_value(nutrients['calcium'], 'mg')}</span>
            </div>
            """, unsafe_allow_html=True)
        with minerals_col2:
            st.markdown(f"""
            <div class="nutrient-card micro-card">
                <b>Iron</b> <span class="nutrient-value">{format_nutrient_value(nutrients['iron'], 'mg')}</span>
            </div>
            """, unsafe_allow_html=True)

def update_nutrition_intake(nutrients):
    """Update session state with new nutrition intake"""
    for nutrient in st.session_state.nutrition_intake:
        if nutrient in nutrients:
            st.session_state.nutrition_intake[nutrient] += nutrients[nutrient]

def display_progress_bars():
    """Display progress bars that actually update in real-time"""
    st.subheader("📊 Daily Nutrition Progress")
    
    # Force update by adding a dummy element that changes
    st.session_state.last_update = datetime.now()
    st.write(f"Last updated: {st.session_state.last_update.strftime('%H:%M:%S')}", visible=False)
    
    # Calculate progress for each nutrient (capped at 100%)
    def get_progress(current, goal):
        return min(current / goal, 1.0) if goal > 0 else 0
    
    # Create columns for better layout
    col1, col2 = st.columns(2)
    
    with col1:
        # Macros
        st.write(f"**Calories:** {st.session_state.nutrition_intake['calories']:.0f}/{NUTRITIONAL_GOALS['calories']:.0f} kcal")
        st.progress(get_progress(st.session_state.nutrition_intake['calories'], NUTRITIONAL_GOALS['calories']))
        
        st.write(f"**Protein:** {st.session_state.nutrition_intake['protein']:.1f}/{NUTRITIONAL_GOALS['protein']:.1f} g")
        st.progress(get_progress(st.session_state.nutrition_intake['protein'], NUTRITIONAL_GOALS['protein']))
        
        st.write(f"**Fat:** {st.session_state.nutrition_intake['fat']:.1f}/{NUTRITIONAL_GOALS['fat']:.1f} g")
        st.progress(get_progress(st.session_state.nutrition_intake['fat'], NUTRITIONAL_GOALS['fat']))
        
        st.write(f"**Carbs:** {st.session_state.nutrition_intake['carbs']:.1f}/{NUTRITIONAL_GOALS['carbs']:.1f} g")
        st.progress(get_progress(st.session_state.nutrition_intake['carbs'], NUTRITIONAL_GOALS['carbs']))
    
    with col2:
        # Fiber and Micros
        st.write(f"**Fiber:** {st.session_state.nutrition_intake['fiber']:.1f}/{NUTRITIONAL_GOALS['fiber']:.1f} g")
        st.progress(get_progress(st.session_state.nutrition_intake['fiber'], NUTRITIONAL_GOALS['fiber']))
        
        # Micro 1
        st.write(f"**{nutrition_goals.data["micronutrients"][0]["name"]}:** {st.session_state.nutrition_intake[nutrition_goals.data["micronutrients"][0]["name"]]:.1f}/{NUTRITIONAL_GOALS[nutrition_goals.data["micronutrients"][0]["name"]]:.1f} {USDA_NUTRIENT_IDS[nutrition_goals.data["micronutrients"][0]["name"]]["unit"]}")
        st.progress(get_progress(
            st.session_state.nutrition_intake[nutrition_goals.data["micronutrients"][0]["name"]],
            NUTRITIONAL_GOALS[nutrition_goals.data["micronutrients"][0]["name"]]
        ))

        # Micro 2
        st.write(f"**{nutrition_goals.data["micronutrients"][1]["name"]}:** {st.session_state.nutrition_intake[nutrition_goals.data["micronutrients"][1]["name"]]:.1f}/{NUTRITIONAL_GOALS[nutrition_goals.data["micronutrients"][1]["name"]]:.1f} {USDA_NUTRIENT_IDS[nutrition_goals.data["micronutrients"][1]["name"]]["unit"]}")
        st.progress(get_progress(
            st.session_state.nutrition_intake[nutrition_goals.data["micronutrients"][1]["name"]],
            NUTRITIONAL_GOALS[nutrition_goals.data["micronutrients"][1]["name"]]
        ))

        # Micro 3
        st.write(f"**{nutrition_goals.data["micronutrients"][2]["name"]}:** {st.session_state.nutrition_intake[nutrition_goals.data["micronutrients"][2]["name"]]:.1f}/{NUTRITIONAL_GOALS[nutrition_goals.data["micronutrients"][2]["name"]]:.1f} {USDA_NUTRIENT_IDS[nutrition_goals.data["micronutrients"][2]["name"]]["unit"]}")
        st.progress(get_progress(
            st.session_state.nutrition_intake[nutrition_goals.data["micronutrients"][2]["name"]],
            NUTRITIONAL_GOALS[nutrition_goals.data["micronutrients"][2]["name"]]
        ))

st.title("🍏 Advanced Nutrition Tracker")

# Sidebar for meal tracking
with st.sidebar:
    st.header("Track Your Meal")
    
    # Get query parameters using the current stable API
    query_params = st.query_params
    fq = query_params.get("fq", None)
    
    meal_type = st.selectbox("Meal Type", ["Breakfast", "Lunch", "Dinner", "Snack"])
    st.session_state.food_input_value = fq if fq else ""
    food_query = st.text_input(
        "Enter food items:",
        value=st.session_state.food_input_value,
        placeholder="e.g., 1 medium apple, 100g chicken breast"
    )
    
    # Automatic processing when URL parameter exists
    if fq and not st.session_state.get('auto_processed', False):
        if fq:  # If there's a food query from URL
            with st.spinner('Automatically adding from URL...'):
                food_data = get_nutrition_info(fq)
                if food_data:
                    nutrients = extract_nutrients(food_data)
                    
                    try:
                        update_nutrition_intake(nutrients)
                        st.success("Local nutrient state updated")
                    except Exception as e:
                        st.error(f"Local update failed: {e}")

                    try:
                        user_id = data.user_id
                        daily_res = update_django_nutrition(user_id, nutrients)
                        monthly_res = update_django_nutrition_monthly(user_id, nutrients)
                        
                        # if daily_res:
                        #     st.info(f"Daily update: {daily_res.status_code}")
                        # if monthly_res:
                        #     st.info(f"Monthly update: {monthly_res.status_code}")
                    except Exception as e:
                        st.error(f"Django update failed: {e}")

                    # Add all foods to history
                    for food in food_data['foods']:
                        st.session_state.food_history.append({
                            'meal': meal_type,
                            'food': food.get('food_name', 'Unknown food'),
                            'nutrients': extract_nutrients({'foods': [food]}),
                            'time': datetime.now().strftime("%H:%M")
                        })
                    
                    st.success(f"Automatically added from URL: {fq}")
                    display_nutrition_card(food_data)
                    st.session_state.auto_processed = True  # Mark as processed
                else:
                    None
    
    # Manual processing via button
    if st.button("Add to Daily Intake", use_container_width=True):
        if food_query:
            with st.spinner('Fetching nutrition data...'):
                food_data = get_nutrition_info(food_query)
                if food_data:
                    nutrients = extract_nutrients(food_data)
                    
                    try:
                        update_nutrition_intake(nutrients)
                        # st.success("Local nutrient state updated")
                    except Exception as e:
                        st.error(f"Local update failed: {e}")

                    try:
                        user_id = data.user_id
                        daily_res = update_django_nutrition(user_id, nutrients)
                        monthly_res = update_django_nutrition_monthly(user_id, nutrients)
                        
                        if daily_res:
                            st.info(f"Daily update: {daily_res.status_code}")
                        if monthly_res:
                            st.info(f"Monthly update: {monthly_res.status_code}")
                    except Exception as e:
                        st.error(f"Django update failed: {e}")

                    # Add all foods to history
                    for food in food_data['foods']:
                        st.session_state.food_history.append({
                            'meal': meal_type,
                            'food': food.get('food_name', 'Unknown food'),
                            'nutrients': extract_nutrients({'foods': [food]}),
                            'time': datetime.now().strftime("%H:%M")
                        })
                    
                    st.success("Added to your daily intake!")
                    display_nutrition_card(food_data)
                else:
                    st.error("Couldn't get nutrition data for these foods")
        else:
            st.warning("Please enter food items")
    
    st.markdown("---")
    if st.button("Reset Daily Intake", type="secondary", use_container_width=True):
        st.session_state.nutrition_intake = nutrition_goals.get_broken()
        # st.session_state.food_history = []
        st.session_state.food_input_value = "water"
        st.success("Daily intake reset!")
        try:
            user_id = data.user_id
            nutrients = get_nutrition_info("water")
            daily_res = update_django_nutrition(user_id, nutrients)
            monthly_res = update_django_nutrition_monthly(user_id, nutrients)
            
            if daily_res:
                st.info(f"Daily update: {daily_res.status_code}")
            if monthly_res:
                st.info(f"Monthly update: {monthly_res.status_code}")
        except Exception as e:
            st.error(f"Django update failed: {e}")
        

# Main content area
tab1, tab2 = st.tabs(["📊 Nutrition Dashboard", "📝 Food History"])

with tab1:
    # Display progress bars
    display_progress_bars()
    
    # Display nutrition goals
    with st.expander("⚙️ Your Nutrition Goals", expanded=False):
        goals_col1, goals_col2 = st.columns(2)
        goals_col1.metric("Calories", f"{NUTRITIONAL_GOALS['calories']:.0f} kcal")
        goals_col1.metric("Protein", f"{NUTRITIONAL_GOALS['protein']:.1f} g")
        goals_col1.metric("Fat", f"{NUTRITIONAL_GOALS['fat']:.1f} g")
        goals_col2.metric("Carbs", f"{NUTRITIONAL_GOALS['carbs']:.1f} g")
        goals_col2.metric("Fiber", f"{NUTRITIONAL_GOALS['fiber']:.1f} g")
        goals_col2.metric(nutrition_goals.data["micronutrients"][0]["name"], f"{NUTRITIONAL_GOALS[nutrition_goals.data["micronutrients"][0]["name"]]:.1f} {USDA_NUTRIENT_IDS[nutrition_goals.data["micronutrients"][0]["name"]]["unit"]}")
        goals_col2.metric(nutrition_goals.data["micronutrients"][1]["name"], f"{NUTRITIONAL_GOALS[nutrition_goals.data["micronutrients"][1]["name"]]:.1f} {USDA_NUTRIENT_IDS[nutrition_goals.data["micronutrients"][1]["name"]]["unit"]}")
        goals_col2.metric(nutrition_goals.data["micronutrients"][2]["name"], f"{NUTRITIONAL_GOALS[nutrition_goals.data["micronutrients"][2]["name"]]:.1f} {USDA_NUTRIENT_IDS[nutrition_goals.data["micronutrients"][2]["name"]]["unit"]}")

with tab2:
    if st.session_state.food_history:
        st.subheader("Your Food History Today")
        for i, entry in enumerate(st.session_state.food_history):
            with st.container():
                st.markdown(f"""
                <div class="history-item">
                    <b>{entry['meal']} at {entry['time']}</b>
                    <p style="margin:4px 0;font-size:14px;">{entry['food']}</p>
                    <p style="margin:0;font-size:12px;color:#6b7280;">
                        {entry['nutrients']['calories']:.0f} kcal • 
                        P: {entry['nutrients']['protein']:.1f}g • 
                        F: {entry['nutrients']['fat']:.1f}g • 
                        C: {entry['nutrients']['carbs']:.1f}g
                    </p>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("No food entries yet today")

# Footer
st.markdown("---")
st.caption("Nutrition data provided by Nutritionix API | USDA Standard Nutrient Database")

# Add some whitespace at bottom
st.write("")
st.write("")