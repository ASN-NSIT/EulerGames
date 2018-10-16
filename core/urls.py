from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', view=views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('q/<id>', view=views.question_detail, name='question_detail')

]
