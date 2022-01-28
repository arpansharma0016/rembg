from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('upload', views.upload, name="upload"),
    path('detach/<int:id>', views.detach, name="detach"),
    path('detachhd/<int:id>', views.detachhd, name="detachhd"),
]