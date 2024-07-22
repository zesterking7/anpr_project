# urls.py

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from anpr_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('video_feed', views.video_feed, name='video_feed'),
    path('start_camera', views.start_camera, name='start_camera'),
    path('stop_camera', views.stop_camera, name='stop_camera'),
    path('plates/', views.plate_list, name='plate_list'),
    path('delete_plate/<int:plate_id>/', views.delete_plate, name='delete_plate'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
