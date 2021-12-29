from django.conf.urls import url, re_path
from django.urls import path, re_path

from userlog import views

urlpatterns = [
    url(r'process', views.process),
    url(r'upload', views.upload),
    url(r'test', views.test),
    url(r'modify', views.modify),
    url(r'remove/(?P<pk>\w{0,500})$', views.remove),
    url(r'create', views.create),
    url(r'list/(?P<user_id>\w{0,500})/(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})$', views.list_by_date),
    url(r'list', views.list),
    url(r'search/(?P<keyword>[ㄱ-힣]{1,500})$', views.search),
]