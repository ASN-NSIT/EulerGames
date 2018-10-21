from django.urls import path
from . import views

urlpatterns = [
    path('', view=views.index, name='index'),
    path('start', view=views.start, name='start'),
    path('finish', view=views.finish, name='finish'),
    path('register', view=views.register, name='register'),
    path('leaderboard', view=views.leaderboard, name='leaderboard'),
    path('q/<num>', view=views.question_detail, name='question_detail')
]
