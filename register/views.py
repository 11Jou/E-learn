from django.shortcuts import render ,redirect
from django.urls import reverse
from django.contrib.auth import authenticate , login , logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required , user_passes_test
from .forms import LoginForm , SignUpForm
from .models import Student, Invitation, Instructor
from instructor.models import Course , StudentCourseAccess , Lesson
from django.utils import timezone


@login_required
@user_passes_test(lambda user: user.is_staff and not user.is_superuser)
def generate_link(request):
    superuser = Instructor.objects.get(staffuser = request.user)
    if request.method == "POST":
        expiration_date = request.POST.get('expiration_date')
        expiration_datetime = timezone.datetime.fromisoformat(expiration_date)
        invitation = Invitation(staffuser = superuser , is_used = False, expiration_datetime = expiration_datetime)
        invitation.save()
        current_url = request.build_absolute_uri()
        invitation_link = f"signup/?token={invitation.token}"
        invitation_link = current_url.replace('generate-invitation', invitation_link)
        return render(request, 'invitation_link.html', {'link':invitation_link,'instructor':superuser.name})
    return render(request, 'invitation_link.html' , {'instructor':superuser.name})

#Ahmed1234@

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
    message = {'email':'Email is already exist', 'username':'username is already exist', 'valid':'Enter Valid Data'}
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
    message = 'username or password is incorrect'
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
                return render(request, 'login.html' , {'form':form, 'message': message})
        else:
                return render(request , 'login.html' , {'form':form , 'message': 'Enter Valid Data'})

    return render(request, 'login.html', {'form': form})

@login_required(login_url='login')
def logout_view(request):
    logout(request)
    return redirect('/')
