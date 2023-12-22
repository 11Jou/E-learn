from django.urls import path
from .views import *


urlpatterns = [
    path('generate-invitation', generate_link, name='generate_invitation'),
    path('login', login_view, name='signin'),
    path('logout', logout_view, name='signout'),
    path('signup/', signup_view, name='registration'),
]