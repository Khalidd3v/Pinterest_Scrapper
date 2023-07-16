from django.urls import path
from . import views

urlpatterns = [

        path('', views.home, name='home'),
        path('download/', views.download_video, name='download_video'),

]
