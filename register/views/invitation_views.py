from django.shortcuts import render
from django.contrib.auth.decorators import login_required , user_passes_test
from register.models import *



@login_required
@user_passes_test(lambda user: user.is_staff and not user.is_superuser)
def generate_link(request):
    superuser = Instructor.objects.filter(staffuser = request.user)
    if superuser:
        superuser = Instructor.objects.get(staffuser = request.user)
    else:
        superuser = Assistant.objects.get(user = request.user).related_instructor
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