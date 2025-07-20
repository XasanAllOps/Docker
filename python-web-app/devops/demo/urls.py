from django.urls import path
from . import views

urlpatterns = [
    path('', views.demo, name='demo'),  # points to demo/views.index
]
