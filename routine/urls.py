from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url

from routine import views

urlpatterns = [
    url(r'test', views.test),
    url(r'upload/(?P<user_id>\w{0,500})$', views.upload),
    url(r'find_all', views.find_all),
    url(r'remove/(?P<pk>\w{0,500})$', views.remove),
    url(r'reject/(?P<id>\w{0,500})$', views.reject_routine),
    # url(r'make_routine/(?P<user_id>\w{0,500})$', views.make_routine),
    url(r'today_top10/(?P<user_id>\w{0,500})$', views.today_top10),
    # url(r'modify', views.modify),
    # url(r'find/(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})$', views.find),
]