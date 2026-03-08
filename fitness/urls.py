from django.urls import path
from . import views

urlpatterns = [
    path('', views.input_data, name='input_data'),
    path('choose/', views.choose_workout, name='choose_workout'), # تأكد من وجود الاسم ده
    path('plan/', views.workout_plan, name='workout_plan'),
    path('log/<int:exercise_id>/', views.log_workout, name='log_workout'),
    path('progress/', views.progress_analysis, name='progress_analysis'),
]