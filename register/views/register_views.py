from django.shortcuts import render ,redirect
from django.contrib.auth import authenticate , login , logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required 
from register.forms import *
from register.models import *
from instructor.models import *
from django.utils import timezone
from core.const import *

def signup_view(request):
    if request.user.is_authenticated:
        logout(request)
    form = SignUpForm()
    token = request.GET.get('token')
    try:
        invitation = Invitation.objects.get(token=token, is_used=False)
        if invitation.is_expired() == True:
            print(invitation.is_expired())
            return render(request, 'error.html', {'is_used':False})
    except:
        return render(request, 'error.html', {'is_used':True})
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data['name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            photo = form.cleaned_data['photo']
            password = form.cleaned_data['password']
            if User.objects.filter(username=username).exists() == True:
                return render(request, 'signup.html',{'form':form, 'message':message['username']})
            elif User.objects.filter(email=email).exists() == True:
                return render(request, 'signup.html',{'form':form, 'message':message['email']})
            else:
                newUser = User.objects.create_user(username, email, password)
                newStudent = Student(user=newUser , name = name, photo=photo, invited_by = invitation.staffuser)
                newUser.save()
                newStudent.save()
                invitation.is_used = True
                invitation.save()
                all_courses = Course.objects.filter(instructor = invitation.staffuser)
                for course in all_courses:
                    course_lessons = Lesson.objects.filter(course = course)
                    for lesson in course_lessons:
                        newAccess = StudentCourseAccess(student = newStudent, lesson=lesson)
                        newAccess.save()
                return redirect('/register/login')
        else:
            print(form.errors)
            return render(request, 'signup.html',{'form':form, 'message':message['valid']})
    return render(request, 'signup.html', {'form':form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('/')
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username , password = password)
            if user:
                login(request, user)
                return redirect("/")
            else:
                return render(request, 'login.html' , {'form':form, 'message': error_message})
        else:
                return render(request , 'login.html' , {'form':form , 'message': 'Enter Valid Data'})
    return render(request, 'login.html', {'form': form})



@login_required(login_url='login')
def logout_view(request):
    logout(request)
    return redirect('/')
