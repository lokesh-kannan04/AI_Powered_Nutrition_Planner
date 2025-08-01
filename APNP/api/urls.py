from django.urls import path
from .views import submit_form, form_data_list, generate_response_view, login_view, logout_view, submit_assessment, get_current_user, get_assessment, chatbot_response, nutritionix_response, tgr, update_nutrition_intake, add_monthly_nutrition_intake, receive_whatsapp_message

urlpatterns = [
    path('submit_form/', submit_form, name='submit_form'),  # Form Submit API
    path('form-list/', form_data_list, name='formdata_list'),  # API for Table Content
    path('generate-response/', generate_response_view, name='generate_response'),
    path('login/', login_view, name='login_view'),  # Login API Route
    path('logout/', logout_view, name='logout_view'),
    path('submit_assessment/', submit_assessment, name='submit_assessment'),
    path('get_current_user/', get_current_user, name='get_current_user'),
    path('get-assessment/', get_assessment, name='get_assessment'),
    path("chatbot/", chatbot_response, name="chatbot_response"),
    path("nutritionix/", nutritionix_response, name="nutrionix_response"),
    path("tgr/", tgr, name="tgr"),
    path('update-nutrition/', update_nutrition_intake, name='update_nutrition'),
    path('add_monthly_nutrition_intake/', add_monthly_nutrition_intake, name='add_monthly_nutrition_intake'),
    path("webhook/", receive_whatsapp_message, name="whatsapp_webhook"),
]
