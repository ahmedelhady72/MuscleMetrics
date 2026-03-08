from django.shortcuts import render, redirect, get_object_or_404
from .models import UserProfile, Exercise, WorkoutLog
from .forms import ProfileForm
import json

def input_data(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            profile = form.save()
            request.session['profile_id'] = profile.id
            return redirect('choose_workout')
    else:
        form = ProfileForm()
    return render(request, 'fitness/input.html', {'form': form})

def choose_workout(request):
    profile_id = request.session.get('profile_id')
    if not profile_id:
        return redirect('input_data')
        
    if request.method == 'POST':
        location = request.POST.get('location')
        level = request.POST.get('level')
        profile = get_object_or_404(UserProfile, id=profile_id)
        
        # --- منطق حساب السعرات (Logic) ---
        # BMR = 10*weight + 6.25*height - 5*age + 5 (للذكور)
        bmr = (10 * profile.weight) + (6.25 * profile.height) - (5 * profile.age) + 5
        
        # نضرب في معامل النشاط اللي المستخدم اختاره
        activity_multipliers = {
            'sedentary': 1.2,
            'light': 1.375,
            'moderate': 1.55,
            'active': 1.725
        }
        multiplier = activity_multipliers.get(profile.activity_level, 1.2)
        profile.calories_needed = int(bmr * multiplier) # لازم تضيف الحقل ده في الموديل لو حبيت تحفظه
        
        profile.workout_location = location
        profile.fitness_level = level
        profile.save()
        
        return redirect('workout_plan')
            
    return render(request, 'fitness/choose_workout.html')

def workout_plan(request):
    profile_id = request.session.get('profile_id')
    if not profile_id:
        return redirect('input_data')
        
    profile = get_object_or_404(UserProfile, id=profile_id)
    exercises = Exercise.objects.filter(
        location=profile.workout_location, 
        level=profile.fitness_level
    )
    
    return render(request, 'fitness/workout_plan.html', {
        'exercises': exercises, 
        'profile': profile
    })

def log_workout(request, exercise_id):
    if request.method == 'POST':
        profile_id = request.session.get('profile_id')
        if not profile_id:
            return redirect('input_data')
            
        profile = get_object_or_404(UserProfile, id=profile_id)
        exercise = get_object_or_404(Exercise, id=exercise_id)
        
        # تحويل البيانات لأرقام لضمان السلامة
        try:
            sets = int(request.POST.get('actual_sets', 0))
            reps = int(request.POST.get('actual_reps', 0))
            
            WorkoutLog.objects.create(
                profile=profile,
                exercise=exercise,
                actual_sets=sets,
                actual_reps=reps
            )
        except ValueError:
            pass # ممكن تضيف رسالة خطأ هنا لو حبيت
            
        return redirect('workout_plan')

def progress_analysis(request):
    profile_id = request.session.get('profile_id')
    if not profile_id:
        return redirect('input_data')
        
    profile = get_object_or_404(UserProfile, id=profile_id)
    # ترتيب السجلات بالتاريخ لعرض التطور الزمني
    logs = WorkoutLog.objects.filter(profile=profile).order_by('date')
    
    dates = [log.date.strftime("%Y-%m-%d") for log in logs]
    # الحساب الرياضي: Volume = Sets * Reps
    performance = [log.actual_sets * log.actual_reps for log in logs]
    
    context = {
        'dates_json': json.dumps(dates),
        'performance_json': json.dumps(performance),
        'profile': profile
    }
    
    return render(request, 'fitness/progress.html', context)