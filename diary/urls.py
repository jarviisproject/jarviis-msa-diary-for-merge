from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url

from diary import views

urlpatterns = [
    url(r'process', views.process),
    url(r'upload/(?P<user_id>\w{0,500})$', views.upload),
    url(r'find/(?P<user_id>\w{0,500})/(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})$', views.find),
    url(r'memo', views.modify_memo),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)