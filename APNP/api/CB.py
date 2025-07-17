import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai
from datetime import datetime

# Load environment variables
load_dotenv()

# Configure Gemini API
api_key = "AIzaSyD4xXiD1kxQL7Hy4Q1wtfTOjF8vyxgl2tk"
if not api_key:
    st.error("API key not found. Set GOOGLE_API_KEY in your environment variables.")
    st.stop()

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-2.0-flash')

# Custom CSS for the app
st.markdown("""
    <style>
        :root {
            --primary-color: #4285F4;
            --secondary-color: #34A853;
            --accent-color: #EA4335;
            --light-bg: #F8F9FA;
            --dark-text: #202124;
            --light-text: #F8F9FA;
        }
        
        .main-container {
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }
        
        .header {
            text-align: center;
            margin-bottom: 30px;
            border-bottom: 1px solid #e0e0e0;
            padding-bottom: 20px;
        }
        
        .info-box {
            background-color: black;
            border-radius: 8px;
            padding: 16px 20px;
            margin: 12px 0;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
            border-left: 4px solid var(--primary-color);
        }
        
        .response-box {
            background-color: black;
            border-radius: 8px;
            padding: 16px 20px;
            margin: 12px 0;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
            border-left: 4px solid var(--secondary-color);
        }
        
        .message-content {
            font-size: 15px;
            line-height: 1.6;
            color: var(--dark-text);
        }
        
        .nutrition-icon {
            vertical-align: middle;
            margin-right: 8px;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .fade-in {
            animation: fadeIn 0.3s ease-out;
        }
        
        .stTextInput>div>div>input {
            border: 1px solid #DADCE0;
            border-radius: 8px;
            padding: 12px 16px;
            font-size: 15px;
        }
        
        .stButton>button {
            background-color: var(--primary-color);
            color: white;
            border: none;
            border-radius: 8px;
            padding: 12px 24px;
            font-weight: 500;
            transition: all 0.2s;
        }
        
        .stButton>button:hover {
            background-color: #3367D6;
            transform: translateY(-1px);
            box-shadow: 0 2px 8px rgba(66, 133, 244, 0.3);
        }
    </style>
""", unsafe_allow_html=True)

# App Header
st.markdown("""
    <div class="main-container">
        <div class="header">
            <h1 style='color: var(--primary-color); font-size: 32px; font-weight: 600;'>
                <span class="nutrition-icon">🍏</span>NutriGuide AI (Gemini)
            </h1>
            <p style='font-size: 15px; margin-top: 8px;'>
                Powered by Gemini - Expert nutrition analysis and dietary recommendations
            </p>
        </div>
    </div>
""", unsafe_allow_html=True)

# Get user data from query parameters or session state
params = st.query_params

# Extract parameters safely with defaults
user_data = {
    "user_id": params.get("user_id", "Unknown"),
    "email": params.get("email", "Not Provided"),
    "location": params.get("location", "Not Specified"),
    "gender": params.get("gender", "Not Specified"),
    "age": params.get("age", "Unknown"),
    "weight": params.get("weight", "Unknown"),
    "goal": params.get("goal", "Fit"),
    "dietary_preference": params.get("dietary_preference", "None"),
    "medical_conditions": params.get("medical_conditions", "None"),
    "symptoms": params.get("symptoms", "[]"),
    "food_frequency": params.get("food_frequency", "{}"),
    "water_intake": params.get("water_intake", "Unknown"),
    "allergies": params.get("allergies", ""),
    "extra_symptoms": params.get("extra_symptoms", ""),
    "deficiency": params.get("dfc", "")
}

# Goal details mapping
goal_details = {
    "Loss": "weight loss through low-calorie, nutrient-dense foods",
    "Gain": "healthy weight gain through high-calorie, protein-rich foods",
    "Fit": "maintaining fitness through balanced, energy-boosting foods"
}

# User Information Section
with st.container():
    st.markdown("### User Profile")
    with st.expander("View User Details"):
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Gender:** {user_data['gender']}")
            st.write(f"**Age:** {user_data['age']}")
            st.write(f"**Weight:** {user_data['weight']} kg")
            st.write(f"**Goal:** {user_data['goal']}")
        
        with col2:
            st.write(f"**Dietary Preference:** {user_data['dietary_preference']}")
            st.write(f"**Allergies:** {user_data['allergies'] if user_data['allergies'] else 'None'}")
            st.write(f"**Medical Conditions:** {user_data['medical_conditions'] if user_data['medical_conditions'] != 'None' else 'None'}")
            st.write(f"**Potential Deficiency:** {user_data['deficiency']}")
            st.write(f"**Water Intake:** {user_data['water_intake']} liters/day")

# Generate prompt for Gemini
def generate_food_prompt(user_data):
    return f"""
    Act as an expert nutritionist analyzing this user profile:
    
    - Gender: {user_data['gender']}
    - Age: {user_data['age']}
    - Weight: {user_data['weight']} kg
    - Goal: {user_data['goal']} ({goal_details.get(user_data['goal'], 'balanced nutrition')})
    - Dietary Preference: {user_data['dietary_preference']}
    - Medical Conditions: {user_data['medical_conditions']}
    - Symptoms: {user_data['symptoms']}
    - Extra Symptoms: {user_data['extra_symptoms']}
    - Allergies: {user_data['allergies']}
    - Food Frequency: {user_data['food_frequency']}
    - Water Intake: {user_data['water_intake']} liters/day
    - Potential Deficiency: {user_data['deficiency']}
    
    Recommend the top 3 foods that would best address this user's nutritional needs while supporting their goal. 
    For each food, provide:
    1. Food name
    2. Key nutrients it provides
    3. How it helps with the user's specific needs
    4. A simple preparation suggestion
    
    Format your response with clear headings for each food recommendation.
    Ensure all recommendations are safe considering the user's allergies and medical conditions.
    """

def generate_modification_prompt(original_recommendation, modifications, user_data):
    return f"""
    Original recommendations:
    {original_recommendation}
    
    The user has requested these modifications: {modifications}
    
    Please update the food recommendations while considering:
    - User's dietary preference: {user_data['dietary_preference']}
    - Allergies: {user_data['allergies']}
    - Medical conditions: {user_data['medical_conditions']}
    - Original goal: {user_data['goal']}
    
    Maintain the same format but with updated foods that fit the modification request.
    Explain why each modified food is a good choice.
    """

# Initialize session state for recommendations
if 'recommendations' not in st.session_state:
    with st.spinner("Generating personalized nutrition recommendations..."):
        prompt = generate_food_prompt(user_data)
        response = model.generate_content(prompt)
        st.session_state.recommendations = response.text
        st.session_state.original_recommendations = response.text

# Display Recommendations
st.markdown("### Personalized Nutrition Recommendations")
with st.container():
    st.markdown(f'<div class="response-box fade-in">{st.session_state.recommendations}</div>', 
                unsafe_allow_html=True)

# Modification Section
st.markdown("### Customize Recommendations")
modifications = st.text_input(
    "How would you like to modify these recommendations?",
    placeholder="e.g., 'make it vegetarian', 'focus on Indian cuisine', 'more protein options'"
)

col1, col2 = st.columns(2)
with col1:
    if st.button("Apply Changes"):
        if modifications:
            with st.spinner("Updating recommendations..."):
                prompt = generate_modification_prompt(
                    st.session_state.recommendations,
                    modifications,
                    user_data
                )
                response = model.generate_content(prompt)
                st.session_state.recommendations = response.text
                st.rerun()
        else:
            st.warning("Please enter modification instructions")

with col2:
    if st.button("Reset to Original"):
        st.session_state.recommendations = st.session_state.original_recommendations
        st.rerun()

# Additional Features
st.markdown("---")
st.markdown("### Additional Options")

if st.button("Generate Meal Plan"):
    with st.spinner("Creating a 3-day meal plan..."):
        meal_prompt = f"""
        Based on these recommendations:
        {st.session_state.recommendations}
        
        Create a 3-day meal plan for this user with:
        - Breakfast
        - Lunch
        - Dinner
        - 2 snacks
        
        Include portion sizes and preparation notes.
        Ensure it meets the user's {user_data['goal']} goal and dietary needs.
        """
        response = model.generate_content(meal_prompt)
        st.markdown(f'<div class="response-box">{response.text}</div>', 
                    unsafe_allow_html=True)

if st.button("Generate Shopping List"):
    with st.spinner("Creating shopping list..."):
        shopping_prompt = f"""
        Based on these recommendations:
        {st.session_state.recommendations}
        
        Create a categorized shopping list with:
        - Fresh produce
        - Proteins
        - Pantry items
        - Dairy/alternatives
        
        Include quantities for a week's supply.
        """
        response = model.generate_content(shopping_prompt)
        st.markdown(f'<div class="response-box">{response.text}</div>', 
                    unsafe_allow_html=True)