from django.conf.urls import url

from weather import views

urlpatterns = [
    url(r'process', views.process),
    url(r'test', views.weather_test),
]