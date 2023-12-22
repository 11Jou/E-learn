from django.contrib import admin
from django.urls import path , include
from home import views
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import handler404
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index , name='index'),
    path('messages', views.view_message , name='view_mesasges'),
    path('register/', include('register.urls')),
    path('instructor/', include('instructor.urls')),
    path('course_view/', include('course_view.urls')),
    path('student/', include('student.urls'))
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

handler404 = 'project.views.handle_404'
