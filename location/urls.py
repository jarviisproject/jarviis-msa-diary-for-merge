from django.conf.urls import url

from location import views

urlpatterns = [
    url(r'getLatLng', views.getLatLng),
]