from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', view=views.index, name='index'),
    path('q/<id>', view=views.question_detail, name='question_detail')
]
