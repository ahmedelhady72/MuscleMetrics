from django.contrib import admin
from .models import UserProfile, Exercise, WorkoutLog

# تسجيل الجداول عشان تظهر في لوحة الإدارة
admin.site.register(UserProfile)
admin.site.register(Exercise)
admin.site.register(WorkoutLog)