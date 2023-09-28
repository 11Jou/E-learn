from django.shortcuts import render ,redirect
from django.contrib.auth.decorators import login_required , user_passes_test
from .models import Message

def index(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        newMessage = Message(name = name, email = email, message=message)
        newMessage.save()
        return redirect('index')
    return render(request, 'index.html')

@login_required
@user_passes_test(lambda user: user.is_superuser)
def view_message(request):
    all_message = Message.objects.all()
    return render(request, 'admin_message.html', {'messages':all_message})