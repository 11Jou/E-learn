from django.urls import path
from . import views

urlpatterns = [
    path('generate-invitation', views.generate_link, name='generate_invitation'),
    path('login', views.login_view, name='signin'),
    path('logout', views.logout_view, name='signout'),
    path('signup/', views.signup_view, name='registration'),
]