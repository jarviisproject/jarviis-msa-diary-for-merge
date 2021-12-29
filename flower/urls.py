from django.conf.urls import url

from flower import views

urlpatterns = [
    url(r'test', views.test),
    url(r'list/(?P<user_id>\w{0,500})$', views.list_by_id),
]