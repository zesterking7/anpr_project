from django.contrib import admin
from django.urls import path
from anpr_app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('video_feed', views.video_feed, name='video_feed'),
    path('plates/', views.plate_list, name='plate_list'),
    path('delete_plate/<int:plate_id>/', views.delete_plate, name='delete_plate'),
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
