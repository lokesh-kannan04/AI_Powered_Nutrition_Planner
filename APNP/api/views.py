from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import FormData, NutritionAssessment
from .serializers import FormDataSerializer, NutritionAssessmentSerializer
from django.http import JsonResponse,  HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from huggingface_hub import InferenceClient
from django.contrib.sessions.models import Session
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.auth.hashers import check_password
from .utils import custom_login_required
from django.shortcuts import get_object_or_404, redirect
import json

@api_view(['POST'])
def submit_form(request):
    """
    Handle form submission and save data to the database.
    """
    if request.method == 'POST':
        serializer = FormDataSerializer(data=request.data)
        print(serializer)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response({"message": "Form data saved successfully!"}, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def form_data_list(request):
    """
    Retrieve a list of all form data entries.
    """
    if request.method == 'GET':
        formdata_list = FormData.objects.all().order_by('-id')
        serializer = FormDataSerializer(formdata_list, many=True)
        # Remove password field from serialized data
        for data in serializer.data:
            data.pop('password', None)
        print(Response(serializer.data, status=status.HTTP_200_OK))
        return Response(serializer.data, status=status.HTTP_200_OK)

from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
import google.generativeai as genai
import streamlit as st
api_key = ""
if not api_key:
    st.error("API key not found. Set GOOGLE_API_KEY in your environment variables.")
    st.stop()

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-2.0-flash')
def generate_response(prompt):
    """
    Generate a response using the Google Gemini API.
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

@api_view(['POST'])
@ensure_csrf_cookie
def generate_response_view(request):
    """
    Django API view to receive symptoms and return predicted deficiencies using Gemini.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            symptoms = data.get('symptoms', '')
            if not symptoms:
                return JsonResponse({'error': 'Symptoms field is required.'}, status=status.HTTP_400_BAD_REQUEST)

            # Refined prompt for structured output
            prompt = (
                f"Given the symptoms: {symptoms}, list the top 3 most likely nutritional deficiencies. "
                "Return the result in JSON format as: "
                "[{\"deficiency\": \"Vitamin D\", \"likelihood\": \"70%\"}, {\"deficiency\": \"Iron\", \"likelihood\": \"60%\"}, ...]"
            )

            response_text = generate_response(prompt)

            # Attempt to parse JSON from Gemini output
            try:
                deficiencies_data = json.loads(response_text)
            except json.JSONDecodeError:
                # Fallback if Gemini returns non-JSON markdown or raw text
                deficiencies = re.findall(r'"?deficiency"?\s*:\s*"([^"]+)"', response_text)
                percentages = re.findall(r'"?likelihood"?\s*:\s*"(\d+%)"', response_text)
                deficiencies_data = [
                    {"deficiency": d, "likelihood": p}
                    for d, p in zip(deficiencies, percentages)
                ]

            return JsonResponse({'deficiencies': deficiencies_data}, status=status.HTTP_200_OK)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data.'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return JsonResponse({'error': 'Invalid request method.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['POST'])
def login_view(request):
    """
    Login view to authenticate users and create session
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            password = data.get('password')
            print("Received username:", email)
            print("Received password:", password)

            if not email or not password:
                return JsonResponse({'error': 'Email and Password are required'}, status=400)

            try:
                user = FormData.objects.get(email=email)
                form_submitted = NutritionAssessment.objects.filter(user=user).exists()
                if check_password(password, user.password):
                    # Start session
                    session = SessionStore()
                    session['user_id'] = user.id
                    session['email'] = user.email
                    session.create()

                    return JsonResponse({
                        'message': 'Login successful!',
                        'session_key': session.session_key,
                        'user': {
                            'id': user.id,
                            'email': user.email,
                            'name': user.name
                        },
                        'form_submitted': form_submitted
                    }, status=200)

                else:
                    return JsonResponse({'error': 'Invalid Password'}, status=401)

            except FormData.DoesNotExist:
                return JsonResponse({'error': 'User not found'}, status=404)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)

# @api_view(['POST'])
@csrf_exempt
def logout_view(request):
    """
    Logout view to destroy the session
    """
    try:
        data = json.loads(request.body)
        session_key = data.get('session_key')

        if not session_key:
            return JsonResponse({'error': 'Session key is required'}, status=400)

        try:
            session = Session.objects.get(session_key=session_key)
            session_data = session.get_decoded()  # Decode session data
            user_id = session_data.get('user_id')

            if user_id:
                user = FormData.objects.get(id=user_id)
                print(f"User Logged out: {user.name}")  # 🔥 This will print the username
            else:
                print("Session does not have user_id")

            session.delete()
            return JsonResponse({'message': 'Logout Successful!'}, status=200)

        except Session.DoesNotExist:
            return JsonResponse({'error': 'Invalid Session Key'}, status=401)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@api_view(['POST'])
def submit_assessment(request):
    print("Inside submit_assessment view")

    # Debugging: Print headers and body
    print("Headers Received:", request.headers)
    print("Body Received:", request.data)

    # Extract session key from headers
    session_key = request.headers.get('Session-Key')  # Check correct header format
    if not session_key:
        return Response({"error": "Session key is required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Retrieve session data
        try:
            session = Session.objects.get(session_key=session_key)
            session_data = session.get_decoded()
            user_id = session_data.get('user_id')  # Ensure your session stores 'user_id'
            print(user_id)
            if not user_id:
                return Response({"error": "Invalid session"}, status=status.HTTP_401_UNAUTHORIZED)

            # Fetch the user (Ensure FormData is correct, or replace with `User`)
            user = FormData.objects.get(id=user_id)

        except Session.DoesNotExist:
            return Response({"error": "Session not found"}, status=status.HTTP_401_UNAUTHORIZED)
        except FormData.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        # Extract nutrition data from request.data
        nutrition_data = request.data.get('nutrition', {})
        if not nutrition_data:
            return Response({"error": "Nutrition data is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Serialize and save assessment data
        serializer = NutritionAssessmentSerializer(data=nutrition_data)
        if serializer.is_valid():
            serializer.save(user=user)  # Attach user before saving
            return Response({"message": "Form submitted successfully!", "data": serializer.data}, status=status.HTTP_201_CREATED)
        print("Serializer Errors:", serializer.errors)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        print(f"Error: {str(e)}")
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@csrf_exempt
def get_current_user(request):
    session_key = request.headers.get('Session-Key')  # Get the session key from headers
    if not session_key:
        return JsonResponse({'status': 'error', 'message': 'Session key is missing'}, status=400)
    print(session_key)
    session = Session.objects.get(session_key=session_key)
    session_data = session.get_decoded()
    user_id = session_data.get('user_id')  # Ensure your session stores 'user_id'
    print(user_id)
    if not user_id:
        return JsonResponse({'status': 'error', 'message': 'User not logged in'}, status=401)

    try:
        user = FormData.objects.get(id=user_id)
        print(user.phone)
        return JsonResponse({
            'status': 'success',
            'user': {
                'name': user.name,
                'email': user.email,
                'phone': user.phone,
                'location': user.location,
                'gender': user.gender,
                'age': user.age,
                'height': user.height,
                'weight': user.weight,
                'goal': user.goal,
            }
        })
    except FormData.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'User not found'}, status=404)
    
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.sessions.models import Session
from .models import NutritionAssessment, FormData

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.sessions.models import Session
from .models import NutritionAssessment, FormData, NutritionalGoal, MonthlyGoal
import json
import re

@csrf_exempt
def get_assessment(request):
    if request.method == 'GET':
        try:
            session_key = request.headers.get('Session-Key')  # Get session_key from headers
            if not session_key:
                return JsonResponse({'error': 'Session key is required.'}, status=400)

            # Fetch the session and user
            session = Session.objects.get(session_key=session_key)
            user_id = session.get_decoded().get('user_id')  # Assuming user_id is stored in the session
            if not user_id:
                return JsonResponse({'error': 'User not found in session.'}, status=404)

            # Fetch the user and their assessment
            user = FormData.objects.get(id=user_id)
            assessment = NutritionAssessment.objects.get(user=user)

            # Combine symptoms and extra_symptoms into a single string
            symptoms_list = assessment.symptoms  # Assuming symptoms is a list
            extra_symptoms = assessment.extra_symptoms  # Assuming extra_symptoms is a string
            if extra_symptoms:
                symptoms_list.append(extra_symptoms)  # Add extra_symptoms to the list
            symptoms = ", ".join(symptoms_list)  # Convert list to a single string

            # Check if deficiencies already exist in the database
            deficiencies_data = generate_response_view_internal(user, symptoms)
            goal = calculate_nutrition_plan(user_id)
            
            print(goal[1])
            def store_raw_data(user, json_data):
                micronutrients = list(json_data['Micronutrients'].items())[:3]  # First 3 micros
                
                print("\n=== Storing Nutrition Data ===")
                print(f"User: {user.id} ({user.phone if hasattr(user, 'phone') else 'No phone'})")
                print("\nMacros:")
                print(f"Calories: {json_data['Goal Calories']}")
                print(f"Protein: {json_data['Macros']['protein_g']}g")
                print(f"Fat: {json_data['Macros']['fat_g']}g")
                print(f"Carbs: {json_data['Macros']['carbs_g']}g")
                print(f"Fiber: {json_data['Macros']['fiber_g']}g")
                
                print("\nMicronutrients:")
                for i, (name, data) in enumerate(micronutrients, 1):
                    print(f"{i}. {name}: {data['pa']} (Personalized: {data['pa']}, Standard: {data['sa']})")

                # Create or update the NutritionalGoal record
                try:
                    nutrition_goal, created = NutritionalGoal.objects.update_or_create(
                        user=user,
                        defaults={
                            # Macros
                            'goal_calories': json_data['Goal Calories'],
                            'protein_goal': f"{json_data['Macros']['protein_g']}g",
                            'fat_goal': f"{json_data['Macros']['fat_g']}g",
                            'carbs_goal': f"{json_data['Macros']['carbs_g']}g",
                            'fiber_goal': f"{json_data['Macros']['fiber_g']}g",
                            
                            # Micronutrients (store up to 3)
                            'micro1_name': micronutrients[0][0] if len(micronutrients) > 0 else "iron",
                            'micro1_goal': micronutrients[0][1]['pa'] if len(micronutrients) > 0 else "18g",
                            
                            'micro2_name': micronutrients[1][0] if len(micronutrients) > 1 else "vitaminb12",
                            'micro2_goal': micronutrients[1][1]['pa'] if len(micronutrients) > 1 else "2mcg",
                            
                            'micro3_name': micronutrients[2][0] if len(micronutrients) > 2 else "folate",
                            'micro3_goal': micronutrients[2][1]['pa'] if len(micronutrients) > 2 else "400mcg",
                        }
                    )
                    
                    print(f"\nSuccessfully {'created' if created else 'updated'} nutritional goals for user {user.id}")
                    return nutrition_goal
                    
                except Exception as e:
                    print(f"\nError saving nutritional goals: {e}")
                    raise  # Re-raise the exception after logging it

            def store_monthly_goals(user, json_data):
                """
                Stores monthly nutrition goals from JSON data into MonthlyGoal model
                """
                try:
                    # Get or create the monthly goals record
                    monthly_goal, created = MonthlyGoal.objects.update_or_create(user=user)
                    
                    # Store basic calorie information
                    monthly_goal.goal_calories = str(json_data['basics']['goal_calories']['value'])
                    
                    # Store macros (converting from monthly to daily values where needed)
                    macros = json_data['macros']
                    monthly_goal.protein_goal = f"{macros['protein_g']['value']}g"
                    
                    monthly_goal.fat_goal = f"{macros['fat_g']['value']}g"
                    
                    monthly_goal.carbs_goal = f"{macros['carbs_g']['value']}g"
                    
                    monthly_goal.fiber_goal = f"{macros['fiber_g']['value']}g"
                    
                    # Store micronutrients (using first 3 from JSON)
                    micros = list(json_data['micronutrients'].items())[:3]
                    
                    if len(micros) > 0:
                        monthly_goal.micro1_name = micros[0][0]
                        monthly_goal.micro1_goal = f"{micros[0][1]['personalized']['value']}{micros[0][1]['personalized']['unit']}"
                    
                    if len(micros) > 1:
                        monthly_goal.micro2_name = micros[1][0]
                        monthly_goal.micro2_goal = f"{micros[1][1]['personalized']['value']}{micros[1][1]['personalized']['unit']}"
                    
                    if len(micros) > 2:
                        monthly_goal.micro3_name = micros[2][0]
                        monthly_goal.micro3_goal = f"{micros[2][1]['personalized']['value']}{micros[2][1]['personalized']['unit']}"
                    print(f"\nSuccessfully {'created' if created else 'updated'} Monthly goals for user {user.id}")
                    
                    monthly_goal.save()
                    return monthly_goal
                
                except KeyError as e:
                    raise ValueError(f"Missing required field in JSON data: {str(e)}")
                except Exception as e:
                    raise Exception(f"Error storing monthly goals: {str(e)}")
                
            store_raw_data(user, goal[0])
            store_monthly_goals(user, goal[1])
            track = NutritionalGoal.objects.get(user=user)
            track_data = {
                'goal_calories': track.goal_calories,
                'calories_taken': track.calories_taken,
                'protein_goal': track.protein_goal,
                'protein_taken': track.protein_taken,
                'fat_goal': track.fat_goal,
                'fat_taken': track.fat_taken,
                'carbs_goal': track.carbs_goal,
                'carbs_taken': track.carbs_taken,
                'fiber_goal': track.fiber_goal,
                'fiber_taken': track.fiber_taken,
                'micro1_name': track.micro1_name,
                'micro1_goal': track.micro1_goal,
                'micro1_taken': track.micro1_taken,
                'micro2_name': track.micro2_name,
                'micro2_goal': track.micro2_goal,
                'micro2_taken': track.micro2_taken,
                'micro3_name': track.micro3_name,
                'micro3_goal': track.micro3_goal,
                'micro3_taken': track.micro3_taken,
            }
            monthly = MonthlyGoal.objects.get(user=user)
            monthly_data = {
                'goal_calories': monthly.goal_calories,
                'calories_taken': monthly.calories_taken,
                'protein_goal': monthly.protein_goal,
                'protein_taken': monthly.protein_taken,
                'fat_goal': monthly.fat_goal,
                'fat_taken': monthly.fat_taken,
                'carbs_goal': monthly.carbs_goal,
                'carbs_taken': monthly.carbs_taken,
                'fiber_goal': monthly.fiber_goal,
                'fiber_taken': monthly.fiber_taken,
                'micro1_name': monthly.micro1_name,
                'micro1_goal': monthly.micro1_goal,
                'micro1_taken': monthly.micro1_taken,
                'micro2_name': monthly.micro2_name,
                'micro2_goal': monthly.micro2_goal,
                'micro2_taken': monthly.micro2_taken,
                'micro3_name': monthly.micro3_name,
                'micro3_goal': monthly.micro3_goal,
                'micro3_taken': monthly.micro3_taken,
            }
            data = {
                'dietaryPreference': assessment.dietaryPreference,
                'medicalConditions': assessment.medicalConditions,
                'symptoms': assessment.symptoms,
                'foodFrequency': assessment.foodFrequency,
                'waterIntake': assessment.waterIntake,
                'allergies': assessment.allergies,
                'extra_symptoms': assessment.extra_symptoms,
                'submitted_at': assessment.submitted_at.strftime('%Y-%m-%d %H:%M:%S'),
                'deficiencies': deficiencies_data.get('deficiencies', [])[:3],
                'percentages': deficiencies_data.get('percentages', [])[:3],
                'goal': goal[0],
                'target': goal[1],
                'nutritional_goals': track_data,
                'monthly_goals': monthly_data
            }
            return JsonResponse(data, status=200)
        except Session.DoesNotExist:
            return JsonResponse({'error': 'Invalid session key.'}, status=404)
        except FormData.DoesNotExist:
            return JsonResponse({'error': 'User not found.'}, status=404)
        except NutritionAssessment.DoesNotExist:
            return JsonResponse({'error': 'No assessment found for this user.'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request method.'}, status=405)

import random
from .models import NutritionalDeficiency, WhatsAppMessage

def generate_response_view_internal(user, symptoms):
    """
    Fetch stored deficiencies if available, else generate and store them.
    """
    try:
        if not symptoms:
            return {'deficiencies': [], 'percentages': []}

        # Check if existing deficiency data is available
        existing_data = NutritionalDeficiency.objects.filter(user=user).first()
        if existing_data:
            print("Already existed", existing_data)
            return {
                'deficiencies': existing_data.deficiencies,
                'percentages': existing_data.percentages
            }

        # Function to extract deficiencies and percentages
        def extract_deficiencies_and_percentages(response):
            deficiencies = re.findall(r"\*\*(.*?)\*\*", response)
            percentages = re.findall(r"(\d+)%", response)

            # Trim percentages if more than deficiencies
            if len(percentages) > len(deficiencies):
                percentages = percentages[:len(deficiencies)]

            # # Return only if the final lists are equal
            # if len(deficiencies) == len(percentages):
            #     return deficiencies, percentages
            # return [], []
            return deficiencies, percentages

        # Generate response
        prompt = (
            f"List the top 3 possible nutritional deficiencies for someone experiencing {symptoms}. "
            "Include only the deficiency name (highlight it in form of **(deficiency name)**) and the % likelihood."
            "Return deficiency and likelihood percentage in form of JSON."
        )

        for attempt in range(4):  # Try up to 4 times
            response = generate_response(prompt if attempt == 0 else f"{prompt} {random_suffix}")
            print(f"Attempt {attempt + 1}: {response}")

            deficiencies, percentages = extract_deficiencies_and_percentages(response)

            if deficiencies and percentages:  # Only store if both lists are valid and equal
                NutritionalDeficiency.objects.create(
                    user=user,
                    deficiencies=deficiencies,
                    percentages=percentages
                )
                return {'deficiencies': deficiencies, 'percentages': percentages}

            # Modify prompt slightly for retry
            random_suffix = ''.join(random.choices("abcdefghijklmnopqrstuvwxyz", k=2))

        return {'deficiencies': [], 'percentages': []}

    except Exception as e:
        print(f"Error generating response: {e}")
        return {'deficiencies': [], 'percentages': []}

def generate_response(prompt):
    """
    Generate a response using Gemini (Google's generative AI).
    """
    try:
        response = model.generate_content(prompt)
        return response.text  # This is the main generated content
    except Exception as e:
        print(f"Gemini generation failed: {e}")
        return ""

from .nutrionix import NutritionCalculator
def calculate_nutrition_plan(user_id):
    """
    Calculate nutrition plan for a user based on their data
    """
    try:
        # Get user data
        user = get_object_or_404(FormData, pk=user_id)
        
        # Get deficiency data if exists
        deficiencies = []
        try:
            deficiency_data = NutritionalDeficiency.objects.get(user=user)
            for deficiency in deficiency_data.deficiencies:
                # Remove content in parentheses and everything after
                deficiency = deficiency.split('/')[0].strip()
                clean_deficiency = deficiency.split('(')[0]
                term = clean_deficiency.lower()
                clean_deficiency = term.replace("deficiency", "")
                term = clean_deficiency.lower()
                clean_deficiency = term.replace("deficiencies", "")
                term = clean_deficiency.lower()
                clean_deficiency = term.replace("acid", "")
                term = clean_deficiency.lower()
                clean_deficiency = term.replace("acids", "")
                # Convert to lowercase and remove non-alphanumeric
                clean_deficiency = ''.join(char.lower() for char in clean_deficiency if char.isalnum())
                if clean_deficiency:
                    deficiencies.append(clean_deficiency)
        except NutritionalDeficiency.DoesNotExist:
            pass
        # print(deficiencies)
        # Prepare calculator input
        calculator_input = {
            'gender': user.gender,
            'age': user.age,
            'height': user.height,
            'weight': user.weight,
            'goal': user.goal,
            'activity': 'moderate',  # Or get from user if available
            'deficiencies': deficiencies
        }
        
        # Initialize calculator with user data
        calculator = NutritionCalculator()
        calculator.set_user_data(**calculator_input)
        
        # Get the daily plan (similar to old calculate_plan)
        daily_plan = calculator.calculate_daily_plan()
        
        # Transform to match old format if needed
        dplan = {
            'BMR': daily_plan['basics']['BMR'],
            'TDEE': daily_plan['basics']['TDEE'],
            'Goal Calories': daily_plan['basics']['goal_calories'],
            'Macros': daily_plan['macros'],
            'Micronutrients': daily_plan['micronutrients']
        }
            
        # Add user info to the plan
        dplan['user_info'] = {
            'name': user.name,
            'email': user.email,
            'phone': user.phone
        }
        
        mplan = calculator.calculate_monthly_plan()
        # Try to get additional assessment data if exists
        try:
            assessment = NutritionAssessment.objects.get(user=user)
            dplan['assessment_info'] = {
                'dietary_preference': assessment.dietaryPreference,
                'medical_conditions': assessment.medicalConditions,
                'allergies': assessment.allergies
            }
        except NutritionAssessment.DoesNotExist:
            pass
        
        return dplan, mplan
    
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    
import urllib.parse
def chatbot_response(request):
    if request.method == 'GET':
        try:
            session_key = request.headers.get('Session-Key')  # Get session key from headers
            if not session_key:
                return JsonResponse({'error': 'Session key is required.'}, status=400)

            # Fetch session and user ID
            session = Session.objects.get(session_key=session_key)
            user_id = session.get_decoded().get('user_id')  # Assuming user_id is stored in the session
            if not user_id:
                return JsonResponse({'error': 'User not found in session.'}, status=404)

            # Fetch the user and their assessment
            user = FormData.objects.get(id=user_id)
            assessment = NutritionAssessment.objects.filter(user=user).first()
            dfc = NutritionalDeficiency.objects.filter(user=user).first()
            if dfc:
                deficiencies = dfc.deficiencies  # This should be a list
                percentages = dfc.percentages  # This should also be a list

                if isinstance(deficiencies, list) and isinstance(percentages, list):
                    for deficiency, percentage in zip(deficiencies, percentages):
                        print(f"{deficiency}: {percentage}%")
                else:
                    print("Invalid data format in deficiencies or percentages.")
            else:
                print("No deficiency data found for the user.")



            if not assessment:
                return JsonResponse({'error': 'No assessment data found for this user'}, status=404)

            # Print user details and nutritional data in Django console
            print("\n=== User Details ===")
            print(f"User ID: {user.id}")
            print(f"Email: {user.email}")
            print(f"Phone: {user.phone}")
            print(f"Location: {user.location}")
            print(f"Gender: {user.gender}")
            print(f"Age: {user.age}")
            print(f"Weight: {user.weight}")
            print(f"Goal: {user.goal}")
            
            print("\n=== Nutrition Assessment ===")
            print(f"Dietary Preference: {assessment.dietaryPreference}")
            print(f"Medical Conditions: {assessment.medicalConditions or 'None'}")
            print(f"Symptoms: {assessment.symptoms}")
            print(f"Food Frequency: {assessment.foodFrequency}")
            print(f"Water Intake: {assessment.waterIntake}")
            print(f"Allergies: {assessment.allergies or 'None'}")
            print(f"Extra Symptoms: {assessment.extra_symptoms or 'None'}")
            print(dfc.deficiencies)
            print(f"Submitted At: {assessment.submitted_at}")

            # Prepare query parameters for Streamlit
            query_params = {
                'user_id': user.id,
                'email': user.email,
                'phone': user.phone,
                'location': user.location,
                'gender': user.gender,
                'age': user.age,
                'weight': user.weight,
                'goal': user.goal,
                'dietary_preference': assessment.dietaryPreference,
                'medical_conditions': assessment.medicalConditions or '',
                'symptoms': assessment.symptoms,
                'food_frequency': assessment.foodFrequency,
                'water_intake': assessment.waterIntake,
                'allergies': assessment.allergies or '',
                'extra_symptoms': assessment.extra_symptoms or '',
                'dfc': dfc.deficiencies,
            }

            encoded_params = urllib.parse.urlencode(query_params)
            streamlit_url = f"http://127.0.0.1:8501/?{encoded_params}"

            # If direct redirect is required
            if request.headers.get('Redirect-Type') == 'direct':
                return HttpResponseRedirect(streamlit_url)

            # Otherwise, send the URL to React for frontend redirection
            return JsonResponse({'redirect_url': streamlit_url})

        except Session.DoesNotExist:
            return JsonResponse({'error': 'Invalid session key.'}, status=400)
        except Exception as e:
            print(e)
            return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def nutritionix_response(request):
    streamlit_url = f"http://127.0.0.1:8502/"

    # If direct redirect is required
    if request.headers.get('Redirect-Type') == 'direct':
        return HttpResponseRedirect(streamlit_url)

    # Otherwise, send the URL to React for frontend redirection
    return JsonResponse({'redirect_url': streamlit_url})

from urllib.parse import urlencode
@csrf_exempt
def tgr(request):
    if request.method == 'GET':
        try:
            session_key = request.headers.get('Session-Key')  # Get session key from headers
            if not session_key:
                return JsonResponse({'error': 'Session key is required.'}, status=400)
            session = Session.objects.get(session_key=session_key)
            session_data = session.get_decoded()
            user_id = session_data.get('user_id')  # or change this based on how you store FormData
            print(session_key)
            user = FormData.objects.get(id=user_id)
            goal = NutritionalGoal.objects.get(user=user)

            # Build the query parameters
            query_params = {
                'user_id' : user_id,
                'fq': 'water',
                'goal_calories': goal.goal_calories,
                'calories_taken': goal.calories_taken,
                'protein_goal': goal.protein_goal,
                'protein_taken': goal.protein_taken,
                'fat_goal': goal.fat_goal,
                'fat_taken': goal.fat_taken,
                'carbs_goal': goal.carbs_goal,
                'carbs_taken': goal.carbs_taken,
                'fiber_goal': goal.fiber_goal,
                'fiber_taken': goal.fiber_taken,
                'micro1_name': goal.micro1_name,
                'micro1_goal': goal.micro1_goal,
                'micro1_taken': goal.micro1_taken,
                'micro2_name': goal.micro2_name,
                'micro2_goal': goal.micro2_goal,
                'micro2_taken': goal.micro2_taken,
                'micro3_name': goal.micro3_name,
                'micro3_goal': goal.micro3_goal,
                'micro3_taken': goal.micro3_taken,
            }

            query_string = urlencode(query_params)
            streamlit_url = f"http://127.0.0.1:8503/?{query_string}"

            if request.headers.get('Redirect-Type') == 'direct':
                return HttpResponseRedirect(streamlit_url)

            # Otherwise, send the URL to React for frontend redirection
            return JsonResponse({'redirect_url': streamlit_url})

        except Session.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Invalid session key'}, status=401)
        except FormData.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'User not found'}, status=404)
        except NutritionalGoal.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'No nutritional goal data found'}, status=404)


from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from urllib.parse import urlencode
from twilio.twiml.messaging_response import MessagingResponse
from django.conf import settings
from twilio.rest import Client

@csrf_exempt
def receive_whatsapp_message(request):
    if request.method == "POST":
        try:
            # Extract WhatsApp data
            from_number = request.POST.get("From", "").replace("whatsapp:", "")
            user_message = request.POST.get("Body", "").strip()
            print(from_number,  user_message)
            # Get or create user
            user, created = FormData.objects.get_or_create(phone=from_number[3:])
            print(user, created)
            
            # Store message
            WhatsAppMessage.objects.create(user=user, message_text=user_message)
            
            # Get nutritional goals
            goal = NutritionalGoal.objects.get(user=user)
            
            # Build query parameters for Streamlit
            query_params = {
                'user_id': user.id,
                'fq': user_message,  # The food items from WhatsApp
                'goal_calories': goal.goal_calories,
                'calories_taken': goal.calories_taken,
                'protein_goal': goal.protein_goal,
                'protein_taken': goal.protein_taken,
                'fat_goal': goal.fat_goal,
                'fat_taken': goal.fat_taken,
                'carbs_goal': goal.carbs_goal,
                'carbs_taken': goal.carbs_taken,
                'fiber_goal': goal.fiber_goal,
                'fiber_taken': goal.fiber_taken,
                'micro1_name': goal.micro1_name,
                'micro1_goal': goal.micro1_goal,
                'micro1_taken': goal.micro1_taken,
                'micro2_name': goal.micro2_name,
                'micro2_goal': goal.micro2_goal,
                'micro2_taken': goal.micro2_taken,
                'micro3_name': goal.micro3_name,
                'micro3_goal': goal.micro3_goal,
                'micro3_taken': goal.micro3_taken,
            }
            
            # Generate Streamlit URL
            query_string = urlencode(query_params)
            streamlit_url = f"http://127.0.0.1:8503/?{query_string}"
            netwrok_url = f"http://192.168.225.33:8503/?{query_string}"
            # Send response to WhatsApp
            response = MessagingResponse()
            
            # Option 1: Send clickable link
            response.message("Your nutrition analysis is ready! Click here:")
            client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
            client.messages.create(
                from_=settings.TWILIO_WHATSAPP_NUMBER,
                to=f"whatsapp:{from_number}",
                body=streamlit_url
            )
            
            # Option 2: Or redirect directly (if you want to open automatically)
            # return HttpResponseRedirect(streamlit_url)
            
        except NutritionalGoal.DoesNotExist:
            # Handle case where user has no goals set
            response = MessagingResponse()
            response.message("Please set your nutritional goals first before tracking meals.")
            return HttpResponse(str(response), content_type="text/xml")
            
        except Exception as e:
            response = MessagingResponse()
            response.message(f"Error processing your request: {str(e)}")
            return HttpResponse(str(response), content_type="text/xml")
    
    return HttpResponse("Invalid request method", status=400)
@csrf_exempt
def update_nutrition_intake(request):
    print("nov")
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_id = data.get('user_id')
            
            # Get the user's nutritional goals
            try:
                goals = NutritionalGoal.objects.get(user_id=user_id)
            except NutritionalGoal.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'User not found'}, status=404)
            
            # Update each field if it exists in the request
            for field in ['calories', 'protein', 'fat', 'carbs', 'fiber']:
                taken_field = f"{field}_taken"
                if taken_field in data:
                    setattr(goals, taken_field, data[taken_field])
            
            # Update micronutrients
            for i in range(1, 4):
                micro_name = f"micro{i}_name"
                if micro_name in data:
                    micro_taken = f"micro{i}_taken"
                    setattr(goals, micro_taken, data[micro_taken])
            
            goals.save()
            return JsonResponse({'status': 'success'})
            
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import MonthlyGoal
import json
import re

def extract_number(val):
    """Extract numeric value from string like '30g' or '200mg'"""
    match = re.search(r'[\d.]+', str(val))
    return float(match.group()) if match else 0.0

@csrf_exempt
def add_monthly_nutrition_intake(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_id = data.get('user_id')

            try:
                goal = MonthlyGoal.objects.get(user_id=user_id)
            except MonthlyGoal.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'User not found'}, status=404)

            # Fields to be updated — these have units in the request, but stored as string
            numeric_fields = [
                'calories_taken',
                'protein_taken',
                'fat_taken',
                'carbs_taken',
                'fiber_taken',
                'micro1_taken',
                'micro2_taken',
                'micro3_taken',
            ]

            for field in numeric_fields:
                if field in data:
                    # Extract numeric part from string (e.g., "30g" → 30.0)
                    new_val = extract_number(data[field])
                    current_val = extract_number(getattr(goal, field, 0))
                    updated_val = current_val + new_val
                    setattr(goal, field, str(updated_val))  # Store back as string

            goal.save()
            return JsonResponse({'status': 'success'})

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)
