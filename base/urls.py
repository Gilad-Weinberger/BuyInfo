from . import views
from django.urls import path

app_name = 'base'

urlpatterns = [
    path('', views.home, name="home"),
]
