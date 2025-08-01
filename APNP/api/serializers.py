from rest_framework import serializers
from .models import FormData, NutritionAssessment
from django.contrib.auth.hashers import make_password

class FormDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormData
        fields = '__all__'

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])  # Hash the password here
        return super(FormDataSerializer, self).create(validated_data)

class NutritionAssessmentSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)  # Ensure user is assigned internally

    class Meta:
        model = NutritionAssessment
        fields = '__all__'
