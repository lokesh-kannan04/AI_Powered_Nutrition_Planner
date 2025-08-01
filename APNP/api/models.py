from django.db import models

class FormData(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True, unique=True)
    phone = models.CharField(max_length=15, null=True, unique=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], blank=True, null=True)
    height = models.FloatField(blank=True, null=True)
    weight = models.FloatField(blank=True, null=True)
    goal = models.CharField(max_length=10, choices=[('Gain', 'Gain'), ('Lose', 'Lose'), ('Fit', 'Fit')], blank=True, null=True)
    password = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name if self.name else self.email

from django.db import models
from django.core.exceptions import ValidationError

class NutritionAssessment(models.Model):
    user = models.ForeignKey(
        FormData, 
        on_delete=models.CASCADE, 
        related_name="assessments", 
        blank=True, 
        null=True, 
        unique=True  # Ensure each user can have only one assessment
    )
    dietaryPreference = models.CharField(max_length=50)
    medicalConditions = models.TextField(blank=True, null=True)
    symptoms = models.JSONField(default=list)  # Stores symptoms as a list
    foodFrequency = models.JSONField(default=dict)  # Stores food frequency as a dictionary
    waterIntake = models.CharField(max_length=50)
    allergies = models.TextField(blank=True, null=True)
    extra_symptoms = models.TextField(blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Assessment ({self.dietaryPreference}) - {self.submitted_at}"
    
class NutritionalDeficiency(models.Model):
    user = models.OneToOneField(FormData, on_delete=models.CASCADE, related_name="deficiency")
    deficiencies = models.JSONField()
    percentages = models.JSONField()

    def __str__(self):
        return f"Deficiencies for {self.user.phone}"
    
class WhatsAppMessage(models.Model):
    user = models.ForeignKey(FormData, on_delete=models.CASCADE)
    message_text = models.TextField()
    received_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.user.phone}: {self.message_text}"
    
from django.db import models
from django.contrib.auth import get_user_model


class NutritionalGoal(models.Model):
    user = models.OneToOneField(
        FormData, 
        on_delete=models.CASCADE,
        related_name='nutritional_goals',
        unique=True
    )
    
    # --- Macros ---
    goal_calories = models.CharField(max_length=20, default='2520')
    calories_taken = models.CharField(max_length=20, default='0')
    
    protein_goal = models.CharField(max_length=20, default='30g')
    protein_taken = models.CharField(max_length=20, default='0g')
    
    fat_goal = models.CharField(max_length=20, default='75g')
    fat_taken = models.CharField(max_length=20, default='0g')
    
    carbs_goal = models.CharField(max_length=20, default='300g')
    carbs_taken = models.CharField(max_length=20, default='0g')
    
    fiber_goal = models.CharField(max_length=20, default='25g')
    fiber_taken = models.CharField(max_length=20, default='0g')
    
    # --- Micronutrients ---
    micro1_name = models.CharField(max_length=50, default='iron', blank=True)
    micro1_goal = models.CharField(max_length=20, default='20mg/day')
    micro1_taken = models.CharField(max_length=20, default='0')
    
    micro2_name = models.CharField(max_length=50, default='vitaminb12', blank=True)
    micro2_goal = models.CharField(max_length=20, default='2mcg/day')
    micro2_taken = models.CharField(max_length=20, default='0')
    
    micro3_name = models.CharField(max_length=50, default='folate', blank=True)
    micro3_goal = models.CharField(max_length=20, default='400mcg/day')
    micro3_taken = models.CharField(max_length=20, default='0')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Nutrition Goals for {self.user.username}"
    
class MonthlyGoal(models.Model):
    user = models.OneToOneField(
        FormData, 
        on_delete=models.CASCADE,
        related_name='monthly_goals',
        unique=True
    )
    
    # --- Macros ---
    goal_calories = models.CharField(max_length=20, default='75600')
    calories_taken = models.CharField(max_length=20, default='0')
    
    protein_goal = models.CharField(max_length=20, default='900g')
    protein_taken = models.CharField(max_length=20, default='0g')
    
    fat_goal = models.CharField(max_length=20, default='2250g')
    fat_taken = models.CharField(max_length=20, default='0g')
    
    carbs_goal = models.CharField(max_length=20, default='9000g')
    carbs_taken = models.CharField(max_length=20, default='0g')
    
    fiber_goal = models.CharField(max_length=20, default='750g')
    fiber_taken = models.CharField(max_length=20, default='0g')
    
    # --- Micronutrients ---
    micro1_name = models.CharField(max_length=50, default='iron', blank=True)
    micro1_goal = models.CharField(max_length=20, default='600mg/month')
    micro1_taken = models.CharField(max_length=20, default='0')
    
    micro2_name = models.CharField(max_length=50, default='vitaminb12', blank=True)
    micro2_goal = models.CharField(max_length=20, default='60mcg/month')
    micro2_taken = models.CharField(max_length=20, default='0')
    
    micro3_name = models.CharField(max_length=50, default='folate', blank=True)
    micro3_goal = models.CharField(max_length=20, default='12000mcg/month')
    micro3_taken = models.CharField(max_length=20, default='0')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Nutrition Goals for {self.user.username}"
    