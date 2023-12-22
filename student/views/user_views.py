from django.shortcuts import render ,redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required , user_passes_test
from register.models import Student , Instructor




# Create your views here.
@login_required
@user_passes_test(lambda user: user.is_active and not (user.is_superuser or user.is_staff))
def user_profile(request, id):
    current_user = User.objects.get(id=id)
    current_student = Student.objects.get(user = current_user)
    related_instructor = Instructor.objects.get(id=current_student.invited_by.id)
    previous_username = current_user.username ; previous_mail = current_user.email
    if request.method == "POST":
        current_student.name = request.POST.get('name')
        current_user.username = request.POST.get('username')
        current_user.email = request.POST.get('email')
        photo = request.FILES.get('photo')
        if photo:
            current_student.photo = photo
        if User.objects.filter(username = current_user.username).exists() and current_user.username != previous_username or User.objects.filter(email = current_user.email).exists() and current_user.email != previous_mail :
                return render(request, 'user_profile.html', {'student':current_student, 'instructor':related_instructor,
                                                            'message':'Username or Email is already exist'})
        current_student.save()
        current_user.save()
        return redirect('user_profile', id=current_user.id)
    return render(request, 'user_profile.html', {'student':current_student, 'instructor':related_instructor})
