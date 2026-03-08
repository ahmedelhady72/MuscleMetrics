from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    # خيارات مستوى النشاط لحساب السعرات
    ACTIVITY_CHOICES = [
        ('sedentary', 'خامل (مكتب)'),
        ('light', 'نشاط خفيف (تمرين 1-3 أيام)'),
        ('moderate', 'نشاط متوسط (تمرين 3-5 أيام)'),
        ('active', 'نشاط عالي (تمرين يومي)'),
    ]
    
    # خيارات النوع
    GENDER_CHOICES = [
        ('M', 'ذكر'),
        ('F', 'أنثى'),
    ]

    # البيانات الأساسية
    age = models.IntegerField(verbose_name="العمر")
    weight = models.FloatField(verbose_name="الوزن (كجم)")
    height = models.FloatField(verbose_name="الطول (سم)")
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='M', verbose_name="النوع")
    activity_level = models.CharField(max_length=20, choices=ACTIVITY_CHOICES, default='moderate', verbose_name="مستوى النشاط")
    
    # تفضيلات التمرين
    workout_location = models.CharField(max_length=50, null=True, blank=True)
    fitness_level = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"بروفايل عمره {self.age}"

class Exercise(models.Model):
    # الخيارات الجديدة للتقسيم
    CATEGORY_CHOICES = [
        ('PUSH', 'Push (صدر، كتف، تراي)'),
        ('PULL', 'Pull (ظهر، باي، ساعد)'),
        ('LEGS', 'Legs (أرجل)'),
        ('CORE', 'Core (بطن وجذع)'),
    ]

    name = models.CharField(max_length=100)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES, default='PUSH') # الحقل الجديد
    image_url = models.URLField(max_length=500, blank=True, null=True)
    location = models.CharField(max_length=10, choices=[('HOME', 'البيت'), ('GYM', 'الجيم')])
    level = models.CharField(max_length=20, choices=[('Beginner', 'مبتدئ'), ('Intermediate', 'متوسط'), ('Advanced', 'متقدم')])
    sets = models.IntegerField()
    reps = models.IntegerField()

    def __str__(self):
        return f"{self.name} ({self.category})"

class WorkoutLog(models.Model):
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    actual_sets = models.IntegerField()
    actual_reps = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.exercise.name} - {self.date.strftime('%Y-%m-%d')}"