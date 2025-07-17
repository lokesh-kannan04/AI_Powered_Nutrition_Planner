class NutritionCalculator:
    # Activity multipliers
    ACTIVITY_MULTIPLIERS = {
        'sedentary': 1.2,
        'light': 1.375,
        'moderate': 1.55,
        'active': 1.725,
        'very_active': 1.9
    }
    
    # Macronutrient ratios by goal
    MACRO_RATIOS = {
        'gain': {'protein': 0.3, 'fat': 0.25, 'carbs': 0.45},
        'lose': {'protein': 0.35, 'fat': 0.25, 'carbs': 0.4},
        'fit': {'protein': 0.3, 'fat': 0.25, 'carbs': 0.45}
    }
    
    MICRONUTRIENT_DB = {
        "iron": {
            "daily_amount": "18mg/day",
            "monthly_amount": "540mg/month",
            "sources": "spinach,redmeat,lentils",
            "deficiency_symptoms": "fatigue,weakness,paleness"
        },
        "anemia": {
            "daily_amount": "18mg/day",
            "monthly_amount": "540mg/month",
            "sources": "spinach,redmeat,lentils",
            "deficiency_symptoms": "fatigue,weakness,paleness"
        },
        'ironanemia':{
            "daily_amount": "18mg/day",
            "monthly_amount": "540mg/month",
            "sources": "spinach,redmeat,lentils",
            "deficiency_symptoms": "fatigue,weakness,paleness"
        },
        "vitamind": {
            "daily_amount": "600iu/day",
            "monthly_amount": "18000iu/month",
            "sources": "fattyfish,eggvolks,sunlight",
            "deficiency_symptoms": "bonepain,muscleweakness,depression"
        },
        "magnesium": {
            "daily_amount": "400mg/day",
            "monthly_amount": "12000mg/month",
            "sources": "almonds,avocados,wholegrains",
            "deficiency_symptoms": "musclecramps,insomnia,anxiety"
        },
        "vitaminb12": {
            "daily_amount": "2.4mcg/day",
            "monthly_amount": "72mcg/month",
            "sources": "meat,fish,dairy",
            "deficiency_symptoms": "fatigue,tinglinghands,memoryloss"
        },
        "vitaminc": {
            "daily_amount": "90mg/day",
            "monthly_amount": "2700mg/month",
            "sources": "oranges,strawberries,broccoli",
            "deficiency_symptoms": "bleedinggums,slowhealing,dryskin"
        },
        "zinc": {
            "daily_amount": "11mg/day",
            "monthly_amount": "330mg/month",
            "sources": "oysters,beef,pumpkinseeds",
            "deficiency_symptoms": "hairloss,diarrhea,lossoftaste"
        },
        "calcium": {
            "daily_amount": "1000mg/day",
            "monthly_amount": "30000mg/month",
            "sources": "milk,cheese,yogurt",
            "deficiency_symptoms": "osteoporosis,toothdecay,musclespasms"
        },
        "potassium": {
            "daily_amount": "4700mg/day",
            "monthly_amount": "141000mg/month",
            "sources": "bananas,sweetpotatoes,beans",
            "deficiency_symptoms": "musclecramps,irregularheartbeat,constipation"
        },
        "omega3": {
            "daily_amount": "1.6g/day",
            "monthly_amount": "48g/month",
            "sources": "salmon,chia,flaxseeds",
            "deficiency_symptoms": "dryskin,poorconcentration,moodswings"
        },
        "folate": {
            "daily_amount": "400mcg/day",
            "monthly_amount": "12000mcg/month",
            "sources": "leafygreens,beans,avocado",
            "deficiency_symptoms": "fatigue,sores,mouth,anemia"
        },
        "folic": {
            "daily_amount": "400mcg/day",
            "monthly_amount": "12000mcg/month",
            "sources": "leafygreens,beans,avocado",
            "deficiency_symptoms": "fatigue,sores,mouth,anemia"
        },
        "iodine": {
            "daily_amount": "150mcg/day",
            "monthly_amount": "4500mcg/month",
            "sources": "seafood,iodizedsalt,dairy",
            "deficiency_symptoms": "goiter,weightgain,dryskin"
        },
        "selenium": {
            "daily_amount": "55mcg/day",
            "monthly_amount": "1650mcg/month",
            "sources": "brazilnuts,tuna,eggs",
            "deficiency_symptoms": "weakenedimmunity,hairloss,fatigue"
        },
        "vitamina": {
            "daily_amount": "900mcg/day",
            "monthly_amount": "27000mcg/month",
            "sources": "carrots,sweetpotatoes,liver",
            "deficiency_symptoms": "nightblindness,dryeyes,skinissues"
        },
        "vitamine": {
            "daily_amount": "15mg/day",
            "monthly_amount": "450mg/month",
            "sources": "nuts,seeds,vegetableoils",
            "deficiency_symptoms": "muscleweakness,visionproblems,immunityissues"
        },
        "vitamink": {
            "daily_amount": "120mcg/day",
            "monthly_amount": "3600mcg/month",
            "sources": "leafygreens,fermentedfoods,meat",
            "deficiency_symptoms": "easybruising,heavybleeding"
        },
        "copper": {
            "daily_amount": "0.9mg/day",
            "monthly_amount": "27mg/month",
            "sources": "organmeats,shellfish,nuts",
            "deficiency_symptoms": "fatigue,paleness,weakbones"
        },
        "manganese": {
            "daily_amount": "2.3mg/day",
            "monthly_amount": "69mg/month",
            "sources": "wholegrains,nuts,legumes",
            "deficiency_symptoms": "weakbones,skirashes,moodchanges"
        },
        "chromium": {
            "daily_amount": "35mcg/day",
            "monthly_amount": "1050mcg/month",
            "sources": "broccoli,grapejuice,potatoes",
            "deficiency_symptoms": "poorsugarcontrol,increasedhunger"
        },
        "molybdenum": {
            "daily_amount": "45mcg/day",
            "monthly_amount": "1350mcg/month",
            "sources": "legumes,grains,nuts",
            "deficiency_symptoms": "rapidheartrate,headaches"
        },
        "phosphorus": {
            "daily_amount": "700mg/day",
            "monthly_amount": "21000mg/month",
            "sources": "meat,dairy,wholegrains",
            "deficiency_symptoms": "bonepain,jointstiffness,fatigue"
        },
        "biotin": {
            "daily_amount": "30mcg/day",
            "monthly_amount": "900mcg/month",
            "sources": "eggs,almonds,sweetpotatoes",
            "deficiency_symptoms": "hairloss,scalyrash,brittlenails"
        },
        "choline": {
            "daily_amount": "550mg/day",
            "monthly_amount": "16500mg/month",
            "sources": "eggs,beef,soybeans",
            "deficiency_symptoms": "memoryproblems,mooddisorders"
        },
        "vitaminb1": {
            "daily_amount": "1.2mg/day",
            "monthly_amount": "36mg/month",
            "sources": "pork,fish,beans",
            "deficiency_symptoms": "fatigue,irritability,nerveissues"
        },
        "vitaminb2": {
            "daily_amount": "1.3mg/day",
            "monthly_amount": "39mg/month",
            "sources": "mushrooms,almonds,eggs",
            "deficiency_symptoms": "cracksmouth,sorethroat,bloodshoteyes"
        },
        "vitaminb3": {
            "daily_amount": "16mg/day",
            "monthly_amount": "480mg/month",
            "sources": "chicken,tuna,peanuts",
            "deficiency_symptoms": "digestiveissues,skinlesions"
        },
        "vitaminb5": {
            "daily_amount": "5mg/day",
            "monthly_amount": "150mg/month",
            "sources": "avocado,chicken,potatoes",
            "deficiency_symptoms": "fatigue,insomnia,stomachpain"
        },
        "vitaminb6": {
            "daily_amount": "1.7mg/day",
            "monthly_amount": "51mg/month",
            "sources": "chickpeas,salmon,bananas",
            "deficiency_symptoms": "depression,confusion,nausea"
        },
        "fluoride": {
            "daily_amount": "4mg/day",
            "monthly_amount": "120mg/month",
            "sources": "tea,seafood,fluoridatedwater",
            "deficiency_symptoms": "toothdecay,weakbones"
        },
        "boron": {
            "daily_amount": "3mg/day",
            "monthly_amount": "90mg/month",
            "sources": "raisins,almonds,prunes",
            "deficiency_symptoms": "boneloss,arthritis"
        },
        
        "vanadium": {
            "daily_amount": "1.8mg/day",
            "monthly_amount": "54mg/month",
            "sources": "mushrooms,shellfish,dill",
            "deficiency_symptoms": "poorsugarcontrol"
        },
        "nickel": {
            "daily_amount": "0.3mg/day",
            "monthly_amount": "9mg/month",
            "sources": "nuts,beans,oats",
            "deficiency_symptoms": "skirashes,liverissues"
        },
        "silicon": {
            "daily_amount": "25mg/day",
            "monthly_amount": "750mg/month",
            "sources": "bananas,beer,wholegrains",
            "deficiency_symptoms": "weakbones,brittlenails"
        },
        "lithium": {
            "daily_amount": "1mg/day",
            "monthly_amount": "30mg/month",
            "sources": "vegetables,grains,drinkingwater",
            "deficiency_symptoms": "mooddisorders"
        }
    }
    DEFICIENCY_ADJUSTMENT_FACTORS = {
        'iron': 1.8,
        'anemia': 1.8,
        'ironanemia': 1.8,
        'vitamind': 2.0,
        'magnesium': 1.5,
        'vitaminb12': 2.0,
        'vitaminc': 1.5,
        'zinc': 1.5,
        'calcium': 1.2,
        'potassium': 1.3,
        'omega3': 1.5,
        'folate': 1.8,
        'folic': 1.8,
        'iodine': 1.5,
        'selenium': 1.5,
        'vitamina': 1.5,
        'vitamine': 1.5,
        'vitamink': 1.5,
        'copper': 1.5,
        'manganese': 1.5,
        'chromium': 1.5,
        'molybdenum': 1.5,
        'phosphorus': 1.2,
        'biotin': 1.5,
        'choline': 1.5,
        'vitaminb1': 1.5,
        'vitaminb2': 1.5,
        'vitaminb3': 1.5,
        'vitaminb5': 1.5,
        'vitaminb6': 1.5,
        'fluoride': 1.2,
        'boron': 1.5,
        'vanadium': 1.5,
        'nickel': 1.5,
        'silicon': 1.5,
        'lithium': 1.5
    }

    

    def __init__(self):
        self.user_data = None

    def set_user_data(self, gender, age, height, weight, goal, activity, deficiencies):
        """Set user data for calculations"""
        self.user_data = {
            'gender': gender.lower(),
            'age': age,
            'height': height,
            'weight': weight,
            'goal': goal.lower(),
            'activity': activity.lower(),
            'deficiencies': [d.lower() for d in deficiencies]
        }

    def calculate_personalized_adjustment(self, nutrient):
        """Calculate personalized adjustment based on WHO guidelines and user metrics"""
        if not self.user_data:
            raise ValueError("User data not set. Call set_user_data() first.")
            
        # Base adjustment from standard factors
        base_factor = self.DEFICIENCY_ADJUSTMENT_FACTORS.get(nutrient, 1.5)
        personalized_factor = base_factor
        
        # Get user metrics
        weight = self.user_data['weight']
        height = self.user_data['height']
        age = self.user_data['age']
        gender = self.user_data['gender']
        activity = self.user_data['activity']
        goal = self.user_data['goal']
        
        # Calculate body composition metrics
        bmi = weight / ((height/100) ** 2)
        bmr = self.calculate_bmr()
        tdee = self.calculate_tdee(bmr)
        
        # 1. WHO Life Stage Adjustments
        if age < 18:
            # Adolescents need more for growth
            if nutrient in ['calcium', 'vitamind', 'phosphorus']:
                personalized_factor *= 1.2
        elif age > 50:
            # Older adults have different absorption
            if nutrient in ['vitaminb12', 'vitamind', 'calcium']:
                personalized_factor *= 1.3
            if nutrient == 'iron' and gender == 'female':
                personalized_factor *= 0.8  # Post-menopausal women need less iron
        
        # 2. Pregnancy/Lactation (would need additional user data)
        # if self.user_data.get('pregnant'):
        #     if nutrient in ['iron', 'folate', 'iodine']:
        #         personalized_factor *= 1.5
        
        # 3. WHO Activity Level Adjustments
        if activity in ['active', 'very_active']:
            if nutrient in ['magnesium', 'potassium', 'sodium']:
                personalized_factor *= 1.2  # Electrolytes lost through sweat
        
        # 4. WHO Body Composition Guidelines
        if bmi > 30:  # Obesity
            if nutrient in ['vitamind', 'vitamine']:
                personalized_factor *= 1.5  # Fat-soluble vitamins sequestered in adipose tissue
        elif bmi < 18.5:  # Underweight
            if nutrient in ['zinc', 'selenium']:
                personalized_factor *= 1.2
        
        # 5. WHO Special Population Considerations
        if gender == 'female':
            if nutrient == 'iron':
                personalized_factor *= 1.5  # Menstrual losses
            if nutrient == 'calcium' and age > 40:
                personalized_factor *= 1.2  # Bone health
        
        # 6. WHO Dietary Pattern Adjustments
        # (Would need additional user data about diet)
        # if self.user_data.get('vegetarian'):
        #     if nutrient in ['iron', 'vitaminb12', 'zinc']:
        #         personalized_factor *= 1.3  # Lower bioavailability from plant sources
        
        # 7. WHO Health Condition Considerations
        # (Would need additional health data)
        # if self.user_data.get('malabsorption_condition'):
        #     if nutrient in ['fat', 'vitaminadek']:
        #         personalized_factor *= 1.5
        
        # 8. Goal-Specific Adjustments
        if goal == 'gain':
            if nutrient in ['vitaminb6', 'magnesium']:
                personalized_factor *= 1.1  # Needed for protein metabolism
        elif goal == 'lose':
            if nutrient in ['chromium', 'zinc']:
                personalized_factor *= 1.1  # Supports metabolism
        
        # 9. WHO Environmental Factors
        if nutrient == 'vitamind':
            # Latitude-based adjustment (would need location data)
            # if self.user_data.get('latitude') > 40:
            #     personalized_factor *= 1.3
            if activity in ['sedentary', 'light']:
                personalized_factor *= 1.3  # Less sun exposure
        
        # 10. WHO Upper Limits Safety Check
        upper_limits = {
            'vitamina': 2.0,
            'vitamind': 3.0,
            'iron': 2.5,
            'zinc': 2.0,
            'selenium': 2.0
        }
        
        # Apply upper limit if specified
        if nutrient in upper_limits:
            personalized_factor = min(personalized_factor, upper_limits[nutrient])
        
        # Final safety bounds
        return max(1.1, min(personalized_factor, 3.0))

    def calculate_bmr(self):
        """Harris-Benedict Equation"""
        if not self.user_data:
            raise ValueError("User data not set")
            
        w = self.user_data['weight']
        h = self.user_data['height']
        a = self.user_data['age']
        
        if self.user_data['gender'] == 'male':
            return 88.362 + (13.397 * w) + (4.799 * h) - (5.677 * a)
        else:
            return 447.593 + (9.247 * w) + (3.098 * h) - (4.330 * a)
        
    def calculate_tdee(self, bmr=None):
        """Calculate Total Daily Energy Expenditure"""
        if not bmr:
            bmr = self.calculate_bmr()
        return bmr * self.ACTIVITY_MULTIPLIERS.get(self.user_data['activity'], 1.55)

    def calculate_daily_plan(self):
        """Calculate complete daily nutrition plan"""
        if not self.user_data:
            raise ValueError("User data not set")
            
        bmr = self.calculate_bmr()
        tdee = self.calculate_tdee(bmr)
        
        # Calculate calories based on goal
        calorie_adjustment = 500 if self.user_data['goal'] in ['gain', 'lose'] else 0
        calories = tdee + (calorie_adjustment if self.user_data['goal'] == 'gain' else -calorie_adjustment)
        
        # Calculate macros
        ratios = self.MACRO_RATIOS.get(self.user_data['goal'], self.MACRO_RATIOS['fit'])
        protein_g = (calories * ratios['protein']) / 4
        fat_g = (calories * ratios['fat']) / 9
        carbs_g = (calories * ratios['carbs']) / 4
        
        # Calculate micronutrients
        micronutrients = {}
        for d in self.user_data['deficiencies']:
            # Try original name first
            nutrient_key = d
            if nutrient_key not in self.MICRONUTRIENT_DB and nutrient_key.endswith('s'):
                # Try without trailing 's' if not found
                nutrient_key = nutrient_key[:-1]
            
            if nutrient_key in self.MICRONUTRIENT_DB:
                amount, unit = self._parse_amount(self.MICRONUTRIENT_DB[nutrient_key]['daily_amount'])
                adjustment = self.calculate_personalized_adjustment(nutrient_key)
                micronutrients[d] = {  # Keep original deficiency name as key
                    'sa': self.MICRONUTRIENT_DB[nutrient_key]['daily_amount'],
                    'pa': f"{amount * adjustment:.1f}{unit}",
                    'adjustment_factor': round(adjustment, 2),
                    'sources': self.MICRONUTRIENT_DB[nutrient_key]['sources'],
                    'deficiency_symptoms': self.MICRONUTRIENT_DB[nutrient_key]['deficiency_symptoms']
                }
        return {
            'basics': {
                'BMR': round(bmr),
                'TDEE': round(tdee),
                'goal_calories': round(calories),
                'goal': self.user_data['goal']
            },
            'macros': {
                'protein_g': round(protein_g),
                'fat_g': round(fat_g),
                'carbs_g': round(carbs_g),
                'fiber_g': 30 if self.user_data['gender'] == 'male' else 25
            },
            'micronutrients': micronutrients
        }

    def calculate_monthly_plan(self):
        """Convert daily nutrition plan to comprehensive monthly plan with proper unit handling"""
        daily_plan = self.calculate_daily_plan()
        
        def convert_amount(amount_str):
            """Convert any amount string from daily to monthly"""
            try:
                # Handle numeric values directly
                if isinstance(amount_str, (int, float)):
                    return amount_str * 30
                
                # Parse string amounts
                amount, unit = self._parse_amount(amount_str)
                monthly_amount = amount * 30
                
                # Clean up units (handle both "mg" and "mg/day" cases)
                if '/day' in unit:
                    unit = unit.replace('/day', '/month')
                elif not any(x in unit for x in ['/', 'per']):
                    unit = f"{unit}/month"
                    
                return f"{monthly_amount:.1f}{unit}".replace(".0", "")  # Remove .0 for whole numbers
            except (ValueError, AttributeError):
                return amount_str  # Return original if parsing fails
        
        # Convert basics
        monthly_basics = {
            'BMR': {
                'value': daily_plan['basics']['BMR'] * 30,
                'unit': 'kcal/month',
                'original': f"{daily_plan['basics']['BMR']} kcal/day"
            },
            'TDEE': {
                'value': daily_plan['basics']['TDEE'] * 30,
                'unit': 'kcal/month',
                'original': f"{daily_plan['basics']['TDEE']} kcal/day"
            },
            'goal_calories': {
                'value': daily_plan['basics']['goal_calories'] * 30,
                'unit': 'kcal/month',
                'original': f"{daily_plan['basics']['goal_calories']} kcal/day"
            },
            'goal': daily_plan['basics']['goal']
        }
        
        # Convert macros
        monthly_macros = {}
        for macro in ['protein_g', 'fat_g', 'carbs_g', 'fiber_g']:
            daily_value = daily_plan['macros'][macro]
            monthly_macros[macro] = {
                'value': daily_value * 30,
                'unit': 'g/month',
                'original': f"{daily_value}g/day"
            }
        
        # Convert micronutrients with precise parsing
        monthly_micronutrients = {}
        for nutrient, info in daily_plan['micronutrients'].items():
            # Parse standard amount
            sa_amount, sa_unit = self._parse_amount(info['sa'])
            # Parse personalized amount
            pa_amount, pa_unit = self._parse_amount(info['pa'])
            
            monthly_micronutrients[nutrient] = {
                'standard': {
                    'value': sa_amount * 30,
                    'unit': sa_unit.replace('/day', '/month'),
                    'original': info['sa']
                },
                'personalized': {
                    'value': pa_amount * 30,
                    'unit': pa_unit.replace('/day', '/month'),
                    'original': info['pa']
                },
                'adjustment_factor': info['adjustment_factor'],
                'sources': info['sources'],
                'deficiency_symptoms': info['deficiency_symptoms']
            }
        
        return {
            'basics': monthly_basics,
            'macros': monthly_macros,
            'micronutrients': monthly_micronutrients,
            'progress_tracking': self._generate_progress_tracking(),
            'period': 'monthly',
            'conversion_note': 'All values calculated for 30-day month'
        }
    
    def _generate_progress_tracking(self):
        """Generate weight progress tracking plan"""
        current_weight = self.user_data['weight']
        goal = self.user_data['goal']
        
        if goal == 'gain':
            return {
                'target_weight': current_weight + 2,
                'weekly_targets': [current_weight + 0.5 * i for i in range(1, 5)],
                'calorie_adjustment': '+500 kcal/day'
            }
        elif goal == 'lose':
            return {
                'target_weight': current_weight - 2,
                'weekly_targets': [current_weight - 0.5 * i for i in range(1, 5)],
                'calorie_adjustment': '-500 kcal/day'
            }
        else:
            return {
                'target_weight': current_weight,
                'weekly_ranges': [
                    {'min': current_weight - 0.2, 'max': current_weight + 0.2}
                    for _ in range(4)
                ],
                'calorie_adjustment': 'Maintain calories'
            }

    @staticmethod
    def _parse_amount(amount_str):
        """Parse nutrient amount string into value and unit"""
        i = 0
        while i < len(amount_str) and (amount_str[i].isdigit() or amount_str[i] in {'.', '-'}):
            i += 1
        numeric_part = amount_str[:i]
        unit_part = amount_str[i:]
        return float(numeric_part), unit_part


# Example usage
if __name__ == "__main__":
    calculator = NutritionCalculator()
    
    # Set user data
    calculator.set_user_data(
        gender='male',
        age=30,
        height=175,
        weight=70,
        goal='gain',
        activity='moderate',
        deficiencies=['iron', 'vitamind']
    )
    
    # Get monthly plan
    monthly_plan = calculator.calculate_monthly_plan()
    
    # Print results
    print("=== MONTHLY NUTRITION PLAN ===")
    print(f"Goal: {monthly_plan['energy']['goal_calories']['daily']} kcal/day")
    print("\nMacros:")
    for macro, values in monthly_plan['macros'].items():
        print(f"{macro}: {values['daily']}g/day | {values['monthly']}g/month")
    
    print("\nMicronutrients:")
    for nutrient, data in monthly_plan['micronutrients'].items():
        print(f"\n{nutrient}:")
        print(f"Daily: {data['daily']['personalized_amount']}")
        print(f"Monthly: {data['monthly']['amount']}")
        print(f"Sources: {data['monthly']['sources']}")
    
    print("\nProgress Tracking:")
    print(f"Target Weight: {monthly_plan['progress_tracking']['target_weight']}kg")
    if 'weekly_targets' in monthly_plan['progress_tracking']:
        print("Weekly Targets:", monthly_plan['progress_tracking']['weekly_targets'])
    else:
        print("Weekly Ranges:", monthly_plan['progress_tracking']['weekly_ranges'])